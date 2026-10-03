# JMMassProd — JMicron 2033x M.P. Tool

Mass production tool for JMicron USB-SATA bridge chips (JMS56x family).

> **Languages:** English · [简体中文](README.cn.md)

## Files

| File | Description |
| --- | --- |
| `JMMassProd2_v1_16_14_1.exe` | M.P. Tool v1.16.14.1 |
| `JMMassProd.ini` | Current configuration (reference) |
| `test.bin` | RW test payload referenced by `WriteFileName` |
| `log/JM2033x.log` | Tool's test log |

## Typical workflow

1. Connect the device, run the tool.
2. Tick **RD Version** and unlock with the password `jmicron`.
3. To change the standby timer: tick **EEPROM Update**, set **Standby Timer** to `0` to disable auto standby (details in `docs/设定休眠时间方法.docx`).
4. To flash firmware: tick **Firmware Update**, load the `.bin` (see `firmware/`).
5. Press **START**, wait for PASS, then **Safe Remove** and replug.

## Current configuration (JMMassProd.ini)

- EEPROM: VID `152D` / PID `9561`, `Standby Timer = 10` minutes
- `EnEEPROMUpdate=1`, `EnFWUpdate=1`
- Note: `FwFileName` still points to an old path (`D:\Library\Desktop\JMS56x\9528U3_固件\JMS551_Orico_v.0.31.4.23.2.BIN`). The firmware has been moved to `firmware/` — update this line to the current location before flashing.