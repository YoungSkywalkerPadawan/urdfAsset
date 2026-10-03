"""CPU-only checks of geometry, data isolation, model gradients and deployment."""
import argparse
import collections
import copy
from pathlib import Path
import time

import numpy as np
import torch
from torch.utils.data._utils.collate import default_collate

from common import config_from, digest, read_json, read_rows, save_json
from data_geometry import child_frame, normalize_pair, sample_pair
from dataset import BalancedDraws
from infer_glb import predict_glb
from model import PairAxisNet, axis_loss, axis_metrics, axis_projection, rotate_points
from train import make_dataset, run, summarize, verify_snapshot


def mathematical_checks():
    points = torch.tensor([[[1., 0., 0.], [0., 1., 0.], [-1., 0., 0.], [0., -1., 0.]]])
    origin = torch.tensor([[0., 0., 0.]])
    direction = torch.tensor([[0., 0., 1.]])
    expected = torch.tensor([[[0., 1., 0.], [-1., 0., 0.], [0., -1., 0.], [1., 0., 0.]]])
    assert torch.allclose(rotate_points(points, origin, direction, [90.])[:, 0], expected, atol=1e-6)
    batch = dict(child=torch.cat((points, torch.zeros_like(points)), -1), origin=origin,
                 direction=direction, scale=torch.ones(1), projection_target=torch.zeros_like(points))
    perfect = dict(origin=origin, direction=direction, projection_points=torch.zeros_like(points))
    loss_options = dict(motion_weight=0.1)
    assert float(axis_loss(perfect, batch, **loss_options)[0]) < 1e-6
    flipped = dict(perfect, direction=-direction, origin=origin + 17 * direction)
    assert float(axis_loss(flipped, batch, **loss_options)[0]) < 1e-6
    assert float(axis_metrics(flipped, batch)['motion_error_normalized']) < 1e-6
    wrong = dict(perfect, origin=torch.tensor([[0.2, 0., 0.]]))
    metrics = axis_metrics(wrong, batch)
    assert torch.allclose(metrics['origin_to_axis_normalized'], torch.tensor([0.2]), atol=1e-6)
    assert float(metrics['motion_error_normalized']) > 0.1
    crossing = dict(perfect, direction=torch.tensor([[1., 0., 0.]]))
    assert float(axis_metrics(crossing, batch)['angle_deg']) == 90.
    assert float(axis_metrics(crossing, batch)['success_5deg_1pct']) == 0.
    # A dense projection is unchanged by either authored axis sign or any
    # authored origin shift along that axis; thin wheels may project to one point.
    assert torch.allclose(axis_projection(points, origin + direction * 9, -direction), torch.zeros_like(points))
    torch.manual_seed(15)
    q, _ = torch.linalg.qr(torch.randn(3, 3))
    if torch.linalg.det(q) < 0:
        q[:, 0] *= -1
    prediction = dict(origin=torch.tensor([[0.2, -0.1, 0.]]),
                      direction=torch.tensor([[0.1, 0.2, 0.97]]),
                      projection_points=torch.randn_like(points) * 0.1)
    rotated_prediction = {key: value @ q.T for key, value in prediction.items()}
    rotated_batch = dict(batch, child=batch['child'].clone(), origin=origin @ q.T,
                         direction=direction @ q.T, projection_target=batch['projection_target'] @ q.T)
    rotated_batch['child'][..., :3] = points @ q.T
    first = axis_loss(prediction, batch, **loss_options)[0]
    second = axis_loss(rotated_prediction, rotated_batch, **loss_options)[0]
    assert torch.allclose(first, second, atol=2e-5), (first, second)
    return dict(sign_and_origin_gauge=True, thin_wheel_projection=True, known_rodrigues_rotation=True,
                child_relative_offset=True, intersecting_wrong_axes_rejected=True, rotation_invariant_loss=True)


