# 本批第 7 例：已验证电扇结果复用

本例输入 `0007-desk-fan-1bb4d940c799.glb` 与此前电扇 GLB 的 SHA-256 完全相同。保留完整拆分、关节、轨迹和 24 秒视频，并在当前目录重新验证资源加载、URDF/GLB 运动学、逐度旋转间隙与视频解码。复检汇总：`validation/final.json`。本例使用随本目录交付的 `scripts/`，具体复现方式如下。

# 绿色复古电扇：GLB 拆分与 URDF 动画

本项目直接拆分用户提供的 `model (2).glb`，保留三片弧形扇叶、源贴图和旧化外观。没有从基础几何体重新拼装整台电扇。原文件的副本在 `source/model.glb`，SHA-256 为 `a76cb161af01651a8f88fd12024023f5fa918c1693e64c3047ad9a9c5d4acb83`。

## 打开结果

| 文件 | 用途 |
| --- | --- |
| `renders/fan_urdf_animation.mp4` | 24 秒渲染预览，包含启动、匀速、停止、俯仰和组合摇头 |
| `fan_urdf_animated.blend` | 从导出的 URDF/OBJ 重新装配并驱动的 Blender 动画工程 |
| `fan_assembled.blend` | 保留独立刚体、源材质和关节原点的静止装配工程 |
| `fan_animated.glb` | 保留层级、一个动画片段同时驱动三个关节 |
| `fan_static.glb` | 同一装配的静止 GLB |
| `fan.urdf` | 使用相对 mesh 路径的机器人描述 |
| `meshes/`、`materials/` | 各 link 的 OBJ、共用 MTL、两张源 PBR 纹理 |
| `joint_trajectory.json` | 24 Hz、576 个姿态的具名关节轨迹 |

## 刚体与关节

```text
base_link（底部圆缘，固定）
└─ pedestal_fixed → pedestal（底座主体）
   └─ yaw_joint → yaw_carrier（推定摇头支承）
      └─ pitch_joint → motor_head（电机壳）
         ├─ guard_fixed → guard（前后护网及浅色装饰盖）
         └─ rotor_joint → rotor（三片扇叶、轮毂与轴）
```

共 6 个 link、5 个 joint，其中 3 个可动。三片扇叶在同一个 `rotor` 刚体中同步旋转；前护网的浅色装饰盖属于 `guard`，不会随扇叶自转。摇头和俯仰时，电机壳、整个护网和转子共同随动，底座保持不动。

| 关节 | 类型 | 范围 | 声明速度上限 |
| --- | --- | --- | --- |
| `rotor_joint` | `continuous` | 不限圈数 | 100 rad/s |
| `yaw_joint` | `revolute` | −35°～+35° | 1 rad/s |
| `pitch_joint` | `revolute` | −15°～+20° | 1.5 rad/s |

转子主轴由源电机前筒的 29 个圆截面拟合，未直接套用世界轴。其机头局部方向为 `[0.000810613, 0.999993500, 0.003513098]`，相对 +Y 约偏转 0.207°。拟合、原点及误差见 `analysis/motor_axis_fit.json` 和 `joints.json`。这些是生成网格的拟合结果，不能视为实物测量精度。

坐标采用米、X 向右、Y 向后、Z 向上。源 GLB 没有实测尺寸，交付按名义总高 **0.50 m** 缩放；真实尺寸、质量、惯量、摇头/俯仰结构及范围均为推定设计。

## 拆分与修正

源文件为 1 个 mesh、98,767 个三角面、两张 2048×2048 纹理。消除 UV 接缝影响后，大部分结构仍融合在同一连通分量中，因此采用轴向分层、几何连通性、法向连续性和叶片轮廓约束拆分。

已完成多轮“拆分 → 多视角渲染 → 运动检查 → 修正 → 再渲染”：

