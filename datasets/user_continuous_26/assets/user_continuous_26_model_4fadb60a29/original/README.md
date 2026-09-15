# Stylized slicer wheel

源文件：`0011-exaggerated-slicer.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- This generated model has a stylized and ambiguous cutting mechanism. The lower circular wheel is treated as the continuous rotary member; upper curved plate, upright, fork and base remain fixed. This is an inferred kinematic interpretation, not a verified real slicer mechanism.
- Axis is determined from the two wheel-face normals and its rim center. The short-cylinder-only fit was unstable and is recorded as a rejected candidate.
- The wheel is reduced to 94% about its axle and compressed a further 15% axially to recover clearance in the fused source geometry. Segmentation boundaries are capped.
- Positive spin direction points toward the visible front wheel face; the actual powered direction and transmission are unknown.
- Nominal 0.5 m height, mass and inertia are estimates; original stylized surface and texture defects remain.
- Stray rotor vertices beyond radius 0.087 source units are brought back to that radial envelope. The wheel rear face is limited to axial -0.039 before scaling. A local 0.089-radius pocket in the fixed support/base clears the wheel sweep within axial +/-0.044, while excluding the central bearing region below radius 0.025. These are explicit clearance repairs of the fused generated mesh.

## 验证

共2个link、1个可动关节。实际三角网格每1°检查一周，360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0011-exaggerated-slicer
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0011-exaggerated-slicer 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0011-exaggerated-slicer
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0011-exaggerated-slicer
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0011-exaggerated-slicer --time 4 --output pose_at_4s.glb
```
