"""Verify PhysX-Mobility or extract one original case with unchanged paths."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify(root=ROOT):
    folder = Path(root) / "datasets/physx_mobility"
    catalog = json.loads((folder / "catalog.json").read_text(encoding="utf-8"))
    archive = folder / "PhysX-Mobility.zip"
    if not archive.is_file() or archive.stat().st_size != catalog["archive_bytes"]:
        raise ValueError("Original archive is missing; run git lfs pull --include='datasets/physx_mobility/**'")
    if digest(archive) != catalog["archive_sha256"]:
        raise ValueError("Original archive checksum mismatch")
    checksums = folder / "ARCHIVE_FILES.sha256.jsonl.gz"
    if digest(checksums) != catalog["checksum_manifest_sha256"]:
        raise ValueError("Archive file manifest checksum mismatch")
    return catalog, archive, checksums


def extract(case_id, output, root=ROOT):
    catalog, archive_path, checksums = verify(root)
    rows = {row["source_id"]: row for row in catalog["assets"]}
    if case_id not in rows:
        raise ValueError("Unknown PhysX-Mobility case ID")
    row = rows[case_id]
    prefixes = [f"PhysX_mobility/partseg/{case_id}/"]
    exact = {f"PhysX_mobility/urdf/{case_id}.urdf", f"PhysX_mobility/finaljson/{case_id}.json"}
    def wanted(name):
        return name in exact or any(name.startswith(prefix) for prefix in prefixes)
    selected = {}
    with gzip.open(checksums, "rt", encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            if wanted(item["path"]):
                selected[item["path"]] = item
    if not exact.issubset(selected):
        raise ValueError("Case URDF or annotation missing from checksum manifest")
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError("Refusing to overwrite an existing output directory")
    with zipfile.ZipFile(archive_path) as archive:
        members = [entry for entry in archive.infolist() if not entry.is_dir() and wanted(entry.filename)]
        if {entry.filename for entry in members} != set(selected):
            raise ValueError("Archive case members differ from manifest")
        for member in members:
            name = PurePosixPath(member.filename)
            target = (output / member.filename).resolve()
            if name.is_absolute() or ".." in name.parts or output not in target.parents or stat.S_ISLNK(member.external_attr >> 16):
                raise ValueError("Unsafe ZIP entry")
        output.mkdir(parents=True)
        for member in members:
            data = archive.read(member)
            expected = selected[member.filename]
            if len(data) != expected["bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
                raise ValueError(f"Extracted content differs: {member.filename}")
            target = output / member.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    report = {"source": "physx_mobility", "source_id": case_id, "source_revision": catalog["source_revision"],
        "archive_sha256": catalog["archive_sha256"], "files_verified": len(selected),
        "original_content_modified": False, "dependency_issues": row["dependency_issues"],
        "urdf": str(output / row["archive_urdf"])}
    (output / "EXTRACTION.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("verify")
    command = commands.add_parser("extract")
    command.add_argument("--case", required=True)
    command.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "verify":
        catalog, _, _ = verify(args.root)
        print(json.dumps({"passed": True, "cases": catalog["asset_count"], "archive_sha256": catalog["archive_sha256"], "files": catalog["archive_files"]}))
    else:
        print(json.dumps(extract(args.case, args.output, args.root), ensure_ascii=False, indent=2))
