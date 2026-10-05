# JMS565 Firmware Static Analysis Materials

> **Languages:** English · [简体中文](JMS565_static_analysis_zh.md)

## 1. Overview

This document compiles the static analysis materials for JMS565 firmware (version 105.03.01.02), including disassembly methodology, control-flow analysis, pseudo-C reconstruction of key code paths, and analysis limitations.

| Item | Value |
|---|---|
| Source file | `JMS565_fw105.03.01.02_2-bay_HW-RAID0-1-Large-JBOD_ChipFlashDump.bin` |
| File size | 524,288 bytes (512 KiB) |
| SHA-256 | `c65feffa30f9697ae383ecbd4b90514c53f1f8ec8ed2de380abddfff2718d623` |
| Code mapping | File `0x10000`-`0x1DFFF` → CPU addr `0x0000`-`0xDFFF` (57,344 bytes) |
| Disassembler | dis8051 v1.2 (interactive-8051-disassembler) + local `disasm8051.py` |
| Results | Linear 37,005 lines; reachable 612 instructions; 13 direct calls |

---

## 2. Disassembly Methodology

### Toolchain

| Tool | Description |
|---|---|
| `dis8051_x64.exe` (v1.2) | Interactive 8051 disassembler, used for full export |
| `disasm8051.py` | Local Python disassembler script supporting linear sweep + control-flow reachability |
| `un.txt` | Full disassembly export from dis8051 (13,928 lines) |

### Address mapping

```
File offset        CPU address     Content
0x00000-0x01FF     —               bank0 config/descriptors (RAID mode table, VID/PID)
0x10000-0x1DBFF    0x0000-0xDBFF   bank1 application code (~56 KB)
0x1DC00-0x1FFFF    0xDC00-0xFFFF   Internal mask ROM (not dumpable, appears as zeros)
0x20000-0x7FFFF    —               High padding (all zeros)
```

bank1 starts with `02 80 16` = `LJMP 0x8016`, the real reset vector.

### Zero-span handling

The code region has ~`0x400`-byte contiguous zero spans every `0x1000` CPU addresses. These appear as `NOP` chains in disassembly but are actually **internal mask ROM mapping holes** — at runtime these addresses map to factory-baked library functions invisible in dumps.

Zero-span targets (control flow entering zero regions):

| CPU addr | File offset | First 8 bytes |
|---|---|---|
| 0x5F43 | 0x015F43 | 00 00 00 00 00 00 00 00 |
| 0xBD0D | 0x01BD0D | 00 00 00 00 00 00 00 00 |
| 0xDDE0 | 0x01DDE0 | 00 00 00 00 00 00 00 00 |
| 0xDDEA | 0x01DDEA | 00 00 00 00 00 00 00 00 |
| 0xDEC4 | 0x01DEC4 | 00 00 00 00 00 00 00 00 |
| 0xDFA4 | 0x01DFA4 | 00 00 00 00 00 00 00 00 |
| 0xDFBC | 0x01DFBC | 00 00 00 00 00 00 00 00 |

---

## 3. Control-Flow Analysis

### Direct call graph

```
CALL TARGET <- CALLERS
002E  <- 9959
59B1  <- 6100
74E5  <- 8042
993D  <- 8045
AB70  <- 22E6
AB84  <- 9949
BD0D  <- 8048
D546  <- DA7F
D792  <- 59D3
DA7F  <- 22EE
DAFD  <- 8016
DDE0  <- 8029
DDEA  <- 802E
```

Reachable instruction starts: 611; direct calls: 13. Many functions are dispatched via indirect calls (`JMP @A+DPTR`, 90+ occurrences) and function-pointer tables, which cannot be fully resolved statically.

### Key strings in code region

