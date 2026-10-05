---
layout: default
title: JMS56x Firmware Collection
nav: true
---

# JMS56x Firmware Collection

JMicron JMS56x family USB-SATA bridge / RAID controller firmware archive. Files follow a unified naming scheme and are cataloged by chip / bay count / feature. **All binaries are unmodified originals.**

> **Languages:** English · [简体中文](README.cn.md)

## Sections

- [Naming scheme](#naming-scheme)
- [Embedded firmware (extracted from tools)](#embedded-firmware-extracted-from-tools)
- [Version storage mechanism (why `fwUnknown`)](#version-storage-mechanism-why-fwunknown)
- [Firmware index](#firmware-index)
- [Chip lineage](#chip-lineage)
- [JMS578 variant index](#jms578-variant-index-1-bay)
- [Flashing notes](#flashing-notes)
- [Analysis basis](#analysis-basis)

## Naming scheme

```
JMS{chip}_fw{version}_{N}-bay_{feature}_{source}_{date}.bin
```

- **Bay count**: `1-bay` single-disk bridge / `2-bay` dual-disk (RAID or standalone)
- **Feature**: `HW-RAID0-1-Large-JBOD` hardware RAID (RAID0 / RAID1 / LARGE / JBOD); `UAS-Bridge` UAS single-disk bridge; `HDD-Clone` offline full-disk clone; `BusPower-ODD-SSD` bus power + ODD + SSD support
- **Source**: `CE702` / `Coltech-CE702` / `ORICO-9528U3` / `AGESTAR` / `SSI` / `STD` / `ChipFlashDump` (read from the actual chip) / `Embedded-*` (extracted from a flasher exe; `slotA`/`slotB` = multiple images inside one tool, ordered by offset)

## Embedded firmware (extracted from tools)

Flasher executables embed factory default firmware. Images were located by known header signatures, MD5-deduplicated and compared against every standalone file: **11 unique new images** (no duplicates):

| File | Chip | Size | Extracted from | Offset | Notes |
|---|---|---|---|---|---|
| `JMS561U_..._Embedded-FwUpdater561U_slotA.bin` | JMS561U | 256 KB | `FwUpdater561U_v1_0_2_0.exe` | 0x17B204 | Full FlashDump format (C0 AE header, default USB ID 197B:0562) |
| `JMS561U_..._Embedded-FwUpdater561U_slotB.bin` | JMS561U | 256 KB | same | 0x1BB204 | Second slot, same format |
| `JMS561_fwBuild4012_..._MultiTool_slotA.bin` | JMS561 | 64 KB | shared by 3 tools | 0x1FAE04 etc. | Header `JMicron JMS561.4012` |
| `JMS561_fwBuild4021_..._MultiTool_slotB.bin` | JMS561 | 64 KB | same | — | Header `JMicron JMS561.4021` |
| `JMS578_..._Embedded-FwUpdateTool119_slotA.bin` | JMS578 | 49 KB | `FwUpdateTool_v1_19_16_24.exe` | 0x1257FC | New version — no match among the 20 standalone files |
| `JMS578_..._Embedded-FwUpdateTool119_slotB.bin` | JMS578 | 49 KB | same | 0x131BFC | Same |
| `JMS578_..._Embedded-JMS567Tool100_slotA.bin` | JMS578 | 49 KB | `JMS567FwUpdateTool_v1_0_0_0.exe` | 0x19DA48 | Same |
| `JMS578_..._Embedded-JMS567Tool100_slotB.bin` | JMS578 | 49 KB | same | 0x1A9E48 | Same |
| `JMS567_..._Embedded-JMS567Tool1bay_slotA.bin` | JMS567 | 48 KB | `JMS567FwUpdateTool_1-bay_v01.exe` | 0x96BB4 | Compressed format (`12 42 00 D3 22` header) |
| `JMS567_..._Embedded-JMS567Tool1bay_slotB.bin` | JMS567 | 48 KB | same | 0xA2DB4 | Same |
| `JMS567_..._Embedded-JMS567Tool100_slotA.bin` | JMS567 | 48 KB | `JMS567FwUpdateTool_v1_0_0_0.exe` | 0x131848 | Same |

Notes:

- The 64 KB JMS561 pair is embedded in three tools (FwUpdater561U / FwUpdateTool v1.19 / JMS567FwUpdateTool v1.0.0.0), so the source is labeled `MultiTool`.
- `JMS567FwUpdateTool_v1_0_0_0.exe` and `JMS567_FwUpdateTool_v1_0_0_0.exe` (different MD5s) contain identical firmware areas — extracted once.
- Embedded JMS578 is 50176 B (standalone is 50688 B, missing the 512 B tail); header version field `04 04 04 04` vs `03 03 05 05` in standalone builds.
- Firmware contains no plaintext version; `fwUnknown` entries are explained in the next section — each was checked and confirmed unreadable offline, not left unchecked.

## Version storage mechanism (why `fwUnknown`)

Field-level conclusion for every binary (2026-10-03, cross-validated against known-version samples):

| Chip | How the version is stored | Readable offline? | Conclusion |
|---|---|---|---|
| JMS561/561B | 4-byte big-endian dword at header offset 0x19 (`6B 01 00 03` = v107.001.000.003), copy at 0x5F0; 256 KB files are **dual-bank mirrors** (full duplicate at 0x20000; version repeated at 0x20019/0x205F0) | yes, verified | both library versions match header fields exactly |
| JMS561 embedded 64 KB | ASCII build number in the version field (`4012`/`4021`) | yes, read | marked `fwBuild` |
| JMS567 | **Version exists only in the release filename**; no in-firmware version field; compressed; the 16-bit value at 0xBFF2 differs per build (v142→88 E6, SSI→12 2F, STD→26 3A) — can tell builds apart but not read a number | no | 3 embedded + 1 FullDump stay Unknown |
| JMS578 | **Version exists only in the release filename**; tail 512 B is the EEPROM factory template (152D:0578 + product string + SN template), no version; header platform tag `JMS579.0103` identical across builds | no | 4 embedded stay Unknown |
| JMS561U / JMS565 FlashDump | Version is returned at runtime by the chip via the tool's `RD Version` command; absent from the static image | no (needs live chip) | JMS565 `105.03.01.02` was read from the live chip; both 561U slots stay Unknown |

Also found: the tool executables contain no usable version string either (searching `NN.NN.NN.NN` only hits ASCII false positives), so embedded firmware versions cannot be recovered from their host tools offline.

## Firmware index

| File | Chip | Bays | Feature | Version | Size | Source |
|---|---|---|---|---|---|---|
| `JMS551_fw18.0.2.23.2_2-bay_HDD-Clone-LED_AGESTAR.bin` | JMS551 | 2 | offline clone (LED) | 18.0.2.23.2 | 50 KB | AGESTAR duplicator |
| `JMS551_fw255.0.6.0.7_2-bay_Full-Function_AGESTAR.bin` | JMS551 | 2 | Full (RAID0 / JBOD / Clone) | 255.0.6.0.7 | 64 KB | AGESTAR |
| `JMS551_fw0.31.4.23.2_2-bay_Dual-Disk-Basic_ORICO-9528U3.bin` | JMS551 | 2 | Dual disk, no RAID | 0.31.4.23.2 | 50 KB | ORICO 9528U3 (early batch) |
| `JMS561_fw107.001.000.003_1-bay_UAS-Bridge_CE702_20180706.bin` | JMS561 | 1 | UAS bridge | 107.001.000.003 | 256 KB | CE702, 2018-07-06 |
| `JMS561B_fw107.01.00.04_1-bay_UAS-Bridge_Coltech-CE702_20240830.bin` | JMS561B | 1 | UAS bridge | 107.01.00.04 | 256 KB | Coltech CE702, 2024-08-30 |
| `JMS565_fw105.03.01.02_2-bay_HW-RAID0-1-Large-JBOD_ChipFlashDump.bin` | JMS565 | 2 | HW-RAID0/1/Large/JBOD | 105.03.01.02 | 512 KB | This machine's chip dump |
| `JMS567_fw142.02.00.01_2-bay_HW-RAID0-1-Large-JBOD_CE-704U3_20240509.bin` | JMS567 | 2 | HW-RAID0/1/Large/JBOD | 142.02.00.01 | 48 KB | CE-704U3, 2024-05-09 |
| `JMS567_fwUnknown_2-bay_HW-RAID0-1-Large-JBOD_FullDump.bin` | JMS567 | 2 | HW-RAID0/1/Large/JBOD | unknown | 64 KB | Full image |
| `JMS567_fw20.06.00.01_2-bay_HW-RAID0-1-Large-JBOD_SSI.bin` | JMS567 | 2 | HW-RAID0/1/Large/JBOD | 20.06.00.01 | 48 KB | SSI OEM |
| `JMS567_fw00.01.01.07_2-bay_HW-RAID0-1-Large-JBOD_STD.bin` | JMS567 | 2 | HW-RAID0/1/Large/JBOD | 00.01.01.07 | 48 KB | STD |
| `JMS578_fw00.04.00.09_1-bay_BusPower-ODD-SSD_STD.bin` | JMS578 | 1 | Bus power / ODD / SSD | 00.04.00.09 | 50 KB | STD |

## Chip lineage

### JMS551 (older-generation USB 3.0 dual-bay)
- USB device ID: **VID 152D : PID 0551** (in firmware header)
- Early 2-bay products: disk duplicators (AGESTAR Clone / Full-Function), ORICO 9528U3 early batch (dual-disk standalone, no RAID)
- Full-Function build embeds `RAID0` / `JBOD` strings

### JMS561 / JMS561B (1-bay UAS bridge)
- Firmware header carries ASCII model mark `0561`; internal default USB ID **197B:0562** (shared family default)
- Same `JMS56X H/W RAID` software platform as JMS565, deployed as a 1-bay bridge
- 256 KB release files are dual-bank mirrors (copies at 0x0 and 0x20000); version at header 0x19 (both CE702 builds validated); tools also embed a 64 KB short build (ASCII build 4012/4021)
- **JMS561U**: USB-direct variant of the 561; the tool embeds two 256 KB FlashDump slots (`FwUpdater561U_v1_0_2_0.exe`, ini marks 561Series VID 1058 / PID 0A10)

### JMS565 (2-bay hardware RAID) — the chip measured on this machine's 9528U3
- Identified by the official JM2033x FW Update Utility as **JMS565 Series**, firmware **105.03.01.02**, Flash `MXIC/KH`
- `ChipFlashDump` is a **512 KB full SPI Flash backup** (exported with `Backup Old Firmware`), contains the config area — not a clean release build
- Firmware contains `JMS H/W RAID`, `RAID0RAID1LARGE` and the RAID0/RAID1/JBOD/LARGE mode tables
- 2-bay RAID variant on the same software platform as JMS561; closely related to JMS562 (official USB3.0 + eSATA → dual SATA RAID)
- Application: ORICO 9528U3 dual-bay basic model (runs non-RAID); the chip has HW-RAID capability but the basic model does not expose it

### JMS577 (2-bay hardware RAID)
- USB device ID **152D:0567** (firmware @0xC000)
- ORICO 9528RU3 array models use the JMS567 + JMS575 dual-chip design
- Compressed firmware (`12 42 00 D3 22` header); strings not directly readable
- 4 standalone variants (STD / SSI / CE-704U3 2024 / unknown FullDump) + 3 embedded (1-bay tool double slot + v1.0.0.0 tool single slot)

### JMS578 (1-bay multi-function bridge)
- USB device ID: **152D:0578** (EEPROM tail template header)
- Internal platform tag **JMS579.0103** (identical across builds); the 512 B tail is the EEPROM factory template (missing in embedded builds)
- Bus power / self power / ODD / SSD
- Library holds 20 standalone + 4 embedded (version only in filenames, see mechanism section); the **PPE (PowerPlus)** build disables HDD auto spin-down, good for Wii/PS2 long sessions (see `JMS578_fw124.01.00.02_1-bay_PPE-NoSpinDown_Guide.txt`)
- `Hardkernel` build targets ODROID boards; `NVRAM` build contains the 557 NVRAM configuration

## JMS578 variant index (1-bay)

| File | Feature | Version | Note |
|---|---|---|---|
| `JMS578_fw0.1.0.5_1-bay_Bridge_EarlyVersion.bin` | basic bridge | 0.1.0.5 | early build |
| `JMS578_fw00.01.00.03_1-bay_SelfPower_STD.bin` | self power | 00.01.00.03 | STD |
| `JMS578_fw00.02.00.02_1-bay_BusPower_STD.bin` | bus power | 00.02.00.02 | STD |
| `JMS578_fw00.02.00.03_1-bay_BusPower_STD.bin` | bus power | 00.02.00.03 | STD |
| `JMS578_fw00.04.00.05_1-bay_BusPower-ODD_STD_20170324.bin` | bus power + ODD | 00.04.00.05 | 2017-03-24 |
| `JMS578_fw0.04.00.07_1-bay_STD_OriginalCaseBackup.bin` | original-case backup | 00.04.00.07 | factory firmware backup |
| `JMS578_fw00.04.00.09_1-bay_BusPower-ODD-SSD_STD.bin` | bus power + ODD + SSD | 00.04.00.09 | STD (main index) |
| `JMS578_fw0.04.01.04_1-bay_SelfPower-ODD_STD.bin` | self power + ODD | 00.04.01.04 | STD |
| `JMS578_fw46.01.00.01_1-bay_NVRAM-Config.bin` | with NVRAM config | 46.01.00.01 | contains 557 NVRAM |
| `JMS578_fw68.01.00.02_1-bay_Bridge_Beihuan.bin` | basic bridge | 68.01.00.02 | Beihuan OEM |
| `JMS578_fw108.01.00.01_1-bay_BusPower-PowerPlus.bin` | bus power + PowerPlus | 108.01.00.01 | power mgmt fix |
| `JMS578_fw124.01.00.02_1-bay_PPE-NoSpinDown.bin` | PPE, no spin-down | 124.01.00.02 | Wii/PS2 recommended, see Guide.txt |
| `JMS578_fw173.01.00.01_1-bay_Bridge_Hardkernel_ODROID.bin` | basic bridge | 173.01.00.01 | ODROID community |
| `JMS578_fw173.01.00.02_1-bay_Bridge_Hardkernel_20190306.bin` | basic bridge | 173.01.00.02 | 2019-03-06 |
| `JMS578_fw255.01.00.01-beta_1-bay_Generic.bin` | beta | 255.01.00.01 | generic beta |
| `JMS578_fw255.01.00.01-beta_1-bay_ACASIS.bin` | beta | 255.01.00.01 | ACASIS |
| `JMS578_fw255.01.00.01-beta_1-bay_ACASIS-B.bin` | beta | 255.01.00.01 | ACASIS B |
| `JMS578_fw255.01.00.01-beta_1-bay_HTS.bin` | beta | 255.01.00.01 | HTS |
| `JMS578_fw255.01.00.01-beta_1-bay_KESU.bin` | beta | 255.01.00.01 | KESU |
| `JMS578_fw255.01.00.01-beta_1-bay_HGST-G-DRIVE.bin` | beta | 255.01.00.01 | HGST G-DRIVE |

## Flashing notes

1. **`JMS565_..._ChipFlashDump.bin` is a full flash backup** — it includes USB descriptors, SN and the config area. Flashing it to another device may overwrite VID/PID/SN — back up the target's original firmware first.
2. 49 KB-level files (JMS567 / JMS578 / JMS551) are **release packages** (code area only), no config area.
3. 256 KB (JMS561) and 512 KB (JMS565 dump) images differ in layout — selecting the wrong Flash layout in the tool bricks the device.
4. Companion tools: `FwUpdater561U_v1_0_2_0.exe` (JMS561U), `JMS567FwUpdateTool_*.exe`, `FwUpdateTool_v1_19_16_24.exe` (JMS578), `tools/JMMassProd/JMMassProd2_v1_16_14_1.exe`.
5. ORICO 9528U3 upgrade steps: `docs/9528u3升级步骤1.jpg` / `9528u3升级步骤2.jpg`.
6. JMS578 PPE flashing essentials (see the Guide.txt): a disk must be attached to read/write firmware; tick **RD Version** and **Including JM557 NVRAM** before writing; always back up the original firmware first.

## Analysis basis

The conclusions above come from binary analysis of every file in this directory (2026-10-03): USB descriptor extraction, string fingerprints, header layout comparison. The JMS565 identity was confirmed by the official JMicron JM2033x FW Update Utility reading the live chip. Embedded tool images were located by signature the same day, MD5-deduplicated and fully diffed against the standalone library before being added.