# Office chair swivel and six casters

源文件：`0020-gs1-office-chair-realistic-001.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- The source GLB has six caster positions. That generated topology is preserved rather than replaced with a presumed five-leg chair base.
- Seat, back, armrests, under-seat controls and exposed upper piston form one rotating seat assembly. Its axis is fitted to the long metallic central piston. Base legs and lower column remain fixed.
- Each caster uses its measured outer cap plane normal and a rim circle for the axle center; its orientation is not set to the seat axis or a shared world axis. Coaxial wheels within one caster are grouped into one rigid rotor for this preview.
- Caster swivel, height adjustment, reclining and control-lever motion are not included. Wheel groups roll in place at three times the seat demo speed; this does not prescribe a common ground velocity or simulate chair translation.
- Complete source caster surfaces are retained, with split boundary openings capped. Wheels shrink 3% and an additional 4% axially; radial outliers are limited to 0.0307 source units. Local fixed-mount annular pockets have inner radius 0.003, outer radius 0.032 and depth 0.120.
- The initial half-symmetry wheel repair was rejected after rendering showed visible seams; the final wheels retain their complete source surfaces. Original upholstery, frame, controls, materials and remaining surface imperfections are retained.
- Nominal height 1.05 m, masses and inertias are estimates. This is a kinematic visual preview, not calibrated seating or ground-contact dynamics.
- At the seat swivel interface, a radius 0.020 source-unit bore is clipped in the fixed gas-lift sleeve. The moving shaft root is limited to radius 0.0168 within an axial interval of -0.040 to 0.035 around the joint, with a radial fade beyond 0.040. This separates fused collar fragments without changing the upholstered seat.

## 验证

共8个link、7个可动关节。主驱动相位每1°采样，累计覆盖360°，其余关节按配置的比例或有限范围随动；实际三角网格在360个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0020-gs1-office-chair-realistic-001
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0020-gs1-office-chair-realistic-001 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0020-gs1-office-chair-realistic-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0020-gs1-office-chair-realistic-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0020-gs1-office-chair-realistic-001 --time 4 --output pose_at_4s.glb
```
