---
layout: default
title: JMS56x — JMicron 桥接芯片资料库
lang: cn
---

# JMS56x

JMicron JMS56x 系列 USB 3.0 → SATA 桥接芯片资料合集（ORICO 9528U3 硬盘盒实测）：固件、UAS → BOT 切换驱动、量产工具，以及深度固件逆向分析。

[**English**](/JMS56x/)

---

## 最新文章

{% for post in site.posts %}
{% if post.lang == "cn" %}
**[{{ post.date | date: "%Y-%m-%d" }}]({{ post.url | relative_url }}) — {{ post.title }}**

{% for tag in post.tags %}`{{ tag }}` {% endfor %}

{% endif %}
{% endfor %}

---

## 目录

| 章节 | 说明 |
|---|---|
| **[💾 固件库](https://github.com/xRetia/JMS56x/tree/main/firmware)** | 41 个二进制 — JMS551 / 561 / 561B / 561U / 565 / 567 / 578 |
| **[🔌 BOT 驱动](https://github.com/xRetia/JMS56x/tree/main/driver)** | UAS → BOT 覆盖驱动（Windows x64） |
| **[🛠️ 量产工具](https://github.com/xRetia/JMS56x/tree/main/tools)** | JMMassProd 量产工具 & FwUpdateTool |
| **[📄 文档](https://github.com/xRetia/JMS56x/tree/main/docs)** | 升级步骤截图、休眠时间设定方法 |
| **[🔍 固件分析](https://github.com/xRetia/JMS56x/tree/main/analysis)** | 反汇编、伪 C、SCSI 实测、电源管理分析 |

---

## 关键发现

- **架构** — 8051 内核（CISC），双层代码空间（外部 Flash + 内部 mask ROM）
- **UAS** — 固件支持 BOT+UAS 双协议，无固件级 UAS 开关
- **SCSI** — 16 项命令确认支持；TRIM 不透传
- **SAT 缺陷** — SMART Return Status 寄存器缺失
- **电源管理** — StandbyTimer=0 解决关机一晚后 VBUS 恢复失败
- **安全删除** — CM API 正常；右键无弹出选项（RMB=0）
- **UAS 掉盘** — 根因在 USB 传输层，非 SCSI 命令层

---

*本站资料仅供学习研究使用。刷写固件有变砖风险，请先备份。*
