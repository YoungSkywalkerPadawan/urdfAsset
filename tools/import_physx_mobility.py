"""Index the original PhysX-Mobility archive and verify every local extracted file.

Keeps the upstream archive unchanged. Metadata copies are exposed for browsing;
large resources remain in the archive and can be extracted per case.
"""
import argparse
from collections import Counter, defaultdict
import concurrent.futures
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import stat
import threading
import time
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SHA256 = "88308cc2a4cc6177c59e32c2de51e881e6b961737295e5082d7ed01cca221908"
REVISION = "d0768ee9e1415f6be8db78d6389ba018b85134c0"
SOURCE_URL = "https://huggingface.co/datasets/Caoza/PhysX-Mobility"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(source, workers):
    source = source.resolve()
    archive_path = source / "PhysX-Mobility.zip"
    if sha(archive_path) != ARCHIVE_SHA256:
        raise ValueError("Source archive differs from verified upstream version")
    destination = ROOT / "datasets/physx_mobility"
    destination.mkdir(parents=True, exist_ok=True)
    started = time.time_ns()
    issues = defaultdict(list)
    cases = {}
    annotations = {}
    with zipfile.ZipFile(archive_path) as archive:
        archive_lock = threading.Lock()
        entries = [entry for entry in archive.infolist() if not entry.is_dir()]
        names = {entry.filename for entry in entries}
        if len(names) != len(entries) or len({name.casefold() for name in names}) != len(names):
            raise ValueError("Duplicate or case-colliding archive names")
        for entry in entries:
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or ".." in path.parts or path.parts[0] != "PhysX_mobility" or stat.S_ISLNK(entry.external_attr >> 16):
                raise ValueError("Unsafe archive entry")
        local_names = {p.relative_to(source).as_posix() for p in (source / "PhysX_mobility").rglob("*") if p.is_file()}
        if local_names != names:
            raise ValueError(f"Local extracted files differ: extra={len(local_names-names)}, missing={len(names-local_names)}")

        def resolve_ref(context, reference):
            reference = reference.strip().strip('"').replace("\\", "/")
            target = posixpath.normpath(posixpath.join(posixpath.dirname(context), reference))
            return target if target in names else None

        def inspect(entry):
            path = source / entry.filename
            before = path.stat()
            with archive_lock:
                try:
                    data = archive.read(entry)
                except Exception as exc:
                    raise ValueError(f"Cannot read archive entry: {entry.filename}") from exc
            digest = hashlib.sha256(data).hexdigest()
            if before.st_size != len(data) or sha(path) != digest:
                raise ValueError(f"Extracted file changed: {entry.filename}")
            after = path.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                raise ValueError("File changed during verification")
            parts = PurePosixPath(entry.filename).parts
            case_id = Path(parts[2]).stem if parts[1] in {"urdf", "finaljson"} else parts[2]
            problems = []
            row = None
            annotation = None
            suffix = path.suffix.lower()
            if suffix == ".urdf":
                try:
                    robot = ET.fromstring(data)
                    links = {link.get("name") for link in robot.findall("link")}
                    joints = robot.findall("joint")
                    types = Counter(joint.get("type", "unknown") for joint in joints)
                    for element in robot.findall(".//mesh") + robot.findall(".//texture"):
                        reference = element.get("filename", "")
                        if reference and not resolve_ref(entry.filename, reference):
                            problems.append({"kind": "missing_urdf_resource", "file": entry.filename, "reference": reference})
                    for joint in joints:
                        for tag in ("parent", "child"):
                            element = joint.find(tag)
                            if element is None or element.get("link") not in links:
                                problems.append({"kind": "unknown_joint_link", "joint": joint.get("name"), "role": tag})
                    row = {"id": f"physx_mobility_{case_id}", "source": "physx_mobility", "source_id": case_id,
                        "path": "datasets/physx_mobility", "group": f"partnet_mobility:{case_id}",
                        "representation": "native_urdf_archive", "geometry_links": len(links),
                        "reference_joints": len(joints), "joint_types": dict(types),
                        "continuous_joints": types["continuous"], "bounded_rotation_joints": types["revolute"],
                        "prismatic_joints": types["prismatic"], "fixed_joints": types["fixed"],
                        "eligible_continuous_joints": 0, "frozen_splits": [],
                        "urdf_description": f"datasets/physx_mobility/descriptions/urdf/{case_id}.urdf",
                        "physics_annotation": f"datasets/physx_mobility/descriptions/finaljson/{case_id}.json",
                        "archive_urdf": entry.filename, "archive_path": "datasets/physx_mobility/PhysX-Mobility.zip",
                        "license": "CC-BY-NC-4.0", "source_url": SOURCE_URL, "source_revision": REVISION}
                except ET.ParseError as exc:
                    raise ValueError(f"Invalid source URDF: {entry.filename}") from exc
            elif parts[1] == "finaljson":
                annotation = json.loads(data)
            elif suffix in {".obj", ".mtl"}:
                pattern = rb"(?m)^mtllib[ \t]+([^\r\n]+)" if suffix == ".obj" else rb"(?m)^(?:map_\w+|bump|disp|decal|norm)[ \t]+([^\r\n]+)"
                for match in re.finditer(pattern, data):
                    reference = match.group(1).decode("utf-8", errors="replace").strip()
                    candidates = [reference] if suffix == ".obj" else [reference] + [" ".join(reference.split()[i:]) for i in range(1, len(reference.split()))]
                    if not any(resolve_ref(entry.filename, value) for value in candidates):
                        problems.append({"kind": "missing_material_resource", "file": entry.filename, "reference": reference})
            return {"path": entry.filename, "bytes": len(data), "sha256": digest}, case_id, row, annotation, problems

        total = 0
        manifest_path = destination / "ARCHIVE_FILES.sha256.jsonl.gz"
        with manifest_path.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as output, concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            for offset in range(0, len(entries), 512):
                for checksum, case_id, row, annotation, problems in pool.map(inspect, entries[offset:offset+512]):
                    output.write((json.dumps(checksum, ensure_ascii=False)+"\n").encode("utf-8"))
                    total += checksum["bytes"]
                    issues[case_id].extend(problems)
                    if row:
                        cases[case_id] = row
                    if annotation is not None:
                        annotations[case_id] = annotation
                if offset % (512*10) == 0:
                    print("VERIFIED", min(offset+512, len(entries)), "/", len(entries), flush=True)
        if set(cases) != set(annotations):
            raise ValueError("URDF / annotation case IDs differ")
    shutil.copyfile(source / "README.md", destination / "UPSTREAM_README.md")
    archived = destination / archive_path.name
    if not archived.exists():
        try:
            os.link(archive_path, archived)
        except OSError:
            shutil.copyfile(archive_path, archived)
    for directory in ("urdf", "finaljson"):
        target = destination / "descriptions" / directory
        target.mkdir(parents=True, exist_ok=True)
        for path in (source / "PhysX_mobility" / directory).iterdir():
            if path.is_file():
                shutil.copyfile(path, target / path.name)
    rows = []
    for case_id in sorted(cases, key=int):
        row = cases[case_id]; annotation = annotations[case_id]
        row.update(name=annotation.get("object_name", case_id), category=annotation.get("category", "unknown"),
            source_dimension=annotation.get("dimension"), annotated_parts=len(annotation.get("parts", [])),
            dependency_issues=issues[case_id], status="source_dependency_issues" if issues[case_id] else "available")
        rows.append(row)
    totals = Counter()
    for row in rows:
        totals.update(row["joint_types"])
    summary = {"schema_version": 1, "source": "physx_mobility", "asset_count": len(rows), "joint_types": dict(totals),
        "cases_with_continuous": sum(r["continuous_joints"] > 0 for r in rows),
        "cases_with_dependency_issues": sum(bool(r["dependency_issues"]) for r in rows),
        "source_url": SOURCE_URL, "source_revision": REVISION, "license": "CC-BY-NC-4.0",
        "archive_sha256": ARCHIVE_SHA256, "archive_bytes": archive_path.stat().st_size,
        "archive_files": len(entries), "uncompressed_bytes": total,
        "checksum_manifest_sha256": sha(manifest_path), "assets": rows}
    write(destination / "catalog.json", summary)
    write(destination / "IMPORT_REPORT.json", {k: v for k, v in summary.items() if k != "assets"} | {
        "local_extracted_files_match_archive": True, "verified_local_files": len(entries),
        "upstream_readme_sha256": sha(source / "README.md"), "audit_started_unix_ns": started,
        "source_content_modified": False, "included_in_frozen_benchmark": False})
    print(json.dumps({k: v for k, v in summary.items() if k != "assets"}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    main(args.source, args.workers)
