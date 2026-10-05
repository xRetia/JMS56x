---
layout: default
title: JMS56x UAS → BOT Override Driver
nav: true
---

# driver — JMS56x UAS → BOT Override Driver (Windows x64)

Some scenarios (older systems, data-recovery tools, certain utilities) require the device to operate in **BOT (Bulk-Only Transport)** mode, while JMS56x loads as **UAS** by default. This package forces the switch with an override INF — no new kernel driver is introduced.

> **Languages:** English · [简体中文](README.cn.md)

## What it does

- Overrides `VID_152D` for all common JMS56x PIDs: 0561 / 0562 / 0567 / 1561 / 2561 / 2566 / 2590 / 3562 / 3569 / 8561 / 9561 / 9562 / 9566 / 9567
- Adds **no new `.sys`** — it only redirects to the system built-in `usbstor.sys` (BOT storage class driver)
- After installation, Device Manager shows **JMicron JMS56x USB 3.0 to SATA Adapter (BOT Mode)**

## Files

| File | Purpose |
| --- | --- |
| `install.bat` | Elevates via `gsudo64.exe`, imports the signing certificate into Trusted Root, then `pnputil /add-driver jms56xbot.inf /install` |
| `uninstall.bat` | Elevates, removes the driver package (`remove-driver.ps1`) and deletes the certificate |
| `remove-driver.ps1` | Locates the published `oem*.inf` matching `jms56xbot.inf` and deletes it |
| `jms56xbot.inf` | Override INF (USB class, includes `usbstor.inf` BOT install sections) |
| `jms56xbot.cat` | Catalog file for the INF |
| `JMS561TestSigner.cer` | Self-signed code-signing certificate (CN=JMS561 Test Signer) |
| `gsudo64.exe` | Portable elevation helper (cached credentials) used by the scripts |

## Install

Right-click **install.bat** → **Run as administrator** (or double-click; the script elevates itself via gsudo). Then unplug and replug the device.

## Uninstall

Right-click **uninstall.bat** → **Run as administrator**. Unplug and replug — UAS mode is restored.

## Notes

- The certificate is **self-signed**; Windows may show "Unknown publisher" — expected.
- Verification: `signtool` `/pa` (application policy) passes; `/kp` (kernel policy / DSE) cannot chain to a Microsoft root for a self-signed chain — expected, and irrelevant here because the INF ships **no new `.sys`**.
- The INF lists the family PIDs including UAS and BOT variants; devices reporting `197B:0562` (the family default ID) or `152D` PIDs both match the respective entries.