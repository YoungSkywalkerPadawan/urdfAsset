# 持续旋转轴预测 v2

输入已知父子部件的静态几何，并已知该关节是 continuous，输出一条轴的原点与方向。每条父子边独立预测；不预测分件、父子图、关节类型、速度或限位。多个网格节点可共同组成一个部件。

本目录独立于 `experiments/continuous_axis_train`，保留 v1 代码、缓存和划分。先在 CPU 上检查实现，再由用户开启 GPU 后测显存和训练。CPU 检查不是模型效果评测。

## 输入与网络

每个部件每次采样 2048 点，包含 XYZ、法向与网络内的父子身份嵌入。点缓存为每个 link 最多 8192 点；已有缓存未覆盖的轴孔细节不能靠加密采样恢复，后续可独立比较更密集的原始 mesh 采样。

1. 父子共用 child 中心和尺寸建立坐标系；child 的 0.5%/99.5% 点坐标分位数包围盒中心、对角线决定这个坐标系。父件不会单独居中，安装关系得到保留。
2. 坐标噪声标准差为 child 尺寸的 0.1%，裁剪至三倍标准差；同时旋转几何、法向和轴标签。投影标签依据增强后的实际输入点重算。
3. A/B 使用整体均匀采样。C/D 各保留至少 50% 整体均匀点，剩余点按对件表面距离软加密；几何距离、法向与采样不读取关节标签。
4. 共享局部几何编码和两层父子交叉注意力。C/D 同时使用 child 尺度细节、pair 尺度整体分支和 24/96 点邻域。
5. C/D 的 64 个 anchor 中至少一半来自全局 FPS，其余在接近对件的半个点云中 FPS。接近区域用对件至多 128 个 FPS 点近似；最终接触特征仍查询完整输入点云。全局与局部 anchor 允许重合。
6. 独立方向头输出单位方向。projection 头预测 child 各点到轴的垂直偏移，得到逐点轴投影，均值聚合并投影为距 child 参考中心最近的轴上点。无候选轴生成或评分。

方向正负等价，原点沿轴平移等价。位置、投影、共线性和运动损失都采用向量范数上的 Huber，避免逐坐标损失随整体旋转而变化。几何损失使用 float32。

运动辅助监督由预测单轴解析旋转 child，与标注轴产生的同点对应轨迹比较；使用 45°、90°，每个样本的所有点和角度统一选择轴方向正负。它保持刚体，且仅重表达已有轴标签，不是额外真实运动数据。圆盘等对称物体不能仅靠旋转后无对应点集 Chamfer 判断运动是否准确。

## 数据审计与冻结划分

`prepare_v2.py` 从 v1 快照派生新索引，原 `splits.json` 原样复制，所有保留样本的 split/group 不变；不会重新随机划分。点缓存复用旧目录并校验 SHA256。

所有来源、所有划分采用相同的几何规则。以下问题隔离整个资产，并将原行及原因记入 `excluded_rows.jsonl`：

- 非有限、退化或格式错误的几何、点云、法向。
- 某个 visual 的对角线同时超过其他每个 link 的 100 倍，且超过它自己的单个原始 primitive collision 的 100 倍。

仅 collision 很小可能是占位碰撞体，不足以触发隔离。仅 child 很小也不删除，会记录警告并使用 child 尺度。规则不使用轴标签误差或验证/测试效果。

审计定位到 4 个 TurtleBot 资产的异常 camera visual，位于训练划分，共 8 根 continuous 轴。其 visual 对角线约 51.85m，约为原始 collision 对角线的 386 倍；远端源 `r200.dae` 声明 `unit meter="0.002539999969303608" name="inch"`。暂不猜测单位修复，保留源文件、URDF 哈希和几何证据供核查。

2026-09-11 在 AutoDL 实际生成的 continuous 数量为训练 1234、验证 166、测试 150，总计1550。自有 26 个物体保留原 16/5/5 划分，其中 continuous 训练实际 15 个物体、33 根轴。有限旋转辅助数据默认不参与训练。

训练抽样按来源 → 冻结家族组 → 资产 → 关节逐级均衡，避免同家族变体或多轮子物体主导。密集标签和几何增强不增加独立机械设计数量。

`quality_report.json/.md` 记录所有资产的决定、证据、警告和前后数量。`READY.json` 绑定源快照、索引、排除报告及几何代码指纹。修改几何预处理时需要新派生快照；不原地覆盖已冻结数据。

## 四组消融

| 配置 | 输出头 | 多尺度与局部加密 | 解析运动损失 |
|---|---|---|---|
| `configs/A_direct.json` | 整体原点＋方向 | 关闭 | 关闭 |
| `configs/B_projection.json` | 方向＋逐点轴投影 | 关闭 | 关闭 |
| `configs/C_multiscale.json` | 方向＋逐点轴投影 | 开启 | 关闭 |
| `configs/D_motion.json` | 方向＋逐点轴投影 | 开启 | 权重 0.1 |

四组共用审计后的数据划分、尺度修正和家族采样。A 是在新版编码框架中的直接回归基线，不能与旧版整机尺度结果混为同一实验。C 同时检验多尺度和加密输入这组改动，若有效，再分别关闭其中一个模块进一步拆分贡献。

默认宽度128、两层交叉注意力、batch8、BF16（GPU支持时）、AdamW、150 epochs、每轮2048次采样。参数量和显存以检查报告为准；这些是工程起始值，不是已验证最优值。

## AutoDL 命令

目录：`/root/autodl-tmp/continuous-axis-training-v2-20260911`。
解释器：`/root/autodl-tmp/envs/instruct-particulate/bin/python`。
`configs/autodl.json` 和四组实验配置已经使用服务器路径；`configs/local.json` 用于本地读取准备结果，不需要在本地训练。