| CPU addr | String | Purpose |
|---|---|---|
| 0x5795 | `RAID0RAID1LARGE` | RAID mode identifier |
| 0x5868 | `Virtual CD` | Virtual CD-ROM |
| 0x5873 | `SES Device` | SES device |
| 0x587E | `USB3.0` | USB version |
| 0xBA03 | `JMicron JMS56x Series   RANDOM__0123456789ABCDEF` | EEPROM template (serial charset) |
| 0xC247 | `vbus_debounce_1 !!!` | VBUS debounce debug string |
| 0xC25B | `vbus_debounce_0 !!!` | VBUS debounce debug string |
| 0xC9CD | `u2_go_suspend` | USB suspend entry |
| 0xC9DB | `u2_exit_suspend` | USB resume entry |
| 0xD08A | `"stop=` | Start/stop debug |
| 0xD091 | `start=` | Start/stop debug |
| 0xD098 | `Active=` | Active state debug |

---

## 4. Key Code Path Pseudo-C Reconstruction

The following pseudo-C is reconstructed from disassembly results. It is **not original vendor source** and cannot compile. Addresses are CPU CODE/XDATA addresses; register names are unknown, abstracted as `xdata_read8`/`xdata_write8`.

### 4.1 Reset entry (CPU 0x8016)

```c
/* Reset vector at CPU 0000: LJMP 0x8016 */
void reset_vector_0000(void) {
    jump_unresolved(0x8016);
}

/* Actual reset target at CPU 0x8016 */
void reset_entry_8016(void) {
    call_unresolved(0xDAFD);              /* Internal ROM init */

    xdata_write8(0x5048, 0x20);          /* USB config */
    xdata_write8(0x5049, 0x00);
    xdata_write8(0x504A, 0x00);
    xdata_write8(0x504B, 0x00);

    if (bit_read(0x00)) {                 /* RAM bit 0 selects init branch */
        call_unresolved(0xDDE0);          /* Internal ROM */
    } else {
        call_unresolved(0xDDEA);          /* Internal ROM */
        xdata_write8(0x0052, 0x3C);
        xdata_write8(0x0062, 0x3C);
    }

    xdata_write8(0x7019, xdata_read8(0x7019) & 0x7F);  /* Clear USB control bit */
    call_unresolved(0x74E5);              /* Internal ROM */
    call_unresolved(0x993D);              /* Internal ROM */
    call_unresolved(0xBD0D);              /* Internal ROM */
    xdata_write8(0x5064, xdata_read8(0x5064) & 0xEF);
    xdata_write8(0x5051, 0x80);
    xdata_write8(0x5056, xdata_read8(0x5056) | 0x02);
    xdata_write8(0x5056, xdata_read8(0x5056) & 0xFE);
    jump_unresolved(0xDFBC);              /* Internal ROM, main loop entry */
}
```

### 4.2 VBUS status candidate handler (CPU 0xC26F)

```c
/* Candidate VBUS detection callback, near string "vbus_debounce_1 !!!" */
void candidate_status_handler_C26F(void) {
    uint8_t status = xdata_read8(0x502E);    /* VBUS status register? */
    if (status & 0x80) {
        call_unresolved(0x9F59);              /* Internal ROM handler */
        callback_low_54  = 0xBD;
        callback_high_55 = 0xA2;             /* callback = 0xA2BD */
        return;
    }

    if (xdata_read8(0x7E1B) == 0) {          /* Bank/config check */
        xdata_write8(0x350C, xdata_read8(0x350C) | 0x02);
        call_unresolved(0xD792);              /* Internal ROM */
    }
    callback_low_54  = 0xDA;
    callback_high_55 = 0x9B;             /* callback = 0x9BDA */
}
```

### 4.3 Parallel status path (CPU 0xC297)

