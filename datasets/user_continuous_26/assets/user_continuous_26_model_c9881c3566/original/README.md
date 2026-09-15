# Folding scooter wheels

源文件：`0012-folding-scooter-001.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- This continuous-motion case articulates the two wheels. Steering, folding latch, brake and telescoping handle remain fixed; their other degrees of freedom are not demonstrated.
- Each axle follows the measured thin wheel plane; outer tire bands determine centers and nominal radii. Positive axes point toward the same side of the scooter.
- The rear wheel speed is scaled by the fitted radius ratio to match the front wheel peripheral speed. This is an in-place wheel-drive preview without vehicle translation or contact dynamics.
- Wheels are reduced by 4% and compressed a further 15% along their axles to recover fork clearance. Small segmentation holes of at most 12 edges are capped; spoke openings remain. Tires, hubs and disconnected spokes are grouped despite belonging to separate source components.
- Nominal 0.9 m height, masses and inertias are estimates. The source GLB remains unchanged and original materials/UVs are retained.
- A small number of front-wheel vertices extending beyond radius 0.106 source units are clamped to that envelope before scaling to clear the fixed fender. This is a geometric repair, not a recovered tire dimension.
- Disconnected thin front-edge fragments outside the wheel hub are omitted from the derived mesh; their count is recorded in the axis report. The main tire, spokes and fender are retained. This cleanup avoids thin detached sheets rotating around the tire.

## 验证

共3个link、2个可动关节。主驱动相位每1°采样一周，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0012-folding-scooter-001
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0012-folding-scooter-001 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0012-folding-scooter-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0012-folding-scooter-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0012-folding-scooter-001 --time 4 --output pose_at_4s.glb
```
