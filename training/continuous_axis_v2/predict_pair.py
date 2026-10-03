"""Inference for archived models; input is a known continuous parent/child pair."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'archive/generalization_20260924/source'
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(ROOT / 'archive/generalization_20260924/experiments'))

def load_model(checkpoint, device='cpu'):
    import torch
    from model import PairAxisNet
    # Historical identity stored torch.__version__ as TorchVersion, not str.
    with torch.serialization.safe_globals([torch.torch_version.TorchVersion]):
        state = torch.load(checkpoint, map_location='cpu', weights_only=True)
    config = state.get('config', state.get('identity', {}).get('config'))
    if config is None:
        raise ValueError('Unknown checkpoint format')
    net = PairAxisNet(**config['model'])
    features = bool(state.get('identity', {}).get('features'))
    if features:
        from geometry_features import FeatureFusion
        net.encoder = FeatureFusion(net.encoder, config['model']['width'])
    net.load_state_dict(state['model'], strict=True)
    if not all(torch.isfinite(t).all() for t in state['model'].values()):
        raise ValueError('Non-finite model weights')
    return net.to(device).eval(), config, state.get('variant') == 'free_chordal', features

def predict(net, parent, child, free_chordal):
    from model import canonical_origin
    if not free_chordal:
        return net(parent, child)
    raw = {}
    def capture(module, inputs, output):
        raw['offset'] = output
    hook = net.projection_head.register_forward_hook(capture)
    try:
        original = net(parent, child)
        points = child[..., :3] + raw['offset'].float()
        return dict(direction=original['direction'], projection_points=points,
                    origin=canonical_origin(points.mean(1), original['direction']))
    finally:
        hook.remove()

def main():
    import numpy as np
    import torch
    from data_geometry import child_frame, normalize_pair, sample_pair
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkpoint', type=Path, required=True)
    p.add_argument('--input', type=Path, help='NPZ: parent/child arrays [N,6], XYZ metres + unit normals')
    p.add_argument('--output', type=Path)
    p.add_argument('--device', choices=['cpu','cuda'], default='cpu')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--verify-only', action='store_true')
    a = p.parse_args()
    torch.set_num_threads(1)
    net, cfg, free, features = load_model(a.checkpoint, a.device)
    if a.verify_only:
        print(json.dumps(dict(checkpoint=str(a.checkpoint),strict_load=True,
                              free_chordal=free,requires_partfield=features,
                              parameters=sum(t.numel() for t in net.parameters()))))
        return
    if features:
        p.error('E3 requires exact point-aligned PartField features; use archived cpu_full.py evaluation path')
    if a.input is None or a.output is None:
        p.error('--input and --output required')
    with np.load(a.input, allow_pickle=False) as z:
        parent,child = [np.asarray(z[k],dtype=np.float32).copy() for k in ('parent','child')]
    for cloud in (parent,child):
        if cloud.ndim != 2 or cloud.shape[1] != 6 or not np.isfinite(cloud).all():
            raise ValueError('Expected finite [N,6] point pool')
        norm=np.linalg.norm(cloud[:,3:],axis=1,keepdims=True)
        if np.any(norm < 1e-6): raise ValueError('Zero normal')
        cloud[:,3:] /= norm
    center,scale=child_frame(child[:,:3])
    parent,child=sample_pair(parent,child,cfg['points'],np.random.default_rng(a.seed),cfg.get('local_fraction',0.))
    parent,child=normalize_pair(parent,child,center,scale)
    with torch.no_grad():
        pred=predict(net,torch.from_numpy(parent)[None].to(a.device),torch.from_numpy(child)[None].to(a.device),free)
    origin=pred['origin'][0].cpu().numpy()*scale+center
    direction=pred['direction'][0].cpu().numpy()
    if not np.isfinite(origin).all() or not np.isfinite(direction).all():
        raise ValueError('Non-finite prediction')
    result=dict(origin_world_m=origin.tolist(),direction_world=direction.tolist(),
                child_center_world_m=center.tolist(),child_scale_m=scale,
                seed=a.seed,free_chordal=free,checkpoint_sha256=hashlib.sha256(a.checkpoint.read_bytes()).hexdigest(),
                frame='Input shared world frame; XYZ in metres; unitless unoriented axis direction')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2),encoding='utf-8')

if __name__ == '__main__': main()
