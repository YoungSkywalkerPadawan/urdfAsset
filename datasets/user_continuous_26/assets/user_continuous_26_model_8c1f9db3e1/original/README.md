# Gate valve handwheel

源文件：`0015-gate-valve-gs1-1.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The blue rim, spokes, center hub and top fastener form one rotary link. Valve body, flange bolts and yoke remain fixed.
- Axis is fitted to the visible straight central stem between source z=0.26 and 0.32; the fitted axis is not a preset world axis. Positive direction points upward. Actual opening/closing direction is unknown.
- Continuous rotation demonstrates the handwheel degree of freedom only. Internal gate travel, screw pitch, end stops and fluid behavior cannot be recovered from this exterior GLB and are not modeled.
- The fused hub/yoke boundary is separated at source axial height 0.425, locally recessed by 0.002/0.001 and shifted outward by 0.004 source units. Only small holes are capped to preserve the open spoke windows.
- Nominal height 0.55 m, masses and inertias are estimates. Original worn paint and imperfect wheel/spoke geometry are preserved.

## 验证

共2个link、1个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0015-gate-valve-gs1-1
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0015-gate-valve-gs1-1 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0015-gate-valve-gs1-1
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0015-gate-valve-gs1-1
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0015-gate-valve-gs1-1 --time 4 --output pose_at_4s.glb
```
