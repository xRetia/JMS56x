---
layout: default
title: JMS56x — JMicron Bridge Chip Archive
lang: en
---

# JMS56x

JMicron JMS56x family USB 3.0 → SATA bridge chip resource archive, verified on an ORICO 9528U3 enclosure. Firmware, UAS → BOT override driver, mass production tools, and in-depth firmware reverse-engineering.

**[中文](index.cn.html)**

---

## Latest Posts

<ul>
{% for post in site.posts %}
{% if post.lang != "cn" %}
<li><time>{{ post.date | date: "%Y-%m-%d" }}</time> — <a href="{{ post.url }}">{{ post.title }}</a><br>
{% for tag in post.tags %}<code>{{ tag }}</code> {% endfor %}</li>
{% endif %}
{% endfor %}
</ul>

---

## Sections

| | |
|---|---|
| **[💾 Firmware](https://github.com/xRetia/JMS56x/tree/main/firmware)** | 41 binaries — JMS551 / 561 / 561B / 561U / 565 / 567 / 578 |
| **[🔌 BOT Driver](https://github.com/xRetia/JMS56x/tree/main/driver)** | UAS → BOT override driver (Windows x64) |
| **[🛠️ Tools](https://github.com/xRetia/JMS56x/tree/main/tools)** | JMMassProd M.P. Tool & FwUpdateTool |
| **[📄 Docs](https://github.com/xRetia/JMS56x/tree/main/docs)** | Upgrade screenshots, standby-timer how-to |
| **[🔍 Analysis](https://github.com/xRetia/JMS56x/tree/main/analysis)** | Disassembly, pseudo-C, SCSI testing, power management |

---

## Key Findings

- **Architecture**: 8051 core (CISC), dual code space (external Flash + internal mask ROM)
- **UAS**: Full BOT+UAS dual-protocol, no firmware-level disable switch
- **SCSI**: 16 commands confirmed; TRIM not passed through
- **SAT defect**: SMART Return Status registers missing
- **Power**: StandbyTimer=0 fixes overnight VBUS-recovery failure
- **Safe removal**: CM API works; right-click eject missing (RMB=0)
- **UAS drops**: Root cause in USB transport layer, not SCSI commands

---

*All materials are for research and study only. Flashing carries brick risk — back up first.*
