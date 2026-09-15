# Cipher dial

源文件：`0009-escape_cipher_dial_g1_bom.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The ticked dial and central knob form one rigid rotor. The lower mounting flange and dark housing remain fixed. Hidden lock tumblers and detents are not reconstructed.
- Axis follows the central cylindrical knob. A 17-degree-inconsistent short-sidewall cylinder candidate was rejected; it is retained in the fit report. Positive direction points outward. The real dialing direction is not inferable from the static GLB.
- Rotor is reduced by 2% and raised 0.006 source units to repair the fused interface. Split boundaries are capped with bronze-colored material.
- Nominal height 0.16 m and mass/inertia are estimates.
- The jagged triangle cut is flattened locally on each side of the interface: the fixed flange stops at axial -0.004 and the rotor starts at +0.002 source units before its 0.006 offset. This removes residual fused triangles without changing the visible upper dial.

## 验证

共2个link、1个可动关节。实际三角网格每1°检查一周，360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0009-escape_cipher_dial_g1_bom
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0009-escape_cipher_dial_g1_bom 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0009-escape_cipher_dial_g1_bom
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0009-escape_cipher_dial_g1_bom
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0009-escape_cipher_dial_g1_bom --time 4 --output pose_at_4s.glb
```
