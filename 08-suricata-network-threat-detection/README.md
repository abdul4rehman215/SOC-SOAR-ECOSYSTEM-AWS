# 🛡️ Suricata IDS + Wazuh SIEM

![SOC Project](https://img.shields.io/badge/SOC-Detection%20Engineering-blue)
![Suricata](https://img.shields.io/badge/IDS-Suricata-orange)
![Wazuh](https://img.shields.io/badge/SIEM-Wazuh-green)
![MITRE](https://img.shields.io/badge/MITRE-ATT%26CK-red)


<div align="center">

<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/230919-suricata-diagram5.png" width="800">

</div>


# Network Threat Detection & Detection Engineering in a SOC Ecosystem

---

## 📌 Project Overview

This project demonstrates a **production-style SOC implementation** of:

* Network Intrusion Detection using Suricata
* Centralized log management using Wazuh SIEM
* Custom detection engineering (decoders + rules)
* MITRE ATT&CK enrichment
* Alert noise reduction
* High-confidence detection building
* Integration into incident response workflow (TheHive)

This is not a basic installation project.

This is a **complete SOC detection engineering lifecycle implementation.**

---

## 🎯 Real-World Problem Statement

Default IDS + SIEM integrations often result in:

* High-volume alert noise
* Limited context
* Slow triage
* Poor field extraction
* No MITRE mapping clarity
* Generic rule grouping
* Mixed endpoint + network telemetry

This project solves that by transforming:

```
Raw Suricata Alerts
        ↓
Structured Wazuh Decoded Events
        ↓
Custom Detection Rules
        ↓
MITRE Enriched Alerts
        ↓
Noise-Reduced High-Confidence Detections
        ↓
SOC-Optimized Visualization
        ↓
IR Case Forwarding
```

---

## 🧠 What This Project Demonstrates

* Network IDS deployment
* SIEM integration
* JSON decoder engineering
* Rule creation & correlation
* Severity normalization
* MITRE ATT&CK mapping
* Alert suppression strategy
* SOC dashboard optimization
* Scalable agent grouping
* Production-style detection lifecycle

---

# 🏗️ Architecture

<div align="center">

<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/Network%20security%20integration%20diagram.png" width="800">

</div>



Conceptual Flow:

```
Kali Linux (Attacker)
        ↓
Ubuntu Endpoint (Suricata + Wazuh Agent)
        ↓
Wazuh Manager
        ↓
Wazuh Dashboard (OpenSearch)
        ↓
TheHive (Incident Response)
```

---

# 🧩 Technologies Used

* Suricata IDS
* Wazuh SIEM
* OpenSearch Dashboards
* Emerging Threats Rules
* MITRE ATT&CK Framework
* TheHive IR Platform
* Ubuntu 24.04
* Kali Linux (Attacker Simulation)

---

# Suricata Deployment & Wazuh Integration

## Step 1 — Install Suricata on Ubuntu 24.04

### Add Suricata Repository

```bash
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt update
```

### Install Suricata

```bash
sudo apt install suricata -y
```

### Verify Installation

```bash
suricata -V
```

---

## Step 2 — Download Emerging Threats Rules

```bash
cd /tmp
curl -LO https://rules.emergingthreats.net/open/suricata-6.0.8/emerging.rules.tar.gz
sudo tar -xvzf emerging.rules.tar.gz -C /etc/suricata
```

Verify:

```bash
ls /etc/suricata/rules
```

---

## Step 3 — Configure Suricata

Edit:

```bash
sudo nano /etc/suricata/suricata.yaml
```

### Set Network Variables

```yaml
vars:
  address-groups:
    HOME_NET: "[YOUR_INTERNAL_IP/24]"
    EXTERNAL_NET: "any"
```

### Configure AF-PACKET

```yaml
af-packet:
  - interface: eth0
    cluster-id: 99
    cluster-type: cluster_flow
    defrag: yes
```

### Enable EVE JSON Logging

```yaml
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: /var/log/suricata/eve.json
      types:
        - alert
        - http
        - dns
        - tls
```

---

## Step 4 — Restart Suricata

```bash
sudo systemctl restart suricata
sudo systemctl status suricata
```

Check logs:

```bash
sudo tail -f /var/log/suricata/eve.json
```

---

## Step 5 — Configure Wazuh Agent to Ingest Suricata Logs

Edit:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
```

---

## Step 6 — Attack Simulation (Validation)

From Kali:

```bash
nmap -sS <TARGET_IP>
nmap --script vuln <TARGET_IP>
```

---

## Step 7 — Validate in Wazuh Dashboard

Filter:

```
rule.groups: suricata
```

You should see:

* ET SCAN alerts
* Source IP
* Destination IP
* Port
* Signature
* Severity
* Protocol

---

## ✅ Part 1 Outcome

* Suricata successfully detecting network attacks
* Wazuh ingesting JSON alerts
* Alerts visible in dashboard
* End-to-end IDS → SIEM workflow validated

---

# Detection Engineering & Noise Reduction

## 🔎 Problems Observed After Default Integration

* Excessive informational alerts
* Important fields buried in full_log
* No structured grouping
* No severity normalization
* No MITRE mapping enrichment
* Alert fatigue

---

# Step 1 — Custom Suricata JSON Decoders

Create:

```bash
sudo nano /var/ossec/etc/decoders/decoder-suricata-custom.xml
```

---

### Base JSON Decoder

```xml
<decoder name="suricata-json">
  <prematch>^\{</prematch>
</decoder>
```

---

### Parent JSON Decoder

```xml
<decoder name="suricata-json-child">
  <parent>suricata-json</parent>
  <plugin_decoder>JSON_Decoder</plugin_decoder>
</decoder>
```

---

### Extract Key Fields

Source IP:

```xml
<decoder name="suricata-srcip">
  <parent>suricata-json</parent>
  <regex>"src_ip":"([^"]+)"</regex>
  <order>srcip</order>
</decoder>
```

Destination IP:

```xml
<decoder name="suricata-dstip">
  <parent>suricata-json</parent>
  <regex>"dest_ip":"([^"]+)"</regex>
  <order>dstip</order>
</decoder>
```

HTTP User-Agent:

```xml
<decoder name="suricata-http-user-agent">
  <parent>suricata-json</parent>
  <regex>"http_user_agent":"([^"]+)"</regex>
  <order>http.user_agent</order>
