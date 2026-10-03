"""Deterministic rotations and point-aligned frozen feature fusion."""
import hashlib
import torch
from torch import nn


def rotation(index, seed=20260924):
    if index == 0:
        return torch.eye(3)
    g = torch.Generator().manual_seed(seed + index)
    q, r = torch.linalg.qr(torch.randn(3, 3, generator=g))
    q = q @ torch.diag(torch.sign(torch.diag(r)))
    if torch.det(q) < 0:
        q[:, 0] *= -1
    return q


def rotate_batch(batch, ids):
    result = dict(batch)
    matrices = torch.stack([rotation(int(i)) for i in ids]).to(batch['parent'])
    for role in ('parent', 'child'):
        cloud = batch[role]
        result[role] = torch.cat((cloud[..., :3] @ matrices.transpose(1, 2),
                                  cloud[..., 3:] @ matrices.transpose(1, 2)), -1)
    for key in ('origin', 'direction'):
        result[key] = (batch[key][:, None] @ matrices.transpose(1, 2)).squeeze(1)
    x = result['child'][..., :3]
    o, d = result['origin'][:, None], result['direction'][:, None]
    result['projection_target'] = o + ((x-o)*d).sum(-1, keepdim=True)*d
    result['rotation_id'] = torch.as_tensor(ids, device=x.device)
    return result


def query_hash(parent, child):
    h = hashlib.sha256()
    for t in (parent, child):
        h.update(t.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def feature_name(row_id, rotation_id):
    return hashlib.sha256(row_id.encode()).hexdigest() + f'_r{rotation_id}.pt'


class FeatureFusion(nn.Module):
    """Preserve geometry encoder, inject frozen features before role interaction.

    Must set exactly two feature tensors before each parent/child forward pair.
    This module owns only the trainable adapter, never the pretrained encoder.
    """
    def __init__(self, encoder, width, feature_dim=448):
        super().__init__()
        self.geometry = encoder
        self.adapter = nn.Sequential(nn.LayerNorm(feature_dim), nn.Linear(feature_dim,width),
                                     nn.GELU(), nn.Linear(width,width))
        self.gate = nn.Parameter(torch.tensor(-2.))
        self.pending = []

    def set_features(self, parent, child):
        if self.pending:
            raise RuntimeError('Unconsumed features from previous forward')
        if parent.requires_grad or child.requires_grad:
            raise ValueError('Pretrained cached features must be frozen')
        self.pending = [parent,child]

    def forward(self, cloud, other, pair_center, pair_scale):
        from model import nearest_neighbors, gather
        if not self.pending:
            raise RuntimeError('Missing aligned features')
        features = self.pending.pop(0)
        if features.shape[:2] != cloud.shape[:2]:
            raise ValueError('Point/feature shape mismatch')
        token,anchors,point = self.geometry(cloud,other,pair_center,pair_scale)
        added = self.adapter(features.float()) * self.gate.sigmoid()
        _, indices = nearest_neighbors(anchors,cloud[..., :3],1,256)
        return token + gather(added,indices[...,0]), anchors, point + added
