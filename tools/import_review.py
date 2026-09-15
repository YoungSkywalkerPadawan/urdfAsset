"""Import existing reviewed assets without changing geometry, labels or point pools.

Binary hardlinks are optional and read-only during import; text/provenance files
are always copied. Original datasets are never modified. No network or credentials.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import tarfile
import xml.etree.ElementTree as ET


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def digest(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def copy_file(source, destination, hardlink=False):
    source, destination = Path(source), Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if digest(source) != digest(destination):
            raise ValueError(f"Existing destination differs: {destination}")
        return
    binary = source.suffix.lower() in {".npz", ".glb", ".gz", ".mp4", ".obj", ".stl", ".png", ".jpg", ".jpeg"}
    if hardlink and binary:
        try:
            os.link(source, destination)
            return
        except OSError:
            pass
    shutil.copy2(source, destination)


def copy_tree(source, destination, hardlink=False):
    for path in sorted(Path(source).rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink in input: {path}")
        if path.is_file():
            copy_file(path, Path(destination) / path.relative_to(source), hardlink)


def unpack(source, destination, strip_root=False):
    """Materialize source archives, rejecting links, devices and escaping paths."""
    destination = Path(destination).resolve()
    with tarfile.open(source) as archive:
        members = archive.getmembers()
        top = {m.name.strip('/').split('/')[0] for m in members}
        drop = strip_root and len(top) == 1
        for member in members:
            name = member.name.partition('/')[2] if drop else member.name
            if not name:
                continue
            target = (destination / name).resolve()
            if destination not in target.parents and target != destination:
                raise ValueError("Unsafe archive path")
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as src, target.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
            else:
                raise ValueError("Source archive contains a link or special file")


def urdf_dependencies(urdf, case):
    files = {urdf}
    for node in ET.parse(urdf).getroot().findall(".//mesh"):
        name = node.get("filename", "")
        if "://" in name:
            raise ValueError(f"Original user URDF has unresolved URI: {name}")
        target = (urdf.parent / name).resolve()
        if case not in target.parents or not target.is_file():
            raise ValueError(f"Missing/escaping user mesh: {target}")
        files.add(target)
        if target.suffix.lower() == ".obj":
            with target.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    if not line.startswith("mtllib "):
                        continue
                    material = (target.parent / line.split(None, 1)[1].strip()).resolve()
                    if not material.is_file():
                        raise ValueError(f"Missing material: {material}")
                    files.add(material)
                    for entry in material.read_text(encoding="utf-8").splitlines():
                        if entry.startswith(("map_", "bump ")):
                            texture = (material.parent / entry.split()[-1]).resolve()
                            if not texture.is_file():
                                raise ValueError(f"Missing texture: {texture}")
                            files.add(texture)
    if any(case not in p.parents for p in files):
        raise ValueError("Dependency outside user case directory")
    return files


def check_original_urdf(path):
    missing = []
    for mesh in ET.parse(path).getroot().findall(".//mesh"):
        name = mesh.get("filename", "")
        if "://" in name or not (path.parent / name).is_file():
            missing.append(name)
    return missing


def main(args):
    repo = args.repo.resolve()
    roots = {k: Path(v).resolve() for k, v in read(args.roots).items()}
    records, assets = [], []
    snapshot = args.frozen
    frozen = defaultdict(list)
    for split in ("train", "val", "test"):
        for line in (snapshot / f"{split}_continuous.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line); frozen[row["asset_key"]].append((split, row))
    excluded = [json.loads(line) for line in (snapshot / "excluded_rows.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    quarantine = {row["id"] for row in excluded}
    asset_paths = {}
    for alias, root in roots.items():
        manifest = read(root / "manifest.json")
        for number, item in enumerate(manifest["assets"], 1):
            source = item.get("dataset", alias)
            asset_id = item["id"]
            source_dir = root / "assets" / asset_id
            destination = repo / "datasets" / source / "assets" / asset_id
            copy_tree(source_dir, destination, args.hardlink)
            asset = read(destination / "asset.json")
            joints = read(destination / "joints.json")["joints"]
            original = destination / "original"
            original_urdfs = []
            if source == "articraft":
                unpack(source_dir / "source.tar.gz", original, strip_root=True)
                original_urdfs = sorted(original.rglob("*.urdf"))
            elif source == "user_continuous_26":
                case = (args.user_cases / asset["source"]["original_case"]).resolve()
                original_urdfs = sorted(case.glob("*.urdf"))
                if len(original_urdfs) != 1:
                    raise ValueError(f"Expected one original URDF: {case}")
                dependencies = urdf_dependencies(original_urdfs[0], case)
                for name in ("README.md", "joints.json", "joint_trajectory.json"):
                    if (case / name).is_file():
                        dependencies.add(case / name)
                for path in sorted(dependencies):
                    copy_file(path, original / path.relative_to(case), args.hardlink)
                original_urdfs = [original / p.relative_to(case) for p in original_urdfs]
            else:
                unpack(source_dir / "source.tar.gz", destination / "source_descriptions")
            missing = {p.relative_to(destination).as_posix(): check_original_urdf(p) for p in original_urdfs}
            portable = bool(original_urdfs) and not any(missing.values())
            if original_urdfs and not portable:
                raise ValueError(f"Incomplete original URDF: {asset_id} {missing}")
            key = alias + "/" + asset_id
            relative = destination.relative_to(repo).as_posix()
            asset_paths[key] = relative
            types = Counter(j["type"] for j in joints)
            q = sum(f"{key}/{i}" in quarantine for i in range(len(joints)))
            status = "partial_quarantine" if q and q < types["continuous"] else "quarantined" if q else "available"
            record = dict(id=asset_id, source=source, path=relative, original_asset_key=key,
                name=item.get("robot_name", asset_id), category=item.get("category", source),
                geometry_links=len(asset["links"]), reference_joints=len(joints),
                continuous_joints=types["continuous"], bounded_rotation_joints=types["revolute"],
                eligible_continuous_joints=len(frozen[key]), quarantined_continuous_joints=q,
                frozen_splits=sorted({s for s, _ in frozen[key]}), status=status,
                portable_original_urdf=portable,
                original_urdfs=[p.relative_to(repo).as_posix() for p in original_urdfs],
                native_format="urdf" if source in {"articraft", "urdf_files", "infinigen_articulated", "user_continuous_26"} else "cad_pair" if source == "fusion_joint" else "usd",
                license=asset["source"]["license"], source_url=asset["source"].get("url"),
                source_revision=asset["source"].get("revision"), scene_sha256=digest(destination / "scene.glb"))
            records.append(record)
            assets.append(dict(item, dataset=source, path=relative,
                training_role="continuous_supervision" if types["continuous"] else "bounded_rotation_axis_auxiliary",
                continuous_joint_count=types["continuous"], bounded_joint_count=types["revolute"],
                evaluation_status=status, eligible_continuous_joints=len(frozen[key]), warnings=item.get("warnings", [])))
            write(destination / "registry.json", record)
            if number % 50 == 0 or number == len(manifest["assets"]):
                print("IMPORTED", alias, number, "/", len(manifest["assets"]), flush=True)
    by_source = {}
    for source in sorted({r["source"] for r in records}):
        subset = [r for r in records if r["source"] == source]
        by_source[source] = {"assets": len(subset), **{k: sum(r[k] for r in subset) for k in
            ("reference_joints", "continuous_joints", "bounded_rotation_joints", "eligible_continuous_joints", "quarantined_continuous_joints", "portable_original_urdf")}}
        write(repo / "datasets" / source / "catalog.json", subset)
    write(repo / "catalog.json", dict(schema_version=1, asset_count=len(records), sources=by_source, assets=records))
    write(repo / "manifest.json", dict(schema_version=1, asset_count=len(assets),
        joint_count=sum(a["joint_count"] for a in assets), sources=by_source, assets=assets))
    with (repo / "catalog.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fields = [k for k in records[0] if k not in ("original_urdfs",)]
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); writer.writeheader(); writer.writerows(records)
    bench = repo / "benchmarks/continuous_axis_v2"
    for split in ("train", "val", "test"):
        result = []
        for key, members in frozen.items():
            for member_split, row in members:
                if member_split != split:
                    continue
                result.append({k: row[k] for k in ("id", "asset_key", "joint_index", "joint_name", "source", "group", "split")}
                    | {"asset_path": asset_paths[key]})
        result.sort(key=lambda r: r["id"])
        bench.mkdir(parents=True, exist_ok=True)
        (bench / f"{split}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False)+"\n" for r in result), encoding="utf-8")
    write(bench / "excluded.json", [{k: v for k, v in row.items() if k not in ("parent_path", "child_path")} for row in excluded])
    copy_file(snapshot / "splits.json", bench / "original_splits.json")
    write(bench / "provenance.json", dict(snapshot_sha256=read(snapshot / "READY.json")["snapshot_sha256"],
        source_ready_sha256=digest(snapshot / "READY.json"), accepted_axes=sum(len(v) for v in frozen.values()),
        excluded_axes=len(excluded), note="Original axis IDs and group splits retained. Labels remain in each asset/joints.json."))
    print(json.dumps(by_source), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--roots", type=Path, required=True)
    p.add_argument("--frozen", type=Path, required=True)
    p.add_argument("--user-cases", type=Path, required=True)
    p.add_argument("--hardlink", action="store_true")
    main(p.parse_args())
