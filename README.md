# URDF 资产库

按来源收录已有的 **1,330 个装配资产或 CAD 部件对**，用于查找、三维预览、父子部件关节轴测试与训练数据读取。这里保存的是数据与参考标注，不是模型预测结果，也不是各公开数据集的全量镜像。

## 数据目录

| 来源 | 资产 / CAD 对 | continuous 轴 | 有限旋转辅助轴 | 冻结评估可用 continuous 轴 | 完整原始 URDF |
|---|---:|---:|---:|---:|---:|
| [Articraft](datasets/articraft/README.md) | 340 | 674 | 0 | 674 | 340 |
| [ArtVIP](datasets/artvip/README.md) | 54 | 203 | 0 | 203 | 0 |
| [Fusion Joint](datasets/fusion_joint/README.md) | 300 | 300 | 0 | 300 | 0 |
| [URDF files](datasets/urdf_files/README.md) | 62 | 316 | 0 | 308 | 59 |
| [GRScenes](datasets/grscenes/README.md) | 48 | 0 | 93 | 0 | 0 |
| [Infinigen-Articulated](datasets/infinigen_articulated/README.md) | 500 | 0 | 500 | 0 | 500 |
| [自有 26 个物体](datasets/user_continuous_26/README.md) | 26 | 65 | 4 | 65 | 26 |
| 合计 | **1330** | **1558** | **597** | **1550** | **925** |

“完整原始 URDF”指已附带并检查相对路径引用的网格文件；不表示通过了物理仿真验收。其中 559 个由上游 URDF 补齐网格、材质与纹理，并将资源引用改为仓库内相对路径，关节与局部坐标语义保留，修改及校验记录见 `original/PORTABILITY.json`。另外 402 个资产的原生格式为 USD/CAD；3 个 URDF files 资产在上游缺少依赖，具体文件列在该来源说明中。所有 1330 个资产均保留可直接读取的已分件 `scene.glb`、参考轴和点云。

- [全局资产索引 JSON](catalog.json) / [CSV](catalog.csv)：名称、来源、部件数、轴数、用途、隔离状态、原始 URDF 入口和数据划分。
- [冻结 continuous 基准](benchmarks/continuous_axis_v2/README.md)：777 个资产、1550 条轴，train/val/test 为 1234/166/150。
- 另 8 条异常轴保留在原资产与隔离清单中，不混入默认评估。一个物体有多条轴时逐轴索引，物体/家族划分保持一致。

## 下载与查看

几何、点云、视频和归档使用 **Git LFS**。首次完整下载为数 GB；不能只下载 GitHub 的普通源码 ZIP 来代替 LFS 拉取。

```bash
git lfs install
git clone https://github.com/YoungSkywalkerPadawan/urdfAsset.git
cd urdfAsset
git lfs pull
python -m http.server 8768 --bind 127.0.0.1
```

浏览器打开 **http://127.0.0.1:8768/**。支持按来源、类型和名称筛选，选择物体中的具体关节，查看参考轴并播放单关节运动。前端依赖已附带，无需 CDN。Windows 也可运行 `start_preview.cmd`。

只取某个来源，先跳过自动下载，再按目录拉 LFS：

```bash
# Bash / AutoDL
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/YoungSkywalkerPadawan/urdfAsset.git
cd urdfAsset
git lfs pull --include="datasets/user_continuous_26/**" --exclude=""
```

```powershell
# PowerShell
$env:GIT_LFS_SKIP_SMUDGE = "1"
git clone https://github.com/YoungSkywalkerPadawan/urdfAsset.git
Remove-Item Env:GIT_LFS_SKIP_SMUDGE
cd urdfAsset
git lfs pull --include="datasets/user_continuous_26/**" --exclude=""
```

按需拉取时只有已下载来源能显示网格；索引仍包含全部来源。

## 每个资产的内容

