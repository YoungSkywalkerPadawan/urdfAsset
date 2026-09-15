# 公开关节数据整理（2026-09-11）

这轮目标是为“已分件几何 → 父子部件关节轴”建立可追溯的数据入口，并优先筛选持续旋转关节。原始数据的可下载性、原始标注含义、转换成功数量分别记录，不能把论文规模当作已处理规模。

## 来源与用途

| 数据来源 | 官方入口 | 本轮处理方式 / 状态 |
| --- | --- | --- |
| Articraft-10K | https://huggingface.co/datasets/camvsl/Articraft-10K | 前一批已交付 340 个资产、674 个 continuous 关节；该批约 2GB 包的大部分是高密度点云。 |
| ArtVIP | https://huggingface.co/datasets/X-Humanoid/ArtVIP | 官方发布目录 476 个物体；下载全部 USD 几何层，解析 USD 关节与双侧坐标，筛选无限旋转。Apache-2.0 数据卡声明。 |
| GRScenes | https://huggingface.co/datasets/InternRobotics/GRScenes | 商业 / 家庭场景中的 articulated 物体；按 ZIP / 分卷 ZIP 中的文件选择下载，不下载整套场景纹理。CC-BY-NC-SA-4.0。 |
| Understanding URDF | https://github.com/Daniella1/urdf_files_dataset | 完整仓库中 `.urdf` / `.URDF` 模型清查，保留原始 continuous；资产来自多个上游，逐包保存许可证，不能把仓库代码许可当成所有模型的许可。 |
| Infinigen-Articulated | https://huggingface.co/datasets/princeton-vl/infinigen-articulated | 首批下载 pepper_grinder 类全部 500 个资产；均为 ±π 的 revolute，转换为独立的有限旋转轴辅助集。其余 16 类尚未全量下载。CC-BY-4.0。 |
| Fusion 360 Gallery Joint / JoinABLe | https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/docs/assembly_joint.md | 接入独立的 CAD 部件对数据；含关节轴、限位开关、接触面、孔洞；几何原始单位 cm，需转 m。仅非商业研究的自定义许可。实际转换状态以运行报告为准。 |
| Lightwheel | https://github.com/LightwheelAI/Lightwheel-simready-asset | 找到官方 259 个资产的 3.41GB 包；本机可访问文件页，实际下载返回 Google Drive Quota exceeded。未绕过下载配额。CC-BY-NC-4.0，要求 lightwheel_ 名称归属。 |
| Shape2Motion | https://github.com/wangxiaogang866/Shape2Motion | 官方 Google Drive 文件返回 404；ANCSH 原始下载站入口也已检查，记录在下载审计中。普通 rotation 标注不能自动当 continuous。 |
| AKB-48 | https://github.com/liuliu66/AKB-48/blob/gh-pages/download.html | 找到作者正式下载页中的 Google Drive 文件夹，当前返回 404；RobotFlow 网站对应卡片的链接是空占位。 |
| PartNeXt | https://huggingface.co/datasets/AuWang/PartNeXt | 数据卡字段为部件分割 / 层级，没有关节轴标注；可用于分件预训练，不能直接作为本轮轴监督数据。仅保存元数据审计。 |
| SketchMobility / Sketch2Arti | https://huggingface.co/datasets/Arlo397/SketchMobility | 数据文件有访问申请 / 条款门槛；未下载。其数据混合 Articraft、Infinigen、PartNeXt、Shape2Motion，未来加入时必须跨来源去重。 |
| PartNet-Mobility / ShapeNet 派生数据 | https://sapien.ucsd.edu/ | 用户尚未完成 ShapeNet 注册，按用户要求暂缓相关来源。 |
| URDF-Anything+ | https://huggingface.co/datasets/URDF-Anything-plus/Dataset | 数据卡明确要求 ShapeNet 注册并同意条款；按用户回复暂缓。 |
| PhysX-Mobility | https://huggingface.co/datasets/Caoza/PhysX-Mobility | 来自 PartNet-Mobility；随上游授权一起暂缓。 |

## 论文与数据复用

- PARTICULATE：使用 PartNet-Mobility、Lightwheel、GRScenes 等来源；不能给每篇论文重复计算一套独立数据。
- Instruct-Particulate：公开推理资源不等于其全部约 150k 训练数据已经发布；已接入可验证公开的 Articraft。
- Articulate-Anything、ArtLLM：官方说明引用 PartNet 系数据，先跟随上游授权状态处理。
- URDFormer：官方代码 README 的训练数据生成 / 训练说明仍标注 coming soon；公开示例和权重不能当成完整训练集发布。
- ANCSH：作者 README 说明大学 Google Drive 重置后正在恢复数据；使用 Shape2Motion / PartNet 等上游，不将失效下载误报为已处理。
- JoinABLe：独立 CAD 关节数据入口，特别适合检查接触面、圆柱面、孔洞等几何线索。

## 标注与质量规则

1. URDF 只将原始 `type="continuous"` 作为持续旋转正样本。
2. USD 仅在 RevoluteJoint 两端限位分别为 -inf / +inf 时按 unlimited rotation 收录。保存原始类型、原始限位和转换依据；有限的 360° 范围不自动升级为 continuous。
3. 每个 USD 关节独立计算 body0 / body1 的世界原点和轴，误差超过容差的样本进入排除记录。
4. GLB 采用世界坐标、米制；每个目标部件 8192 点及法线。Fusion 另存 BRep 面编号和接触面辅助标签，默认训练读取器不把这些标签用作输入。未显式声明 USD 单位时使用 schema 默认厘米，并保留警告；尚未逐例核实物理尺寸。
5. 有限旋转辅助样本保留 revolute 类型；预览在原始限位内摆动，不能进入 continuous 分类正样本池。
6. `source.tar.gz` 是原始描述 / 许可证摘录包，不包含重复的所有网格与纹理，USD 摘录可能不能独立重放。完整下载的原始几何、关节描述保留在 AutoDL；Fusion 解压校验后移除重复压缩归档，保留完整目录清单和哈希。`asset.json` 记录源文件与哈希。
7. 格式 / 坐标校验不等于机械合理性验证，未进行碰撞、接触仿真，也未将样本标成“人工验收通过”。
8. 同一物理模型的不同 URDF、同一生成家族、同一资产在不同数据集的副本必须按组划分训练 / 验证集，不能按单关节随机划分。
9. Fusion 仅将 RevoluteJointType 且两个限位开关均明确为 false 的约束收录为 unlimited revolute；这是 CAD 约束语义，未证明实物运动无碰撞。完整关节集清查和有预算限制的几何预览分别统计。

AutoDL 工作目录：`/root/continuous-public-data-20260911`。固定版本、下载目录清单、逐样本排除原因、运行统计位于该目录的 `catalogs/` 和 `reports/`。最终实际数量以下载到本地的 `manifest.json` / 运行报告为准。
