# Vault handwheel

源文件：`0010-escape_vault_handle_g1_bom.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The gold rim, three spokes and central hub form one rigid handwheel. Black mounting plate, bolts and rear housing remain fixed.
- Axis is measured from the rear spindle. Positive direction points out of the front handwheel; real operating direction is not known.
- Continuous spin demonstrates the visible degree of freedom. Internal bolts, gears and locking stops are not visible and are not reconstructed.
- The fused handwheel/plate interface is repaired by flattening the fixed side at axial +0.018 and moving side at +0.022 source units, plus a 0.008 outward wheel offset. Existing upper faces and textures are retained.
- Small segmentation holes are capped. The handwheel back is triangulated from planar cut-boundary polygons while preserving their interior holes; this avoids the solid sheets produced by naive hole filling. Source rear-shell holes and texture damage remain visible limitations.
- Nominal 0.5 m height, masses and inertias are estimates.

## 验证

共2个link、1个可动关节。实际三角网格每1°检查一周，360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0010-escape_vault_handle_g1_bom
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0010-escape_vault_handle_g1_bom 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0010-escape_vault_handle_g1_bom
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0010-escape_vault_handle_g1_bom
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0010-escape_vault_handle_g1_bom --time 4 --output pose_at_4s.glb
```
