# FwUpdateTool — JM203x FW Update Utility

JMicron 桥接芯片固件升级工具。

> **语言：** [English](README.md) · 简体中文

## 文件

| 文件 | 说明 |
| --- | --- |
| `FwUpdateTool_v1_19_16_24.exe` | 工具本体（JM203x FW Update Utility） |
| `FwUpdateTool.ini` | 配置：561Series VID/PID（`VID = 1058 : PID = 0A10`）、序列号模板、复位缓冲 |

## 说明

- 该工具用于刷写 JMS578 系列固件（如 PPE 版，见 `firmware/JMS578_fw124.01.00.02_1-bay_PPE-NoSpinDown_Guide.txt`）——必须接硬盘后才能读写固件。
- 本机芯片即由该工具识别为 **JMS565 Series**（固件 `105.03.01.02`，Flash `MXIC/KH`）。
- 刷写前务必先备份原固件（`Backup Old Firmware`）；刷 PPE 版时还需勾选 **RD Version** 与 **Including JM557 NVRAM**。