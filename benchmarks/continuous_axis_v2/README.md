# 冻结的 continuous 关节集合

原 v2 训练数据身份、分组与划分保持不变：1234 train、166 val、150 test，总计 1550 条轴，来自 777 个资产/CAD 对。8 条异常 continuous 轴记录在 `excluded.json`，不自动恢复到训练或评估。

每个 JSONL 行对应一条 `(asset_path, joint_index)`，`joint_index` 指资产 `joints.json` 中的下标。`id` 仍为原始 `articraft/...`、`public/...` 或 `user/...` ID；新仓库的物理路径用 `asset_path`，两者不可混用。

全部自有物体的 continuous 轴按已确定方案分为 33 train、23 val、9 test；不是将 26 个物体全部作为独立测试。

不按单条轴随机重新划分。保留 `group` 与 `original_splits.json`，同一物体和既有去重组不跨划分。公开预训练模型可能已见过这些来源，不能凭这里的 test 字段宣称与其预训练数据无重合。

有限旋转辅助关节另见全局目录，共 597 条，不进入这个 continuous 清单。数据集的训练/验证结果、预测曲线和权重不放在本资产库中。
