"""Package existing native URDF dependencies on the data host; never execute asset code.

Only file-reference strings are rewritten for portability. Source hashes and
the unchanged source descriptions remain available for tracing every change.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import tarfile
import xml.etree.ElementTree as ET


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


class Resolver:
    def __init__(self, root):
        self.root = root.resolve()
        self.by_name = defaultdict(list)
        for p in self.root.rglob("*"):
            if p.is_file():
                self.by_name[p.name.lower()].append(p)

    def resolve(self, value, context):
        value = value.removeprefix("package://").removeprefix("file://").replace("\\", "/")
        for parent in (context.parent, *context.parent.parents):
            if not parent.is_relative_to(self.root):
                break
            p = (parent / value).resolve()
            if p.is_relative_to(self.root) and p.is_file():
                return p
        parts = Path(value).parts
        if len(parts) < 2:
            raise FileNotFoundError(f"Unresolved local resource: {value}")
        candidates = self.by_name[Path(value).name.lower()]
        matches = []
        # Match a multi-component suffix, never an unrelated basename.
        for offset in range(max(1, len(parts)-1)):
            suffix = "/" + "/".join(parts[offset:]).lower()
            matches = [p for p in candidates if p.as_posix().lower().endswith(suffix)]
            if matches:
                break
        if not matches:
            raise FileNotFoundError(f"Unresolved resource: {value}")
        rank = lambda p: len(Path(os.path.commonpath([p, context])).parts)
        best = max(map(rank, matches)); matches = [p for p in matches if rank(p) == best]
        if len(matches) > 1 and len({sha(p) for p in matches}) > 1:
            raise ValueError(f"Ambiguous resource: {value}")
        return sorted(matches)[0]


class Package:
    def __init__(self, resolver):
        self.resolver = resolver
        self.resources, self.mapping = {}, {}

    def resource(self, path):
        path = path.resolve()
        if path in self.mapping:
            return self.mapping[path]
        name = "resources/" + sha(path)[:24] + path.suffix.lower()
        self.mapping[path] = name
        content = None
        if path.suffix.lower() == ".obj":
            lines = []
            with path.open(encoding="utf-8", errors="strict") as f:
                for line in f:
                    if line.lstrip().startswith("mtllib "):
                        value = line.strip().partition(" ")[2].strip()
                        refs = [value] if (path.parent / value).is_file() else shlex.split(value)
                        names = [Path(self.resource(self.resolver.resolve(ref, path))).name for ref in refs]
                        line = "mtllib " + " ".join(names) + "\n"
                    lines.append(line)
            content = "".join(lines).encode("utf-8")
        elif path.suffix.lower() == ".mtl":
            lines = []
            for line in path.read_text(encoding="utf-8").splitlines():
                tokens = shlex.split(line, comments=True)
                if tokens and (tokens[0].lower().startswith("map_") or tokens[0].lower() in {"bump", "disp", "decal", "norm"}):
                    image = None
                    # OBJ/MTL exports often leave spaces in texture names unquoted.
                    # Keep any map options, then resolve the complete filename suffix.
                    for offset in range(1, len(tokens)):
                        try:
                            image = self.resolver.resolve(" ".join(tokens[offset:]), path)
                            break
                        except FileNotFoundError:
                            continue
                    if image is None:
                        raise FileNotFoundError(f"Unresolved material texture: {line}")
                    line = " ".join(tokens[:offset] + [Path(self.resource(image)).name])
                lines.append(line)
            content = ("\n".join(lines) + "\n").encode("utf-8")
        elif path.suffix.lower() == ".dae":
            tree = ET.parse(path)
            for image in tree.getroot().iter():
                if image.tag.rsplit("}", 1)[-1] != "image":
                    continue
                for node in image.iter():
                    if node.tag.rsplit("}", 1)[-1] in {"init_from", "ref"} and node.text and node.text.strip():
                        image_path = self.resolver.resolve(node.text.strip(), path)
                        node.text = Path(self.resource(image_path)).name
            content = ET.tostring(tree.getroot(), encoding="utf-8", xml_declaration=True)
        item = {"path": path, "content": content, "original_sha256": sha(path)}
        if name in self.resources:
            other = self.resources[name]
            # Equal geometry bytes can refer to differently resolved materials.
            if other["content"] != content:
                raise ValueError("Identical resource basename has different dependency resolution")
        self.resources[name] = item
        return name


def main(args):
    root = args.root.resolve()
    review = root / "review"
    manifest = json.loads((review / "manifest.json").read_text())
    resolvers = {s: Resolver(root / "extracted" / s) for s in ("urdf_files", "infinigen_articulated")}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    records = []
    with tarfile.open(args.output, "w:gz", compresslevel=1) as tar:
        for item in manifest["assets"]:
            source = item.get("dataset")
            if source not in resolvers:
                continue
            asset = json.loads((review / "assets" / item["id"] / "asset.json").read_text())
            record = {"id": item["id"], "source": source}
            try:
                files = asset["source"]["files"]
                candidates = [Path(f["path"]) for f in files if Path(f["path"]).suffix.lower() == ".urdf"]
                if len(candidates) != 1:
                    raise ValueError("Expected one source URDF")
                urdf = candidates[0]
                expected = next(f["sha256"] for f in files if f["path"] == str(urdf))
                if sha(urdf) != expected:
                    raise ValueError("Source URDF checksum changed")
                package = Package(resolvers[source])
                tree = ET.parse(urdf)
                references = []
                for element in tree.getroot().iter():
                    if element.tag not in {"mesh", "texture"} or not element.get("filename"):
                        continue
                    previous = element.get("filename")
                    path = resolvers[source].resolve(previous, urdf)
                    element.set("filename", package.resource(path))
                    references.append({"original_uri": previous, "portable_uri": element.get("filename")})
                prefix = f"datasets/{source}/assets/{item['id']}/original"
                def add_bytes(name, data):
                    info = tarfile.TarInfo(prefix + "/" + name); info.size = len(data)
                    tar.addfile(info, io.BytesIO(data))
                payload = ET.tostring(tree.getroot(), encoding="utf-8", xml_declaration=True)
                add_bytes("model.urdf", payload)
                resource_metadata = []
                for name, resource in sorted(package.resources.items()):
                    path, content = resource["path"], resource["content"]
                    if content is None:
                        tar.add(path, arcname=prefix + "/" + name, recursive=False)
                    else:
                        add_bytes(name, content)
                    resource_metadata.append({"portable_uri": name, "source_path": str(path.relative_to(root)),
                        "source_sha256": resource["original_sha256"],
                        "packaged_sha256": hashlib.sha256(content).hexdigest() if content is not None else resource["original_sha256"],
                        "reference_strings_rewritten": content is not None})
                provenance = {"source_urdf_sha256": expected, "source_urdf_path": str(urdf.relative_to(root)),
                    "modification": "Only resource filenames and material/texture references are rewritten. Original joint/link/limit data retained.",
                    "urdf_references": references, "resources": resource_metadata}
                add_bytes("PORTABILITY.json", (json.dumps(provenance, ensure_ascii=False, indent=2)+"\n").encode())
                record.update(status="portable", resources=len(package.resources), urdf=prefix + "/model.urdf")
            except Exception as exc:
                record.update(status="error", error=f"{type(exc).__name__}: {exc}")
            records.append(record)
            if len(records) % 25 == 0 or record["status"] != "portable":
                print("PACKAGED", len(records), record["source"], record["status"], record.get("error", ""), flush=True)
        data = (json.dumps(records, ensure_ascii=False, indent=2)+"\n").encode()
        info = tarfile.TarInfo("provenance/REMOTE_URDF_PACKAGES.json"); info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    summary = {"assets": len(records), "statuses": dict(Counter(r["status"] for r in records)),
        "by_source": {s: dict(Counter(r["status"] for r in records if r["source"] == s)) for s in resolvers},
        "archive_bytes": args.output.stat().st_size, "archive_sha256": sha(args.output),
        "errors": [r for r in records if r["status"] != "portable"]}
    args.output.with_suffix(args.output.suffix + ".json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("/root/continuous-public-data-20260911"))
    p.add_argument("--output", type=Path, required=True)
    main(p.parse_args())
