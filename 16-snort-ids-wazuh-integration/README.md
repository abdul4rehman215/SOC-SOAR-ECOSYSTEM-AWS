# 🐷 Snort IDS Exploration + Custom Rule Development + Wazuh SIEM Integration

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/what-is-snort.jpg" alt="Snort IDS" width="720" />
</p>

---

## 📌 Project Overview

This project is a **hands-on, practical exploration of Snort IDS** in a real SOC-style lab environment. The goal is **not just installation**, but real learning through:

- Running Snort in **IDS (NIDS)** mode on an Ubuntu (AWS EC2) endpoint
- Understanding how Snort inspects traffic and generates alerts
- Writing and validating **custom Snort detection rules**
- Using **Snorpy** (GUI rule generator) to create rules visually (to reduce syntax mistakes)
- Simulating attacker traffic from **Kali Linux**
- Integrating Snort alerts into **Wazuh SIEM** for centralized monitoring and investigation

✅ **Snort** gives network-layer visibility (**what’s happening on the wire**)  
✅ **Wazuh** gives SOC visibility (**central alerts + dashboards + investigation**)  

---

## 🧩 Role in My SOC Ecosystem

Wazuh is primarily a **host-based** monitoring platform (HIDS/XDR). Adding Snort expands the SOC to include **network-based detection**:

- Detect reconnaissance and scanning **before** payload execution
- Detect suspicious protocol behavior (ICMP/TCP/FTP attempts)
- Generate network alerts that can be **correlated** inside the SIEM

This project adds:

✅ **Network Intrusion Detection Visibility** → directly into the Wazuh dashboard

---

## 🎯 Objectives

By completing this project, I was able to:

- Install Snort on Ubuntu EC2 and configure it correctly
- Understand Snort modes and where rules/logs/config live
- Create and test **custom rules**:
  - ICMP Echo Request/Reply detection
  - FTP authentication attempt detection
  - SSH connection attempt detection (rule pack)
  - Web traversal attempt detection (rule pack)
- Validate Snort configuration and rule syntax (`snort -T`)
- Generate real test traffic (ICMP + TCP/FTP)
- Simulate attacker behavior from Kali Linux
- Configure Snort logging (fast alert format)
- Integrate Snort alerts into Wazuh using `localfile` monitoring
- (Optional improvement) Add a **Wazuh decoder + ruleset** for clean parsing and better severity

---

## 🧰 Prerequisites

Before doing this project, it helps to know:

- Basic Linux CLI and editing files with `nano`
- Basic networking concepts (ICMP, TCP, ports)
- Understanding of SOC alerting concepts (rules → alerts → triage)
- Wazuh agent basics (service restart + ossec.conf)

---

## 🧪 Environment

| Component | Details |
|----------|---------|
| Sensor | Ubuntu (AWS EC2) running Snort + Wazuh Agent |
| Attacker simulation | Kali Linux |
| IDS | Snort 2.9.x |
| SIEM | Wazuh Manager + Wazuh Dashboard |
| Snort log used | `/var/log/snort/snort.alert.fast` |
| Work style | Mostly terminal-based (plus Snorpy web UI for rule building) |

---

## 🏗️ Architecture Overview

### 🖼️ Snort → Wazuh SOC Flow Diagram
<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/wazuh-snort-architecture.png" alt="Wazuh + Snort Architecture" width="900" />
</p>

### 🔁 High-Level Data Flow
```

Kali Linux (Attacker)
|
| ICMP / FTP / TCP Traffic
v
Ubuntu EC2 (Snort IDS + Wazuh Agent)
|
| Snort Alerts (fast alert log)
v
Wazuh Manager (SIEM)
|
v
Wazuh Dashboard (OpenSearch)
|
v
SOC Analyst (central monitoring + investigation)

````

---

## 🧠 What is Snort?

**Snort** is an open-source **Network Intrusion Detection System (NIDS)** and can also be used as an IPS. It inspects network traffic and triggers alerts when packets match defined rules/signatures.

### 🧰 Snort Modes (high-level)
- **Sniffer mode** → view packets live
- **Packet logger mode** → save packets/logs for analysis
- **NIDS mode** → detect suspicious traffic using rules (what we used)

---

## ✅ Why Snort is Valuable for SOC Monitoring

### ⭐ Key Benefits
- Real-time traffic inspection (network layer visibility)
- Signature/rule-based detection (customizable)
- Detects reconnaissance and scanning patterns early
- Works well as a “network alarm system” for servers and subnets
- Can be extended with community rules and custom rules

### ⚠️ Considerations
- Requires tuning to reduce false positives
- Rule writing needs good understanding of protocols and patterns
- High traffic environments may need performance tuning/resources

---

## 🔥 Why Integrate Snort with Wazuh?

Snort generates alerts locally (terminal/log file). Wazuh ingests Snort logs so that:

- Alerts are visible in a **single SOC dashboard**
- Network alerts can be correlated with endpoint alerts
- SOC analysts avoid switching between multiple tools
- Network detections can feed IR workflows (triage → investigation)

This gives a **network + host** monitoring layer together.

---

## 🔗 Useful References

- Create rules visually using **Snorpy**: **[Snorpy Rule Generator](https://www.cyb3rs3c.net/)**
- Optional rule reference collection for further exploration: **[Snort Rule Collection Reference](https://github.com/ADORSYS-GIS/wazuh-snort/blob/main/rules/snort3.rules)**

---

## 🧭 Implementation Guide (Step-by-Step)

> ✅ This is a self-done project in my SOC ecosystem.  
> Commands are shown inside this guide for clarity.  
> Full sequential command history is also available in `commands.sh`.

---

### ✅ Step 0 — Identify Your Interface and Subnet (Ubuntu EC2 Sensor)

Check network interface and IP:

```bash
ip a
````

