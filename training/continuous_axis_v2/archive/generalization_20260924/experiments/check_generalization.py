"""CPU checks for geometry transforms, feature alignment and adapter gradients."""
import argparse
import sys
from pathlib import Path
import torch
from geometry_features import rotation,rotate_batch,FeatureFusion,query_hash

p=argparse.ArgumentParser(); p.add_argument('--source',type=Path,required=True)
a=p.parse_args(); sys.path.insert(0,str(a.source))
from model import PairAxisNet,canonical_origin
torch.set_num_threads(1); torch.manual_seed(17)
parent,child=torch.randn(2,128,6),torch.randn(2,128,6)
d=torch.nn.functional.normalize(torch.randn(2,3),dim=-1)
o=canonical_origin(torch.randn(2,3),d)
b=dict(parent=parent,child=child,origin=o,direction=d)
for i in range(4):
    r=rotation(i)
    assert torch.allclose(r@r.T,torch.eye(3),atol=1e-6) and torch.det(r)>0
    rotated=rotate_batch(b,[i,i])
    assert torch.allclose(rotated['child'][...,:3]@r,child[...,:3],atol=2e-6)
    target=o[:,None]+((child[...,:3]-o[:,None])*d[:,None]).sum(-1,keepdim=True)*d[:,None]
    assert torch.allclose(rotated['projection_target'],target@r.T,atol=2e-6)
net=PairAxisNet(multiscale=True,dropout=0.)
net.encoder=FeatureFusion(net.encoder,128)
features=torch.randn(2,128,448)
net.encoder.set_features(features,features)
out=net(parent,child)
out['origin'].square().mean().backward()
assert net.encoder.adapter[1].weight.grad is not None
assert torch.isfinite(net.encoder.adapter[1].weight.grad).all()
assert net.encoder.adapter[1].weight.grad.abs().sum()>0
assert not net.encoder.pending and features.grad is None
assert query_hash(parent[0],child[0])!=query_hash(parent[0].flip(0),child[0])
print('PASS: proper rotations, label covariance, query ordering, adapter gradients, frozen inputs')
