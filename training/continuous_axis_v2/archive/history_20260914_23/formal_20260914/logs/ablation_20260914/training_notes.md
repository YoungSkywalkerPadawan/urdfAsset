# Continuous axis v2 正式训练

2026-09-14 10:18（北京时间）已在 AutoDL RTX4090 上启动正式训练。A→B→C→D 顺序运行，各150个epoch；CPU/显存/完整GPU测速已通过，新增step日志也通过了GPU前向反向、文件写入和断点恢复检查。

启动后的检查记录：A组已完成9轮，未发现异常堆栈；第9轮训练平均loss约1.2993，`best.pt`、`last.pt` 均已保存，checkpoint各约9.36MB。此记录是启动检查快照，不是实时进度或最终效果结论。

## Loss 输出

- 每32个step，以及每轮最后一个step：当前batch loss、最近窗口平均loss、该轮累计loss、损失分量、学习率、裁剪前梯度范数、轮内耗时。
- 每个epoch：该轮平均loss、损失分量、完整验证集的轴角度/位置/运动误差、验证选模分数、耗时及是否更新best。
- 每组每轮256个step，因此一般有8条step进度和1条epoch总结。`log_interval` 可配置，当前为32。
- A组仅开启方向与原点损失；其他未开启的损失项输出0。各分量是未乘配置权重的值，总loss按配置加权。
- step日志的 `epoch` 从1开始，并带从0开始的 `epoch_index`；`metrics.jsonl` 原有epoch索引从0开始。

## AutoDL 位置

项目：`/root/autodl-tmp/continuous-axis-training-v2-20260911`。

| 内容 | 相对于项目的路径 |
|---|---|
| 队列状态 | `logs/ablation_20260914/status.json` |
| 后台队列日志 | `logs/ablation_20260914/runner.log` |
| 每组实时控制台日志 | `logs/ablation_20260914/A_direct.log`，后续对应B/C/D名称 |
| step指标 | `runs/A_direct/progress.jsonl` |
| epoch指标 | `runs/A_direct/metrics.jsonl` |
| 权重 | `runs/A_direct/best.pt`、`last.pt` |
| 本次启动源码归档 | `logs/ablation_20260914/launch_source.tar.gz` |
| 启动配置及指纹 | `logs/ablation_20260914/launch_manifest.json` |

查看当前A组实时日志：

```bash
tail -f /root/autodl-tmp/continuous-axis-training-v2-20260911/logs/ablation_20260914/A_direct.log
```

队列独立于SSH会话，断开SSH后继续运行。一组成功完成150轮才启动下一组；报错会停止队列并记录错误，不会在失败后继续剩余实验。队列进程PID为3747，启动时A组进程PID为3813，后续阶段PID以status.json为准。

本轮预计总耗时约3.5–4小时。此次仅启动训练与验证，不自动执行测试集评估。训练结束后再结合验证结果和保留测试物体评估效果。

## 版本

- 正式训练代码指纹：`fbd9dbc44fbc0d31a663e34fe7d0301aec0ff9022f1bb6ab78884294d0f2ba9a`。
- 数据快照：`cd36c28ef0f9754fca9ec49cb60e29ad6aa0520c1af4b3003b011185228d4ace`。
- 相比GPU测速版本，仅增加训练进度日志和独立队列启动器；模型、数据及训练超参数保持原配置。
- 本地启动回执及源码归档位于 `inference_outputs/continuous_axis_v2/formal_20260914/`。