</decoder>
```

Restart:

```bash
sudo systemctl restart wazuh-manager
```

---

# Step 2 — Custom Wazuh Rule File

Create:

```bash
sudo nano /var/ossec/etc/rules/100002-suricata-custom.xml
```

---

## HTTP Classification Group

```xml
<group name="suricata,suricata_http">
  <rule id="100006" level="3">
    <if_sid>86602</if_sid>
    <description>Suricata HTTP Traffic</description>
  </rule>
</group>
```

---

## DNS Classification

```xml
<group name="suricata,suricata_dns">
  <rule id="100007" level="3">
    <if_sid>86603</if_sid>
    <description>Suricata DNS Traffic</description>
  </rule>
</group>
```

---

## TLS Classification

```xml
<group name="suricata,suricata_tls">
  <rule id="100008" level="3">
    <if_sid>86604</if_sid>
    <description>Suricata TLS Traffic</description>
  </rule>
</group>
```

---

# Step 3 — Noise Reduction

Suppress low-value alerts:

```xml
<rule id="200300" level="0">
  <if_sid>86601</if_sid>
  <description>Suppress low severity Suricata alerts</description>
</rule>
```

---

# Step 4 — MITRE ATT&CK Mapping

Example: Nmap Detection

```xml
<rule id="100201" level="12">
  <if_sid>86600</if_sid>
  <match>Nmap</match>
  <description>Nmap scripting engine detected.</description>
  <mitre>
    <id>T1595</id>
  </mitre>
</rule>
```

---

# Step 5 — High-Confidence Detection

```xml
<rule id="100210" level="12">
  <if_sid>86600</if_sid>
  <match>Nmap</match>
  <description>Port scanning activity detected</description>
  <mitre>
    <id>T1595</id>
  </mitre>
