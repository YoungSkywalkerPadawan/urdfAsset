"""Independent kinematic checks for the derived pair exporter and label separation."""
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

import numpy as np
import trimesh

from export_pair_urdf import export_pair
from load_pair import load_pair
from package_remote_urdfs import Package, Resolver


class PairExportTests(unittest.TestCase):
    def test_portable_material_keeps_texture_filenames_with_spaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "textures").mkdir()
            (root / "textures/Full Base_DIFFUSE.png").write_bytes(b"fixture image")
            (root / "material file.mtl").write_text("newmtl sample\nmap_Kd textures/Full Base_DIFFUSE.png\n")
            (root / "part.obj").write_text("mtllib material file.mtl\nv 0 0 0\n")
            package = Package(Resolver(root)); package.resource(root / "part.obj")
            self.assertEqual(len(package.resources), 3)
            material = next(r for name, r in package.resources.items() if name.endswith(".mtl"))
            self.assertIn(b"map_Kd ", material["content"])
            (root / "unrelated").mkdir(); (root / "unrelated/missing.png").write_bytes(b"wrong image")
            with self.assertRaises(FileNotFoundError):
                Resolver(root).resolve("missing.png", root / "part.obj")

    def fixture(self, root, kind="continuous"):
        root.mkdir()
        scene = trimesh.Scene()
        scene.add_geometry(trimesh.creation.box(), node_name="link_000")
        transform = trimesh.transformations.rotation_matrix(.3, [1, 1, 0])
        transform[:3, 3] = [3, 4, 5]
        scene.add_geometry(trimesh.creation.box(extents=[1, 2, 3]), node_name="link_001", transform=transform)
        scene.export(root / "scene.glb")
        axis = np.array([.2, .8, .4]); axis /= np.linalg.norm(axis)
        joint = dict(name="rotation", type=kind, parent="link_000", child="link_001",
                     origin_world=[1., -2., 3.], direction_world=axis.tolist(), mimic={"joint": "other"},
                     reference_q=.2, source_limits=[-1., 1.])
        (root / "joints.json").write_text(json.dumps({"joints": [joint]}))
        (root / "inputs").mkdir()
        for i in (0, 1):
            np.savez(root / "inputs" / f"link_{i:03d}.npz", xyz=np.full((10, 3), i, dtype=np.float32),
                     normals=np.tile([0., 0., 1.], (10, 1)))
        (root / "asset.json").write_text(json.dumps({"links": [
            {"id": f"link_{i:03d}", "point_file": f"inputs/link_{i:03d}.npz"} for i in (0, 1)]}))
        return joint

    def test_zero_pose_and_rotated_pose_match_reference_axis(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            joint = self.fixture(root / "asset")
            path = export_pair(root / "asset", 0, root / "export")
            robot = ET.parse(path).getroot()
            element = robot.find("joint")
            pivot = np.fromstring(element.find("origin").get("xyz"), sep=" ")
            axis = np.fromstring(element.find("axis").get("xyz"), sep=" ")
            visual = robot.find("link[@name='child']/visual")
            offset = np.fromstring(visual.find("origin").get("xyz"), sep=" ")
            mesh = trimesh.load(path.parent / visual.find("geometry/mesh").get("filename"), process=False)
            scene = trimesh.load(root / "asset/scene.glb", force="scene", process=False)
            transform, name = scene.graph["link_001"]
            expected = scene.geometry[name].copy(); expected.apply_transform(transform)
            np.testing.assert_allclose(mesh.bounds, expected.bounds, atol=1e-6)
            for angle in (0., .7, -.4):
                rotation = trimesh.transformations.rotation_matrix(angle, axis)[:3, :3]
                actual = (mesh.vertices + offset) @ rotation.T + pivot
                direct = trimesh.transform_points(mesh.vertices, trimesh.transformations.rotation_matrix(angle, joint["direction_world"], joint["origin_world"]))
                np.testing.assert_allclose(actual, direct, atol=1e-7)
            self.assertIsNone(element.find("mimic"))
            self.assertTrue(json.loads((path.parent / "provenance.json").read_text())["derived_pair_only"])

    def test_finite_type_not_upgraded_and_limits_shift_by_reference_pose(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root / "asset", "revolute")
            with self.assertRaises(ValueError):
                export_pair(root / "asset", 0, root / "refused")
            path = export_pair(root / "asset", 0, root / "allowed", allow_bounded=True)
            joint = ET.parse(path).getroot().find("joint")
            self.assertEqual(joint.get("type"), "revolute")
            self.assertAlmostEqual(float(joint.find("limit").get("lower")), -1.2)
            self.assertAlmostEqual(float(joint.find("limit").get("upper")), .8)

    def test_point_features_have_no_axis_or_contact_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root / "asset")
            a, label = load_pair(root / "asset", 0, points=6, seed=7)
            b, _ = load_pair(root / "asset", 0, points=6, seed=7)
            self.assertEqual(set(a), {"parent_xyz", "child_xyz", "parent_normals", "child_normals"})
            for key in a:
                np.testing.assert_array_equal(a[key], b[key])
            self.assertIn("origin_world", label)


if __name__ == "__main__":
    unittest.main()
