"""Search the asset registry without loading meshes or point clouds."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def search(root=ROOT, source=None, joint_type=None, split=None, eligible=False, text=""):
    entries = json.loads((Path(root) / "catalog.json").read_text(encoding="utf-8"))["assets"]
    return [r for r in entries if (not source or r["source"] == source)
            and (not joint_type or r["continuous_joints" if joint_type == "continuous" else "bounded_rotation_joints"] > 0)
            and (not split or split in r["frozen_splits"])
            and (not eligible or r["eligible_continuous_joints"] > 0)
            and (not text or text.lower() in (r["id"] + " " + r["name"] + " " + r["category"]).lower())]


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source")
    p.add_argument("--type", choices=("continuous", "revolute"))
    p.add_argument("--split", choices=("train", "val", "test"))
    p.add_argument("--eligible", action="store_true")
    p.add_argument("--search", default="")
    p.add_argument("--json", action="store_true")
    p.add_argument("--limit", type=int, default=30)
    a = p.parse_args()
    rows = search(source=a.source, joint_type=a.type, split=a.split, eligible=a.eligible, text=a.search)
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(f"Matched {len(rows)} assets")
        for r in rows[:a.limit]:
            print(f"{r['source']}  continuous={r['continuous_joints']}  eligible={r['eligible_continuous_joints']}  {r['path']}")
