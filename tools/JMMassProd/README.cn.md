# JMMassProd — JMicron 2033x M.P. Tool

JMicron USB-SATA 桥接芯片量产工具（JMS56x 系列）。

> **语言：** [English](README.md) · 简体中文

## 文件

| 文件 | 说明 |
| --- | --- |
| `JMMassProd2_v1_16_14_1.exe` | M.P. Tool v1.16.14.1 |
| `JMMassProd.ini` | 当前配置（参考） |
| `test.bin` | 读写测试载荷（`WriteFileName` 引用） |
| `log/JM2033x.log` | 工具的测试日志 |

## 常用操作

1. 连接设备后运行工具；
2. 勾选 `RD Version`，输入口令 `jmicron` 解锁；
3. 改休眠时间：勾选 `EEPROM Update`，将 `Standby Timer` 设为 `0` 即取消自动休眠（详见 `docs/设定休眠时间方法.docx`）；
4. 刷固件：勾选 `Firmware Update`，加载固件文件（见 `firmware/`）；
5. 点 `START` 执行，完成后 `Safe Remove` 并重新插拔。

## 当前配置（JMMassProd.ini）

- EEPROM：VID `152D` / PID `9561`，`Standby Timer = 10` 分钟
- `EnEEPROMUpdate=1`、`EnFWUpdate=1`
- 注意：`FwFileName` 仍指向旧路径（`D:\Library\Desktop\JMS56x\9528U3_固件\JMS551_Orico_v.0.31.4.23.2.BIN`），固件已迁移到 `firmware/`，刷写前请更新该行。