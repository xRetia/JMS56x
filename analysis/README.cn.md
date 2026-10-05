---
layout: default
title: JMS565 固件分析
nav: true
---

# analysis — JMS565 固件分析（Firmware Analysis）

JMS565 固件（版本 105.03.01.02）的静态反汇编、伪 C 还原、SCSI 命令支持度实测、电源管理与安全删除分析。

> **语言：** [English](README.md) · 简体中文

## 报告

| 文件 | 说明 |
| --- | --- |
| [`JMS565_firmware_analysis_cn.md`](JMS565_firmware_analysis_cn.md) | 完整分析报告（架构 / UAS / SCSI / 电源管理 / 安全删除） |
| [`JMS565_static_analysis_cn.md`](JMS565_static_analysis_cn.md) | 静态分析资料（反汇编方法 / 控制流 / 伪 C 还原） |
| [`JMS565_analysis_cn.md`](JMS565_analysis_cn.md) | 早期初步静态分析（VBUS / suspend 路径） |

## 附件

| 文件 | 说明 |
| --- | --- |
| [`JMS565_full_linear_disassembly.lst`](JMS565_full_linear_disassembly.lst) | 代码区逐字节线性反汇编（37 005 行） |
| [`JMS565_reachable_disassembly.lst`](JMS565_reachable_disassembly.lst) | 从 reset / 中断向量出发的可达反汇编（612 条） |
| [`JMS565_control_flow_summary.txt`](JMS565_control_flow_summary.txt) | 调用关系、零区目标、字符串表 |
| [`JMS565_pseudocode.c`](JMS565_pseudocode.c) | 关键路径伪 C（reset / VBUS / suspend / StandbyTimer） |
| [`disasm8051.py`](disasm8051.py) | 本地 8051 反汇编脚本 |

## 复现

```bash
# 用 dis8051 v1.2 交互式导出
dis8051_x64.exe jms565_bank1.bin

# 用本地脚本生成所有附件
python disasm8051.py --input firmware.bin --outdir analysis/ --file-base 0x10000 --code-size 0xE000
```
