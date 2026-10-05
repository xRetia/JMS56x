---
layout: default
title: "JMS565 Firmware Analysis: Architecture, UAS, SCSI, Power Management"
date: 2026-10-05
author: xRetia
lang: en
tags: [firmware, 8051, UAS, SCSI, power-management]
---

> 中文版: [/posts/2026/10/05/firmware-analysis-cn.html]({/posts/2026/10/05/firmware-analysis-cn.html})

﻿---
layout: default
title: JMS565 Firmware Analysis Report
nav: true
---

# JMS565 Firmware Analysis Report

> **Languages:** English · [简体中文](JMS565_firmware_analysis_cn.md)

## Test Environment

| Item | Value |
|---|---|
| Chip | JMicron JMS565 (2-bay HW-RAID variant) |
| Firmware | 105.03.01.02 (RAID0 / RAID1 / Large / JBOD) |
| Enclosure | ORICO 9528U3 |
| Drive | TOSHIBA DT01ACA100 1TB (7200 rpm, SATA 3.0) |
| Code analysis | dis8051 v1.2 full disassembly (13,928 lines) |
| Live test tool | smartctl 8.0-585 (read-only, uninstalled after testing) |
| Test date | 2026-10-05 |

---

## 1. Firmware Architecture

### Processor: 8051 core (CISC), not RISC