Note:

* Interface name (example: `ens5`, `eth0`)
* Private IP (example: `10.0.1.214`)
* Subnet range used as HOME_NET (example: `10.0.1.0/24`)

---

### ✅ Step 1 — Install Required Dependencies

```bash
sudo apt update
sudo apt install -y \
  build-essential \
  libpcap-dev \
  libpcre3-dev \
  libdumbnet-dev \
  zlib1g-dev \
  liblzma-dev \
  openssl \
  libssl-dev
```

---

### ✅ Step 2 — Install Snort

```bash
sudo apt install -y snort
```

During installation, you will be asked to define **HOME_NET** (protected network).

Set it to your EC2 private subnet, for example:

```text
10.0.1.0/24
```

---

### ✅ Step 3 — Verify Snort Installation

```bash
snort -V
```

You should see output similar to:

```text
Snort Version 2.9.x ...
```

---

### ✅ Step 4 — Locate Config, Rules, and Logs

Important paths:

* Main config:

  * `/etc/snort/snort.conf`
* Default rule directory:

  * `/etc/snort/rules/`
* Local custom rules:

  * `/etc/snort/rules/local.rules`
* Logs:

  * `/var/log/snort/`

---

### ✅ Step 5 — Create First Custom Rule (ICMP Ping)

Edit local rules:

```bash
sudo nano /etc/snort/rules/local.rules
```

Add:

```conf
alert icmp any any -> $HOME_NET any (msg:"CUSTOM ICMP Ping Detected"; sid:1000001; rev:1;)
```

Save and exit.

---

### ✅ Step 6 — Validate Configuration (Syntax Test)

```bash
sudo snort -T -c /etc/snort/snort.conf
```

Expected:

```text
Snort successfully validated the configuration!
```

---

### ✅ Step 7 — Run Snort in IDS Mode (Console Alerts)

Replace `<interface>` with your actual interface name:

```bash
sudo snort -q -A console -c /etc/snort/snort.conf -i <interface>
```

Keep this running.

---

### ✅ Step 8 — Generate ICMP Traffic (Test Rule)

Run a ping test (from the same host or another host):

```bash
ping -c 3 8.8.8.8
```

Expected Snort alert:

```text
[**] CUSTOM ICMP Ping Detected [**]
```

---

## 🧪 Improving ICMP Rules (Echo Request vs Echo Reply)

Edit local.rules again:

```bash
sudo nano /etc/snort/rules/local.rules
```

Add:

```conf
# Echo Request (Outbound)
alert icmp $HOME_NET any -> any any (msg:"ICMP Echo Request Detected"; itype:8; sid:1000003; rev:1;)

# Echo Reply (Inbound)
alert icmp any any -> $HOME_NET any (msg:"ICMP Echo Reply Detected"; itype:0; sid:1000002; rev:1;)
```

Validate:

```bash
sudo snort -T -c /etc/snort/snort.conf
```

Run Snort again and re-test ping.

---

## 🧩 Step 9 — Create Rules Using Snorpy (GUI)

Use Snorpy to generate a TCP rule visually:

