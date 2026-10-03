"""Axis inference for caller-supplied continuous parent/child mesh groups."""
import argparse
import numpy as np
import torch
import trimesh

from common import read_json, save_json, stable_seed, verify_checkpoint_code
from data_geometry import child_frame, normalize_pair, sample_pair
from model import PairAxisNet


def scene_meshes(path):
    scene = trimesh.load(path, force='scene', process=False)
    meshes = {}
    for node in scene.graph.nodes_geometry:
        transform, geometry = scene.graph[node]
        mesh = scene.geometry[geometry].copy()
        mesh.apply_transform(transform)
        meshes[node] = mesh
    if not meshes:
        raise ValueError('GLB has no mesh nodes')
    return meshes


def cloud_from_nodes(meshes, names, count, rng):
    if not names or len(set(names)) != len(names):
        raise ValueError('Empty or repeated part mesh nodes')
    unknown = set(names) - set(meshes)
    if unknown:
        raise ValueError('Unknown mesh nodes: ' + str(sorted(unknown)))
    mesh = trimesh.util.concatenate([meshes[name] for name in names])
    weights = np.asarray(mesh.area_faces, dtype=np.float64)
    if not np.isfinite(weights).all() or weights.sum() <= 0:
        raise ValueError('Invalid part surface')
    faces = rng.choice(len(weights), count, p=weights / weights.sum())
    triangles = mesh.triangles[faces]
    uv = rng.random((count, 2))
    over = uv.sum(1) > 1
    uv[over] = 1 - uv[over]
    xyz = triangles[:, 0] + uv[:, :1] * (triangles[:, 1] - triangles[:, 0]) + uv[:, 1:] * (triangles[:, 2] - triangles[:, 0])
    return np.concatenate([xyz, mesh.face_normals[faces]], axis=-1).astype('float32')


def predict_glb(glb, pairs, checkpoint, output, device_name='cuda', meters_per_unit=1., allow_smoke=False):
    if not np.isfinite(meters_per_unit) or meters_per_unit <= 0:
        raise ValueError('meters_per_unit must be finite and positive')
    meshes = scene_meshes(glb)
    for mesh in meshes.values():
        mesh.apply_scale(meters_per_unit)
    device = torch.device(device_name)
    state = torch.load(checkpoint, map_location=device, weights_only=True)
    verify_checkpoint_code(state)
    if state.get('smoke_only') and not allow_smoke:
        raise ValueError('Smoke checkpoint is not a trained predictor')
    config = state['config']
    torch.set_num_threads(config.get('cpu_threads', 4))
    model = PairAxisNet(**config['model']).to(device)
    model.load_state_dict(state['model'])
    model.eval()
    names = [pair['name'] for pair in pairs]
    if not pairs or len(set(names)) != len(names):
        raise ValueError('Provide nonempty pairs with unique names')
    results = []
    for pair in pairs:
        if pair.get('type') != 'continuous':
            raise ValueError('Each supplied pair must explicitly declare type=continuous')
        if set(pair['parent_nodes']) & set(pair['child_nodes']):
            raise ValueError('Parent and child share mesh nodes')
        rng = np.random.default_rng(stable_seed(pair['name']))
        pool_size = config.get('pool_size', 8192)
        parent_pool = cloud_from_nodes(meshes, pair['parent_nodes'], pool_size, rng)
        child_pool = cloud_from_nodes(meshes, pair['child_nodes'], pool_size, rng)
        center, scale = child_frame(child_pool[:, :3])
        parent, child = sample_pair(parent_pool, child_pool, config['points'], rng,
                                    config.get('local_fraction', 0.0))
        parent, child = normalize_pair(parent, child, center, scale)
        inputs = [torch.from_numpy(value).unsqueeze(0).to(device) for value in (parent, child)]
        with torch.no_grad():
            prediction = model(*inputs)
        origin = prediction['origin'][0].cpu().numpy() * scale + center
        direction = prediction['direction'][0].cpu().numpy()
        if not np.isfinite(origin).all() or not np.isfinite(direction).all():
            raise ValueError('Nonfinite prediction')
        results.append(dict(name=pair['name'], type='continuous', parent_nodes=pair['parent_nodes'],
            child_nodes=pair['child_nodes'], origin_world_m=origin.tolist(), direction_world=direction.tolist(),
            child_reference_center_world_m=np.asarray(center).tolist(), child_scale_m=float(scale)))
    save_json(output, dict(frame='GLB scene world axes; metres; parent/child pair supplied by caller',
              origin_convention='axis point nearest the child reference center',
              smoke_only=state.get('smoke_only', False), meters_per_input_unit=meters_per_unit, joints=results))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--glb', required=True)
    parser.add_argument('--list-parts', action='store_true')
    parser.add_argument('--pairs')
    parser.add_argument('--checkpoint')
    parser.add_argument('--output')
    parser.add_argument('--device', default='cuda', choices=['cuda', 'cpu'])
    parser.add_argument('--meters-per-unit', type=float, default=1.)
    parser.add_argument('--allow-smoke-checkpoint', action='store_true')
    args = parser.parse_args()
    if args.list_parts:
        import json
        print(json.dumps([dict(node=name, bounds=mesh.bounds.tolist(), faces=len(mesh.faces))
                          for name, mesh in scene_meshes(args.glb).items()], indent=2))
    else:
        if not all((args.pairs, args.checkpoint, args.output)):
            parser.error('--pairs, --checkpoint and --output are required')
        predict_glb(args.glb, read_json(args.pairs)['pairs'], args.checkpoint, args.output,
                    args.device, args.meters_per_unit, args.allow_smoke_checkpoint)
