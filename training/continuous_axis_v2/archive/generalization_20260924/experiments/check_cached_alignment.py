"""Check batch-4 transforms match the individually extracted feature queries."""
import argparse,json,sys
from pathlib import Path
import torch
from torch.utils.data._utils.collate import default_collate
from geometry_features import rotate_batch,feature_name,query_hash
p=argparse.ArgumentParser()
for name in ('source','metadata','features'): p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();sys.path.insert(0,str(a.source));torch.set_num_threads(1)
from train import make_dataset
cfg=json.loads(a.metadata.read_text())['config'];data=make_dataset(cfg,'train',False)
count=0
for start in range(0,32,4):
    b=default_collate([data[i] for i in range(start,start+4)]);data._weights.clear()
    for rid in range(4):
        rotated=rotate_batch(b,[rid]*4)
        for j in range(4):
            f=torch.load(a.features/feature_name(data.rows[start+j]['id'],rid),weights_only=True)
            assert f['query_sha256']==query_hash(rotated['parent'][j],rotated['child'][j])
            assert f['parent_features'].shape==(2048,448) and f['child_features'].shape==(2048,448)
            count+=1
print('PASS: batch-4 query alignment for',count,'cached sample/rotation pairs')
