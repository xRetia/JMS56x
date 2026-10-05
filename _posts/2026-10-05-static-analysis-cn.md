---
layout: default
title: "JMS565 固件静态分析：反汇编、控制流、伪 C 还原"
date: 2026-10-05
author: xRetia
lang: cn
tags: [反汇编, 8051, 伪C, 逆向]
---

> **English**: [/posts/2026/10/05/static-analysis/](/posts/2026/10/05/static-analysis/)

---

## 一、概述

本文档整理 JMS565 固件（版本 105.03.01.02）的静态分析资料，包括反汇编方法、控制流分析、关键代码路径的伪 C 还原，以及分析限制说明。

| 项目 | 值 |
|---|---|
| 源文件 | `JMS565_fw105.03.01.02_2-bay_HW-RAID0-1-Large-JBOD_ChipFlashDump.bin` |
| 文件大小 | 524,288 字节（512 KiB） |
| SHA-256 | `c65feffa30f9697ae383ecbd4b90514c53f1f8ec8ed2de380abddfff2718d623` |
| 代码区映射 | 文件 `0x10000`-`0x1DFFF` → CPU 地址 `0x0000`-`0xDFFF`（57,344 字节） |
| 反汇编工具 | dis8051 v1.2（interactive-8051-disassembler）+ 本地 `disasm8051.py` |
| 反汇编结果 | 线性 37,005 行；可达 612 条；直接调用 13 处 |

---

## 二、反汇编方法

### 工具链

| 工具 | 说明 |
|---|---|
| `dis8051_x64.exe` (v1.2) | 交互式 8051 反汇编器，用于完整反汇编导出 |
| `disasm8051.py` | 本地 Python 反汇编脚本，支持线性扫描 + 控制流可达性分析 |
| `un.txt` | dis8051 导出的完整反汇编结果（13,928 行） |

### 地址映射

```
文件偏移          CPU 地址        内容
0x00000-0x01FF    —              bank0 配置/描述区（RAID 模式表、VID/PID）
0x10000-0x1DBFF   0x0000-0xDBFF  bank1 应用代码区（~56 KB）
0x1DC00-0x1FFFF   0xDC00-0xFFFF  内部 mask ROM（dump 不到，显示为全零）
0x20000-0x7FFFF   —              高位填充（全零）
```

bank1 开头 `02 80 16` = `LJMP 0x8016`，为真正的 reset 向量。

### 零区处理

代码区每隔 `0x1000` CPU 地址出现约 `0x400` 字节连续零区。这些区域在反汇编中显示为 `NOP` 链，但实际是**内部 mask ROM 的映射空洞**——芯片运行时这些地址映射到出厂固化的库函数，dump 不到。

零区目标（控制流进入的零区）：

| CPU 地址 | 文件偏移 | 前 8 字节 |
|---|---|---|
| 0x5F43 | 0x015F43 | 00 00 00 00 00 00 00 00 |
| 0xBD0D | 0x01BD0D | 00 00 00 00 00 00 00 00 |
| 0xDDE0 | 0x01DDE0 | 00 00 00 00 00 00 00 00 |
| 0xDDEA | 0x01DDEA | 00 00 00 00 00 00 00 00 |
| 0xDEC4 | 0x01DEC4 | 00 00 00 00 00 00 00 00 |
| 0xDFA4 | 0x01DFA4 | 00 00 00 00 00 00 00 00 |
| 0xDFBC | 0x01DFBC | 00 00 00 00 00 00 00 00 |

---

## 三、控制流分析

### 直接调用关系

```
调用目标 <- 调用者
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

可达指令起点：611 条；直接调用：13 处。大量函数通过间接调用（`JMP @A+DPTR`，90+ 处）和函数指针分派，无法通过静态控制流完全还原。

### 代码区关键字符串

| CPU 地址 | 字符串 | 用途 |
|---|---|---|
| 0x5795 | `RAID0RAID1LARGE` | RAID 模式标识 |
| 0x5868 | `Virtual CD` | 虚拟光驱 |
| 0x5873 | `SES Device` | SES 设备 |
| 0x587E | `USB3.0` | USB 版本 |
| 0xBA03 | `JMicron JMS56x Series   RANDOM__0123456789ABCDEF` | EEPROM 模板（序列号字符集） |
| 0xC247 | `vbus_debounce_1 !!!` | VBUS 去抖调试字符串 |
| 0xC25B | `vbus_debounce_0 !!!` | VBUS 去抖调试字符串 |
| 0xC9CD | `u2_go_suspend` | USB 挂起入口 |
| 0xC9DB | `u2_exit_suspend` | USB 恢复入口 |
| 0xD08A | `"stop=` | 启停状态调试 |
| 0xD091 | `start=` | 启停状态调试 |
| 0xD098 | `Active=` | 活动状态调试 |

---

## 四、关键代码路径伪 C 还原

以下伪 C 基于反汇编结果重建，**不是原厂源码**，也不可编译。地址为 CPU CODE/XDATA 地址，寄存器名称未知，用 `xdata_read8`/`xdata_write8` 抽象表示。

### 4.1 复位入口（CPU 0x8016）

