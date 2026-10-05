# JMS56x

JMicron JMS56x 系列 USB 3.0 → SATA 桥接芯片资料合集（ORICO 9528U3 硬盘盒实测），包含：

- **固件** — 刷写 / 更新用固件
- **BOT 驱动** — UAS → BOT 模式切换驱动（Windows x64）
- **量产工具** — EEPROM / VID / PID / 休眠时间 / 序列号修改
- **文档** — 升级步骤截图、休眠时间设定方法

> **语言：** [English](README.md) · 简体中文

## 目录结构

| 目录 | 说明 |
| --- | --- |
| [`analysis/`](analysis/) | JMS565 固件完整分析报告（架构 / UAS / SCSI 命令支持度 / 电源管理 / 安全删除） |
| [`docs/`](docs/) | ORICO 9528U3 升级步骤截图、休眠时间设定方法文档 |
| [`driver/`](driver/) | JMS56x 全系列 UAS → BOT 覆盖驱动（自包含，不引入新 `.sys`） |
| [`firmware/`](firmware/) | JMS56x 系列固件库 — 41 个二进制、统一命名、芯片谱系与版本说明 |
| [`tools/`](tools/) | JMicron 量产工具（JMMassProd）与固件升级工具（FwUpdateTool） |

每个目录都带有 `README.md`（英文）与 `README.cn.md`（中文）双版本，英文文件中链接到中文文件。

## 快速开始

- **UAS → BOT 切换**：右键 `driver/install.bat` 管理员运行（或双击，脚本自动提权），完成后重新插拔设备。卸载用 `driver/uninstall.bat`。
- **查找固件**：见 [固件索引](firmware/README.cn.md)。
- **固件分析**：见 [JMS565 固件完整分析报告](analysis/JMS565_firmware_analysis_zh.md)；静态反汇编与伪 C 还原见 [静态分析资料](analysis/JMS565_static_analysis_zh.md)。
- **修改 VID / PID / 休眠时间**：用 [`tools/JMMassProd/`](tools/JMMassProd/README.cn.md) 中的 M.P. Tool，勾选 `EEPROM Update`，`Standby Timer` 设为 `0` 即取消自动休眠。

## 免责声明

刷写固件、修改 EEPROM 存在变砖/损坏设备风险，请先备份原固件并自行评估风险。本仓库所有工具与固件均来自网络收集或个人备份，仅供学习研究使用。