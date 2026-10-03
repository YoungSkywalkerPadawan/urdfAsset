"""Rebuild historical NPY cache from existing repository NPZ assets; verify every hash."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import numpy as np

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--splits',nargs='+',choices=['train','val','test'],default=['train','val','test'])
    a=p.parse_args()
    root=Path(__file__).resolve().parent
    prepared=root/'archive/generalization_20260924/source/prepared'
    manifest=json.loads((prepared/'cache_manifest.json').read_text())
    by_path={v['path']:(k,v) for k,v in manifest.items()}
    targets={}
    for split in a.splits:
        index={r['id']:r for r in map(json.loads,(a.repo/f'benchmarks/continuous_axis_v2/{split}.jsonl').read_text().splitlines())}
        for r in map(json.loads,(prepared/f'{split}_continuous.jsonl').read_text().splitlines()):
            for role in ('parent','child'):
                relative=r[role+'_file']
                key,record=by_path[relative]
                asset=a.repo/index[r['id']]['asset_path']
                link_id=key.rsplit('/',1)[1]
                links=json.loads((asset/'asset.json').read_text())['links']
                point=next(x['point_file'] for x in links if x['id']==link_id)
                targets[relative]=(asset/point,key,record)
    for relative,(source,key,record) in sorted(targets.items()):
        target=a.output/relative
        if target.exists():
            if sha(target)!=record['sha256']: raise ValueError('Existing cache differs: '+str(target))
            continue
        if sha(source)!=record['source_sha256']: raise ValueError('Source NPZ differs or is an LFS pointer: '+str(source))
        with np.load(source,allow_pickle=False) as z:
            xyz,normals=z['xyz'],z['normals']
            rng=np.random.default_rng(int(hashlib.sha256(key.encode()).hexdigest()[:8],16))
            chosen=rng.choice(len(xyz),min(8192,len(xyz)),replace=False)
            points=np.concatenate([xyz[chosen],normals[chosen]],axis=1).astype('float32')
            points[:,3:]/=np.linalg.norm(points[:,3:],axis=1,keepdims=True)
        target.parent.mkdir(parents=True,exist_ok=True)
        temporary=target.with_suffix('.partial.npy')
        np.save(temporary,points,allow_pickle=False)
        if sha(temporary)!=record['sha256']:
            raise ValueError('Reconstructed hash differs; preserve original cache instead: '+str(temporary))
        temporary.replace(target)
    a.output.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(prepared/'cache_manifest.json',a.output/'cache_manifest.json')
    print(json.dumps(dict(verified_files=len(targets),splits=a.splits,output=str(a.output))))

if __name__=='__main__':main()
