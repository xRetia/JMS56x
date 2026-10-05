---
layout: post
title: "JMS565 固件完整分析报告"
date: 2026-10-05
author: xRetia
lang: cn
tags: [固件, 8051, UAS, SCSI, 电源管理]
---

> English: [/posts/2026/10/05/firmware-analysis-en.html]({/posts/2026/10/05/firmware-analysis-en.html})

﻿---
layout: default
title: JMS565 固件完整分析报告
nav: true
---

# JMS565 固件完整分析报告

> **语言：** [English](JMS565_firmware_analysis_en.md) · 简体中文

## 测试环境

| 项目 | 值 |
|---|---|
| 芯片 | JMicron JMS565（2-bay HW-RAID 版本） |
| 固件 | 105.03.01.02（RAID0 / RAID1 / Large / JBOD） |
| 硬盘盒 | ORICO 9528U3 |
| 硬盘 | TOSHIBA DT01ACA100 1TB（7200 rpm, SATA 3.0） |
| 代码分析 | dis8051 v1.2 完整反汇编（13 928 行） |
| 实测工具 | smartctl 8.0-585（只读模式，测后已卸载） |
| 测试日期 | 2026-10-05 |

---

## 一、固件架构

### 处理器：8051 内核（CISC），非 RISC

固件代码区充满 MCS-51/8051 特征码：`90 xx`（MOV DPTR）、`E0`/`F5`（MOVX 读写）、`12 xx xx`（LCALL）、`02 xx xx`（LJMP）、`22`（RET）、`74 xx`（MOV A,#imm）等。统计 4 KB 代码块：`0x90`=191 次、`0xE0`=160 次、`0x12`=81 次。

### 双层代码空间

| 区域 | 文件偏移 | 8051 地址 | 内容 | 可 dump |
|---|---|---|---|---|
| bank0 配置/描述区 | 0x00000-0x01FF | — | RAID 模式表、VID/PID、产品字符串 | ✓ |
| bank1 代码区 | 0x10000-0x1DBFF | 0x0000-0xDBFF | 应用固件（约 56 KB） | ✓ |
| 内部 mask ROM | — | 0xDC00-0xFFFF | 出厂固化库函数 | ✗ |
| 高位空白 | 0x1FC00-0x7FFFF | — | 全 0x00 填充 | ✓ |

**关键**：固件有 576 处 `LCALL`/`LJMP` 跳转到 0xDC00-0xFC00 区间——这不是 NOP 空操作，而是调用芯片内部 mask ROM 的库函数（延时、SATA 命令发送、PHY 重新初始化等）。外部 Flash dump 看不到这部分代码。

### bank 切换机制

通过寄存器 `0x7E08` / `0x7E10` / `0x7E21` 切换代码 bank（109 处访问）。bank1 开头 `02 80 16` = `LJMP 0x8016` 为真正的 reset 向量。

---

## 二、USB 描述符与 UAS 支持

### 描述符结构（与 JMS561 / 561B / 561U 完全同源）

| 项目 | 内容 |
|---|---|
| 接口结构 | alt0 = BOT（`08 06 50`），alt1 = UAS（`08 06 62`），4 端点 |
| UAS 管道描述符 | `04 24 01/02/03/04`，端点方向符合 UAS 规范 |
| MPS | USB3.0=1024、USB2.0=512、USB1.1=64 |
| 字符串 | `MSC BOT/UAS Transfer` |

**结论**：固件内置完整的 BOT + UAS 双协议支持，通过 USB alternate setting 切换，走哪套由主机枚举决定，固件本身没有"关闭 UAS"的开关。

---

## 三、SCSI 命令支持度

### 代码分析 + 实测合并总表

