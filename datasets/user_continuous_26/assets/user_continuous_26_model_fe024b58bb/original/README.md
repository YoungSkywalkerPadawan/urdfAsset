# Desktop Ferris wheel

源文件：`0008-desktop-ferris-wheel-gs1-1.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- Ten cabin hinges use axes parallel to the measured central spindle. Each is a -1 URDF mimic of wheel_spin, with the same coupling saved in the trajectory.
- Counter-rotation represents gravity-aligned suspension through prescribed kinematics; no pendulum dynamics or gravity simulation is claimed.
- Cabin pivots are estimated from their upper painted arches and nearby suspension pins. Hidden bearings and exact linkages are unknown.
- To correct collisions in the fused generated mesh, cabins are scaled to 90% about their hinges, compressed a further 40% along the axle and centered between the wheel frames. Small segmentation holes of at most 12 edges are capped; existing window openings remain.
- Wheel frames are separated about an axial half-gap of 0.047 source units, except at suspension pins. Shaft radial clearance is 0.036 source units. Pin annuli, unintended cross-cavity sheets and disconnected front text shards are omitted; counts are recorded in analysis/axis_fit.json.
- The rear sun plate and front axle cap are fixed. Original inner support rods are reassigned to fixed links and shifted by 0.080 and 0.065 source units toward the front and back respectively; the front cap moves forward 0.040. Outer support upper portions are locally moved away from the swept wheel. These are inferred mechanical clearance repairs, not recovered CAD dimensions.
- Original UVs and textures are retained. Incomplete source cabin surfaces and low-detail base lettering remain limitations.
- Nominal 0.5 m height, masses and inertias are estimates.

## 验证

共15个link、11个可动关节。实际三角网格每1°检查一周，360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0008-desktop-ferris-wheel-gs1-1
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0008-desktop-ferris-wheel-gs1-1 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0008-desktop-ferris-wheel-gs1-1
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0008-desktop-ferris-wheel-gs1-1
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0008-desktop-ferris-wheel-gs1-1 --time 4 --output pose_at_4s.glb
```
