---
layout: default
title: JMS56x — JMicron Bridge Chip Archive
lang: en
---

# JMS56x

JMicron JMS56x family USB 3.0 → SATA bridge chip resource archive, verified on an ORICO 9528U3 enclosure. Firmware, UAS → BOT override driver, mass production tools, and in-depth firmware reverse-engineering.

<div class="text-end mb-4">
  <a href="{{ '/cn/' | relative_url }}" class="badge-tag">中文 →</a>
</div>

---

## Latest Posts

<ul class="post-list">
{% for post in site.posts %}
{% if post.lang != "cn" %}
<li>
  <time>{{ post.date | date: "%Y-%m-%d" }}</time>
  <a class="post-title-sm" href="{{ post.url | relative_url }}">{{ post.title }}</a>
  {% for tag in post.tags %}<span class="badge-tag">{{ tag }}</span> {% endfor %}
</li>
{% endif %}
{% endfor %}
</ul>

---

## Sections

<div class="section-grid">
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/firmware"><i class="bi bi-hdd"></i> Firmware</a></h3>
    <p>41 binaries — JMS551 / 561 / 561B / 561U / 565 / 567 / 578</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/driver"><i class="bi bi-plug"></i> BOT Driver</a></h3>
    <p>UAS → BOT override driver (Windows x64)</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/tools"><i class="bi bi-tools"></i> Tools</a></h3>
    <p>JMMassProd M.P. Tool & FwUpdateTool</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/docs"><i class="bi bi-file-text"></i> Docs</a></h3>
    <p>Upgrade screenshots, standby-timer how-to</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/analysis"><i class="bi bi-search"></i> Analysis</a></h3>
    <p>Disassembly, pseudo-C, SCSI testing, power management</p>
  </div>
</div>

---

## Key Findings

<ul class="key-findings">
  <li><strong>Architecture</strong> — 8051 core (CISC), dual code space (external Flash + internal mask ROM)</li>
  <li><strong>UAS</strong> — Full BOT+UAS dual-protocol, no firmware-level disable switch</li>
  <li><strong>SCSI</strong> — 16 commands confirmed; TRIM not passed through</li>
  <li><strong>SAT defect</strong> — SMART Return Status registers missing</li>
  <li><strong>Power</strong> — StandbyTimer=0 fixes overnight VBUS-recovery failure</li>
  <li><strong>Safe removal</strong> — CM API works; right-click eject missing (RMB=0)</li>
  <li><strong>UAS drops</strong> — Root cause in USB transport layer, not SCSI commands</li>
</ul>

---

<p class="text-muted small">All materials are for research and study only. Flashing carries brick risk — back up first.</p>
