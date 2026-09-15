# Hand crank egg beater

源文件：`0017-gs1-hand-crank-egg-beater-stylized-001.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- This stylized source is not a mechanically complete gear train. The crank, two beaters and four visible gear disks receive continuous joints; the support frame and hand grip remain fixed.
- URDF mimic relations prescribe opposite 2:1 beater speeds and alternating 1:1 visible gear speeds. These are illustrative kinematic ratios, not tooth-count or torque-based gear engagement.
- The original cages interpenetrate and share triangles. Each healthy outward half is retained and duplicated by 180-degree symmetry with its source UVs. Beater axes are shifted apart by 0.065 source units per side and cage radial dimensions reduced 10%; the lower left support is bent to follow its relocated shaft. Axial dimensions are retained.
- The crank arm and ball move to the front by a smooth 0.23 source-unit dogleg so they can clear the frame and hand grip during a full turn. The root bearing axis is fitted from its cylinder.
- Visible gear centers come from outer-rim circles and axes from measured face planes. Gear disks are moved outward by 0.075 source units and reduced 18%; small hub regions extend toward the original support. Local actual-surface bores create pin clearances.
- Only small openings are capped; beater wire cages and gear spoke windows retain their empty interiors. Original missing/wavy teeth and fused-surface imperfections remain.
- Height 0.34 m, masses, inertias and internal transmission relationships are estimates. This is a URDF-driven visual articulation, not a calibrated mechanical or food-contact simulation.

## 验证

共8个link、7个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0017-gs1-hand-crank-egg-beater-stylized-001
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0017-gs1-hand-crank-egg-beater-stylized-001 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0017-gs1-hand-crank-egg-beater-stylized-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0017-gs1-hand-crank-egg-beater-stylized-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0017-gs1-hand-crank-egg-beater-stylized-001 --time 4 --output pose_at_4s.glb
```
