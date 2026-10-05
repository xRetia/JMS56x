---
layout: default
title: 文档
nav: true
---

# docs

ORICO 9528U3（JMS551 / JMS56x 系列）配套文档。

> **语言：** [English](README.md) · 简体中文

## 内容

| 文件 | 说明 |
| --- | --- |
| `9528u3升级步骤1.jpg` | ORICO 9528U3 固件升级界面截图（第 1 步） |
| `9528u3升级步骤2.jpg` | ORICO 9528U3 固件升级界面截图（第 2 步） |
| `设定休眠时间方法.docx` | 修改自动休眠时间的方法（EEPROM `Standby Timer`） |

## 说明

- 截图中的升级操作在量产工具中完成（见 [`tools/JMMassProd/`](../tools/JMMassProd/README.cn.md)）：勾选 `Firmware Update`、加载对应固件、点 `START`。
- 休眠时间通过 `EEPROM Update` 修改，`Standby Timer` 设为 `0` 即取消自动休眠。