```c
/* Reset vector at CPU 0000: LJMP 0x8016 */
void reset_vector_0000(void) {
    jump_unresolved(0x8016);
}

/* Actual reset target at CPU 0x8016 */
void reset_entry_8016(void) {
    call_unresolved(0xDAFD);              /* 内部 ROM 初始化 */

    xdata_write8(0x5048, 0x20);          /* USB 配置 */
    xdata_write8(0x5049, 0x00);
    xdata_write8(0x504A, 0x00);
    xdata_write8(0x504B, 0x00);

    if (bit_read(0x00)) {                 /* RAM bit 0 选择初始化分支 */
        call_unresolved(0xDDE0);          /* 内部 ROM */
    } else {
        call_unresolved(0xDDEA);          /* 内部 ROM */
        xdata_write8(0x0052, 0x3C);
        xdata_write8(0x0062, 0x3C);
    }

    xdata_write8(0x7019, xdata_read8(0x7019) & 0x7F);  /* 清 USB 控制位 */
    call_unresolved(0x74E5);              /* 内部 ROM */
    call_unresolved(0x993D);              /* 内部 ROM */
    call_unresolved(0xBD0D);              /* 内部 ROM */
    xdata_write8(0x5064, xdata_read8(0x5064) & 0xEF);
    xdata_write8(0x5051, 0x80);
    xdata_write8(0x5056, xdata_read8(0x5056) | 0x02);
    xdata_write8(0x5056, xdata_read8(0x5056) & 0xFE);
    jump_unresolved(0xDFBC);              /* 内部 ROM，主循环入口 */
}
```

### 4.2 VBUS 状态候选处理器（CPU 0xC26F）

```c
/* 候选 VBUS 检测回调，邻近字符串 "vbus_debounce_1 !!!" */
void candidate_status_handler_C26F(void) {
    uint8_t status = xdata_read8(0x502E);    /* VBUS 状态寄存器? */
    if (status & 0x80) {
        call_unresolved(0x9F59);              /* 内部 ROM 处理 */
        callback_low_54  = 0xBD;
        callback_high_55 = 0xA2;             /* callback = 0xA2BD */
        return;
    }

    if (xdata_read8(0x7E1B) == 0) {          /* bank/配置检查 */
        xdata_write8(0x350C, xdata_read8(0x350C) | 0x02);
        call_unresolved(0xD792);              /* 内部 ROM */
    }
    callback_low_54  = 0xDA;
    callback_high_55 = 0x9B;             /* callback = 0x9BDA */
}
```

### 4.3 平行状态路径（CPU 0xC297）

```c
/* 平行状态路径，检查 XDATA 0x008B */
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

### 4.4 USB 挂起序列（CPU 0xC9AF）

```c
/* 邻近字符串 "u2_go_suspend" / "u2_exit_suspend" */
void suspend_like_sequence_C9AF(void) {
    /* 断开 USB（清 softconnect 位） */
    xdata_write8(0x0017, xdata_read8(0x0017) & 0xDF);
    call_unresolved(0xDF9E);                 /* 内部 ROM 延时 */

    /* 重连 USB（置 softconnect 位） */
    xdata_write8(0x0017, xdata_read8(0x0017) | 0x20);
    call_unresolved(0xDE44);                 /* 内部 ROM 重新初始化 */

    /* R6=0xCD, R7=0xCD → 延时参数 */
    call_unresolved(0xD76E);                 /* 内部 ROM 延时服务 */

    jump_unresolved(0x9280);                 /* 跳转到主循环/状态处理 */
}
```

### 4.5 USB 恢复 / PHY 重新初始化（CPU 0xC9EB）

```c
/* exit_suspend: 写 PHY 重新初始化寄存器序列 */
void exit_suspend_C9EB(void) {
    xdata_write8(0x3474, 0x62);    /* PHY 寄存器 */
    xdata_write8(0x3475, 0x52);    /* PHY 寄存器 */
    xdata_write8(0x3476, xdata_read8(0x3476));  /* 保留原值 */
    xdata_write8(0x3477, 0x02);    /* PHY 寄存器 */
    xdata_write8(0x3470, 0x04);    /* PHY 控制寄存器 */
    /* RET */
}
```

### 4.6 StandbyTimer 影子寄存器加载（CPU 0x140C7）

```c
/* 唯一的 0x351E 写入点：开机时加载 StandbyTimer 到运行时寄存器 */
void standby_timer_load_140C7(void) {
    /* ... 前置逻辑 ... */
    xdata_write8(0x351E, 0x01);           /* 启用 StandbyTimer 影子寄存器 */
    /* 后续读取 0x4B08 做乘法，结果存入 0x351E/0x351F */
    /* 具体值由内部 EEPROM 的 StandbyTimer 参数决定 */
}
```

---

## 五、分析限制

1. **内部 mask ROM 不可读**：0xDC00-0xFFFF 的库函数代码看不到，`call_unresolved()` 标记的函数无法还原语义。
2. **间接调用无法静态还原**：90+ 处 `JMP @A+DPTR` 跳转表分派，无法确定所有目标。
3. **寄存器名称未知**：XDATA 地址（如 0x502E、0x0017）的硬件含义只能从字符串关联和上下文推断。
4. **单份固件无对照**：没有正常/故障版本对比，不能归因到具体历史改动。
5. **线性扫描包含数据**：反汇编结果中常量、字符串、描述符也会被解码为指令，不代表真实代码边界。

---

## 六、附件文件索引

| 文件 | 说明 | 格式 |
|---|---|---|
| `JMS565_full_linear_disassembly.lst` | 代码区逐字节线性反汇编（37,005 行） | 文本 |
| `JMS565_reachable_disassembly.lst` | 从 reset/中断向量出发的可达反汇编（612 条） | 文本 |
| `JMS565_control_flow_summary.txt` | 调用关系、零区目标、字符串表（126 行） | 文本 |
| `JMS565_pseudocode.c` | 关键路径伪 C（146 行） | C 伪代码 |
| `disasm8051.py` | 本地反汇编脚本（206 行） | Python |

### 复现反汇编

```bash
# 使用 dis8051 v1.2 交互式导出
dis8051_x64.exe jms565_bank1.bin

# 使用本地脚本生成所有附件
python disasm8051.py --input firmware.bin --outdir analysis/ --file-base 0x10000 --code-size 0xE000
```
