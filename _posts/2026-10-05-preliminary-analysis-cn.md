---
layout: default
title: "JMS565 固件初步分析：VBUS 与 suspend 路径"
date: 2026-10-05
author: xRetia
lang: cn
tags: [VBUS, suspend, 初步分析]
---

## 结论先行

这份镜像里**确实能看到 USB/VBUS 状态采样与延迟回调结构**，也有 `vbus_debounce_1`、`vbus_debounce_0`、`u2_go_suspend`、`u2_exit_suspend` 等字符串。因此，“主控 8051 一直供电、Windows 关机时 USB VBUS 消失、隔夜后再上电无法重新枚举”与**USB PHY/控制器在长时间 suspend/VBUS 缺失后未彻底恢复**的方向相符。

但静态证据**不足以把根因锁定为某一条代码缺陷**：

- 相关 VBUS 候选处理器检查状态寄存器 bit7，并设置后续 callback/状态；它不是简单的“检测到 VBUS 就无条件重置 USB”的代码。
- 镜像中存在周期性 `0x400` 长零区，且多个调用/跳转目标落入这些零区。可能涉及 JMS565 的代码银行、内部 ROM 或映射规则；仅凭当前 Flash dump 无法还原这些目标的真实内容。
- 在 VBUS 两个候选处理器上没有找到直接 `LCALL` 字节引用；可能经函数指针/银行机制调用，也可能是未使用代码。关联度是**中等而非定论**。
- 没有器件的完整寄存器手册、实机总线波形、运行日志或可对照的正常/故障固件，不能声称伪 C 等同于原厂源码。

**最值得先验证的假设**：VBUS 恢复时，USB PHY/状态机或 debounce/suspend 的软件状态没有复位干净；短时断开仍处于可恢复窗口，长时断开后留下超时、陈旧状态或时钟/定时器异常。其次要排除主机侧根端口没有重新提供 VBUS，或设备物理层未产生 attach 信号。

## 输入镜像与映射

- 文件：`JMS565_fw105.03.01.02_2-bay_HW-RAID0-1-Large-JBOD_ChipFlashDump.bin`
- 大小：524,288 字节（512 KiB）
- SHA-256：`c65feffa30f9697ae383ecbd4b90514c53f1f8ec8ed2de380abddfff2718d623`
- 前 512 字节包含 RAID0/RAID1/JBOD、`JMS56X H/W RAID`、`JMicron Technology Corp.` 等字符串/配置数据。
- 文件偏移 `0x10000` 处存在 8051 指令样式的向量：`02 80 16`，即 `LJMP 0x8016`。按这一复位向量建立暂定映射：**文件 `0x10000 + CPU CODE 地址`**。
- 因此本报告对 `CPU CODE 0x0000–0xDFFF` 作了 `file 0x10000–0x1DFFF` 的线性反汇编。代码/数据边界及 JMS565 扩展银行映射并非完全已知；映射是可由复位向量支持的分析假设，不是芯片手册结论。
- 文件中 `0x15400` 附近可见 USB 描述符形态数据；代码区也包含 `RAID0RAID1LARGE`、`Virtual CD`、`SES Device`、`USB3.0` 等字符串。

## 反汇编范围和准确性

交付的线性 listing 覆盖上述 `0xE000` 字节窗口，含 CPU 地址、文件偏移、机器码和 8051 指令；也另外输出从复位向量与常见向量点出发的近似控制流 listing。

**重要限制**：8051 固件里可能有字符串、表、描述符和内嵌常数，线性 sweep 会把它们也译成指令；这种情况下即使 opcode 解码正确，边界仍不代表真实代码。控制流 listing 也不是证明完备的静态分析：跳转表、寄存器间接调用、定时器 callback、bank switching、外部 ROM 和缺失的代码区都可能漏掉路径。

代码映像每隔 `0x1000` CPU 地址观察到约 `0x400` 连续零字节（如 `0x0C00–0x0FFF`、`0x1C00–0x1FFF`、…、`0xDC00–0xDFFF`）。有些可达调用目标也落入这样的区间（例如 `0x9F59`、`0xBD0D`、`0xDDE0`、`0xDDEA`、`0xDFBC`）。这些区域在 listing 中仍按字节解码为 `NOP`，**不能据此断言芯片运行时真的执行 NOP**；它们可能是空洞、ROM/银行映射、镜像剥离内容或其他特殊映射。

