---
layout: default
title: JMS56x — JMicron 桥接芯片资料库
lang: cn
---

<div style="position:absolute;top:8px;right:16px;font-size:14px">
  <a href="index.html">English</a>
</div>

# JMS56x

JMicron JMS56x 系列 USB 3.0 → SATA 桥接芯片资料合集（ORICO 9528U3 硬盘盒实测）：固件、UAS → BOT 切换驱动、官方量产工具、配套文档，以及深度固件分析。

---

## 目录

| 章节 | 说明 |
| --- | --- |
| [🔍 固件分析](#固件分析) | 反汇编报告、伪 C 还原、SCSI 实测 |
| [💾 固件库](#固件库) | 41 个二进制 — JMS551 / 561 / 561B / 561U / 565 / 567 / 578 |
| [🔌 BOT 驱动](#bot-驱动) | UAS → BOT 覆盖驱动（Windows x64） |
| [🛠️ 量产工具](#量产工具) | JMMassProd 量产工具与 FwUpdateTool |
| [📄 文档](#文档) | 9528U3 升级步骤、休眠时间设定方法 |

---

## 固件分析

JMS565 固件（版本 105.03.01.02）的完整逆向分析：8051 架构、BOT/UAS 双协议、SCSI 命令支持度实测、电源管理（StandbyTimer / go_suspend / VBUS 恢复）、安全删除、SAT 透传缺陷。

### 报告

| 文档 | 说明 |
| --- | --- |
| [📋 完整分析报告](analysis/JMS565_firmware_analysis_cn.md) | 架构 / UAS / SCSI / 电源管理 / 安全删除 |
| [🔧 静态分析资料](analysis/JMS565_static_analysis_cn.md) | 反汇编方法 / 控制流 / 伪 C 还原 |
| [📝 早期初步分析](analysis/JMS565_analysis_cn.md) | VBUS / suspend 路径初步分析 |

### 附件

| 文件 | 说明 |
| --- | --- |
| [线性反汇编（37 005 行）](analysis/JMS565_full_linear_disassembly.lst) | 代码区逐字节反汇编 |
| [可达反汇编（612 条）](analysis/JMS565_reachable_disassembly.lst) | 从 reset / 中断向量出发 |
| [控制流摘要](analysis/JMS565_control_flow_summary.txt) | 调用关系 / 零区目标 / 字符串表 |
| [伪 C 代码](analysis/JMS565_pseudocode.c) | reset / VBUS / suspend / StandbyTimer |
| [反汇编脚本](analysis/disasm8051.py) | 本地 8051 反汇编工具 |

---

## 固件库

41 个固件二进制，覆盖 JMS551 / 561 / 561B / 561U / 565 / 567 / 578，统一命名，按芯片 / 盘位 / 功能编目。

| 链接 | 说明 |
| --- | --- |
| [📦 固件索引](firmware/README.cn.md) | 命名规则、芯片谱系、版本说明 |

---

## BOT 驱动

UAS → BOT 覆盖驱动（Windows x64，自签名），不引入新 `.sys`，仅用系统自带 `usbstor.sys`。

| 链接 | 说明 |
| --- | --- |
| [🔌 驱动说明](driver/README.cn.md) | 安装方法、支持 PID、技术细节 |

---

## 量产工具

JMicron 官方量产工具与固件升级工具。

| 链接 | 说明 |
| --- | --- |
| [🛠️ 工具说明](tools/README.cn.md) | 量产工具与固件升级工具 |
| [JMMassProd](tools/JMMassProd/README.cn.md) | 量产工具 — EEPROM / VID / PID / 休眠时间 |
| [FwUpdateTool](tools/FwUpdateTool/README.cn.md) | 固件升级 / 备份工具 |

---

## 文档

ORICO 9528U3 升级步骤截图、休眠时间设定方法。

| 链接 | 说明 |
| --- | --- |
| [📄 文档说明](docs/README.cn.md) | 升级步骤截图、休眠时间设定方法 |

---

## 免责声明

刷写固件、修改 EEPROM 存在变砖风险，请务必先备份原固件。本站资料来自网络收集与个人备份，仅供学习研究使用。