def sampling_checks():
    rows = []
    for group, asset_count in (('family_small', 1), ('family_large', 5)):
        for asset in range(asset_count):
            for joint in range(asset + 1):
                rows.append(dict(source='source', group=group, asset_key=f'{group}/{asset}', type='continuous'))
    sampler = BalancedDraws(rows, 100, 2, 0)
    mass = collections.Counter()
    for row, weight in zip(rows, sampler.weights):
        mass[row['group']] += weight
    assert abs(mass['family_small'] - mass['family_large']) < 1e-8, mass
    assert len(list(sampler)) == 100
    return dict(equal_family_mass=True, draw_count=True)


def check(config, output, skip_hashes=False, skip_full_model=False):
    started = time.monotonic()
    torch.set_num_threads(1)
    torch.manual_seed(3)
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use a new preflight output directory')
    output.mkdir(parents=True, exist_ok=True)
    ready = verify_snapshot(config['prepared_dir'], config['cache_root'])
    cache_root = Path(config['cache_root'])
    caches = read_json(Path(config['prepared_dir']) / 'cache_manifest.json')
    if not skip_hashes:
        for item in caches.values():
            if digest(cache_root / item['path']) != item['sha256']:
                raise AssertionError('Point cache checksum mismatch: ' + item['path'])
    print('CACHE_HASHES_OK', len(caches), flush=True)
    base_rows = {}
    groups, assets = {}, {}
    continuous = 0
    for split in ('train', 'val', 'test'):
        for kind in ('continuous', 'auxiliary'):
            for row in read_rows(Path(config['base_prepared_dir']) / f'{split}_{kind}.jsonl'):
                base_rows[row['id']] = row
            rows = read_rows(Path(config['prepared_dir']) / f'{split}_{kind}.jsonl')
            for row in rows:
                original = base_rows[row['id']]
                assert row['split'] == original['split'] == split
                assert row['group'] == original['group']
                assert groups.setdefault(row['group'], split) == split
                assert assets.setdefault(row['asset_key'], split) == split
                assert abs(np.dot(row['origin'], row['direction'])) < 1e-5
                assert row['scale'] > 0
            if kind == 'continuous':
                continuous += len(rows)
    lightweight = copy.deepcopy(config)
    lightweight.update(points=16, local_fraction=0.0)
    for split in ('train', 'val', 'test'):
        data = make_dataset(lightweight, split)
        for index in range(len(data)):
            sample = data[index]
            assert sample['parent'].shape == (16, 6)
            assert torch.isfinite(sample['parent']).all() and torch.isfinite(sample['child']).all()
            expected = axis_projection(sample['child'][None, :, :3], sample['origin'][None], sample['direction'][None])[0]
            assert torch.allclose(expected, sample['projection_target'], atol=2e-5)
    print('ALL_CONTINUOUS_INPUTS_OK', continuous, flush=True)
    data = make_dataset(lightweight, 'train')
    before = data[0]
    saved = copy.deepcopy(data.rows[0])
    data.rows[0]['origin'] = [42., 43., 44.]
    data.rows[0]['direction'] = [1., 0., 0.]
    after = data[0]
    assert torch.equal(before['parent'], after['parent']) and torch.equal(before['child'], after['child'])
    data.rows[0] = saved
    augmented = make_dataset(dict(lightweight, points=128, local_fraction=0.5), 'train', True)
    sample = augmented[0]
    expected = axis_projection(sample['child'][None, :, :3], sample['origin'][None], sample['direction'][None])[0]
    assert torch.allclose(sample['projection_target'], expected, atol=2e-5)
    geometry_report = mathematical_checks()
    sampling_report = sampling_checks()
    small = copy.deepcopy(config)
    small.update(points=128, batch_size=2, workers=0, cpu_threads=1, epoch_samples=4, epochs=2, amp=False)
    small['model'].update(width=32, tokens=8, neighbors=8, large_neighbors=24, layers=1, dropout=0., distance_chunk=64)
    batch = default_collate([make_dataset(small, 'train', True)[i] for i in (0, 1)])
    variants = {}
    for name, head, multiscale, motion in [('A', 'direct', False, 0.), ('B', 'projection', False, 0.),
                                          ('C', 'projection', True, 0.), ('D', 'projection', True, .1)]:
        kwargs = dict(small['model'], head=head, multiscale=multiscale)
        model = PairAxisNet(**kwargs)
        prediction = model(batch['parent'], batch['child'])
        loss, _ = axis_loss(prediction, batch, **dict(small['loss'], motion_weight=motion))
        loss.backward()
        assert torch.isfinite(loss)
        assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
        variants[name] = dict(finite_forward_backward=True, parameters=sum(p.numel() for p in model.parameters()))
    print('ALL_ABLATION_GRADIENTS_OK', flush=True)
    run(small, 'cpu', max_batches=2, max_epochs=1, output_override=output / 'smoke_run')
    run(small, 'cpu', resume=output / 'smoke_run/last.pt', max_batches=2, max_epochs=1, output_override=output / 'smoke_run')
    state = torch.load(output / 'smoke_run/last.pt', map_location='cpu', weights_only=True)
    assert state['epoch'] == 1 and state['smoke_only']
    mismatch = copy.deepcopy(small)
    mismatch['loss']['motion_weight'] += 0.01
    try:
        run(mismatch, 'cpu', resume=output / 'smoke_run/last.pt', max_batches=1, max_epochs=1,
            output_override=output / 'should_not_exist')
        raise AssertionError('Changed loss was accepted on resume')
    except ValueError as error:
        assert 'configuration mismatch' in str(error)
    # Only use the validation split to exercise the caller-provided GLB path.
    row = next(row for row in read_rows(Path(config['prepared_dir']) / 'val_continuous.jsonl') if row['private'])
    root = next(Path(source['path']) for source in config['data_roots'] if source.get('private'))
    folder = root / 'assets' / row['asset_id']
    joint = read_json(folder / 'joints.json')['joints'][row['joint_index']]
    pairs = [dict(name='cpu_pipeline_check', type='continuous', parent_nodes=[joint['parent']], child_nodes=[joint['child']])]
    predict_glb(folder / 'scene.glb', pairs, output / 'smoke_run/last.pt', output / 'smoke_prediction.json',
                'cpu', allow_smoke=True)
    result = read_json(output / 'smoke_prediction.json')['joints'][0]
    assert np.isfinite(result['origin_world_m']).all()
    assert abs(np.linalg.norm(result['direction_world']) - 1.) < 1e-5
    full = None
    if not skip_full_model:
        full_model = PairAxisNet(**config['model'])
        full_data = make_dataset(config, 'train', True)
        full_batch = default_collate([full_data[0]])
        prediction = full_model(full_batch['parent'], full_batch['child'])
        loss, _ = axis_loss(prediction, full_batch, **config['loss'])
        loss.backward()
        assert torch.isfinite(loss)
        assert all(torch.isfinite(p.grad).all() for p in full_model.parameters() if p.grad is not None)
        full = dict(parameters=sum(p.numel() for p in full_model.parameters()), batch_size=1,
                    points_per_part=config['points'], finite_forward_backward=True)
    report = dict(all_passed=True, device='cpu', gpu_training_started=False, not_a_quality_benchmark=True,
                  continuous_inputs=continuous, cached_links=len(caches), cache_hashes_verified=not skip_hashes,
                  original_groups_and_splits_preserved=True, label_independent_inputs=True,
                  projection_targets_recomputed_after_augmentation=True, geometry=geometry_report,
                  sampling=sampling_report, variants=variants, optimizer_steps=4, resume_completed=True,
                  incompatible_resume_rejected=True, glb_inference_completed=True, full_model=full,
                  snapshot_sha256=ready['snapshot_sha256'], seconds=time.monotonic() - started)
    save_json(output / 'preflight.json', report)
    print(report, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--skip-hashes', action='store_true')
    parser.add_argument('--skip-full-model', action='store_true')
    args = parser.parse_args()
    check(config_from(args.config), args.output, args.skip_hashes, args.skip_full_model)
