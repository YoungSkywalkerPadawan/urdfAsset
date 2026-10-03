"""Render the recorded CPU fitting measurements; never estimates missing results."""
import argparse
import base64
import html
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p=argparse.ArgumentParser()
    p.add_argument('run', type=Path)
    a=p.parse_args()
    records=[json.loads(x) for x in (a.run/'progress.jsonl').read_text(encoding='utf8').splitlines() if x.strip()]
    curves={}
    for r in records:
        if r['event']=='evaluation':
            curves.setdefault(r['variant'], []).append(r)
    identity=json.loads((a.run/'identity.json').read_text(encoding='utf8'))
    complete=records[-1]['event']=='complete'
    fields=[('loss','Total loss (different objectives)',1),('mean_angle','Mean axis angle (degrees)',1),
            ('mean_offset','Mean position error (% child size)',100),('strict_count','Strict passes / 100',1),
            ('direction_loss','Direction loss (different objectives)',1),('projection_loss','Projection loss (same radial Huber)',1)]
    fig,axs=plt.subplots(2,3,figsize=(15,8),layout='constrained')
    for ax,(key,title,mult) in zip(axs.flat,fields):
        for name,rs in curves.items():
            vals=[r.get(key,r.get('components',{}).get(key))*mult for r in rs]
            ax.plot([r['epoch'] for r in rs],vals,label=name,linewidth=1.7)
        ax.set_title(title,fontsize=10)
        ax.set_xlabel('Epoch (100 samples, once each)')
        ax.grid(alpha=.25)
        if key.endswith('loss'):
            ax.set_yscale('symlog',linthresh=.001)
    axs[0,0].legend(fontsize=8)
    fig.suptitle('CPU fixed-input training fit — '+('complete' if complete else 'in progress'),fontsize=15)
    fig.savefig(a.run/'curves.png',dpi=150)
    plt.close(fig)

    def table(headers, rows):
        return '<table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'

    main_rows=[]
    source_rows=[]
    case_rows=[]
    final={}
    for name,rs in curves.items():
        last=rs[-1]
        bp=a.run/f'{name}_best_metrics.json'
        best=json.loads(bp.read_text(encoding='utf8')) if bp.exists() else last
        final[name]=dict(last=last,best=best)
        main_rows.append([name,last['epoch'],f"{last['strict_count']}/100",f"{last['loose_count']}/100",
            f"{last['mean_angle']:.3f}°",f"{100*last['mean_offset']:.3f}%",
            f"{best['strict_count']}/100（第 {best['epoch']} 轮）"])
        for source,m in last['by_source'].items():
            source_rows.append([name,source,m['samples'],f"{int(m['strict_count'])}/{m['samples']}",f"{m['mean_angle']:.3f}°",f"{100*m['mean_offset']:.3f}%"])
        pp=a.run/f'{name}_last_predictions.json'
        if pp.exists():
            predictions=json.loads(pp.read_text(encoding='utf8'))
            for r in sorted(predictions,key=lambda x:x['angle_deg']/5+x['origin_to_axis_normalized']/.01,reverse=True):
                case_rows.append([name,r['source'],r['id'],f"{r['angle_deg']:.3f}°",f"{100*r['origin_to_axis_normalized']:.3f}%",'通过' if r['success_5deg_1pct'] else '未通过'])
    summary=dict(complete=complete,identity=identity,results=final,last_event=records[-1])
    (a.run/'report_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    encoded=base64.b64encode((a.run/'curves.png').read_bytes()).decode()
    text=f'''<!doctype html><html lang="zh"><meta charset="utf-8"><title>100 个样本 CPU 拟合对照</title>
<style>body{{font:16px/1.7 system-ui,sans-serif;max-width:1250px;margin:32px auto;padding:0 24px;color:#182638;background:#f5f7fa}}table{{border-collapse:collapse;width:100%;font-size:14px;background:white;margin:20px 0}}th,td{{border:1px solid #dce2eb;padding:9px;text-align:left}}th{{background:#e8eef6}}img{{width:100%;background:white}}code{{background:#e8eef6;padding:2px 5px}}.note{{border-left:4px solid #3978bb;padding:12px 20px;background:white}}</style>
<h1>100 个真实样本：CPU 拟合对照</h1><p>2026-09-23 · 状态：{'已完成' if complete else '运行中，仅显示已测结果'}</p>
<p class="note">本报告评估固定训练输入的拟合能力，不代表新物体上的泛化。100 个不同训练资产，每个取一条轴；每部件 2,048 点。关闭旋转等增强、dropout 和 weight decay。完整 C 模型，915,846 参数，从头初始化。</p>
<p>PyTorch {html.escape(identity['torch'])}；CPU 线程 {identity['threads']}；batch {identity['batch_size']}；最多 {identity['epochs']} 轮；AdamW 3e-4，余弦下降到 3e-5。所有组使用相同初始化和每轮样本顺序。</p>
<p>baseline：原约束与原损失；free_sin2：解除方向对投影偏移的硬约束，只保留 sin² 方向和投影损失；free_chordal：再将方向损失改为正负等价弦距离。第一项对照同时改两项，不能单独归因。不同目标的总 Loss 不宜直接排名。</p>
<p>严格：轴角度 ≤5° 且位置 ≤子件尺度 1%；宽松：≤10° 且 ≤2%。位置指标沿用 v2 的预测规范原点到真实轴距离。最佳权重按本批训练严格通过数选取，不是验证集最佳。</p>
<h2>最后一轮与训练最佳</h2>{table(['方案','最后轮次','严格','宽松','平均角度','平均位置','训练最佳严格'],main_rows)}
<img alt="六项训练拟合曲线" src="data:image/png;base64,{encoded}">
<h2>最后一轮分来源</h2>{table(['方案','来源','样本数','严格','平均角度','平均位置'],source_rows)}
<h2>逐样本结果</h2><p>各组按角度/5+位置/0.01 从差到好排列。</p>{table(['方案','来源','ID','角度','位置','严格'],case_rows)}
<p>限制：单种子、固定点、无增强；标签经过缓存和元数据检查，未重新人工逐例核验。不同资产可能属于相同设计家族。未使用独立测试集。</p></html>'''
    (a.run/'report.html').write_text(text,encoding='utf8')
    print(json.dumps({k:dict(epoch=v['last']['epoch'],strict=v['last']['strict_count'],angle=v['last']['mean_angle'],position=v['last']['mean_offset']) for k,v in final.items()},ensure_ascii=False))


if __name__=='__main__':
    main()
