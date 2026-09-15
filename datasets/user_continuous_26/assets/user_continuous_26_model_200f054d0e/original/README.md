# Tilted-head stand mixer

源文件：`0025-stand-mixer-c0c754aeec9a.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The source head is raised and its output shaft is tilted. The whisk and its coupling form one continuous rotor around the measured shaft, while the bowl, base, head and controls stay fixed.
- No planetary orbit, gear ratio, head tilt range or hidden linkage is inferred. The animation is an in-place shaft and cage demonstration, not mixing food or simulating contact.
- The whisk retains original wire surfaces and UVs; only small holes are capped, preserving cage openings. A reviewed inside-bowl region excludes the reflective bowl wall.
- The whisk is scaled to 84% around its joint and shortened a further 8% along the shaft to clear the bowl rim throughout rotation in the generated raised-head pose. The original 90% trial still struck the inner rim. A small coupling recess separates the fused head interface; these are explicit geometric repairs.
- Nominal 0.42 m height, masses and inertias are estimates; the original GLB remains unchanged.
- Two detached source coupling caps (components 62 and 66) are moved 0.045 native units toward the shaft and 0.074 inward from either side; they remain in the same rotating rigid body. This is a documented placement repair.
- Residual collisions after the bowl cleared were at the output coupling, not the cage. The fixed annular coupling recess has radius 0.044 and depth 0.060 native units, preserving the central 0.007-radius pin region. Further cage shrink trials were rejected.

## 验证

共2个link、1个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0025-stand-mixer-c0c754aeec9a
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0025-stand-mixer-c0c754aeec9a 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0025-stand-mixer-c0c754aeec9a
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0025-stand-mixer-c0c754aeec9a
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0025-stand-mixer-c0c754aeec9a --time 4 --output pose_at_4s.glb
```
