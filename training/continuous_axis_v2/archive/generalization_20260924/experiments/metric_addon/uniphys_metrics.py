"""CPU-only UniPhysGen pivot metric for saved world-frame predictions.

Uses the actual complete-object coordinate frames saved by UniPhysGen, not
child or pair bounds. Does not canonicalize the model's predicted pivot.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding='utf-8')
    temporary.replace(path)


def vector(value):
    if len(value) != 3 or not all(math.isfinite(float(x)) for x in value):
        raise ValueError('Expected finite 3-vector')
    return tuple(float(x) for x in value)


def point_to_axis(point, origin, direction):
    p, o, a = map(vector, (point, origin, direction))
    norm = math.sqrt(sum(x*x for x in a))
    if norm < 1e-12:
        raise ValueError('Zero axis')
    a = [x/norm for x in a]
    d = [x-y for x, y in zip(p, o)]
    cross = (d[1]*a[2]-d[2]*a[1], d[2]*a[0]-d[0]*a[2], d[0]*a[1]-d[1]*a[0])
    return math.sqrt(sum(x*x for x in cross))


def pivot_error(point, origin, direction, frame):
    # The shared translation cancels; official scalar scale is max AABB
    # half-extent. Reuse its saved value to avoid point-sampling differences.
    scale = float(frame['scale'])
    if not math.isfinite(scale) or scale <= 1e-12:
        raise ValueError('Invalid complete-object AABB scale')
    return point_to_axis(point, origin, direction) / scale


def build_reference(records, ground_truth, output):
    gt = {r['sample_id']: r for r in read(ground_truth)}
    items = {}
    for path in sorted(Path(records).glob('*.json')):
        record = read(path)
        key = record.get('sample_id')
        if key not in gt or 'coordinate_frame' not in record:
            continue
        frame = record['coordinate_frame']
        if frame.get('name') != 'source_to_aabb_0_2' or gt[key].get('context') not in ('whole', 'cad_pair'):
            raise ValueError('Not a complete-object frame: ' + key)
        pivot_error(gt[key]['origin_world'], gt[key]['origin_world'], gt[key]['direction_world'], frame)
        if key in items:
            raise ValueError('Duplicate sample: ' + key)
        items[key] = dict(coordinate_frame=frame, context=gt[key]['context'], origin_world=gt[key]['origin_world'],
                          direction_world=gt[key]['direction_world'], asset_key=gt[key]['asset_key'],
                          source_scene_sha256=gt[key].get('source_scene_sha256'),
                          record_sha256=sha(path))
    save(output, dict(schema='uniphys_pivot_reference.v1', ground_truth_sha256=sha(ground_truth),
                     frame_source='saved UniPhysGen complete-object inference frames', samples=items))
    return len(items)


def score(predictions, reference, labels):
    refs = reference['samples']
    labels = {r['id']: r for r in labels}
    output, missing, seen = [], [], set()
    for pred in predictions:
        key = pred['id']
        if key in seen:
            raise ValueError('Duplicate prediction: ' + key)
        seen.add(key)
        if key not in refs:
            missing.append(key)
            continue
        gt, row = refs[key], labels[key]
        if gt['asset_key'] != row['asset_key']:
            raise ValueError('Asset mismatch: ' + key)
        # Verify old benchmark and current training labels describe the same
        # line in the same world frame. Along-axis origin changes are allowed.
        origin = [x*row['scale']+c for x,c in zip(row['origin'], row['center'])]
        if point_to_axis(origin, gt['origin_world'], gt['direction_world']) > max(1e-7, row['scale']*1e-5):
            raise ValueError('Ground-truth frame mismatch: ' + key)
        a, b = vector(row['direction']), vector(gt['direction_world'])
        cosine = abs(sum(x*y for x,y in zip(a,b))) / math.sqrt(sum(x*x for x in a)*sum(x*x for x in b))
        if cosine < 1-1e-6:
            raise ValueError('Ground-truth axis mismatch: ' + key)
        value = pivot_error(pred['predicted_origin_world'], gt['origin_world'],
                            gt['direction_world'], gt['coordinate_frame'])
        output.append(dict(pred, uniphys_context=gt['context'], pivot_distance_error_aabb_0_2=value))

    def summary(rows):
        n = len(rows)
        return dict(samples=n,
            pivot_distance_error_aabb_0_2=sum(r['pivot_distance_error_aabb_0_2'] for r in rows)/n if n else None,
            axis_accuracy_le10=sum(r['angle_deg'] <= 10 for r in rows)/n if n else None,
            axis_accuracy_lt10_official=sum(r['angle_deg'] < 10 for r in rows)/n if n else None,
            strict_count=sum(r['angle_deg'] <= 5 and r['origin_to_axis_normalized'] <= .01 for r in rows),
            loose_count=sum(r['angle_deg'] <= 10 and r['origin_to_axis_normalized'] <= .02 for r in rows))
    return dict(metric='pivot_distance_error_aabb_0_2', units='dimensionless',
                definition='distance(raw predicted world pivot, GT world axis) / saved complete-object AABB half-longest-side',
                scope='known continuous joints; no joint-type classification or type-based filtering',
                expected_samples=len(predictions), scored_samples=len(output), missing_reference_ids=missing,
                by_context={s:summary([r for r in output if r['uniphys_context']==s])
                            for s in sorted({r['uniphys_context'] for r in output})},
                micro=summary(output), by_source={s:summary([r for r in output if r['source']==s])
                for s in sorted({r['source'] for r in output})}), output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    build = sub.add_parser('reference')
    build.add_argument('--records', required=True)
    build.add_argument('--ground-truth', required=True)
    build.add_argument('--output', required=True)
    run = sub.add_parser('score')
    for name in ['predictions', 'reference', 'labels', 'output']:
        run.add_argument('--'+name, required=True)
    args = parser.parse_args()
    if args.command == 'reference':
        print('reference_samples', build_reference(args.records, args.ground_truth, args.output))
    else:
        labels = [json.loads(l) for l in Path(args.labels).read_text(encoding='utf-8').splitlines() if l.strip()]
        result, rows = score(read(args.predictions), read(args.reference), labels)
        result['input_sha256'] = {k:sha(getattr(args,k)) for k in ['predictions','reference','labels']}
        save(Path(args.output)/'metrics.json', result)
        save(Path(args.output)/'predictions.json', rows)
        print(json.dumps(result['micro']))
        if result['missing_reference_ids']:
            raise SystemExit('Incomplete coverage; inspect missing_reference_ids before comparing results')


if __name__ == '__main__':
    main()
