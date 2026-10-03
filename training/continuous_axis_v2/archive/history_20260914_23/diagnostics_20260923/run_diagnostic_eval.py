"""Bounded diagnostics for the original v2 model, without changing its trainer.

Use only train/val. No production checkpoints are modified or selected here.
"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
import torch
from torch.utils.data._utils.collate import default_collate


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n',encoding='utf-8')


def main(args):
    torch.set_num_threads(args.threads)
    sys.path.insert(0,str(args.source.resolve()))
    from model import PairAxisNet, axis_loss, axis_metrics, unit_direction
    from train import make_dataset, loader, move, summarize, seed_all, verify_snapshot
    from dataset import BalancedDraws
    from common import digest
    output=args.output.resolve()
    if output.exists() and any(output.iterdir()): raise ValueError('Output must be new/empty')
    output.mkdir(parents=True,exist_ok=True)
    config=json.loads((args.run/'run_config.json').read_text())['config']
    config.update(prepared_dir=str(args.prepared),cache_root=str(args.cache),workers=0,batch_size=args.batch_size)
    ready=verify_snapshot(args.prepared,args.cache)
    if args.device=='cuda' and not torch.cuda.is_available():raise RuntimeError('CUDA unavailable')
    device=torch.device(args.device)
    save(output/'identity.json',dict(mode=args.mode,device=str(device),torch=torch.__version__,seed=args.seed,
        snapshot=ready['snapshot_sha256'],config=config,source_hashes={p.name:digest(p) for p in args.source.glob('*.py')},
        diagnostic_sha256=digest(Path(__file__)),steps=args.steps,clip=args.clip,losses=args.losses,
        note='Diagnostic only; no held-out test evaluation. Selected training samples metadata-checked, not newly human-verified.'))
    def log(value):
        with (output/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(value,allow_nan=False)+'\n')
        print(json.dumps(value,allow_nan=False),flush=True)

    def modified_loss(pred,batch,kind):
        total, parts=axis_loss(pred,batch,**config['loss'])
        if kind=='sin2':return total,parts
        d=unit_direction(pred['direction']);g=unit_direction(batch['direction'])
        dot=(d*g).sum(-1)
        if kind=='chordal_abs': directional=(2-2*dot.abs()).mean()
        else:
            # Explicit choice at the +/- tie; torch.abs/minimum may have zero
            # subgradient at exactly orthogonal axes.
            signed=torch.where((dot.detach()>=0)[:,None],g,-g)
            directional=((d-signed)**2).sum(-1).mean()
        total=total-parts['direction_loss']+directional
        return total,dict(parts,direction_loss=directional)

    if args.mode=='math':
        findings=[]
        for theta in [0,5,45,85,89,89.9,90]:
            for kind in ['sin2','chordal_abs','chordal_branch']:
                # Use an exactly orthogonal vector at 90 degrees.
                v=torch.tensor([[1.,0.,0.]]) if theta==90 else torch.tensor([[math.sin(math.radians(theta)),0.,math.cos(math.radians(theta))]])
                v.requires_grad_(); d=unit_direction(v);g=torch.tensor([[0.,0.,1.]])
                dot=(d*g).sum(-1)
                if kind=='sin2':loss=(1-dot.square()).mean()
                elif kind=='chordal_abs':loss=(2-2*dot.abs()).mean()
                else:loss=((d-torch.where((dot.detach()>=0)[:,None],g,-g))**2).sum(-1).mean()
                loss.backward();findings.append(dict(angle=theta,kind=kind,loss=loss.item(),gradient_norm=v.grad.norm().item()))
        # Reuse the repository's actual torch geometry/loss invariance checks.
        from preflight import mathematical_checks
        result=dict(direction_gradients=findings,geometry_checks=mathematical_checks())
        save(output/'summary.json',result);log(result);return

    train=make_dataset(config,'train',False)
    if args.mode=='evaluate':
        checkpoint=args.run/args.checkpoint
        state=torch.load(checkpoint,map_location='cpu',weights_only=True)
        assert state['snapshot_sha256']==ready['snapshot_sha256']
        for name in ('model','points','loss','local_fraction'):
            assert state['config'][name]==config[name],name
        net=PairAxisNet(**config['model']).to(device);net.load_state_dict(state['model']);net.eval()
        summaries={}
        for split in ('train','val'):
            data=train if split=='train' else make_dataset(config,'val',False)
            predictions=[];totals=[];started=time.monotonic()
            with torch.no_grad():
                for step,batch in enumerate(loader(data,config)):
                    indices=batch['row_index'].tolist();batch=move(batch,device)
                    pred=net(batch['parent'],batch['child']);loss,parts=axis_loss(pred,batch,**config['loss']);metrics=axis_metrics(pred,batch)
                    totals.extend([float(loss)]*len(indices))
                    for j,index in enumerate(indices):
                        row=data.rows[index]
                        individual={k:v[j:j+1] for k,v in batch.items()}
                        individual_pred={k:v[j:j+1] for k,v in pred.items()}
                        individual_loss,individual_parts=axis_loss(individual_pred,individual,**config['loss'])
                        predictions.append(dict(id=row['id'],asset_key=row['asset_key'],source=row['source'],group=row['group'],
                            axis_loss=float(individual_loss),loss_components={k:float(v) for k,v in individual_parts.items()},
                            **{k:float(v[j]) for k,v in metrics.items()}))
                    if step%10==0:log(dict(event='evaluate',split=split,done=len(predictions),total=len(data),seconds=time.monotonic()-started))
            result=summarize(predictions);result.update(mean_unweighted_axis_loss=float(np.mean(totals)),seconds=time.monotonic()-started,
                angle_over_45=sum(r['angle_deg']>45 for r in predictions),strict_count=sum(r['success_5deg_1pct'] for r in predictions))
            result['direction_pass_count']=sum(r['angle_deg']<=5 for r in predictions)
            result['position_pass_count']=sum(r['origin_to_axis_normalized']<=.01 for r in predictions)
            if split=='train':
                weights=BalancedDraws(data.rows,config['epoch_samples'],config['seed'],0,0).weights
                result['balanced_expected_loss_no_augmentation']=sum(w*r['axis_loss'] for w,r in zip(weights,predictions))
            summaries[split]=result;save(output/f'{split}_predictions.json',predictions)
        save(output/'summary.json',dict(checkpoint_sha256=digest(checkpoint),checkpoint_epoch=state['epoch']+1,results=summaries));return

    seed_all(args.seed)
    # Deterministic round-robin source selection, one asset at a time.
    by_source={s:[] for s in sorted({r['source'] for r in train.rows})}
    for i,r in enumerate(train.rows):by_source[r['source']].append(i)
    rng=np.random.default_rng(args.seed)
    for s in by_source:rng.shuffle(by_source[s])
    selected=[];seen=set()
    while len(selected)<min(args.samples,len(train)):
        changed=False
        for s,indices in by_source.items():
            while indices:
                i=indices.pop();asset=train.rows[i]['asset_key']
                if asset not in seen:
                    seen.add(asset);selected.append(i);changed=True;break
            if len(selected)>=args.samples:break
        if not changed:break
    selected_rows=[train.rows[i] for i in selected]
    save(output/'selected_rows.json',selected_rows)
    # Verify only needed cached files against the frozen manifest.
    manifest=json.loads((args.cache/'cache_manifest.json').read_text())
    hashes={m['path']:m['sha256'] for m in manifest.values()}
    for relative in {r[f] for r in selected_rows for f in ('parent_file','child_file')}:
        assert digest(args.cache/relative)==hashes[relative],relative
    samples=[train[i] for i in selected]
    fixed=move(default_collate(samples),device)
    save(output/'input_check.json',dict(samples=len(samples),hash_verified=True,finite=all(torch.isfinite(v).all().item() for v in fixed.values() if torch.is_tensor(v)),points=config['points']))
    model_config=copy.deepcopy(config['model']);model_config['dropout']=0.
    net=PairAxisNet(**model_config).to(device)
    if args.mode=='benchmark':
        batch={k:v[:args.batch_size] for k,v in fixed.items()};opt=torch.optim.AdamW(net.parameters(),lr=3e-4)
        times=[]
        for i in range(args.steps):
            start=time.monotonic();opt.zero_grad();pred=net(batch['parent'],batch['child']);loss,_=modified_loss(pred,batch,'sin2');loss.backward();opt.step()
            if device.type=='cuda':torch.cuda.synchronize()
            times.append(time.monotonic()-start);log(dict(event='benchmark',step=i+1,seconds=times[-1],loss=float(loss.detach())))
        save(output/'summary.json',dict(seconds=times,steady_median=float(np.median(times[1:] or times)),samples=len(samples),points=config['points']))
        return

    summaries={};initial=copy.deepcopy(net.state_dict())
    for kind in args.losses:
        seed_all(args.seed);net.load_state_dict(initial);net.train()
        opt=torch.optim.AdamW(net.parameters(),lr=3e-4,weight_decay=0.)
        history=[];start=time.monotonic()
        for step in range(args.steps+1):
            if step%args.log_interval==0 or step==args.steps:
                net.eval()
                with torch.no_grad():
                    loss_sum=0.;part_sums={};metric_chunks={}
                    for begin in range(0,len(samples),args.batch_size):
                        chunk={k:v[begin:begin+args.batch_size] for k,v in fixed.items()}
                        pred=net(chunk['parent'],chunk['child']);loss,parts=modified_loss(pred,chunk,kind)
                        n=len(chunk['parent']);loss_sum+=float(loss)*n
                        for k,v in parts.items():part_sums[k]=part_sums.get(k,0.)+float(v)*n
                        for k,v in axis_metrics(pred,chunk).items():metric_chunks.setdefault(k,[]).append(v)
                    metrics={k:torch.cat(v) for k,v in metric_chunks.items()}
                    entry=dict(event='overfit',kind=kind,step=step,loss=loss_sum/len(samples),seconds=time.monotonic()-start,
                        components={k:v/len(samples) for k,v in part_sums.items()},mean_angle=float(metrics['angle_deg'].mean()),
                        max_angle=float(metrics['angle_deg'].max()),mean_offset=float(metrics['origin_to_axis_normalized'].mean()),
                        strict_count=int(metrics['success_5deg_1pct'].sum()),sample_count=len(samples))
                    history.append(entry);log(entry)
                net.train()
            if step==args.steps:break
            # Fixed round-robin batches; identical draws across loss variants.
            indices=torch.arange(step*args.batch_size,(step+1)*args.batch_size,device=device)%len(samples)
            batch={k:v[indices] for k,v in fixed.items()};opt.zero_grad(set_to_none=True)
            pred=net(batch['parent'],batch['child']);loss,_=modified_loss(pred,batch,kind)
            if not torch.isfinite(loss):raise ValueError('Nonfinite loss')
            loss.backward();norm=torch.nn.utils.clip_grad_norm_(net.parameters(),args.clip)
            if not torch.isfinite(norm):raise ValueError('Nonfinite gradient')
            opt.step()
        summaries[kind]=history
        save(output/f'{kind}_per_sample.json',[dict(id=r['id'],**{k:float(v[i]) for k,v in metrics.items()}) for i,r in enumerate(selected_rows)])
    save(output/'summary.json',dict(experiment='diagnostic overfit, fixed sampled inputs; no augmentation/dropout/weight decay',clip=args.clip,steps=args.steps,history=summaries))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--prepared',type=Path,required=True);p.add_argument('--cache',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--mode',choices=['math','benchmark','overfit','evaluate'],required=True);p.add_argument('--device',choices=['cpu','cuda'],default='cpu');p.add_argument('--threads',type=int,default=1)
    p.add_argument('--seed',type=int,default=20260923);p.add_argument('--samples',type=int,default=16);p.add_argument('--batch-size',type=int,default=8);p.add_argument('--steps',type=int,default=400);p.add_argument('--log-interval',type=int,default=25);p.add_argument('--clip',type=float,default=1.)
    p.add_argument('--losses',nargs='+',choices=['sin2','chordal_abs','chordal_branch'],default=['sin2','chordal_branch']);p.add_argument('--checkpoint',default='best.pt')
    main(p.parse_args())