</rule>
```

---

# Step 6 — Validation

From Kali:

```bash
nmap -sS -p 1433 <TARGET_IP>
```

Confirm:

* Custom rule ID triggered
* Correct severity
* MITRE mapping visible
* Structured fields parsed

---

# Step 7 — Forward to TheHive

Confirm:

* Alert becomes case
* Observables extracted

  * IP
  * URL
  * Domain
* MITRE context visible

---

# ✅ Part 2 Outcome

* Reduced Suricata alert noise
* Clean structured fields
* Custom MITRE mapping
* High-confidence detections
* SOC-style rule grouping
* Case management integration

---

# 🏆 PART 1 + 2 Final Result

This project now reflects:

* Detection engineering mindset
* SOC operational thinking
* Alert quality optimization
* Structured enrichment
* Real-world threat simulation validation

---

# Repository Structure:

```
08-suricata-network-threat-detection/
│
├── README.md                     ← Part 1 + Part 2 (Full Detection Engineering Guide)
├── commands.sh                   ← All commands clearly separated by machine
├── architecture-notes.txt
├── interview_qna.md
├── troubleshooting.md
├── rules/
│   ├── decoder-suricata-custom.xml
│   ├── 100002-suricata-custom.xml
│   └── 100050-suricata-enhanced.xml
│
├── dashboard-agent-group/        ← Part 3 (SOC Operationalization)
│   ├── README.md
│   ├── dashboard.json
│   ├── images/
│   ├── interview_qna.md
│   ├── troubleshooting.md
│   └── architecture.txt
│ 
└── docs/
    ├──
    └── Suricata_Wazuh_SOC_Project.pdf
```

---

# 📘 Official References Used

Wazuh + Suricata Integration Guide:
[documentation-wazuh_proof-of-concept-guide](https://documentation.wazuh.com/current/proof-of-concept-guide/integrate-network-ids-suricata.html)

Wazuh Blog – Responding to Network Attacks:
[Detailed-Installation-Guide](https://wazuh.com/blog/responding-to-network-attacks-with-suricata-and-wazuh-xdr/)

---

# 🚀 Final Project Summary

This project evolved from:

Suricata Installation  
→ Wazuh Integration  
→ Custom JSON Decoder Engineering  
→ Detection Rule Development  
→ Noise Reduction Strategy  
→ MITRE ATT&CK Enrichment  
→ High-Confidence Detection Logic  
→ Attack Simulation Validation  
→ SOC-Oriented Structuring  

It demonstrates the full lifecycle of modern detection engineering inside a Security Operations Center.

This is not a lab experiment.

It reflects how production SOC teams:

- Deploy network IDS sensors
- Normalize and structure logs
- Reduce alert fatigue
- Enrich detections with threat intelligence
- Map detections to MITRE ATT&CK
- Build investigation-ready alerts
- Optimize analyst workflow

---

# 🧠 Detection Engineering Philosophy Applied

Throughout this project, the following principles were implemented:

✔ Collect everything  
✔ Parse intelligently  
✔ Reduce noise without losing visibility  
✔ Enrich alerts with context  
✔ Elevate meaningful detections  
✔ Separate signal from telemetry  
✔ Validate with real attack simulations  
✔ Design for SOC scalability  

---

# 🏢 Real-World Relevance

This project directly aligns with responsibilities in:

- SOC Analyst roles  
- Detection Engineer roles  
- Security Engineer roles  
- Blue Team operations  
- Threat Detection & Response teams  

It demonstrates hands-on capability in:

- IDS deployment
- SIEM integration
- Log parsing engineering
- Rule development
- MITRE mapping
- Attack simulation validation
- Alert tuning strategy
- Incident escalation workflow

---

# 📂 Project Documentation

Full implementation details, screenshots, validation evidence, and dashboard exports are available in:

🔗 **[Suricata + Wazuh SOC Implementation PDF](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/08-suricata-network-threat-detection/docs/Implementation%20of%20Suricata%20IDS%20with%20Wazuh%20SIEM.pdf)**  

🔗 **[Custom-Rule-Decoder](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/08-suricata-network-threat-detection/docs/Wazuh%20Suricata%20Custom%20Rules%20and%20Decoders.pdf)**  

---

# 🏆 What Makes This Different

Most projects stop at:

“Suricata installed and logs visible.”

This project goes further:

✔ Detection logic improved  
✔ Alert fatigue reduced  
✔ Context enriched  
✔ MITRE mapping applied  
✔ Structured rule grouping implemented  
✔ SOC workflow optimized  
✔ Operational scalability introduced  

This is production-style SOC engineering.

---

# 🔚 Closing Statement

Security monitoring is not about generating alerts.

It is about generating meaningful signals.

This project demonstrates how to transform raw network telemetry into structured, contextualized, and investigation-ready intelligence inside a modern SOC ecosystem.

---
