---
layout: default
title: JMS56x — JMicron Bridge Chip Archive
lang: en
---

# JMS56x

JMicron JMS56x family USB 3.0 → SATA bridge chip resource archive, verified on an ORICO 9528U3 enclosure. Firmware, UAS → BOT override driver, mass production tools, and in-depth firmware reverse-engineering.

---

## Latest Analysis Posts

<ul class="post-list">
{% for post in site.posts %}
  {% if post.lang != "cn" %}
  <li>
    <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span>
    <a class="post-title-sm" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    {% if post.tags %}<br>{% for tag in post.tags %}<span class="tag">{{ tag }}</span> {% endfor %}{% endif %}
  </li>
  {% endif %}
{% endfor %}
</ul>

---

## Sections

<div class="section-grid">
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/firmware">💾 Firmware</a></h3>
    <p>41 binaries — JMS551 / 561 / 561B / 561U / 565 / 567 / 578. Unified naming, chip lineage, version notes.</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/driver">🔌 BOT Driver</a></h3>
    <p>UAS → BOT override driver (Windows x64, self-signed). No new .sys — uses system usbstor.sys.</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/tools">🛠️ Tools</a></h3>
    <p>JMMassProd M.P. Tool (EEPROM / VID / PID / standby timer) & FwUpdateTool.</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/docs">📄 Docs</a></h3>
    <p>ORICO 9528U3 upgrade screenshots, standby-timer how-to.</p>
  </div>
  <div class="section-card">
    <h3><a href="https://github.com/xRetia/JMS56x/tree/main/analysis">🔍 Analysis</a></h3>
    <p>Full disassembly, pseudo-C, control flow, SCSI command testing, power management analysis.</p>
  </div>
</div>

---

## Key Findings

- **Architecture**: 8051 core (CISC), dual code space (external Flash 56 KB + internal mask ROM)
- **UAS**: Full BOT+UAS dual-protocol support via USB alternate setting, no firmware-level disable switch
- **SCSI**: 16 standard commands confirmed supported; TRIM (UNMAP/WRITE SAME) not passed through
- **SAT defect**: SMART Return Status registers missing — bridge chip swallows ATA output registers
- **Power**: StandbyTimer=0 in chip EEPROM fixes overnight VBUS-recovery enumeration failure
- **Safe removal**: CM API eject works; right-click "Eject" missing (INQUIRY RMB=0)
- **UAS drops**: Root cause in USB transport layer, not SCSI command layer

---

*Flashing firmware or modifying EEPROM carries a real brick risk — always back up first. All materials are for research and study only.*