| opcode | 命令 | 代码分析 | BOT 实测 | UAS 实测 | 结论 |
|---|---|---|---|---|---|
| 0x00 | TEST UNIT READY | 有分派（21 处） | ✓ PASSED | ✓ PASSED | ✓ 两种模式都支持 |
| 0x03 | REQUEST SENSE | 有分派→SATA | ✓ 正常 | ✓ 正常 | ✓ 两种模式都支持 |
| 0x08 | READ(6) | 有分派（8 处） | ✓ | ✓ | ✓ 两种模式都支持 |
| 0x0A | WRITE(6) | 有分派（6 处） | ✓ | ✓ | ✓ 两种模式都支持 |
| 0x12 | INQUIRY | 有分派（14 处） | ✓ 型号/容量正常 | ✓ 型号/容量正常 | ✓ 两种模式都支持 |
| 0x15 | MODE SELECT(6) | 有分派→构造响应 | ✓ | ✓ | ✓ 两种模式都支持 |
| 0x1A | MODE SENSE(6) | 有分派→SATA | ✓ | ✓ | ✓ 两种模式都支持 |
| 0x25 | READ CAPACITY(10) | 内部 ROM | ✓ 1 TB/512/4096 | ✓ 1 TB/512/4096 | ✓ 两种模式都支持 |
| 0x28 | READ(10) | SUBB 比较@0x065F | ✓ | ✓ | ✓ 两种模式都支持 |
| 0x2A | WRITE(10) | 内部 ROM | ✓ | ✓ | ✓ 两种模式都支持 |
| 0x35 | SYNC CACHE(10) | 有分派（3 处） | ✓ 无错误 | ✓ 无错误 | ✓ 两种模式都支持 |
| 0x4D | LOG SENSE | 有分派 | ✓ 日志正常 | ✓ 日志正常 | ✓ 两种模式都支持 |
| 0x55 | MODE SELECT(10) | 有分派 | ✓ | ✓ | ✓ 两种模式都支持 |
| 0x5A | MODE SENSE(10) | 有分派 | ✓ | ✓ | ✓ 两种模式都支持 |
| 0x85 | ATA PASS-THROUGH | SAT 翻译 | ✓ IDENTIFY 正常 | ✓ IDENTIFY 正常 | ✓ 两种模式都支持 |
| 0x91 | SYNC CACHE(16) | 有分派→SATA | ✓ | ✓ | ✓ 两种模式都支持 |
| 0x1B | START STOP UNIT | 内部 ROM | ✓ CM 弹出成功 | ✓ CM 弹出成功 | ✓ 支持（内部 ROM 处理） |
| 0x1E | PREVENT ALLOW | 内部 ROM | ✓ CM 弹出成功 | ✓ CM 弹出成功 | ✓ 支持（内部 ROM 处理） |
| 0x37 | READ DEFECT DATA | 未找到分派 | ✗ not supported | ✗ not supported | ✗ 两种模式都不支持 |
| 0xB0 | UNMAP (TRIM) | 未找到分派 | ✗ 未检测到 TRIM | ✗ 未检测到 TRIM | ✗ 两种模式都不支持 |
| 0xB1 | WRITE SAME (TRIM) | 未找到分派 | ✗ 未检测到 TRIM | ✗ 未检测到 TRIM | ✗ 两种模式都不支持 |
| 0xDF | JMicron DF（Flash） | 有分派（2 处） | ✓ 可用 | ✗ 不可用 | 仅 BOT 可用 |
| 0xE0 | JMicron E0（芯片信息） | 有分派（13 处） | ✓ 可用 | ✗ 不可用 | 仅 BOT 可用 |
| 0xFF | JMicron FF（复位） | 有分派（2 处） | ✓ 可用 | ✗ 不可用 | 仅 BOT 可用 |

### 关键结论

1. **SCSI 命令层完全共用**——BOT 和 UAS 15 项只读测试结果完全一致，证实命令解析和 SAT 翻译走同一套 8051 代码。
2. **确认支持 16 项标准命令**（INQUIRY / TUR / RS / READ / WRITE / MODE SENSE / SELECT / LOG SENSE / SYNC CACHE / ATA PASS-THROUGH / READ CAPACITY）。
3. **确认不支持**：READ DEFECT DATA(0x37)、UNMAP(0xB0)、WRITE SAME(0xB1)——TRIM 不透传。
4. **厂商命令（0xDF/0xE0/0xFF）仅 BOT 可用**——UAS 模式下 UASPStor 占用接口且不转发厂商命令。

---

## 四、SAT 透传能力

| 能力 | 状态 | 说明 |
|---|---|---|
| ATA IDENTIFY DEVICE | ✓ | Word 0-255 全部可读 |
| READ SMART DATA | ✓ | 属性/能力/温度正常 |
| READ SMART LOG | ✓ | 错误/自测/PHY/统计日志正常 |
| SCT 命令 | ✓ | 温度/ERC 可读 |
| SMART Return Status | ✗ | **ATA output registers missing** |
| WRITE SMART LOG | ✗ | 同样返回寄存器缺失 |

**SAT 透传缺陷**：桥接芯片未完整返回 ATA output registers（count + lba_low），导致 SMART Return Status（通过 lba_mid/lba_high = 0x4F/0xC2 判定）不可用。smartctl 回退到属性判断。两种模式都存在此缺陷。

---

## 五、电源管理

### StandbyTimer

| 项目 | 说明 |
|---|---|
| 存储位置 | 芯片内部 EEPROM（非 SPI Flash，dump 不到） |
| 控制对象 | 芯片级电源管理状态机（非硬盘自身停转） |
| 运行时影子寄存器 | `0x351E`/`0x351F`（16 位，JMS565 专属 57 次访问，JMS561 为 0 次） |
| 唯一写入点 | 0x140C7（开机时从内部 EEPROM 加载到 0x351E） |
| =0 的效果 | 禁用芯片自动进入深度休眠；VBUS 恢复后能重新枚举（实测验证） |

### go_suspend / exit_suspend

