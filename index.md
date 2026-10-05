---
layout: default
title: JMS56x — JMicron Bridge Chip Archive
lang: en
---

<div style="position:absolute;top:8px;right:16px;font-size:14px">
  <a href="index.cn.html">中文</a>
</div>

# JMS56x

JMicron JMS56x family USB 3.0 → SATA bridge chip resource archive, verified on an ORICO 9528U3 enclosure. Firmware, a UAS → BOT override driver, official mass production tools, documents, and in-depth firmware analysis.

---

## Sections

| Section | Description |
| --- | --- |
| [🔍 Analysis](#analysis) | Firmware analysis reports, disassembly, pseudo-C |
| [💾 Firmware](#firmware) | 41 binaries — JMS551 / 561 / 561B / 561U / 565 / 567 / 578 |
| [🔌 BOT Driver](#bot-driver) | UAS → BOT override driver (Windows x64) |
| [🛠️ Tools](#tools) | JMMassProd M.P. Tool & FwUpdateTool |
| [📄 Docs](#docs) | 9528U3 upgrade steps, standby timer how-to |

---

## Analysis

JMS565 firmware (version 105.03.01.02) reverse-engineering: 8051 architecture, BOT/UAS dual-protocol, SCSI command support live testing, power management (StandbyTimer / go_suspend / VBUS recovery), safe removal, SAT pass-through defects.

### Reports

| Document | Description |
| --- | --- |
| [📋 Full Analysis Report](analysis/JMS565_firmware_analysis_en.md) | Architecture / UAS / SCSI / Power / Safe Removal |
| [🔧 Static Analysis Materials](analysis/JMS565_static_analysis_en.md) | Disassembly / Control Flow / Pseudo-C |
| [📝 Preliminary Analysis](analysis/JMS565_analysis_cn.md) | Early VBUS / suspend path analysis |

### Attachments

| File | Description |
| --- | --- |
| [Linear disassembly (37,005 lines)](analysis/JMS565_full_linear_disassembly.lst) | Byte-by-byte disassembly of code region |
| [Reachable disassembly (612 insns)](analysis/JMS565_reachable_disassembly.lst) | From reset / interrupt vectors |
| [Control flow summary](analysis/JMS565_control_flow_summary.txt) | Call graph / zero-span targets / strings |
| [Pseudo-C](analysis/JMS565_pseudocode.c) | Reset / VBUS / suspend / StandbyTimer |
| [Disassembly script](analysis/disasm8051.py) | Local 8051 disassembler |

---

## Firmware

41 firmware binaries covering JMS551 / 561 / 561B / 561U / 565 / 567 / 578, unified naming, cataloged by chip / bay / feature.

| Link | Description |
| --- | --- |
| [📦 Firmware Index](firmware/README.md) | Naming scheme, chip lineage, version notes |

---

## BOT Driver

UAS → BOT override driver (Windows x64, self-signed). Adds no new `.sys` — uses the system built-in `usbstor.sys`.

| Link | Description |
| --- | --- |
| [🔌 Driver README](driver/README.md) | Installation, supported PIDs, technical details |

---

## Tools

JMicron official mass production and firmware update utilities.

| Link | Description |
| --- | --- |
| [🛠️ Tools](tools/README.md) | JMMassProd & FwUpdateTool overview |
| [JMMassProd](tools/JMMassProd/README.md) | M.P. Tool — EEPROM / VID / PID / standby timer |
| [FwUpdateTool](tools/FwUpdateTool/README.md) | Firmware update / backup utility |

---

## Docs

ORICO 9528U3 upgrade screenshots and standby-timer how-to.

| Link | Description |
| --- | --- |
| [📄 Docs](docs/README.md) | Upgrade steps, standby-timer how-to |

---

## Safety

Flashing firmware or modifying EEPROM carries a real brick risk — always back up the original firmware first. All materials come from web collection and personal backups, for research and study only.
