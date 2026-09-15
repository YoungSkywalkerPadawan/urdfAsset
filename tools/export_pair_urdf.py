"""Export a kinematic parent-child URDF from review geometry and one reference axis.

This is an explicitly derived two-link test fixture, not a reconstruction of the
full assembly. It does not invent missing axes, inertia or collision geometry.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
import trimesh


def vec(value):
    return " ".join(f"{float(x):.12g}" for x in value)


def export_pair(asset_dir, joint_index, output, allow_bounded=False):
    asset_dir, output = Path(asset_dir), Path(output)
    if (output / "model.urdf").exists():
        raise ValueError("Output already exists; choose a fresh directory")
    joint = json.loads((asset_dir / "joints.json").read_text(encoding="utf-8"))["joints"][joint_index]
    if joint["type"] not in ("continuous", "revolute"):
        raise ValueError("Only stored rotation axes are supported")
    if joint["type"] == "revolute" and not allow_bounded:
        raise ValueError("Use --allow-bounded to export finite rotation auxiliary samples")
    scene = trimesh.load(asset_dir / "scene.glb", force="scene", process=False)
    pivot = np.asarray(joint["origin_world"], dtype=np.float64)
    axis = np.asarray(joint["direction_world"], dtype=np.float64)
    if not np.isfinite(pivot).all() or not np.isfinite(axis).all() or np.linalg.norm(axis) < 1e-12:
        raise ValueError("Invalid stored axis")
    axis /= np.linalg.norm(axis)
    robot = ET.Element("robot", name=asset_dir.name + "_pair")
    robot.append(ET.Comment("Derived pair: zero configuration equals the stored reference pose; no dynamic parameters."))
    (output / "meshes").mkdir(parents=True, exist_ok=True)
    for role in ("parent", "child"):
        node = joint[role]
        if node not in scene.graph.nodes_geometry:
            raise ValueError(f"No mesh for {role}: {node}")
        transform, name = scene.graph[node]
        mesh = scene.geometry[name].copy(); mesh.apply_transform(transform)
        # STL is broadly supported by URDF readers. The original GLB stays intact.
        mesh.export(output / "meshes" / (role + ".stl"))
        link = ET.SubElement(robot, "link", name=role)
        visual = ET.SubElement(link, "visual")
        ET.SubElement(visual, "origin", xyz=vec(-pivot if role == "child" else [0, 0, 0]), rpy="0 0 0")
        geometry = ET.SubElement(visual, "geometry")
        ET.SubElement(geometry, "mesh", filename=f"meshes/{role}.stl")
    element = ET.SubElement(robot, "joint", name="reference_rotation", type=joint["type"])
    ET.SubElement(element, "parent", link="parent")
    ET.SubElement(element, "child", link="child")
    ET.SubElement(element, "origin", xyz=vec(pivot), rpy="0 0 0")
    ET.SubElement(element, "axis", xyz=vec(axis))
    if joint["type"] == "revolute":
        limits = joint.get("limits_radians", joint.get("source_limits"))
        if not isinstance(limits, list) or len(limits) != 2 or not np.isfinite(np.asarray(limits, dtype=float)).all():
            raise ValueError("Finite rotation has no valid stored limits")
        q = float(joint.get("reference_q", 0))
        ET.SubElement(element, "limit", lower=str(float(limits[0])-q), upper=str(float(limits[1])-q), effort="1", velocity="1")
    ET.indent(robot)
    ET.ElementTree(robot).write(output / "model.urdf", encoding="utf-8", xml_declaration=True)
    metadata = {"source_asset": asset_dir.name, "joint_index": joint_index, "reference_joint": joint,
        "derived_pair_only": True, "pose": "q=0 is the stored review reference pose",
        "inertial_and_collision_parameters": "not supplied",
        "finite_limit_effort_velocity": "placeholders of 1 for URDF parser compatibility, not measured physical specifications",
        "mimic": "Original relation retained above; isolated joint is independently actuated in this pair fixture."}
    (output / "provenance.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return output / "model.urdf"


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--asset", type=Path, required=True)
    p.add_argument("--joint-index", type=int, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--allow-bounded", action="store_true")
    a = p.parse_args()
    print(export_pair(a.asset, a.joint_index, a.output, a.allow_bounded))
