# Rotating cutting table

源文件：`0024-rotating-cutting-table.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The circular top platter including its radial lattice and outer rim forms one continuous rotor. The lower cylindrical pedestal remains fixed.
- The small upper cutting roller has its own continuous axle; the upper frame, wide blade-like plate and vertical handle remain fixed. The static GLB does not establish additional feed or linkage motions.
- The table axis uses the measured plane of the complete thin outer rim and its robust circle center; a short-cylinder candidate that tilted the platter was rejected. The roller axis follows its cylindrical tread. Positive directions and multiplier 2 are visualization settings, not recovered transmission ratios.
- A small horizontal seam separates the fused platter from its pedestal. The roller is scaled to 95%, with an annular fork clearance and a central shaft bore. These are explicit geometric repairs; original UVs are preserved.
- The source contains malformed lattice spokes and an incomplete upper support arrangement. This is a visual and kinematic articulation, without a fabricated hidden support mechanism or material-cutting simulation.
- Nominal 0.6 m height, mass and inertia are estimates. The source GLB remains unchanged.
- The roller radius is limited to 0.0565 native units before 95% scaling to remove long fused triangles extending into the upper fork.
- The center fork is retained in the gap between the paired roller faces. A 0.0065-radius fixed axle pin and short center support are added as an explicitly inferred connection; they are not recovered source triangles. The roller center gap is 0.032 native units wide.

## 验证

共3个link、2个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0024-rotating-cutting-table
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0024-rotating-cutting-table 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0024-rotating-cutting-table
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0024-rotating-cutting-table
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0024-rotating-cutting-table --time 4 --output pose_at_4s.glb
```
