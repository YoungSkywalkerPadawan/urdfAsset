"""Real-data GPU benchmark for the frozen PartField cache + free axis head."""
import argparse,json,sys,time
from pathlib import Path
import torch
from torch.utils.data._utils.collate import default_collate
from cpu100 import digest,save
from geometry_features import FeatureFusion,rotate_batch,feature_name,query_hash


def main(a):
    if not torch.cuda.is_available(): raise RuntimeError('GPU required')
    torch.set_num_threads(1)
    sys.path.insert(0,str(a.source))
    from train import seed_all,make_dataset
    from model import PairAxisNet,canonical_origin,unit_direction,vector_huber,axis_metrics
    cfg=json.loads(a.metadata.read_text())['config'];cfg['model']['dropout']=0. if a.fit else .05
    data=make_dataset(cfg,'train',False)
    inputs=[data[i] for i in range(32)]
    data._weights.clear()
    manifest=json.loads((a.features/'manifest.json').read_text())
    assert manifest['metadata_sha256']==digest(a.metadata)
    assert manifest['rotation_code_sha256']==digest(Path(__file__).with_name('geometry_features.py'))
    mh=digest(a.features/'manifest.json')
    a.output.mkdir(parents=True,exist_ok=False)
    seed_all(20260924)
    net=PairAxisNet(**cfg['model'])
    net.encoder=FeatureFusion(net.encoder,cfg['model']['width'])
    net.cuda()
    raw={}
    def capture(m,i,o):raw['offset']=o
    hook=net.projection_head.register_forward_hook(capture)
    opt=torch.optim.AdamW(net.parameters(),lr=3e-4,weight_decay=1e-4)
    if a.fit:
        opt=torch.optim.AdamW(net.parameters(),lr=3e-4,weight_decay=0.)
    schedule=torch.optim.lr_scheduler.CosineAnnealingLR(opt,T_max=a.steps,eta_min=3e-5)
    timings=[];losses=[];before=None
    torch.cuda.reset_peak_memory_stats()
    for step in range(a.steps):
        idx=step%32;rid=0 if a.fit else (step//32)%4
        batch=rotate_batch(default_collate([inputs[idx]]),[rid])
        f=torch.load(a.features/feature_name(data.rows[idx]['id'],rid),weights_only=True)
        assert f['query_sha256']==query_hash(batch['parent'][0],batch['child'][0])
        assert f['manifest_sha256']==mh
        batch={k:v.cuda() for k,v in batch.items()}
        pf,cf=f['parent_features'][None].cuda(),f['child_features'][None].cuda()
        assert torch.isfinite(pf).all() and torch.isfinite(cf).all()
        torch.cuda.synchronize();started=time.monotonic()
        opt.zero_grad(set_to_none=True);net.encoder.set_features(pf,cf)
        pred=net(batch['parent'],batch['child'])
        q=batch['child'][...,:3]+raw.pop('offset')
        pred=dict(direction=pred['direction'],origin=canonical_origin(q.mean(1),pred['direction']),projection_points=q)
        d,g=unit_direction(pred['direction']),unit_direction(batch['direction'])
        signed=torch.where(((d*g).sum(-1).detach()>=0)[:,None],g,-g)
        loss=((d-signed)**2).sum(-1).mean()+vector_huber(q-batch['projection_target']).mean()
        assert torch.isfinite(loss);loss.backward()
        assert torch.isfinite(net.encoder.adapter[1].weight.grad).all()
        assert net.encoder.adapter[1].weight.grad.abs().sum()>0
        norm=torch.nn.utils.clip_grad_norm_(net.parameters(),1.)
        assert torch.isfinite(norm);opt.step();schedule.step();torch.cuda.synchronize()
        timings.append(time.monotonic()-started);losses.append(float(loss.detach()))
        if step%(100 if a.fit else 8)==0:
            print(json.dumps(dict(step=step+1,loss=losses[-1],seconds=timings[-1])),flush=True)
    metrics=[]
    net.eval()
    with torch.no_grad():
        for idx in range(32):
            batch=rotate_batch(default_collate([inputs[idx]]),[0])
            f=torch.load(a.features/feature_name(data.rows[idx]['id'],0),weights_only=True)
            batch={k:v.cuda() for k,v in batch.items()}
            net.encoder.set_features(f['parent_features'][None].cuda(),f['child_features'][None].cuda())
            pred=net(batch['parent'],batch['child']);q=batch['child'][...,:3]+raw.pop('offset')
            pred=dict(direction=pred['direction'],origin=canonical_origin(q.mean(1),pred['direction']),projection_points=q)
            metrics.append({k:float(v[0]) for k,v in axis_metrics(pred,batch).items()})
    result=dict(steps=a.steps,fit=a.fit,parameters=sum(p.numel() for p in net.parameters()),
        peak_cuda_bytes=torch.cuda.max_memory_allocated(),mean_step_seconds=sum(timings[2:])/len(timings[2:]),
        losses=losses,feature_alignment_pass=True,finite_backward_pass=True,
        strict_count=sum(x['success_5deg_1pct'] for x in metrics),samples=32,
        mean_angle=sum(x['angle_deg'] for x in metrics)/32,
        mean_offset=sum(x['origin_to_axis_normalized'] for x in metrics)/32,
        note='Timing excludes disk reads and PartField encoding. Evaluated on these same 32 training inputs; not generalization.')
    save(a.output/'smoke.json',result);save(a.output/'predictions_metrics.json',metrics)
    torch.save(net.state_dict(),a.output/'model.pt')
    hook.remove();print(json.dumps({k:v for k,v in result.items() if k!='losses'}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('source','metadata','features','output'): p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--steps',type=int,default=32)
    p.add_argument('--fit',action='store_true')
    main(p.parse_args())
