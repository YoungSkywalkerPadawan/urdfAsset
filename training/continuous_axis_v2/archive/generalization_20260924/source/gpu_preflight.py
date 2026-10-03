"""Run only after the user enables GPU: measure a real training step's memory."""
import argparse
import contextlib
import time
import torch
from torch.utils.data._utils.collate import default_collate

from common import config_from, save_json
from model import PairAxisNet, axis_loss
from train import make_dataset, move, verify_snapshot


def profile(config, output):
    if not torch.cuda.is_available():
        raise RuntimeError('Enable GPU first; no GPU work was started')
    verify_snapshot(config['prepared_dir'], config['cache_root'])
    torch.set_num_threads(config.get('cpu_threads', 4))
    device = torch.device('cuda')
    torch.cuda.reset_peak_memory_stats()
    data = make_dataset(config, 'train', True)
    batch = move(default_collate([data[i % len(data)] for i in range(config['batch_size'])]), device)
    model = PairAxisNet(**config['model']).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config['learning_rate'])
    amp = config.get('amp', True) and torch.cuda.is_bf16_supported()
    started = time.monotonic()
    for _ in range(3):
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast('cuda', dtype=torch.bfloat16) if amp else contextlib.nullcontext():
            prediction = model(batch['parent'], batch['child'])
        loss, _ = axis_loss(prediction, batch, **config['loss'])
        if not torch.isfinite(loss):
            raise ValueError('Nonfinite GPU loss')
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), config['gradient_clip'])
        if not torch.isfinite(norm):
            raise ValueError('Nonfinite GPU gradient')
        optimizer.step()
    torch.cuda.synchronize()
    report = dict(gpu=torch.cuda.get_device_name(), total_vram_bytes=torch.cuda.get_device_properties(0).total_memory,
                  batch_size=config['batch_size'], points_per_part=config['points'], amp_bfloat16=amp,
                  peak_allocated_bytes=torch.cuda.max_memory_allocated(), peak_reserved_bytes=torch.cuda.max_memory_reserved(),
                  three_steps_seconds=time.monotonic() - started, finite_forward_backward=True,
                  checkpoint_saved=False, not_a_quality_benchmark=True)
    save_json(output, report)
    print(report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    profile(config_from(args.config), args.output)
