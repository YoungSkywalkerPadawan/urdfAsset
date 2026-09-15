# Microscope knobs and objective turret

源文件：`0019-gs1-microscope-realistic-001.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- Four large adjustment knobs and the objective turret receive continuous joints. The light outer turret rim, black lower plate and all attached silver objective bodies form one rigid link; the upper microscope tube and support remain fixed.
- Each knob pair uses the line between independently fitted cylinder centers as its common shaft axis. The right-hand knob mimics its left partner with negative angle because both local axes point outward.
- The turret axis comes from a measured mounting-plane normal, with its origin refined by an outer-rim circle. It is inclined approximately 21.4 degrees from vertical toward positive source Y, not assigned a preset world Z axis.
- The two knob pairs and turret are independent drivers. Turret demo speed is 0.65 times the knob speed; actual focus lead, optical indexing detents and gear ratios are unknown.
- Knobs are reduced 2%, shifted outward 0.003 source units and separated by local radius 0.055, depth 0.014 source-unit cavities. The turret is shifted outward along its underside by 0.006 source units, with its fused interface separated locally.
- The stage, mirror/illumination assembly, eyepiece, focus supports and base remain fixed. Focus translation, optical behavior and small unverified adjustment screws are not modeled.
- Nominal height 0.38 m, masses and inertias are estimates. Original textures and generated-surface imperfections remain.

## 验证

共6个link、5个可动关节。主驱动相位每1°采样，累计覆盖720°，其余关节按配置的比例或有限范围随动；实际三角网格在720个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0019-gs1-microscope-realistic-001
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0019-gs1-microscope-realistic-001 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0019-gs1-microscope-realistic-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0019-gs1-microscope-realistic-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0019-gs1-microscope-realistic-001 --time 4 --output pose_at_4s.glb
```
