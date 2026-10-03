"""Derive audited child-frame indexes without modifying the frozen v1 split.

Only geometry can quarantine an asset. Labels, prediction errors and split names
never enter the quarantine rule. Original cache files and splits are immutable.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import xml.etree.ElementTree as ET
import numpy as np
try:
    from .data_geometry import child_frame
    from .common import config_from
except ImportError:
    from data_geometry import child_frame
    from common import config_from


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def read_rows(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]


def load_config(path):
    return config_from(path)


def _single_primitive_collision(folder, link_name):
    """Use a simple authored collision as corroboration, never guessed units.

    A lone tiny collision can be an intentional placeholder. Consequently this
    measurement alone cannot quarantine anything; a >100x visual outlier among
    the other links is required independently.
    """
    archive = folder / 'source.tar.gz'
    if not archive.exists():
        return None
    with tarfile.open(archive, 'r:gz') as source:
        urdfs = [item for item in source.getmembers() if item.isfile() and item.name.lower().endswith('.urdf')]
        if len(urdfs) != 1 or urdfs[0].size > 25_000_000:
            return None
        raw = source.extractfile(urdfs[0]).read()
        robot = ET.fromstring(raw)
        link = next((node for node in robot.findall('link') if node.get('name') == link_name), None)
        if link is None or len(link.findall('collision')) != 1:
            return None
        geometry = link.find('collision/geometry')
        if geometry is None or len(geometry) != 1:
            return None
        primitive = geometry[0]
        if primitive.tag == 'box':
            dimensions = np.array([float(value) for value in primitive.get('size').split()])
            if dimensions.shape != (3,):
                return None
        elif primitive.tag == 'sphere':
            dimensions = np.full(3, 2 * float(primitive.get('radius')))
        elif primitive.tag == 'cylinder':
            dimensions = np.array([2 * float(primitive.get('radius')), 2 * float(primitive.get('radius')), float(primitive.get('length'))])
        else:
            return None
        if not np.isfinite(dimensions).all() or np.any(dimensions <= 0):
            return None
        return dict(diagonal_m=float(np.linalg.norm(dimensions)), primitive=primitive.tag,
                    primitive_dimensions_m=dimensions.tolist(), source_member=urdfs[0].name,
                    source_urdf_sha256=hashlib.sha256(raw).hexdigest(),
                    source_archive_sha256=digest(archive))


def audit_asset(folder):
    """Return a reviewable geometry-only decision, independent of its split."""
    asset = read_json(folder / 'asset.json')
    report = dict(asset_json_sha256=digest(folder / 'asset.json'), quarantine_reasons=[], warnings=[], evidence=[])
    sizes = []
    for link in asset['links']:
        bounds = np.asarray(link['bounds'], dtype=np.float64)
        if bounds.shape != (2, 3) or not np.isfinite(bounds).all() or np.any(bounds[1] < bounds[0]):
            report['quarantine_reasons'].append('invalid_visual_bounds')
            report['evidence'].append(dict(link=link['name'], problem='Nonfinite, malformed or reversed bounds'))
            continue
        size = float(np.linalg.norm(bounds[1] - bounds[0]))
        if size <= 1e-8:
            report['quarantine_reasons'].append('degenerate_visual_bounds')
            report['evidence'].append(dict(link=link['name'], visual_diagonal_m=size))
        sizes.append((size, link['name']))
    sizes.sort(reverse=True)
    if len(sizes) >= 2 and sizes[1][0] > 1e-8:
        largest, runner_up = sizes[:2]
        relative = largest[0] / runner_up[0]
        if relative > 100:
            corroboration = _single_primitive_collision(folder, largest[1])
            evidence = dict(link=largest[1], visual_diagonal_m=largest[0],
                            largest_other_link=runner_up[1], largest_other_diagonal_m=runner_up[0],
                            ratio_to_largest_other_visual=relative)
            if corroboration is not None:
                evidence.update(corroboration)
                evidence['ratio_to_authored_collision'] = largest[0] / corroboration['diagonal_m']
                if evidence['ratio_to_authored_collision'] > 100:
                    report['quarantine_reasons'].append('visual_scale_contradicts_collision_and_other_links')
                else:
                    report['warnings'].append('dominant_visual_without_collision_scale_contradiction')
            else:
                report['warnings'].append('dominant_visual_without_simple_collision_reference')
            report['evidence'].append(evidence)
    report['quarantine_reasons'] = sorted(set(report['quarantine_reasons']))
    report['decision'] = 'quarantine' if report['quarantine_reasons'] else 'retain'
    return report


def _statistics(rows):
    return dict(pairs=len(rows), assets=len({row['asset_key'] for row in rows}),
                groups=len({row['group'] for row in rows}),
                sources=dict(sorted(collections.Counter(row['source'] for row in rows).items())),
                private_pairs=sum(row['private'] for row in rows),
                private_assets=len({row['asset_key'] for row in rows if row['private']}))


def build(config):
    base = Path(config['base_prepared_dir']).resolve()
    cache_root = Path(config['cache_root']).resolve()
    output = Path(config['prepared_dir']).resolve()
    if output == base or output == cache_root:
        raise ValueError('v2 must use a new output directory, never the v1 cache/index directory')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Prepared output is not empty; use a new snapshot directory')
    ready = read_json(base / 'READY.json')
    for name, expected in ready['files'].items():
        if digest(base / name) != expected:
            raise ValueError('Frozen base index fingerprint mismatch: ' + name)
    manifest = read_json(base / 'cache_manifest.json')
    if digest(cache_root / 'cache_manifest.json') != digest(base / 'cache_manifest.json'):
        raise ValueError('cache_root does not contain the frozen base cache manifest')
    by_path = {value['path']: value for value in manifest.values()}
    roots = {item['alias']: Path(item['path']) for item in config['data_roots']}
    for alias, root in roots.items():
        expected = ready.get('source_manifests', {}).get(alias)
        if expected is None or digest(root / 'manifest.json') != expected:
            raise ValueError('Source manifest differs from frozen v1 snapshot: ' + alias)
    frozen = read_json(base / 'splits.json')
    assignment = {}
    for group in frozen['groups']:
        for asset_key in group['assets']:
            if asset_key in assignment:
                raise ValueError('Repeated asset in frozen split: ' + asset_key)
            assignment[asset_key] = (group['split'], group['group'])
    rows = []
    for split in ('train', 'val', 'test'):
        for kind in ('continuous', 'auxiliary'):
            rows.extend(read_rows(base / f'{split}_{kind}.jsonl'))
    if len({row['id'] for row in rows}) != len(rows):
        raise ValueError('Repeated row id in frozen indexes')
    for row in rows:
        if assignment.get(row['asset_key']) != (row['split'], row['group']):
            raise ValueError('Row differs from frozen object/group split: ' + row['id'])

    reports = {}
    for index, asset_key in enumerate(sorted(assignment), 1):
        alias, asset_id = asset_key.split('/', 1)
        if alias not in roots:
            raise ValueError('Missing source root for ' + alias)
        report = audit_asset(roots[alias] / 'assets' / asset_id)
        report.update(asset_key=asset_key, split=assignment[asset_key][0], group=assignment[asset_key][1])
        reports[asset_key] = report
        if index % 200 == 0:
            print('AUDITED_ASSETS', index, len(assignment), flush=True)

    clouds = {}
    frames = {}
    cloud_problems = {}
    # Cache summaries, not all point pools; memory stays bounded independently
    # of the dataset size. Verify immutable hashes before deriving a frame.
    for row in rows:
        for field in ('parent_file', 'child_file'):
            relative = row[field]
            if relative in clouds or relative in cloud_problems:
                continue
            path = (cache_root / relative).resolve()
            if not path.is_relative_to(cache_root) or relative not in by_path:
                raise ValueError('Unexpected cache file: ' + relative)
            if digest(path) != by_path[relative]['sha256']:
                raise ValueError('Frozen point cache fingerprint mismatch: ' + relative)
            pool = np.load(path, mmap_mode='r', allow_pickle=False)
            if pool.ndim != 2 or pool.shape[1] != 6 or len(pool) < 3 or not np.isfinite(pool).all():
                cloud_problems[relative] = 'nonfinite_or_malformed_point_cloud'
                continue
            normals = np.linalg.norm(pool[:, 3:], axis=1)
            if np.any(normals < 1e-6) or np.max(np.abs(normals - 1)) > 0.01:
                cloud_problems[relative] = 'invalid_surface_normals'
                continue
            try:
                center, scale = child_frame(pool[:, :3])
            except ValueError:
                cloud_problems[relative] = 'degenerate_target_surface'
                continue
            frames[relative] = (center, scale)
            clouds[relative] = dict(points=len(pool), robust_diagonal_m=scale,
                                    raw_diagonal_m=float(np.linalg.norm(np.ptp(pool[:, :3], axis=0))))
    for row in rows:
        for field in ('parent_file', 'child_file'):
            if row[field] in cloud_problems:
                report = reports[row['asset_key']]
                report['quarantine_reasons'].append(cloud_problems[row[field]])
                report['evidence'].append(dict(cache_file=row[field], problem=cloud_problems[row[field]]))
                report['decision'] = 'quarantine'

    retained, excluded = [], []
    for row in rows:
        if reports[row['asset_key']]['decision'] == 'quarantine':
            excluded.append(dict(**row, exclusion_reasons=sorted(set(reports[row['asset_key']]['quarantine_reasons']))))
            continue
        center, scale = frames[row['child_file']]
        direction = np.asarray(row['direction'], dtype=np.float64)
        if not np.isfinite(direction).all() or np.linalg.norm(direction) <= 1e-8:
            raise ValueError('Malformed axis label requires explicit source repair: ' + row['id'])
        direction /= np.linalg.norm(direction)
        world_origin = np.asarray(row['origin'], dtype=np.float64) * row['scale'] + np.asarray(row['center'], dtype=np.float64)
        origin = (world_origin - center.astype(np.float64)) / scale
        origin -= direction * np.dot(origin, direction)
        if not np.isfinite(origin).all():
            raise ValueError('Malformed origin label requires explicit source repair: ' + row['id'])
        entry = dict(row)
        entry.update(center=center.tolist(), scale=scale, origin=origin.tolist(), direction=direction.tolist(),
                     frame='shared_child_center_robust_diagonal', base_scene_scale=float(row['scale']),
                     child_to_scene_scale=scale / row['scale'])
        retained.append(entry)
        if entry['child_to_scene_scale'] < 0.01:
            reports[row['asset_key']]['warnings'].append('child_smaller_than_one_percent_of_scene')
        if clouds[row['child_file']]['raw_diagonal_m'] / scale > 2:
            reports[row['asset_key']]['warnings'].append('child_surface_has_large_tail_outside_robust_bounds')
    for asset_key, report in reports.items():
        report['warnings'] = sorted(set(report['warnings']))
        report['quarantine_reasons'] = sorted(set(report['quarantine_reasons']))
        member_rows = [row for row in rows if row['asset_key'] == asset_key]
        report['indexed_pairs'] = len(member_rows)
        report['continuous_pairs'] = sum(row['type'] == 'continuous' for row in member_rows)

    output.mkdir(parents=True, exist_ok=True)
    stats = {}
    for split in ('train', 'val', 'test'):
        for role, kind in (('continuous', 'continuous'), ('auxiliary', 'revolute')):
            chosen = [row for row in retained if row['split'] == split and row['type'] == kind]
            path = output / f'{split}_{role}.jsonl'
            path.write_text(''.join(json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n' for row in chosen), encoding='utf-8')
            stats[f'{split}_{role}'] = _statistics(chosen)
    shutil.copyfile(base / 'splits.json', output / 'splits.json')
    shutil.copyfile(base / 'cache_manifest.json', output / 'cache_manifest.json')
    save_json(output / 'statistics.json', stats)
    save_json(output / 'config.json', config)
    (output / 'excluded_rows.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n' for row in excluded), encoding='utf-8')
    decisions = dict(schema_version=2, label_or_prediction_based_filtering=False,
        source_split_sha256=digest(base / 'splits.json'),
        rule=dict(name='conservative_geometry_v1',
                  quarantine=['Invalid/nonfinite visual or target surface geometry',
                              'One visual is >100x every other link AND >100x its own single authored primitive collision'],
                  caution='A tiny authored collision alone is not evidence; it may be an intentional placeholder.',
                  repair='No guessed unit rescaling or silent source changes.'),
        frame=dict(center='0.5%/99.5% child surface quantile bounding-box midpoint',
                   scale='Diagonal of the same child bounds', shared_by_parent_and_child=True),
        base_pairs=len(rows), retained_pairs=len(retained), excluded_pairs=len(excluded),
        retained_continuous=sum(row['type'] == 'continuous' for row in retained),
        excluded_continuous=sum(row['type'] == 'continuous' for row in excluded),
        quarantined_assets=[key for key in sorted(reports) if reports[key]['decision'] == 'quarantine'],
        checked_cache_files=len(clouds) + len(cloud_problems), assets=list(reports.values()))
    save_json(output / 'quality_report.json', decisions)
    lines = ['# Geometry audit for continuous-axis v2', '',
             f'Frozen original pairs: {len(rows)}; retained: {len(retained)}; excluded: {len(excluded)}.',
             'The original split and group assignments are preserved byte-for-byte in splits.json.',
             'All decisions use geometry only. No labels, predictions, validation scores or test scores decide exclusions.',
             'A visual/collision scale contradiction must also be a >100x outlier among all other links; tiny collision placeholders alone do not trigger exclusion.',
             'Child-centred robust scaling replaces whole-scene scaling; source meshes and labels are not rescaled or edited.', '',
             '| Quarantined asset | Original split | Indexed pairs | Reason |', '|---|---|---:|---|']
    for key in decisions['quarantined_assets']:
        item = reports[key]
        lines.append(f'| {key} | {item["split"]} | {item["indexed_pairs"]} | {", ".join(item["quarantine_reasons"])} |')
    (output / 'quality_report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    files = [path for path in output.iterdir() if path.is_file() and path.name != 'config.json']
    fingerprints = {path.name: digest(path) for path in sorted(files)}
    snapshot = hashlib.sha256(json.dumps(fingerprints, sort_keys=True).encode()).hexdigest()
    save_json(output / 'READY.json', dict(schema_version=2, snapshot_sha256=snapshot,
        base_snapshot_sha256=ready['snapshot_sha256'], base_ready_sha256=digest(base / 'READY.json'),
        source_manifests=ready.get('source_manifests', {}), frozen_split_sha256=digest(base / 'splits.json'),
        cache_manifest_sha256=digest(base / 'cache_manifest.json'),
        geometry_code_sha256=digest(Path(__file__).with_name('data_geometry.py')),
        preparation_code_sha256=digest(Path(__file__)),
        assets=len({row['asset_key'] for row in retained}), pairs=len(retained),
        excluded_assets=len(decisions['quarantined_assets']), excluded_pairs=len(excluded),
        cached_links=len(manifest), files=fingerprints))
    print(json.dumps(dict(statistics=stats, excluded_assets=decisions['quarantined_assets'], excluded_pairs=len(excluded)), ensure_ascii=False), flush=True)
    return decisions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    build(load_config(parser.parse_args().config))
