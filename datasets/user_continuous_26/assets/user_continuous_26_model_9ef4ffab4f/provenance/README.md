# Kinetic orbital ornament

源文件：`0023-perpetual-motion-machine-ce4fab940bc5.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The central ball, inner curved rods, dark orbit balls and the middle YZ ring form one rigid rotor. The largest outer rings, upright rod, outer bearing decorations and base remain fixed.
- The lower central cylindrical collar supplies the axis. The static source does not establish a complete working gimbal or energy mechanism; the single inner-rotor degree of freedom is an explicitly inferred kinematic design. This animation does not model a perpetual-energy device.
- The generated outer arcs have pre-existing gaps and irregularities. They are preserved rather than invented into a complete mechanism; the original GLB remains unchanged.
- The rotor is scaled to 90% and bored around the fixed upright with radius 0.028 native units. This repairs the original overlapping concentric surfaces. Small cut boundaries are capped where possible; true ring openings remain open.
- Nominal 0.3 m height, masses and inertias are estimates; initial positive direction and speed are demonstration choices.

## 验证

共2个link、1个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0023-perpetual-motion-machine-ce4fab940bc5
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0023-perpetual-motion-machine-ce4fab940bc5 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0023-perpetual-motion-machine-ce4fab940bc5
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0023-perpetual-motion-machine-ce4fab940bc5
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0023-perpetual-motion-machine-ce4fab940bc5 --time 4 --output pose_at_4s.glb
```
