"""Read an annotated parent/child pair in world metres, with labels kept separate."""
import json
from pathlib import Path

import numpy as np


def load_pair(asset_dir, joint_index, points=2048, seed=42, allow_bounded=False):
    asset_dir = Path(asset_dir)
    metadata = json.loads((asset_dir / "asset.json").read_text(encoding="utf-8"))
    joint = json.loads((asset_dir / "joints.json").read_text(encoding="utf-8"))["joints"][joint_index]
    if joint["type"] != "continuous" and not allow_bounded:
        raise ValueError("Finite rotation is auxiliary data; pass allow_bounded=True explicitly")
    links = {link["id"]: link for link in metadata["links"]}
    rng = np.random.default_rng(seed)
    features = {}
    for role in ("parent", "child"):
        with np.load(asset_dir / links[joint[role]]["point_file"], allow_pickle=False) as pool:
            indices = rng.choice(len(pool["xyz"]), points, replace=points > len(pool["xyz"]))
            features[role + "_xyz"] = pool["xyz"][indices].astype(np.float32)
            features[role + "_normals"] = pool["normals"][indices].astype(np.float32)
    label = {"type": joint["type"], "origin_world": np.asarray(joint["origin_world"], dtype=np.float64),
             "direction_world": np.asarray(joint["direction_world"], dtype=np.float64),
             "mimic": joint.get("mimic"), "joint_name": joint["name"]}
    return features, label
