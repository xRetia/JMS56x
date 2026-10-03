# JMS56x 固件库（Firmware Collection）

JMicron JMS56x 系列 USB-SATA 桥接/RAID 控制器固件归档。统一命名、按芯片/盘位/功能编目。**全部文件为原始二进制，未做修改。**

> **语言：** [English](README.md) · 简体中文

## 章节

- [命名规则](#命名规则)
- [工具内嵌固件（Embedded）](#工具内嵌固件embedded)
- [版本号存储机制（fwUnknown 原因说明）](#版本号存储机制fwunknown-原因说明)
- [固件索引](#固件索引)
- [芯片谱系](#芯片谱系)
- [JMS578 变体索引（1-bay）](#jms578-变体索引1-bay)
- [刷写注意事项](#刷写注意事项)
- [分析依据](#分析依据)

## 命名规则

```
JMS{芯片型号}_fw{固件版本}_{N}-bay_{功能描述}_{来源/变体}_{发布日期}.bin
```

- **盘位**：`1-bay` 单盘桥接 / `2-bay` 双盘（RAID 或独立双盘）
- **功能**：`HW-RAID0-1-Large-JBOD` 硬件 RAID（RAID0 / RAID1 / LARGE / JBOD）；`UAS-Bridge` UAS 单盘桥接；`HDD-Clone` 离线整盘克隆；`BusPower-ODD-SSD` 总线供电+光驱+SSD 支持
- **来源**：`CE702` / `Coltech-CE702` / `ORICO-9528U3` / `AGESTAR` / `SSI` / `STD` / `ChipFlashDump`（芯片实测导出）/ `Embedded-*`（从刷写工具 exe 中提取，后缀 `slotA`/`slotB` 表示同一工具内相邻排列的多份镜像，按偏移顺序命名）

## 工具内嵌固件（Embedded）

刷写工具 exe 内嵌了出厂默认固件，按已知固件头特征定位提取，MD5 去重并对照独立固件全量比对后，共 **11 份独立新固件**（均与独立固件库无重复）：

| 文件 | 芯片 | 尺寸 | 提取自 | 偏移 | 说明 |
|---|---|---|---|---|---|
| `JMS561U_..._Embedded-FwUpdater561U_slotA.bin` | JMS561U | 256 KB | `FwUpdater561U_v1_0_2_0.exe` | 0x17B204 | JMS56x 完整 FlashDump 格式（C0 AE 头，含 197B:0562 默认 USB ID） |
| `JMS561U_..._Embedded-FwUpdater561U_slotB.bin` | JMS561U | 256 KB | 同上 | 0x1BB204 | 同格式第二槽 |
| `JMS561_fwBuild4012_..._MultiTool_slotA.bin` | JMS561 | 64 KB | 三个工具共用 | 0x1FAE04 等 | 头部标识 `JMicron JMS561.4012` |
| `JMS561_fwBuild4021_..._MultiTool_slotB.bin` | JMS561 | 64 KB | 同上 | — | 头部标识 `JMicron JMS561.4021` |
| `JMS578_..._Embedded-FwUpdateTool119_slotA.bin` | JMS578 | 49 KB | `FwUpdateTool_v1_19_16_24.exe` | 0x1257FC | 库内 20 个独立版本均无匹配，为新版本 |
| `JMS578_..._Embedded-FwUpdateTool119_slotB.bin` | JMS578 | 49 KB | 同上 | 0x131BFC | 同上 |
| `JMS578_..._Embedded-JMS567Tool100_slotA.bin` | JMS578 | 49 KB | `JMS567FwUpdateTool_v1_0_0_0.exe` | 0x19DA48 | 同上 |
| `JMS578_..._Embedded-JMS567Tool100_slotB.bin` | JMS578 | 49 KB | 同上 | 0x1A9E48 | 同上 |
| `JMS567_..._Embedded-JMS567Tool1bay_slotA.bin` | JMS567 | 48 KB | `JMS567FwUpdateTool_1-bay_v01.exe` | 0x96BB4 | 压缩格式（12 42 00 D3 22 头） |
| `JMS567_..._Embedded-JMS567Tool1bay_slotB.bin` | JMS567 | 48 KB | 同上 | 0xA2DB4 | 同上 |
| `JMS567_..._Embedded-JMS567Tool100_slotA.bin` | JMS567 | 48 KB | `JMS567FwUpdateTool_v1_0_0_0.exe` | 0x131848 | 同上 |

提取说明：

- `JMS561` 64 KB 双槽在三个工具（FwUpdater561U / FwUpdateTool v1.19 / JMS567FwUpdateTool v1.0.0.0）中重复嵌入同一对镜像，故来源标 `MultiTool`
- `JMS567FwUpdateTool_v1_0_0_0.exe` 与 `JMS567_FwUpdateTool_v1_0_0_0.exe`（两个文件 MD5 不同）内嵌固件区完全一致，只提取一份
- 嵌入版 JMS578 为 50176 B（发布版 50688 B 少 512 B 尾块），版本头字段为 `04 04 04 04`（独立版为 `03 03 05 05`）
- 固件内无明文版本号，`fwUnknown` 标记的版本见下方「版本号存储机制」，均经排查确认无法离线读取，非未尝试

## 版本号存储机制（fwUnknown 原因说明）

对全部固件版本字段的定位结论（2026-10-03，以已知版本样本交叉验证）：

| 芯片 | 版本存储方式 | 离线可读? | 结论 |
|---|---|---|---|
| JMS561/561B | 固件头 @0x19 存 4 字节大端版本（`6B 01 00 03` = v107.001.000.003），@0x5F0 有副本；256 KB 文件为**双 bank 镜像**（0x20000 处重复完整拷贝，版本标记同步出现在 0x20019/0x205F0） | 可读且已验证 | 库内 2 份版本号与头部字段完全吻合 |
| JMS561 嵌入 64K | 版本位为 ASCII build 号（`4012`/`4021`） | 已读取 | 已用 fwBuild 标记 |
| JMS567 | **版本仅存于发布文件名**，固件内无版本字段；压缩格式；@0xBFF2 处 16 位值为逐版不同的校验特征（v142→88 E6，SSI→12 2F，STD→26 3A），可区分版本但读不出号 | 不可 | 嵌入 3 份 + FullDump 1 份保持 Unknown |
| JMS578 | **版本仅存于发布文件名**；尾部 512 B 为 EEPROM 出厂模板（152D:0578 + 产品串 + SN 模板），不含版本；头部平台标识 `JMS579.0103` 各版相同 | 不可 | 嵌入 4 份保持 Unknown |
| JMS561U / JMS565 FlashDump | 版本号由芯片运行时经工具 `RD Version` 命令返回，静态镜像中不存在 | 不可（需接芯实读） | JMS565 的 105.03.01.02 即实机所读；561U 两槽保持 Unknown |

附带发现：工具 exe 内亦无有效版本串（正文搜索 `NN.NN.NN.NN` 仅命中 ASCII 误匹配），故内嵌固件版本无法从宿主工具离线获取。

## 固件索引

| 文件 | 芯片 | 盘位 | 功能 | 固件版本 | 尺寸 | 来源 |
|---|---|---|---|---|---|---|
| `JMS551_fw18.0.2.23.2_2-bay_HDD-Clone-LED_AGESTAR.bin` | JMS551 | 2-bay | 离线克隆（带 LED） | 18.0.2.23.2 | 50 KB | AGESTAR 拷贝机 |
| `JMS551_fw255.0.6.0.7_2-bay_Full-Function_AGESTAR.bin` | JMS551 | 2-bay | 全功能（RAID0 / JBOD / Clone） | 255.0.6.0.7 | 64 KB | AGESTAR |
| `JMS551_fw0.31.4.23.2_2-bay_Dual-Disk-Basic_ORICO-9528U3.bin` | JMS551 | 2-bay | 双盘独立，无 RAID | 0.31.4.23.2 | 50 KB | ORICO 9528U3（老批次） |
| `JMS561_fw107.001.000.003_1-bay_UAS-Bridge_CE702_20180706.bin` | JMS561 | 1-bay | UAS 单盘桥接 | 107.001.000.003 | 256 KB | CE702，2018-07-06 |
| `JMS561B_fw107.01.00.04_1-bay_UAS-Bridge_Coltech-CE702_20240830.bin` | JMS561B | 1-bay | UAS 单盘桥接 | 107.01.00.04 | 256 KB | Coltech CE702，2024-08-30 |
| `JMS565_fw105.03.01.02_2-bay_HW-RAID0-1-Large-JBOD_ChipFlashDump.bin` | JMS565 | 2-bay | 硬件 RAID0/1/Large/JBOD | 105.03.01.02 | 512 KB | 本机芯片实测导出 |
| `JMS567_fw142.02.00.01_2-bay_HW-RAID0-1-Large-JBOD_CE-704U3_20240509.bin` | JMS567 | 2-bay | 硬件 RAID0/1/Large/JBOD | 142.02.00.01 | 48 KB | CE-704U3，2024-05-09 |
| `JMS567_fwUnknown_2-bay_HW-RAID0-1-Large-JBOD_FullDump.bin` | JMS567 | 2-bay | 硬件 RAID0/1/Large/JBOD | 未知 | 64 KB | 完整镜像 |
| `JMS567_fw20.06.00.01_2-bay_HW-RAID0-1-Large-JBOD_SSI.bin` | JMS567 | 2-bay | 硬件 RAID0/1/Large/JBOD | 20.06.00.01 | 48 KB | SSI 定制 |
| `JMS567_fw00.01.01.07_2-bay_HW-RAID0-1-Large-JBOD_STD.bin` | JMS567 | 2-bay | 硬件 RAID0/1/Large/JBOD | 00.01.01.07 | 48 KB | 标准版 |
| `JMS578_fw00.04.00.09_1-bay_BusPower-ODD-SSD_STD.bin` | JMS578 | 1-bay | 总线供电 / 光驱 / SSD | 00.04.00.09 | 50 KB | 标准版 |

## 芯片谱系

### JMS551（老一代 USB 3.0 双盘）
- USB 设备 ID：**VID 152D : PID 0551**（写在固件头部）
- 用于早期 2-bay 产品：硬盘拷贝机（AGESTAR Clone/Full-Function）、ORICO 9528U3 老批次（双盘独立、无 RAID）
- Full-Function 版固件内含 `RAID0` / `JBOD` 字符串

### JMS561 / JMS561B（单盘 UAS 桥）
- 固件头部自带 ASCII 型号标识 `0561`，内部默认 USB 设备 ID：**197B:0562**（JMS56x 家族共用默认值）
- 固件与 JMS565 同属 `JMS H/W RAID` 软件平台，按单盘桥应用
- 256 KB 发布固件为双 bank 镜像（0x0 与 0x20000 各一份）；版本号存于头部 @0x19（二进制单段大端，CE702 两版均验证吻合）；工具内嵌另有 64 KB 短版（ASCII build 4012/4021）
- **JMS561U**：561 的 USB 直连变体，工具内嵌 256 KB FlashDump 双槽（配套 `FwUpdater561U_v1_0_2_0.exe`，ini 标注 561Series VID 1058 / PID 0A10）

### JMS565（双盘硬件 RAID）— 本机 9528U3 实测芯片
- 官方 JM203x FW Update Utility 识别：**JMS565 Series**，固件版本 **105.03.01.02**，Flash：MXIC/KH
- `ChipFlashDump` 版为 512 KB 完整 SPI Flash 备份（工具勾选 Backup Old Firmware 导出），**含配置区，非纯净发布固件**
- 固件内含 `JMS56X H/W RAID`、`RAID0RAID1LARGE` 及 RAID0/RAID1/JBOD/LARGE 模式表
- 与 JMS561 同软件平台的 2-bay RAID 变体；与 JMS562（官方定义 USB3.0+eSATA→双 SATA RAID）为近亲
- 应用：ORICO 9528U3 双盘基础款（非 RAID 模式运行）；芯片具备 HW-RAID 能力但基础款未开放

### JMS567（双盘硬件 RAID）
- USB 设备 ID：**152D:0567**（固件 @0xC000）
- ORICO 9528RU3 阵列款采用 JMS567 + JMS575 双芯片方案
- 固件为压缩格式（头部 `12 42 00 D3 22`），字符串不可直读
- 4 个独立变体（STD / SSI / CE-704U3 2024 / 未知版本完整镜像）+ 3 份工具内嵌版（1-bay 工具双槽 + v1.0.0.0 工具单槽）

### JMS578（单盘多功能桥）
- USB 设备 ID：**152D:0578**（固件尾块 EEPROM 模板头部）
- 内部平台标识 **JMS579.0103**（各版本固件头部相同）；尾部 512 B 为 EEPROM 出厂模板，嵌入版不含此尾块
- 支持总线供电（Bus Power）/ 自供电（Self Power）/ 光驱（ODD）/ SSD
- 本库收录 20 个独立变体 + 4 份工具内嵌版（版本仅存于发布文件名，见「版本号存储机制」）；**PPE（PowerPlus）版禁用 HDD 自动停转**，适合 Wii/PS2 长时挂机（配套 `JMS578_fw124.01.00.02_1-bay_PPE-NoSpinDown_Guide.txt` 为原始说明，含刷写步骤与参考论坛）
- `Hardkernel` 版用于 ODROID 等开发板；`NVRAM` 版含 557 NVRAM 配置区

## JMS578 变体索引（1-bay）

| 文件 | 功能特征 | 固件版本 | 备注 |
|---|---|---|---|
| `JMS578_fw0.1.0.5_1-bay_Bridge_EarlyVersion.bin` | 基础桥接 | 0.1.0.5 | 早期版本 |
| `JMS578_fw00.01.00.03_1-bay_SelfPower_STD.bin` | 自供电 | 00.01.00.03 | STD |
| `JMS578_fw00.02.00.02_1-bay_BusPower_STD.bin` | 总线供电 | 00.02.00.02 | STD |
| `JMS578_fw00.02.00.03_1-bay_BusPower_STD.bin` | 总线供电 | 00.02.00.03 | STD |
| `JMS578_fw00.04.00.05_1-bay_BusPower-ODD_STD_20170324.bin` | 总线供电+光驱 | 00.04.00.05 | 2017-03-24 |
| `JMS578_fw00.04.00.07_1-bay_STD_OriginalCaseBackup.bin` | 原盒备份 | 00.04.00.07 | 出厂原固件备份 |
| `JMS578_fw00.04.00.09_1-bay_BusPower-ODD-SSD_STD.bin` | 总线供电+光驱+SSD | 00.04.00.09 | STD（主索引） |
| `JMS578_fw00.04.01.04_1-bay_SelfPower-ODD_STD.bin` | 自供电+光驱 | 00.04.01.04 | STD |
| `JMS578_fw46.01.00.01_1-bay_NVRAM-Config.bin` | 含 NVRAM 配置 | 46.01.00.01 | 含 557 NVRAM |
| `JMS578_fw68.01.00.02_1-bay_Bridge_Beihuan.bin` | 基础桥接 | 68.01.00.02 | Beihuan 定制 |
| `JMS578_fw108.01.00.01_1-bay_BusPower-PowerPlus.bin` | 总线供电+PowerPlus | 108.01.00.01 | 电源管理修正 |
| `JMS578_fw124.01.00.02_1-bay_PPE-NoSpinDown.bin` | PPE 禁停转 | 124.01.00.02 | Wii/PS2 推荐，见 Guide.txt |
| `JMS578_fw173.01.00.01_1-bay_Bridge_Hardkernel_ODROID.bin` | 基础桥接 | 173.01.00.01 | ODROID 社区 |
| `JMS578_fw173.01.00.02_1-bay_Bridge_Hardkernel_20190306.bin` | 基础桥接 | 173.01.00.02 | 2019-03-06 |
| `JMS578_fw255.01.00.01-beta_1-bay_Generic.bin` | beta | 255.01.00.01 | 通用 beta |
| `JMS578_fw255.01.00.01-beta_1-bay_ACASIS.bin` | beta | 255.01.00.01 | ACASIS（阿卡西斯） |
| `JMS578_fw255.01.00.01-beta_1-bay_ACASIS-B.bin` | beta | 255.01.00.01 | ACASIS B 版 |
| `JMS578_fw255.01.00.01-beta_1-bay_HTS.bin` | beta | 255.01.00.01 | HTS |
| `JMS578_fw255.01.00.01-beta_1-bay_KESU.bin` | beta | 255.01.00.01 | KESU |
| `JMS578_fw255.01.00.01-beta_1-bay_HGST-G-DRIVE.bin` | beta | 255.01.00.01 | HGST G-DRIVE 移动盘 |

## 刷写注意事项

1. **`JMS565_..._ChipFlashDump.bin` 是完整 Flash 备份**，包含 USB 描述符、SN、配置区，跨设备刷写可能导致 VID/PID/SN 被覆盖，务必先备份目标芯片原固件
2. 49 KB 级（JMS567 / JMS578 / JMS551）为**发布固件包**（仅代码区），不含配置区
3. 256 KB（JMS561）与 512 KB（JMS565 dump）镜像布局不同，刷写工具选错 Flash 布局会变砖
4. 配套工具：`FwUpdater561U_v1_0_2_0.exe`（JMS561U）、`JMS567FwUpdateTool_*.exe`、`FwUpdateTool_v1_19_16_24.exe`（JMS578 刷写）、`tools/JMMassProd/JMMassProd2_v1_16_14_1.exe`
5. ORICO 9528U3 升级步骤图解见 `docs/9528u3升级步骤1.jpg / 9528u3升级步骤2.jpg`
6. JMS578 PPE 版刷写要点（详见 `JMS578_fw124.01.00.02_1-bay_PPE-NoSpinDown_Guide.txt`）：必须接硬盘才能读写固件；刷写前勾选 `RD Version` 与 `Including JM557 NVRAM`；先备份原厂固件

## 分析依据

以上结论来自对本目录全部固件的二进制分析（2026-10-03）：USB 设备描述符提取、字符串指纹对比、头部结构比对；JMS565 身份由 JMicron 官方 JM2033x FW Update Utility 实机识别确认。工具内嵌固件于同日按特征定位提取，MD5 去重并独立固件全量对比后入库。