```bash
cd /root/autodl-tmp/continuous-axis-training-v2-20260911
export PATH=/root/autodl-tmp/envs/instruct-particulate/bin:$PATH

# 仅在新 prepared 目录第一次生成；已有快照不重复运行。
python prepare_v2.py --config configs/autodl.json

# CPU 实现检查，不代表预测质量。
python preflight.py --config configs/autodl.json --output checks/cpu_preflight
```

用户开启 GPU 后，先测默认 D 配置的真实前向、反向和优化器显存。这个命令不保存训练权重：

```bash
python gpu_preflight.py --config configs/D_motion.json --output checks/gpu_profile_D.json
```

确认显存后，先训练 A 与 B 比较输出表示，再运行 C、D；各命令需要单独启动，不会因 CPU 检查自动触发：

```bash
python train.py --config configs/A_direct.json --device cuda
python train.py --config configs/B_projection.json --device cuda
python train.py --config configs/C_multiscale.json --device cuda
python train.py --config configs/D_motion.json --device cuda
```

断点续训示例：

```bash
python train.py --config configs/B_projection.json --device cuda --resume runs/B_projection/last.pt
```

训练保存 `last.pt`、`best.pt`、逐 epoch 指标、各损失分量、验证集逐关节预测和每物体汇总。非空运行目录只允许从自己的 `last.pt` 续训；从其他检查点分支需指定新的 `--output`。续训核对数据、代码和关键配置，不允许把 CPU smoke checkpoint 当正式训练权重。

2026-09-14 增加 step 进度日志：默认 `log_interval=32`，即每32个训练batch及每轮最后一步输出当前batch loss、窗口平均loss、该轮累计loss、各损失分量、学习率、梯度范数和轮内预计剩余时间。记录同时写入运行目录的 `progress.jsonl`；`metrics.jsonl` 仍为完整epoch指标。每轮有256步，通常输出8次step进度和1次epoch总结。step控制台的epoch从1开始，`epoch_index` 和历史metrics索引从0开始。

`scripts/run_ablation.py` 用于按 A→B→C→D 顺序启动正式训练，独立进程持有互斥锁，并记录队列状态和每组stdout/stderr。每组必须成功完成150轮才开始下一组；任何失败会停止队列。此脚本不自动访问测试集。

## 评估

每轮只用验证集选择权重，测试集不参与调参。指标包括无向轴角度、预测规范原点到参考轴的距离、child 尺度位置误差、名义米制距离、5°且child尺寸1%通过率、45°/90°同点运动误差。

保留逐关节、逐资产、逐家族和来源汇总。选模采用来源 → 家族 → 资产宏平均的 `角度/5 + child归一化轴偏移/0.01`。角度和位置必须一起看，错误的相交轴也可能有零位置距离。米制距离依赖源数据名义单位，不是实物测量精度。自有测试仅5个物体9根轴，应同时逐例查看，不据此宣称广泛泛化。

```bash
python evaluate.py --config configs/B_projection.json --checkpoint runs/B_projection/best.pt --split test --device cuda --output runs/B_projection/test
```

## 新 GLB

```bash
python infer_glb.py --glb /path/object.glb --list-parts
```

调用者提供已知父子 mesh node 组合，例如：

```json
{"pairs":[{"name":"rotor_spin","type":"continuous","parent_nodes":["base_mesh"],"child_nodes":["rotor_mesh"]}]}
```

```bash
python infer_glb.py --glb /path/object.glb --pairs /path/pairs.json --checkpoint runs/B_projection/best.pt --output /path/axes.json --device cuda
```

输入先按 checkpoint 的设置生成8192点池，再使用训练相同的 child frame、采样和归一化。输出是 GLB 世界坐标方向、米制位置；写 URDF 时仍需转换到父件局部坐标。其他输入长度单位用 `--meters-per-unit` 指定。

评估、推理和续训都绑定 checkpoint 的 Python 源代码指纹；移动文件目录不影响指纹，修改实现则需要保留原代码运行旧权重或开始新实验。

## 实现参考

- [PointNet++](https://web.stanford.edu/~rqi/pointnet2/)：局部到整体的点云几何特征。
- [PARTICULATE §3.3/4.3](https://arxiv.org/html/2512.11798v1)：逐点轴投影表示。
- [RPM-Net §7.3.5/7.3.6](https://people.scs.carleton.ca/~olivervankaick/pubs/rpm-net.pdf)：预测位移噪声与原始几何对轴估计的作用。

v2 的配对编码、数据规则与具体训练组合为本项目实现，不是这些论文的完整复现。

## 已完成检查（2026-09-11）

在 AutoDL 完成 CPU 检查：3598 个缓存哈希、1550 条 continuous 输入、原 split/group 隔离、标签不进入输入、增强后投影目标、轴符号与原点等价性、径向损失旋转不变性、家族均衡、四种配置的前向反向、4 次小网络优化器更新和断点恢复、拒绝不兼容续训、GLB 推理。

完整 C/D 网络为915846参数，已用每部件2048点、batch1在CPU完成有限数值的前向与反向。GPU batch8显存、收敛和预测质量尚未测量。检查权重标记为smoke_only，不作为已训练模型使用。

数据快照：`cd36c28ef0f9754fca9ec49cb60e29ad6aa0520c1af4b3003b011185228d4ace`。
报告：服务器 `checks/cpu_preflight/preflight.json`；本地项目 `inference_outputs/continuous_axis_v2/checks/cpu_preflight/preflight.json`。