```c
/* Parallel status path, checks XDATA 0x008B */
void candidate_status_handler_C297(void) {
    uint8_t status = xdata_read8(0x008B);
    if (status & 0x80) {
        call_unresolved(0x9F59);
        callback_low_54  = 0xBD;
        callback_high_55 = 0xD3;             /* callback = 0xD3BD */
        return;
    }

    if (xdata_read8(0x7E1B) == 0) {
        xdata_write8(0x350C, xdata_read8(0x350C) | 0x02);
        call_unresolved(0xD792);
    }
    callback_low_54  = 0xDA;
    callback_high_55 = 0x9B;
}
```

### 4.4 USB suspend sequence (CPU 0xC9AF)

```c
/* Near strings "u2_go_suspend" / "u2_exit_suspend" */
void suspend_like_sequence_C9AF(void) {
    /* Disconnect USB (clear softconnect bit) */
    xdata_write8(0x0017, xdata_read8(0x0017) & 0xDF);
    call_unresolved(0xDF9E);                 /* Internal ROM delay */

    /* Reconnect USB (set softconnect bit) */
    xdata_write8(0x0017, xdata_read8(0x0017) | 0x20);
    call_unresolved(0xDE44);                 /* Internal ROM reinitialization */

    /* R6=0xCD, R7=0xCD → delay parameters */
    call_unresolved(0xD76E);                 /* Internal ROM delay service */

    jump_unresolved(0x9280);                 /* Jump to main loop/state handler */
}
```

### 4.5 USB resume / PHY reinitialization (CPU 0xC9EB)

```c
/* exit_suspend: write PHY reinitialization register sequence */
void exit_suspend_C9EB(void) {
    xdata_write8(0x3474, 0x62);    /* PHY register */
    xdata_write8(0x3475, 0x52);    /* PHY register */
    xdata_write8(0x3476, xdata_read8(0x3476));  /* Preserve original value */
    xdata_write8(0x3477, 0x02);    /* PHY register */
    xdata_write8(0x3470, 0x04);    /* PHY control register */
    /* RET */
}
```

### 4.6 StandbyTimer shadow register load (CPU 0x140C7)

```c
/* Sole 0x351E write point: load StandbyTimer to runtime register at boot */
void standby_timer_load_140C7(void) {
    /* ... preceding logic ... */
    xdata_write8(0x351E, 0x01);           /* Enable StandbyTimer shadow register */
    /* Subsequent: read 0x4B08, multiply, store into 0x351E/0x351F */
    /* Actual value determined by internal EEPROM StandbyTimer parameter */
}
```

---

## 5. Analysis Limitations

1. **Internal mask ROM not readable**: Library functions at 0xDC00-0xFFFF are invisible; `call_unresolved()` semantics cannot be recovered.
2. **Indirect calls not statically resolvable**: 90+ `JMP @A+DPTR` jump-table dispatches cannot be fully resolved.
3. **Register names unknown**: XDATA addresses (e.g., 0x502E, 0x0017) are inferred from string proximity and context, not from a datasheet.
4. **Single firmware, no control**: No normal/failed version comparison; cannot attribute to a specific change.
5. **Linear sweep includes data**: Constants, strings, and descriptors are disassembled as instructions; not all represent real code boundaries.

---

## 6. Attachment File Index

| File | Description | Format |
|---|---|---|
| `JMS565_full_linear_disassembly.lst` | Byte-by-byte linear disassembly of code region (37,005 lines) | Text |
| `JMS565_reachable_disassembly.lst` | Reachable disassembly from reset/interrupt vectors (612 instructions) | Text |
| `JMS565_control_flow_summary.txt` | Call graph, zero-span targets, string table (126 lines) | Text |
| `JMS565_pseudocode.c` | Key-path pseudo-C (146 lines) | C pseudocode |
| `disasm8051.py` | Local disassembly script (206 lines) | Python |

### Reproducing the disassembly

```bash
# Using dis8051 v1.2 interactive export
dis8051_x64.exe jms565_bank1.bin

# Using local script to generate all attachments
python disasm8051.py --input firmware.bin --outdir analysis/ --file-base 0x10000 --code-size 0xE000
```
