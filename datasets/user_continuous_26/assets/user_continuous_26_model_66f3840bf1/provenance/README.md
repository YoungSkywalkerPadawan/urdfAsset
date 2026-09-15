# Four-sail wheat mill

源文件：`0026-wheat-mill.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The four cloth sails, their wooden spars and front hub form one rigid rotor with one continuous joint. Each sail retains its fixed position relative to the hub.
- The axle connects the measured front hub center to the mean of three exposed rear-shaft section centers. An initial cylinder fit contaminated by the roof was rejected. Tower, roof and rear shaft remain fixed; internal milling gears and roof yaw are not inferred.
- Small local interface recesses and a 0.003-native-unit outward shift separate the generated fused shaft interface. Original sails, thickness irregularities, UVs and materials are preserved.
- Rotation direction and speed are demonstration choices. Nominal 0.65 m height, mass and inertia are estimates; the source GLB remains unchanged.

## 验证

共2个link、1个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0026-wheat-mill
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0026-wheat-mill 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0026-wheat-mill
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0026-wheat-mill
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0026-wheat-mill --time 4 --output pose_at_4s.glb
```
