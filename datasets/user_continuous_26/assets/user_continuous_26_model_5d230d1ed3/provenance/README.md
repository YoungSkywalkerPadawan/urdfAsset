# Stroller wheel assembly

源文件：`0013-folding-stroller-001.glb`。直接拆分原 GLB，保留源 UV 与材质。

- 动画：`renders/preview.mp4`（10 秒；静止、加速、持续转动、减速停止）。
- Blender：`animated_urdf.blend`；静态装配：`assembled.blend`。
- GLB：`model_animated.glb`（一个片段包含全部可动关节）；`model_static.glb`。
- URDF：`model.urdf`，依赖同目录 `meshes/` 和 `materials/`，路径为相对路径。
- 关节轨迹：`joint_trajectory.json`，24 Hz；视频12 Hz实际渲染、24 fps编码。
- 分区与轴证据：`analysis/`、`case.json`、`joints.json`。

## 本案例设定与推定

- Four tire/hub assemblies receive independent continuous joints. Caster steering, folding, canopy and seat adjustment remain fixed in this wheel-motion case.
- Front wheel rim centers in the generated mesh are offset from the visible axle caps by about 0.02 source units. Joint origins follow the axle caps; outer tire/rim surfaces are translated to those centers, with a smooth transition through the spokes between radii 0.015 and 0.050. These are explicit geometric repairs of the source, not recovered manufacturing dimensions.
- Rear wheel axes and centers are fitted from their tire bands and thin wheel planes. Positive axes point outward; opposite-side velocity signs make all wheels turn in the same travel sense.
- Angular speeds are inversely proportional to the fitted tire radii for this in-place demonstration. Vehicle translation and contact dynamics are not simulated.
- Wheels are reduced by 5% and compressed a further 12% axially for clearance; small segmentation holes are capped while spoke openings remain.
- Nominal 1.05 m height, masses and inertias are estimates. Source fabric and frame irregularities are retained.
- Rear inner supports are recessed to axial -0.040 source units locally while retaining the central shaft. Front-wheel side faces are limited to axial +/-0.016 before scaling and their radial envelope to 0.069, close to the fitted 0.068 tire radius, to remove projecting fork remnants. An annular pocket, inner radius 0.010, outer radius 0.081 and depth 0.045 source units, removes intersecting fork surfaces while retaining the central pin. It uses 96-sided convex clipping of the actual textured triangles rather than assuming a watertight solid; UVs are interpolated and cut edges are left open. The fork wedge is explicitly excluded from rotating parts.
- Each front wheel receives a 0.012-source-unit-radius axle bore so the retained fixed central pin does not intersect its rotating hub.

## 验证

共5个link、4个可动关节。主驱动相位每1°采样，累计覆盖720°，其余关节按配置的比例或有限范围随动；实际三角网格在720个姿态未发现相交。检查保留固定件空腔，不使用填满空腔的凸包。离散浮点检查不构成连续旋转的数学证明，也不等于对任意多关节组合的穷举。

动画由导出的URDF重新读取原点、轴、父子关系及OBJ后驱动；标准yourdfpy另行加载检查。材料金属度/粗糙度以Blender和GLB的PBR表现为准，部分OBJ加载器仅显示基础色。碰撞mesh为实际表面；不同动力学引擎对非凸动态mesh的支持不同，质量惯量未实物标定。

## 复现

从 `assembly-output` 目录运行共用脚本：

```powershell
& 'D:\soft\ble\blender.exe' -b --python scripts/build_case.py -- cases/0013-folding-stroller-001
& 'D:\soft\ble\blender.exe' -b --python scripts/check_case_motion.py -- cases/0013-folding-stroller-001 1
& 'D:\soft\ble\blender.exe' -b --python scripts/animate_case.py -- cases/0013-folding-stroller-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/finish_case.py cases/0013-folding-stroller-001
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_case.py cases/0013-folding-stroller-001 --time 4 --output pose_at_4s.glb
```
