# Toy dump truck

源文件：`0004-casual_dump_truck_g1_bom.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- Four wheels have independent continuous joints. The paired centers define each axle rather than using a hard-coded world axis.
- Chassis and dump bed remain fixed in this continuous-rotation demonstration. Steering, suspension and dump-bed actuation are not inferred.
- This is a stationary joint test, not ground-contact rolling simulation. Nominal height, mass and inertia are estimates.
- Tires reduced by 5% and moved outward by 0.006 native units to recover generated wheel-arch clearance.
- Local wheel-well recesses are formed in the fused chassis using each measured tire rotation envelope. These are clearance repairs, not reconstructed suspension mechanics.
- Open boundaries left by tire segmentation are capped with neutral rubber surfaces. Original tire surface UVs are retained; caps are explicit repairs.

## 验证

共5个link、4个可动关节。实际三角网格每1°检查一周，360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0004-casual_dump_truck_g1_bom
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0004-casual_dump_truck_g1_bom 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0004-casual_dump_truck_g1_bom
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0004-casual_dump_truck_g1_bom
```
