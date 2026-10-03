---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'dab0b024-d201-4254-b7fb-7f66263f564f'
  PropagateID: 'dab0b024-d201-4254-b7fb-7f66263f564f'
  ReservedCode1: 'e1e102aa-562d-4e3f-867d-99b8b9cf8dd9'
  ReservedCode2: 'e1e102aa-562d-4e3f-867d-99b8b9cf8dd9'
---

# JMS56x

JMicron JMS56x 系列 USB 3.0 → SATA 桥接芯片资料合集（ORICO 9528U3 硬盘盒实测），包含：

- 固件升级（刷写 / 恢复）
- UAS → BOT 模式切换驱动（x64）
- 官方量产工具（EEPROM / 休眠 / 序列号等修改）

## 目录结构

| 目录 | 说明 |
| --- | --- |
| `9528U3_固件/` | ORICO 9528U3（JMS551 主控）固件文件与升级步骤截图 |
| `JMS56x_BOT驱动_x64/` | JMS56x 全系列 UAS → BOT 覆盖驱动（Windows x64） |
| `JMS56x_量产工具/` | JMicron 2033x M.P. Tool v1.16.14.1 量产工具及配置 |

## 各部分说明

### 9528U3_固件

- `JMS551_Orico_v.0.31.4.23.2.BIN` — ORICO 9528U3（JMS551 主控）原厂固件
- `9528u3升级步骤1.jpg` / `9528u3升级步骤2.jpg`：固件升级操作界面截图

刷写固件需配合量产工具使用，勾选 `Firmware Update` 并加载本 BIN 文件即可。

### JMS56x_BOT驱动_x64

部分场景（老系统、数据恢复、部分工具软件）需要设备以 **BOT（Bulk-Only Transport）** 模式工作，而 JMS56x 默认以 **UAS** 模式加载。本驱动通过覆盖 INF 强制切换：

- 覆盖 `VID_152D` 下全部 JMS56x 常见 PID（0561 / 0562 / 0567 / 1561 / 2561 / 2566 / 2590 / 3562 / 3569 / 8561 / 9561 / 9562 / 9566 / 9567）
- 不引入任何新驱动 `.sys`，仅复用系统自带 `usbstor.sys`
- 安装后设备管理器显示 `JMicron JMS56x USB 3.0 to SATA Adapter (BOT Mode)`

**安装**：右键管理员运行 `install.bat`（自动将测试签名证书导入受信任根，并通过 `pnputil` 安装驱动包），完成后重新插拔设备即可生效。

**卸载**：右键管理员运行 `uninstall.bat`，重新插拔后恢复 UAS 模式。

> 说明：驱动为自签名测试证书，Windows 可能提示未知发布者，属正常现象。

### JMS56x_量产工具

JMicron 2033x M.P. Tool v1.16.14.1，用于：

- 固件升级（`Firmware Update`）
- EEPROM 修改（`EEPROM Update`）：VID/PID、厂商字符串、序列号、**休眠时间**等
- 分区 / 格式化 / 读写测试等量产流程

常用操作备忘：

1. 勾选 `RD Version`，输入口令 `jmicron` 解锁；
2. 需要改休眠时间时：勾选 `EEPROM Update`，将 `Standby Timer` 设为 `0` 即取消自动休眠（详见 `设定休眠时间方法.docx`）；
3. 点 `START` 执行，完成后 `Safe Remove` 并重新插拔。

`JMMassProd.ini` 为当前配置参考（EEPROM：VID `152D` / PID `9561`，Standby Timer `10` 分钟）。

## 免责声明

刷写固件、修改 EEPROM 存在变砖/损坏设备风险，请自行评估风险并做好备份；本仓库所有工具与固件均来自网络收集或个人备份，仅供学习研究使用。

> AI生成