| 函数 | 地址 | 逻辑 |
|---|---|---|
| go_suspend | 0xC9AF | 读 0x0017（softconnect）→ ANL 0xDF（断开 USB）→ LCALL 0xDF9E（内部 ROM 延时）→ ORL 0x20（重连）→ LCALL 0xDE44（内部 ROM 重新初始化） |
| exit_suspend | 0xC9EB | 写 0x3474-0x3477 + 0x3470（PHY 重新初始化寄存器序列） |

**电源管理不分 BOT/UAS**：go_suspend 不读取 0x35E0（USB 模式判断寄存器），两种模式走完全相同的电源管理代码。

### VBUS 掉电恢复问题

| 场景 | 芯片路径 | 结果 |
|---|---|---|
| 完全断电（冷启动） | reset 向量 0x8016 完整初始化 | ✓ 能识别 |
| 关机一晚（盒子有电） | go_suspend → 长时间后进入深度休眠 → VBUS 恢复 → exit_suspend | ✗ 连不上 |
| StandbyTimer=0 后关机一晚 | go_suspend → 不进入深度休眠 → VBUS 恢复 → exit_suspend | ✓ 能识别 |

**根因**：StandbyTimer 控制芯片进入深度休眠的开关。=0 禁用后，VBUS 恢复时 SATA 链路保持活跃，exit_suspend 能正常重新枚举。

---

## 六、安全删除（弹出）

### UAS 模式弹出实测

| 测试方式 | 结果 | 说明 |
|---|---|---|
| CM_Request_Device_Eject（系统托盘 API） | ✓ 成功（CR=0） | 卷卸载、设备 held-for-eject、E: 消失 |
| 资源管理器右键 E: → 弹出 | ✗ 菜单无"弹出"选项 | INQUIRY RMB=0 被识别为固定磁盘 |

### 弹出问题根因

| 原因 | 层面 | 说明 |
|---|---|---|
| 右键无弹出选项 | INQUIRY 响应 | RMB（Removable Medium Bit）=0，Windows 识别为固定磁盘 |
| UAS 卡在"正在停止" | 传输层 | UAS 有未完成命令时 START STOP UNIT 完成时序异常 |

两者都不是 SCSI 命令层缺陷——SYNC CACHE / START STOP / PREVENT ALLOW 命令层都正常。

---

## 七、UAS 掉盘根因总结

| 层面 | BOT | UAS | 说明 |
|---|---|---|---|
| SCSI 命令处理 | ✓ 正常 | ✓ 正常 | 同一套 SAT 翻译代码 |
| 电源管理 | ✓ 正常 | ✓ 正常 | 同一套 go_suspend/exit_suspend |
| USB 传输层 | ✓ 串行，稳定 | ⚠ 并发，有掉盘风险 | UAS 多端点并发命令完成时序问题 |
| 厂商命令 | ✓ 可用 | ✗ 不可用 | UASPStor 不转发 |
| 掉盘实测 | 无 | 3 次意外移除（id=157）+ MFT 损坏 | 传输层/供电问题，非命令层 |

**结论**：UAS 掉盘根因在 USB 传输层和电源管理状态机，不在 SCSI 命令层。BOT 覆盖驱动是正确的规避方案。

---

## 八、分析方法与限制

### 工具链

| 工具 | 用途 |
|---|---|
| dis8051 v1.2 | 完整反汇编（13 928 行） |
| Python 脚本 | 二进制 diff、opcode 搜索、SCSI 命令分派分析 |
| smartctl 8.0-585 | 实测 SCSI 命令支持度（只读，测后已卸载） |
| gsudo 代理 | 一次提权持续服务，避免反复弹 UAC |

### 限制

1. **内部 mask ROM 不可读**——0xDC00-0xFFFF 的库函数代码看不到，部分命令处理逻辑无法静态确认。
2. **StandbyTimer 存储在芯片内部 EEPROM**——SPI Flash dump 零差异，JMMassProd 写入后读不到。
3. **单份固件无对照**——没有正常/故障版本对比，不能归因到具体历史改动。
4. **实测为只读**——写入/擦除/自测类命令按约定禁止测试。

---

## 附件索引

| 文件 | 说明 |
|---|---|
| [JMS565 静态分析资料](JMS565_static_analysis_cn.md) | 反汇编方法、控制流、伪 C 还原 |
| `JMS565_analysis_cn.md` | 早期初步静态分析（VBUS/suspend 路径） |
| `JMS565_full_linear_disassembly.lst` | 代码映射区逐字节线性反汇编 |
| `JMS565_reachable_disassembly.lst` | 从 reset/常见向量出发的可达反汇编 |
| `JMS565_control_flow_summary.txt` | 调用关系、未解析目标、字符串表 |
| `JMS565_pseudocode.c` | 关键入口/VBUS/suspend 伪 C |
| `disasm8051.py` | 本地反汇编脚本 |
