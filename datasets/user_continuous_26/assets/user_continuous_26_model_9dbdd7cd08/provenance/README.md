# Flower pinwheel

源文件：`0006-casual_windmill_g1_bom.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- All six petals and the central pink hub are a single rotating rigid body. Rear cylindrical housing and stand are fixed.
- Source GLB has a large unsupported gap between the housing and green support. The rear arm is bent upward by up to 0.19 native units to join the housing; the front portion is moved behind the rotor clearance plane. These are inferred assembly repairs.
- Rotor is moved forward by 0.008 native units to restore the generated shaft interface clearance.
- Nominal 0.4 m height and mass/inertia are estimates; positive spin is a right-hand convention. No motor internals or preferred real spin direction are inferred.

## 验证

共3个link、1个可动关节。实际三角网格每1°检查一周，360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0006-casual_windmill_g1_bom
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0006-casual_windmill_g1_bom 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0006-casual_windmill_g1_bom
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0006-casual_windmill_g1_bom
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0006-casual_windmill_g1_bom --time 4 --output pose_at_4s.glb
```
