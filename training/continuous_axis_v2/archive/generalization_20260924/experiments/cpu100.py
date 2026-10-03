"""CPU-only fixed-input fitting ablation. Never reads the held-out test split.

Export sampled tensors on the cache host; benchmark/train on any CPU host with
the identical original source. Experimental heads do not modify model.py.
"""
import argparse
import collections
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time

import numpy as np
import torch
from torch.utils.data._utils.collate import default_collate


def digest(path):
    with open(path, 'rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def save(path, obj):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    tmp.replace(path)


def main(a):
    torch.set_num_threads(a.threads)
    sys.path.insert(0, str(a.source.resolve()))
    from model import PairAxisNet, axis_loss, axis_metrics, canonical_origin, unit_direction, vector_huber
    from train import seed_all, make_dataset, verify_snapshot
    a.output.mkdir(parents=True, exist_ok=True)
    if any(a.output.iterdir()):
        raise ValueError('Use a new, empty output directory')
    started = time.monotonic()

    def log(obj):
        obj = dict(obj, wall_seconds=round(time.monotonic() - started, 2))
        with (a.output / 'progress.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(obj, allow_nan=False) + '\n')
        save(a.output / 'status.json', obj)
        print(json.dumps(obj, allow_nan=False), flush=True)

    if a.mode == 'export':
        cfg = json.loads((a.run / 'run_config.json').read_text())['config']
        cfg.update(prepared_dir=str(a.prepared), cache_root=str(a.cache), workers=0)
        ready = verify_snapshot(a.prepared, a.cache)
        data = make_dataset(cfg, 'train', False)
        sources = {s: [] for s in sorted({r['source'] for r in data.rows})}
        for i, row in enumerate(data.rows):
            sources[row['source']].append(i)
        rng = np.random.default_rng(a.seed)
        for indices in sources.values():
            rng.shuffle(indices)
        selected, seen = [], set()
        while len(selected) < a.samples:
            before = len(selected)
            for indices in sources.values():
                while indices:
                    i = indices.pop()
                    asset = data.rows[i]['asset_key']
                    if asset not in seen:
                        seen.add(asset)
                        selected.append(i)
                        break
                if len(selected) == a.samples:
                    break
            if before == len(selected):
                raise ValueError('Not enough distinct training assets')
        rows = [data.rows[i] for i in selected]
        manifest = json.loads((a.cache / 'cache_manifest.json').read_text())
        hashes = {m['path']: m['sha256'] for m in manifest.values()}
        files = {r[key] for r in rows for key in ('parent_file', 'child_file')}
        for relative in files:
            assert digest(a.cache / relative) == hashes[relative], relative
        fixed = default_collate([data[i] for i in selected])
        assert all(torch.is_tensor(v) and torch.isfinite(v).all() for v in fixed.values())
        assert len(fixed['parent']) == a.samples
        torch.save(fixed, a.output / 'fixed_inputs.pt')
        metadata = dict(config=cfg, rows=rows, snapshot_sha256=ready['snapshot_sha256'],
            source_hashes={p.name: digest(p) for p in a.source.glob('*.py')},
            tensor_sha256=digest(a.output / 'fixed_inputs.pt'), selection_seed=a.seed,
            sources=dict(collections.Counter(r['source'] for r in rows)), distinct_assets=len(seen),
            hash_verified_files=len(files), shapes={k:list(v.shape) for k,v in fixed.items()},
            note='100 distinct train assets, one axis each; metadata/hash checked, not newly human-verified. No augmentation.')
        save(a.output / 'inputs.json', metadata)
        log(dict(event='export_complete', samples=len(rows), sources=metadata['sources'], bytes=(a.output/'fixed_inputs.pt').stat().st_size))
        return

    meta = json.loads((a.inputs / 'inputs.json').read_text(encoding='utf-8'))
    assert digest(a.inputs / 'fixed_inputs.pt') == meta['tensor_sha256']
    for name in ('model.py', 'data_geometry.py'):
        assert digest(a.source / name) == meta['source_hashes'][name], name
    fixed = torch.load(a.inputs / 'fixed_inputs.pt', map_location='cpu', weights_only=True)
    assert all(v.device.type == 'cpu' for v in fixed.values())
    count = len(fixed['parent'])
    cfg = copy.deepcopy(meta['config'])
    cfg['model']['dropout'] = 0.
    seed_all(a.seed)
    net = PairAxisNet(**cfg['model']).cpu()
    initial = copy.deepcopy(net.state_dict())
    save(a.output/'identity.json', dict(mode=a.mode, torch=torch.__version__, device='cpu', threads=a.threads,
        cpu_count=os.cpu_count(), seed=a.seed, epochs=a.epochs, batch_size=a.batch_size, learning_rate=a.lr,
        scheduler='cosine to 0.1*initial LR', gradient_clip=a.clip, weight_decay=0., dropout=0., augmentation=False,
        variants=a.variants, parameter_count=sum(p.numel() for p in net.parameters()), samples=count,
        input_sha256=meta['tensor_sha256'], script_sha256=digest(__file__), source_hashes=meta['source_hashes'],
        cfg=cfg, note='Training fit only. No validation/test evaluation. Best selected on these same training inputs.'))

    # Capture the raw residual to bypass ONLY the original direction-dependent
    # constraint, without copying or editing the original model implementation.
    raw = {}
    def capture(module, inputs, output):
        raw['offset'] = output
    hook = net.projection_head.register_forward_hook(capture)

    def forward(batch, variant):
        pred = net(batch['parent'], batch['child'])
        offset = raw.pop('offset')
        if variant != 'baseline':
            points = batch['child'][..., :3] + offset.float()
            pred = dict(direction=pred['direction'], projection_points=points,
                        origin=canonical_origin(points.mean(1), pred['direction']))
        return pred

    def loss_fn(pred, batch, variant):
        if variant == 'baseline':
            return axis_loss(pred, batch, **cfg['loss'])
        d, g = unit_direction(pred['direction']), unit_direction(batch['direction'])
        dot = (d*g).sum(-1).clamp(-1, 1)
        if variant == 'free_sin2':
            direction = (1-dot.square()).mean()
        else:
            signed = torch.where((dot.detach() >= 0)[:, None], g, -g)
            direction = ((d-signed)**2).sum(-1).mean()
        projection = vector_huber(pred['projection_points']-batch['projection_target']).mean()
        return direction + projection, dict(direction_loss=direction, projection_loss=projection)

    def batch_at(indices):
        return {k:v[indices] for k,v in fixed.items()}

    # Check labels and the experimental computation graph before optimization.
    probe = batch_at(slice(0, a.batch_size))
    net.eval()
    original = net(probe['parent'], probe['child'])
    raw.clear()
    baseline = forward(probe, 'baseline')
    assert all(torch.equal(original[k], baseline[k]) for k in original)
    free = forward(probe, 'free_sin2')
    projection_only = vector_huber(free['projection_points']-probe['projection_target']).mean()
    dependency = torch.autograd.grad(projection_only, free['direction'], allow_unused=True)[0]
    assert dependency is None, 'Free projection supervision must not depend on predicted direction'
    target_pred = dict(origin=probe['origin'], direction=probe['direction'], projection_points=probe['projection_target'])
    assert axis_metrics(target_pred, probe)['success_5deg_1pct'].sum() == len(probe['parent'])
    assert float(loss_fn(target_pred, probe, 'free_sin2')[0]) < 1e-5
    save(a.output/'preflight.json', dict(baseline_unchanged=True, free_projection_decoupled=True,
        ground_truth_metrics_pass=True, input_hash_pass=True, original_model_hash_pass=True, device='cpu'))
    del original, baseline, free, projection_only, probe
    net.train()

    @torch.no_grad()
    def evaluate(variant):
        net.eval()
        chunks, totals, parts_sum, predicted = {}, [], {}, []
        for begin in range(0, count, a.batch_size):
            batch = batch_at(slice(begin, begin+a.batch_size))
            pred = forward(batch, variant)
            loss, parts = loss_fn(pred, batch, variant)
            n = len(batch['parent'])
            totals.extend([float(loss)] * n)
            for key, value in parts.items():
                parts_sum[key] = parts_sum.get(key, 0.) + float(value)*n
            for key, value in axis_metrics(pred, batch).items():
                chunks.setdefault(key, []).append(value)
            predicted.extend([dict(origin=o.tolist(), direction=d.tolist()) for o,d in zip(pred['origin'],pred['direction'])])
        metrics = {k:torch.cat(v) for k,v in chunks.items()}
        angle, offset = metrics['angle_deg'], metrics['origin_to_axis_normalized']
        rows = [dict(id=row['id'], asset_key=row['asset_key'], source=row['source'],
            **{k:float(v[i]) for k,v in metrics.items()}, **predicted[i]) for i,row in enumerate(meta['rows'])]
        result = dict(loss=float(np.mean(totals)), components={k:v/count for k,v in parts_sum.items()},
            mean_angle=float(angle.mean()), median_angle=float(angle.median()), max_angle=float(angle.max()),
            mean_offset=float(offset.mean()), median_offset=float(offset.median()), max_offset=float(offset.max()),
            strict_count=int(((angle<=5)&(offset<=.01)).sum()),
            loose_count=int(((angle<=10)&(offset<=.02)).sum()),
            direction_pass=int((angle<=5).sum()), position_pass=int((offset<=.01).sum()), samples=count)
        result['by_source'] = {}
        for source in meta['sources']:
            subset=[r for r in rows if r['source']==source]
            result['by_source'][source] = dict(samples=len(subset), strict_count=sum(r['success_5deg_1pct'] for r in subset),
                mean_angle=float(np.mean([r['angle_deg'] for r in subset])),
                mean_offset=float(np.mean([r['origin_to_axis_normalized'] for r in subset])))
        net.train()
        return result, rows

    if a.mode == 'benchmark':
        batch = batch_at(slice(0, a.batch_size))
        opt = torch.optim.AdamW(net.parameters(), lr=a.lr, weight_decay=0.)
        timing = []
        for step in range(8):
            t = time.monotonic()
            opt.zero_grad(set_to_none=True)
            pred = forward(batch, 'free_sin2')
            loss, _ = loss_fn(pred, batch, 'free_sin2')
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), a.clip)
            opt.step()
            timing.append(time.monotonic()-t)
        log(dict(event='benchmark_complete', seconds=timing, steady_median=float(np.median(timing[2:]))))
        hook.remove()
        return

    summaries = {}
    for variant in a.variants:
        seed_all(a.seed)
        net.load_state_dict(initial)
        net.train()
        opt = torch.optim.AdamW(net.parameters(), lr=a.lr, weight_decay=0.)
        schedule = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=a.epochs, eta_min=a.lr*.1)
        best_key = None
        stable_passes = 0
        history = []
        update = 0
        for epoch in range(a.epochs+1):
            if epoch % a.eval_every == 0 or epoch == a.epochs:
                result, rows = evaluate(variant)
                result.update(event='evaluation', variant=variant, epoch=epoch, updates=update,
                              learning_rate=opt.param_groups[0]['lr'])
                history.append(result)
                log(result)
                score = (result['strict_count'], -(result['mean_angle']/5 + result['mean_offset']/.01))
                state = dict(model=net.state_dict(), optimizer=opt.state_dict(), scheduler=schedule.state_dict(),
                    variant=variant, epoch=epoch, result=result, config=cfg, input_sha256=meta['tensor_sha256'])
                torch.save(state, a.output/f'{variant}_last.pt')
                save(a.output/f'{variant}_last_predictions.json', rows)
                if best_key is None or score > best_key:
                    best_key=score
                    torch.save(state, a.output/f'{variant}_best.pt')
                    save(a.output/f'{variant}_best_predictions.json', rows)
                    save(a.output/f'{variant}_best_metrics.json', result)
                stable_passes = stable_passes+1 if result['strict_count']==count else 0
                if stable_passes >= 3:
                    log(dict(event='early_stop_all_fit', variant=variant, epoch=epoch))
                    break
            if epoch == a.epochs:
                break
            # Same random permutation every corresponding epoch across variants;
            # every sample is used once per epoch, no balanced resampling.
            generator = torch.Generator().manual_seed(a.seed+epoch)
            order = torch.randperm(count, generator=generator)
            for begin in range(0, count, a.batch_size):
                batch = batch_at(order[begin:begin+a.batch_size])
                opt.zero_grad(set_to_none=True)
                pred = forward(batch, variant)
                loss, parts = loss_fn(pred, batch, variant)
                if not torch.isfinite(loss):
                    raise ValueError('Non-finite loss')
                loss.backward()
                norm = torch.nn.utils.clip_grad_norm_(net.parameters(), a.clip)
                if not torch.isfinite(norm):
                    raise ValueError('Non-finite gradient')
                opt.step()
                update+=1
                if update % a.log_every == 0:
                    log(dict(event='update', variant=variant, epoch=epoch+1, update=update,
                        batch_loss=float(loss.detach()), gradient_norm=float(norm)))
            schedule.step()
        summaries[variant]=history
        save(a.output/'summary.json', summaries)
    hook.remove()
    log(dict(event='complete', variants=a.variants, samples=count))


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--mode', choices=['export','benchmark','train'], required=True)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--inputs', type=Path)
    p.add_argument('--prepared', type=Path)
    p.add_argument('--cache', type=Path)
    p.add_argument('--run', type=Path)
    p.add_argument('--samples', type=int, default=100)
    p.add_argument('--seed', type=int, default=20260923)
    p.add_argument('--threads', type=int, default=1)
    p.add_argument('--batch-size', type=int, default=4)
    p.add_argument('--epochs', type=int, default=120)
    p.add_argument('--lr', type=float, default=3e-4)
    p.add_argument('--clip', type=float, default=1.)
    p.add_argument('--eval-every', type=int, default=5)
    p.add_argument('--log-every', type=int, default=25)
    p.add_argument('--variants', nargs='+', choices=['baseline','free_sin2','free_chordal'], default=['baseline','free_sin2','free_chordal'])
    main(p.parse_args())
