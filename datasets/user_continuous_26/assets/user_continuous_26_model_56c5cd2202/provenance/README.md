# Suitcase caster wheels

源文件：`0014-front-opening-suitcase-acc8c9452179.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- Each caster tire and its red hub covers form one continuous rotary link. The suitcase, extended handle, open front lid, side tags and caster mounts remain fixed. Caster swivel and lid/handle motion are not included in this continuous-wheel preview.
- Wheel axes are measured from the outer red cap faces; central tire tread circles determine wheel centers. Mixing both cap faces in one plane fit was rejected.
- Positive axes point outward, with opposite-side angle signs. Speeds are scaled inversely with tire radius for an in-place wheel preview; no vehicle translation or ground-contact simulation is claimed.
- Wheels are reduced by 3% and compressed a further 8% axially to separate fused interfaces. Small segmentation holes are capped with rubber-colored material.
- Nominal 0.7 m height, masses and inertias are estimates. Original texture details, side-tag markings and surface irregularities are retained.
- Rotor outlier vertices are limited to radius 0.0335 source units before scaling. Local annular pockets in the fixed mounts use inner radius 0.003, outer radius 0.035 and axial depth 0.066. Textured triangles are clipped while preserving UVs and central pin regions; cut edges remain open, so this is a visual/kinematic mesh rather than a closed manufacturing solid.
- The rendered preview moves from the whole suitcase to a lower-wheel close-up during acceleration, then returns to the whole object while stopping. This camera motion is saved separately from the URDF-driven wheel trajectory.
- The fused caster top leaves an open notch when separated from the mount. Each wheel is completed by retaining its healthy lower half and copying that source geometry and UVs to the upper half with a 180-degree rotation about the fitted axle, then capping remaining seam openings. This uses inferred rotational symmetry and does not preserve every original upper-wheel triangle.

## 验证

共5个link、4个可动关节。主驱动相位每1°采样，累计覆盖720°，其余关节按配置的比例或有限范围随动；实际三角网格在720个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0014-front-opening-suitcase-acc8c9452179
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0014-front-opening-suitcase-acc8c9452179 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0014-front-opening-suitcase-acc8c9452179
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0014-front-opening-suitcase-acc8c9452179
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0014-front-opening-suitcase-acc8c9452179 --time 4 --output pose_at_4s.glb
```
