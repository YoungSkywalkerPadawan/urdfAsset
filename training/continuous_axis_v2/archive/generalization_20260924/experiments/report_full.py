"""Plot completed full-run logs without rerunning evaluation."""
import argparse,base64,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args()
rows=[json.loads(s) for s in (a.run/'progress.jsonl').read_text().splitlines()]
fig,axes=plt.subplots(2,2,figsize=(12,8))
for split in ('train','val'):
    r=[x for x in rows if x['event']=='evaluation' and x['split']==split]
    for ax,key,title,scale in zip(axes.flat,['loss','mean_angle','mean_offset','strict_count'],
            ['Evaluation loss','Mean angle (degrees)','Position (% child scale)','Strict pass (%)'],[1,1,100,None]):
        ax.plot([x['epoch'] for x in r],[x[key]*scale if scale else x[key]/x['samples']*100 for x in r],label=split)
        ax.set_title(title);ax.set_xlabel('Epoch');ax.grid(alpha=.25);ax.legend()
axes[0,0].set_yscale('log');fig.tight_layout();fig.savefig(a.run/'curves.png',dpi=150)
img=base64.b64encode((a.run/'curves.png').read_bytes()).decode()
(a.run/'report.html').write_text('<!doctype html><meta charset="utf-8"><title>全量拟合诊断</title><h1>全量训练／验证曲线</h1><p>训练拟合充分，验证泛化仍差。Strict: 5° and 1% child scale. No held-out test evaluation.</p><img style="max-width:100%" src="data:image/png;base64,'+img+'">',encoding='utf-8')
print('report written',flush=True)
