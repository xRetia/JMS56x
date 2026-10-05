# JMS56x

JMicron JMS56x family USB 3.0 → SATA bridge chip resource collection, verified on an ORICO 9528U3 enclosure. Covers:

- **Firmware** — flashing / recovery binaries
- **BOT driver** — UAS → BOT mode override driver (Windows x64)
- **Mass production tools** — EEPROM / VID / PID / standby timer / serial number editing
- **Documents** — upgrade steps and standby-timer how-to

> **Languages:** English · [简体中文](README.cn.md)

## Directory layout

| Path | Contents |
| --- | --- |
| [`analysis/`](analysis/) | JMS565 firmware analysis report (architecture / UAS / SCSI command support / power management / safe removal) |
| [`docs/`](docs/) | ORICO 9528U3 upgrade screenshots, standby-timer how-to |
| [`driver/`](driver/) | JMS56x UAS → BOT override driver (self-contained, no new `.sys`) |
| [`firmware/`](firmware/) | JMS56x family firmware archive — 41 binaries, unified naming, chip lineage and version notes |
| [`tools/`](tools/) | JMicron M.P. Tool (JMMassProd) and FW Update Utility (FwUpdateTool) |

Every directory ships both `README.md` (English) and `README.cn.md` (简体中文), with the English file linking to the Chinese one.

## Quick start

- **Switch UAS → BOT**: right-click `driver/install.bat` → Run as administrator (or double-click; it elevates itself), then replug the device. Uninstall with `driver/uninstall.bat`.
- **Find a firmware**: see the [firmware index](firmware/README.md).
- **Firmware analysis**: see the [JMS565 firmware analysis report](analysis/JMS565_firmware_analysis_en.md); static disassembly and pseudo-C reconstruction in the [static analysis materials](analysis/JMS565_static_analysis_en.md).
- **Change VID/PID or standby timer**: open the M.P. Tool under [`tools/JMMassProd`](tools/JMMassProd/README.md), check `EEPROM Update`, set `Standby Timer = 0` to disable auto standby.

## Disclaimer

Flashing firmware or modifying EEPROM carries a real risk of bricking or damaging the device. Back up the original firmware first and proceed at your own risk. All tools and firmware in this repository were collected from the web or from personal backups, for research and study only.