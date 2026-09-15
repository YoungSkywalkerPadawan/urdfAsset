"""Import a verified portable URDF package and update the asset indexes."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(archive, expected):
    with archive.open("rb") as stream:
        assert hashlib.file_digest(stream, "sha256").hexdigest() == expected, "Archive checksum mismatch"
    with tarfile.open(archive, "r:gz") as package:
        for member in package:
            target = (ROOT / member.name).resolve()
            if ROOT not in target.parents or not member.isfile():
                raise ValueError(f"Unsafe archive entry: {member.name}")
            if not (member.name.startswith(("datasets/urdf_files/assets/", "datasets/infinigen_articulated/assets/"))
                    or member.name == "provenance/REMOTE_URDF_PACKAGES.json"):
                raise ValueError(f"Unexpected archive entry: {member.name}")
            with package.extractfile(member) as source:
                if target.exists():
                    with target.open("rb") as previous:
                        if hashlib.file_digest(previous, "sha256").digest() != hashlib.file_digest(source, "sha256").digest():
                            raise ValueError(f"Refusing to replace different file: {member.name}")
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with target.open("wb") as destination:
                        shutil.copyfileobj(source, destination)
    packages = {(r["source"], r["id"]): r for r in read(ROOT / "provenance/REMOTE_URDF_PACKAGES.json")}
    catalog = read(ROOT / "catalog.json")
    records = catalog["assets"]
    for row in records:
        entry = packages.get((row["source"], row["id"]))
        if entry:
            row["portable_original_urdf"] = entry["status"] == "portable"
            row["original_urdfs"] = [entry["urdf"]] if row["portable_original_urdf"] else []
            row["native_package_status"] = entry["status"]
            if entry.get("error"):
                row["native_package_error"] = entry["error"]
            write(ROOT / row["path"] / "registry.json", row)
    for source, summary in catalog["sources"].items():
        subset = [r for r in records if r["source"] == source]
        summary["portable_original_urdf"] = sum(r["portable_original_urdf"] for r in subset)
        write(ROOT / "datasets" / source / "catalog.json", subset)
    write(ROOT / "catalog.json", catalog)
    manifest = read(ROOT / "manifest.json")
    manifest["sources"] = catalog["sources"]
    write(ROOT / "manifest.json", manifest)
    fields = [k for k in records[0] if k != "original_urdfs"] + ["native_package_status", "native_package_error"]
    with (ROOT / "catalog.csv").open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(records)
    intros = {
        "urdf_files": "59 个资产已补齐原始 URDF 的网格与纹理，资源引用改为仓库内相对路径；修改记录见 original/PORTABILITY.json。另 3 个资产在上游缺少依赖，详见下方清单，仍保留 GLB、参考轴和描述。8 条隔离轴保持原样，不自动加入默认评估。",
        "infinigen_articulated": "仅 pepper_grinder 类 500 个已处理资产，标签为有限 revolute [-π, π]，不能当 continuous 正样本。500 个原始 URDF 均已补齐网格、材质与纹理，仅将资源引用改为相对路径，关节语义与局部坐标保留；修改记录见 original/PORTABILITY.json。",
    }
    for source, intro in intros.items():
        path = ROOT / "datasets" / source / "README.md"
        paragraphs = path.read_text(encoding="utf-8").split("\n\n")
        paragraphs[1] = intro
        prefix = "\n\n".join(paragraphs).split("| 资产 |")[0]
        lines = ["| 资产 | 持续轴 | 辅助轴 | 可评估持续轴 | 原始 URDF |", "|---|---:|---:|---:|---|"]
        for row in records:
            if row["source"] != source:
                continue
            link = f"assets/{row['id']}/registry.json"
            native = f"[URDF](assets/{row['id']}/original/model.urdf)" if row["portable_original_urdf"] else "上游依赖缺失"
            name = row["name"].replace("|", "\\|")
            lines.append(f"| [{name}]({link}) | {row['continuous_joints']} | {row['bounded_rotation_joints']} | {row['eligible_continuous_joints']} | {native} |")
        failed = [r for r in packages.values() if r["source"] == source and r["status"] != "portable"]
        if failed:
            lines.extend(["", "### 上游依赖缺失", ""])
            lines.extend(f"- `{r['id']}`：`{r['error']}`" for r in failed)
        path.write_text(prefix + "\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({s: x["portable_original_urdf"] for s, x in catalog["sources"].items()}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()
    main(args.archive, args.sha256)
