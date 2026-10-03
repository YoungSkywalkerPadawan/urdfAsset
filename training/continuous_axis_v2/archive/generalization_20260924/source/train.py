"""Single-GPU training, family-balanced validation, and strict resumability."""
import argparse
import collections
import contextlib
import json
from pathlib import Path
import random
import time

import numpy as np
import torch
from torch.utils.data import DataLoader

from common import code_digest, config_from, digest, read_json, save_json, write_rows
from dataset import AxisDataset, BalancedDraws
from model import PairAxisNet, axis_loss, axis_metrics


def seed_all(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def move(batch, device):
    return {key: value.to(device, non_blocking=True) if torch.is_tensor(value) else value
            for key, value in batch.items()}


def make_dataset(config, split, augment=False):
    return AxisDataset(config['prepared_dir'], split, config['points'], config['seed'],
                       augment, augment and config['auxiliary_fraction'] > 0,
                       config['jitter'], config['normal_dropout'],
                       cache_root=config['cache_root'], local_fraction=config.get('local_fraction', 0.0))


def loader(data, config, train=False, epoch=0):
    data.epoch = epoch
    sampler = BalancedDraws(data.rows, config['epoch_samples'], config['seed'], epoch,
                            config['auxiliary_fraction']) if train else None
    return DataLoader(data, batch_size=config['batch_size'], sampler=sampler, shuffle=False,
                      num_workers=config['workers'], pin_memory=torch.cuda.is_available(),
                      persistent_workers=False, drop_last=False,
                      generator=torch.Generator().manual_seed(config['seed'] + epoch))


def summarize(predictions):
    if not predictions:
        raise ValueError('No evaluation samples')
    fields = [key for key in ('angle_deg', 'origin_to_axis_normalized', 'origin_to_axis_m',
              'canonical_origin_normalized', 'success_5deg_1pct', 'motion_error_normalized')
              if key in predictions[0]]

    def mean(items):
        return {field: float(np.mean([item[field] for item in items])) for field in fields}

    by_asset = collections.defaultdict(list)
    for row in predictions:
        by_asset[(row['source'], row['group'], row['asset_key'])].append(row)
    per_asset = {key: mean(rows) for key, rows in by_asset.items()}
    by_group = collections.defaultdict(list)
    for (source, group, _), metrics in per_asset.items():
        by_group[(source, group)].append(metrics)
    per_group = {key: mean(rows) for key, rows in by_group.items()}
    by_source = {}
    for source in sorted({key[0] for key in per_asset}):
        assets = [value for key, value in per_asset.items() if key[0] == source]
        groups = [value for key, value in per_group.items() if key[0] == source]
        by_source[source] = dict(assets=len(assets), groups=len(groups),
            pairs=sum(row['source'] == source for row in predictions),
            macro_asset=mean(assets), macro_group=mean(groups))
    macro = mean([value['macro_group'] for value in by_source.values()])
    return dict(pairs=len(predictions), assets=len(per_asset), groups=len(per_group),
                micro=mean(predictions), macro_asset=mean(list(per_asset.values())),
                macro_group=mean(list(per_group.values())), by_source=by_source,
                macro_source_group=macro,
                selection_score=macro['angle_deg'] / 5 + macro['origin_to_axis_normalized'] / 0.01,
                position_normalization='child robust bounding-box diagonal',
                per_asset=[dict(source=k[0], group=k[1], asset_key=k[2], **v) for k, v in per_asset.items()])


@torch.no_grad()
def evaluate(model, data, config, device, max_batches=None):
    model.eval()
    predictions = []
    for step, batch in enumerate(loader(data, config)):
        if max_batches is not None and step >= max_batches:
            break
        indices = batch['row_index'].tolist()
        batch = move(batch, device)
        result = model(batch['parent'], batch['child'])
        metrics = axis_metrics(result, batch)
        origins = (result['origin'] * batch['scale'][:, None] + batch['center']).cpu().tolist()
        directions = result['direction'].cpu().tolist()
        for index, row_index in enumerate(indices):
            row = data.rows[row_index]
            predictions.append(dict(id=row['id'], asset_key=row['asset_key'], source=row['source'],
                group=row['group'], joint_name=row['joint_name'], private=row['private'],
                predicted_origin_world=origins[index], predicted_direction_world=directions[index],
                **{key: float(value[index].cpu()) for key, value in metrics.items()}))
    return summarize(predictions), predictions


def atomic_checkpoint(path, state):
    path = Path(path)
    temporary = path.with_suffix('.partial')
    torch.save(state, temporary)
    temporary.replace(path)


def verify_snapshot(prepared, cache_root=None):
    ready = read_json(Path(prepared) / 'READY.json')
    if ready.get('schema_version') != 2:
        raise ValueError('This trainer requires a derived v2 snapshot')
    if ready.get('geometry_code_sha256') != digest(Path(__file__).with_name('data_geometry.py')):
        raise ValueError('Geometry preprocessing changed; derive a new snapshot first')
    for name, expected in ready['files'].items():
        if digest(Path(prepared) / name) != expected:
            raise ValueError('Prepared split/index changed: ' + name)
    if cache_root is not None:
        if digest(Path(cache_root) / 'cache_manifest.json') != ready['cache_manifest_sha256']:
            raise ValueError('cache_root does not match the frozen point-cache manifest')
    return ready


RESUME_FIELDS = ('model', 'loss', 'points', 'seed', 'auxiliary_fraction', 'epochs',
                 'learning_rate', 'weight_decay', 'epoch_samples', 'batch_size',
                 'jitter', 'normal_dropout', 'local_fraction', 'gradient_clip', 'amp')


def run(config, device_name='cuda', resume=None, max_batches=None, max_epochs=None, output_override=None):
    seed_all(config['seed'])
    torch.set_num_threads(config.get('cpu_threads', 4))
    if device_name == 'cuda' and not torch.cuda.is_available():
        raise RuntimeError('CUDA unavailable; no training started. Enable the GPU first.')
    if any(value is not None and value <= 0 for value in (max_batches, max_epochs)):
        raise ValueError('Smoke limits must be positive')
    log_interval = config.get('log_interval', 32)
    if not isinstance(log_interval, int) or log_interval < 1:
        raise ValueError('log_interval must be a positive integer')
    device = torch.device(device_name)
    ready = verify_snapshot(config['prepared_dir'], config['cache_root'])
    output = Path(output_override or config['run_dir'])
    if output.exists() and any(output.iterdir()) and not resume:
        raise ValueError('Run directory is not empty; use --resume or a new --output')
    if output.exists() and any(output.iterdir()) and resume:
        if Path(resume).resolve() != (output / 'last.pt').resolve():
            raise ValueError('A nonempty run can only resume its own last.pt; use a new output to branch')
    smoke = max_batches is not None or max_epochs is not None
    source_hash = code_digest()
    state = None
    if resume:
        state = torch.load(resume, map_location=device, weights_only=True)
        if state['snapshot_sha256'] != ready['snapshot_sha256']:
            raise ValueError('Resume split snapshot mismatch')
        if state['code_sha256'] != source_hash:
            raise ValueError('Resume source code changed; keep the original code or start a new run')
        for field in RESUME_FIELDS:
            if state['config'].get(field) != config.get(field):
                raise ValueError('Resume configuration mismatch: ' + field)
        if output.exists() and any(output.iterdir()):
            recorded = read_json(output / 'run_config.json')
            if recorded['code_sha256'] != source_hash or recorded['prepared_snapshot']['snapshot_sha256'] != ready['snapshot_sha256']:
                raise ValueError('Existing output belongs to another code/data snapshot')
            for field in RESUME_FIELDS:
                if recorded['config'].get(field) != config.get(field):
                    raise ValueError('Existing output configuration mismatch: ' + field)
            metric_file = output / 'metrics.jsonl'
            if metric_file.exists():
                last_report = json.loads(metric_file.read_text('utf-8').strip().splitlines()[-1])
                if last_report['epoch'] != state['epoch']:
                    raise ValueError('Metrics and checkpoint epochs disagree; resume into a new output for recovery')
        if state.get('smoke_only', False) != smoke:
            raise ValueError('Smoke and production checkpoints must not be mixed')
    train_data = make_dataset(config, 'train', True)
    val_data = make_dataset(config, 'val')
    if not len(train_data) or not len(val_data):
        raise ValueError('Training and validation need nonempty grouped splits')
    model = PairAxisNet(**config['model']).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config['learning_rate'], weight_decay=config['weight_decay'])
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=config['epochs'],
                                                          eta_min=config['learning_rate'] * 0.05)
    use_amp = config.get('amp', True) and device.type == 'cuda' and torch.cuda.is_bf16_supported()
    start, best = 0, float('inf')
    if state:
        model.load_state_dict(state['model'])
        optimizer.load_state_dict(state['optimizer'])
        scheduler.load_state_dict(state['scheduler'])
        start, best = state['epoch'] + 1, state['best_score']
        torch.set_rng_state(state['torch_rng'].cpu())
        if device.type == 'cuda' and state.get('cuda_rng'):
            torch.cuda.set_rng_state_all([value.cpu() for value in state['cuda_rng']])
    stop = min(config['epochs'], start + max_epochs) if max_epochs is not None else config['epochs']
    if start >= stop:
        raise ValueError('Checkpoint has already reached the requested epoch count')
    output.mkdir(parents=True, exist_ok=True)
    save_json(output / 'run_config.json', dict(config=config, device=str(device), smoke_only=smoke,
              prepared_snapshot=ready, code_sha256=source_hash))
    print(json.dumps(dict(parameters=sum(p.numel() for p in model.parameters()), train_pairs=len(train_data),
                          val_pairs=len(val_data), device=str(device), amp_bfloat16=use_amp)), flush=True)
    if device.type == 'cuda':
        torch.cuda.reset_peak_memory_stats(device)
    for epoch in range(start, stop):
        started = time.monotonic()
        model.train()
        total, count = 0.0, 0
        components = collections.Counter()
        window_total, window_count = 0.0, 0
        window_components = collections.Counter()
        train_loader = loader(train_data, config, True, epoch)
        planned_steps = min(len(train_loader), max_batches) if max_batches is not None else len(train_loader)
        for step, batch in enumerate(train_loader):
            if max_batches is not None and step >= max_batches:
                break
            batch = move(batch, device)
            optimizer.zero_grad(set_to_none=True)
            amp = torch.autocast(device_type='cuda', dtype=torch.bfloat16) if use_amp else contextlib.nullcontext()
            with amp:
                prediction = model(batch['parent'], batch['child'])
            loss, losses = axis_loss(prediction, batch, **config['loss'])
            if not torch.isfinite(loss):
                raise ValueError('Nonfinite training loss')
            loss.backward()
            norm = torch.nn.utils.clip_grad_norm_(model.parameters(), config['gradient_clip'])
            if not torch.isfinite(norm):
                raise ValueError('Nonfinite gradient')
            optimizer.step()
            size = len(batch['parent'])
            batch_loss = float(loss.detach())
            total += batch_loss * size
            count += size
            window_total += batch_loss * size
            window_count += size
            for key, value in losses.items():
                weighted_value = float(value.detach()) * size
                components[key] += weighted_value
                window_components[key] += weighted_value
            if (step + 1) % log_interval == 0 or step + 1 == planned_steps:
                elapsed = time.monotonic() - started
                progress = dict(event='train_progress', epoch=epoch + 1, epoch_index=epoch,
                    total_epochs=config['epochs'], step=step + 1, steps_per_epoch=planned_steps,
                    global_step=epoch * len(train_loader) + step + 1,
                    batch_loss=batch_loss, window_mean_loss=window_total / window_count,
                    epoch_mean_loss=total / count,
                    loss_components={key: value / window_count for key, value in window_components.items()},
                    learning_rate=optimizer.param_groups[0]['lr'], gradient_norm=float(norm.detach()),
                    epoch_elapsed_seconds=elapsed,
                    remaining_train_seconds_in_epoch=elapsed / (step + 1) * (planned_steps - step - 1),
                    smoke_only=smoke)
                with (output / 'progress.jsonl').open('a', encoding='utf-8') as stream:
                    stream.write(json.dumps(progress, allow_nan=False) + '\n')
                print(json.dumps(progress, allow_nan=False), flush=True)
                window_total, window_count = 0.0, 0
                window_components.clear()
        if not count:
            raise ValueError('No training batches')
        validation, predictions = evaluate(model, val_data, config, device, max_batches)
        scheduler.step()
        score = validation['selection_score']
        improved = score < best
        best = min(best, score)
        report = dict(epoch=epoch, train_loss=total / count,
                      loss_components={key: value / count for key, value in components.items()},
                      seconds=time.monotonic() - started, validation=validation, smoke_only=smoke,
                      peak_cuda_allocated_bytes=torch.cuda.max_memory_allocated(device) if device.type == 'cuda' else None)
        with (output / 'metrics.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(report, allow_nan=False) + '\n')
        checkpoint = dict(model=model.state_dict(), optimizer=optimizer.state_dict(), scheduler=scheduler.state_dict(),
                          config=config, epoch=epoch, best_score=best, snapshot_sha256=ready['snapshot_sha256'],
                          code_sha256=source_hash, torch_rng=torch.get_rng_state(),
                          cuda_rng=torch.cuda.get_rng_state_all() if device.type == 'cuda' else [], smoke_only=smoke)
        atomic_checkpoint(output / 'last.pt', checkpoint)
        if improved:
            atomic_checkpoint(output / 'best.pt', checkpoint)
            save_json(output / 'best_validation.json', validation)
            write_rows(output / 'best_val_predictions.jsonl', predictions)
        print(json.dumps(dict(event='epoch_complete', epoch=epoch + 1, epoch_index=epoch,
                              total_epochs=config['epochs'], train_loss=report['train_loss'],
                              loss_components=report['loss_components'], validation_score=score,
                              validation_macro=validation['macro_source_group'],
                              seconds=report['seconds'], improved=improved, best_score=best,
                              smoke_only=smoke)), flush=True)
    save_json(output / 'status.json', dict(completed=True, smoke_only=smoke, epochs_completed=stop, test_evaluated=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cuda')
    parser.add_argument('--resume')
    parser.add_argument('--max-batches', type=int)
    parser.add_argument('--max-epochs', type=int)
    parser.add_argument('--output')
    args = parser.parse_args()
    run(config_from(args.config), args.device, args.resume, args.max_batches, args.max_epochs, args.output)