🧠 Rule builder: **[Snorpy Rule Generator](https://www.cyb3rs3c.net/)**

Example FTP rule settings:

* Action: `alert`
* Protocol: `tcp`
* Source IP/Port: `any/any`
* Direction: `->`
* Destination IP: `$HOME_NET`
* Destination Port: `21`
* Message: `FTP Authentication Attempt`
* SID: `1000004`
* REV: `1`

Generated rule:

```conf
alert tcp any any -> $HOME_NET 21 (msg:"FTP Authentication Attempt"; sid:1000004; rev:1;)
```

---

### ✅ Step 10 — Add Snorpy Rule to Snort

```bash
sudo nano /etc/snort/rules/local.rules
```

Add:

```conf
alert tcp any any -> $HOME_NET 21 (msg:"FTP Authentication Attempt"; sid:1000004; rev:1;)
```

Validate:

```bash
sudo snort -T -c /etc/snort/snort.conf
```

---

### ✅ Step 11 — Simulate Attacker Activity (FTP Attempt from Kali)

From Kali Linux:

```bash
ftp <SNORT_PRIVATE_IP> 21
```

Example:

```bash
ftp 10.0.1.214 21
```

Even if refused, the attempt generates traffic that Snort can detect.

---

### ✅ Step 12 — Confirm Detection on Snort Console

You should see alerts similar to:

```text
FTP Authentication Attempt [**] {TCP} <kali-ip>:<srcport> -> <snort-ip>:21
```

---

## 🧾 Step 13 — Enable Snort Fast Alert Logging

Edit config:

```bash
sudo nano /etc/snort/snort.conf
```

Ensure output plugin is enabled:

```conf
output alert_fast: snort.alert.fast
```

Snort fast alert log path:

```text
/var/log/snort/snort.alert.fast
```

Live view:

```bash
tail -f /var/log/snort/snort.alert.fast
```

---

## 🔗 Step 14 — Integrate Snort Alerts into Wazuh (Agent Side)

Edit Wazuh agent config:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/snort/snort.alert.fast</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent
```

---

## ✅ Step 15 — Validate Alerts in Wazuh Dashboard

Trigger alerts (ICMP/FTP).

In Wazuh Dashboard:

* Go to **Security Events**
* Filter by the Snort host/agent
* Confirm Snort alerts are visible

You can correlate what Snort wrote locally:

```bash
tail -f /var/log/snort/snort.alert.fast
```

---

## 🧱 Optional Enhancement — Add Custom Rule Pack + Wazuh Decoder/Rules

> These are optional improvements I prepared to make the integration more SOC-friendly:
>
> * A clean Snort custom rule pack
> * A Wazuh decoder + ruleset to parse Snort fast alerts into structured fields

✅ These are included in this repository under:

* `snort/rules/snort_custom_lab.rules`
* `wazuh/decoders/snort_decoders.xml`
* `wazuh/rules/snort_rules.xml`

---

## 📈 Results

This project successfully achieved:

* ✅ Snort installed and configured correctly on Ubuntu EC2
* ✅ Custom rule writing + testing (ICMP + FTP)
* ✅ Rule creation using GUI tool (Snorpy)
* ✅ Attacker simulation from Kali Linux
* ✅ Snort alerts written to fast log format
* ✅ Wazuh ingested Snort alerts for centralized SOC visibility
* ✅ (Optional) Better parsing + severity using custom Wazuh decoder/rules

---

## 🧠 What I Learned

* How network intrusion detection works in practice (rule-based)
* Snort rule syntax + testing workflow (`snort -T`)
* Difference between generating traffic and verifying detection
* Why centralized SIEM ingestion makes detections more operational
* How Wazuh can unify endpoint + network detections

---

## 🌍 Why This Matters

Network-based detection is critical because many attacks begin with:

* Reconnaissance (scans, probes)
* Protocol abuse and brute-force attempts
* Exploit delivery attempts hitting network services

Snort detects those patterns at the network layer, and Wazuh brings them into a single SOC dashboard for investigation and correlation.

---

## 🧩 Real-World Applications

* Detect scanning and reconnaissance against servers
* Monitor exposed services (SSH/FTP/HTTP) for suspicious behavior
* Reduce blind spots by adding network telemetry to SOC visibility
* Support incident response through correlated alerts inside SIEM

---

## ✅ Project Outcome

By integrating Snort with Wazuh, network-layer alerts became:

* Searchable
* Centralized
* Correlatable
* SOC-ready for triage and investigation

---

## 📁 Repository Structure

```
16-snort-ids-wazuh-integration/
├── README.md
├── commands.sh
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
├── snort/
│   ├── rules/
│   │   ├── local.rules
│   │   └── snort_custom_lab.rules
│   └── notes/
│       └── snort_paths_and_logs.txt
├── wazuh/
│   ├── agent/
│   │   └── ossec.conf.snippet.xml
│   ├── decoders/
│   │   └── snort_decoders.xml
│   └── rules/
│       └── snort_rules.xml
└── docs/
    └── Snort Network Monitoring with Custom Rules and Wazuh SIEM Integration.pdf
```

---

## 📎 PDF Guide

For the full step-by-step PDF with screenshots and validation, see:

📄 **[Snort + Wazuh Integration PDF Guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/16-snort-ids-wazuh-integration/doc/Snort%20Network%20Monitoring%20with%20Custom%20Rules%20and%20Wazuh%20SIEM%20Integration.pdf)**

---
