"""Explicit held-out evaluation using checkpoint preprocessing and architecture."""
import argparse
from pathlib import Path
import torch

from common import config_from, save_json, verify_checkpoint_code, write_rows
from model import PairAxisNet
from train import evaluate, make_dataset, verify_snapshot


def evaluate_checkpoint(config, checkpoint, split, output, device_name='cuda', allow_smoke=False):
    device = torch.device(device_name)
    state = torch.load(checkpoint, map_location=device, weights_only=True)
    verify_checkpoint_code(state)
    if state.get('smoke_only') and not allow_smoke:
        raise ValueError('Smoke checkpoint is not a trained model')
    if verify_snapshot(config['prepared_dir'], config['cache_root'])['snapshot_sha256'] != state['snapshot_sha256']:
        raise ValueError('Split mismatch')
    # A supplied configuration locates data and controls workers only. The saved
    # training configuration defines every model and preprocessing choice.
    resolved = dict(state['config'])
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError('Evaluation output already exists; choose a new directory')
    for key in ('prepared_dir', 'cache_root', 'workers', 'cpu_threads', 'batch_size'):
        resolved[key] = config[key]
    torch.set_num_threads(resolved.get('cpu_threads', 4))
    model = PairAxisNet(**resolved['model']).to(device)
    model.load_state_dict(state['model'])
    report, rows = evaluate(model, make_dataset(resolved, split), resolved, device)
    output.mkdir(parents=True, exist_ok=True)
    save_json(output / 'metrics.json', dict(split=split, checkpoint=str(checkpoint),
              smoke_only=state.get('smoke_only', False), **report))
    write_rows(output / 'predictions.jsonl', rows)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--split', choices=['val', 'test'], default='test')
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cuda')
    parser.add_argument('--output', required=True)
    parser.add_argument('--allow-smoke-checkpoint', action='store_true')
    args = parser.parse_args()
    report = evaluate_checkpoint(config_from(args.config), args.checkpoint, args.split,
                                 args.output, args.device, args.allow_smoke_checkpoint)
    print(report)
