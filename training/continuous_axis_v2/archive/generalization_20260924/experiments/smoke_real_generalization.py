"""Two real train pairs, E1/E2 forward/backward only, no long training."""
import argparse,json,sys
from pathlib import Path
import torch
from torch.utils.data._utils.collate import default_collate
from geometry_features import rotate_batch
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True);p.add_argument('--metadata',type=Path,required=True)
a=p.parse_args();sys.path.insert(0,str(a.source));torch.set_num_threads(1)
from train import make_dataset,seed_all
from model import PairAxisNet,canonical_origin,unit_direction,vector_huber
cfg=json.loads(a.metadata.read_text())['config'];cfg['model']['dropout']=.05
data=make_dataset(cfg,'train',False)
for experiment in ('E1','E2'):
    seed_all(20260923)
    net=PairAxisNet(**cfg['model']);raw={}
    def capture(m,i,o): raw['offset']=o
    handle=net.projection_head.register_forward_hook(capture)
    opt=torch.optim.AdamW(net.parameters(),lr=3e-4,weight_decay=1e-4)
    losses=[]
    for index in (0,1):
        b=default_collate([data[index]]);data._weights.clear()
        b=rotate_batch(b,[index+1 if experiment=='E2' else 0])
        opt.zero_grad(set_to_none=True)
        pred=net(b['parent'],b['child'])
        points=b['child'][...,:3]+raw.pop('offset')
        d,g=unit_direction(pred['direction']),unit_direction(b['direction'])
        signed=torch.where(((d*g).sum(-1).detach()>=0)[:,None],g,-g)
        loss=((d-signed)**2).sum(-1).mean()+vector_huber(points-b['projection_target']).mean()
        assert torch.isfinite(loss)
        loss.backward();norm=torch.nn.utils.clip_grad_norm_(net.parameters(),1.)
        assert torch.isfinite(norm);opt.step();losses.append(float(loss.detach()))
    handle.remove()
    print(json.dumps(dict(experiment=experiment,steps=2,losses=losses,parameters=sum(p.numel() for p in net.parameters()),
                         result='finite forward/backward; not a convergence experiment')),flush=True)
    del net,opt,pred,loss,points,d,g,signed
