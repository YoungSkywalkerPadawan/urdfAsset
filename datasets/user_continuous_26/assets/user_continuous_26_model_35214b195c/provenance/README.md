# Citrus press lever hinge

源文件：`0018-gs1-lever-citrus-press-stylized-001.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、抬起、回落、停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The visible long lever uses a bounded revolute joint, not continuous: a full revolution would sweep through the press body. This is an exception within the continuous-focused input collection.
- The hinge axis is fitted to 266 faces of the visible transverse pin. The lever, tip grip and hinge cap surfaces form one rigid link.
- The demonstrated range is 0 to 0.45 rad (about 25.8 degrees) above the source pose, then back. It is an inferred collision-free lift range, not a measured physical stop specification.
- The cup, cones, press head, support column and base remain fixed. The source lacks a complete visible connection from the lever to the pressing head; no screw, rack or vertical pressing linkage is invented. This animation demonstrates the lever joint rather than a complete squeezing cycle.
- A radius 0.065, depth 0.145 source-unit local hole separates the fused hinge interface. Actual triangle surfaces and their UVs are retained; the solid lever and hinge cap split openings are capped.
- Nominal height 0.42 m, masses and inertias are estimates. Original gray material and irregular generated surfaces are preserved.
- Root vertices within radius 0.070 are trimmed to a 0.054 source-unit pivot envelope, fading to unchanged geometry at radius 0.100. This removes long triangles exposed by capping the fused hinge boundary while preserving the long arm.

## 验证

共2个link、1个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0018-gs1-lever-citrus-press-stylized-001
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0018-gs1-lever-citrus-press-stylized-001 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0018-gs1-lever-citrus-press-stylized-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0018-gs1-lever-citrus-press-stylized-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0018-gs1-lever-citrus-press-stylized-001 --time 4 --output pose_at_4s.glb
```
