"""Full frozen train/validation CPU ablation; no held-out test evaluation.

Same C network and free_chordal computation as cpu100.py. Fixed inputs are
materialized once, without retaining the expensive geometry sampling cache.
"""
import argparse
import collections
import json
import os
from pathlib import Path
import sys
import time

import torch
from cpu100 import digest, save


def main(a):
    torch.set_num_threads(1)
    sys.path.insert(0, str(a.source.resolve()))
    from model import PairAxisNet, axis_metrics, canonical_origin, unit_direction, vector_huber
    from train import seed_all, make_dataset, verify_snapshot, summarize, atomic_checkpoint

    if a.output.exists() and any(a.output.iterdir()) and not a.resume:
        raise ValueError('Output already contains files; use --resume or a new directory')
    a.output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()

    def log(**obj):
        obj['wall_seconds'] = round(time.monotonic()-started, 2)
        with (a.output/'progress.jsonl').open('a') as f:
            f.write(json.dumps(obj, allow_nan=False)+'\n')
        save(a.output/'status.json', obj)
        print(json.dumps(obj, allow_nan=False), flush=True)

    meta = json.loads(a.metadata.read_text())
    cfg = meta['config']
    for name, expected in meta['source_hashes'].items():
        assert digest(a.source/name) == expected, name
    ready = verify_snapshot(Path(cfg['prepared_dir']), Path(cfg['cache_root']))
    cfg['model']['dropout'] = 0.
    cfg.update(batch_size=a.batch_size, workers=0, epochs=a.epochs,
               learning_rate=3e-4, weight_decay=0., amp=False,
               jitter=0., normal_dropout=0., epoch_samples=1234)
    datasets = {s:make_dataset(cfg, s, False) for s in ('train','val')}
    assert len(datasets['train']) == 1234 and len(datasets['val']) == 166
    for key in ('asset_key', 'group'):
        keys = [{(r['source'],r[key]) for r in d.rows} for d in datasets.values()]
        assert keys[0].isdisjoint(keys[1]), key
    # Verify actual geometry files, not only the manifest checksum.
    manifest = json.loads((Path(cfg['cache_root'])/'cache_manifest.json').read_text())
    hashes = {m['path']:m['sha256'] for m in manifest.values()}
    paths = {r[k] for d in datasets.values() for r in d.rows for k in ('parent_file','child_file')}
    def release_file_cache(relative):
        # Release only clean cache pages belonging to this run's input files.
        with (Path(cfg['cache_root'])/relative).open('rb') as f:
            os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
    log(event='verify_geometry', files=len(paths))
    for p in sorted(paths):
        assert digest(Path(cfg['cache_root'])/p) == hashes[p], p
        release_file_cache(p)
    frozen = {}
    for split, data in datasets.items():
        # Fill preallocated tensors to keep peak RAM low on the 2 GiB host.
        for i in range(len(data)):
            item = {k:torch.as_tensor(v) for k,v in data[i].items()}
            if i == 0:
                frozen[split] = {k:torch.empty((len(data),)+v.shape, dtype=v.dtype) for k,v in item.items()}
            for k,v in item.items():
                assert torch.isfinite(v).all(), (split,i,k)
                frozen[split][k][i] = v
            data._weights.clear()
            for field in ('parent_file','child_file'):
                release_file_cache(data.rows[i][field])
            if (i+1) % 100 == 0 or i+1 == len(data):
                log(event='prepare_inputs', split=split, samples=i+1, total=len(data))

    seed_all(a.seed)
    net = PairAxisNet(**cfg['model']).cpu()
    identity = dict(variant='free_chordal', parameters=sum(p.numel() for p in net.parameters()),
        config=cfg, seed=a.seed, batch_size=a.batch_size, micro_batch_size=a.micro_batch_size, epochs=a.epochs, device='cpu',
        threads=1, augmentation=False, sampling='each train row exactly once per epoch',
        snapshot_sha256=ready['snapshot_sha256'], source_hashes=meta['source_hashes'],
        script_sha256=digest(__file__), samples={s:len(d) for s,d in datasets.items()},
        sources={s:dict(collections.Counter(r['source'] for r in d.rows)) for s,d in datasets.items()},
        selection='lowest validation macro_source_group angle/5 + offset/0.01',
        test_used=False, initialization='from scratch; not cpu100 weights')
    assert identity['parameters'] == 915846
    if a.resume:
        assert json.loads((a.output/'identity.json').read_text()) == identity
    else:
        save(a.output/'identity.json', identity)

    raw = {}
    def capture(module, inputs, output):
        raw['offset'] = output
    hook = net.projection_head.register_forward_hook(capture)
    def forward(batch):
        original = net(batch['parent'], batch['child'])
        points = batch['child'][..., :3] + raw.pop('offset').float()
        return dict(direction=original['direction'], projection_points=points,
                    origin=canonical_origin(points.mean(1), original['direction']))
    def loss_fn(pred, batch):
        d,g = unit_direction(pred['direction']),unit_direction(batch['direction'])
        dot = (d*g).sum(-1)
        signed = torch.where((dot.detach()>=0)[:,None],g,-g)
        direction = ((d-signed)**2).sum(-1).mean()
        projection = vector_huber(pred['projection_points']-batch['projection_target']).mean()
        return direction+projection, dict(direction_loss=direction, projection_loss=projection)
    def batch_at(split, indices):
        return {k:v[indices] for k,v in frozen[split].items()}

    probe = batch_at('train', slice(0,a.micro_batch_size))
    pred = forward(probe)
    projection = vector_huber(pred['projection_points']-probe['projection_target']).mean()
    assert torch.autograd.grad(projection,pred['direction'],allow_unused=True)[0] is None
    target = dict(origin=probe['origin'],direction=probe['direction'],projection_points=probe['projection_target'])
    assert float(loss_fn(target,probe)[0]) < 1e-5
    assert int(axis_metrics(target,probe)['success_5deg_1pct'].sum()) == len(probe['parent'])
    del probe, pred, projection, target
    log(event='preflight_pass', parameters=identity['parameters'], samples=identity['samples'])

    @torch.no_grad()
    def evaluate(split, epoch):
        net.eval()
        rows, total, parts_sum = [], 0., collections.defaultdict(float)
        data = datasets[split]
        for begin in range(0,len(data),a.micro_batch_size):
            batch = batch_at(split,slice(begin,begin+a.micro_batch_size))
            pred = forward(batch)
            loss,parts = loss_fn(pred,batch)
            n = len(batch['parent'])
            total += float(loss)*n
            for k,v in parts.items(): parts_sum[k] += float(v)*n
            metrics = axis_metrics(pred,batch)
            world = pred['origin']*batch['scale'][:,None]+batch['center']
            for j in range(n):
                row = data.rows[begin+j]
                rows.append(dict(id=row['id'],source=row['source'],group=row['group'],asset_key=row['asset_key'],
                    predicted_origin_world=world[j].tolist(),predicted_direction_world=pred['direction'][j].tolist(),
                    **{k:float(v[j]) for k,v in metrics.items()}))
        result = summarize(rows)
        def counts(items):
            return dict(strict_count=sum(r['angle_deg']<=5 and r['origin_to_axis_normalized']<=.01 for r in items),
                loose_count=sum(r['angle_deg']<=10 and r['origin_to_axis_normalized']<=.02 for r in items))
        result.update(loss=total/len(data),components={k:v/len(data) for k,v in parts_sum.items()},**counts(rows))
        for source,values in result['by_source'].items():
            values.update(counts([r for r in rows if r['source']==source]))
        save(a.output/f'{split}_latest_metrics.json',dict(epoch=epoch,**result))
        save(a.output/f'{split}_latest_predictions.json',rows)
        log(event='evaluation',split=split,epoch=epoch,loss=result['loss'],components=result['components'],
            mean_angle=result['micro']['angle_deg'],mean_offset=result['micro']['origin_to_axis_normalized'],
            strict_count=result['strict_count'],loose_count=result['loose_count'],samples=len(data),
            selection_score=result['selection_score'])
        net.train()
        return result,rows

    opt = torch.optim.AdamW(net.parameters(),lr=3e-4,weight_decay=0.)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(opt,T_max=a.epochs,eta_min=3e-5)
    first, updates, best = 1,0,float('inf')
    if a.resume:
        state = torch.load(a.output/'last.pt',map_location='cpu',weights_only=False)
        net.load_state_dict(state['model']); opt.load_state_dict(state['optimizer'])
        scheduler.load_state_dict(state['scheduler'])
        first,updates,best = state['epoch']+1,state['updates'],state['best_score']
    else:
        evaluate('val',0)
    for epoch in range(first,a.epochs+1):
        t = time.monotonic()
        order = torch.randperm(len(datasets['train']),generator=torch.Generator().manual_seed(a.seed+epoch-1))
        sums = collections.defaultdict(float)
        for begin in range(0,len(order),a.batch_size):
            indices = order[begin:begin+a.batch_size]
            opt.zero_grad(set_to_none=True)
            batch_loss = 0.
            for offset in range(0,len(indices),a.micro_batch_size):
                batch = batch_at('train',indices[offset:offset+a.micro_batch_size])
                pred = forward(batch)
                loss,parts = loss_fn(pred,batch)
                if not torch.isfinite(loss): raise ValueError('Non-finite loss')
                n = len(batch['parent'])
                (loss*n/len(indices)).backward()
                batch_loss += float(loss.detach())*n/len(indices)
                sums['loss'] += float(loss.detach())*n
                for k,v in parts.items(): sums[k] += float(v.detach())*n
                del pred,loss,parts,batch
            norm = torch.nn.utils.clip_grad_norm_(net.parameters(),1.)
            if not torch.isfinite(norm): raise ValueError('Non-finite gradient')
            opt.step(); updates+=1
            if updates%25 == 0 or (epoch==first and begin==0):
                log(event='update',epoch=epoch,update=updates,batch_loss=batch_loss,gradient_norm=float(norm))
        scheduler.step()
        log(event='epoch',epoch=epoch,updates=updates,seconds=time.monotonic()-t,
            learning_rate=opt.param_groups[0]['lr'],**{k:v/len(order) for k,v in sums.items()})
        improved = False
        if epoch%5 == 0 or epoch==a.epochs:
            evaluate('train',epoch)
            result,rows = evaluate('val',epoch)
            if result['selection_score'] < best:
                best = result['selection_score']; improved=True
                save(a.output/'best_val_metrics.json',dict(epoch=epoch,**result))
                save(a.output/'best_val_predictions.json',rows)
        state = dict(model=net.state_dict(),optimizer=opt.state_dict(),scheduler=scheduler.state_dict(),
            epoch=epoch,updates=updates,best_score=best,identity=identity,variant='free_chordal')
        atomic_checkpoint(a.output/'last.pt',state)
        if improved: atomic_checkpoint(a.output/'best.pt',state)
    hook.remove()
    log(event='complete',epochs=a.epochs,best_validation_score=best)


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--metadata',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--epochs',type=int,default=120)
    p.add_argument('--batch-size',type=int,default=4)
    p.add_argument('--micro-batch-size',type=int,default=2)
    p.add_argument('--seed',type=int,default=20260923)
    p.add_argument('--resume',action='store_true')
    main(p.parse_args())