The code region is saturated with MCS-51/8051 signatures: `90 xx` (MOV DPTR), `E0`/`F5` (MOVX r/w), `12 xx xx` (LCALL), `02 xx xx` (LJMP), `22` (RET), `74 xx` (MOV A,#imm). In a 4 KB code block: `0x90`=191, `0xE0`=160, `0x12`=81 occurrences.

### Two-layer code space

| Region | File offset | 8051 addr | Content | Dumpable |
|---|---|---|---|---|
| bank0 config/descriptors | 0x00000-0x01FF | — | RAID mode table, VID/PID, product strings | ✓ |
| bank1 code | 0x10000-0x1DBFF | 0x0000-0xDBFF | Application firmware (~56 KB) | ✓ |
| Internal mask ROM | — | 0xDC00-0xFFFF | Factory-baked library functions | ✗ |
| High padding | 0x1FC00-0x7FFFF | — | All 0x00 | ✓ |

**Key**: 576 `LCALL`/`LJMP` instructions target 0xDC00-0xFC00 — these are calls into the chip's internal mask ROM (delay, SATA command send, PHY reinit, etc.), not NOP slides. This code is invisible in external Flash dumps.

### Bank switching

Bank switching via registers `0x7E08` / `0x7E10` / `0x7E21` (109 accesses). bank1 starts with `02 80 16` = `LJMP 0x8016`, the real reset vector.

---

## 2. USB Descriptors & UAS Support

### Descriptor structure (identical across JMS561 / 561B / 561U)

| Item | Content |
|---|---|
| Interface | alt0 = BOT (`08 06 50`), alt1 = UAS (`08 06 62`), 4 endpoints |
| UAS pipe descriptors | `04 24 01/02/03/04`, endpoint directions per UAS spec |
| MPS | USB3.0=1024, USB2.0=512, USB1.1=64 |
| String | `MSC BOT/UAS Transfer` |

**Conclusion**: Firmware has full BOT + UAS dual-protocol support via USB alternate setting. Which protocol is used is decided by host enumeration; there is no firmware-level "disable UAS" switch.

---

## 3. SCSI Command Support

### Combined code-analysis + live-test table

| opcode | Command | Code analysis | BOT live | UAS live | Verdict |
|---|---|---|---|---|---|
| 0x00 | TEST UNIT READY | Dispatch (21 hits) | ✓ PASSED | ✓ PASSED | ✓ Both modes |
| 0x03 | REQUEST SENSE | Dispatch→SATA | ✓ OK | ✓ OK | ✓ Both modes |
| 0x08 | READ(6) | Dispatch (8 hits) | ✓ | ✓ | ✓ Both modes |
| 0x0A | WRITE(6) | Dispatch (6 hits) | ✓ | ✓ | ✓ Both modes |
| 0x12 | INQUIRY | Dispatch (14 hits) | ✓ Model/capacity | ✓ Model/capacity | ✓ Both modes |
| 0x15 | MODE SELECT(6) | Dispatch→construct | ✓ | ✓ | ✓ Both modes |
| 0x1A | MODE SENSE(6) | Dispatch→SATA | ✓ | ✓ | ✓ Both modes |
| 0x25 | READ CAPACITY(10) | Internal ROM | ✓ 1 TB/512/4096 | ✓ 1 TB/512/4096 | ✓ Both modes |
| 0x28 | READ(10) | SUBB cmp@0x065F | ✓ | ✓ | ✓ Both modes |
| 0x2A | WRITE(10) | Internal ROM | ✓ | ✓ | ✓ Both modes |
| 0x35 | SYNC CACHE(10) | Dispatch (3 hits) | ✓ No error | ✓ No error | ✓ Both modes |
| 0x4D | LOG SENSE | Dispatch | ✓ Logs OK | ✓ Logs OK | ✓ Both modes |
| 0x55 | MODE SELECT(10) | Dispatch | ✓ | ✓ | ✓ Both modes |
| 0x5A | MODE SENSE(10) | Dispatch | ✓ | ✓ | ✓ Both modes |
| 0x85 | ATA PASS-THROUGH | SAT translation | ✓ IDENTIFY OK | ✓ IDENTIFY OK | ✓ Both modes |
| 0x91 | SYNC CACHE(16) | Dispatch→SATA | ✓ | ✓ | ✓ Both modes |
| 0x1B | START STOP UNIT | Internal ROM | ✓ CM eject OK | ✓ CM eject OK | ✓ Supported (internal ROM) |
| 0x1E | PREVENT ALLOW | Internal ROM | ✓ CM eject OK | ✓ CM eject OK | ✓ Supported (internal ROM) |
| 0x37 | READ DEFECT DATA | No dispatch | ✗ not supported | ✗ not supported | ✗ Neither mode |
| 0xB0 | UNMAP (TRIM) | No dispatch | ✗ No TRIM | ✗ No TRIM | ✗ Neither mode |
| 0xB1 | WRITE SAME (TRIM) | No dispatch | ✗ No TRIM | ✗ No TRIM | ✗ Neither mode |
| 0xDF | JMicron DF (Flash) | Dispatch (2 hits) | ✓ Available | ✗ Unavailable | BOT only |
| 0xE0 | JMicron E0 (chip info) | Dispatch (13 hits) | ✓ Available | ✗ Unavailable | BOT only |
| 0xFF | JMicron FF (reset) | Dispatch (2 hits) | ✓ Available | ✗ Unavailable | BOT only |

### Key findings

1. **SCSI command layer is fully shared** — BOT and UAS produced identical results across 15 read-only tests, confirming command parsing and SAT translation use the same 8051 code.
2. **16 standard commands confirmed supported** (INQUIRY / TUR / RS / READ / WRITE / MODE SENSE / SELECT / LOG SENSE / SYNC CACHE / ATA PASS-THROUGH / READ CAPACITY).
3. **Confirmed unsupported**: READ DEFECT DATA(0x37), UNMAP(0xB0), WRITE SAME(0xB1) — TRIM is not passed through.
4. **Vendor commands (0xDF/0xE0/0xFF) are BOT-only** — UASPStor occupies the interface in UAS mode and does not forward vendor commands.

---

## 4. SAT Pass-Through

| Capability | Status | Notes |
|---|---|---|
| ATA IDENTIFY DEVICE | ✓ | Words 0-255 readable |
| READ SMART DATA | ✓ | Attributes/caps/temp OK |
| READ SMART LOG | ✓ | Error/selftest/PHY/stats logs OK |
| SCT commands | ✓ | Temp/ERC readable |
| SMART Return Status | ✗ | **ATA output registers missing** |
| WRITE SMART LOG | ✗ | Same register loss |

**SAT defect**: The bridge chip does not fully return ATA output registers (count + lba_low), so SMART Return Status (judged via lba_mid/lba_high = 0x4F/0xC2) is unavailable. smartctl falls back to attribute-based assessment. This defect exists in both modes.

---

## 5. Power Management

### StandbyTimer

| Item | Details |
|---|---|
| Storage | Chip's internal EEPROM (not SPI Flash, not dumpable) |
| Controls | Chip-level power-management state machine (not drive spin-down) |
| Runtime shadow register | `0x351E`/`0x351F` (16-bit, JMS565-exclusive 57 accesses, JMS561 has 0) |
| Sole write point | 0x140C7 (loaded from internal EEPROM at boot) |
| Effect of =0 | Disables deep-suspend entry; VBUS recovery re-enumerates successfully (verified) |

### go_suspend / exit_suspend

| Function | Address | Logic |
|---|---|---|
| go_suspend | 0xC9AF | Read 0x0017 (softconnect) → ANL 0xDF (disconnect) → LCALL 0xDF9E (internal ROM delay) → ORL 0x20 (reconnect) → LCALL 0xDE44 (internal ROM reinit) |
| exit_suspend | 0xC9EB | Write 0x3474-0x3477 + 0x3470 (PHY reinit register sequence) |

**Power management does not differ between BOT and UAS**: go_suspend does not read 0x35E0 (USB mode register); both modes use identical power-management code.

### VBUS-loss recovery

| Scenario | Chip path | Result |
|---|---|---|
| Full power loss (cold boot) | Reset vector 0x8016 full init | ✓ Enumerates |
| Overnight shutdown (enclosure powered) | go_suspend → deep suspend after timeout → VBUS returns → exit_suspend | ✗ Fails to enumerate |
| StandbyTimer=0, overnight shutdown | go_suspend → no deep suspend → VBUS returns → exit_suspend | ✓ Enumerates |

**Root cause**: StandbyTimer controls whether the chip enters deep suspend. Setting it to 0 keeps the SATA link active during VBUS loss, allowing exit_suspend to re-enumerate successfully.

---

## 6. Safe Removal (Eject)

### UAS-mode eject test

| Method | Result | Notes |
|---|---|---|
| CM_Request_Device_Eject (system-tray API) | ✓ Success (CR=0) | Volume unmounted, device held-for-eject, E: disappeared |
| Explorer right-click E: → Eject | ✗ No "Eject" verb in menu | INQUIRY RMB=0 treated as fixed disk |

### Eject failure root causes

| Cause | Layer | Notes |
|---|---|---|
| No right-click eject option | INQUIRY response | RMB (Removable Medium Bit) = 0, Windows treats as fixed disk |
| UAS "stopping" hang | Transport layer | START STOP UNIT completion timing with outstanding UAS commands |

Neither is a SCSI command-layer defect — SYNC CACHE / START STOP / PREVENT ALLOW are all functional at the command level.

---

## 7. UAS Drop-Disk Root Cause Summary

| Layer | BOT | UAS | Notes |
|---|---|---|---|
| SCSI command processing | ✓ Normal | ✓ Normal | Same SAT translation code |
| Power management | ✓ Normal | ✓ Normal | Same go_suspend/exit_suspend |
| USB transport | ✓ Serial, stable | ⚠ Concurrent, drop risk | UAS multi-endpoint command completion timing |
| Vendor commands | ✓ Available | ✗ Unavailable | UASPStor does not forward |
| Drop-disk observed | None | 3 surprise removals (id=157) + MFT corruption | Transport/power issue, not command layer |

**Conclusion**: UAS drop-disk root cause is in the USB transport layer and power-management state machine, not the SCSI command layer. The BOT override driver is the correct workaround.

---

## 8. Methodology & Limitations

### Toolchain

| Tool | Purpose |
|---|---|
| dis8051 v1.2 | Full disassembly (13,928 lines) |
| Python scripts | Binary diff, opcode search, SCSI dispatch analysis |
| smartctl 8.0-585 | Live SCSI command support testing (read-only, uninstalled after) |
| gsudo proxy | One-time elevation, persistent service to avoid repeated UAC prompts |

### Limitations

1. **Internal mask ROM is not readable** — library functions at 0xDC00-0xFFFF are invisible; some command-handling logic cannot be statically confirmed.
2. **StandbyTimer is in chip-internal EEPROM** — SPI Flash dump shows zero difference; JMMassProd writes are not visible in dumps.
3. **Single firmware, no control** — no normal/failed version comparison; cannot attribute to a specific historical change.
4. **Live tests are read-only** — write/erase/selftest commands were not tested by agreement.

---

## Attachment Index

| File | Description |
|---|---|
| [JMS565 Static Analysis Materials](JMS565_static_analysis_en.md) | Disassembly methodology, control flow, pseudo-C reconstruction |
| `JMS565_analysis_cn.md` | Earlier preliminary static analysis (VBUS/suspend paths) |
| `JMS565_full_linear_disassembly.lst` | Linear byte-by-byte disassembly of code region |
| `JMS565_reachable_disassembly.lst` | Reachable disassembly from reset/common vectors |
| `JMS565_control_flow_summary.txt` | Call graph, unresolved targets, string table |
| `JMS565_pseudocode.c` | Pseudo-C for key entry/VBUS/suspend paths |
| `disasm8051.py` | Local disassembly script |