本地解码脚本覆盖经典 MCS-51 的 256 个 opcode 值；`0xA5` 按保留/厂商扩展 opcode 标记。已做向量、入口、指令长度表检查。由于缺少 JMS565 处理器语言模块和符号表，结果不是有寄存器语义数据库的 Ghidra/IDA 级原厂反编译。

## 关键代码观察

### 1. 复位入口与初始化

- CPU `0x0000`：`LJMP 0x8016`。
- CPU `0x8016` 的首条指令实际是 `LCALL 0xDAFD`，**不是**低地址 `0x0016` 处的指令。前一版把 `0x0016` 与 `0x8016` 混淆；入口伪代码已按 `0x8016` 修正。
- 随后初始化 XDATA `0x5048–0x504B` 为 `20 00 00 00`；按 RAM bit `0x00` 选择调用 `0xDDE0` 或 `0xDDEA`（后一分支还写 `XDATA[0x0052]` 与 `[0x0062]` 为 `0x3C`）；然后清 `XDATA[0x7019].bit7`、调用 `0x74E5`、`0x993D`、`0xBD0D`，再更新 `0x5064`、`0x5051`、`0x5056`，最后跳 `0xDFBC`。
- 多个 helper/tail-jump 目标落在本镜像的长零区，因此可见的是初始化序列和调用参数，helper 实际功能无法从该 dump 还原。

文件中的低地址 `0x0016` 是另一段代码，不能当成复位入口。复位向量和 8051 跳转目标支持 `CPU 地址 0x8016` 这一解释；目标函数 `0xDAFD` 从一条线性反汇编边界中间开始，也再次提示需考虑函数入口/银行或镜像布局。

### 2. VBUS/debounce 候选路径：CPU `0xC26F`

相邻镜像数据区有 ASCII：`vbus_debounce_1 !!!` 和 `vbus_debounce_0 !!!`。其后可解码到一段结构如下的代码：

```asm
C26F  MOV  DPTR,#0x502E
C272  MOVX A,@DPTR
C273  JNB  ACC.7,0xC280
C276  LCALL 0x9F59
C279  MOV  0x54,#0xBD
C27C  MOV  0x55,#0xA2
C27F  RET
C280  MOV  DPTR,#0x7E1B
C283  MOVX A,@DPTR
C284  JNZ  0xC296
C286  MOV  DPTR,#0x350C
C289  MOVX A,@DPTR
C28A  ORL  A,#0x02
C28C  MOVX @DPTR,A
C28D  LCALL 0xD792
C290  MOV  0x54,#0xDA
C293  MOV  0x55,#0x9B
C296  RET
```

按标准 8051 的位寻址语义，前面的 `MOVX A,@DPTR` 后的 `JNB 0xE7` 检查 ACC.7。伪 C 可概括为：

```c
status = xdata[0x502E];
if (status & 0x80) {
    call_unknown(0x9F59);
    callback = 0xA2BD;
    return;
}
if (xdata[0x7E1B] == 0) {
    xdata[0x350C] |= 0x02;
    call_unknown(0xD792);
}
callback = 0x9BDA;
```

### 3. 平行状态路径：CPU `0xC297`

该段对 XDATA `0x008B` 执行同类 bit7 检查；状态分支设置 callback 值 `0xD3BD` 或 `0x9BDA`，低状态分支还可能置 `XDATA[0x350C].bit1` 并调用 `0xD792`。其逻辑见单独的伪 C 文件。

**解释边界**：寄存器 `0x502E`、`0x008B` 的准确硬件名称未在这份固件中给出；不能凭地址断言哪个就是 VBUS。字符串邻接只提供线索。直接扫描镜像未找到对 `0xC26F/0xC297` 的直接 `LCALL`，故它们可能通过间接 callback/银行方式调用，也可能不在当前运行路径上。

### 4. USB2 suspend/resume 线索：CPU `0xC9AF`

紧邻字符串 `u2_go_suspend` / `u2_exit_suspend` 的附近代码有如下序列：

```asm
C9AF  MOV  DPTR,#0x0017
C9B2  MOVX A,@DPTR
C9B3  ANL  A,#0xDF
C9B5  MOVX @DPTR,A
C9B6  LCALL 0xDF9E
C9B9  MOV  DPTR,#0x0017
C9BC  MOVX A,@DPTR
C9BD  ORL  A,#0x20
C9BF  MOVX @DPTR,A
C9C0  LCALL 0xDE44
C9C3  MOV  R6,#0xCD
C9C5  MOV  R7,#0xCD
C9C7  LCALL 0xD76E
C9CA  LJMP 0x9280
```

