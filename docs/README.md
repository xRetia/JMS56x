# docs

Supporting documents for the ORICO 9528U3 enclosure (JMS551 / JMS56x family).

> **Languages:** English · [简体中文](README.cn.md)

## Contents

| File | Description |
| --- | --- |
| `9528u3升级步骤1.jpg` | Firmware upgrade dialog, step 1 (ORICO 9528U3) |
| `9528u3升级步骤2.jpg` | Firmware upgrade dialog, step 2 (ORICO 9528U3) |
| `设定休眠时间方法.docx` | How to set the auto standby timer (EEPROM `Standby Timer`) |

## Notes

- The upgrade steps shown in the screenshots are performed with the M.P. Tool (see [`tools/JMMassProd/`](../tools/JMMassProd/README.md)): check **Firmware Update**, load the `.bin`, press **START**.
- The standby timer is modified via **EEPROM Update**; a `Standby Timer` value of `0` disables auto standby.