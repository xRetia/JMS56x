---
layout: default
title: JMS56x — JMicron 桥接芯片资料库
lang: cn
---

# JMS56x

JMicron JMS56x 系列 USB 3.0 → SATA 桥接芯片资料合集（ORICO 9528U3 硬盘盒实测）：固件、UAS → BOT 切换驱动、量产工具，以及深度固件逆向分析。

<div class="text-end mb-4">
  <a href="{{ '/' | relative_url }}" class="badge-tag">English →</a>
</div>

---

## 最新文章

<ul class="post-list">
{% for post in site.posts %}
{% if post.lang == "cn" %}
<li>
  <time>{{ post.date | date: "%Y-%m-%d" }}</time>
  <a class="post-title-sm" href="{{ post.url | relative_url }}">{{ post.title }}</a>
  {% for tag in post.tags %}<span class="badge-tag">{{ tag }}</span> {% endfor %}
</li>
{% endif %}
{% endfor %}
</ul>

---

## 目录

<div class="section-grid">
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/firmware"><i class="bi bi-hdd"></i> 固件库</a></h3>
    <p>41 个二进制 — JMS551 / 561 / 561B / 561U / 565 / 567 / 578</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/driver"><i class="bi bi-plug"></i> BOT 驱动</a></h3>
    <p>UAS → BOT 覆盖驱动（Windows x64）</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/tools"><i class="bi bi-tools"></i> 量产工具</a></h3>
    <p>JMMassProd 量产工具 & FwUpdateTool</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/docs"><i class="bi bi-file-text"></i> 文档</a></h3>
    <p>升级步骤截图、休眠时间设定方法</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/analysis"><i class="bi bi-search"></i> 固件分析</a></h3>
    <p>反汇编、伪 C、SCSI 实测、电源管理分析</p>
  </div>
</div>

---

## 关键发现

<ul class="key-findings">
  <li><strong>架构</strong> — 8051 内核（CISC），双层代码空间（外部 Flash + 内部 mask ROM）</li>
  <li><strong>UAS</strong> — 固件支持 BOT+UAS 双协议，无固件级 UAS 开关</li>
  <li><strong>SCSI</strong> — 16 项命令确认支持；TRIM 不透传</li>
  <li><strong>SAT 缺陷</strong> — SMART Return Status 寄存器缺失</li>
  <li><strong>电源管理</strong> — StandbyTimer=0 解决关机一晚后 VBUS 恢复失败</li>
  <li><strong>安全删除</strong> — CM API 正常；右键无弹出选项（RMB=0）</li>
  <li><strong>UAS 掉盘</strong> — 根因在 USB 传输层，非 SCSI 命令层</li>
</ul>

---

<p class="text-muted small">本站资料仅供学习研究使用。刷写固件有变砖风险，请先备份。</p>
