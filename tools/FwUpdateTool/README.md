# FwUpdateTool — JM203x FW Update Utility

Simple firmware update utility for JMicron bridge chips.

> **Languages:** English · [简体中文](README.cn.md)

## Files

| File | Description |
| --- | --- |
| `FwUpdateTool_v1_19_16_24.exe` | The utility itself (JM203x FW Update Utility) |
| `FwUpdateTool.ini` | Window title, 561Series VID/PID preset (`VID 1058 : PID 0A10`), serial number template, reset control |

## Notes

- This tool is used to flash JMS578-family firmware (e.g. the PPE build, see `firmware/JMS578_fw124.01.00.02_1-bay_PPE-NoSpinDown_Guide.txt`) — a disk must be attached before it can read/write firmware.
- It is also the tool that identifies the chip on this machine as **JMS565 Series** (firmware `105.03.01.02`, Flash MXIC/KH).
- Always back up the original firmware first (`Backup Old Firmware`); for the PPE build, also tick **RD Version** and **Including JM557 NVRAM** before writing.