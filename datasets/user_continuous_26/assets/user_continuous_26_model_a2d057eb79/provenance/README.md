# Race kart four wheels

源文件：`0022-race-car-gs1-3.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- Four continuous wheel joints use the fitted left/right tread centers; opposite outward axis signs are compensated in the trajectory for a common rolling direction.
- The steering wheel, steering linkage, suspension, seat and engine remain fixed. This is an in-place wheel test, without tire contact dynamics or vehicle translation.
- Wheels retain original UVs, are reduced 2%, compressed another 10% along their axles and shifted outward 0.022 source units to clear fused suspension strips. Small shaft bores and bearing recesses repair fused interfaces; these are inferred clearances.
- Nominal height 0.65 m, masses and inertias are estimates. Source mesh shape irregularities are retained; original GLB remains unchanged.

## 验证

共5个link、4个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0022-race-car-gs1-3
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0022-race-car-gs1-3 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0022-race-car-gs1-3
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0022-race-car-gs1-3
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0022-race-car-gs1-3 --time 4 --output pose_at_4s.glb
```
