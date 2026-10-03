"""Run E0/E1/E2 from archived source, with new paths and unchanged frozen data."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--experiment',choices=['E0','E1','E2'],required=True)
    p.add_argument('--cache-root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--device',choices=['cpu','cuda'],default='cuda')
    p.add_argument('--epochs',type=int,default=120)
    p.add_argument('--smoke-steps',type=int,default=0)
    a=p.parse_args()
    root=Path(__file__).resolve().parent
    g=root/'archive/generalization_20260924'
    if a.output.exists(): raise ValueError('Use a new output directory; archived runs are immutable')
    a.output.mkdir(parents=True)
    meta=json.loads((g/'metadata/inputs.json').read_text())
    meta['config']['prepared_dir']=str(g/'source/prepared')
    meta['config']['cache_root']=str(a.cache_root.resolve())
    meta['config']['base_prepared_dir']=str(a.cache_root.resolve())
    path=a.output/'relocated_inputs.json'
    path.write_text(json.dumps(meta,indent=2),encoding='utf-8')
    regularized=a.experiment!='E0'
    cmd=[sys.executable,str(g/'experiments/cpu_full.py'),'--source',str(g/'source'),
         '--metadata',str(path),'--output',str(a.output/'run'),'--device',a.device,
         '--epochs',str(a.epochs),'--batch-size','4','--micro-batch-size','2' if a.experiment=='E0' else '4',
         '--dropout','.05' if regularized else '0','--weight-decay','.0001' if regularized else '0',
         '--rotation-count','4' if a.experiment=='E2' else '1','--smoke-steps',str(a.smoke_steps)]
    print('Launching',a.experiment,'with relocated paths; new run, not a resumed historical run',flush=True)
    subprocess.run(cmd,check=True)

if __name__=='__main__':main()
