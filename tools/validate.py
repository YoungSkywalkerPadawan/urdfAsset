"""Validate registry, labels, frozen split membership, URDF references and optional file hashes."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def validate(root=ROOT, source=None, hashes=False):
    root = Path(root)
    catalog = read(root / "catalog.json")
    rows = [r for r in catalog["assets"] if not source or r["source"] == source]
    if not rows:
        raise ValueError("No matching source")
    errors, warnings, original_urdfs = [], [], 0
    labels = {}
    for row in rows:
        folder = root / row["path"]
        try:
            asset, joints = read(folder / "asset.json"), read(folder / "joints.json")["joints"]
            assert read(folder / "registry.json") == row, "registry mismatch"
            assert len(joints) == row["reference_joints"], "joint count"
            assert sum(j["type"] == "continuous" for j in joints) == row["continuous_joints"], "type count"
            with (folder / "scene.glb").open("rb") as f:
                assert f.read(4) == b"glTF", "GLB missing; run git lfs pull"
            links = {link["id"]: link for link in asset["links"]}
            for index, joint in enumerate(joints):
                for role in ("parent", "child"):
                    assert joint[role] in links, "unknown target link"
                    assert links[joint[role]]["point_file"], "missing target point pool"
                    path = folder / links[joint[role]]["point_file"]
                    with path.open("rb") as f:
                        assert f.read(2) == b"PK", "point pool missing; run git lfs pull"
                axis = joint["direction_world"]
                assert len(axis) == 3 and all(math.isfinite(x) for x in axis), "invalid axis"
                assert abs(math.sqrt(sum(x*x for x in axis))-1) < 1e-4, "nonunit axis"
                assert len(joint["origin_world"]) == 3 and all(math.isfinite(x) for x in joint["origin_world"]), "invalid anchor"
                labels[f"{row['original_asset_key']}/{index}"] = (row, joint)
            for entry in row["original_urdfs"]:
                urdf = root / entry
                robot = ET.parse(urdf).getroot()
                for mesh in robot.findall(".//mesh") + robot.findall(".//texture"):
                    value = mesh.get("filename", "")
                    if mesh.tag == "texture" and not value:
                        warnings.append({"asset": row["id"], "warning": "Source URDF contains an empty optional texture filename; original syntax retained"})
                        continue
                    assert "://" not in value, "URDF is not portable"
                    target = (urdf.parent / value).resolve()
                    assert root.resolve() in target.parents and target.is_file(), "URDF mesh dependency missing"
                    with target.open("rb") as f:
                        assert not f.read(64).startswith(b"version https://git-lfs.github.com/spec"), "LFS mesh pointer only"
                original_urdfs += 1
                provenance = urdf.parent / "PORTABILITY.json"
                if provenance.is_file():
                    for resource in read(provenance)["resources"]:
                        target = (urdf.parent / resource["portable_uri"]).resolve()
                        assert root.resolve() in target.parents and target.is_file(), "material/texture dependency missing"
                        assert digest(target) == resource["packaged_sha256"], "packaged resource checksum mismatch"
        except Exception as exc:
            errors.append({"asset": row["id"], "error": str(exc)})
    ids, groups, counts = set(), {}, Counter()
    for split in ("train", "val", "test"):
        for line in (root / "benchmarks/continuous_axis_v2" / f"{split}.jsonl").read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if source and row["source"] != source:
                continue
            assert row["id"] not in ids, "duplicate frozen axis"
            ids.add(row["id"]); counts[split] += 1
            assert row["split"] == split, "wrong split file"
            assert groups.setdefault(row["group"], split) == split, "group split leakage"
            asset, joint = labels[row["id"]]
            assert joint["type"] == "continuous" and joint["name"] == row["joint_name"], "reference identity changed"
            assert row["asset_path"] == asset["path"], "asset path changed"
    excluded = read(root / "benchmarks/continuous_axis_v2/excluded.json")
    assert not ids & {r["id"] for r in excluded}, "quarantine overlaps accepted axes"
    hash_count = 0
    if hashes:
        for line in (root / "FILES.sha256.jsonl").read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if source and not row["path"].startswith(f"datasets/{source}/"):
                continue
            path = root / row["path"]
            if not path.is_file() or path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
                errors.append({"file": row["path"], "error": "checksum/size mismatch"})
            hash_count += 1
    result = {"assets_checked": len(rows), "original_urdfs_checked": original_urdfs,
              "frozen_axes_checked": len(ids), "splits": dict(counts), "hashes_checked": hash_count,
              "errors": errors, "warnings": warnings, "passed": not errors}
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source")
    p.add_argument("--hashes", action="store_true")
    p.add_argument("--output", type=Path)
    a = p.parse_args(); result = validate(source=a.source, hashes=a.hashes)
    if a.output:
        a.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
