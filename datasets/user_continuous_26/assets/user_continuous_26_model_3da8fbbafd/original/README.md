# Tripod telescope azimuth and tilt

源文件：`0021-gs1-tripod-telescope-fantasy-001.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The tripod stays fixed. The azimuth head carries the mounting cradle and the telescope pitch joint, so the pitch axis follows the azimuth rotation in the URDF hierarchy.
- Azimuth uses a measured annular face normal, with its center averaged from four horizontal rim-circle sections. Free fits to the short irregular base cylinder produced implausible large tilts and were rejected.
- The pitch axis is the line between the two measured outer trunnion-cap centers. Telescope tube, end rims and its small attached sight-like object form one rigid child link. Its visible caps remain with the cradle.
- The small object above the front tube has an axis nearly parallel to the telescope. It is not reliably identifiable as a rotary adjustment knob, so it stays fixed to the tube.
- Pitch range 0 to 0.15 rad (about 8.6 degrees) is an inferred lift range from the source pose; actual mechanical stops are unknown. Tripod leg adjustment, lock-screw travel and optical behavior are not modeled.
- The azimuth fused interface is separated by local axial recesses of 0.003 and 0.002 source units. Tube width along the pitch axis is reduced by 3% at the cradle interface; only small split openings are capped.
- Nominal height 0.9 m, masses and inertias are estimates. Source turquoise paint, wear, metal bands and decorative tripod geometry are retained.
- The full front mouth is grouped with the tube. Near the pitch trunnion, the fixed cradle inner faces are spread to axial +/-0.080 source units within radius 0.075, fading over another 0.025, to separate the fused fork/tube interface.
- Long fused triangles that still bridged the spread fork are clipped within a local pitch-axis cylinder of radius 0.083 and axial depth 0.150. This acts on actual triangle surfaces and preserves the open cradle cavity.

## 验证

共3个link、2个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0021-gs1-tripod-telescope-fantasy-001
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0021-gs1-tripod-telescope-fantasy-001 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0021-gs1-tripod-telescope-fantasy-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0021-gs1-tripod-telescope-fantasy-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0021-gs1-tripod-telescope-fantasy-001 --time 4 --output pose_at_4s.glb
```