1. 首轮发现底部细护网被带入转子，以及底叶后缘遗留在固定件中；补回叶背、移除误选护网，并检查孤立转子和 60° 姿态。
2. 从电机圆柱截面拟合主轴，修正轮毂中心和转轴方向。
3. 源模型的叶缘与护网存在穿插；保持叶片曲面，对干涉护网沿轴向让位。随后恢复扫掠范围之外的外圈原形，消除局部拉伸伪影。调整量见 `validation/grille_clearance_adjustment.json`。
4. 将误切进转子的电机端盖归回静止结构。中央界面采用精确三角裁切并插值 UV，保留约 **1.50 mm** 的名义间隙，见 `validation/central_interface_repair.json`。

宽扇叶仍保留源网格的弯曲、扭转、厚度和纹理；中央接口与部分护网经过修正，因此不宣称全部顶点与原 GLB 完全相同。源文件中已有的护网缺杆、不规则卷边和后壳开口仍可见，没有将缺失处冒充为精确重建的实物结构。细节旧化来自原贴图，没有编造品牌或铭牌文字。

原始视图、第一版问题图在 `inspection/`；最终前、侧、背面、单独转子及拆解图在 `renders/`。

## 动画与复现

视频顺序：0–2 秒静止；2–4 秒加速；4–8 秒匀速；8–10 秒减速停止；10–12 秒转子停止并展示推定俯仰；12–14 秒再次启动；14–20 秒摇头和自转组合；20–22 秒减速；22–24 秒停止展示。

演示最高转速 54 RPM，便于观察三片叶形，不代表实机标定转速。轨迹和 GLB 按 24 Hz 保存。视频使用 288 个真实渲染帧（12 Hz），编码为 24 fps；静止段复用相同画面。标题和关节参数置于画面外，不遮挡模型。

动画并非仅在 Blender 手工打关键帧：`animate_fan.py` 重新读取 `fan.urdf` 和对应 OBJ，由 URDF 的父子关系、原点及局部轴计算并驱动各帧，再导出 Blender 与 GLB。`drive_urdf.py` 还可以通过标准 `yourdfpy` 独立加载并复现姿态。

在本目录运行（当前机器环境）：

```powershell
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_urdf.py --time 16 --output pose_16s.glb
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/drive_urdf.py --joint rotor_joint=1.57 --joint yaw_joint=0.3 --output custom_pose.glb
& 'D:\soft\ble\blender.exe' -b --threads 8 --python scripts/animate_fan.py
& 'D:\soft\ble\blender.exe' -b --threads 8 --python scripts/render_animation.py
& 'D:\soft\conda\envs\assembly-comfyui\python.exe' scripts/encode_preview.py
```

如需重新拆分，可先运行 `inspect_source.py` 生成源 Blender 场景，再运行 `build_fan.py`；已包含固定的语义 mask、拟合数据及分析脚本。GLB 导出后自动合并三个同时发生的关节通道为单片段。Blender 导出的首关键帧为 1/24 秒；跨格式验证按轨迹帧号对齐。

## 验证结果与范围

- `validation/clearance.json`：每 1°、共 **360 姿态**，转子源表面与护网、电机壳均无三角相交，中央接触为零。该结果是浮点三角表面的离散检查，不冒充连续运动数学证明或实物公差认证。
- `validation/independent_validation.json`：标准 URDF 加载、资源引用、单树层级、正定惯量与关节限位通过；89 姿态、1,068 次变换比较，最大误差约 `4.9e-16`。
- `validation/drive_trajectory_validation.json`：独立重载姿态、两轮 0→54→0 RPM、摇头组合、关节速度限制均通过。
- `validation/animated_glb.json`：单动画片段含三个关节，6 link 层级正确；8 个时刻与 URDF 轨迹比较，最大矩阵误差约 `4.1e-6`。
- `validation/video.json`：视频完整解码检查。

护网碰撞体由开放环形分段组成，保留内部空腔；没有填满风罩的实心护罩碰撞体。其他碰撞体为简化近似，质量和惯量为名义估计。上述无相交检查使用实际三角表面；该资产以可驱动装配和运动预览为目标，并非经实物标定的动力学模型。

纹理 PNG 保留源字节。Blender/GLB 使用源 PBR 材质；通用 OBJ/MTL 加载器主要读取基础色贴图，其金属度和粗糙度效果可能不同。无需新增网络服务即可打开交付文件。
