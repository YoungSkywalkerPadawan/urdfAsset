"""Add paper-style metrics beside immutable training results; CPU, no weights.

--watch follows the existing finite pipeline and exits when pipeline.exit appears.
It never changes checkpoints, losses, existing results, or selection scores.
"""
import argparse
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from uniphys_metrics import read, save, score, sha


def refresh(root, prepared, reference_path):
    reference = read(reference_path)
    labels = [json.loads(l) for l in (prepared/'val_continuous.jsonl').read_text().splitlines() if l.strip()]
    reports = []
    for experiment in ('E1', 'E2', 'E3'):
        run = root/(experiment+'_run120')
        for prefix in ('val_latest', 'best_val'):
            metrics = run/(prefix+'_metrics.json')
            predictions = run/(prefix+'_predictions.json')
            if not metrics.exists() or not predictions.exists():
                continue
            before = sha(metrics)
            old = read(metrics)
            pred_bytes = predictions.read_bytes()
            rows = json.loads(pred_bytes)
            # The training writer saves these separately. Never label a new
            # metrics file with the previous epoch's predictions during a write.
            if sha(metrics) != before or not rows:
                continue
            if abs(sum(r['angle_deg'] for r in rows)/len(rows)-old['micro']['angle_deg']) > 1e-7:
                continue
            result, augmented = score(rows, reference, labels)
            import hashlib
            result.update(experiment=experiment, checkpoint=prefix, epoch=old['epoch'],
                          predictions_sha256=hashlib.sha256(pred_bytes).hexdigest(),
                          reference_sha256=sha(reference_path), scorer_sha256=sha(Path(__file__).resolve().parents[1]/'uniphys_metrics.py'))
            target = root/'uniphys_metrics'/experiment/prefix
            save(target/'metrics.json', result)
            save(target/'predictions.json', augmented)
            reports.append(result)
    save(root/'uniphys_metrics'/'comparison.json', reports)
    print(json.dumps([dict(experiment=r['experiment'],checkpoint=r['checkpoint'],epoch=r['epoch'],
                           coverage=[r['scored_samples'],r['expected_samples']],**r['micro']) for r in reports]),flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--prepared', type=Path, required=True)
    p.add_argument('--reference', type=Path, required=True)
    p.add_argument('--watch', action='store_true')
    a = p.parse_args()
    while True:
        refresh(a.root, a.prepared, a.reference)
        if not a.watch or (a.root/'pipeline.exit').exists():
            break
        time.sleep(30)
