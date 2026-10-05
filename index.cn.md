---
layout: default
title: JMS56x — JMicron 桥接芯片资料库
lang: cn
---

# JMS56x

JMicron JMS56x 系列 USB 3.0 → SATA 桥接芯片资料合集（ORICO 9528U3 硬盘盒实测）：固件、UAS → BOT 切换驱动、量产工具，以及深度固件逆向分析。

---

## 最新分析文章

<ul class="post-list">
{% for post in site.posts %}
  {% if post.lang == "cn" %}
  <li>
    <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span>
    <a class="post-title-sm" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    {% if post.tags %}<br>{% for tag in post.tags %}<span class="tag">{{ tag }}</span> {% endfor %}{% endif %}
  </li>
  {% endif %}
{% endfor %}
</ul>

---

## 目录

<div class="section-grid">
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/firmware">💾 固件库</a></h3>
    <p>41 个固件二进制 — JMS551 / 561 / 561B / 561U / 565 / 567 / 578。统一命名、芯片谱系、版本说明。</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/driver">🔌 BOT 驱动</a></h3>
    <p>UAS → BOT 覆盖驱动（Windows x64，自签名）。不引入新 .sys，仅用系统自带 usbstor.sys。</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/tools">🛠️ 量产工具</a></h3>
    <p>JMMassProd 量产工具（EEPROM / VID / PID / 休眠时间）与 FwUpdateTool 固件升级工具。</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/docs">📄 文档</a></h3>
    <p>ORICO 9528U3 升级步骤截图、休眠时间设定方法。</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/analysis">🔍 固件分析</a></h3>
    <p>完整反汇编、伪 C 还原、控制流、SCSI 命令实测、电源管理分析。</p>
  </div>
</div>

---

## 关键发现

- **架构**：8051 内核（CISC），双层代码空间（外部 Flash 56 KB + 内部 mask ROM）
- **UAS**：固件支持 BOT+UAS 双协议（USB alternate setting），无固件级 UAS 开关
- **SCSI**：16 项标准命令确认支持；TRIM（UNMAP/WRITE SAME）不透传
- **SAT 缺陷**：SMART Return Status 寄存器缺失——桥接芯片吞了 ATA 返回寄存器
- **电源管理**：StandbyTimer=0（芯片内部 EEPROM）解决关机一晚后 VBUS 恢复枚举失败
- **安全删除**：CM API 弹出正常；右键无"弹出"选项（INQUIRY RMB=0）
- **UAS 掉盘**：根因在 USB 传输层，非 SCSI 命令层

---

*刷写固件、修改 EEPROM 存在变砖风险，请务必先备份。本站资料仅供学习研究使用。*
