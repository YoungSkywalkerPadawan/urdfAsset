# PhysX-Mobility

收录本地已有的 **2,024 个原生 URDF case**，包含原始分件网格、材质纹理及物理属性 JSON。所有内容保留原始字节和路径。

[官方数据集](https://huggingface.co/datasets/Caoza/PhysX-Mobility) · [原始数据卡](UPSTREAM_README.md) · [逐 case 索引](catalog.json) · [导入校验](IMPORT_REPORT.json)

版本：`d0768ee9e1415f6be8db78d6389ba018b85134c0`；许可：**CC-BY-NC-4.0**。原数据基于 PartNet-Mobility，署名与引用见原始数据卡。

## 内容与关节统计

- `PhysX-Mobility.zip`：937,374,668 字节，完整原始包；内含 295,353 个文件，解压后 3,265,545,028 字节。
- `descriptions/urdf/`：2,024 份原始 URDF，供直接查阅；加载时先按下方方法解压其网格。
- `descriptions/finaljson/`：2,024 份原始属性与语义 JSON。
- `ARCHIVE_FILES.sha256.jsonl.gz`：每个原始文件的 SHA-256 与大小。

| 原始关节类型 | 数量 |
|---|---:|
| fixed | 14,096 |
| revolute | 2,633 |
| prismatic | 7,250 |
| floating | 13 |
| continuous | 0 |

**没有 continuous 标签，不自动当作持续旋转正样本。** 本次未转换为现有 GLB/点云基准，也未加入原有训练/验证/测试划分。索引中的 `partnet_mobility:<ID>` 分组用于后续检查与其他 PartNet-Mobility 派生来源的重叠。

导入时逐文件对比了本地解压内容与原始包，295,353 个文件全部一致；URDF 网格、OBJ 材质与 MTL 纹理引用检查均通过。这是文件与资源检查，不代表物理参数已经仿真验收。

## 按需下载和解压

在仓库根目录运行：

```bash
git lfs pull --include="datasets/physx_mobility/**" --exclude=""
python tools/catalog.py --source physx_mobility --type revolute --limit 20
python tools/physx_mobility.py verify
python tools/physx_mobility.py extract --case 100013 --output exports/physx_100013
```

若当前使用稀疏检出，先运行 `git sparse-checkout add datasets/physx_mobility`。只解压指定 case 的网格、URDF 与 JSON；输出目录必须尚不存在，以免覆盖已有数据。

URDF 入口为 `exports/physx_100013/PhysX_mobility/urdf/100013.urdf`，原相对路径可直接解析。每个提取文件都会核对 SHA-256，结果写入 `EXTRACTION.json`。

压缩包 SHA-256：`88308cc2a4cc6177c59e32c2de51e881e6b961737295e5082d7ed01cca221908`。

## case 目录

| ID | 名称 | 类别 | 转动 | 滑动 | 固定 | 原始标注 |
|---|---|---|---:|---:|---:|---|
| [148](descriptions/urdf/148.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/148.json) |
| [149](descriptions/urdf/149.urdf) | Faucet | Plumbing Fixture | 3 | 0 | 6 | [JSON](descriptions/finaljson/149.json) |
| [152](descriptions/urdf/152.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/152.json) |
| [153](descriptions/urdf/153.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/153.json) |
| [154](descriptions/urdf/154.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/154.json) |
| [156](descriptions/urdf/156.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/156.json) |
| [167](descriptions/urdf/167.urdf) | Faucet | Plumbing Fixture | 3 | 0 | 4 | [JSON](descriptions/finaljson/167.json) |
| [168](descriptions/urdf/168.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/168.json) |
| [693](descriptions/urdf/693.urdf) | Faucet | Plumbing Fixture | 1 | 1 | 3 | [JSON](descriptions/finaljson/693.json) |
| [811](descriptions/urdf/811.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/811.json) |
| [822](descriptions/urdf/822.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/822.json) |
| [857](descriptions/urdf/857.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/857.json) |
| [862](descriptions/urdf/862.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 4 | [JSON](descriptions/finaljson/862.json) |
| [866](descriptions/urdf/866.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/866.json) |
| [885](descriptions/urdf/885.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/885.json) |
| [908](descriptions/urdf/908.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/908.json) |
| [912](descriptions/urdf/912.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/912.json) |
| [920](descriptions/urdf/920.urdf) | Faucet | Plumbing Fixture | 3 | 0 | 4 | [JSON](descriptions/finaljson/920.json) |
| [929](descriptions/urdf/929.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/929.json) |
| [931](descriptions/urdf/931.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/931.json) |
| [960](descriptions/urdf/960.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/960.json) |
| [991](descriptions/urdf/991.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/991.json) |
| [1028](descriptions/urdf/1028.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/1028.json) |
| [1034](descriptions/urdf/1034.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1034.json) |
| [1052](descriptions/urdf/1052.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1052.json) |
| [1053](descriptions/urdf/1053.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1053.json) |
| [1280](descriptions/urdf/1280.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 4 | [JSON](descriptions/finaljson/1280.json) |
| [1288](descriptions/urdf/1288.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1288.json) |
| [1343](descriptions/urdf/1343.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1343.json) |
| [1386](descriptions/urdf/1386.urdf) | Faucet | Plumbing Fixture | 3 | 0 | 4 | [JSON](descriptions/finaljson/1386.json) |
| [1401](descriptions/urdf/1401.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/1401.json) |
| [1435](descriptions/urdf/1435.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/1435.json) |
| [1444](descriptions/urdf/1444.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1444.json) |
| [1466](descriptions/urdf/1466.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1466.json) |
| [1479](descriptions/urdf/1479.urdf) | Faucet | Plumbing Fixture | 3 | 0 | 4 | [JSON](descriptions/finaljson/1479.json) |
| [1488](descriptions/urdf/1488.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1488.json) |
| [1492](descriptions/urdf/1492.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1492.json) |
| [1528](descriptions/urdf/1528.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1528.json) |
| [1556](descriptions/urdf/1556.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1556.json) |
| [1596](descriptions/urdf/1596.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1596.json) |
| [1626](descriptions/urdf/1626.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/1626.json) |
| [1633](descriptions/urdf/1633.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1633.json) |
| [1646](descriptions/urdf/1646.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1646.json) |
| [1653](descriptions/urdf/1653.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1653.json) |
| [1667](descriptions/urdf/1667.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1667.json) |
| [1668](descriptions/urdf/1668.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1668.json) |
| [1712](descriptions/urdf/1712.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1712.json) |
| [1741](descriptions/urdf/1741.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1741.json) |
| [1785](descriptions/urdf/1785.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1785.json) |
| [1788](descriptions/urdf/1788.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 2 | [JSON](descriptions/finaljson/1788.json) |
| [1794](descriptions/urdf/1794.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1794.json) |
| [1795](descriptions/urdf/1795.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1795.json) |
| [1802](descriptions/urdf/1802.urdf) | Faucet | Plumbing Fixture | 3 | 0 | 6 | [JSON](descriptions/finaljson/1802.json) |
| [1817](descriptions/urdf/1817.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 2 | [JSON](descriptions/finaljson/1817.json) |
| [1823](descriptions/urdf/1823.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1823.json) |
| [1832](descriptions/urdf/1832.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/1832.json) |
| [1886](descriptions/urdf/1886.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1886.json) |
| [1896](descriptions/urdf/1896.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 4 | [JSON](descriptions/finaljson/1896.json) |
| [1901](descriptions/urdf/1901.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 6 | [JSON](descriptions/finaljson/1901.json) |
| [1903](descriptions/urdf/1903.urdf) | Faucet | Plumbing Fixture | 2 | 1 | 7 | [JSON](descriptions/finaljson/1903.json) |
| [1925](descriptions/urdf/1925.urdf) | Faucet | Plumbing Fixture | 1 | 1 | 4 | [JSON](descriptions/finaljson/1925.json) |
| [1931](descriptions/urdf/1931.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 2 | [JSON](descriptions/finaljson/1931.json) |
| [1935](descriptions/urdf/1935.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 2 | [JSON](descriptions/finaljson/1935.json) |
| [1941](descriptions/urdf/1941.urdf) | Faucet | Plumbing Fixture | 3 | 0 | 4 | [JSON](descriptions/finaljson/1941.json) |
| [1961](descriptions/urdf/1961.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1961.json) |
| [1986](descriptions/urdf/1986.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/1986.json) |
| [2017](descriptions/urdf/2017.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/2017.json) |
| [2035](descriptions/urdf/2035.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 2 | [JSON](descriptions/finaljson/2035.json) |
| [2054](descriptions/urdf/2054.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 3 | [JSON](descriptions/finaljson/2054.json) |
| [2082](descriptions/urdf/2082.urdf) | Faucet | Plumbing Fixture | 3 | 0 | 4 | [JSON](descriptions/finaljson/2082.json) |
| [2083](descriptions/urdf/2083.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/2083.json) |
| [2084](descriptions/urdf/2084.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 4 | [JSON](descriptions/finaljson/2084.json) |
| [2095](descriptions/urdf/2095.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/2095.json) |
| [2108](descriptions/urdf/2108.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/2108.json) |
| [2113](descriptions/urdf/2113.urdf) | Faucet | Plumbing Fixture | 2 | 0 | 4 | [JSON](descriptions/finaljson/2113.json) |
| [2140](descriptions/urdf/2140.urdf) | Faucet | Plumbing Fixture | 3 | 0 | 6 | [JSON](descriptions/finaljson/2140.json) |
| [2170](descriptions/urdf/2170.urdf) | Faucet | Plumbing Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/2170.json) |
| [3386](descriptions/urdf/3386.urdf) | Display | ElectronicDevice | 0 | 1 | 2 | [JSON](descriptions/finaljson/3386.json) |
| [3392](descriptions/urdf/3392.urdf) | Display | ElectronicDevice | 0 | 1 | 2 | [JSON](descriptions/finaljson/3392.json) |
| [3393](descriptions/urdf/3393.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/3393.json) |
| [3395](descriptions/urdf/3395.urdf) | Display | ElectronicDevice | 0 | 4 | 6 | [JSON](descriptions/finaljson/3395.json) |
| [3519](descriptions/urdf/3519.urdf) | Bottle | Container | 0 | 1 | 4 | [JSON](descriptions/finaljson/3519.json) |
| [3593](descriptions/urdf/3593.urdf) | Bottle | Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/3593.json) |
| [3625](descriptions/urdf/3625.urdf) | Bottle | Container | 0 | 1 | 3 | [JSON](descriptions/finaljson/3625.json) |
| [3830](descriptions/urdf/3830.urdf) | Bottle | Container | 0 | 1 | 3 | [JSON](descriptions/finaljson/3830.json) |
| [3944](descriptions/urdf/3944.urdf) | Bottle | Container | 0 | 1 | 3 | [JSON](descriptions/finaljson/3944.json) |
| [3971](descriptions/urdf/3971.urdf) | Bottle | Container | 1 | 0 | 4 | [JSON](descriptions/finaljson/3971.json) |
| [4094](descriptions/urdf/4094.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4094.json) |
| [4108](descriptions/urdf/4108.urdf) | Pot | Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/4108.json) |
| [4204](descriptions/urdf/4204.urdf) | Pot | Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/4204.json) |
| [4393](descriptions/urdf/4393.urdf) | Pot | Container | 0 | 1 | 3 | [JSON](descriptions/finaljson/4393.json) |
| [4500](descriptions/urdf/4500.urdf) | Pot | Container | 0 | 1 | 3 | [JSON](descriptions/finaljson/4500.json) |
| [4529](descriptions/urdf/4529.urdf) | Display | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/4529.json) |
| [4530](descriptions/urdf/4530.urdf) | Display | ElectronicDevice | 0 | 4 | 7 | [JSON](descriptions/finaljson/4530.json) |
| [4533](descriptions/urdf/4533.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4533.json) |
| [4541](descriptions/urdf/4541.urdf) | Display | ElectronicDevice | 0 | 1 | 2 | [JSON](descriptions/finaljson/4541.json) |
| [4542](descriptions/urdf/4542.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4542.json) |
| [4552](descriptions/urdf/4552.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4552.json) |
| [4555](descriptions/urdf/4555.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4555.json) |
| [4562](descriptions/urdf/4562.urdf) | Display | ElectronicDevice | 0 | 1 | 2 | [JSON](descriptions/finaljson/4562.json) |
| [4563](descriptions/urdf/4563.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4563.json) |
| [4564](descriptions/urdf/4564.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4564.json) |
| [4566](descriptions/urdf/4566.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4566.json) |
| [4571](descriptions/urdf/4571.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4571.json) |
| [4574](descriptions/urdf/4574.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4574.json) |
| [4576](descriptions/urdf/4576.urdf) | Display | ElectronicDevice | 0 | 1 | 2 | [JSON](descriptions/finaljson/4576.json) |
| [4578](descriptions/urdf/4578.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4578.json) |
| [4586](descriptions/urdf/4586.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4586.json) |
| [4589](descriptions/urdf/4589.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4589.json) |
| [4590](descriptions/urdf/4590.urdf) | Display | ElectronicDevice | 0 | 1 | 2 | [JSON](descriptions/finaljson/4590.json) |
| [4592](descriptions/urdf/4592.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4592.json) |
| [4594](descriptions/urdf/4594.urdf) | Display | ElectronicDevice | 0 | 1 | 2 | [JSON](descriptions/finaljson/4594.json) |
| [4608](descriptions/urdf/4608.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4608.json) |
| [4627](descriptions/urdf/4627.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4627.json) |
| [4628](descriptions/urdf/4628.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4628.json) |
| [4633](descriptions/urdf/4633.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4633.json) |
| [4681](descriptions/urdf/4681.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4681.json) |
| [4853](descriptions/urdf/4853.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/4853.json) |
| [5050](descriptions/urdf/5050.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/5050.json) |
| [5088](descriptions/urdf/5088.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/5088.json) |
| [5103](descriptions/urdf/5103.urdf) | Display | ElectronicDevice | 0 | 1 | 2 | [JSON](descriptions/finaljson/5103.json) |
| [5306](descriptions/urdf/5306.urdf) | Display | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/5306.json) |
| [5601](descriptions/urdf/5601.urdf) | Pot | Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/5601.json) |
| [5696](descriptions/urdf/5696.urdf) | Clock | WallClock | 2 | 0 | 4 | [JSON](descriptions/finaljson/5696.json) |
| [5850](descriptions/urdf/5850.urdf) | Pot | CeramicContainer | 0 | 1 | 2 | [JSON](descriptions/finaljson/5850.json) |
| [5902](descriptions/urdf/5902.urdf) | Pot | Container | 0 | 1 | 3 | [JSON](descriptions/finaljson/5902.json) |
| [6209](descriptions/urdf/6209.urdf) | Pot | Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/6209.json) |
| [6335](descriptions/urdf/6335.urdf) | Pot | Kitchenware | 0 | 1 | 3 | [JSON](descriptions/finaljson/6335.json) |
| [6500](descriptions/urdf/6500.urdf) | Clock | Timekeeping Device | 3 | 0 | 6 | [JSON](descriptions/finaljson/6500.json) |
| [6568](descriptions/urdf/6568.urdf) | Clock | Timekeeping Device | 2 | 0 | 4 | [JSON](descriptions/finaljson/6568.json) |
| [6613](descriptions/urdf/6613.urdf) | Clock | Timekeeping Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/6613.json) |
| [6638](descriptions/urdf/6638.urdf) | Clock | WallClock | 3 | 0 | 4 | [JSON](descriptions/finaljson/6638.json) |
| [6641](descriptions/urdf/6641.urdf) | Clock | Timekeeping Device | 1 | 0 | 5 | [JSON](descriptions/finaljson/6641.json) |
| [6643](descriptions/urdf/6643.urdf) | Mantel Clock | Clock | 1 | 0 | 3 | [JSON](descriptions/finaljson/6643.json) |
| [6665](descriptions/urdf/6665.urdf) | Clock | WallClock | 2 | 0 | 3 | [JSON](descriptions/finaljson/6665.json) |
| [6728](descriptions/urdf/6728.urdf) | Clock | Timekeeping Device | 2 | 0 | 5 | [JSON](descriptions/finaljson/6728.json) |
| [6797](descriptions/urdf/6797.urdf) | Clock | Timekeeping Device | 3 | 0 | 5 | [JSON](descriptions/finaljson/6797.json) |
| [6808](descriptions/urdf/6808.urdf) | Clock | Timekeeping Device | 2 | 0 | 5 | [JSON](descriptions/finaljson/6808.json) |
| [6813](descriptions/urdf/6813.urdf) | Clock | Timekeeping Device | 3 | 0 | 6 | [JSON](descriptions/finaljson/6813.json) |
| [6839](descriptions/urdf/6839.urdf) | Clock | Timekeeping Device | 2 | 0 | 4 | [JSON](descriptions/finaljson/6839.json) |
| [6917](descriptions/urdf/6917.urdf) | Clock | Timekeeping Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/6917.json) |
| [6934](descriptions/urdf/6934.urdf) | Clock | WallClock | 3 | 0 | 5 | [JSON](descriptions/finaljson/6934.json) |
| [6953](descriptions/urdf/6953.urdf) | Clock | Timekeeping Device | 3 | 0 | 5 | [JSON](descriptions/finaljson/6953.json) |
| [6963](descriptions/urdf/6963.urdf) | Clock | Timekeeping Device | 3 | 0 | 5 | [JSON](descriptions/finaljson/6963.json) |
| [7004](descriptions/urdf/7004.urdf) | Clock | WallClock | 2 | 0 | 4 | [JSON](descriptions/finaljson/7004.json) |
| [7007](descriptions/urdf/7007.urdf) | Clock | Timekeeping Device | 2 | 0 | 4 | [JSON](descriptions/finaljson/7007.json) |
| [7015](descriptions/urdf/7015.urdf) | Clock | Timekeeping Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/7015.json) |
| [7032](descriptions/urdf/7032.urdf) | Clock | WallClock | 2 | 0 | 4 | [JSON](descriptions/finaljson/7032.json) |
| [7037](descriptions/urdf/7037.urdf) | Clock | Timekeeping Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/7037.json) |
| [7054](descriptions/urdf/7054.urdf) | Clock | Timekeeping Device | 3 | 0 | 5 | [JSON](descriptions/finaljson/7054.json) |
| [7064](descriptions/urdf/7064.urdf) | Clock | WallClock | 3 | 0 | 6 | [JSON](descriptions/finaljson/7064.json) |
| [7068](descriptions/urdf/7068.urdf) | Clock | Timekeeping Device | 2 | 0 | 4 | [JSON](descriptions/finaljson/7068.json) |
| [7074](descriptions/urdf/7074.urdf) | Clock | Timekeeping Device | 2 | 0 | 4 | [JSON](descriptions/finaljson/7074.json) |
| [7078](descriptions/urdf/7078.urdf) | Clock | WallClock | 3 | 0 | 4 | [JSON](descriptions/finaljson/7078.json) |
| [7104](descriptions/urdf/7104.urdf) | Clock | Timekeeping Device | 3 | 0 | 5 | [JSON](descriptions/finaljson/7104.json) |
| [7111](descriptions/urdf/7111.urdf) | Clock | Timekeeping Device | 3 | 0 | 5 | [JSON](descriptions/finaljson/7111.json) |
| [7119](descriptions/urdf/7119.urdf) | Microwave | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/7119.json) |
| [7120](descriptions/urdf/7120.urdf) | Microwave | Home Appliance | 2 | 2 | 6 | [JSON](descriptions/finaljson/7120.json) |
| [7128](descriptions/urdf/7128.urdf) | Microwave | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/7128.json) |
| [7130](descriptions/urdf/7130.urdf) | Microwave | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/7130.json) |
| [7138](descriptions/urdf/7138.urdf) | Microwave | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/7138.json) |
| [7179](descriptions/urdf/7179.urdf) | Microwave | Home Appliance | 2 | 2 | 6 | [JSON](descriptions/finaljson/7179.json) |
| [7187](descriptions/urdf/7187.urdf) | Microwave | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/7187.json) |
| [7201](descriptions/urdf/7201.urdf) | Microwave | Home Appliance | 2 | 2 | 6 | [JSON](descriptions/finaljson/7201.json) |
| [7220](descriptions/urdf/7220.urdf) | Microwave | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/7220.json) |
| [7221](descriptions/urdf/7221.urdf) | Microwave | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/7221.json) |
| [7236](descriptions/urdf/7236.urdf) | Microwave | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/7236.json) |
| [7273](descriptions/urdf/7273.urdf) | Microwave | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/7273.json) |
| [7290](descriptions/urdf/7290.urdf) | Microwave | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/7290.json) |
| [7292](descriptions/urdf/7292.urdf) | Microwave | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/7292.json) |
| [7304](descriptions/urdf/7304.urdf) | Microwave | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/7304.json) |
| [7306](descriptions/urdf/7306.urdf) | Microwave | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/7306.json) |
| [7310](descriptions/urdf/7310.urdf) | Microwave | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/7310.json) |
| [7320](descriptions/urdf/7320.urdf) | Microwave | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/7320.json) |
| [7332](descriptions/urdf/7332.urdf) | Microwave | Home Appliance | 2 | 2 | 6 | [JSON](descriptions/finaljson/7332.json) |
| [7347](descriptions/urdf/7347.urdf) | Microwave | Home Appliance | 2 | 1 | 5 | [JSON](descriptions/finaljson/7347.json) |
| [7366](descriptions/urdf/7366.urdf) | Microwave | Home Appliance | 2 | 1 | 4 | [JSON](descriptions/finaljson/7366.json) |
| [7619](descriptions/urdf/7619.urdf) | Keyboard | ComputerPeripheral | 0 | 115 | 116 | [JSON](descriptions/finaljson/7619.json) |
| [8736](descriptions/urdf/8736.urdf) | Mug | Drinkware | 0 | 1 | 4 | [JSON](descriptions/finaljson/8736.json) |
| [8848](descriptions/urdf/8848.urdf) | Mug | Drinkware | 0 | 1 | 3 | [JSON](descriptions/finaljson/8848.json) |
| [8877](descriptions/urdf/8877.urdf) | Door Set | Architectural Structure | 2 | 0 | 3 | [JSON](descriptions/finaljson/8877.json) |
| [8919](descriptions/urdf/8919.urdf) | Door Set | Architectural Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/8919.json) |
| [8936](descriptions/urdf/8936.urdf) | Door Set | Furniture/Building Component | 2 | 0 | 3 | [JSON](descriptions/finaljson/8936.json) |
| [8983](descriptions/urdf/8983.urdf) | Door Set | Architectural Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/8983.json) |
| [8997](descriptions/urdf/8997.urdf) | Door Set | Architectural Component | 1 | 0 | 3 | [JSON](descriptions/finaljson/8997.json) |
| [9032](descriptions/urdf/9032.urdf) | Door Set | Architectural Component | 0 | 1 | 2 | [JSON](descriptions/finaljson/9032.json) |
| [9041](descriptions/urdf/9041.urdf) | Door Set | Architectural Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/9041.json) |
| [9107](descriptions/urdf/9107.urdf) | Door Set | Architectural Component | 1 | 0 | 7 | [JSON](descriptions/finaljson/9107.json) |
| [9128](descriptions/urdf/9128.urdf) | Door Set | Architectural Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/9128.json) |
| [9148](descriptions/urdf/9148.urdf) | Door Set | Architectural Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/9148.json) |
| [9386](descriptions/urdf/9386.urdf) | Door Set | Architectural Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/9386.json) |
| [9388](descriptions/urdf/9388.urdf) | Door Set | Architectural Structure | 1 | 0 | 3 | [JSON](descriptions/finaljson/9388.json) |
| [9748](descriptions/urdf/9748.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/9748.json) |
| [9912](descriptions/urdf/9912.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/9912.json) |
| [9918](descriptions/urdf/9918.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/9918.json) |
| [9960](descriptions/urdf/9960.urdf) | Laptop | ElectronicDevice | 1 | 0 | 5 | [JSON](descriptions/finaljson/9960.json) |
| [9968](descriptions/urdf/9968.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/9968.json) |
| [9987](descriptions/urdf/9987.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/9987.json) |
| [9992](descriptions/urdf/9992.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/9992.json) |
| [9996](descriptions/urdf/9996.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/9996.json) |
| [10036](descriptions/urdf/10036.urdf) | Refrigerator | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/10036.json) |
| [10040](descriptions/urdf/10040.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/10040.json) |
| [10068](descriptions/urdf/10068.urdf) | Refrigerator | Home Appliance | 2 | 0 | 5 | [JSON](descriptions/finaljson/10068.json) |
| [10090](descriptions/urdf/10090.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10090.json) |
| [10098](descriptions/urdf/10098.urdf) | Laptop | ElectronicDevice | 1 | 0 | 5 | [JSON](descriptions/finaljson/10098.json) |
| [10101](descriptions/urdf/10101.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10101.json) |
| [10108](descriptions/urdf/10108.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/10108.json) |
| [10125](descriptions/urdf/10125.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/10125.json) |
| [10211](descriptions/urdf/10211.urdf) | Laptop | ElectronicDevice | 1 | 0 | 5 | [JSON](descriptions/finaljson/10211.json) |
| [10213](descriptions/urdf/10213.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10213.json) |
| [10238](descriptions/urdf/10238.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/10238.json) |
| [10239](descriptions/urdf/10239.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/10239.json) |
| [10243](descriptions/urdf/10243.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10243.json) |
| [10248](descriptions/urdf/10248.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10248.json) |
| [10269](descriptions/urdf/10269.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10269.json) |
| [10270](descriptions/urdf/10270.urdf) | Laptop | Electronic Device | 1 | 0 | 3 | [JSON](descriptions/finaljson/10270.json) |
| [10280](descriptions/urdf/10280.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/10280.json) |
| [10289](descriptions/urdf/10289.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10289.json) |
| [10305](descriptions/urdf/10305.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/10305.json) |
| [10306](descriptions/urdf/10306.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10306.json) |
| [10356](descriptions/urdf/10356.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/10356.json) |
| [10357](descriptions/urdf/10357.urdf) | Trash Can | Household Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/10357.json) |
| [10373](descriptions/urdf/10373.urdf) | Refrigerator | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/10373.json) |
| [10383](descriptions/urdf/10383.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10383.json) |
| [10449](descriptions/urdf/10449.urdf) | Scissors | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/10449.json) |
| [10450](descriptions/urdf/10450.urdf) | Scissors | Cutting Tool | 1 | 0 | 5 | [JSON](descriptions/finaljson/10450.json) |
| [10495](descriptions/urdf/10495.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10495.json) |
| [10499](descriptions/urdf/10499.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10499.json) |
| [10502](descriptions/urdf/10502.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10502.json) |
| [10537](descriptions/urdf/10537.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10537.json) |
| [10546](descriptions/urdf/10546.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10546.json) |
| [10557](descriptions/urdf/10557.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10557.json) |
| [10558](descriptions/urdf/10558.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10558.json) |
| [10559](descriptions/urdf/10559.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10559.json) |
| [10561](descriptions/urdf/10561.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10561.json) |
| [10562](descriptions/urdf/10562.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10562.json) |
| [10564](descriptions/urdf/10564.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10564.json) |
| [10567](descriptions/urdf/10567.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10567.json) |
| [10569](descriptions/urdf/10569.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10569.json) |
| [10584](descriptions/urdf/10584.urdf) | Trash Can | Household Utility Object | 1 | 0 | 3 | [JSON](descriptions/finaljson/10584.json) |
| [10586](descriptions/urdf/10586.urdf) | Refrigerator | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/10586.json) |
| [10620](descriptions/urdf/10620.urdf) | Refrigerator | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/10620.json) |
| [10622](descriptions/urdf/10622.urdf) | Scissors | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/10622.json) |
| [10626](descriptions/urdf/10626.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/10626.json) |
| [10627](descriptions/urdf/10627.urdf) | Refrigerator | Home Appliance | 2 | 0 | 3 | [JSON](descriptions/finaljson/10627.json) |
| [10638](descriptions/urdf/10638.urdf) | Refrigerator | Home Appliance | 2 | 0 | 3 | [JSON](descriptions/finaljson/10638.json) |
| [10655](descriptions/urdf/10655.urdf) | Refrigerator | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/10655.json) |
| [10685](descriptions/urdf/10685.urdf) | Refrigerator | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/10685.json) |
| [10686](descriptions/urdf/10686.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10686.json) |
| [10697](descriptions/urdf/10697.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10697.json) |
| [10707](descriptions/urdf/10707.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/10707.json) |
| [10751](descriptions/urdf/10751.urdf) | Refrigerator | Home Appliance | 2 | 0 | 3 | [JSON](descriptions/finaljson/10751.json) |
| [10797](descriptions/urdf/10797.urdf) | Refrigerator | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/10797.json) |
| [10844](descriptions/urdf/10844.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10844.json) |
| [10867](descriptions/urdf/10867.urdf) | Refrigerator | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/10867.json) |
| [10885](descriptions/urdf/10885.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/10885.json) |
| [10889](descriptions/urdf/10889.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10889.json) |
| [10893](descriptions/urdf/10893.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10893.json) |
| [10894](descriptions/urdf/10894.urdf) | Scissors | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/10894.json) |
| [10895](descriptions/urdf/10895.urdf) | Scissors | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/10895.json) |
| [10902](descriptions/urdf/10902.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10902.json) |
| [10907](descriptions/urdf/10907.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10907.json) |
| [10915](descriptions/urdf/10915.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/10915.json) |
| [10960](descriptions/urdf/10960.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10960.json) |
| [10962](descriptions/urdf/10962.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10962.json) |
| [10968](descriptions/urdf/10968.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10968.json) |
| [10973](descriptions/urdf/10973.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10973.json) |
| [10975](descriptions/urdf/10975.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/10975.json) |
| [11013](descriptions/urdf/11013.urdf) | Scissors | Cutting Tool | 1 | 0 | 4 | [JSON](descriptions/finaljson/11013.json) |
| [11020](descriptions/urdf/11020.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11020.json) |
| [11021](descriptions/urdf/11021.urdf) | Scissors | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/11021.json) |
| [11026](descriptions/urdf/11026.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11026.json) |
| [11028](descriptions/urdf/11028.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11028.json) |
| [11029](descriptions/urdf/11029.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11029.json) |
| [11030](descriptions/urdf/11030.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/11030.json) |
| [11036](descriptions/urdf/11036.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11036.json) |
| [11040](descriptions/urdf/11040.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11040.json) |
| [11047](descriptions/urdf/11047.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11047.json) |
| [11052](descriptions/urdf/11052.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11052.json) |
| [11075](descriptions/urdf/11075.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/11075.json) |
| [11077](descriptions/urdf/11077.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11077.json) |
| [11080](descriptions/urdf/11080.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11080.json) |
| [11089](descriptions/urdf/11089.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11089.json) |
| [11099](descriptions/urdf/11099.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11099.json) |
| [11100](descriptions/urdf/11100.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11100.json) |
| [11103](descriptions/urdf/11103.urdf) | Scissors | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/11103.json) |
| [11111](descriptions/urdf/11111.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11111.json) |
| [11113](descriptions/urdf/11113.urdf) | Scissors | Cutting Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/11113.json) |
| [11124](descriptions/urdf/11124.urdf) | Trash Can | Waste Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/11124.json) |
| [11141](descriptions/urdf/11141.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/11141.json) |
| [11156](descriptions/urdf/11156.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/11156.json) |
| [11229](descriptions/urdf/11229.urdf) | Trash Can | Household Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/11229.json) |
| [11231](descriptions/urdf/11231.urdf) | Refrigerator | Home Appliance | 2 | 0 | 3 | [JSON](descriptions/finaljson/11231.json) |
| [11242](descriptions/urdf/11242.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/11242.json) |
| [11248](descriptions/urdf/11248.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/11248.json) |
| [11259](descriptions/urdf/11259.urdf) | Trash Can | Household Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/11259.json) |
| [11260](descriptions/urdf/11260.urdf) | Refrigerator | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/11260.json) |
| [11299](descriptions/urdf/11299.urdf) | Refrigerator | Home Appliance | 2 | 0 | 3 | [JSON](descriptions/finaljson/11299.json) |
| [11361](descriptions/urdf/11361.urdf) | Trash Can | Household Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/11361.json) |
| [11395](descriptions/urdf/11395.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/11395.json) |
| [11405](descriptions/urdf/11405.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/11405.json) |
| [11406](descriptions/urdf/11406.urdf) | Laptop | Electronic Device | 1 | 0 | 3 | [JSON](descriptions/finaljson/11406.json) |
| [11429](descriptions/urdf/11429.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/11429.json) |
| [11477](descriptions/urdf/11477.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/11477.json) |
| [11538](descriptions/urdf/11538.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/11538.json) |
| [11581](descriptions/urdf/11581.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/11581.json) |
| [11586](descriptions/urdf/11586.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/11586.json) |
| [11661](descriptions/urdf/11661.urdf) | Dishwasher | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/11661.json) |
| [11691](descriptions/urdf/11691.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/11691.json) |
| [11712](descriptions/urdf/11712.urdf) | Refrigerator | Home Appliance | 2 | 0 | 4 | [JSON](descriptions/finaljson/11712.json) |
| [11778](descriptions/urdf/11778.urdf) | Laptop | Electronic Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/11778.json) |
| [11818](descriptions/urdf/11818.urdf) | Trash Can | Household Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/11818.json) |
| [11854](descriptions/urdf/11854.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/11854.json) |
| [11876](descriptions/urdf/11876.urdf) | Laptop | ElectronicDevice | 1 | 0 | 4 | [JSON](descriptions/finaljson/11876.json) |
| [11888](descriptions/urdf/11888.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/11888.json) |
| [11945](descriptions/urdf/11945.urdf) | Laptop | ElectronicDevice | 1 | 0 | 5 | [JSON](descriptions/finaljson/11945.json) |
| [12038](descriptions/urdf/12038.urdf) | Refrigerator | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12038.json) |
| [12042](descriptions/urdf/12042.urdf) | Refrigerator | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12042.json) |
| [12043](descriptions/urdf/12043.urdf) | Refrigerator | Home Appliance | 2 | 0 | 3 | [JSON](descriptions/finaljson/12043.json) |
| [12055](descriptions/urdf/12055.urdf) | Refrigerator | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/12055.json) |
| [12066](descriptions/urdf/12066.urdf) | Refrigerator | Home Appliance | 2 | 0 | 3 | [JSON](descriptions/finaljson/12066.json) |
| [12073](descriptions/urdf/12073.urdf) | Laptop | ElectronicDevice | 1 | 0 | 3 | [JSON](descriptions/finaljson/12073.json) |
| [12085](descriptions/urdf/12085.urdf) | Dishwasher | Home Appliance | 0 | 1 | 4 | [JSON](descriptions/finaljson/12085.json) |
| [12115](descriptions/urdf/12115.urdf) | Laptop | ElectronicDevice | 1 | 0 | 2 | [JSON](descriptions/finaljson/12115.json) |
| [12231](descriptions/urdf/12231.urdf) | Trash Can | Household Object | 0 | 1 | 3 | [JSON](descriptions/finaljson/12231.json) |
| [12250](descriptions/urdf/12250.urdf) | Refrigerator | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12250.json) |
| [12289](descriptions/urdf/12289.urdf) | Trash Can | Household Object | 0 | 1 | 2 | [JSON](descriptions/finaljson/12289.json) |
| [12447](descriptions/urdf/12447.urdf) | Trash Can | Waste Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/12447.json) |
| [12477](descriptions/urdf/12477.urdf) | Trash Can | Waste Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/12477.json) |
| [12480](descriptions/urdf/12480.urdf) | Dishwasher | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12480.json) |
| [12530](descriptions/urdf/12530.urdf) | Dishwasher | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12530.json) |
| [12531](descriptions/urdf/12531.urdf) | Dishwasher | Home Appliance | 0 | 0 | 2 | [JSON](descriptions/finaljson/12531.json) |
| [12559](descriptions/urdf/12559.urdf) | Dishwasher | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/12559.json) |
| [12561](descriptions/urdf/12561.urdf) | Dishwasher | Home Appliance | 0 | 0 | 2 | [JSON](descriptions/finaljson/12561.json) |
| [12562](descriptions/urdf/12562.urdf) | Dishwasher | Home Appliance | 0 | 0 | 2 | [JSON](descriptions/finaljson/12562.json) |
| [12565](descriptions/urdf/12565.urdf) | Dishwasher | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12565.json) |
| [12578](descriptions/urdf/12578.urdf) | Dishwasher | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/12578.json) |
| [12579](descriptions/urdf/12579.urdf) | Dishwasher | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12579.json) |
| [12584](descriptions/urdf/12584.urdf) | Dishwasher | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12584.json) |
| [12592](descriptions/urdf/12592.urdf) | Dishwasher | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12592.json) |
| [12597](descriptions/urdf/12597.urdf) | Dishwasher | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/12597.json) |
| [12606](descriptions/urdf/12606.urdf) | Dishwasher | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12606.json) |
| [12614](descriptions/urdf/12614.urdf) | Dishwasher | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/12614.json) |
| [12654](descriptions/urdf/12654.urdf) | Dishwasher | Home Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/12654.json) |
| [12727](descriptions/urdf/12727.urdf) | Keyboard | ComputerPeripheral | 0 | 77 | 78 | [JSON](descriptions/finaljson/12727.json) |
| [12738](descriptions/urdf/12738.urdf) | Keyboard | ComputerPeripheral | 0 | 103 | 104 | [JSON](descriptions/finaljson/12738.json) |
| [12829](descriptions/urdf/12829.urdf) | Keyboard | ComputerPeripheral | 0 | 85 | 86 | [JSON](descriptions/finaljson/12829.json) |
| [12834](descriptions/urdf/12834.urdf) | Keyboard | ComputerPeripheral | 0 | 109 | 111 | [JSON](descriptions/finaljson/12834.json) |
| [12836](descriptions/urdf/12836.urdf) | Keyboard | ComputerPeripheral | 0 | 105 | 106 | [JSON](descriptions/finaljson/12836.json) |
| [12838](descriptions/urdf/12838.urdf) | Keyboard | ComputerPeripheral | 0 | 101 | 102 | [JSON](descriptions/finaljson/12838.json) |
| [12851](descriptions/urdf/12851.urdf) | Keyboard | ComputerPeripheral | 0 | 105 | 108 | [JSON](descriptions/finaljson/12851.json) |
| [12880](descriptions/urdf/12880.urdf) | Keyboard | ComputerPeripheral | 0 | 115 | 116 | [JSON](descriptions/finaljson/12880.json) |
| [12886](descriptions/urdf/12886.urdf) | Keyboard | ComputerPeripheral | 2 | 104 | 108 | [JSON](descriptions/finaljson/12886.json) |
| [12902](descriptions/urdf/12902.urdf) | Keyboard | ComputerPeripheral | 0 | 78 | 81 | [JSON](descriptions/finaljson/12902.json) |
| [12917](descriptions/urdf/12917.urdf) | Keyboard | ComputerPeripheral | 0 | 102 | 103 | [JSON](descriptions/finaljson/12917.json) |
| [12923](descriptions/urdf/12923.urdf) | Keyboard | ComputerPeripheral | 0 | 79 | 84 | [JSON](descriptions/finaljson/12923.json) |
| [12947](descriptions/urdf/12947.urdf) | Keyboard | ComputerPeripheral | 0 | 110 | 113 | [JSON](descriptions/finaljson/12947.json) |
| [12953](descriptions/urdf/12953.urdf) | Keyboard | ComputerPeripheral | 0 | 104 | 105 | [JSON](descriptions/finaljson/12953.json) |
| [12956](descriptions/urdf/12956.urdf) | Keyboard | ComputerPeripheral | 0 | 109 | 110 | [JSON](descriptions/finaljson/12956.json) |
| [12965](descriptions/urdf/12965.urdf) | Keyboard | ComputerPeripheral | 0 | 104 | 105 | [JSON](descriptions/finaljson/12965.json) |
| [12968](descriptions/urdf/12968.urdf) | Keyboard | ComputerPeripheral | 0 | 77 | 78 | [JSON](descriptions/finaljson/12968.json) |
| [12977](descriptions/urdf/12977.urdf) | Keyboard | ComputerPeripheral | 0 | 104 | 107 | [JSON](descriptions/finaljson/12977.json) |
| [12996](descriptions/urdf/12996.urdf) | Keyboard | ComputerPeripheral | 0 | 104 | 105 | [JSON](descriptions/finaljson/12996.json) |
| [12999](descriptions/urdf/12999.urdf) | Keyboard | ComputerPeripheral | 0 | 110 | 112 | [JSON](descriptions/finaljson/12999.json) |
| [13004](descriptions/urdf/13004.urdf) | Keyboard | ComputerPeripheral | 0 | 24 | 29 | [JSON](descriptions/finaljson/13004.json) |
| [13023](descriptions/urdf/13023.urdf) | Keyboard | ComputerPeripheral | 0 | 29 | 30 | [JSON](descriptions/finaljson/13023.json) |
| [13024](descriptions/urdf/13024.urdf) | Keyboard | ComputerPeripheral | 0 | 96 | 97 | [JSON](descriptions/finaljson/13024.json) |
| [13027](descriptions/urdf/13027.urdf) | Keyboard | ComputerPeripheral | 0 | 95 | 98 | [JSON](descriptions/finaljson/13027.json) |
| [13062](descriptions/urdf/13062.urdf) | Keyboard | ComputerPeripheral | 0 | 104 | 105 | [JSON](descriptions/finaljson/13062.json) |
| [13064](descriptions/urdf/13064.urdf) | Keyboard | ComputerPeripheral | 0 | 104 | 105 | [JSON](descriptions/finaljson/13064.json) |
| [13075](descriptions/urdf/13075.urdf) | Keyboard | ComputerPeripheral | 0 | 109 | 111 | [JSON](descriptions/finaljson/13075.json) |
| [13082](descriptions/urdf/13082.urdf) | Keyboard | ComputerPeripheral | 0 | 60 | 65 | [JSON](descriptions/finaljson/13082.json) |
| [13086](descriptions/urdf/13086.urdf) | Keyboard | ComputerPeripheral | 0 | 109 | 110 | [JSON](descriptions/finaljson/13086.json) |
| [13095](descriptions/urdf/13095.urdf) | Keyboard | ComputerPeripheral | 0 | 104 | 108 | [JSON](descriptions/finaljson/13095.json) |
| [13100](descriptions/urdf/13100.urdf) | Keyboard | ComputerPeripheral | 0 | 110 | 111 | [JSON](descriptions/finaljson/13100.json) |
| [13106](descriptions/urdf/13106.urdf) | Keyboard | ComputerPeripheral | 0 | 77 | 78 | [JSON](descriptions/finaljson/13106.json) |
| [13120](descriptions/urdf/13120.urdf) | Keyboard | ComputerPeripheral | 0 | 106 | 109 | [JSON](descriptions/finaljson/13120.json) |
| [13136](descriptions/urdf/13136.urdf) | Keyboard | ComputerPeripheral | 0 | 105 | 107 | [JSON](descriptions/finaljson/13136.json) |
| [13153](descriptions/urdf/13153.urdf) | Keyboard | ComputerPeripheral | 0 | 110 | 111 | [JSON](descriptions/finaljson/13153.json) |
| [13154](descriptions/urdf/13154.urdf) | Keyboard | ComputerPeripheral | 0 | 110 | 113 | [JSON](descriptions/finaljson/13154.json) |
| [13491](descriptions/urdf/13491.urdf) | Pendant Lamp | Lighting Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/13491.json) |
| [14127](descriptions/urdf/14127.urdf) | Lamp | Lighting Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/14127.json) |
| [14205](descriptions/urdf/14205.urdf) | Lamp | Lighting Fixture | 1 | 0 | 2 | [JSON](descriptions/finaljson/14205.json) |
| [14563](descriptions/urdf/14563.urdf) | Desk Lamp | Lighting Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/14563.json) |
| [15913](descriptions/urdf/15913.urdf) | Lamp | Lighting Fixture | 1 | 0 | 3 | [JSON](descriptions/finaljson/15913.json) |
| [19179](descriptions/urdf/19179.urdf) | Table with Drawers | Furniture | 0 | 2 | 7 | [JSON](descriptions/finaljson/19179.json) |
| [19825](descriptions/urdf/19825.urdf) | Table with Storage Cabinet | Furniture | 2 | 0 | 11 | [JSON](descriptions/finaljson/19825.json) |
| [19836](descriptions/urdf/19836.urdf) | Table with Drawers | Furniture | 0 | 3 | 10 | [JSON](descriptions/finaljson/19836.json) |
| [19855](descriptions/urdf/19855.urdf) | Table | Furniture | 0 | 1 | 14 | [JSON](descriptions/finaljson/19855.json) |
| [20043](descriptions/urdf/20043.urdf) | Table | Furniture | 0 | 2 | 23 | [JSON](descriptions/finaljson/20043.json) |
| [20411](descriptions/urdf/20411.urdf) | Table | Furniture | 0 | 1 | 13 | [JSON](descriptions/finaljson/20411.json) |
| [20453](descriptions/urdf/20453.urdf) | Table | Furniture | 0 | 1 | 7 | [JSON](descriptions/finaljson/20453.json) |
| [20555](descriptions/urdf/20555.urdf) | Table | Furniture | 0 | 1 | 23 | [JSON](descriptions/finaljson/20555.json) |
| [20985](descriptions/urdf/20985.urdf) | Table | Furniture | 0 | 1 | 14 | [JSON](descriptions/finaljson/20985.json) |
| [22241](descriptions/urdf/22241.urdf) | Table | Furniture | 0 | 1 | 20 | [JSON](descriptions/finaljson/22241.json) |
| [22301](descriptions/urdf/22301.urdf) | Table | Furniture | 0 | 1 | 2 | [JSON](descriptions/finaljson/22301.json) |
| [22339](descriptions/urdf/22339.urdf) | Table | Furniture | 0 | 1 | 15 | [JSON](descriptions/finaljson/22339.json) |
| [22367](descriptions/urdf/22367.urdf) | Table with Drawers | Furniture | 0 | 8 | 47 | [JSON](descriptions/finaljson/22367.json) |
| [22433](descriptions/urdf/22433.urdf) | Table with Cabinet | Furniture | 3 | 0 | 16 | [JSON](descriptions/finaljson/22433.json) |
| [22508](descriptions/urdf/22508.urdf) | Table | Furniture | 0 | 1 | 15 | [JSON](descriptions/finaljson/22508.json) |
| [22692](descriptions/urdf/22692.urdf) | Table with Drawers | Furniture | 0 | 2 | 12 | [JSON](descriptions/finaljson/22692.json) |
| [23372](descriptions/urdf/23372.urdf) | Storage Table with Drawers and Cabinet Doors | Furniture | 2 | 2 | 21 | [JSON](descriptions/finaljson/23372.json) |
| [23472](descriptions/urdf/23472.urdf) | Table | Furniture | 1 | 1 | 15 | [JSON](descriptions/finaljson/23472.json) |
| [23511](descriptions/urdf/23511.urdf) | Table | Furniture | 0 | 1 | 10 | [JSON](descriptions/finaljson/23511.json) |
| [23782](descriptions/urdf/23782.urdf) | Table | Furniture | 2 | 0 | 9 | [JSON](descriptions/finaljson/23782.json) |
| [23807](descriptions/urdf/23807.urdf) | Table | Furniture | 0 | 4 | 20 | [JSON](descriptions/finaljson/23807.json) |
| [24644](descriptions/urdf/24644.urdf) | Table | Furniture | 0 | 1 | 9 | [JSON](descriptions/finaljson/24644.json) |
| [25493](descriptions/urdf/25493.urdf) | Table | Furniture | 0 | 3 | 19 | [JSON](descriptions/finaljson/25493.json) |
| [25913](descriptions/urdf/25913.urdf) | Table | Furniture | 0 | 3 | 19 | [JSON](descriptions/finaljson/25913.json) |
| [25959](descriptions/urdf/25959.urdf) | Table | Furniture | 4 | 0 | 17 | [JSON](descriptions/finaljson/25959.json) |
| [26073](descriptions/urdf/26073.urdf) | Table | Furniture | 0 | 1 | 10 | [JSON](descriptions/finaljson/26073.json) |
| [26503](descriptions/urdf/26503.urdf) | Table | Furniture | 0 | 1 | 9 | [JSON](descriptions/finaljson/26503.json) |
| [26525](descriptions/urdf/26525.urdf) | Table | Furniture | 0 | 1 | 26 | [JSON](descriptions/finaljson/26525.json) |
| [26608](descriptions/urdf/26608.urdf) | Table with Drawers | Furniture | 0 | 8 | 24 | [JSON](descriptions/finaljson/26608.json) |
| [26652](descriptions/urdf/26652.urdf) | Table | Furniture | 0 | 1 | 10 | [JSON](descriptions/finaljson/26652.json) |
| [26670](descriptions/urdf/26670.urdf) | Table | Furniture | 0 | 1 | 28 | [JSON](descriptions/finaljson/26670.json) |
| [26806](descriptions/urdf/26806.urdf) | Table | Furniture | 0 | 1 | 19 | [JSON](descriptions/finaljson/26806.json) |
| [26899](descriptions/urdf/26899.urdf) | Table | Furniture | 1 | 0 | 20 | [JSON](descriptions/finaljson/26899.json) |
| [27044](descriptions/urdf/27044.urdf) | Table | Furniture | 0 | 1 | 12 | [JSON](descriptions/finaljson/27044.json) |
| [27189](descriptions/urdf/27189.urdf) | Table | Furniture | 0 | 1 | 8 | [JSON](descriptions/finaljson/27189.json) |
| [27267](descriptions/urdf/27267.urdf) | Table with Storage Cabinet | Furniture | 1 | 1 | 18 | [JSON](descriptions/finaljson/27267.json) |
| [28164](descriptions/urdf/28164.urdf) | Table | Furniture | 0 | 2 | 16 | [JSON](descriptions/finaljson/28164.json) |
| [28668](descriptions/urdf/28668.urdf) | Table | Furniture | 0 | 1 | 12 | [JSON](descriptions/finaljson/28668.json) |
| [29133](descriptions/urdf/29133.urdf) | Table | Furniture | 0 | 2 | 12 | [JSON](descriptions/finaljson/29133.json) |
| [29525](descriptions/urdf/29525.urdf) | Table | Furniture | 0 | 1 | 6 | [JSON](descriptions/finaljson/29525.json) |
| [29557](descriptions/urdf/29557.urdf) | Table | Furniture | 0 | 1 | 9 | [JSON](descriptions/finaljson/29557.json) |
| [29921](descriptions/urdf/29921.urdf) | Table | Furniture | 0 | 1 | 9 | [JSON](descriptions/finaljson/29921.json) |
| [30663](descriptions/urdf/30663.urdf) | Table | Furniture | 0 | 3 | 17 | [JSON](descriptions/finaljson/30663.json) |
| [30666](descriptions/urdf/30666.urdf) | Table | Furniture | 0 | 9 | 92 | [JSON](descriptions/finaljson/30666.json) |
| [30739](descriptions/urdf/30739.urdf) | Table | Furniture | 0 | 2 | 7 | [JSON](descriptions/finaljson/30739.json) |
| [30857](descriptions/urdf/30857.urdf) | Table | Furniture | 0 | 3 | 14 | [JSON](descriptions/finaljson/30857.json) |
| [30869](descriptions/urdf/30869.urdf) | Workbench Table | Furniture | 0 | 1 | 17 | [JSON](descriptions/finaljson/30869.json) |
| [31601](descriptions/urdf/31601.urdf) | Table | Furniture | 0 | 2 | 12 | [JSON](descriptions/finaljson/31601.json) |
| [32052](descriptions/urdf/32052.urdf) | Table | Furniture | 0 | 7 | 20 | [JSON](descriptions/finaljson/32052.json) |
| [32086](descriptions/urdf/32086.urdf) | Table with Cabinet Storage | Furniture | 2 | 0 | 21 | [JSON](descriptions/finaljson/32086.json) |
| [32174](descriptions/urdf/32174.urdf) | Table | Furniture | 1 | 1 | 8 | [JSON](descriptions/finaljson/32174.json) |
| [32213](descriptions/urdf/32213.urdf) | Table | Furniture | 0 | 6 | 24 | [JSON](descriptions/finaljson/32213.json) |
| [32324](descriptions/urdf/32324.urdf) | Office Table with Drawers | Furniture | 0 | 3 | 23 | [JSON](descriptions/finaljson/32324.json) |
| [32354](descriptions/urdf/32354.urdf) | Table | Furniture | 0 | 3 | 10 | [JSON](descriptions/finaljson/32354.json) |
| [32566](descriptions/urdf/32566.urdf) | Table | Furniture | 1 | 0 | 18 | [JSON](descriptions/finaljson/32566.json) |
| [32601](descriptions/urdf/32601.urdf) | Table | Furniture | 0 | 4 | 40 | [JSON](descriptions/finaljson/32601.json) |
| [32625](descriptions/urdf/32625.urdf) | Table | Furniture | 0 | 4 | 20 | [JSON](descriptions/finaljson/32625.json) |
| [32746](descriptions/urdf/32746.urdf) | Table | Furniture | 0 | 2 | 14 | [JSON](descriptions/finaljson/32746.json) |
| [32761](descriptions/urdf/32761.urdf) | Office Table | Furniture | 0 | 4 | 12 | [JSON](descriptions/finaljson/32761.json) |
| [32932](descriptions/urdf/32932.urdf) | Table | Furniture | 0 | 2 | 28 | [JSON](descriptions/finaljson/32932.json) |
| [33457](descriptions/urdf/33457.urdf) | L-shaped Table | Furniture | 1 | 2 | 24 | [JSON](descriptions/finaljson/33457.json) |
| [33810](descriptions/urdf/33810.urdf) | Office Desk | Furniture | 1 | 4 | 24 | [JSON](descriptions/finaljson/33810.json) |
| [33914](descriptions/urdf/33914.urdf) | Table | Furniture | 0 | 2 | 45 | [JSON](descriptions/finaljson/33914.json) |
| [33930](descriptions/urdf/33930.urdf) | Office Table | Furniture | 0 | 6 | 38 | [JSON](descriptions/finaljson/33930.json) |
| [34178](descriptions/urdf/34178.urdf) | Table with Storage | Furniture | 2 | 2 | 35 | [JSON](descriptions/finaljson/34178.json) |
| [34610](descriptions/urdf/34610.urdf) | Table with Drawers | Furniture | 0 | 5 | 32 | [JSON](descriptions/finaljson/34610.json) |
| [34617](descriptions/urdf/34617.urdf) | Table | Furniture | 0 | 2 | 32 | [JSON](descriptions/finaljson/34617.json) |
| [35059](descriptions/urdf/35059.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/35059.json) |
| [38516](descriptions/urdf/38516.urdf) | Dressing Cabinet with Mirror | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/38516.json) |
| [40147](descriptions/urdf/40147.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/40147.json) |
| [40417](descriptions/urdf/40417.urdf) | Storage Cabinet | Storage Furniture | 4 | 2 | 9 | [JSON](descriptions/finaljson/40417.json) |
| [40453](descriptions/urdf/40453.urdf) | Storage Cabinet | Storage Furniture | 0 | 3 | 7 | [JSON](descriptions/finaljson/40453.json) |
| [41003](descriptions/urdf/41003.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 9 | [JSON](descriptions/finaljson/41003.json) |
| [41004](descriptions/urdf/41004.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/41004.json) |
| [41083](descriptions/urdf/41083.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 7 | [JSON](descriptions/finaljson/41083.json) |
| [41085](descriptions/urdf/41085.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 9 | [JSON](descriptions/finaljson/41085.json) |
| [41086](descriptions/urdf/41086.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/41086.json) |
| [41452](descriptions/urdf/41452.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/41452.json) |
| [41510](descriptions/urdf/41510.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/41510.json) |
| [41529](descriptions/urdf/41529.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/41529.json) |
| [44781](descriptions/urdf/44781.urdf) | Storage Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/44781.json) |
| [44817](descriptions/urdf/44817.urdf) | Cabinet Drawer Unit | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/44817.json) |
| [44826](descriptions/urdf/44826.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/44826.json) |
| [44853](descriptions/urdf/44853.urdf) | Three-Drawer Cabinet | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/44853.json) |
| [44962](descriptions/urdf/44962.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/44962.json) |
| [45001](descriptions/urdf/45001.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/45001.json) |
| [45007](descriptions/urdf/45007.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45007.json) |
| [45087](descriptions/urdf/45087.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45087.json) |
| [45091](descriptions/urdf/45091.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45091.json) |
| [45092](descriptions/urdf/45092.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/45092.json) |
| [45130](descriptions/urdf/45130.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45130.json) |
| [45132](descriptions/urdf/45132.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/45132.json) |
| [45134](descriptions/urdf/45134.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45134.json) |
| [45135](descriptions/urdf/45135.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/45135.json) |
| [45146](descriptions/urdf/45146.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45146.json) |
| [45159](descriptions/urdf/45159.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/45159.json) |
| [45162](descriptions/urdf/45162.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45162.json) |
| [45164](descriptions/urdf/45164.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 6 | [JSON](descriptions/finaljson/45164.json) |
| [45166](descriptions/urdf/45166.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45166.json) |
| [45168](descriptions/urdf/45168.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45168.json) |
| [45173](descriptions/urdf/45173.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 6 | [JSON](descriptions/finaljson/45173.json) |
| [45176](descriptions/urdf/45176.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45176.json) |
| [45177](descriptions/urdf/45177.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45177.json) |
| [45189](descriptions/urdf/45189.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 10 | [JSON](descriptions/finaljson/45189.json) |
| [45194](descriptions/urdf/45194.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 8 | [JSON](descriptions/finaljson/45194.json) |
| [45203](descriptions/urdf/45203.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 6 | [JSON](descriptions/finaljson/45203.json) |
| [45212](descriptions/urdf/45212.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 6 | [JSON](descriptions/finaljson/45212.json) |
| [45213](descriptions/urdf/45213.urdf) | Storage Cabinet | Storage Furniture | 1 | 2 | 5 | [JSON](descriptions/finaljson/45213.json) |
| [45219](descriptions/urdf/45219.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 7 | [JSON](descriptions/finaljson/45219.json) |
| [45235](descriptions/urdf/45235.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45235.json) |
| [45238](descriptions/urdf/45238.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 7 | [JSON](descriptions/finaljson/45238.json) |
| [45243](descriptions/urdf/45243.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/45243.json) |
| [45244](descriptions/urdf/45244.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45244.json) |
| [45247](descriptions/urdf/45247.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45247.json) |
| [45248](descriptions/urdf/45248.urdf) | Storage Cabinet | Storage Furniture | 0 | 1 | 6 | [JSON](descriptions/finaljson/45248.json) |
| [45249](descriptions/urdf/45249.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/45249.json) |
| [45261](descriptions/urdf/45261.urdf) | Drawer Cabinet | Storage Furniture | 0 | 5 | 6 | [JSON](descriptions/finaljson/45261.json) |
| [45262](descriptions/urdf/45262.urdf) | Wooden Cabinet with Drawers and Shelves | Storage Furniture | 0 | 4 | 8 | [JSON](descriptions/finaljson/45262.json) |
| [45267](descriptions/urdf/45267.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45267.json) |
| [45271](descriptions/urdf/45271.urdf) | Kitchen Cabinet | Storage Furniture | 4 | 2 | 9 | [JSON](descriptions/finaljson/45271.json) |
| [45290](descriptions/urdf/45290.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/45290.json) |
| [45297](descriptions/urdf/45297.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45297.json) |
| [45305](descriptions/urdf/45305.urdf) | Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/45305.json) |
| [45323](descriptions/urdf/45323.urdf) | Wall-mounted Storage Cabinet with Mirror | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45323.json) |
| [45332](descriptions/urdf/45332.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 7 | [JSON](descriptions/finaljson/45332.json) |
| [45354](descriptions/urdf/45354.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 9 | [JSON](descriptions/finaljson/45354.json) |
| [45372](descriptions/urdf/45372.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45372.json) |
| [45374](descriptions/urdf/45374.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/45374.json) |
| [45378](descriptions/urdf/45378.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/45378.json) |
| [45384](descriptions/urdf/45384.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45384.json) |
| [45385](descriptions/urdf/45385.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45385.json) |
| [45387](descriptions/urdf/45387.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 9 | [JSON](descriptions/finaljson/45387.json) |
| [45397](descriptions/urdf/45397.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 5 | [JSON](descriptions/finaljson/45397.json) |
| [45403](descriptions/urdf/45403.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 6 | [JSON](descriptions/finaljson/45403.json) |
| [45413](descriptions/urdf/45413.urdf) | Cabinet | Storage Furniture | 0 | 1 | 6 | [JSON](descriptions/finaljson/45413.json) |
| [45415](descriptions/urdf/45415.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45415.json) |
| [45419](descriptions/urdf/45419.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45419.json) |
| [45420](descriptions/urdf/45420.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/45420.json) |
| [45423](descriptions/urdf/45423.urdf) | Tall Storage Cabinet | Storage Furniture | 2 | 0 | 7 | [JSON](descriptions/finaljson/45423.json) |
| [45427](descriptions/urdf/45427.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/45427.json) |
| [45443](descriptions/urdf/45443.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45443.json) |
| [45444](descriptions/urdf/45444.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 7 | [JSON](descriptions/finaljson/45444.json) |
| [45448](descriptions/urdf/45448.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45448.json) |
| [45463](descriptions/urdf/45463.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/45463.json) |
| [45503](descriptions/urdf/45503.urdf) | Cabinet | Storage Furniture | 3 | 0 | 8 | [JSON](descriptions/finaljson/45503.json) |
| [45504](descriptions/urdf/45504.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45504.json) |
| [45505](descriptions/urdf/45505.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/45505.json) |
| [45516](descriptions/urdf/45516.urdf) | Wall-mounted Storage Cabinet with Mirror | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45516.json) |
| [45523](descriptions/urdf/45523.urdf) | Wall Cabinet | Storage Furniture | 2 | 0 | 3 | [JSON](descriptions/finaljson/45523.json) |
| [45524](descriptions/urdf/45524.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/45524.json) |
| [45526](descriptions/urdf/45526.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45526.json) |
| [45573](descriptions/urdf/45573.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/45573.json) |
| [45575](descriptions/urdf/45575.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45575.json) |
| [45594](descriptions/urdf/45594.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/45594.json) |
| [45600](descriptions/urdf/45600.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45600.json) |
| [45606](descriptions/urdf/45606.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45606.json) |
| [45612](descriptions/urdf/45612.urdf) | Storage Cabinet | Storage Furniture | 4 | 2 | 9 | [JSON](descriptions/finaljson/45612.json) |
| [45620](descriptions/urdf/45620.urdf) | Cabinet | Storage Furniture | 0 | 1 | 6 | [JSON](descriptions/finaljson/45620.json) |
| [45621](descriptions/urdf/45621.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45621.json) |
| [45622](descriptions/urdf/45622.urdf) | Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/45622.json) |
| [45623](descriptions/urdf/45623.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/45623.json) |
| [45632](descriptions/urdf/45632.urdf) | Storage Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/45632.json) |
| [45633](descriptions/urdf/45633.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45633.json) |
| [45636](descriptions/urdf/45636.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 7 | [JSON](descriptions/finaljson/45636.json) |
| [45638](descriptions/urdf/45638.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45638.json) |
| [45642](descriptions/urdf/45642.urdf) | Storage Cabinet with Mirror and Drawers | Storage Furniture | 0 | 4 | 12 | [JSON](descriptions/finaljson/45642.json) |
| [45645](descriptions/urdf/45645.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45645.json) |
| [45662](descriptions/urdf/45662.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 5 | [JSON](descriptions/finaljson/45662.json) |
| [45667](descriptions/urdf/45667.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45667.json) |
| [45670](descriptions/urdf/45670.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/45670.json) |
| [45671](descriptions/urdf/45671.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45671.json) |
| [45676](descriptions/urdf/45676.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45676.json) |
| [45677](descriptions/urdf/45677.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/45677.json) |
| [45687](descriptions/urdf/45687.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45687.json) |
| [45689](descriptions/urdf/45689.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45689.json) |
| [45690](descriptions/urdf/45690.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 6 | [JSON](descriptions/finaljson/45690.json) |
| [45691](descriptions/urdf/45691.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45691.json) |
| [45694](descriptions/urdf/45694.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45694.json) |
| [45696](descriptions/urdf/45696.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 10 | [JSON](descriptions/finaljson/45696.json) |
| [45699](descriptions/urdf/45699.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45699.json) |
| [45710](descriptions/urdf/45710.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/45710.json) |
| [45717](descriptions/urdf/45717.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45717.json) |
| [45725](descriptions/urdf/45725.urdf) | Storage Cabinet | Storage Furniture | 8 | 6 | 24 | [JSON](descriptions/finaljson/45725.json) |
| [45746](descriptions/urdf/45746.urdf) | Two-Drawer Cabinet | Storage Furniture | 0 | 2 | 3 | [JSON](descriptions/finaljson/45746.json) |
| [45747](descriptions/urdf/45747.urdf) | Wall Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/45747.json) |
| [45749](descriptions/urdf/45749.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 9 | [JSON](descriptions/finaljson/45749.json) |
| [45756](descriptions/urdf/45756.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/45756.json) |
| [45759](descriptions/urdf/45759.urdf) | Tall Storage Cabinet | Storage Furniture | 3 | 1 | 10 | [JSON](descriptions/finaljson/45759.json) |
| [45767](descriptions/urdf/45767.urdf) | Tall Storage Cabinet | Storage Furniture | 2 | 0 | 5 | [JSON](descriptions/finaljson/45767.json) |
| [45776](descriptions/urdf/45776.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45776.json) |
| [45779](descriptions/urdf/45779.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45779.json) |
| [45780](descriptions/urdf/45780.urdf) | Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/45780.json) |
| [45783](descriptions/urdf/45783.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/45783.json) |
| [45784](descriptions/urdf/45784.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45784.json) |
| [45790](descriptions/urdf/45790.urdf) | Cabinet | Storage Furniture | 1 | 1 | 4 | [JSON](descriptions/finaljson/45790.json) |
| [45801](descriptions/urdf/45801.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/45801.json) |
| [45841](descriptions/urdf/45841.urdf) | Three-Drawer Cabinet | Storage Furniture | 0 | 3 | 4 | [JSON](descriptions/finaljson/45841.json) |
| [45850](descriptions/urdf/45850.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45850.json) |
| [45853](descriptions/urdf/45853.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45853.json) |
| [45855](descriptions/urdf/45855.urdf) | Wall Cabinet | Storage Furniture | 0 | 1 | 3 | [JSON](descriptions/finaljson/45855.json) |
| [45908](descriptions/urdf/45908.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45908.json) |
| [45910](descriptions/urdf/45910.urdf) | Cabinet | Storage Furniture | 0 | 1 | 3 | [JSON](descriptions/finaljson/45910.json) |
| [45915](descriptions/urdf/45915.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45915.json) |
| [45916](descriptions/urdf/45916.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45916.json) |
| [45922](descriptions/urdf/45922.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/45922.json) |
| [45936](descriptions/urdf/45936.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45936.json) |
| [45937](descriptions/urdf/45937.urdf) | Display Cabinet | Storage Furniture | 1 | 0 | 9 | [JSON](descriptions/finaljson/45937.json) |
| [45940](descriptions/urdf/45940.urdf) | Storage Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/45940.json) |
| [45948](descriptions/urdf/45948.urdf) | Storage Cabinet | Storage Furniture | 4 | 2 | 9 | [JSON](descriptions/finaljson/45948.json) |
| [45949](descriptions/urdf/45949.urdf) | Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/45949.json) |
| [45950](descriptions/urdf/45950.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45950.json) |
| [45961](descriptions/urdf/45961.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/45961.json) |
| [45963](descriptions/urdf/45963.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 5 | [JSON](descriptions/finaljson/45963.json) |
| [45964](descriptions/urdf/45964.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/45964.json) |
| [45984](descriptions/urdf/45984.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/45984.json) |
| [46002](descriptions/urdf/46002.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 8 | [JSON](descriptions/finaljson/46002.json) |
| [46014](descriptions/urdf/46014.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 4 | 5 | [JSON](descriptions/finaljson/46014.json) |
| [46019](descriptions/urdf/46019.urdf) | Cabinet | Storage Furniture | 2 | 0 | 5 | [JSON](descriptions/finaljson/46019.json) |
| [46029](descriptions/urdf/46029.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/46029.json) |
| [46033](descriptions/urdf/46033.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/46033.json) |
| [46037](descriptions/urdf/46037.urdf) | Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/46037.json) |
| [46044](descriptions/urdf/46044.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/46044.json) |
| [46045](descriptions/urdf/46045.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/46045.json) |
| [46057](descriptions/urdf/46057.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/46057.json) |
| [46060](descriptions/urdf/46060.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/46060.json) |
| [46084](descriptions/urdf/46084.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 7 | [JSON](descriptions/finaljson/46084.json) |
| [46092](descriptions/urdf/46092.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/46092.json) |
| [46107](descriptions/urdf/46107.urdf) | Cabinet | Storage Furniture | 0 | 1 | 2 | [JSON](descriptions/finaljson/46107.json) |
| [46108](descriptions/urdf/46108.urdf) | Cabinet | Storage Furniture | 4 | 0 | 6 | [JSON](descriptions/finaljson/46108.json) |
| [46109](descriptions/urdf/46109.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 5 | 6 | [JSON](descriptions/finaljson/46109.json) |
| [46117](descriptions/urdf/46117.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/46117.json) |
| [46120](descriptions/urdf/46120.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 7 | [JSON](descriptions/finaljson/46120.json) |
| [46123](descriptions/urdf/46123.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/46123.json) |
| [46127](descriptions/urdf/46127.urdf) | Cabinet | Storage Furniture | 0 | 1 | 2 | [JSON](descriptions/finaljson/46127.json) |
| [46130](descriptions/urdf/46130.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/46130.json) |
| [46132](descriptions/urdf/46132.urdf) | Cabinet | Storage Furniture | 0 | 1 | 2 | [JSON](descriptions/finaljson/46132.json) |
| [46134](descriptions/urdf/46134.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/46134.json) |
| [46145](descriptions/urdf/46145.urdf) | Storage Cabinet | Storage Furniture | 4 | 2 | 9 | [JSON](descriptions/finaljson/46145.json) |
| [46166](descriptions/urdf/46166.urdf) | Wall Cabinet | Storage Furniture | 2 | 0 | 3 | [JSON](descriptions/finaljson/46166.json) |
| [46179](descriptions/urdf/46179.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/46179.json) |
| [46180](descriptions/urdf/46180.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 4 | [JSON](descriptions/finaljson/46180.json) |
| [46197](descriptions/urdf/46197.urdf) | Tall Storage Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/46197.json) |
| [46199](descriptions/urdf/46199.urdf) | Storage Cabinet | Storage Furniture | 2 | 4 | 8 | [JSON](descriptions/finaljson/46199.json) |
| [46230](descriptions/urdf/46230.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/46230.json) |
| [46236](descriptions/urdf/46236.urdf) | Tall Storage Cabinet | Storage Furniture | 1 | 1 | 7 | [JSON](descriptions/finaljson/46236.json) |
| [46277](descriptions/urdf/46277.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/46277.json) |
| [46334](descriptions/urdf/46334.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/46334.json) |
| [46380](descriptions/urdf/46380.urdf) | Drawer Cabinet | Storage Furniture | 0 | 4 | 5 | [JSON](descriptions/finaljson/46380.json) |
| [46401](descriptions/urdf/46401.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/46401.json) |
| [46403](descriptions/urdf/46403.urdf) | Cabinet | Storage Furniture | 0 | 2 | 5 | [JSON](descriptions/finaljson/46403.json) |
| [46408](descriptions/urdf/46408.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/46408.json) |
| [46417](descriptions/urdf/46417.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/46417.json) |
| [46427](descriptions/urdf/46427.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/46427.json) |
| [46430](descriptions/urdf/46430.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/46430.json) |
| [46437](descriptions/urdf/46437.urdf) | Display Cabinet | Storage Furniture | 2 | 0 | 11 | [JSON](descriptions/finaljson/46437.json) |
| [46440](descriptions/urdf/46440.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/46440.json) |
| [46443](descriptions/urdf/46443.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/46443.json) |
| [46452](descriptions/urdf/46452.urdf) | Cabinet | Storage Furniture | 1 | 1 | 4 | [JSON](descriptions/finaljson/46452.json) |
| [46456](descriptions/urdf/46456.urdf) | Tall Storage Cabinet | Storage Furniture | 2 | 0 | 8 | [JSON](descriptions/finaljson/46456.json) |
| [46462](descriptions/urdf/46462.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/46462.json) |
| [46466](descriptions/urdf/46466.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/46466.json) |
| [46480](descriptions/urdf/46480.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/46480.json) |
| [46481](descriptions/urdf/46481.urdf) | Wooden Storage Cabinet | Storage Furniture | 2 | 0 | 5 | [JSON](descriptions/finaljson/46481.json) |
| [46490](descriptions/urdf/46490.urdf) | Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/46490.json) |
| [46537](descriptions/urdf/46537.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/46537.json) |
| [46544](descriptions/urdf/46544.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/46544.json) |
| [46549](descriptions/urdf/46549.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/46549.json) |
| [46556](descriptions/urdf/46556.urdf) | Storage Cabinet | Storage Furniture | 0 | 1 | 6 | [JSON](descriptions/finaljson/46556.json) |
| [46563](descriptions/urdf/46563.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/46563.json) |
| [46598](descriptions/urdf/46598.urdf) | Tall Storage Cabinet | Storage Furniture | 2 | 2 | 8 | [JSON](descriptions/finaljson/46598.json) |
| [46616](descriptions/urdf/46616.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/46616.json) |
| [46641](descriptions/urdf/46641.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/46641.json) |
| [46653](descriptions/urdf/46653.urdf) | Three-Drawer Cabinet | Storage Furniture | 0 | 3 | 4 | [JSON](descriptions/finaljson/46653.json) |
| [46655](descriptions/urdf/46655.urdf) | Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/46655.json) |
| [46699](descriptions/urdf/46699.urdf) | Wooden Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/46699.json) |
| [46700](descriptions/urdf/46700.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/46700.json) |
| [46732](descriptions/urdf/46732.urdf) | Tall Storage Cabinet | Storage Furniture | 2 | 0 | 7 | [JSON](descriptions/finaljson/46732.json) |
| [46741](descriptions/urdf/46741.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/46741.json) |
| [46744](descriptions/urdf/46744.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/46744.json) |
| [46762](descriptions/urdf/46762.urdf) | Cabinet Drawer Unit | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/46762.json) |
| [46768](descriptions/urdf/46768.urdf) | Cabinet | Storage Furniture | 0 | 2 | 6 | [JSON](descriptions/finaljson/46768.json) |
| [46787](descriptions/urdf/46787.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/46787.json) |
| [46801](descriptions/urdf/46801.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/46801.json) |
| [46825](descriptions/urdf/46825.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/46825.json) |
| [46839](descriptions/urdf/46839.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 7 | [JSON](descriptions/finaljson/46839.json) |
| [46847](descriptions/urdf/46847.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 7 | [JSON](descriptions/finaljson/46847.json) |
| [46856](descriptions/urdf/46856.urdf) | Storage Cabinet | Storage Furniture | 2 | 2 | 7 | [JSON](descriptions/finaljson/46856.json) |
| [46859](descriptions/urdf/46859.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/46859.json) |
| [46874](descriptions/urdf/46874.urdf) | Storage Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/46874.json) |
| [46879](descriptions/urdf/46879.urdf) | Storage Cabinet with Shelves and Drawers | Storage Furniture | 0 | 3 | 9 | [JSON](descriptions/finaljson/46879.json) |
| [46889](descriptions/urdf/46889.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/46889.json) |
| [46893](descriptions/urdf/46893.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/46893.json) |
| [46896](descriptions/urdf/46896.urdf) | Storage Cabinet with Shelves and Drawers | Storage Furniture | 0 | 2 | 8 | [JSON](descriptions/finaljson/46896.json) |
| [46906](descriptions/urdf/46906.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/46906.json) |
| [46922](descriptions/urdf/46922.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/46922.json) |
| [46944](descriptions/urdf/46944.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/46944.json) |
| [46955](descriptions/urdf/46955.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 10 | [JSON](descriptions/finaljson/46955.json) |
| [46966](descriptions/urdf/46966.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/46966.json) |
| [46981](descriptions/urdf/46981.urdf) | Storage Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/46981.json) |
| [47021](descriptions/urdf/47021.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/47021.json) |
| [47024](descriptions/urdf/47024.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 6 | [JSON](descriptions/finaljson/47024.json) |
| [47088](descriptions/urdf/47088.urdf) | Storage Cabinet | Storage Furniture | 2 | 1 | 5 | [JSON](descriptions/finaljson/47088.json) |
| [47089](descriptions/urdf/47089.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 4 | 7 | [JSON](descriptions/finaljson/47089.json) |
| [47099](descriptions/urdf/47099.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/47099.json) |
| [47133](descriptions/urdf/47133.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/47133.json) |
| [47168](descriptions/urdf/47168.urdf) | Cabinet | Storage Furniture | 0 | 1 | 6 | [JSON](descriptions/finaljson/47168.json) |
| [47178](descriptions/urdf/47178.urdf) | Three-Drawer Cabinet | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/47178.json) |
| [47180](descriptions/urdf/47180.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/47180.json) |
| [47182](descriptions/urdf/47182.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/47182.json) |
| [47183](descriptions/urdf/47183.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/47183.json) |
| [47185](descriptions/urdf/47185.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/47185.json) |
| [47187](descriptions/urdf/47187.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/47187.json) |
| [47207](descriptions/urdf/47207.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/47207.json) |
| [47227](descriptions/urdf/47227.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 9 | [JSON](descriptions/finaljson/47227.json) |
| [47233](descriptions/urdf/47233.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/47233.json) |
| [47235](descriptions/urdf/47235.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 6 | 8 | [JSON](descriptions/finaljson/47235.json) |
| [47238](descriptions/urdf/47238.urdf) | Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/47238.json) |
| [47252](descriptions/urdf/47252.urdf) | Storage Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/47252.json) |
| [47254](descriptions/urdf/47254.urdf) | Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/47254.json) |
| [47278](descriptions/urdf/47278.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/47278.json) |
| [47281](descriptions/urdf/47281.urdf) | Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/47281.json) |
| [47290](descriptions/urdf/47290.urdf) | Storage Cabinet | Storage Furniture | 6 | 0 | 12 | [JSON](descriptions/finaljson/47290.json) |
| [47296](descriptions/urdf/47296.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/47296.json) |
| [47315](descriptions/urdf/47315.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/47315.json) |
| [47316](descriptions/urdf/47316.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/47316.json) |
| [47388](descriptions/urdf/47388.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/47388.json) |
| [47391](descriptions/urdf/47391.urdf) | Cabinet | Storage Furniture | 0 | 1 | 2 | [JSON](descriptions/finaljson/47391.json) |
| [47419](descriptions/urdf/47419.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/47419.json) |
| [47438](descriptions/urdf/47438.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/47438.json) |
| [47443](descriptions/urdf/47443.urdf) | Bookshelf Cabinet | Storage Furniture | 2 | 0 | 12 | [JSON](descriptions/finaljson/47443.json) |
| [47466](descriptions/urdf/47466.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 10 | 11 | [JSON](descriptions/finaljson/47466.json) |
| [47514](descriptions/urdf/47514.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/47514.json) |
| [47529](descriptions/urdf/47529.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/47529.json) |
| [47565](descriptions/urdf/47565.urdf) | Two-Drawer Cabinet | Storage Furniture | 0 | 2 | 3 | [JSON](descriptions/finaljson/47565.json) |
| [47570](descriptions/urdf/47570.urdf) | Cabinet | Storage Furniture | 1 | 1 | 4 | [JSON](descriptions/finaljson/47570.json) |
| [47577](descriptions/urdf/47577.urdf) | Tall Storage Cabinet | Storage Furniture | 2 | 0 | 7 | [JSON](descriptions/finaljson/47577.json) |
| [47578](descriptions/urdf/47578.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/47578.json) |
| [47595](descriptions/urdf/47595.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 8 | [JSON](descriptions/finaljson/47595.json) |
| [47601](descriptions/urdf/47601.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/47601.json) |
| [47613](descriptions/urdf/47613.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/47613.json) |
| [47632](descriptions/urdf/47632.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/47632.json) |
| [47645](descriptions/urdf/47645.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 6 | [JSON](descriptions/finaljson/47645.json) |
| [47648](descriptions/urdf/47648.urdf) | Wooden Cabinet with Shelves and Drawers | Storage Furniture | 4 | 2 | 12 | [JSON](descriptions/finaljson/47648.json) |
| [47651](descriptions/urdf/47651.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/47651.json) |
| [47669](descriptions/urdf/47669.urdf) | Storage Cabinet | Storage Furniture | 6 | 0 | 12 | [JSON](descriptions/finaljson/47669.json) |
| [47686](descriptions/urdf/47686.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/47686.json) |
| [47701](descriptions/urdf/47701.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 8 | [JSON](descriptions/finaljson/47701.json) |
| [47711](descriptions/urdf/47711.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 4 | [JSON](descriptions/finaljson/47711.json) |
| [47729](descriptions/urdf/47729.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/47729.json) |
| [47742](descriptions/urdf/47742.urdf) | Cabinet | Storage Furniture | 1 | 0 | 4 | [JSON](descriptions/finaljson/47742.json) |
| [47747](descriptions/urdf/47747.urdf) | Tall Storage Cabinet | Storage Furniture | 2 | 0 | 7 | [JSON](descriptions/finaljson/47747.json) |
| [47808](descriptions/urdf/47808.urdf) | Tall Storage Cabinet | Storage Furniture | 2 | 0 | 7 | [JSON](descriptions/finaljson/47808.json) |
| [47817](descriptions/urdf/47817.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/47817.json) |
| [47853](descriptions/urdf/47853.urdf) | Tall Storage Cabinet | Storage Furniture | 3 | 0 | 9 | [JSON](descriptions/finaljson/47853.json) |
| [47926](descriptions/urdf/47926.urdf) | Storage Cabinet | Storage Furniture | 4 | 2 | 9 | [JSON](descriptions/finaljson/47926.json) |
| [47944](descriptions/urdf/47944.urdf) | Storage Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/47944.json) |
| [47954](descriptions/urdf/47954.urdf) | Wall Cabinet | Storage Furniture | 0 | 2 | 3 | [JSON](descriptions/finaljson/47954.json) |
| [47963](descriptions/urdf/47963.urdf) | Cabinet | Storage Furniture | 0 | 1 | 2 | [JSON](descriptions/finaljson/47963.json) |
| [47976](descriptions/urdf/47976.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 9 | [JSON](descriptions/finaljson/47976.json) |
| [48010](descriptions/urdf/48010.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/48010.json) |
| [48013](descriptions/urdf/48013.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 5 | [JSON](descriptions/finaljson/48013.json) |
| [48018](descriptions/urdf/48018.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 9 | [JSON](descriptions/finaljson/48018.json) |
| [48023](descriptions/urdf/48023.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/48023.json) |
| [48036](descriptions/urdf/48036.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/48036.json) |
| [48051](descriptions/urdf/48051.urdf) | Drawer Cabinet | Storage Furniture | 0 | 5 | 6 | [JSON](descriptions/finaljson/48051.json) |
| [48063](descriptions/urdf/48063.urdf) | Kitchen Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/48063.json) |
| [48167](descriptions/urdf/48167.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/48167.json) |
| [48169](descriptions/urdf/48169.urdf) | Chest of Drawers | Storage Furniture | 0 | 5 | 6 | [JSON](descriptions/finaljson/48169.json) |
| [48177](descriptions/urdf/48177.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/48177.json) |
| [48243](descriptions/urdf/48243.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/48243.json) |
| [48253](descriptions/urdf/48253.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/48253.json) |
| [48258](descriptions/urdf/48258.urdf) | Cabinet with Drawers | Storage Furniture | 0 | 4 | 6 | [JSON](descriptions/finaljson/48258.json) |
| [48263](descriptions/urdf/48263.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 4 | 5 | [JSON](descriptions/finaljson/48263.json) |
| [48271](descriptions/urdf/48271.urdf) | Storage Cabinet | Storage Furniture | 1 | 0 | 5 | [JSON](descriptions/finaljson/48271.json) |
| [48356](descriptions/urdf/48356.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 9 | [JSON](descriptions/finaljson/48356.json) |
| [48379](descriptions/urdf/48379.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/48379.json) |
| [48381](descriptions/urdf/48381.urdf) | Wall Cabinet | Storage Furniture | 2 | 0 | 3 | [JSON](descriptions/finaljson/48381.json) |
| [48413](descriptions/urdf/48413.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/48413.json) |
| [48452](descriptions/urdf/48452.urdf) | Cabinet | Storage Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/48452.json) |
| [48467](descriptions/urdf/48467.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/48467.json) |
| [48479](descriptions/urdf/48479.urdf) | Storage Cabinet | Storage Furniture | 0 | 2 | 5 | [JSON](descriptions/finaljson/48479.json) |
| [48490](descriptions/urdf/48490.urdf) | Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/48490.json) |
| [48491](descriptions/urdf/48491.urdf) | Three-Drawer Cabinet | Storage Furniture | 0 | 3 | 4 | [JSON](descriptions/finaljson/48491.json) |
| [48492](descriptions/urdf/48492.urdf) | Storage Chest | Storage Furniture | 3 | 0 | 8 | [JSON](descriptions/finaljson/48492.json) |
| [48497](descriptions/urdf/48497.urdf) | Storage Cabinet | Storage Furniture | 0 | 8 | 20 | [JSON](descriptions/finaljson/48497.json) |
| [48513](descriptions/urdf/48513.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/48513.json) |
| [48517](descriptions/urdf/48517.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/48517.json) |
| [48519](descriptions/urdf/48519.urdf) | Wall Cabinet | Storage Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/48519.json) |
| [48623](descriptions/urdf/48623.urdf) | Storage Cabinet | Storage Furniture | 6 | 0 | 12 | [JSON](descriptions/finaljson/48623.json) |
| [48686](descriptions/urdf/48686.urdf) | Cabinet | Storage Furniture | 0 | 1 | 3 | [JSON](descriptions/finaljson/48686.json) |
| [48700](descriptions/urdf/48700.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 5 | [JSON](descriptions/finaljson/48700.json) |
| [48721](descriptions/urdf/48721.urdf) | Tall Storage Cabinet | Storage Furniture | 1 | 0 | 7 | [JSON](descriptions/finaljson/48721.json) |
| [48740](descriptions/urdf/48740.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/48740.json) |
| [48746](descriptions/urdf/48746.urdf) | Cabinet | Storage Furniture | 0 | 1 | 6 | [JSON](descriptions/finaljson/48746.json) |
| [48797](descriptions/urdf/48797.urdf) | Tall Storage Cabinet | Storage Furniture | 3 | 0 | 9 | [JSON](descriptions/finaljson/48797.json) |
| [48855](descriptions/urdf/48855.urdf) | Storage Cabinet | Storage Furniture | 2 | 1 | 6 | [JSON](descriptions/finaljson/48855.json) |
| [48859](descriptions/urdf/48859.urdf) | Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/48859.json) |
| [48876](descriptions/urdf/48876.urdf) | Storage Cabinet with Drawers | Storage Furniture | 0 | 3 | 5 | [JSON](descriptions/finaljson/48876.json) |
| [48878](descriptions/urdf/48878.urdf) | Storage Cabinet | Storage Furniture | 1 | 1 | 5 | [JSON](descriptions/finaljson/48878.json) |
| [49025](descriptions/urdf/49025.urdf) | Storage Cabinet | Storage Furniture | 4 | 0 | 9 | [JSON](descriptions/finaljson/49025.json) |
| [49038](descriptions/urdf/49038.urdf) | Cabinet | Storage Furniture | 2 | 0 | 3 | [JSON](descriptions/finaljson/49038.json) |
| [49042](descriptions/urdf/49042.urdf) | Cabinet | Storage Furniture | 2 | 0 | 4 | [JSON](descriptions/finaljson/49042.json) |
| [49062](descriptions/urdf/49062.urdf) | Storage Cabinet | Storage Furniture | 6 | 0 | 12 | [JSON](descriptions/finaljson/49062.json) |
| [49132](descriptions/urdf/49132.urdf) | Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/49132.json) |
| [49133](descriptions/urdf/49133.urdf) | Storage Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/49133.json) |
| [49140](descriptions/urdf/49140.urdf) | Drawer Cabinet | Storage Furniture | 0 | 4 | 5 | [JSON](descriptions/finaljson/49140.json) |
| [49182](descriptions/urdf/49182.urdf) | Cabinet | Storage Furniture | 2 | 0 | 6 | [JSON](descriptions/finaljson/49182.json) |
| [49188](descriptions/urdf/49188.urdf) | Storage Cabinet | Storage Furniture | 6 | 0 | 12 | [JSON](descriptions/finaljson/49188.json) |
| [100013](descriptions/urdf/100013.urdf) | Remote Control | Electronic Device | 0 | 39 | 40 | [JSON](descriptions/finaljson/100013.json) |
| [100015](descriptions/urdf/100015.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100015.json) |
| [100017](descriptions/urdf/100017.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100017.json) |
| [100021](descriptions/urdf/100021.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100021.json) |
| [100023](descriptions/urdf/100023.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100023.json) |
| [100025](descriptions/urdf/100025.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100025.json) |
| [100028](descriptions/urdf/100028.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100028.json) |
| [100031](descriptions/urdf/100031.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100031.json) |
| [100032](descriptions/urdf/100032.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100032.json) |
| [100033](descriptions/urdf/100033.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100033.json) |
| [100038](descriptions/urdf/100038.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100038.json) |
| [100040](descriptions/urdf/100040.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100040.json) |
| [100045](descriptions/urdf/100045.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100045.json) |
| [100047](descriptions/urdf/100047.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100047.json) |
| [100051](descriptions/urdf/100051.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100051.json) |
| [100054](descriptions/urdf/100054.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100054.json) |
| [100055](descriptions/urdf/100055.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100055.json) |
| [100056](descriptions/urdf/100056.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100056.json) |
| [100057](descriptions/urdf/100057.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100057.json) |
| [100058](descriptions/urdf/100058.urdf) | Kitchen Pot | Cookware | 0 | 3 | 4 | [JSON](descriptions/finaljson/100058.json) |
| [100060](descriptions/urdf/100060.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100060.json) |
| [100061](descriptions/urdf/100061.urdf) | USB Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100061.json) |
| [100064](descriptions/urdf/100064.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100064.json) |
| [100065](descriptions/urdf/100065.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100065.json) |
| [100068](descriptions/urdf/100068.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100068.json) |
| [100071](descriptions/urdf/100071.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100071.json) |
| [100072](descriptions/urdf/100072.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100072.json) |
| [100073](descriptions/urdf/100073.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100073.json) |
| [100075](descriptions/urdf/100075.urdf) | Cart | Transport Equipment | 2 | 0 | 4 | [JSON](descriptions/finaljson/100075.json) |
| [100078](descriptions/urdf/100078.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100078.json) |
| [100079](descriptions/urdf/100079.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100079.json) |
| [100082](descriptions/urdf/100082.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100082.json) |
| [100084](descriptions/urdf/100084.urdf) | Cart | Transport Equipment | 1 | 0 | 2 | [JSON](descriptions/finaljson/100084.json) |
| [100085](descriptions/urdf/100085.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100085.json) |
| [100086](descriptions/urdf/100086.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100086.json) |
| [100087](descriptions/urdf/100087.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100087.json) |
| [100092](descriptions/urdf/100092.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100092.json) |
| [100095](descriptions/urdf/100095.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100095.json) |
| [100103](descriptions/urdf/100103.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100103.json) |
| [100106](descriptions/urdf/100106.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100106.json) |
| [100108](descriptions/urdf/100108.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100108.json) |
| [100109](descriptions/urdf/100109.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100109.json) |
| [100113](descriptions/urdf/100113.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100113.json) |
| [100116](descriptions/urdf/100116.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100116.json) |
| [100123](descriptions/urdf/100123.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100123.json) |
| [100128](descriptions/urdf/100128.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100128.json) |
| [100129](descriptions/urdf/100129.urdf) | Box | Container | 2 | 0 | 4 | [JSON](descriptions/finaljson/100129.json) |
| [100133](descriptions/urdf/100133.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100133.json) |
| [100141](descriptions/urdf/100141.urdf) | Storage Box | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100141.json) |
| [100142](descriptions/urdf/100142.urdf) | Pliers | HandTool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100142.json) |
| [100144](descriptions/urdf/100144.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100144.json) |
| [100146](descriptions/urdf/100146.urdf) | Pliers | HandTool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100146.json) |
| [100150](descriptions/urdf/100150.urdf) | Pliers | HandTool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100150.json) |
| [100154](descriptions/urdf/100154.urdf) | Box | Container | 4 | 0 | 5 | [JSON](descriptions/finaljson/100154.json) |
| [100162](descriptions/urdf/100162.urdf) | Box | Container | 4 | 0 | 5 | [JSON](descriptions/finaljson/100162.json) |
| [100172](descriptions/urdf/100172.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100172.json) |
| [100174](descriptions/urdf/100174.urdf) | Storage Box | Container | 1 | 0 | 3 | [JSON](descriptions/finaljson/100174.json) |
| [100178](descriptions/urdf/100178.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100178.json) |
| [100179](descriptions/urdf/100179.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100179.json) |
| [100180](descriptions/urdf/100180.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100180.json) |
| [100182](descriptions/urdf/100182.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100182.json) |
| [100188](descriptions/urdf/100188.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100188.json) |
| [100189](descriptions/urdf/100189.urdf) | Storage Box | Container | 1 | 0 | 3 | [JSON](descriptions/finaljson/100189.json) |
| [100191](descriptions/urdf/100191.urdf) | Box | Packaging Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100191.json) |
| [100194](descriptions/urdf/100194.urdf) | Box | Container | 6 | 0 | 7 | [JSON](descriptions/finaljson/100194.json) |
| [100197](descriptions/urdf/100197.urdf) | Box | Container | 4 | 0 | 5 | [JSON](descriptions/finaljson/100197.json) |
| [100202](descriptions/urdf/100202.urdf) | Box | Container | 4 | 0 | 5 | [JSON](descriptions/finaljson/100202.json) |
| [100214](descriptions/urdf/100214.urdf) | Storage Box | Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/100214.json) |
| [100221](descriptions/urdf/100221.urdf) | Storage Chest | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100221.json) |
| [100224](descriptions/urdf/100224.urdf) | Box | Packaging Container | 4 | 0 | 5 | [JSON](descriptions/finaljson/100224.json) |
| [100234](descriptions/urdf/100234.urdf) | Box | Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/100234.json) |
| [100243](descriptions/urdf/100243.urdf) | Storage Box | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100243.json) |
| [100247](descriptions/urdf/100247.urdf) | Storage Box | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100247.json) |
| [100248](descriptions/urdf/100248.urdf) | Suitcase | Luggage | 0 | 1 | 2 | [JSON](descriptions/finaljson/100248.json) |
| [100249](descriptions/urdf/100249.urdf) | Suitcase | Luggage | 1 | 0 | 3 | [JSON](descriptions/finaljson/100249.json) |
| [100269](descriptions/urdf/100269.urdf) | Remote | ElectronicControlDevice | 0 | 44 | 45 | [JSON](descriptions/finaljson/100269.json) |
| [100270](descriptions/urdf/100270.urdf) | Remote Control | Electronic Device Accessory | 0 | 46 | 47 | [JSON](descriptions/finaljson/100270.json) |
| [100279](descriptions/urdf/100279.urdf) | Printer | Office Equipment | 1 | 11 | 14 | [JSON](descriptions/finaljson/100279.json) |
| [100282](descriptions/urdf/100282.urdf) | Washing Machine | Home Appliance | 2 | 7 | 10 | [JSON](descriptions/finaljson/100282.json) |
| [100283](descriptions/urdf/100283.urdf) | Washing Machine | Home Appliance | 2 | 9 | 12 | [JSON](descriptions/finaljson/100283.json) |
| [100285](descriptions/urdf/100285.urdf) | Lighter | Handheld Fire Ignition Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100285.json) |
| [100289](descriptions/urdf/100289.urdf) | Lighter | Portable Fire Ignition Device | 2 | 0 | 4 | [JSON](descriptions/finaljson/100289.json) |
| [100292](descriptions/urdf/100292.urdf) | Lighter | Handheld Fire Ignition Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100292.json) |
| [100293](descriptions/urdf/100293.urdf) | Lighter | Handheld Fire Ignition Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/100293.json) |
| [100294](descriptions/urdf/100294.urdf) | Lighter | Handheld Ignition Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100294.json) |
| [100295](descriptions/urdf/100295.urdf) | Lighter | Handheld Fire Ignition Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100295.json) |
| [100309](descriptions/urdf/100309.urdf) | Lighter | Portable Fire Ignition Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100309.json) |
| [100310](descriptions/urdf/100310.urdf) | Lighter | Everyday Object / Fire-starting Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/100310.json) |
| [100311](descriptions/urdf/100311.urdf) | Lighter | Handheld Ignition Device | 1 | 1 | 4 | [JSON](descriptions/finaljson/100311.json) |
| [100313](descriptions/urdf/100313.urdf) | Lighter | Handheld Fire Ignition Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/100313.json) |
| [100317](descriptions/urdf/100317.urdf) | Lighter | Portable Fire Ignition Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100317.json) |
| [100318](descriptions/urdf/100318.urdf) | Lighter | Portable Fire Ignition Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100318.json) |
| [100319](descriptions/urdf/100319.urdf) | Lighter | Handheld Fire Ignition Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100319.json) |
| [100320](descriptions/urdf/100320.urdf) | Lighter | Handheld Fire Ignition Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100320.json) |
| [100321](descriptions/urdf/100321.urdf) | Lighter | Portable Fire Ignition Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100321.json) |
| [100330](descriptions/urdf/100330.urdf) | Lighter | Handheld Fire Ignition Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100330.json) |
| [100334](descriptions/urdf/100334.urdf) | Lighter | Handheld Fire Ignition Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100334.json) |
| [100335](descriptions/urdf/100335.urdf) | Lighter | Portable Fire Ignition Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100335.json) |
| [100340](descriptions/urdf/100340.urdf) | Lighter | Handheld Fire Ignition Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/100340.json) |
| [100343](descriptions/urdf/100343.urdf) | Lighter | Handheld Fire Ignition Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/100343.json) |
| [100348](descriptions/urdf/100348.urdf) | Lighter | Handheld Fire Ignition Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/100348.json) |
| [100350](descriptions/urdf/100350.urdf) | Lighter | Portable Fire Ignition Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100350.json) |
| [100354](descriptions/urdf/100354.urdf) | Lighter | Portable Fire Ignition Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100354.json) |
| [100355](descriptions/urdf/100355.urdf) | Lighter | Handheld Fire Ignition Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/100355.json) |
| [100366](descriptions/urdf/100366.urdf) | Electrical Wall Switch | Electrical Control Device | 0 | 2 | 3 | [JSON](descriptions/finaljson/100366.json) |
| [100367](descriptions/urdf/100367.urdf) | Wall Switch | Electrical Control Device | 4 | 0 | 5 | [JSON](descriptions/finaljson/100367.json) |
| [100368](descriptions/urdf/100368.urdf) | Wall Switch | Electrical Control Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100368.json) |
| [100385](descriptions/urdf/100385.urdf) | Remote Control | Electronic Device | 0 | 40 | 42 | [JSON](descriptions/finaljson/100385.json) |
| [100392](descriptions/urdf/100392.urdf) | Remote Control | Electronic Device | 0 | 42 | 43 | [JSON](descriptions/finaljson/100392.json) |
| [100395](descriptions/urdf/100395.urdf) | Remote | Electronic Controller | 0 | 7 | 10 | [JSON](descriptions/finaljson/100395.json) |
| [100405](descriptions/urdf/100405.urdf) | Remote | Electronic Control Device | 1 | 8 | 10 | [JSON](descriptions/finaljson/100405.json) |
| [100408](descriptions/urdf/100408.urdf) | Remote Control | Electronic Device | 0 | 37 | 38 | [JSON](descriptions/finaljson/100408.json) |
| [100412](descriptions/urdf/100412.urdf) | Remote Control | Electronic Device | 0 | 29 | 30 | [JSON](descriptions/finaljson/100412.json) |
| [100426](descriptions/urdf/100426.urdf) | Box | Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/100426.json) |
| [100431](descriptions/urdf/100431.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100431.json) |
| [100432](descriptions/urdf/100432.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100432.json) |
| [100435](descriptions/urdf/100435.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100435.json) |
| [100438](descriptions/urdf/100438.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100438.json) |
| [100439](descriptions/urdf/100439.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100439.json) |
| [100441](descriptions/urdf/100441.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100441.json) |
| [100442](descriptions/urdf/100442.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100442.json) |
| [100443](descriptions/urdf/100443.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100443.json) |
| [100444](descriptions/urdf/100444.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100444.json) |
| [100446](descriptions/urdf/100446.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100446.json) |
| [100448](descriptions/urdf/100448.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100448.json) |
| [100452](descriptions/urdf/100452.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100452.json) |
| [100454](descriptions/urdf/100454.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100454.json) |
| [100460](descriptions/urdf/100460.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100460.json) |
| [100461](descriptions/urdf/100461.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100461.json) |
| [100462](descriptions/urdf/100462.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100462.json) |
| [100464](descriptions/urdf/100464.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100464.json) |
| [100465](descriptions/urdf/100465.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100465.json) |
| [100466](descriptions/urdf/100466.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100466.json) |
| [100468](descriptions/urdf/100468.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100468.json) |
| [100469](descriptions/urdf/100469.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100469.json) |
| [100470](descriptions/urdf/100470.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100470.json) |
| [100472](descriptions/urdf/100472.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100472.json) |
| [100473](descriptions/urdf/100473.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100473.json) |
| [100477](descriptions/urdf/100477.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100477.json) |
| [100481](descriptions/urdf/100481.urdf) | Bucket | Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/100481.json) |
| [100482](descriptions/urdf/100482.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100482.json) |
| [100484](descriptions/urdf/100484.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100484.json) |
| [100486](descriptions/urdf/100486.urdf) | Bucket | Container | 1 | 0 | 3 | [JSON](descriptions/finaljson/100486.json) |
| [100487](descriptions/urdf/100487.urdf) | Cart | Manual Transport Equipment | 1 | 0 | 2 | [JSON](descriptions/finaljson/100487.json) |
| [100488](descriptions/urdf/100488.urdf) | Cart | Vehicle | 5 | 0 | 6 | [JSON](descriptions/finaljson/100488.json) |
| [100490](descriptions/urdf/100490.urdf) | Cart | Wheelbarrow | 1 | 0 | 2 | [JSON](descriptions/finaljson/100490.json) |
| [100491](descriptions/urdf/100491.urdf) | Shopping Cart | Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/100491.json) |
| [100494](descriptions/urdf/100494.urdf) | Cart | Hand Truck / Trolley | 2 | 0 | 3 | [JSON](descriptions/finaljson/100494.json) |
| [100496](descriptions/urdf/100496.urdf) | Cart | Utility Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/100496.json) |
| [100498](descriptions/urdf/100498.urdf) | Shopping Cart | Transport/Utility Object | 4 | 0 | 5 | [JSON](descriptions/finaljson/100498.json) |
| [100500](descriptions/urdf/100500.urdf) | Cart | Wheelbarrow | 1 | 0 | 2 | [JSON](descriptions/finaljson/100500.json) |
| [100501](descriptions/urdf/100501.urdf) | Cart | Transport/Utility Object | 4 | 0 | 5 | [JSON](descriptions/finaljson/100501.json) |
| [100502](descriptions/urdf/100502.urdf) | Cart | Hand Truck / Trolley | 4 | 0 | 5 | [JSON](descriptions/finaljson/100502.json) |
| [100504](descriptions/urdf/100504.urdf) | Cart | Mobile Display Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/100504.json) |
| [100507](descriptions/urdf/100507.urdf) | Cart | Manual Transport Equipment | 1 | 0 | 2 | [JSON](descriptions/finaljson/100507.json) |
| [100508](descriptions/urdf/100508.urdf) | Cart | Utility Vehicle / Shopping Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/100508.json) |
| [100509](descriptions/urdf/100509.urdf) | Cart | Transport Equipment | 1 | 0 | 2 | [JSON](descriptions/finaljson/100509.json) |
| [100511](descriptions/urdf/100511.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100511.json) |
| [100513](descriptions/urdf/100513.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100513.json) |
| [100520](descriptions/urdf/100520.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100520.json) |
| [100521](descriptions/urdf/100521.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100521.json) |
| [100523](descriptions/urdf/100523.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100523.json) |
| [100526](descriptions/urdf/100526.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100526.json) |
| [100531](descriptions/urdf/100531.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100531.json) |
| [100532](descriptions/urdf/100532.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100532.json) |
| [100550](descriptions/urdf/100550.urdf) | Suitcase | Luggage | 2 | 0 | 3 | [JSON](descriptions/finaljson/100550.json) |
| [100557](descriptions/urdf/100557.urdf) | Folding Chair | Furniture | 2 | 0 | 3 | [JSON](descriptions/finaljson/100557.json) |
| [100561](descriptions/urdf/100561.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100561.json) |
| [100562](descriptions/urdf/100562.urdf) | Folding Chair | Furniture | 2 | 0 | 3 | [JSON](descriptions/finaljson/100562.json) |
| [100568](descriptions/urdf/100568.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100568.json) |
| [100579](descriptions/urdf/100579.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100579.json) |
| [100586](descriptions/urdf/100586.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100586.json) |
| [100590](descriptions/urdf/100590.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100590.json) |
| [100599](descriptions/urdf/100599.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100599.json) |
| [100600](descriptions/urdf/100600.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100600.json) |
| [100608](descriptions/urdf/100608.urdf) | Folding Chair | Furniture | 2 | 0 | 3 | [JSON](descriptions/finaljson/100608.json) |
| [100609](descriptions/urdf/100609.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100609.json) |
| [100611](descriptions/urdf/100611.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100611.json) |
| [100613](descriptions/urdf/100613.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100613.json) |
| [100616](descriptions/urdf/100616.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/100616.json) |
| [100619](descriptions/urdf/100619.urdf) | Kitchen Pot | Cookware | 0 | 2 | 3 | [JSON](descriptions/finaljson/100619.json) |
| [100623](descriptions/urdf/100623.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100623.json) |
| [100658](descriptions/urdf/100658.urdf) | Box | Container | 4 | 0 | 5 | [JSON](descriptions/finaljson/100658.json) |
| [100664](descriptions/urdf/100664.urdf) | Storage Box | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100664.json) |
| [100671](descriptions/urdf/100671.urdf) | Storage Box | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100671.json) |
| [100676](descriptions/urdf/100676.urdf) | Box | Packaging Container | 4 | 0 | 5 | [JSON](descriptions/finaljson/100676.json) |
| [100685](descriptions/urdf/100685.urdf) | Pizza Box | Packaging Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/100685.json) |
| [100693](descriptions/urdf/100693.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/100693.json) |
| [100705](descriptions/urdf/100705.urdf) | Pliers | HandTool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100705.json) |
| [100706](descriptions/urdf/100706.urdf) | Remote Control | Electronic Device | 0 | 27 | 28 | [JSON](descriptions/finaljson/100706.json) |
| [100712](descriptions/urdf/100712.urdf) | Remote Control | Electronic Device | 0 | 8 | 10 | [JSON](descriptions/finaljson/100712.json) |
| [100720](descriptions/urdf/100720.urdf) | Globe | Educational/Decorative Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100720.json) |
| [100731](descriptions/urdf/100731.urdf) | Trashcan | Household Utility Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100731.json) |
| [100732](descriptions/urdf/100732.urdf) | Trashcan | Household Utility Object | 1 | 1 | 3 | [JSON](descriptions/finaljson/100732.json) |
| [100733](descriptions/urdf/100733.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100733.json) |
| [100736](descriptions/urdf/100736.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100736.json) |
| [100739](descriptions/urdf/100739.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100739.json) |
| [100740](descriptions/urdf/100740.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100740.json) |
| [100741](descriptions/urdf/100741.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100741.json) |
| [100743](descriptions/urdf/100743.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100743.json) |
| [100744](descriptions/urdf/100744.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100744.json) |
| [100745](descriptions/urdf/100745.urdf) | Globe | Educational Instrument | 1 | 0 | 2 | [JSON](descriptions/finaljson/100745.json) |
| [100746](descriptions/urdf/100746.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100746.json) |
| [100747](descriptions/urdf/100747.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100747.json) |
| [100748](descriptions/urdf/100748.urdf) | Globe | Educational Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/100748.json) |
| [100749](descriptions/urdf/100749.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100749.json) |
| [100750](descriptions/urdf/100750.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100750.json) |
| [100751](descriptions/urdf/100751.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100751.json) |
| [100753](descriptions/urdf/100753.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100753.json) |
| [100754](descriptions/urdf/100754.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100754.json) |
| [100755](descriptions/urdf/100755.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100755.json) |
| [100756](descriptions/urdf/100756.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100756.json) |
| [100757](descriptions/urdf/100757.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100757.json) |
| [100758](descriptions/urdf/100758.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100758.json) |
| [100759](descriptions/urdf/100759.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100759.json) |
| [100760](descriptions/urdf/100760.urdf) | Globe | Educational Instrument | 2 | 0 | 3 | [JSON](descriptions/finaljson/100760.json) |
| [100761](descriptions/urdf/100761.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100761.json) |
| [100762](descriptions/urdf/100762.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100762.json) |
| [100763](descriptions/urdf/100763.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100763.json) |
| [100764](descriptions/urdf/100764.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100764.json) |
| [100765](descriptions/urdf/100765.urdf) | Globe | Educational Instrument | 2 | 0 | 3 | [JSON](descriptions/finaljson/100765.json) |
| [100767](descriptions/urdf/100767.urdf) | Suitcase | Luggage | 4 | 0 | 5 | [JSON](descriptions/finaljson/100767.json) |
| [100768](descriptions/urdf/100768.urdf) | Globe | Educational Instrument | 2 | 0 | 3 | [JSON](descriptions/finaljson/100768.json) |
| [100770](descriptions/urdf/100770.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100770.json) |
| [100776](descriptions/urdf/100776.urdf) | Suitcase | Luggage | 4 | 0 | 5 | [JSON](descriptions/finaljson/100776.json) |
| [100778](descriptions/urdf/100778.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100778.json) |
| [100779](descriptions/urdf/100779.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100779.json) |
| [100781](descriptions/urdf/100781.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100781.json) |
| [100782](descriptions/urdf/100782.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100782.json) |
| [100783](descriptions/urdf/100783.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100783.json) |
| [100784](descriptions/urdf/100784.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100784.json) |
| [100785](descriptions/urdf/100785.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100785.json) |
| [100786](descriptions/urdf/100786.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100786.json) |
| [100787](descriptions/urdf/100787.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/100787.json) |
| [100788](descriptions/urdf/100788.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100788.json) |
| [100789](descriptions/urdf/100789.urdf) | Globe | Educational Instrument | 2 | 0 | 3 | [JSON](descriptions/finaljson/100789.json) |
| [100790](descriptions/urdf/100790.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100790.json) |
| [100791](descriptions/urdf/100791.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100791.json) |
| [100792](descriptions/urdf/100792.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100792.json) |
| [100793](descriptions/urdf/100793.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100793.json) |
| [100794](descriptions/urdf/100794.urdf) | Globe | Decorative Object / Educational Instrument | 3 | 0 | 4 | [JSON](descriptions/finaljson/100794.json) |
| [100795](descriptions/urdf/100795.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100795.json) |
| [100796](descriptions/urdf/100796.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100796.json) |
| [100798](descriptions/urdf/100798.urdf) | Globe | Educational Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/100798.json) |
| [100799](descriptions/urdf/100799.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100799.json) |
| [100800](descriptions/urdf/100800.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100800.json) |
| [100801](descriptions/urdf/100801.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100801.json) |
| [100803](descriptions/urdf/100803.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/100803.json) |
| [100809](descriptions/urdf/100809.urdf) | Remote Control | Electronic Device | 0 | 57 | 59 | [JSON](descriptions/finaljson/100809.json) |
| [100811](descriptions/urdf/100811.urdf) | Remote Control | Electronic Device Accessory | 0 | 44 | 45 | [JSON](descriptions/finaljson/100811.json) |
| [100814](descriptions/urdf/100814.urdf) | Remote Controller | Electronic Device | 0 | 7 | 8 | [JSON](descriptions/finaljson/100814.json) |
| [100816](descriptions/urdf/100816.urdf) | Remote Control | Electronic Device | 0 | 19 | 20 | [JSON](descriptions/finaljson/100816.json) |
| [100819](descriptions/urdf/100819.urdf) | Remote Control | Electronic Device | 0 | 37 | 38 | [JSON](descriptions/finaljson/100819.json) |
| [100825](descriptions/urdf/100825.urdf) | Suitcase | Luggage | 1 | 0 | 3 | [JSON](descriptions/finaljson/100825.json) |
| [100828](descriptions/urdf/100828.urdf) | Remote | Electronic Control Device | 0 | 4 | 5 | [JSON](descriptions/finaljson/100828.json) |
| [100836](descriptions/urdf/100836.urdf) | Luggage | TravelBag | 2 | 1 | 4 | [JSON](descriptions/finaljson/100836.json) |
| [100837](descriptions/urdf/100837.urdf) | Luggage | Travel Equipment | 2 | 1 | 4 | [JSON](descriptions/finaljson/100837.json) |
| [100839](descriptions/urdf/100839.urdf) | Luggage | Travel Equipment | 4 | 0 | 5 | [JSON](descriptions/finaljson/100839.json) |
| [100840](descriptions/urdf/100840.urdf) | Luggage | TravelAccessory | 2 | 1 | 4 | [JSON](descriptions/finaljson/100840.json) |
| [100842](descriptions/urdf/100842.urdf) | Luggage | TravelAccessory | 0 | 1 | 2 | [JSON](descriptions/finaljson/100842.json) |
| [100845](descriptions/urdf/100845.urdf) | Switch Panel | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100845.json) |
| [100846](descriptions/urdf/100846.urdf) | Wall Switch Panel | Electrical Control Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100846.json) |
| [100847](descriptions/urdf/100847.urdf) | Slide Switch | Electronic Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/100847.json) |
| [100848](descriptions/urdf/100848.urdf) | Electrical Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100848.json) |
| [100849](descriptions/urdf/100849.urdf) | Toggle Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100849.json) |
| [100850](descriptions/urdf/100850.urdf) | Electrical Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100850.json) |
| [100852](descriptions/urdf/100852.urdf) | Shopping Cart | Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/100852.json) |
| [100853](descriptions/urdf/100853.urdf) | Cart | Utility Cart | 2 | 0 | 4 | [JSON](descriptions/finaljson/100853.json) |
| [100854](descriptions/urdf/100854.urdf) | Cart | Vehicle | 5 | 0 | 6 | [JSON](descriptions/finaljson/100854.json) |
| [100856](descriptions/urdf/100856.urdf) | Cart | Transport Vehicle | 4 | 0 | 5 | [JSON](descriptions/finaljson/100856.json) |
| [100858](descriptions/urdf/100858.urdf) | Cart | Vehicle | 5 | 0 | 6 | [JSON](descriptions/finaljson/100858.json) |
| [100860](descriptions/urdf/100860.urdf) | Cart | Shopping Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/100860.json) |
| [100861](descriptions/urdf/100861.urdf) | Cart | Handcart/Wheelbarrow | 1 | 0 | 2 | [JSON](descriptions/finaljson/100861.json) |
| [100866](descriptions/urdf/100866.urdf) | Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100866.json) |
| [100870](descriptions/urdf/100870.urdf) | Wall Switch | Electrical Control Device | 0 | 2 | 3 | [JSON](descriptions/finaljson/100870.json) |
| [100871](descriptions/urdf/100871.urdf) | Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100871.json) |
| [100880](descriptions/urdf/100880.urdf) | Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100880.json) |
| [100882](descriptions/urdf/100882.urdf) | Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100882.json) |
| [100883](descriptions/urdf/100883.urdf) | Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100883.json) |
| [100885](descriptions/urdf/100885.urdf) | Switch Panel | Electrical Control Device | 4 | 0 | 5 | [JSON](descriptions/finaljson/100885.json) |
| [100888](descriptions/urdf/100888.urdf) | Wall Switch with Socket | Electrical Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100888.json) |
| [100889](descriptions/urdf/100889.urdf) | Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100889.json) |
| [100900](descriptions/urdf/100900.urdf) | Electrical Wall Switch | Electrical Component | 2 | 0 | 3 | [JSON](descriptions/finaljson/100900.json) |
| [100901](descriptions/urdf/100901.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100901.json) |
| [100902](descriptions/urdf/100902.urdf) | Wall Switch with Power Sockets | Electrical Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100902.json) |
| [100904](descriptions/urdf/100904.urdf) | Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100904.json) |
| [100905](descriptions/urdf/100905.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100905.json) |
| [100906](descriptions/urdf/100906.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100906.json) |
| [100907](descriptions/urdf/100907.urdf) | Rocker Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100907.json) |
| [100908](descriptions/urdf/100908.urdf) | Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100908.json) |
| [100910](descriptions/urdf/100910.urdf) | Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100910.json) |
| [100911](descriptions/urdf/100911.urdf) | Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100911.json) |
| [100914](descriptions/urdf/100914.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100914.json) |
| [100915](descriptions/urdf/100915.urdf) | Wall Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100915.json) |
| [100919](descriptions/urdf/100919.urdf) | Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100919.json) |
| [100920](descriptions/urdf/100920.urdf) | Electrical Switch | Electrical Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/100920.json) |
| [100924](descriptions/urdf/100924.urdf) | Wall Switch Socket | Electrical Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100924.json) |
| [100925](descriptions/urdf/100925.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100925.json) |
| [100928](descriptions/urdf/100928.urdf) | Wall Switch | Electrical Control Device | 0 | 2 | 3 | [JSON](descriptions/finaljson/100928.json) |
| [100930](descriptions/urdf/100930.urdf) | Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100930.json) |
| [100933](descriptions/urdf/100933.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100933.json) |
| [100934](descriptions/urdf/100934.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100934.json) |
| [100935](descriptions/urdf/100935.urdf) | Wall Switch | Electrical Control Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100935.json) |
| [100937](descriptions/urdf/100937.urdf) | Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100937.json) |
| [100938](descriptions/urdf/100938.urdf) | Cart | Transport Equipment | 1 | 0 | 2 | [JSON](descriptions/finaljson/100938.json) |
| [100948](descriptions/urdf/100948.urdf) | Wall Switch | Electrical Control Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100948.json) |
| [100952](descriptions/urdf/100952.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100952.json) |
| [100953](descriptions/urdf/100953.urdf) | Wall Switch Panel | Electrical Control Device | 0 | 4 | 5 | [JSON](descriptions/finaljson/100953.json) |
| [100954](descriptions/urdf/100954.urdf) | Wall Switch | Electrical Control Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/100954.json) |
| [100955](descriptions/urdf/100955.urdf) | Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100955.json) |
| [100957](descriptions/urdf/100957.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100957.json) |
| [100959](descriptions/urdf/100959.urdf) | Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100959.json) |
| [100963](descriptions/urdf/100963.urdf) | Electrical Wall Switch Panel | Electrical Control Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100963.json) |
| [100965](descriptions/urdf/100965.urdf) | Toggle Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100965.json) |
| [100966](descriptions/urdf/100966.urdf) | Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100966.json) |
| [100968](descriptions/urdf/100968.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100968.json) |
| [100970](descriptions/urdf/100970.urdf) | Switch | Electrical Component | 0 | 1 | 2 | [JSON](descriptions/finaljson/100970.json) |
| [100971](descriptions/urdf/100971.urdf) | Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100971.json) |
| [100974](descriptions/urdf/100974.urdf) | Triple Light Switch | Electrical Control Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100974.json) |
| [100976](descriptions/urdf/100976.urdf) | Electrical Wall Switch | Electrical Control Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/100976.json) |
| [100978](descriptions/urdf/100978.urdf) | Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/100978.json) |
| [100979](descriptions/urdf/100979.urdf) | Wall Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100979.json) |
| [100980](descriptions/urdf/100980.urdf) | Triple Light Switch | Electrical Control Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/100980.json) |
| [100981](descriptions/urdf/100981.urdf) | Electrical Wall Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/100981.json) |
| [100982](descriptions/urdf/100982.urdf) | Window | BuildingComponent | 0 | 3 | 4 | [JSON](descriptions/finaljson/100982.json) |
| [100991](descriptions/urdf/100991.urdf) | Remote Control | Electronic Device | 0 | 53 | 54 | [JSON](descriptions/finaljson/100991.json) |
| [100993](descriptions/urdf/100993.urdf) | Remote Control | Electronic Device | 0 | 25 | 26 | [JSON](descriptions/finaljson/100993.json) |
| [100997](descriptions/urdf/100997.urdf) | Remote Control | Electronic Device | 4 | 38 | 43 | [JSON](descriptions/finaljson/100997.json) |
| [100999](descriptions/urdf/100999.urdf) | Remote Control | Electronic Device | 0 | 28 | 29 | [JSON](descriptions/finaljson/100999.json) |
| [101002](descriptions/urdf/101002.urdf) | Remote Control | Electronic Device | 0 | 8 | 9 | [JSON](descriptions/finaljson/101002.json) |
| [101004](descriptions/urdf/101004.urdf) | Remote | Electronic Control Device | 0 | 2 | 3 | [JSON](descriptions/finaljson/101004.json) |
| [101007](descriptions/urdf/101007.urdf) | Remote Control | Electronic Device | 0 | 27 | 28 | [JSON](descriptions/finaljson/101007.json) |
| [101010](descriptions/urdf/101010.urdf) | Remote Control | Electronic Device | 0 | 58 | 59 | [JSON](descriptions/finaljson/101010.json) |
| [101011](descriptions/urdf/101011.urdf) | Remote | Electronic Control Device | 0 | 5 | 6 | [JSON](descriptions/finaljson/101011.json) |
| [101014](descriptions/urdf/101014.urdf) | Remote Control | Electronic Device | 0 | 27 | 28 | [JSON](descriptions/finaljson/101014.json) |
| [101015](descriptions/urdf/101015.urdf) | Remote Control | Electronic Device | 0 | 59 | 60 | [JSON](descriptions/finaljson/101015.json) |
| [101016](descriptions/urdf/101016.urdf) | Remote Control | Electronic Device Accessory | 2 | 45 | 48 | [JSON](descriptions/finaljson/101016.json) |
| [101023](descriptions/urdf/101023.urdf) | Remote Control | Electronic Device | 0 | 16 | 17 | [JSON](descriptions/finaljson/101023.json) |
| [101028](descriptions/urdf/101028.urdf) | Remote Control | Electronic Device | 0 | 37 | 38 | [JSON](descriptions/finaljson/101028.json) |
| [101034](descriptions/urdf/101034.urdf) | Remote | ElectronicControlDevice | 0 | 12 | 13 | [JSON](descriptions/finaljson/101034.json) |
| [101048](descriptions/urdf/101048.urdf) | Luggage | TravelAccessory | 8 | 1 | 10 | [JSON](descriptions/finaljson/101048.json) |
| [101049](descriptions/urdf/101049.urdf) | Luggage | TravelAccessory | 8 | 1 | 10 | [JSON](descriptions/finaljson/101049.json) |
| [101050](descriptions/urdf/101050.urdf) | Luggage | TravelAccessory | 2 | 1 | 4 | [JSON](descriptions/finaljson/101050.json) |
| [101051](descriptions/urdf/101051.urdf) | Luggage | Travel Equipment | 4 | 1 | 6 | [JSON](descriptions/finaljson/101051.json) |
| [101052](descriptions/urdf/101052.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/101052.json) |
| [101053](descriptions/urdf/101053.urdf) | Cart | Transport Equipment | 1 | 0 | 2 | [JSON](descriptions/finaljson/101053.json) |
| [101054](descriptions/urdf/101054.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/101054.json) |
| [101055](descriptions/urdf/101055.urdf) | Cart | Transport/Utility Vehicle | 1 | 0 | 2 | [JSON](descriptions/finaljson/101055.json) |
| [101057](descriptions/urdf/101057.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/101057.json) |
| [101059](descriptions/urdf/101059.urdf) | Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/101059.json) |
| [101060](descriptions/urdf/101060.urdf) | Cart | Transport Equipment | 2 | 0 | 3 | [JSON](descriptions/finaljson/101060.json) |
| [101062](descriptions/urdf/101062.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/101062.json) |
| [101064](descriptions/urdf/101064.urdf) | Cart | Agricultural Equipment | 4 | 0 | 5 | [JSON](descriptions/finaljson/101064.json) |
| [101065](descriptions/urdf/101065.urdf) | Cart | Transport Vehicle | 4 | 0 | 6 | [JSON](descriptions/finaljson/101065.json) |
| [101066](descriptions/urdf/101066.urdf) | Shopping Cart | Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/101066.json) |
| [101068](descriptions/urdf/101068.urdf) | Swiss Army Knife | Multi-tool Knife | 7 | 1 | 9 | [JSON](descriptions/finaljson/101068.json) |
| [101072](descriptions/urdf/101072.urdf) | Cart | Transport Equipment | 1 | 0 | 2 | [JSON](descriptions/finaljson/101072.json) |
| [101073](descriptions/urdf/101073.urdf) | Cart | Transport Equipment | 2 | 0 | 3 | [JSON](descriptions/finaljson/101073.json) |
| [101075](descriptions/urdf/101075.urdf) | Cart | Transport Vehicle | 2 | 0 | 3 | [JSON](descriptions/finaljson/101075.json) |
| [101077](descriptions/urdf/101077.urdf) | Cart | Vehicle | 3 | 0 | 4 | [JSON](descriptions/finaljson/101077.json) |
| [101079](descriptions/urdf/101079.urdf) | Folding Knife | Cutting Tool | 3 | 0 | 4 | [JSON](descriptions/finaljson/101079.json) |
| [101080](descriptions/urdf/101080.urdf) | Folding Knife | Multi-tool Knife | 7 | 0 | 8 | [JSON](descriptions/finaljson/101080.json) |
| [101081](descriptions/urdf/101081.urdf) | Shopping Cart | Utility Cart | 4 | 0 | 6 | [JSON](descriptions/finaljson/101081.json) |
| [101083](descriptions/urdf/101083.urdf) | Cart | MaterialHandlingEquipment | 4 | 0 | 9 | [JSON](descriptions/finaljson/101083.json) |
| [101085](descriptions/urdf/101085.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/101085.json) |
| [101086](descriptions/urdf/101086.urdf) | Shopping Cart | Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/101086.json) |
| [101090](descriptions/urdf/101090.urdf) | Cart | Utility Transport Equipment | 4 | 0 | 5 | [JSON](descriptions/finaljson/101090.json) |
| [101091](descriptions/urdf/101091.urdf) | Cart | Wheelbarrow | 1 | 0 | 2 | [JSON](descriptions/finaljson/101091.json) |
| [101092](descriptions/urdf/101092.urdf) | Cart | Transport/Utility Vehicle | 1 | 0 | 2 | [JSON](descriptions/finaljson/101092.json) |
| [101093](descriptions/urdf/101093.urdf) | Cart | Wheelbarrow | 1 | 0 | 2 | [JSON](descriptions/finaljson/101093.json) |
| [101095](descriptions/urdf/101095.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/101095.json) |
| [101097](descriptions/urdf/101097.urdf) | Cart | Transport Equipment | 4 | 0 | 5 | [JSON](descriptions/finaljson/101097.json) |
| [101099](descriptions/urdf/101099.urdf) | Cart | TransportVehicle | 2 | 0 | 3 | [JSON](descriptions/finaljson/101099.json) |
| [101102](descriptions/urdf/101102.urdf) | Cart | Transport Equipment | 1 | 0 | 2 | [JSON](descriptions/finaljson/101102.json) |
| [101104](descriptions/urdf/101104.urdf) | Remote Control | Electronic Device | 0 | 34 | 35 | [JSON](descriptions/finaljson/101104.json) |
| [101106](descriptions/urdf/101106.urdf) | Swiss Army Knife | Multi-tool Knife | 8 | 0 | 9 | [JSON](descriptions/finaljson/101106.json) |
| [101107](descriptions/urdf/101107.urdf) | Folding Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/101107.json) |
| [101108](descriptions/urdf/101108.urdf) | Folding Knife | Cutting Tool | 3 | 0 | 4 | [JSON](descriptions/finaljson/101108.json) |
| [101112](descriptions/urdf/101112.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/101112.json) |
| [101114](descriptions/urdf/101114.urdf) | Folding Multi-tool Knife | Hand Tool | 7 | 0 | 8 | [JSON](descriptions/finaljson/101114.json) |
| [101115](descriptions/urdf/101115.urdf) | Folding Knife | Hand Tool | 5 | 0 | 6 | [JSON](descriptions/finaljson/101115.json) |
| [101117](descriptions/urdf/101117.urdf) | Remote Control | Electronic Device | 0 | 4 | 5 | [JSON](descriptions/finaljson/101117.json) |
| [101118](descriptions/urdf/101118.urdf) | Remote | ElectronicControlDevice | 1 | 30 | 32 | [JSON](descriptions/finaljson/101118.json) |
| [101121](descriptions/urdf/101121.urdf) | Remote Control | Electronic Device | 0 | 47 | 48 | [JSON](descriptions/finaljson/101121.json) |
| [101131](descriptions/urdf/101131.urdf) | Remote | Electronic Control Device | 0 | 5 | 6 | [JSON](descriptions/finaljson/101131.json) |
| [101133](descriptions/urdf/101133.urdf) | Remote | ElectronicController | 0 | 8 | 9 | [JSON](descriptions/finaljson/101133.json) |
| [101139](descriptions/urdf/101139.urdf) | Remote Control | Electronic Device | 0 | 33 | 34 | [JSON](descriptions/finaljson/101139.json) |
| [101142](descriptions/urdf/101142.urdf) | Remote Control | Electronic Device | 0 | 26 | 27 | [JSON](descriptions/finaljson/101142.json) |
| [101176](descriptions/urdf/101176.urdf) | Cart | Transport Equipment | 2 | 0 | 3 | [JSON](descriptions/finaljson/101176.json) |
| [101178](descriptions/urdf/101178.urdf) | Cart | Transport Equipment | 2 | 0 | 3 | [JSON](descriptions/finaljson/101178.json) |
| [101182](descriptions/urdf/101182.urdf) | Cart | Wheelbarrow | 1 | 0 | 2 | [JSON](descriptions/finaljson/101182.json) |
| [101183](descriptions/urdf/101183.urdf) | Cart | Transport Equipment | 2 | 0 | 3 | [JSON](descriptions/finaljson/101183.json) |
| [101217](descriptions/urdf/101217.urdf) | Knife | CuttingTool | 1 | 0 | 2 | [JSON](descriptions/finaljson/101217.json) |
| [101220](descriptions/urdf/101220.urdf) | Ventilation Fan | Electrical Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/101220.json) |
| [101236](descriptions/urdf/101236.urdf) | Swiss Army Knife | Multi-tool Knife | 6 | 1 | 8 | [JSON](descriptions/finaljson/101236.json) |
| [101245](descriptions/urdf/101245.urdf) | Swiss Army Knife | Multi-tool Knife | 10 | 0 | 11 | [JSON](descriptions/finaljson/101245.json) |
| [101253](descriptions/urdf/101253.urdf) | Swiss Army Knife | Multi-tool Knife | 8 | 0 | 9 | [JSON](descriptions/finaljson/101253.json) |
| [101260](descriptions/urdf/101260.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/101260.json) |
| [101284](descriptions/urdf/101284.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101284.json) |
| [101285](descriptions/urdf/101285.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101285.json) |
| [101287](descriptions/urdf/101287.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101287.json) |
| [101288](descriptions/urdf/101288.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101288.json) |
| [101291](descriptions/urdf/101291.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101291.json) |
| [101293](descriptions/urdf/101293.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101293.json) |
| [101297](descriptions/urdf/101297.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101297.json) |
| [101300](descriptions/urdf/101300.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101300.json) |
| [101303](descriptions/urdf/101303.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101303.json) |
| [101305](descriptions/urdf/101305.urdf) | Kettle | Kitchenware | 0 | 1 | 3 | [JSON](descriptions/finaljson/101305.json) |
| [101311](descriptions/urdf/101311.urdf) | Kettle | Kitchenware | 1 | 1 | 3 | [JSON](descriptions/finaljson/101311.json) |
| [101313](descriptions/urdf/101313.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/101313.json) |
| [101315](descriptions/urdf/101315.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/101315.json) |
| [101319](descriptions/urdf/101319.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/101319.json) |
| [101320](descriptions/urdf/101320.urdf) | Toilet | SanitaryWare | 1 | 0 | 2 | [JSON](descriptions/finaljson/101320.json) |
| [101323](descriptions/urdf/101323.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/101323.json) |
| [101326](descriptions/urdf/101326.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101326.json) |
| [101328](descriptions/urdf/101328.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101328.json) |
| [101332](descriptions/urdf/101332.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101332.json) |
| [101335](descriptions/urdf/101335.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101335.json) |
| [101352](descriptions/urdf/101352.urdf) | Camera | ElectronicDevice | 1 | 17 | 19 | [JSON](descriptions/finaljson/101352.json) |
| [101362](descriptions/urdf/101362.urdf) | Camera | ElectronicDevice | 2 | 3 | 6 | [JSON](descriptions/finaljson/101362.json) |
| [101363](descriptions/urdf/101363.urdf) | Safe | SecurityStorageDevice | 2 | 0 | 3 | [JSON](descriptions/finaljson/101363.json) |
| [101365](descriptions/urdf/101365.urdf) | Fan | Cooling Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101365.json) |
| [101366](descriptions/urdf/101366.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101366.json) |
| [101369](descriptions/urdf/101369.urdf) | Ventilation Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101369.json) |
| [101371](descriptions/urdf/101371.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101371.json) |
| [101372](descriptions/urdf/101372.urdf) | Fan | Cooling Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101372.json) |
| [101373](descriptions/urdf/101373.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101373.json) |
| [101374](descriptions/urdf/101374.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101374.json) |
| [101375](descriptions/urdf/101375.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101375.json) |
| [101377](descriptions/urdf/101377.urdf) | Trashcan | Household Utility Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/101377.json) |
| [101378](descriptions/urdf/101378.urdf) | Trashcan | Household Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/101378.json) |
| [101380](descriptions/urdf/101380.urdf) | Trashcan | Household Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/101380.json) |
| [101382](descriptions/urdf/101382.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101382.json) |
| [101383](descriptions/urdf/101383.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101383.json) |
| [101384](descriptions/urdf/101384.urdf) | Trashcan | Waste Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/101384.json) |
| [101386](descriptions/urdf/101386.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101386.json) |
| [101387](descriptions/urdf/101387.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101387.json) |
| [101388](descriptions/urdf/101388.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101388.json) |
| [101389](descriptions/urdf/101389.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101389.json) |
| [101396](descriptions/urdf/101396.urdf) | Cooling Fan Assembly | Computer Component (CPU Cooler) | 1 | 0 | 2 | [JSON](descriptions/finaljson/101396.json) |
| [101397](descriptions/urdf/101397.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101397.json) |
| [101399](descriptions/urdf/101399.urdf) | Computer Mouse | Input Device | 1 | 2 | 4 | [JSON](descriptions/finaljson/101399.json) |
| [101401](descriptions/urdf/101401.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101401.json) |
| [101402](descriptions/urdf/101402.urdf) | Marine Propeller System | Mechanical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/101402.json) |
| [101403](descriptions/urdf/101403.urdf) | Computer Mouse | Input Device | 1 | 2 | 4 | [JSON](descriptions/finaljson/101403.json) |
| [101405](descriptions/urdf/101405.urdf) | Cooling Fan | Electronic Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/101405.json) |
| [101407](descriptions/urdf/101407.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101407.json) |
| [101408](descriptions/urdf/101408.urdf) | Computer Mouse | Input Device | 1 | 2 | 4 | [JSON](descriptions/finaljson/101408.json) |
| [101413](descriptions/urdf/101413.urdf) | Fan | Electrical Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/101413.json) |
| [101416](descriptions/urdf/101416.urdf) | Computer Mouse | Input Device | 1 | 2 | 4 | [JSON](descriptions/finaljson/101416.json) |
| [101417](descriptions/urdf/101417.urdf) | Dispenser | Spray Bottle | 2 | 0 | 4 | [JSON](descriptions/finaljson/101417.json) |
| [101419](descriptions/urdf/101419.urdf) | Axial Flow Fan | Ventilation Equipment | 1 | 0 | 2 | [JSON](descriptions/finaljson/101419.json) |
| [101420](descriptions/urdf/101420.urdf) | Electric Fan | Home Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101420.json) |
| [101421](descriptions/urdf/101421.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101421.json) |
| [101422](descriptions/urdf/101422.urdf) | Electric Fan | Home Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/101422.json) |
| [101423](descriptions/urdf/101423.urdf) | Electric Fan | Home Appliance | 1 | 1 | 5 | [JSON](descriptions/finaljson/101423.json) |
| [101425](descriptions/urdf/101425.urdf) | Cooling Fan Assembly | Computer Cooling Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101425.json) |
| [101428](descriptions/urdf/101428.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101428.json) |
| [101429](descriptions/urdf/101429.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101429.json) |
| [101432](descriptions/urdf/101432.urdf) | Axial Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101432.json) |
| [101433](descriptions/urdf/101433.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101433.json) |
| [101435](descriptions/urdf/101435.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101435.json) |
| [101436](descriptions/urdf/101436.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101436.json) |
| [101437](descriptions/urdf/101437.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101437.json) |
| [101439](descriptions/urdf/101439.urdf) | Cooling Fan Assembly | Electronic Cooling Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101439.json) |
| [101440](descriptions/urdf/101440.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101440.json) |
| [101441](descriptions/urdf/101441.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101441.json) |
| [101442](descriptions/urdf/101442.urdf) | Dispenser | Liquid Container / Pump Dispenser | 2 | 0 | 4 | [JSON](descriptions/finaljson/101442.json) |
| [101444](descriptions/urdf/101444.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101444.json) |
| [101445](descriptions/urdf/101445.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101445.json) |
| [101446](descriptions/urdf/101446.urdf) | Ventilation Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101446.json) |
| [101448](descriptions/urdf/101448.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101448.json) |
| [101449](descriptions/urdf/101449.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101449.json) |
| [101450](descriptions/urdf/101450.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101450.json) |
| [101456](descriptions/urdf/101456.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101456.json) |
| [101457](descriptions/urdf/101457.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101457.json) |
| [101460](descriptions/urdf/101460.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101460.json) |
| [101461](descriptions/urdf/101461.urdf) | Axial Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101461.json) |
| [101465](descriptions/urdf/101465.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101465.json) |
| [101467](descriptions/urdf/101467.urdf) | Ventilation Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101467.json) |
| [101468](descriptions/urdf/101468.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101468.json) |
| [101469](descriptions/urdf/101469.urdf) | Fan | Electrical Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/101469.json) |
| [101470](descriptions/urdf/101470.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101470.json) |
| [101472](descriptions/urdf/101472.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101472.json) |
| [101474](descriptions/urdf/101474.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/101474.json) |
| [101475](descriptions/urdf/101475.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101475.json) |
| [101476](descriptions/urdf/101476.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101476.json) |
| [101481](descriptions/urdf/101481.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101481.json) |
| [101483](descriptions/urdf/101483.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101483.json) |
| [101489](descriptions/urdf/101489.urdf) | Dispenser | Liquid Dispenser | 0 | 1 | 2 | [JSON](descriptions/finaljson/101489.json) |
| [101490](descriptions/urdf/101490.urdf) | Dispenser | Liquid Dispenser / Pump Bottle | 1 | 0 | 2 | [JSON](descriptions/finaljson/101490.json) |
| [101493](descriptions/urdf/101493.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101493.json) |
| [101494](descriptions/urdf/101494.urdf) | Cooling Fan Unit | Electrical Appliance Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/101494.json) |
| [101496](descriptions/urdf/101496.urdf) | Electric Fan | Home Appliance | 1 | 1 | 5 | [JSON](descriptions/finaljson/101496.json) |
| [101499](descriptions/urdf/101499.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/101499.json) |
| [101501](descriptions/urdf/101501.urdf) | Liquid Soap Dispenser | Dispenser | 2 | 0 | 3 | [JSON](descriptions/finaljson/101501.json) |
| [101504](descriptions/urdf/101504.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101504.json) |
| [101505](descriptions/urdf/101505.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101505.json) |
| [101507](descriptions/urdf/101507.urdf) | Liquid Soap Dispenser | Bathroom Accessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101507.json) |
| [101510](descriptions/urdf/101510.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101510.json) |
| [101511](descriptions/urdf/101511.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101511.json) |
| [101517](descriptions/urdf/101517.urdf) | Liquid Soap Dispenser | Bathroom Accessory | 1 | 0 | 3 | [JSON](descriptions/finaljson/101517.json) |
| [101523](descriptions/urdf/101523.urdf) | Axial Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101523.json) |
| [101524](descriptions/urdf/101524.urdf) | Axial Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101524.json) |
| [101533](descriptions/urdf/101533.urdf) | Dispenser | Liquid Dispenser (e.g., Soap or Lotion Dispenser) | 2 | 0 | 3 | [JSON](descriptions/finaljson/101533.json) |
| [101539](descriptions/urdf/101539.urdf) | Dispenser | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/101539.json) |
| [101541](descriptions/urdf/101541.urdf) | Dispenser | Liquid Container / Pump Dispenser | 2 | 0 | 3 | [JSON](descriptions/finaljson/101541.json) |
| [101546](descriptions/urdf/101546.urdf) | Dispenser | Liquid Dispenser | 2 | 0 | 3 | [JSON](descriptions/finaljson/101546.json) |
| [101548](descriptions/urdf/101548.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/101548.json) |
| [101557](descriptions/urdf/101557.urdf) | Dispenser | Liquid Dispenser / Soap Pump | 2 | 0 | 3 | [JSON](descriptions/finaljson/101557.json) |
| [101560](descriptions/urdf/101560.urdf) | Liquid Dispenser | Hygiene Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/101560.json) |
| [101561](descriptions/urdf/101561.urdf) | Liquid Soap Dispenser | Hygiene Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/101561.json) |
| [101563](descriptions/urdf/101563.urdf) | Liquid Soap Dispenser | Hygiene Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/101563.json) |
| [101564](descriptions/urdf/101564.urdf) | Safe | SecurityStorageDevice | 1 | 12 | 15 | [JSON](descriptions/finaljson/101564.json) |
| [101566](descriptions/urdf/101566.urdf) | Dispenser | Aerosol Can | 1 | 0 | 2 | [JSON](descriptions/finaljson/101566.json) |
| [101579](descriptions/urdf/101579.urdf) | Safe | SecurityStorageDevice | 3 | 0 | 5 | [JSON](descriptions/finaljson/101579.json) |
| [101583](descriptions/urdf/101583.urdf) | Safe | SecurityStorageDevice | 2 | 12 | 16 | [JSON](descriptions/finaljson/101583.json) |
| [101584](descriptions/urdf/101584.urdf) | Safe | Security Storage Device | 3 | 0 | 4 | [JSON](descriptions/finaljson/101584.json) |
| [101591](descriptions/urdf/101591.urdf) | Safe | SecurityStorageDevice | 2 | 5 | 8 | [JSON](descriptions/finaljson/101591.json) |
| [101593](descriptions/urdf/101593.urdf) | Safe | SecurityStorageDevice | 3 | 0 | 4 | [JSON](descriptions/finaljson/101593.json) |
| [101594](descriptions/urdf/101594.urdf) | Safe | SecurityStorageDevice | 2 | 0 | 3 | [JSON](descriptions/finaljson/101594.json) |
| [101599](descriptions/urdf/101599.urdf) | Safe | SecurityStorageDevice | 2 | 12 | 16 | [JSON](descriptions/finaljson/101599.json) |
| [101603](descriptions/urdf/101603.urdf) | Safe | SecurityStorageDevice | 3 | 0 | 4 | [JSON](descriptions/finaljson/101603.json) |
| [101604](descriptions/urdf/101604.urdf) | Safe | SecurityStorageDevice | 2 | 12 | 15 | [JSON](descriptions/finaljson/101604.json) |
| [101605](descriptions/urdf/101605.urdf) | Safe | SecurityStorage | 2 | 0 | 3 | [JSON](descriptions/finaljson/101605.json) |
| [101611](descriptions/urdf/101611.urdf) | Safe | SecurityStorage | 3 | 0 | 6 | [JSON](descriptions/finaljson/101611.json) |
| [101612](descriptions/urdf/101612.urdf) | Safe | SecurityStorage | 3 | 0 | 4 | [JSON](descriptions/finaljson/101612.json) |
| [101613](descriptions/urdf/101613.urdf) | Safe | SecurityStorageDevice | 2 | 0 | 3 | [JSON](descriptions/finaljson/101613.json) |
| [101619](descriptions/urdf/101619.urdf) | Safe | SecurityStorage | 3 | 0 | 6 | [JSON](descriptions/finaljson/101619.json) |
| [101623](descriptions/urdf/101623.urdf) | Safe | SecurityStorageDevice | 3 | 0 | 4 | [JSON](descriptions/finaljson/101623.json) |
| [101659](descriptions/urdf/101659.urdf) | Knife | Folding Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/101659.json) |
| [101660](descriptions/urdf/101660.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/101660.json) |
| [101662](descriptions/urdf/101662.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/101662.json) |
| [101668](descriptions/urdf/101668.urdf) | Suitcase | Luggage | 2 | 2 | 5 | [JSON](descriptions/finaljson/101668.json) |
| [101673](descriptions/urdf/101673.urdf) | Suitcase | Luggage | 1 | 0 | 2 | [JSON](descriptions/finaljson/101673.json) |
| [101681](descriptions/urdf/101681.urdf) | Suitcase | Luggage | 2 | 0 | 3 | [JSON](descriptions/finaljson/101681.json) |
| [101685](descriptions/urdf/101685.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101685.json) |
| [101698](descriptions/urdf/101698.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101698.json) |
| [101703](descriptions/urdf/101703.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101703.json) |
| [101712](descriptions/urdf/101712.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101712.json) |
| [101713](descriptions/urdf/101713.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101713.json) |
| [101714](descriptions/urdf/101714.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101714.json) |
| [101722](descriptions/urdf/101722.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101722.json) |
| [101727](descriptions/urdf/101727.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101727.json) |
| [101732](descriptions/urdf/101732.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101732.json) |
| [101735](descriptions/urdf/101735.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101735.json) |
| [101736](descriptions/urdf/101736.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101736.json) |
| [101741](descriptions/urdf/101741.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101741.json) |
| [101748](descriptions/urdf/101748.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101748.json) |
| [101770](descriptions/urdf/101770.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101770.json) |
| [101773](descriptions/urdf/101773.urdf) | Oven | Home Appliance | 4 | 5 | 10 | [JSON](descriptions/finaljson/101773.json) |
| [101786](descriptions/urdf/101786.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101786.json) |
| [101787](descriptions/urdf/101787.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101787.json) |
| [101793](descriptions/urdf/101793.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101793.json) |
| [101796](descriptions/urdf/101796.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/101796.json) |
| [101808](descriptions/urdf/101808.urdf) | Oven | Home Appliance | 9 | 0 | 10 | [JSON](descriptions/finaljson/101808.json) |
| [101831](descriptions/urdf/101831.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101831.json) |
| [101833](descriptions/urdf/101833.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101833.json) |
| [101836](descriptions/urdf/101836.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101836.json) |
| [101838](descriptions/urdf/101838.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101838.json) |
| [101839](descriptions/urdf/101839.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101839.json) |
| [101840](descriptions/urdf/101840.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101840.json) |
| [101842](descriptions/urdf/101842.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101842.json) |
| [101843](descriptions/urdf/101843.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101843.json) |
| [101844](descriptions/urdf/101844.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101844.json) |
| [101845](descriptions/urdf/101845.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101845.json) |
| [101848](descriptions/urdf/101848.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101848.json) |
| [101859](descriptions/urdf/101859.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101859.json) |
| [101860](descriptions/urdf/101860.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101860.json) |
| [101861](descriptions/urdf/101861.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101861.json) |
| [101863](descriptions/urdf/101863.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101863.json) |
| [101864](descriptions/urdf/101864.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101864.json) |
| [101866](descriptions/urdf/101866.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101866.json) |
| [101868](descriptions/urdf/101868.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101868.json) |
| [101869](descriptions/urdf/101869.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101869.json) |
| [101870](descriptions/urdf/101870.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101870.json) |
| [101871](descriptions/urdf/101871.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101871.json) |
| [101874](descriptions/urdf/101874.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/101874.json) |
| [101886](descriptions/urdf/101886.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101886.json) |
| [101892](descriptions/urdf/101892.urdf) | Cart | Transport Equipment | 2 | 0 | 3 | [JSON](descriptions/finaljson/101892.json) |
| [101908](descriptions/urdf/101908.urdf) | Oven | Kitchen Appliance | 12 | 0 | 13 | [JSON](descriptions/finaljson/101908.json) |
| [101909](descriptions/urdf/101909.urdf) | Oven | Home Appliance | 5 | 0 | 7 | [JSON](descriptions/finaljson/101909.json) |
| [101917](descriptions/urdf/101917.urdf) | Oven | Kitchen Appliance | 8 | 0 | 9 | [JSON](descriptions/finaljson/101917.json) |
| [101921](descriptions/urdf/101921.urdf) | Oven | Home Appliance | 8 | 1 | 10 | [JSON](descriptions/finaljson/101921.json) |
| [101924](descriptions/urdf/101924.urdf) | Oven | KitchenAppliance | 11 | 0 | 14 | [JSON](descriptions/finaljson/101924.json) |
| [101930](descriptions/urdf/101930.urdf) | Oven | KitchenAppliance | 7 | 0 | 8 | [JSON](descriptions/finaljson/101930.json) |
| [101931](descriptions/urdf/101931.urdf) | Oven | Kitchen Appliance | 6 | 0 | 7 | [JSON](descriptions/finaljson/101931.json) |
| [101940](descriptions/urdf/101940.urdf) | Oven | Kitchen Appliance | 5 | 0 | 7 | [JSON](descriptions/finaljson/101940.json) |
| [101943](descriptions/urdf/101943.urdf) | Oven | KitchenAppliance | 8 | 0 | 9 | [JSON](descriptions/finaljson/101943.json) |
| [101946](descriptions/urdf/101946.urdf) | Oven | Home Appliance | 7 | 0 | 8 | [JSON](descriptions/finaljson/101946.json) |
| [101947](descriptions/urdf/101947.urdf) | Oven | Kitchen Appliance | 8 | 0 | 9 | [JSON](descriptions/finaljson/101947.json) |
| [101948](descriptions/urdf/101948.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101948.json) |
| [101950](descriptions/urdf/101950.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101950.json) |
| [101952](descriptions/urdf/101952.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/101952.json) |
| [101960](descriptions/urdf/101960.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/101960.json) |
| [101971](descriptions/urdf/101971.urdf) | Oven | Home Appliance | 1 | 11 | 13 | [JSON](descriptions/finaljson/101971.json) |
| [101982](descriptions/urdf/101982.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101982.json) |
| [101983](descriptions/urdf/101983.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/101983.json) |
| [101994](descriptions/urdf/101994.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101994.json) |
| [101999](descriptions/urdf/101999.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/101999.json) |
| [102001](descriptions/urdf/102001.urdf) | Oven | KitchenAppliance | 9 | 0 | 10 | [JSON](descriptions/finaljson/102001.json) |
| [102004](descriptions/urdf/102004.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102004.json) |
| [102008](descriptions/urdf/102008.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102008.json) |
| [102009](descriptions/urdf/102009.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/102009.json) |
| [102016](descriptions/urdf/102016.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/102016.json) |
| [102018](descriptions/urdf/102018.urdf) | Oven | Home Appliance | 6 | 0 | 7 | [JSON](descriptions/finaljson/102018.json) |
| [102019](descriptions/urdf/102019.urdf) | Oven | Kitchen Appliance | 5 | 0 | 7 | [JSON](descriptions/finaljson/102019.json) |
| [102021](descriptions/urdf/102021.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/102021.json) |
| [102024](descriptions/urdf/102024.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/102024.json) |
| [102025](descriptions/urdf/102025.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/102025.json) |
| [102033](descriptions/urdf/102033.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102033.json) |
| [102037](descriptions/urdf/102037.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102037.json) |
| [102042](descriptions/urdf/102042.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/102042.json) |
| [102044](descriptions/urdf/102044.urdf) | Oven | Kitchen Appliance | 6 | 0 | 7 | [JSON](descriptions/finaljson/102044.json) |
| [102052](descriptions/urdf/102052.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/102052.json) |
| [102053](descriptions/urdf/102053.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/102053.json) |
| [102055](descriptions/urdf/102055.urdf) | Oven | Kitchen Appliance | 4 | 0 | 5 | [JSON](descriptions/finaljson/102055.json) |
| [102060](descriptions/urdf/102060.urdf) | Oven | KitchenAppliance | 6 | 0 | 7 | [JSON](descriptions/finaljson/102060.json) |
| [102062](descriptions/urdf/102062.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/102062.json) |
| [102063](descriptions/urdf/102063.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102063.json) |
| [102065](descriptions/urdf/102065.urdf) | USB Flash Drive | Electronic Storage Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102065.json) |
| [102068](descriptions/urdf/102068.urdf) | USB Flash Drive | Electronic Storage Device | 0 | 1 | 2 | [JSON](descriptions/finaljson/102068.json) |
| [102070](descriptions/urdf/102070.urdf) | Axial Cooling Fan | Electrical Appliance Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/102070.json) |
| [102073](descriptions/urdf/102073.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102073.json) |
| [102074](descriptions/urdf/102074.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102074.json) |
| [102075](descriptions/urdf/102075.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102075.json) |
| [102080](descriptions/urdf/102080.urdf) | Kitchen Pot | Cookware | 0 | 1 | 2 | [JSON](descriptions/finaljson/102080.json) |
| [102085](descriptions/urdf/102085.urdf) | Kitchen Pot | Cookware | 0 | 1 | 3 | [JSON](descriptions/finaljson/102085.json) |
| [102090](descriptions/urdf/102090.urdf) | Box Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/102090.json) |
| [102092](descriptions/urdf/102092.urdf) | Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102092.json) |
| [102093](descriptions/urdf/102093.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/102093.json) |
| [102095](descriptions/urdf/102095.urdf) | Axial Cooling Fan | Electromechanical Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102095.json) |
| [102099](descriptions/urdf/102099.urdf) | Fan | Cooling Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102099.json) |
| [102100](descriptions/urdf/102100.urdf) | Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/102100.json) |
| [102130](descriptions/urdf/102130.urdf) | Remote Control | Electronic Device | 0 | 19 | 20 | [JSON](descriptions/finaljson/102130.json) |
| [102145](descriptions/urdf/102145.urdf) | Coffeemachine | Kitchen Appliance | 2 | 2 | 5 | [JSON](descriptions/finaljson/102145.json) |
| [102149](descriptions/urdf/102149.urdf) | Coffee Machine | Kitchen Appliance | 1 | 4 | 8 | [JSON](descriptions/finaljson/102149.json) |
| [102153](descriptions/urdf/102153.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102153.json) |
| [102154](descriptions/urdf/102154.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102154.json) |
| [102155](descriptions/urdf/102155.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102155.json) |
| [102156](descriptions/urdf/102156.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102156.json) |
| [102158](descriptions/urdf/102158.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102158.json) |
| [102160](descriptions/urdf/102160.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102160.json) |
| [102163](descriptions/urdf/102163.urdf) | Trashcan | Waste Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102163.json) |
| [102165](descriptions/urdf/102165.urdf) | Trashcan | Household Utility Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/102165.json) |
| [102171](descriptions/urdf/102171.urdf) | Trashcan | Household Waste Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102171.json) |
| [102173](descriptions/urdf/102173.urdf) | Trashcan | Waste Container | 1 | 0 | 3 | [JSON](descriptions/finaljson/102173.json) |
| [102177](descriptions/urdf/102177.urdf) | Trashcan | Household Utility Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/102177.json) |
| [102181](descriptions/urdf/102181.urdf) | Trashcan | Household Utility Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/102181.json) |
| [102182](descriptions/urdf/102182.urdf) | Trashcan | Household Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102182.json) |
| [102186](descriptions/urdf/102186.urdf) | Trashcan | Household Utility Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/102186.json) |
| [102187](descriptions/urdf/102187.urdf) | Trashcan | Waste Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102187.json) |
| [102189](descriptions/urdf/102189.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102189.json) |
| [102192](descriptions/urdf/102192.urdf) | Trashcan | Household Utility Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/102192.json) |
| [102193](descriptions/urdf/102193.urdf) | Trashcan | Waste Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102193.json) |
| [102194](descriptions/urdf/102194.urdf) | Trashcan | Household Waste Container | 1 | 1 | 5 | [JSON](descriptions/finaljson/102194.json) |
| [102200](descriptions/urdf/102200.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102200.json) |
| [102201](descriptions/urdf/102201.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102201.json) |
| [102202](descriptions/urdf/102202.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102202.json) |
| [102209](descriptions/urdf/102209.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102209.json) |
| [102210](descriptions/urdf/102210.urdf) | Trashcan | Waste Container | 3 | 0 | 5 | [JSON](descriptions/finaljson/102210.json) |
| [102218](descriptions/urdf/102218.urdf) | Trashcan | Waste Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/102218.json) |
| [102219](descriptions/urdf/102219.urdf) | Trashcan | Waste Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/102219.json) |
| [102221](descriptions/urdf/102221.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102221.json) |
| [102227](descriptions/urdf/102227.urdf) | Trashcan | Household Utility Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/102227.json) |
| [102229](descriptions/urdf/102229.urdf) | Trashcan | Household Utility Object | 3 | 0 | 4 | [JSON](descriptions/finaljson/102229.json) |
| [102234](descriptions/urdf/102234.urdf) | Trashcan | Household Waste Container | 1 | 1 | 3 | [JSON](descriptions/finaljson/102234.json) |
| [102242](descriptions/urdf/102242.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102242.json) |
| [102243](descriptions/urdf/102243.urdf) | Pliers | Hand Tool | 1 | 0 | 4 | [JSON](descriptions/finaljson/102243.json) |
| [102244](descriptions/urdf/102244.urdf) | Trashcan | Household Waste Container | 1 | 1 | 3 | [JSON](descriptions/finaljson/102244.json) |
| [102251](descriptions/urdf/102251.urdf) | Pliers | Hand Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/102251.json) |
| [102252](descriptions/urdf/102252.urdf) | Trashcan | Waste Container | 1 | 1 | 3 | [JSON](descriptions/finaljson/102252.json) |
| [102253](descriptions/urdf/102253.urdf) | Pliers | HandTool | 1 | 0 | 4 | [JSON](descriptions/finaljson/102253.json) |
| [102254](descriptions/urdf/102254.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102254.json) |
| [102255](descriptions/urdf/102255.urdf) | Folding Chair | Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/102255.json) |
| [102256](descriptions/urdf/102256.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102256.json) |
| [102257](descriptions/urdf/102257.urdf) | Trashcan | Household Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102257.json) |
| [102258](descriptions/urdf/102258.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102258.json) |
| [102259](descriptions/urdf/102259.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/102259.json) |
| [102260](descriptions/urdf/102260.urdf) | Pliers | HandTool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102260.json) |
| [102263](descriptions/urdf/102263.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/102263.json) |
| [102269](descriptions/urdf/102269.urdf) | Folding Chair | Furniture | 2 | 0 | 3 | [JSON](descriptions/finaljson/102269.json) |
| [102272](descriptions/urdf/102272.urdf) | Computer Mouse | Input Device | 1 | 2 | 4 | [JSON](descriptions/finaljson/102272.json) |
| [102273](descriptions/urdf/102273.urdf) | Mouse | ComputerPeripheral | 1 | 6 | 8 | [JSON](descriptions/finaljson/102273.json) |
| [102276](descriptions/urdf/102276.urdf) | Computer Mouse | Input Device | 1 | 6 | 8 | [JSON](descriptions/finaljson/102276.json) |
| [102278](descriptions/urdf/102278.urdf) | Safe | SecurityStorageDevice | 2 | 13 | 19 | [JSON](descriptions/finaljson/102278.json) |
| [102285](descriptions/urdf/102285.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102285.json) |
| [102288](descriptions/urdf/102288.urdf) | Pliers | HandTool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102288.json) |
| [102290](descriptions/urdf/102290.urdf) | Mouse | ComputerPeripheral | 2 | 0 | 3 | [JSON](descriptions/finaljson/102290.json) |
| [102292](descriptions/urdf/102292.urdf) | Pliers | Hand Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102292.json) |
| [102301](descriptions/urdf/102301.urdf) | Safe | SecurityStorageDevice | 2 | 0 | 3 | [JSON](descriptions/finaljson/102301.json) |
| [102309](descriptions/urdf/102309.urdf) | Safe | SecurityStorage | 3 | 0 | 5 | [JSON](descriptions/finaljson/102309.json) |
| [102311](descriptions/urdf/102311.urdf) | Safe | SecurityStorageDevice | 3 | 0 | 4 | [JSON](descriptions/finaljson/102311.json) |
| [102314](descriptions/urdf/102314.urdf) | Folding Chair | Furniture | 1 | 0 | 2 | [JSON](descriptions/finaljson/102314.json) |
| [102316](descriptions/urdf/102316.urdf) | Safe | SecurityStorageDevice | 3 | 0 | 4 | [JSON](descriptions/finaljson/102316.json) |
| [102318](descriptions/urdf/102318.urdf) | Safe | SecurityStorage | 2 | 12 | 15 | [JSON](descriptions/finaljson/102318.json) |
| [102333](descriptions/urdf/102333.urdf) | Folding Chair | Furniture | 1 | 0 | 3 | [JSON](descriptions/finaljson/102333.json) |
| [102347](descriptions/urdf/102347.urdf) | Cart | Material Handling Equipment | 4 | 0 | 5 | [JSON](descriptions/finaljson/102347.json) |
| [102352](descriptions/urdf/102352.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102352.json) |
| [102358](descriptions/urdf/102358.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102358.json) |
| [102359](descriptions/urdf/102359.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102359.json) |
| [102363](descriptions/urdf/102363.urdf) | Bucket | Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/102363.json) |
| [102365](descriptions/urdf/102365.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102365.json) |
| [102367](descriptions/urdf/102367.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102367.json) |
| [102369](descriptions/urdf/102369.urdf) | Bucket | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102369.json) |
| [102373](descriptions/urdf/102373.urdf) | Box | Container | 4 | 0 | 5 | [JSON](descriptions/finaljson/102373.json) |
| [102377](descriptions/urdf/102377.urdf) | Toolbox | StorageBox | 1 | 1 | 3 | [JSON](descriptions/finaljson/102377.json) |
| [102379](descriptions/urdf/102379.urdf) | Wooden Storage Box | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102379.json) |
| [102380](descriptions/urdf/102380.urdf) | Safe | SecurityStorage | 2 | 0 | 4 | [JSON](descriptions/finaljson/102380.json) |
| [102381](descriptions/urdf/102381.urdf) | Safe | SecurityStorage | 3 | 0 | 4 | [JSON](descriptions/finaljson/102381.json) |
| [102384](descriptions/urdf/102384.urdf) | Safe | SecurityStorageDevice | 3 | 0 | 4 | [JSON](descriptions/finaljson/102384.json) |
| [102387](descriptions/urdf/102387.urdf) | Safe | SecurityStorageDevice | 2 | 0 | 3 | [JSON](descriptions/finaljson/102387.json) |
| [102389](descriptions/urdf/102389.urdf) | Safe | SecurityStorageDevice | 2 | 14 | 18 | [JSON](descriptions/finaljson/102389.json) |
| [102394](descriptions/urdf/102394.urdf) | Digital Camera | Electronic Device | 0 | 8 | 9 | [JSON](descriptions/finaljson/102394.json) |
| [102398](descriptions/urdf/102398.urdf) | Camera | ElectronicDevice | 2 | 1 | 4 | [JSON](descriptions/finaljson/102398.json) |
| [102400](descriptions/urdf/102400.urdf) | Knife | Folding Tool | 1 | 0 | 3 | [JSON](descriptions/finaljson/102400.json) |
| [102401](descriptions/urdf/102401.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102401.json) |
| [102402](descriptions/urdf/102402.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/102402.json) |
| [102403](descriptions/urdf/102403.urdf) | Camera | ElectronicDevice | 0 | 6 | 7 | [JSON](descriptions/finaljson/102403.json) |
| [102407](descriptions/urdf/102407.urdf) | Camera | Optical Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/102407.json) |
| [102408](descriptions/urdf/102408.urdf) | Camera | ElectronicDevice | 1 | 5 | 7 | [JSON](descriptions/finaljson/102408.json) |
| [102411](descriptions/urdf/102411.urdf) | Digital Camera | Electronic Device | 2 | 10 | 13 | [JSON](descriptions/finaljson/102411.json) |
| [102414](descriptions/urdf/102414.urdf) | Camera | ElectronicDevice | 1 | 6 | 8 | [JSON](descriptions/finaljson/102414.json) |
| [102417](descriptions/urdf/102417.urdf) | Camera | ElectronicDevice | 3 | 16 | 20 | [JSON](descriptions/finaljson/102417.json) |
| [102418](descriptions/urdf/102418.urdf) | Safe | SecurityStorageDevice | 1 | 9 | 11 | [JSON](descriptions/finaljson/102418.json) |
| [102423](descriptions/urdf/102423.urdf) | Safe | SecurityStorageDevice | 2 | 0 | 4 | [JSON](descriptions/finaljson/102423.json) |
| [102431](descriptions/urdf/102431.urdf) | Camera | ElectronicDevice | 2 | 1 | 5 | [JSON](descriptions/finaljson/102431.json) |
| [102432](descriptions/urdf/102432.urdf) | Camera | ElectronicDevice | 2 | 9 | 12 | [JSON](descriptions/finaljson/102432.json) |
| [102434](descriptions/urdf/102434.urdf) | Camera | ElectronicDevice | 1 | 4 | 6 | [JSON](descriptions/finaljson/102434.json) |
| [102442](descriptions/urdf/102442.urdf) | Camera | ElectronicDevice | 0 | 12 | 13 | [JSON](descriptions/finaljson/102442.json) |
| [102456](descriptions/urdf/102456.urdf) | Storage Box | Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/102456.json) |
| [102472](descriptions/urdf/102472.urdf) | Camera | ElectronicDevice | 2 | 4 | 7 | [JSON](descriptions/finaljson/102472.json) |
| [102505](descriptions/urdf/102505.urdf) | Camera | ElectronicDevice | 3 | 17 | 21 | [JSON](descriptions/finaljson/102505.json) |
| [102506](descriptions/urdf/102506.urdf) | Camera | ElectronicDevice | 1 | 1 | 3 | [JSON](descriptions/finaljson/102506.json) |
| [102520](descriptions/urdf/102520.urdf) | Camera | ElectronicDevice | 2 | 2 | 5 | [JSON](descriptions/finaljson/102520.json) |
| [102523](descriptions/urdf/102523.urdf) | Camera | ElectronicDevice | 3 | 6 | 10 | [JSON](descriptions/finaljson/102523.json) |
| [102527](descriptions/urdf/102527.urdf) | Camera | ElectronicDevice | 1 | 7 | 9 | [JSON](descriptions/finaljson/102527.json) |
| [102528](descriptions/urdf/102528.urdf) | Camera | ElectronicDevice | 5 | 11 | 17 | [JSON](descriptions/finaljson/102528.json) |
| [102532](descriptions/urdf/102532.urdf) | Camera | Optical Device | 1 | 1 | 5 | [JSON](descriptions/finaljson/102532.json) |
| [102536](descriptions/urdf/102536.urdf) | Camera | ElectronicDevice | 2 | 2 | 5 | [JSON](descriptions/finaljson/102536.json) |
| [102539](descriptions/urdf/102539.urdf) | Camera | ElectronicDevice | 1 | 15 | 17 | [JSON](descriptions/finaljson/102539.json) |
| [102542](descriptions/urdf/102542.urdf) | Digital Camera | Electronic Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/102542.json) |
| [102546](descriptions/urdf/102546.urdf) | Cart | Wheelbarrow | 1 | 0 | 2 | [JSON](descriptions/finaljson/102546.json) |
| [102548](descriptions/urdf/102548.urdf) | Cart | Vehicle | 4 | 0 | 6 | [JSON](descriptions/finaljson/102548.json) |
| [102551](descriptions/urdf/102551.urdf) | Cart | Shopping Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/102551.json) |
| [102552](descriptions/urdf/102552.urdf) | Cart | Utility Vehicle / Shopping Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/102552.json) |
| [102555](descriptions/urdf/102555.urdf) | Cart | Wheelbarrow | 1 | 0 | 2 | [JSON](descriptions/finaljson/102555.json) |
| [102556](descriptions/urdf/102556.urdf) | Cart | Utility Vehicle / Handcart | 4 | 0 | 5 | [JSON](descriptions/finaljson/102556.json) |
| [102557](descriptions/urdf/102557.urdf) | Cart | Transport/Utility Vehicle | 4 | 0 | 5 | [JSON](descriptions/finaljson/102557.json) |
| [102561](descriptions/urdf/102561.urdf) | Cart | Utility Vehicle / Transport Cart | 4 | 0 | 5 | [JSON](descriptions/finaljson/102561.json) |
| [102562](descriptions/urdf/102562.urdf) | Cart | Transport Equipment | 3 | 0 | 4 | [JSON](descriptions/finaljson/102562.json) |
| [102567](descriptions/urdf/102567.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102567.json) |
| [102568](descriptions/urdf/102568.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102568.json) |
| [102569](descriptions/urdf/102569.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102569.json) |
| [102570](descriptions/urdf/102570.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102570.json) |
| [102571](descriptions/urdf/102571.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102571.json) |
| [102572](descriptions/urdf/102572.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102572.json) |
| [102573](descriptions/urdf/102573.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102573.json) |
| [102578](descriptions/urdf/102578.urdf) | Eyeglasses | VisionAidDevice | 2 | 0 | 3 | [JSON](descriptions/finaljson/102578.json) |
| [102586](descriptions/urdf/102586.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102586.json) |
| [102587](descriptions/urdf/102587.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102587.json) |
| [102588](descriptions/urdf/102588.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102588.json) |
| [102589](descriptions/urdf/102589.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102589.json) |
| [102590](descriptions/urdf/102590.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102590.json) |
| [102591](descriptions/urdf/102591.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102591.json) |
| [102596](descriptions/urdf/102596.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102596.json) |
| [102599](descriptions/urdf/102599.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102599.json) |
| [102601](descriptions/urdf/102601.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102601.json) |
| [102603](descriptions/urdf/102603.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102603.json) |
| [102608](descriptions/urdf/102608.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102608.json) |
| [102611](descriptions/urdf/102611.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102611.json) |
| [102612](descriptions/urdf/102612.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102612.json) |
| [102617](descriptions/urdf/102617.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/102617.json) |
| [102619](descriptions/urdf/102619.urdf) | Toilet | Sanitary Ware | 1 | 1 | 3 | [JSON](descriptions/finaljson/102619.json) |
| [102620](descriptions/urdf/102620.urdf) | Toilet | Sanitary Ware | 1 | 0 | 2 | [JSON](descriptions/finaljson/102620.json) |
| [102621](descriptions/urdf/102621.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102621.json) |
| [102622](descriptions/urdf/102622.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102622.json) |
| [102625](descriptions/urdf/102625.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102625.json) |
| [102628](descriptions/urdf/102628.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102628.json) |
| [102629](descriptions/urdf/102629.urdf) | Toilet | Sanitary Ware | 1 | 1 | 3 | [JSON](descriptions/finaljson/102629.json) |
| [102630](descriptions/urdf/102630.urdf) | Toilet | SanitaryWare | 2 | 0 | 3 | [JSON](descriptions/finaljson/102630.json) |
| [102631](descriptions/urdf/102631.urdf) | Toilet | SanitaryWare | 1 | 0 | 2 | [JSON](descriptions/finaljson/102631.json) |
| [102632](descriptions/urdf/102632.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102632.json) |
| [102634](descriptions/urdf/102634.urdf) | Toilet | Sanitary Ware | 2 | 0 | 3 | [JSON](descriptions/finaljson/102634.json) |
| [102636](descriptions/urdf/102636.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102636.json) |
| [102639](descriptions/urdf/102639.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102639.json) |
| [102641](descriptions/urdf/102641.urdf) | Toilet | Sanitary Ware | 1 | 1 | 3 | [JSON](descriptions/finaljson/102641.json) |
| [102643](descriptions/urdf/102643.urdf) | Toilet | SanitaryWare | 0 | 1 | 2 | [JSON](descriptions/finaljson/102643.json) |
| [102645](descriptions/urdf/102645.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102645.json) |
| [102646](descriptions/urdf/102646.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102646.json) |
| [102647](descriptions/urdf/102647.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102647.json) |
| [102648](descriptions/urdf/102648.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102648.json) |
| [102649](descriptions/urdf/102649.urdf) | Toilet | SanitaryWare | 1 | 0 | 2 | [JSON](descriptions/finaljson/102649.json) |
| [102650](descriptions/urdf/102650.urdf) | Toilet | SanitaryWare | 0 | 3 | 4 | [JSON](descriptions/finaljson/102650.json) |
| [102651](descriptions/urdf/102651.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102651.json) |
| [102652](descriptions/urdf/102652.urdf) | Toilet | SanitaryWare | 1 | 0 | 2 | [JSON](descriptions/finaljson/102652.json) |
| [102654](descriptions/urdf/102654.urdf) | Toilet | SanitaryWare | 3 | 0 | 4 | [JSON](descriptions/finaljson/102654.json) |
| [102655](descriptions/urdf/102655.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102655.json) |
| [102657](descriptions/urdf/102657.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102657.json) |
| [102658](descriptions/urdf/102658.urdf) | Toilet | Sanitary Ware | 2 | 0 | 3 | [JSON](descriptions/finaljson/102658.json) |
| [102660](descriptions/urdf/102660.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102660.json) |
| [102662](descriptions/urdf/102662.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102662.json) |
| [102663](descriptions/urdf/102663.urdf) | Toilet | SanitaryWare | 2 | 2 | 5 | [JSON](descriptions/finaljson/102663.json) |
| [102664](descriptions/urdf/102664.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102664.json) |
| [102665](descriptions/urdf/102665.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102665.json) |
| [102666](descriptions/urdf/102666.urdf) | Toilet | Sanitary Ware | 2 | 0 | 3 | [JSON](descriptions/finaljson/102666.json) |
| [102667](descriptions/urdf/102667.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102667.json) |
| [102668](descriptions/urdf/102668.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102668.json) |
| [102669](descriptions/urdf/102669.urdf) | Toilet | SanitaryWare | 1 | 0 | 2 | [JSON](descriptions/finaljson/102669.json) |
| [102670](descriptions/urdf/102670.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102670.json) |
| [102676](descriptions/urdf/102676.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102676.json) |
| [102677](descriptions/urdf/102677.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102677.json) |
| [102678](descriptions/urdf/102678.urdf) | Toilet | SanitaryWare | 0 | 1 | 2 | [JSON](descriptions/finaljson/102678.json) |
| [102679](descriptions/urdf/102679.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102679.json) |
| [102682](descriptions/urdf/102682.urdf) | Toilet | SanitaryWare | 0 | 2 | 3 | [JSON](descriptions/finaljson/102682.json) |
| [102684](descriptions/urdf/102684.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102684.json) |
| [102685](descriptions/urdf/102685.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102685.json) |
| [102687](descriptions/urdf/102687.urdf) | Toilet | SanitaryWare | 2 | 0 | 3 | [JSON](descriptions/finaljson/102687.json) |
| [102688](descriptions/urdf/102688.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102688.json) |
| [102689](descriptions/urdf/102689.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102689.json) |
| [102690](descriptions/urdf/102690.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102690.json) |
| [102692](descriptions/urdf/102692.urdf) | Toilet | Sanitary Ware | 2 | 1 | 4 | [JSON](descriptions/finaljson/102692.json) |
| [102694](descriptions/urdf/102694.urdf) | Toilet | SanitaryWare | 1 | 0 | 2 | [JSON](descriptions/finaljson/102694.json) |
| [102697](descriptions/urdf/102697.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102697.json) |
| [102698](descriptions/urdf/102698.urdf) | Toilet | SanitaryWare | 2 | 0 | 3 | [JSON](descriptions/finaljson/102698.json) |
| [102699](descriptions/urdf/102699.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102699.json) |
| [102701](descriptions/urdf/102701.urdf) | Toilet | Sanitary Ware | 2 | 1 | 4 | [JSON](descriptions/finaljson/102701.json) |
| [102702](descriptions/urdf/102702.urdf) | Toilet | Sanitary Ware | 1 | 1 | 3 | [JSON](descriptions/finaljson/102702.json) |
| [102703](descriptions/urdf/102703.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102703.json) |
| [102704](descriptions/urdf/102704.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102704.json) |
| [102706](descriptions/urdf/102706.urdf) | Toilet | Sanitary Ware | 1 | 1 | 3 | [JSON](descriptions/finaljson/102706.json) |
| [102707](descriptions/urdf/102707.urdf) | Toilet | SanitaryWare | 3 | 1 | 5 | [JSON](descriptions/finaljson/102707.json) |
| [102708](descriptions/urdf/102708.urdf) | Toilet | SanitaryWare | 2 | 1 | 4 | [JSON](descriptions/finaljson/102708.json) |
| [102710](descriptions/urdf/102710.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/102710.json) |
| [102714](descriptions/urdf/102714.urdf) | Kettle | Household Appliance | 1 | 1 | 4 | [JSON](descriptions/finaljson/102714.json) |
| [102715](descriptions/urdf/102715.urdf) | Kettle | Kitchenware | 0 | 1 | 3 | [JSON](descriptions/finaljson/102715.json) |
| [102720](descriptions/urdf/102720.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102720.json) |
| [102724](descriptions/urdf/102724.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102724.json) |
| [102726](descriptions/urdf/102726.urdf) | Kettle | Kitchen Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/102726.json) |
| [102730](descriptions/urdf/102730.urdf) | Kettle | Kitchen Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/102730.json) |
| [102732](descriptions/urdf/102732.urdf) | Kettle | Kitchenware | 0 | 1 | 3 | [JSON](descriptions/finaljson/102732.json) |
| [102736](descriptions/urdf/102736.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102736.json) |
| [102738](descriptions/urdf/102738.urdf) | Kettle | Kitchen Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/102738.json) |
| [102739](descriptions/urdf/102739.urdf) | Kettle | Kitchen Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/102739.json) |
| [102753](descriptions/urdf/102753.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102753.json) |
| [102756](descriptions/urdf/102756.urdf) | Kettle | Kitchen Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/102756.json) |
| [102761](descriptions/urdf/102761.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102761.json) |
| [102763](descriptions/urdf/102763.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102763.json) |
| [102765](descriptions/urdf/102765.urdf) | Kettle | Household Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102765.json) |
| [102768](descriptions/urdf/102768.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102768.json) |
| [102773](descriptions/urdf/102773.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102773.json) |
| [102786](descriptions/urdf/102786.urdf) | Kettle | Kitchen Appliance | 0 | 1 | 3 | [JSON](descriptions/finaljson/102786.json) |
| [102798](descriptions/urdf/102798.urdf) | Window | BuildingComponent | 0 | 4 | 5 | [JSON](descriptions/finaljson/102798.json) |
| [102801](descriptions/urdf/102801.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/102801.json) |
| [102802](descriptions/urdf/102802.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/102802.json) |
| [102803](descriptions/urdf/102803.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/102803.json) |
| [102804](descriptions/urdf/102804.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/102804.json) |
| [102805](descriptions/urdf/102805.urdf) | Window | BuildingComponent | 0 | 3 | 5 | [JSON](descriptions/finaljson/102805.json) |
| [102810](descriptions/urdf/102810.urdf) | Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102810.json) |
| [102812](descriptions/urdf/102812.urdf) | Switch | Electrical Component | 0 | 1 | 2 | [JSON](descriptions/finaljson/102812.json) |
| [102817](descriptions/urdf/102817.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102817.json) |
| [102829](descriptions/urdf/102829.urdf) | Camera | ElectronicDevice | 1 | 2 | 4 | [JSON](descriptions/finaljson/102829.json) |
| [102831](descriptions/urdf/102831.urdf) | Camera | ElectronicDevice | 2 | 11 | 15 | [JSON](descriptions/finaljson/102831.json) |
| [102834](descriptions/urdf/102834.urdf) | Camera | ElectronicDevice | 1 | 1 | 3 | [JSON](descriptions/finaljson/102834.json) |
| [102836](descriptions/urdf/102836.urdf) | Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102836.json) |
| [102839](descriptions/urdf/102839.urdf) | DIP Switch | Electronic Component | 0 | 6 | 7 | [JSON](descriptions/finaljson/102839.json) |
| [102843](descriptions/urdf/102843.urdf) | Wall Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102843.json) |
| [102844](descriptions/urdf/102844.urdf) | Switch | Electrical Control Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/102844.json) |
| [102845](descriptions/urdf/102845.urdf) | Camera | ElectronicDevice | 1 | 7 | 10 | [JSON](descriptions/finaljson/102845.json) |
| [102852](descriptions/urdf/102852.urdf) | Camera | ElectronicDevice | 1 | 1 | 3 | [JSON](descriptions/finaljson/102852.json) |
| [102856](descriptions/urdf/102856.urdf) | DIP Switch | Electronic Component | 0 | 8 | 9 | [JSON](descriptions/finaljson/102856.json) |
| [102860](descriptions/urdf/102860.urdf) | Switch | Electrical Component | 0 | 1 | 2 | [JSON](descriptions/finaljson/102860.json) |
| [102864](descriptions/urdf/102864.urdf) | Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/102864.json) |
| [102870](descriptions/urdf/102870.urdf) | Camera | ElectronicDevice | 4 | 1 | 7 | [JSON](descriptions/finaljson/102870.json) |
| [102872](descriptions/urdf/102872.urdf) | Switch | Electrical Component | 1 | 0 | 2 | [JSON](descriptions/finaljson/102872.json) |
| [102873](descriptions/urdf/102873.urdf) | Camera | ElectronicDevice | 1 | 2 | 4 | [JSON](descriptions/finaljson/102873.json) |
| [102874](descriptions/urdf/102874.urdf) | Camera | ElectronicDevice | 4 | 22 | 27 | [JSON](descriptions/finaljson/102874.json) |
| [102876](descriptions/urdf/102876.urdf) | Camera | Electronic Device | 4 | 2 | 7 | [JSON](descriptions/finaljson/102876.json) |
| [102882](descriptions/urdf/102882.urdf) | Camera | ElectronicDevice | 3 | 2 | 6 | [JSON](descriptions/finaljson/102882.json) |
| [102890](descriptions/urdf/102890.urdf) | Camera | DigitalCamera | 4 | 14 | 20 | [JSON](descriptions/finaljson/102890.json) |
| [102892](descriptions/urdf/102892.urdf) | Camera | ElectronicDevice | 2 | 5 | 8 | [JSON](descriptions/finaljson/102892.json) |
| [102896](descriptions/urdf/102896.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/102896.json) |
| [102901](descriptions/urdf/102901.urdf) | Coffee Machine | Kitchen Appliance | 3 | 6 | 10 | [JSON](descriptions/finaljson/102901.json) |
| [102903](descriptions/urdf/102903.urdf) | Sliding Window | Building Component | 0 | 3 | 4 | [JSON](descriptions/finaljson/102903.json) |
| [102905](descriptions/urdf/102905.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/102905.json) |
| [102906](descriptions/urdf/102906.urdf) | Sliding Window | Building Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/102906.json) |
| [102909](descriptions/urdf/102909.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102909.json) |
| [102910](descriptions/urdf/102910.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102910.json) |
| [102911](descriptions/urdf/102911.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102911.json) |
| [102915](descriptions/urdf/102915.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102915.json) |
| [102916](descriptions/urdf/102916.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102916.json) |
| [102917](descriptions/urdf/102917.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102917.json) |
| [102918](descriptions/urdf/102918.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102918.json) |
| [102922](descriptions/urdf/102922.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102922.json) |
| [102931](descriptions/urdf/102931.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102931.json) |
| [102938](descriptions/urdf/102938.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102938.json) |
| [102939](descriptions/urdf/102939.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102939.json) |
| [102940](descriptions/urdf/102940.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102940.json) |
| [102942](descriptions/urdf/102942.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102942.json) |
| [102943](descriptions/urdf/102943.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102943.json) |
| [102944](descriptions/urdf/102944.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102944.json) |
| [102945](descriptions/urdf/102945.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102945.json) |
| [102946](descriptions/urdf/102946.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102946.json) |
| [102952](descriptions/urdf/102952.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102952.json) |
| [102957](descriptions/urdf/102957.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102957.json) |
| [102960](descriptions/urdf/102960.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102960.json) |
| [102961](descriptions/urdf/102961.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102961.json) |
| [102962](descriptions/urdf/102962.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102962.json) |
| [102963](descriptions/urdf/102963.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102963.json) |
| [102965](descriptions/urdf/102965.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102965.json) |
| [102966](descriptions/urdf/102966.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102966.json) |
| [102970](descriptions/urdf/102970.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102970.json) |
| [102973](descriptions/urdf/102973.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102973.json) |
| [102975](descriptions/urdf/102975.urdf) | Pen | WritingInstrument | 0 | 2 | 3 | [JSON](descriptions/finaljson/102975.json) |
| [102977](descriptions/urdf/102977.urdf) | Window | Architectural Component | 0 | 3 | 4 | [JSON](descriptions/finaljson/102977.json) |
| [102980](descriptions/urdf/102980.urdf) | Pen | Writing Instrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102980.json) |
| [102981](descriptions/urdf/102981.urdf) | Window | BuildingComponent | 0 | 2 | 4 | [JSON](descriptions/finaljson/102981.json) |
| [102982](descriptions/urdf/102982.urdf) | Pen | WritingInstrument | 0 | 1 | 2 | [JSON](descriptions/finaljson/102982.json) |
| [102984](descriptions/urdf/102984.urdf) | Window | BuildingComponent | 0 | 2 | 4 | [JSON](descriptions/finaljson/102984.json) |
| [102985](descriptions/urdf/102985.urdf) | Window | BuildingComponent | 0 | 2 | 4 | [JSON](descriptions/finaljson/102985.json) |
| [102989](descriptions/urdf/102989.urdf) | Street Food Cart | Mobile Vending Cart | 2 | 0 | 4 | [JSON](descriptions/finaljson/102989.json) |
| [102990](descriptions/urdf/102990.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/102990.json) |
| [102992](descriptions/urdf/102992.urdf) | Trashcan | Household Utility Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/102992.json) |
| [102994](descriptions/urdf/102994.urdf) | Coffeemachine | KitchenAppliance | 3 | 0 | 5 | [JSON](descriptions/finaljson/102994.json) |
| [102996](descriptions/urdf/102996.urdf) | Trashcan | Household Waste Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/102996.json) |
| [103002](descriptions/urdf/103002.urdf) | Coffee Machine | Kitchen Appliance | 0 | 9 | 10 | [JSON](descriptions/finaljson/103002.json) |
| [103007](descriptions/urdf/103007.urdf) | Trashcan | Waste Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/103007.json) |
| [103008](descriptions/urdf/103008.urdf) | Trashcan | Household Utility Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/103008.json) |
| [103009](descriptions/urdf/103009.urdf) | Coffee Machine | Kitchen Appliance | 4 | 1 | 10 | [JSON](descriptions/finaljson/103009.json) |
| [103010](descriptions/urdf/103010.urdf) | Trashcan | Waste Container | 3 | 0 | 4 | [JSON](descriptions/finaljson/103010.json) |
| [103012](descriptions/urdf/103012.urdf) | Trashcan | Waste Container | 3 | 0 | 5 | [JSON](descriptions/finaljson/103012.json) |
| [103013](descriptions/urdf/103013.urdf) | Trashcan | Household Waste Container | 0 | 1 | 2 | [JSON](descriptions/finaljson/103013.json) |
| [103015](descriptions/urdf/103015.urdf) | Window | Architectural Element | 3 | 0 | 4 | [JSON](descriptions/finaljson/103015.json) |
| [103016](descriptions/urdf/103016.urdf) | Coffee Machine | Kitchen Appliance | 6 | 0 | 9 | [JSON](descriptions/finaljson/103016.json) |
| [103020](descriptions/urdf/103020.urdf) | Computer Mouse | Input Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/103020.json) |
| [103022](descriptions/urdf/103022.urdf) | Computer Mouse | Input Device | 1 | 6 | 8 | [JSON](descriptions/finaljson/103022.json) |
| [103023](descriptions/urdf/103023.urdf) | Computer Mouse | Input Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/103023.json) |
| [103024](descriptions/urdf/103024.urdf) | Mouse | ComputerPeripheral | 1 | 0 | 2 | [JSON](descriptions/finaljson/103024.json) |
| [103025](descriptions/urdf/103025.urdf) | Computer Mouse | Input Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/103025.json) |
| [103026](descriptions/urdf/103026.urdf) | Computer Mouse | Input Device | 1 | 2 | 4 | [JSON](descriptions/finaljson/103026.json) |
| [103028](descriptions/urdf/103028.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/103028.json) |
| [103029](descriptions/urdf/103029.urdf) | Eyeglasses | VisionAid | 2 | 0 | 3 | [JSON](descriptions/finaljson/103029.json) |
| [103030](descriptions/urdf/103030.urdf) | Coffee Machine | Kitchen Appliance | 1 | 2 | 4 | [JSON](descriptions/finaljson/103030.json) |
| [103031](descriptions/urdf/103031.urdf) | Coffeemachine | Kitchen Appliance | 7 | 0 | 8 | [JSON](descriptions/finaljson/103031.json) |
| [103032](descriptions/urdf/103032.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/103032.json) |
| [103037](descriptions/urdf/103037.urdf) | Coffee Machine | Kitchen Appliance | 1 | 4 | 7 | [JSON](descriptions/finaljson/103037.json) |
| [103038](descriptions/urdf/103038.urdf) | Coffee Machine | Kitchen Appliance | 0 | 2 | 3 | [JSON](descriptions/finaljson/103038.json) |
| [103040](descriptions/urdf/103040.urdf) | Window | BuildingComponent | 1 | 0 | 2 | [JSON](descriptions/finaljson/103040.json) |
| [103041](descriptions/urdf/103041.urdf) | Coffee Machine | Kitchen Appliance | 3 | 3 | 7 | [JSON](descriptions/finaljson/103041.json) |
| [103042](descriptions/urdf/103042.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103042.json) |
| [103044](descriptions/urdf/103044.urdf) | Window | Architectural Component | 0 | 3 | 4 | [JSON](descriptions/finaljson/103044.json) |
| [103046](descriptions/urdf/103046.urdf) | Coffee Machine | Kitchen Appliance | 6 | 9 | 17 | [JSON](descriptions/finaljson/103046.json) |
| [103048](descriptions/urdf/103048.urdf) | Coffee Machine | Kitchen Appliance | 1 | 3 | 5 | [JSON](descriptions/finaljson/103048.json) |
| [103050](descriptions/urdf/103050.urdf) | Window | BuildingComponent | 0 | 2 | 4 | [JSON](descriptions/finaljson/103050.json) |
| [103051](descriptions/urdf/103051.urdf) | Sliding Window | Building Fixture | 0 | 2 | 3 | [JSON](descriptions/finaljson/103051.json) |
| [103052](descriptions/urdf/103052.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103052.json) |
| [103056](descriptions/urdf/103056.urdf) | Window | BuildingComponent | 1 | 0 | 2 | [JSON](descriptions/finaljson/103056.json) |
| [103057](descriptions/urdf/103057.urdf) | Coffee Machine | Kitchen Appliance | 2 | 1 | 5 | [JSON](descriptions/finaljson/103057.json) |
| [103058](descriptions/urdf/103058.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/103058.json) |
| [103060](descriptions/urdf/103060.urdf) | Coffee Machine | Kitchen Appliance | 0 | 1 | 2 | [JSON](descriptions/finaljson/103060.json) |
| [103062](descriptions/urdf/103062.urdf) | Coffeemachine | Kitchen Appliance | 1 | 2 | 4 | [JSON](descriptions/finaljson/103062.json) |
| [103063](descriptions/urdf/103063.urdf) | Sliding Window | Architectural Component | 0 | 6 | 7 | [JSON](descriptions/finaljson/103063.json) |
| [103064](descriptions/urdf/103064.urdf) | Coffee Machine | Kitchen Appliance | 0 | 15 | 16 | [JSON](descriptions/finaljson/103064.json) |
| [103065](descriptions/urdf/103065.urdf) | Coffee Machine | Kitchen Appliance | 0 | 2 | 6 | [JSON](descriptions/finaljson/103065.json) |
| [103067](descriptions/urdf/103067.urdf) | Coffee Machine | Kitchen Appliance | 1 | 1 | 4 | [JSON](descriptions/finaljson/103067.json) |
| [103069](descriptions/urdf/103069.urdf) | Coffee Machine | Kitchen Appliance | 0 | 10 | 11 | [JSON](descriptions/finaljson/103069.json) |
| [103070](descriptions/urdf/103070.urdf) | Sliding Window | Building Component | 0 | 4 | 5 | [JSON](descriptions/finaljson/103070.json) |
| [103071](descriptions/urdf/103071.urdf) | Coffee Machine | Kitchen Appliance | 5 | 0 | 7 | [JSON](descriptions/finaljson/103071.json) |
| [103072](descriptions/urdf/103072.urdf) | Coffee Machine | Kitchen Appliance | 0 | 6 | 7 | [JSON](descriptions/finaljson/103072.json) |
| [103074](descriptions/urdf/103074.urdf) | Coffee Machine | Kitchen Appliance | 3 | 0 | 6 | [JSON](descriptions/finaljson/103074.json) |
| [103075](descriptions/urdf/103075.urdf) | Coffee Machine | Kitchen Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/103075.json) |
| [103077](descriptions/urdf/103077.urdf) | Window | BuildingComponent | 0 | 2 | 4 | [JSON](descriptions/finaljson/103077.json) |
| [103079](descriptions/urdf/103079.urdf) | Coffee Machine | Kitchen Appliance | 0 | 4 | 7 | [JSON](descriptions/finaljson/103079.json) |
| [103080](descriptions/urdf/103080.urdf) | Coffee Machine | Kitchen Appliance | 0 | 2 | 3 | [JSON](descriptions/finaljson/103080.json) |
| [103082](descriptions/urdf/103082.urdf) | Coffee Machine | Kitchen Appliance | 1 | 0 | 4 | [JSON](descriptions/finaljson/103082.json) |
| [103084](descriptions/urdf/103084.urdf) | Coffee Machine | Kitchen Appliance | 9 | 2 | 12 | [JSON](descriptions/finaljson/103084.json) |
| [103086](descriptions/urdf/103086.urdf) | Coffee Machine | Kitchen Appliance | 0 | 2 | 3 | [JSON](descriptions/finaljson/103086.json) |
| [103087](descriptions/urdf/103087.urdf) | Coffee Machine | Kitchen Appliance | 1 | 2 | 5 | [JSON](descriptions/finaljson/103087.json) |
| [103088](descriptions/urdf/103088.urdf) | Coffee Machine | Kitchen Appliance | 0 | 1 | 5 | [JSON](descriptions/finaljson/103088.json) |
| [103092](descriptions/urdf/103092.urdf) | Coffee Machine | Kitchen Appliance | 1 | 4 | 6 | [JSON](descriptions/finaljson/103092.json) |
| [103095](descriptions/urdf/103095.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103095.json) |
| [103098](descriptions/urdf/103098.urdf) | Coffee Machine | Kitchen Appliance | 0 | 4 | 7 | [JSON](descriptions/finaljson/103098.json) |
| [103099](descriptions/urdf/103099.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103099.json) |
| [103100](descriptions/urdf/103100.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103100.json) |
| [103101](descriptions/urdf/103101.urdf) | Coffee Machine | Kitchen Appliance | 3 | 8 | 12 | [JSON](descriptions/finaljson/103101.json) |
| [103104](descriptions/urdf/103104.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103104.json) |
| [103105](descriptions/urdf/103105.urdf) | Coffee Machine | Kitchen Appliance | 1 | 2 | 5 | [JSON](descriptions/finaljson/103105.json) |
| [103111](descriptions/urdf/103111.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103111.json) |
| [103113](descriptions/urdf/103113.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103113.json) |
| [103118](descriptions/urdf/103118.urdf) | Coffee Machine | Kitchen Appliance | 7 | 0 | 10 | [JSON](descriptions/finaljson/103118.json) |
| [103121](descriptions/urdf/103121.urdf) | Coffee Machine | Kitchen Appliance | 2 | 8 | 11 | [JSON](descriptions/finaljson/103121.json) |
| [103123](descriptions/urdf/103123.urdf) | Coffee Machine | Kitchen Appliance | 1 | 10 | 12 | [JSON](descriptions/finaljson/103123.json) |
| [103124](descriptions/urdf/103124.urdf) | Coffee Machine | Kitchen Appliance | 3 | 8 | 12 | [JSON](descriptions/finaljson/103124.json) |
| [103125](descriptions/urdf/103125.urdf) | Coffee Machine | Kitchen Appliance | 3 | 0 | 5 | [JSON](descriptions/finaljson/103125.json) |
| [103126](descriptions/urdf/103126.urdf) | Coffee Machine | Kitchen Appliance | 4 | 8 | 15 | [JSON](descriptions/finaljson/103126.json) |
| [103127](descriptions/urdf/103127.urdf) | Coffee Machine | Kitchen Appliance | 0 | 4 | 5 | [JSON](descriptions/finaljson/103127.json) |
| [103128](descriptions/urdf/103128.urdf) | Coffee Machine | Kitchen Appliance | 2 | 5 | 9 | [JSON](descriptions/finaljson/103128.json) |
| [103129](descriptions/urdf/103129.urdf) | Coffee Machine | Kitchen Appliance | 1 | 3 | 5 | [JSON](descriptions/finaljson/103129.json) |
| [103134](descriptions/urdf/103134.urdf) | Coffee Machine | Kitchen Appliance | 0 | 9 | 10 | [JSON](descriptions/finaljson/103134.json) |
| [103135](descriptions/urdf/103135.urdf) | Window | BuildingComponent | 1 | 0 | 2 | [JSON](descriptions/finaljson/103135.json) |
| [103137](descriptions/urdf/103137.urdf) | Coffee Machine | Kitchen Appliance | 1 | 6 | 8 | [JSON](descriptions/finaljson/103137.json) |
| [103138](descriptions/urdf/103138.urdf) | Coffee Machine | Kitchen Appliance | 1 | 2 | 4 | [JSON](descriptions/finaljson/103138.json) |
| [103140](descriptions/urdf/103140.urdf) | Coffee Machine | Kitchen Appliance | 0 | 9 | 10 | [JSON](descriptions/finaljson/103140.json) |
| [103143](descriptions/urdf/103143.urdf) | Coffee Machine | Kitchen Appliance | 1 | 6 | 8 | [JSON](descriptions/finaljson/103143.json) |
| [103144](descriptions/urdf/103144.urdf) | Coffee Machine | Kitchen Appliance | 1 | 9 | 11 | [JSON](descriptions/finaljson/103144.json) |
| [103146](descriptions/urdf/103146.urdf) | Coffeemachine | Kitchen Appliance | 0 | 1 | 2 | [JSON](descriptions/finaljson/103146.json) |
| [103148](descriptions/urdf/103148.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103148.json) |
| [103149](descriptions/urdf/103149.urdf) | Window | BuildingComponent | 0 | 1 | 2 | [JSON](descriptions/finaljson/103149.json) |
| [103150](descriptions/urdf/103150.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/103150.json) |
| [103153](descriptions/urdf/103153.urdf) | Tower Fan | Electrical Appliance | 3 | 0 | 4 | [JSON](descriptions/finaljson/103153.json) |
| [103154](descriptions/urdf/103154.urdf) | Tower Fan | Electrical Appliance | 3 | 0 | 4 | [JSON](descriptions/finaljson/103154.json) |
| [103171](descriptions/urdf/103171.urdf) | Ceiling Fan | Electrical Appliance | 1 | 0 | 2 | [JSON](descriptions/finaljson/103171.json) |
| [103177](descriptions/urdf/103177.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/103177.json) |
| [103178](descriptions/urdf/103178.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/103178.json) |
| [103184](descriptions/urdf/103184.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 4 | [JSON](descriptions/finaljson/103184.json) |
| [103186](descriptions/urdf/103186.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/103186.json) |
| [103189](descriptions/urdf/103189.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/103189.json) |
| [103194](descriptions/urdf/103194.urdf) | Eyeglasses | OpticalAccessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/103194.json) |
| [103201](descriptions/urdf/103201.urdf) | Kettle | Kitchenware | 0 | 1 | 3 | [JSON](descriptions/finaljson/103201.json) |
| [103207](descriptions/urdf/103207.urdf) | Kettle | Kitchenware | 0 | 1 | 3 | [JSON](descriptions/finaljson/103207.json) |
| [103208](descriptions/urdf/103208.urdf) | Kettle | Household Appliance | 0 | 2 | 5 | [JSON](descriptions/finaljson/103208.json) |
| [103222](descriptions/urdf/103222.urdf) | Kettle | Kitchenware | 0 | 1 | 3 | [JSON](descriptions/finaljson/103222.json) |
| [103223](descriptions/urdf/103223.urdf) | Kettle | Household Appliance | 1 | 0 | 3 | [JSON](descriptions/finaljson/103223.json) |
| [103227](descriptions/urdf/103227.urdf) | Toilet | SanitaryWare | 1 | 0 | 2 | [JSON](descriptions/finaljson/103227.json) |
| [103230](descriptions/urdf/103230.urdf) | Toilet | SanitaryWare | 0 | 3 | 4 | [JSON](descriptions/finaljson/103230.json) |
| [103233](descriptions/urdf/103233.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/103233.json) |
| [103234](descriptions/urdf/103234.urdf) | Toilet | SanitaryWare | 1 | 1 | 3 | [JSON](descriptions/finaljson/103234.json) |
| [103235](descriptions/urdf/103235.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103235.json) |
| [103236](descriptions/urdf/103236.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/103236.json) |
| [103238](descriptions/urdf/103238.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/103238.json) |
| [103239](descriptions/urdf/103239.urdf) | Window | BuildingComponent | 0 | 1 | 2 | [JSON](descriptions/finaljson/103239.json) |
| [103242](descriptions/urdf/103242.urdf) | Window | Architectural Element | 0 | 1 | 2 | [JSON](descriptions/finaljson/103242.json) |
| [103251](descriptions/urdf/103251.urdf) | Phone | ElectronicDevice | 0 | 22 | 23 | [JSON](descriptions/finaljson/103251.json) |
| [103252](descriptions/urdf/103252.urdf) | Flip Phone | Communication Device | 0 | 19 | 21 | [JSON](descriptions/finaljson/103252.json) |
| [103253](descriptions/urdf/103253.urdf) | Window | BuildingComponent | 0 | 3 | 4 | [JSON](descriptions/finaljson/103253.json) |
| [103255](descriptions/urdf/103255.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103255.json) |
| [103268](descriptions/urdf/103268.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/103268.json) |
| [103271](descriptions/urdf/103271.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103271.json) |
| [103273](descriptions/urdf/103273.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103273.json) |
| [103275](descriptions/urdf/103275.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103275.json) |
| [103276](descriptions/urdf/103276.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103276.json) |
| [103280](descriptions/urdf/103280.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103280.json) |
| [103283](descriptions/urdf/103283.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103283.json) |
| [103285](descriptions/urdf/103285.urdf) | Mobile Phone | Communication Device | 0 | 13 | 14 | [JSON](descriptions/finaljson/103285.json) |
| [103292](descriptions/urdf/103292.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103292.json) |
| [103293](descriptions/urdf/103293.urdf) | Stapler | OfficeTool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103293.json) |
| [103297](descriptions/urdf/103297.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103297.json) |
| [103299](descriptions/urdf/103299.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103299.json) |
| [103301](descriptions/urdf/103301.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103301.json) |
| [103303](descriptions/urdf/103303.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103303.json) |
| [103305](descriptions/urdf/103305.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103305.json) |
| [103307](descriptions/urdf/103307.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103307.json) |
| [103311](descriptions/urdf/103311.urdf) | Window | Architectural Component | 4 | 0 | 5 | [JSON](descriptions/finaljson/103311.json) |
| [103312](descriptions/urdf/103312.urdf) | Window | BuildingComponent | 0 | 1 | 2 | [JSON](descriptions/finaljson/103312.json) |
| [103315](descriptions/urdf/103315.urdf) | Window | BuildingComponent | 0 | 4 | 5 | [JSON](descriptions/finaljson/103315.json) |
| [103316](descriptions/urdf/103316.urdf) | Window | Architectural Component | 0 | 4 | 5 | [JSON](descriptions/finaljson/103316.json) |
| [103318](descriptions/urdf/103318.urdf) | Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103318.json) |
| [103319](descriptions/urdf/103319.urdf) | Window | Architectural Element | 0 | 3 | 5 | [JSON](descriptions/finaljson/103319.json) |
| [103320](descriptions/urdf/103320.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103320.json) |
| [103321](descriptions/urdf/103321.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/103321.json) |
| [103323](descriptions/urdf/103323.urdf) | Window | BuildingComponent | 0 | 2 | 3 | [JSON](descriptions/finaljson/103323.json) |
| [103325](descriptions/urdf/103325.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103325.json) |
| [103329](descriptions/urdf/103329.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103329.json) |
| [103332](descriptions/urdf/103332.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103332.json) |
| [103333](descriptions/urdf/103333.urdf) | Sliding Window | Architectural Component | 0 | 2 | 3 | [JSON](descriptions/finaljson/103333.json) |
| [103339](descriptions/urdf/103339.urdf) | Window | BuildingComponent | 0 | 2 | 4 | [JSON](descriptions/finaljson/103339.json) |
| [103340](descriptions/urdf/103340.urdf) | Window | BuildingComponent | 0 | 4 | 5 | [JSON](descriptions/finaljson/103340.json) |
| [103347](descriptions/urdf/103347.urdf) | Phone | ElectronicDevice | 0 | 19 | 20 | [JSON](descriptions/finaljson/103347.json) |
| [103350](descriptions/urdf/103350.urdf) | Flip Phone | Electronic Device | 1 | 14 | 16 | [JSON](descriptions/finaljson/103350.json) |
| [103351](descriptions/urdf/103351.urdf) | Washing Machine | Home Appliance | 3 | 7 | 12 | [JSON](descriptions/finaljson/103351.json) |
| [103352](descriptions/urdf/103352.urdf) | Liquid Soap Dispenser | Bathroom Accessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/103352.json) |
| [103353](descriptions/urdf/103353.urdf) | Dispenser | Liquid Container / Pump Dispenser | 2 | 0 | 3 | [JSON](descriptions/finaljson/103353.json) |
| [103354](descriptions/urdf/103354.urdf) | Dispenser | Liquid Dispenser / Pump Bottle | 2 | 0 | 3 | [JSON](descriptions/finaljson/103354.json) |
| [103355](descriptions/urdf/103355.urdf) | Dispenser | Liquid Container / Pump Bottle | 2 | 0 | 3 | [JSON](descriptions/finaljson/103355.json) |
| [103356](descriptions/urdf/103356.urdf) | Liquid Soap Dispenser | Hygiene Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/103356.json) |
| [103357](descriptions/urdf/103357.urdf) | Dispenser | Liquid Container / Pump Bottle | 2 | 0 | 3 | [JSON](descriptions/finaljson/103357.json) |
| [103358](descriptions/urdf/103358.urdf) | Dispenser | Liquid Container / Pump Bottle | 2 | 0 | 3 | [JSON](descriptions/finaljson/103358.json) |
| [103359](descriptions/urdf/103359.urdf) | Dispenser | Liquid Container / Pump Bottle | 2 | 0 | 3 | [JSON](descriptions/finaljson/103359.json) |
| [103360](descriptions/urdf/103360.urdf) | Dispenser | Liquid Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/103360.json) |
| [103361](descriptions/urdf/103361.urdf) | Washing Machine | Home Appliance | 2 | 7 | 10 | [JSON](descriptions/finaljson/103361.json) |
| [103369](descriptions/urdf/103369.urdf) | Washing Machine | Home Appliance | 2 | 11 | 14 | [JSON](descriptions/finaljson/103369.json) |
| [103371](descriptions/urdf/103371.urdf) | Dispenser | Liquid Dispenser | 2 | 0 | 4 | [JSON](descriptions/finaljson/103371.json) |
| [103372](descriptions/urdf/103372.urdf) | Dispenser | Liquid Container | 1 | 1 | 3 | [JSON](descriptions/finaljson/103372.json) |
| [103377](descriptions/urdf/103377.urdf) | Dispenser | Liquid Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/103377.json) |
| [103378](descriptions/urdf/103378.urdf) | Liquid Dispenser | Container/Dispenser | 2 | 0 | 4 | [JSON](descriptions/finaljson/103378.json) |
| [103379](descriptions/urdf/103379.urdf) | Dispenser | Liquid Dispenser / Pump Bottle | 2 | 0 | 3 | [JSON](descriptions/finaljson/103379.json) |
| [103380](descriptions/urdf/103380.urdf) | Dispenser | Liquid Container / Pump Dispenser | 2 | 0 | 3 | [JSON](descriptions/finaljson/103380.json) |
| [103394](descriptions/urdf/103394.urdf) | Liquid Soap Dispenser | Hygiene Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/103394.json) |
| [103397](descriptions/urdf/103397.urdf) | Liquid Soap Dispenser | Dispenser | 2 | 0 | 3 | [JSON](descriptions/finaljson/103397.json) |
| [103402](descriptions/urdf/103402.urdf) | Dispenser | Liquid Dispenser | 1 | 0 | 3 | [JSON](descriptions/finaljson/103402.json) |
| [103404](descriptions/urdf/103404.urdf) | Liquid Soap Dispenser | Hygiene Accessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/103404.json) |
| [103405](descriptions/urdf/103405.urdf) | Dispenser | Spray Bottle | 2 | 0 | 3 | [JSON](descriptions/finaljson/103405.json) |
| [103406](descriptions/urdf/103406.urdf) | Dispenser | LiquidContainer | 2 | 0 | 4 | [JSON](descriptions/finaljson/103406.json) |
| [103408](descriptions/urdf/103408.urdf) | Liquid Soap Dispenser | Hygiene Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/103408.json) |
| [103410](descriptions/urdf/103410.urdf) | Liquid Soap Dispenser | Hygiene Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/103410.json) |
| [103416](descriptions/urdf/103416.urdf) | Liquid Soap Dispenser | Bathroom Accessory | 2 | 0 | 3 | [JSON](descriptions/finaljson/103416.json) |
| [103419](descriptions/urdf/103419.urdf) | Dispenser | Liquid Dispenser | 0 | 1 | 2 | [JSON](descriptions/finaljson/103419.json) |
| [103422](descriptions/urdf/103422.urdf) | Liquid Soap Dispenser | Hygiene Container | 2 | 0 | 3 | [JSON](descriptions/finaljson/103422.json) |
| [103423](descriptions/urdf/103423.urdf) | Liquid Soap Dispenser | Hygiene Container | 2 | 0 | 4 | [JSON](descriptions/finaljson/103423.json) |
| [103424](descriptions/urdf/103424.urdf) | Dispenser | Liquid Container / Pump Bottle | 2 | 0 | 3 | [JSON](descriptions/finaljson/103424.json) |
| [103425](descriptions/urdf/103425.urdf) | Washing Machine | Home Appliance | 2 | 7 | 10 | [JSON](descriptions/finaljson/103425.json) |
| [103452](descriptions/urdf/103452.urdf) | Washing Machine | Home Appliance | 3 | 10 | 14 | [JSON](descriptions/finaljson/103452.json) |
| [103465](descriptions/urdf/103465.urdf) | Toaster | Kitchen Appliance | 1 | 1 | 5 | [JSON](descriptions/finaljson/103465.json) |
| [103466](descriptions/urdf/103466.urdf) | Toaster | Kitchen Appliance | 1 | 2 | 6 | [JSON](descriptions/finaljson/103466.json) |
| [103469](descriptions/urdf/103469.urdf) | Toaster | Kitchen Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/103469.json) |
| [103473](descriptions/urdf/103473.urdf) | Toaster | Kitchen Appliance | 0 | 2 | 3 | [JSON](descriptions/finaljson/103473.json) |
| [103475](descriptions/urdf/103475.urdf) | Toaster | Kitchen Appliance | 1 | 1 | 5 | [JSON](descriptions/finaljson/103475.json) |
| [103477](descriptions/urdf/103477.urdf) | Toaster | Kitchen Appliance | 1 | 2 | 4 | [JSON](descriptions/finaljson/103477.json) |
| [103480](descriptions/urdf/103480.urdf) | Washing Machine | Home Appliance | 2 | 6 | 9 | [JSON](descriptions/finaljson/103480.json) |
| [103482](descriptions/urdf/103482.urdf) | Toaster | Kitchen Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/103482.json) |
| [103483](descriptions/urdf/103483.urdf) | Toaster | Kitchen Appliance | 0 | 1 | 2 | [JSON](descriptions/finaljson/103483.json) |
| [103485](descriptions/urdf/103485.urdf) | Toaster | Kitchen Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/103485.json) |
| [103486](descriptions/urdf/103486.urdf) | Toaster | Kitchen Appliance | 1 | 4 | 6 | [JSON](descriptions/finaljson/103486.json) |
| [103490](descriptions/urdf/103490.urdf) | Washing Machine | Home Appliance | 1 | 4 | 6 | [JSON](descriptions/finaljson/103490.json) |
| [103498](descriptions/urdf/103498.urdf) | Toaster | Kitchen Appliance | 0 | 1 | 2 | [JSON](descriptions/finaljson/103498.json) |
| [103502](descriptions/urdf/103502.urdf) | Toaster | Kitchen Appliance | 2 | 2 | 5 | [JSON](descriptions/finaljson/103502.json) |
| [103503](descriptions/urdf/103503.urdf) | Lighter | Handheld Fire Ignition Device | 2 | 0 | 3 | [JSON](descriptions/finaljson/103503.json) |
| [103508](descriptions/urdf/103508.urdf) | Washing Machine | Home Appliance | 4 | 0 | 5 | [JSON](descriptions/finaljson/103508.json) |
| [103513](descriptions/urdf/103513.urdf) | Lighter | Household Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/103513.json) |
| [103514](descriptions/urdf/103514.urdf) | Toaster | Kitchen Appliance | 1 | 2 | 4 | [JSON](descriptions/finaljson/103514.json) |
| [103515](descriptions/urdf/103515.urdf) | Lighter | Handheld Fire Ignition Device | 1 | 1 | 3 | [JSON](descriptions/finaljson/103515.json) |
| [103516](descriptions/urdf/103516.urdf) | Lighter | Everyday Object / Fire-starting Tool | 3 | 0 | 4 | [JSON](descriptions/finaljson/103516.json) |
| [103518](descriptions/urdf/103518.urdf) | Washing Machine | Home Appliance | 3 | 4 | 8 | [JSON](descriptions/finaljson/103518.json) |
| [103521](descriptions/urdf/103521.urdf) | Washing Machine | Home Appliance | 3 | 1 | 5 | [JSON](descriptions/finaljson/103521.json) |
| [103524](descriptions/urdf/103524.urdf) | Toaster | Kitchen Appliance | 1 | 2 | 10 | [JSON](descriptions/finaljson/103524.json) |
| [103528](descriptions/urdf/103528.urdf) | Washing Machine | Home Appliance | 5 | 1 | 7 | [JSON](descriptions/finaljson/103528.json) |
| [103540](descriptions/urdf/103540.urdf) | Sliding Window | Architectural Component | 0 | 4 | 5 | [JSON](descriptions/finaljson/103540.json) |
| [103545](descriptions/urdf/103545.urdf) | Toaster | Kitchen Appliance | 0 | 4 | 5 | [JSON](descriptions/finaljson/103545.json) |
| [103547](descriptions/urdf/103547.urdf) | Toaster | Kitchen Appliance | 1 | 3 | 5 | [JSON](descriptions/finaljson/103547.json) |
| [103548](descriptions/urdf/103548.urdf) | Toaster | Kitchen Appliance | 8 | 2 | 11 | [JSON](descriptions/finaljson/103548.json) |
| [103549](descriptions/urdf/103549.urdf) | Toaster | Kitchen Appliance | 0 | 5 | 6 | [JSON](descriptions/finaljson/103549.json) |
| [103553](descriptions/urdf/103553.urdf) | Toaster | Kitchen Appliance | 2 | 10 | 13 | [JSON](descriptions/finaljson/103553.json) |
| [103555](descriptions/urdf/103555.urdf) | Toaster | Kitchen Appliance | 0 | 3 | 4 | [JSON](descriptions/finaljson/103555.json) |
| [103556](descriptions/urdf/103556.urdf) | Toaster | Kitchen Appliance | 2 | 2 | 5 | [JSON](descriptions/finaljson/103556.json) |
| [103558](descriptions/urdf/103558.urdf) | Toaster | Kitchen Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/103558.json) |
| [103559](descriptions/urdf/103559.urdf) | Toaster | Kitchen Appliance | 0 | 3 | 4 | [JSON](descriptions/finaljson/103559.json) |
| [103560](descriptions/urdf/103560.urdf) | Toaster | Kitchen Appliance | 1 | 4 | 6 | [JSON](descriptions/finaljson/103560.json) |
| [103561](descriptions/urdf/103561.urdf) | Toaster | Kitchen Appliance | 2 | 2 | 9 | [JSON](descriptions/finaljson/103561.json) |
| [103572](descriptions/urdf/103572.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/103572.json) |
| [103575](descriptions/urdf/103575.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/103575.json) |
| [103582](descriptions/urdf/103582.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/103582.json) |
| [103583](descriptions/urdf/103583.urdf) | Knife | Folding Knife | 1 | 0 | 2 | [JSON](descriptions/finaljson/103583.json) |
| [103585](descriptions/urdf/103585.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/103585.json) |
| [103593](descriptions/urdf/103593.urdf) | Phone | ElectronicDevice | 1 | 1 | 4 | [JSON](descriptions/finaljson/103593.json) |
| [103619](descriptions/urdf/103619.urdf) | Dispenser | Spray Bottle | 2 | 0 | 5 | [JSON](descriptions/finaljson/103619.json) |
| [103633](descriptions/urdf/103633.urdf) | Trashcan | Household Utility Object | 2 | 0 | 4 | [JSON](descriptions/finaljson/103633.json) |
| [103634](descriptions/urdf/103634.urdf) | Trashcan | WasteContainer | 3 | 0 | 5 | [JSON](descriptions/finaljson/103634.json) |
| [103635](descriptions/urdf/103635.urdf) | Trashcan | Waste Container | 1 | 0 | 2 | [JSON](descriptions/finaljson/103635.json) |
| [103639](descriptions/urdf/103639.urdf) | Trashcan | Waste Container | 5 | 0 | 6 | [JSON](descriptions/finaljson/103639.json) |
| [103646](descriptions/urdf/103646.urdf) | Trashcan | Household Utility Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/103646.json) |
| [103647](descriptions/urdf/103647.urdf) | Trashcan | Household Utility Object | 2 | 0 | 3 | [JSON](descriptions/finaljson/103647.json) |
| [103669](descriptions/urdf/103669.urdf) | Window | Architectural Component | 0 | 3 | 4 | [JSON](descriptions/finaljson/103669.json) |
| [103684](descriptions/urdf/103684.urdf) | Window | BuildingComponent | 0 | 3 | 4 | [JSON](descriptions/finaljson/103684.json) |
| [103699](descriptions/urdf/103699.urdf) | Phone | Electronic Device | 0 | 15 | 16 | [JSON](descriptions/finaljson/103699.json) |
| [103700](descriptions/urdf/103700.urdf) | Knife | Folding Knife | 1 | 0 | 2 | [JSON](descriptions/finaljson/103700.json) |
| [103706](descriptions/urdf/103706.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/103706.json) |
| [103713](descriptions/urdf/103713.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/103713.json) |
| [103716](descriptions/urdf/103716.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/103716.json) |
| [103723](descriptions/urdf/103723.urdf) | Knife | Folding Knife | 1 | 0 | 2 | [JSON](descriptions/finaljson/103723.json) |
| [103725](descriptions/urdf/103725.urdf) | Knife | Utility Knife | 0 | 1 | 2 | [JSON](descriptions/finaljson/103725.json) |
| [103728](descriptions/urdf/103728.urdf) | Utility Knife | Cutting Tool | 0 | 1 | 2 | [JSON](descriptions/finaljson/103728.json) |
| [103729](descriptions/urdf/103729.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/103729.json) |
| [103733](descriptions/urdf/103733.urdf) | Knife | Cutting Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103733.json) |
| [103735](descriptions/urdf/103735.urdf) | Knife | Cutting Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/103735.json) |
| [103739](descriptions/urdf/103739.urdf) | Folding Knife | Hand Tool | 4 | 0 | 5 | [JSON](descriptions/finaljson/103739.json) |
| [103740](descriptions/urdf/103740.urdf) | Folding Knife | Cutting Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103740.json) |
| [103755](descriptions/urdf/103755.urdf) | Suitcase | Luggage | 2 | 0 | 3 | [JSON](descriptions/finaljson/103755.json) |
| [103757](descriptions/urdf/103757.urdf) | Suitcase | Luggage | 1 | 0 | 3 | [JSON](descriptions/finaljson/103757.json) |
| [103761](descriptions/urdf/103761.urdf) | Suitcase | Luggage | 2 | 0 | 3 | [JSON](descriptions/finaljson/103761.json) |
| [103762](descriptions/urdf/103762.urdf) | Suitcase | Luggage | 2 | 0 | 3 | [JSON](descriptions/finaljson/103762.json) |
| [103770](descriptions/urdf/103770.urdf) | Luggage | TravelBag | 0 | 1 | 2 | [JSON](descriptions/finaljson/103770.json) |
| [103775](descriptions/urdf/103775.urdf) | Washing Machine | Home Appliance | 1 | 1 | 3 | [JSON](descriptions/finaljson/103775.json) |
| [103776](descriptions/urdf/103776.urdf) | Washing Machine | Home Appliance | 4 | 0 | 5 | [JSON](descriptions/finaljson/103776.json) |
| [103778](descriptions/urdf/103778.urdf) | Washing Machine | Home Appliance | 2 | 6 | 9 | [JSON](descriptions/finaljson/103778.json) |
| [103781](descriptions/urdf/103781.urdf) | Washing Machine | Home Appliance | 5 | 0 | 6 | [JSON](descriptions/finaljson/103781.json) |
| [103789](descriptions/urdf/103789.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103789.json) |
| [103792](descriptions/urdf/103792.urdf) | Stapler | Office Tool | 2 | 0 | 3 | [JSON](descriptions/finaljson/103792.json) |
| [103811](descriptions/urdf/103811.urdf) | Printer | Office Equipment | 0 | 30 | 33 | [JSON](descriptions/finaljson/103811.json) |
| [103813](descriptions/urdf/103813.urdf) | Phone | Electronic Device | 0 | 7 | 8 | [JSON](descriptions/finaljson/103813.json) |
| [103814](descriptions/urdf/103814.urdf) | Phone | Electronic Device | 0 | 17 | 19 | [JSON](descriptions/finaljson/103814.json) |
| [103828](descriptions/urdf/103828.urdf) | Phone | ElectronicDevice | 0 | 1 | 7 | [JSON](descriptions/finaljson/103828.json) |
| [103853](descriptions/urdf/103853.urdf) | Printer | Office Equipment | 0 | 27 | 29 | [JSON](descriptions/finaljson/103853.json) |
| [103859](descriptions/urdf/103859.urdf) | Printer | Office Equipment | 0 | 9 | 10 | [JSON](descriptions/finaljson/103859.json) |
| [103863](descriptions/urdf/103863.urdf) | Printer | ElectronicDevice | 0 | 2 | 4 | [JSON](descriptions/finaljson/103863.json) |
| [103866](descriptions/urdf/103866.urdf) | Printer | Office Equipment | 0 | 24 | 25 | [JSON](descriptions/finaljson/103866.json) |
| [103867](descriptions/urdf/103867.urdf) | Printer | Office Equipment | 0 | 17 | 18 | [JSON](descriptions/finaljson/103867.json) |
| [103869](descriptions/urdf/103869.urdf) | Printer | Office Equipment | 0 | 33 | 35 | [JSON](descriptions/finaljson/103869.json) |
| [103872](descriptions/urdf/103872.urdf) | Printer | ElectronicDevice | 0 | 3 | 5 | [JSON](descriptions/finaljson/103872.json) |
| [103878](descriptions/urdf/103878.urdf) | Printer | ElectronicDevice | 0 | 8 | 9 | [JSON](descriptions/finaljson/103878.json) |
| [103886](descriptions/urdf/103886.urdf) | Flip Phone | Electronic Device | 1 | 0 | 2 | [JSON](descriptions/finaljson/103886.json) |
| [103892](descriptions/urdf/103892.urdf) | Phone | ElectronicDevice | 2 | 19 | 22 | [JSON](descriptions/finaljson/103892.json) |
| [103894](descriptions/urdf/103894.urdf) | Printer | ElectronicDevice | 0 | 1 | 3 | [JSON](descriptions/finaljson/103894.json) |
| [103916](descriptions/urdf/103916.urdf) | Phone | ElectronicDevice | 0 | 4 | 10 | [JSON](descriptions/finaljson/103916.json) |
| [103917](descriptions/urdf/103917.urdf) | Phone | Electronic Device | 0 | 19 | 20 | [JSON](descriptions/finaljson/103917.json) |
| [103925](descriptions/urdf/103925.urdf) | Phone | ElectronicDevice | 0 | 16 | 17 | [JSON](descriptions/finaljson/103925.json) |
| [103927](descriptions/urdf/103927.urdf) | Phone | Electronic Device | 0 | 7 | 8 | [JSON](descriptions/finaljson/103927.json) |
| [103935](descriptions/urdf/103935.urdf) | Phone | Communication Device | 0 | 18 | 19 | [JSON](descriptions/finaljson/103935.json) |
| [103941](descriptions/urdf/103941.urdf) | Remote Control | Electronic Device | 0 | 57 | 58 | [JSON](descriptions/finaljson/103941.json) |
| [103963](descriptions/urdf/103963.urdf) | Globe | Educational Instrument | 1 | 0 | 2 | [JSON](descriptions/finaljson/103963.json) |
| [103964](descriptions/urdf/103964.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/103964.json) |
| [103965](descriptions/urdf/103965.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/103965.json) |
| [103967](descriptions/urdf/103967.urdf) | Globe | Educational Model | 1 | 0 | 2 | [JSON](descriptions/finaljson/103967.json) |
| [103968](descriptions/urdf/103968.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/103968.json) |
| [103969](descriptions/urdf/103969.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/103969.json) |
| [103971](descriptions/urdf/103971.urdf) | Globe | Educational Tool | 1 | 0 | 2 | [JSON](descriptions/finaljson/103971.json) |
| [103972](descriptions/urdf/103972.urdf) | Printer | Office Equipment | 0 | 22 | 23 | [JSON](descriptions/finaljson/103972.json) |
| [103974](descriptions/urdf/103974.urdf) | Printer | ElectronicDevice | 0 | 1 | 3 | [JSON](descriptions/finaljson/103974.json) |
| [103978](descriptions/urdf/103978.urdf) | Printer | Office Equipment | 0 | 16 | 17 | [JSON](descriptions/finaljson/103978.json) |
| [103981](descriptions/urdf/103981.urdf) | Printer | Office Equipment | 0 | 5 | 6 | [JSON](descriptions/finaljson/103981.json) |
| [103988](descriptions/urdf/103988.urdf) | Printer | ElectronicDevice | 0 | 8 | 9 | [JSON](descriptions/finaljson/103988.json) |
| [103989](descriptions/urdf/103989.urdf) | Printer | Office Equipment | 0 | 7 | 9 | [JSON](descriptions/finaljson/103989.json) |
| [103990](descriptions/urdf/103990.urdf) | Globe | Educational Object | 1 | 0 | 2 | [JSON](descriptions/finaljson/103990.json) |
| [103996](descriptions/urdf/103996.urdf) | Printer | Office Equipment | 0 | 16 | 18 | [JSON](descriptions/finaljson/103996.json) |
| [104000](descriptions/urdf/104000.urdf) | Printer | Office Equipment | 1 | 19 | 22 | [JSON](descriptions/finaljson/104000.json) |
| [104004](descriptions/urdf/104004.urdf) | Printer | Office Equipment | 0 | 4 | 6 | [JSON](descriptions/finaljson/104004.json) |
| [104006](descriptions/urdf/104006.urdf) | Printer | Office Equipment | 0 | 4 | 6 | [JSON](descriptions/finaljson/104006.json) |
| [104007](descriptions/urdf/104007.urdf) | Printer | Office Equipment | 0 | 11 | 13 | [JSON](descriptions/finaljson/104007.json) |
| [104009](descriptions/urdf/104009.urdf) | Printer | Office Equipment | 0 | 9 | 11 | [JSON](descriptions/finaljson/104009.json) |
| [104011](descriptions/urdf/104011.urdf) | Printer | OfficeEquipment | 0 | 27 | 29 | [JSON](descriptions/finaljson/104011.json) |
| [104013](descriptions/urdf/104013.urdf) | Printer | ElectronicDevice | 0 | 6 | 9 | [JSON](descriptions/finaljson/104013.json) |
| [104016](descriptions/urdf/104016.urdf) | Printer | ElectronicDevice | 0 | 1 | 2 | [JSON](descriptions/finaljson/104016.json) |
| [104020](descriptions/urdf/104020.urdf) | Printer | ElectronicDevice | 0 | 9 | 10 | [JSON](descriptions/finaljson/104020.json) |
| [104027](descriptions/urdf/104027.urdf) | Printer | Office Equipment | 0 | 7 | 10 | [JSON](descriptions/finaljson/104027.json) |
| [104030](descriptions/urdf/104030.urdf) | Printer | ElectronicDevice | 0 | 8 | 10 | [JSON](descriptions/finaljson/104030.json) |
| [104036](descriptions/urdf/104036.urdf) | Remote Control | Electronic Device | 0 | 34 | 35 | [JSON](descriptions/finaljson/104036.json) |
| [104038](descriptions/urdf/104038.urdf) | Remote Control | Electronic Device | 0 | 51 | 52 | [JSON](descriptions/finaljson/104038.json) |
| [104039](descriptions/urdf/104039.urdf) | Remote Control | Electronic Device Accessory | 0 | 35 | 36 | [JSON](descriptions/finaljson/104039.json) |
| [104040](descriptions/urdf/104040.urdf) | Remote Control | Electronic Device Accessory | 0 | 25 | 26 | [JSON](descriptions/finaljson/104040.json) |
| [104041](descriptions/urdf/104041.urdf) | Remote | Electronic Control Device | 0 | 39 | 40 | [JSON](descriptions/finaljson/104041.json) |
| [104044](descriptions/urdf/104044.urdf) | Remote Control | Electronic Device | 0 | 47 | 48 | [JSON](descriptions/finaljson/104044.json) |
| [104045](descriptions/urdf/104045.urdf) | Remote Control | Electronic Device | 0 | 28 | 29 | [JSON](descriptions/finaljson/104045.json) |