它对 XDATA `0x0017` 的 bit5 做清除/置位，并调用多个未知 helper，形态与 suspend/状态切换有关；字符串关联和函数名**尚未证明**。相关 helper 的一些目标同样在零填充代码窗口内。

### 5. 没有证实的事情

- 没有证据证明 firmware 在长时间 VBUS 为低后一定会进入某种特定省电模式。
- 没有完整证据证明 VBUS 恢复时缺少硬复位；可见代码是状态检查与 callback 更新，不是明确、完整的 USB PHY reset 序列。
- 没有证据能只靠静态 dump 分辨“Windows 侧枚举缓存/端口策略”和“设备侧完全没有 attach/设备侧 attach 后协议失败”。
- 单份版本固件没有对照差异，因此不能将问题归因到某一具体历史改动。

## 故障假设与验证顺序

### 优先假设 A：长 VBUS-off 后状态机/定时器未复位

“断 10–20 分钟正常、过夜不正常”通常更像**持续时间相关的状态保持/超时/时钟或计数器问题**，而不是立即失效的断线问题。固件存在 debounce/suspend 相关路径，这使它成为合理调查方向，但还不是定论。

### 优先假设 B：VBUS 或 USB 物理层恢复不到固件预期状态

即便 8051 主电源不断，主机 USB VBUS 在关机时可能消失。需测 VBUS 下降、回升、D+/D− pull-up/attach、SuperSpeed 链路训练与 reset。设备没在总线上 attach 和“attach 了但枚举失败”是不同问题。

### 建议试验（先不刷固件）

1. **做对照时序**：同一个 USB 端口、同一硬件分别断电 20 分钟和隔夜；记录主控供电、USB VBUS、桥接芯片 reset/enable（若可探测）。确认 Windows 关机后 VBUS 是否真的为 0 V，开机时是否按预期回到约 5 V。
2. **抓总线现象**：用 USB 分析仪或示波器观察 VBUS 恢复后，设备是否产生 attach/pull-up、是否收到 USB reset、主机是否发出 GET_DESCRIPTOR。若无 attach，重点看 VBUS detect/PHY enable/固件状态；若 attach 后请求失败，重点看控制端点状态机和描述符/中断处理。
3. **交叉主机测试**：故障隔夜后先不要给 8051 断电，接另一台电脑/USB 口。如果也不枚举，问题偏设备侧；如果只在原 Windows 主机故障，重点检查根集线器/端口策略、BIOS ErP/关机供电、Windows 快速启动/电源管理。
4. **分离复位类型**：在故障状态仅重启 PC、仅拔插 USB、仅重置桥接芯片（保留 SATA 供电）、整机断电；记录哪一种能恢复。若“重置 8051/桥接芯片即可恢复，但 USB 重新上电不行”，很支持设备固件/PHY 未处理 VBUS 回升。
5. **比较固件**：若能取得同硬件已知正常版本，只比较代码和配置区差异，不要直接刷相近 JMS56x 的固件；桥接芯片配置/VID/PID/RAID 参数可能不兼容。

### 修复方向（需先靠波形和芯片寄存器表确认）

在 VBUS 下降事件里清理 USB suspend/debounce/endpoint pending 状态并停止/重置相关计时器；在 VBUS 上升后强制重新初始化 USB PHY/控制器、清中断、重置 EP0/端点状态，并做一个有界的 soft-disconnect/reconnect 或控制器 reset。若规定时间内没有主机 reset/枚举完成，再由 watchdog 触发受控 USB 子系统恢复。不要在未确认寄存器含义和电源域关系前照抄地址或修改二进制。

## 伪 C 的范围说明

`JMS565_pseudocode.c` 给出复位向量、`0x8016` 入口、两条 VBUS 候选路径和一段 suspend-like 序列的结构化伪 C。**它不是全固件 C 源码的逐函数恢复**：要完整还原所有语义，需要 JMS565 扩展 8051/银行映射、SFR/XDATA 寄存器表、间接调用约定，以及缺失的 ROM/银行代码。完整逐字节反汇编另附 `.lst`，可以按地址继续人工审查。

## 附件索引

- `JMS565_full_linear_disassembly.lst`：代码映射区逐字节线性反汇编；含地址和文件偏移。
- `JMS565_reachable_disassembly.lst`：从复位/常见向量出发的近似可达反汇编；进入长零区时停止探索。
- `JMS565_control_flow_summary.txt`：直接调用关系、长零区未解析目标和字符串表。
- `JMS565_pseudocode.c`：关键入口/VBUS/suspend-like 伪 C。
- `disasm8051.py`：用于复现反汇编的本地 Python 解码脚本。
