# analysis — JMS565 Firmware Analysis

Static disassembly, pseudo-C reconstruction, live SCSI command support testing, power management, and safe-removal analysis of JMS565 firmware (version 105.03.01.02).

> **Languages:** English · [简体中文](README.cn.md)

## Reports

| File | Description |
| --- | --- |
| [`JMS565_firmware_analysis_en.md`](JMS565_firmware_analysis_en.md) | Full analysis report (architecture / UAS / SCSI / power management / safe removal) |
| [`JMS565_static_analysis_en.md`](JMS565_static_analysis_en.md) | Static analysis materials (disassembly methodology / control flow / pseudo-C) |
| [`JMS565_analysis_zh.md`](JMS565_analysis_zh.md) | Earlier preliminary static analysis (VBUS / suspend paths) |

## Attachments

| File | Description |
| --- | --- |
| [`JMS565_full_linear_disassembly.lst`](JMS565_full_linear_disassembly.lst) | Byte-by-byte linear disassembly of code region (37,005 lines) |
| [`JMS565_reachable_disassembly.lst`](JMS565_reachable_disassembly.lst) | Reachable disassembly from reset/interrupt vectors (612 instructions) |
| [`JMS565_control_flow_summary.txt`](JMS565_control_flow_summary.txt) | Call graph, zero-span targets, string table |
| [`JMS565_pseudocode.c`](JMS565_pseudocode.c) | Key-path pseudo-C (reset / VBUS / suspend / StandbyTimer) |
| [`disasm8051.py`](disasm8051.py) | Local 8051 disassembly script |

## Reproducing

```bash
# Using dis8051 v1.2 interactive export
dis8051_x64.exe jms565_bank1.bin

# Using local script to generate all attachments
python disasm8051.py --input firmware.bin --outdir analysis/ --file-base 0x10000 --code-size 0xE000
```
