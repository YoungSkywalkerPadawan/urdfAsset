# Capsule machine

源文件：`0003-casual_capsule_machine_g1_bom.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- Only the visible knob and its integral grip are articulated. Internal capsule metering, ratchet and transmission are not visible and are not reconstructed.
- Continuous rotation is a kinematic demonstration; the real mechanism may impose stops or one-way operation.
- Nominal 0.45 m height and inertia are estimates. The inferred positive direction points out of the knob face.
- Knob is reduced by 3% and offset outward by 0.012 native units to recover clearance in the generated mesh. The source materials are preserved, including the appearance of the upper container.
- A local circular recess is formed in the fixed housing behind the knob to remove the fused source interface. This clearance pocket is an inferred repair, not an observed internal mechanism.

## 验证

共2个link、1个可动关节。实际三角网格每1°检查一周，360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0003-casual_capsule_machine_g1_bom
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0003-casual_capsule_machine_g1_bom 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0003-casual_capsule_machine_g1_bom
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0003-casual_capsule_machine_g1_bom
```