```text
datasets/<来源>/assets/<稳定资产 ID>/
  registry.json          # 本仓库索引与评估状态
  asset.json             # 来源、完整结构摘要、部件映射、坐标与检查记录
  joints.json            # 已筛选关节的参考轴、类型、parent/child、mimic
  scene.glb              # 已分件、米制公共世界坐标下的参考装配
  inputs/link_XXX.npz     # 原有点云池，保留原始点数和字段
  source.tar.gz          # 原始包或描述/许可摘录，范围按来源说明
  original/              # 已补齐的原始 URDF 与资源；可移植副本附 PORTABILITY.json
  source_descriptions/   # 其他来源包中可展开的原始描述和许可
  preview.mp4            # 自有物体已有的整机动画（如存在）
  provenance/            # 自有资产的整理、修正与质量说明（如存在）
```

原始数据未被重新居中或重新缩放；点云池不重新采样。reference GLB 与轴标签使用米制公共世界坐标，已应用来源单位换算。`original/` 保留各源 URDF 自身的局部坐标，部分资源路径作了可移植化修改；不应直接拿其局部顶点与 world-frame 标签比较。

## 查找与测试

索引查询不需要 GPU 或第三方库：

```bash
python tools/catalog.py --source user_continuous_26
python tools/catalog.py --type continuous --eligible --split test
python tools/catalog.py --source articraft --search fan --json
```

读取父子部件点云和独立标签：

```bash
pip install -r requirements.txt
```

```python
import json
from pathlib import Path
from tools.load_pair import load_pair

root = Path(".")
row = json.loads((root / "benchmarks/continuous_axis_v2/test.jsonl").read_text(encoding="utf-8").splitlines()[0])
features, label = load_pair(root / row["asset_path"], row["joint_index"], points=2048)
# features: parent_xyz / child_xyz / parent_normals / child_normals
# label: type / origin_world / direction_world / mimic / joint_name
# 输入与标签分开返回；坐标仍为世界米制，归一化由训练/推理适配器决定。
```

需要单个关节的可加载 URDF 时，可由 GLB 和参考轴生成一个**派生父子部件对**：

```bash
python tools/export_pair_urdf.py --asset datasets/<来源>/assets/<资产ID> \
  --joint-index 0 --output exports/my_pair
```

输出 `model.urdf`、两个 STL 和出处说明。有限转动须显式加 `--allow-bounded`，不会自动改成 continuous。该导出只包含指定父子对；不重建整机层级，不合并子树，不模拟 mimic 联动，也不提供物理质量、惯量或碰撞参数。完整原始 URDF 可通过 `catalog.json` 的 `original_urdfs` 字段找到。

## 校验与来源

```bash
python tools/validate.py
python tools/validate.py --hashes   # 读取全部文件校验 SHA-256
python -m unittest discover -s tools -p "test_*.py" -v
```

校验结果见 [IMPORT_REPORT.json](IMPORT_REPORT.json)，文件校验清单见 [FILES.sha256.jsonl](FILES.sha256.jsonl)。清单记录实际文件内容，而非 LFS 指针；清单自身、校验报告、Git 元数据与本地导出不参与清单，避免循环依赖。允许只取一个来源时，使用 `--source <来源>` 校验该来源。

来源、版本、修改记录与条款保留在每个 `asset.json` 和各来源说明中。Fusion 部分是 **Fusion 360 Gallery Dataset 的经筛选派生子集**，仅限非商业研究并适用所附原许可；GRScenes 为 CC-BY-NC-SA-4.0；Articraft / Infinigen 为 CC-BY-4.0；ArtVIP 数据卡声明 Apache-2.0；URDF files 随各上游资产条款；自有资产未额外授予第三方再分发许可。不能用一个统一许可替代这些来源条款。

数据标签来自生成、作者/CAD 标注或自有几何整理，未全部经过实物测量或机械验收。轴线方向正负等价、轴上原点可沿轴移动；评估时应使用轴线误差，避免对原点直接做唯一点误差。

2026-09-15 首次整理并从 AutoDL 补取原始 URDF 依赖。范围是此前已经筛选处理的资产；未镜像全部上游数据，也未补齐原生 USD 依赖层。原有 1550 条 continuous 基准及物体/家族划分保持不变。
