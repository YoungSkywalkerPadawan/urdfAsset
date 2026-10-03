"""GPU-only extraction with exact query alignment and bounded subset support."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import torch
from cpu100 import digest,save
from geometry_features import rotate_batch,feature_name,query_hash


def main(a):
    if not torch.cuda.is_available():
        raise RuntimeError('PartField extraction requires enabled GPU; no CPU fallback')
    sys.path.insert(0,str(a.source))
    from train import make_dataset,verify_snapshot
    cfg=json.loads(a.metadata.read_text())['config']
    verify_snapshot(Path(cfg['prepared_dir']),Path(cfg['cache_root']))
    data=make_dataset(cfg,a.split,False)
    count=min(a.limit,len(data)) if a.limit else len(data)
    # Full 448-dim fp16 features; no hidden compression.
    estimated=count*a.rotations*cfg['points']*2*448*2
    a.output.mkdir(parents=True,exist_ok=True)
    if shutil.disk_usage(a.output).free < estimated + 512*1024**2:
        raise RuntimeError(f'Need approximately {estimated/1024**3:.2f} GiB features plus 0.5 GiB reserve')
    spec=importlib.util.spec_from_file_location('upstream_partfield_adapter',a.adapter)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    if not module._PARTFIELD_CHECKPOINT_PATH.is_file():
        raise FileNotFoundError('Existing trusted PartField weights required; no implicit download')
    provenance=dict(adapter_sha256=digest(a.adapter),weight_sha256=digest(module._PARTFIELD_CHECKPOINT_PATH),
        partfield_source_hashes={str(p.relative_to(module._PARTFIELD_ROOT)):digest(p)
                                for p in sorted(module._PARTFIELD_ROOT.rglob('*.py'))},
        config_sha256=digest(module._PARTFIELD_CONFIG_PATH),feature_dim=448,dtype='float16',
        metadata_sha256=digest(a.metadata),geometry_code_sha256=digest(a.source/'data_geometry.py'),
        rotation_code_sha256=digest(Path(__file__).with_name('geometry_features.py')),
        points=cfg['points'],encode='concatenated parent/child fixed XYZ',
        normalization='upstream union bbox center, longest extent to 1.8',
        query='exact input points in parent then child order')
    manifest=a.output/'manifest.json'
    if manifest.exists():
        assert json.loads(manifest.read_text())==provenance,'Incompatible cache manifest'
    else: save(manifest,provenance)
    extractor=module.PartFieldFeatureExtractor()
    for i in range(count):
        row=data.rows[i]
        item={k:torch.as_tensor(v)[None] for k,v in data[i].items()}
        data._weights.clear()
        for rid in range(a.rotations):
            batch=rotate_batch(item,[rid])
            p,c=batch['parent'][0],batch['child'][0]
            expected=query_hash(p,c)
            path=a.output/feature_name(row['id'],rid)
            if path.exists():
                old=torch.load(path,weights_only=True)
                assert old['query_sha256']==expected and old['manifest_sha256']==digest(manifest)
                continue
            xyz=torch.cat((p[:,:3],c[:,:3]),0)[None].cuda()
            torch.cuda.reset_peak_memory_stats()
            feat,_=extractor.extract(encode_points=xyz,decode_shape_points=xyz)
            assert feat.shape==(1,len(p)+len(c),448) and torch.isfinite(feat).all()
            assert all(not q.requires_grad for q in extractor._model.parameters())
            record=dict(id=row['id'],split=a.split,rotation_id=rid,query_sha256=expected,
                manifest_sha256=digest(manifest),parent_features=feat[0,:len(p)].cpu().half(),
                child_features=feat[0,len(p):].cpu().half())
            temp=path.with_suffix('.partial'); torch.save(record,temp); temp.replace(path)
            print(json.dumps(dict(event='features',split=a.split,index=i,rotation=rid,
                peak_cuda_bytes=torch.cuda.max_memory_allocated())),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('source','metadata','adapter','output'):
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--split',choices=['train','val'],required=True)
    p.add_argument('--rotations',type=int,choices=[1,4],default=4)
    p.add_argument('--limit',type=int,default=32)
    main(p.parse_args())
