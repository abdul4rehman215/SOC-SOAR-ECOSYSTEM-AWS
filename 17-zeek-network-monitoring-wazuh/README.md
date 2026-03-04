# 👁️ Zeek Network Security Monitoring + Threat Detection Integrated with Wazuh SIEM

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/zeek01.png" alt="Zeek Logo" width="300" />

  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/wazuh.png" alt="Wazuh Logo" width="300" />
</p>

---

## 📌 Project Overview

Modern SOC monitoring can’t rely only on endpoint logs or signature IDS alerts.  
To understand **what is really happening on the network**—who is talking to whom, which protocols are used, suspicious DNS, scanning activity, TLS anomalies, rejected connections—you need **Network Security Monitoring (NSM)** visibility.

This project deploys **Zeek** as a **network traffic analysis engine** and integrates its logs into **Wazuh SIEM** for:

- ✅ Centralized alerting & correlation
- ✅ Custom detections (rules)
- ✅ SOC-ready dashboards (visual monitoring)
- ✅ Investigation context (not just alerts)

**Snort = alarm system 🚨 (fast, signature/rule-based)**  
**Zeek = surveillance + forensics 🔍 (high-fidelity network context)**  
**Wazuh = correlation + SOC dashboards 🧠**

---

## 🧩 Role in My SOC Ecosystem

This project extends my SOC ecosystem beyond “detect known bad” into **deep network visibility**:

- Snort answers: **“Does this traffic match a known rule?”**
- Zeek answers: **“What is actually happening on the network?”**
- Wazuh correlates: **network + host telemetry in one place**

This adds SOC capabilities like:

- DNS activity monitoring & abuse hunting
- Recon/scan detection (REJ spikes, port scan behavior)
- SSL/TLS certificate anomaly detection (self-signed/expired)
- Rejected connections timeline (situational awareness)
- Top talkers, protocol distribution, and network trends

---

## 🎯 Objectives

By completing this project, I was able to:

- Install and configure Zeek as an NSM sensor
- Configure Zeek monitoring scope (interface + internal networks)
- Enable **JSON logging** for structured, SIEM-friendly ingestion
- Deploy and run Zeek continuously using `zeekctl`
- Integrate Zeek logs into Wazuh via agent log monitoring
- Build custom **Wazuh decoders** and **rules** for:
  - DNS activity alerts
  - Rejected connections + scan detection
  - TLS anomalies (self-signed and expired certs)
- Validate detections using real test scenarios
- Build SOC-ready dashboards for network visibility

---

## 🧰 Prerequisites

- Basic Linux CLI and file editing (`nano`)
- Understanding of:
  - DNS, TCP/UDP, ports, TLS basics
- Wazuh basics:
  - Agent config (`ossec.conf`)
  - Manager rules understanding (restart after changes)
- Access to:
  - Ubuntu endpoint (Zeek sensor)
  - Wazuh SIEM stack (manager + dashboard)
  - Optional Kali machine for recon simulation

---

## 🧪 Environment

| Component | Details |
|----------|---------|
| Sensor | Ubuntu (AWS EC2) running Zeek + Wazuh Agent |
| SIEM | Wazuh Manager + Wazuh Dashboard (OpenSearch) |
| Attacker simulation | Kali Linux (optional but used for scan testing) |
| Zeek logs path | `/opt/zeek/logs/current/` |
| Log format | JSON (`json-logs.zeek`) |
| Style | Mostly terminal-based + Wazuh Dashboard GUI supported |

---

## 🏗️ Architecture Overview

### 🖼️ Zeek → Wazuh SOC Flow Diagram
<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/Zeek%2C%20Wazuh%2C%20and%20TheHive%20integration%20diagram.png" alt="Zeek + Wazuh + TheHive integration diagram" width="900" />
</p>

### 🔁 High-Level Data Flow
```

Network Traffic (real)
│
▼
Zeek Sensor (passive monitoring + high-fidelity logs)
│
│ JSON logs (conn.log, dns.log, ssl.log, ...)
▼
Wazuh Agent (log collection via <localfile>)
│
▼
Wazuh Manager (decoding + rules + alerts)
│
▼
OpenSearch (indexing)
│
▼
Wazuh Dashboard (visibility + hunting)
│
▼
SOC Analyst (context + investigation)

````

---

## 🧠 What is Zeek?

**Zeek (formerly Bro)** is an open-source **passive network traffic analyzer** and security monitoring framework that generates **high-fidelity structured logs** describing network behavior (connections, DNS, HTTP, TLS, files, etc.).

Zeek is not a “blocker.” It is **visibility and evidence**:
- Who talked to whom
- What protocol
- What ports
- What certificates
- What DNS queries
- What connection outcomes (e.g., REJ)

---

## ✅ Why Zeek is Valuable for Security Monitoring

### ⭐ What Zeek Adds Beyond IDS Alerts
- **Deep context** (metadata-rich logs)
- **Behavior visibility** (not only signature matches)
- **Forensic trail** for incident reconstruction
- **Protocol-level understanding** (DNS/TLS/HTTP/Conn)

### ⚠️ Considerations
- Works best with:
  - proper tuning of “internal networks”
  - JSON logging
  - good SIEM parsing/rules
- High volume environments require storage and retention planning

---

## 🔥 Why Integrate Zeek with Wazuh?

Zeek logs are powerful, but SOC teams need:
- Central visibility
- Alerting
- Correlation
- Dashboards

Wazuh provides:
- JSON ingestion + indexing
- Rule-based detection and severity
- Dashboards for monitoring and threat hunting

Together:
- **Zeek = network surveillance & evidence**
- **Wazuh = SOC operations layer (alerts + correlation + visuals)**

---

## 🔗 Useful Official References (Embedded)

- Official Wazuh reference implementation: **[Network security monitoring with Wazuh and Zeek](https://wazuh.com/blog/network-security-monitoring-with-wazuh-and-zeek/)**
- Zeek official installation documentation (alternative methods): **[Zeek installation options](https://docs.zeek.org/en/current/install.html)**

---

## 🧭 Implementation Guide (Step-by-Step)

> ✅ This is a self-done project inside my SOC ecosystem.  
> Commands are shown inside this guide for a beginner-friendly walkthrough.  
> Full sequential command history is also available in `commands.sh`.

---

### ✅ Step 1 — Add Zeek Repository + GPG Key (Ubuntu)

```bash
echo 'deb http://download.opensuse.org/repositories/security:/zeek/Ubuntu_24.04/ /' | sudo tee /etc/apt/sources.list.d/security:zeek.list
curl -fsSL https://download.opensuse.org/repositories/security:zeek/Ubuntu_24.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null
sudo apt update -y
````

---

### ✅ Step 2 — Install Zeek

```bash
sudo apt install zeek -y
```

---

### ✅ Step 3 — Postfix Configuration Prompt (During Install)

During installation, Postfix configuration may appear. Choose:

* **Internet Site**
* System mail name: your hostname/FQDN (e.g., `thehive`, `zeek-sensor`, etc.)

> This is dependency-related and does not change Zeek’s monitoring behavior.

---

### ✅ Step 4 — Add Zeek to PATH + Verify

```bash
echo "export PATH=\$PATH:/opt/zeek/bin" >> ~/.bashrc
source ~/.bashrc
zeek --version
```

---

### ✅ Step 5 — Configure Zeek Node Settings (`node.cfg`)

Find your network interface:

```bash
ip a
```

Edit node configuration:

```bash
sudo nano /opt/zeek/etc/node.cfg
```

Example standalone node:

```ini
[zeek]
type=standalone
host=localhost
interface=ensX0
```

✅ Replace `ensX0` with your real interface (e.g., `ens5`, `eth0`).

---

### ✅ Step 6 — Define Internal Networks (`networks.cfg`)

Edit:

```bash
sudo nano /opt/zeek/etc/networks.cfg
```

Add your internal ranges (example):

```ini
10.0.1.0/24      AWS-Internal-Network
192.168.1.0/24   Home-LAN
```

**Why this matters:** Zeek uses this to classify traffic as internal vs external—critical for correct detection logic.

---

### ✅ Step 7 — Enable JSON Log Output (IMPORTANT)

Wazuh ingestion is easiest when Zeek outputs JSON.

Edit:

```bash
sudo nano /opt/zeek/share/zeek/site/local.zeek
```

Add:

```zeek
@load policy/tuning/json-logs.zeek
```

---

### ✅ Step 8 — Validate Zeek Configuration

```bash
sudo zeekctl check
```

Expected:

* Zeek scripts OK / configuration OK

---

### ✅ Step 9 — Deploy and Start Zeek

```bash
sudo zeekctl deploy
```

Zeek logs will be generated under:

```text
/opt/zeek/logs/current/
```

Quick verify:

```bash
ls -lah /opt/zeek/logs/current/
```

You should see logs like:

* `conn.log`
* `dns.log`
* `ssl.log`
* `http.log` (depends on traffic)

---

# 🔗 Wazuh Integration

## ✅ Step 10 — Configure Wazuh Agent to Monitor Zeek Logs

On the Zeek sensor where Wazuh agent is installed:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/opt/zeek/logs/current/*.log</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent
```

---

## ✅ Step 11 — Create Wazuh Decoders (GUI + Terminal)

> In this project, decoders were created using Wazuh Dashboard GUI, but for GitHub reproducibility I also provide the terminal-based method.

### 🧭 Option A — GUI Method (Wazuh Dashboard)

1. Go to: **Server management → Decoders**
2. Create a new decoders file (example: `zeek_decoders.xml`)
3. Paste the decoder content (provided in this repo under `wazuh/decoders/zeek_decoders.xml`)
4. Save and deploy changes

### 🧰 Option B — Terminal Method (Recommended for GitHub reproducibility)

On Wazuh Manager:

```bash
sudo nano /var/ossec/etc/decoders/zeek_decoders.xml
```

✅ Use the full decoder content provided in this repo:

* `wazuh/decoders/zeek_decoders.xml`

Restart manager:

```bash
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager
```

---

## ✅ Step 12 — Create Wazuh Rules (GUI + Terminal)

### 🧭 Option A — GUI Method (Wazuh Dashboard)

1. Go to: **Server management → Rules**
2. Create a new rules file (example: `zeek_rules.xml`)
3. Paste the rules content (provided in this repo under `wazuh/rules/zeek_rules.xml`)
4. Save and deploy changes

### 🧰 Option B — Terminal Method (Recommended for GitHub reproducibility)

On Wazuh Manager:

```bash
sudo nano /var/ossec/etc/rules/zeek_rules.xml
```

✅ Use the full rules content provided in this repo:

* `wazuh/rules/zeek_rules.xml`

Restart manager:

```bash
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager
```

---

# 🧪 Detection & Validation Tests (Traffic Simulation)

## ✅ Step 13 — Test DNS Query Activity (Generate `dns.log`)

On Zeek sensor:

```bash
dig wazuh.com
dig virustotal.com
```

Verify log updates:

```bash
tail -n 20 /opt/zeek/logs/current/dns.log
```

### ✅ Step 14 — Confirm DNS Alerts in Wazuh

In Wazuh Dashboard → Security Events / Threat Hunting:

* Filter by: `rule.groups : zeek`
* Or filter by rule id (example): `rule.id : 100901`

---

## ✅ Step 15 — Test Recon / Port Scan Behavior (From Kali)

From Kali attacker machine:

```bash
for port in {5555..5559}; do nc -zv <TARGET_IP> $port || true; done
```

This generates rejected connections (REJ) in `conn.log`.

### ✅ Step 16 — Confirm Scan / REJ Alerts in Wazuh

Filter:

* `rule.groups : zeek`
* `rule.id : 100903` (single REJ)
* `rule.id : 100904` (5+ REJ in 20 seconds — scan behavior)

---

## ✅ Step 17 — Test SSL/TLS Certificate Anomalies

On Zeek sensor:

```bash
curl -k https://self-signed.badssl.com/
curl -k https://expired.badssl.com/
```

Verify `ssl.log` updates:

```bash
tail -n 20 /opt/zeek/logs/current/ssl.log
```

### ✅ Step 18 — Confirm TLS Alerts in Wazuh

Filter:

* `rule.groups : zeek`
* `rule.id : 100906` (self-signed)
* `rule.id : 100907` (expired)

---

# 📊 SOC Dashboard Build (Wazuh Dashboard / OpenSearch)

Dashboards are critical in real SOC environments because analysts need **visual context**, not only alerts.

## ✅ Step 19 — Create SOC Dashboard for Zeek Visibility

Go to:

* **Dashboards → Create dashboard → Add panels**

Use index pattern:

* `wazuh-alerts-*`

Recommended global filter:

* `rule.groups : zeek`

Below are the core visuals built in this project (9 panels):

---

### 📌 Visual 1 — Metric: Total Network Events

* **Type:** Metric
* **Metric:** Count
* **Name:** `Total Network Events`

---

### 📌 Visual 2 — Line: Network Activity Over Time

* **Type:** Line
* **Y:** Count
* **X:** Date Histogram (`@timestamp`, interval Auto/1m)
* **Name:** `Network Activity Over Time`

---

### 📌 Visual 3 — Pie: Protocol Distribution

* **Type:** Pie
* **Metric:** Count
* **Bucket:** Terms → Field `protocol` (or `data.protocol` depending on indexing)
* **Name:** `Protocol Distribution`

---

### 📌 Visual 4 — Table: Top Source IPs

* **Type:** Data Table
* **Metric:** Count
* **Split Rows:** Terms → `srcip` (or `data.srcip`) size 10
* **Name:** `Top Source IPs`

---

### 📌 Visual 5 — Table: Top Destination IPs

* **Type:** Data Table
* **Metric:** Count
* **Split Rows:** Terms → `dstip` (or `data.dstip`) size 10
* **Name:** `Top Destination IPs`

---

### 📌 Visual 6 — Bar/Line: Rejected Connections Timeline

* **Type:** Line or Bar
* **Filter:** `rule.id : 100903`
* **X:** Date histogram (`@timestamp`)
* **Name:** `Rejected Connections Over Time`

---

### 📌 Visual 7 — Bar/Line: Port Scan Activity

* **Type:** Line or Bar
* **Filter:** `rule.id : 100904`
* **X:** Date histogram
* **Name:** `Port Scan Activity Over Time`

---

### 📌 Visual 8 — Table: SSL/TLS Certificate Issues

* **Type:** Data Table
* **Filter:** `rule.id : 100906 OR rule.id : 100907`
* **Split Rows:** `dstip`, optionally `ssl_validation_status`
* **Name:** `TLS Certificate Issues`

---

### 📌 Visual 9 — Raw Events Table (Threat Hunting View)

* **Type:** Data Table
* Suggested columns:

  * `rule.description`
  * `srcip`, `dstip`, `dstport`
  * `protocol`
  * `dnsquery` (when present)
  * `ssl_validation_status` (when present)
* **Name:** `Raw Network Events`

---

## ✅ Results

This project successfully achieved:

* ✅ Zeek installed + configured correctly
* ✅ JSON logs enabled for SIEM ingestion
* ✅ Wazuh ingested Zeek logs from `/opt/zeek/logs/current/*.log`
* ✅ Custom decoders + rules created for real network detections
* ✅ Validated detections using DNS, scan, and TLS anomaly tests
* ✅ Built SOC dashboards for network visibility and threat hunting

---

## 🧠 What I Learned

* Zeek provides “network stories,” not just alerts
* JSON logging makes NSM pipelines and SIEM parsing easier
* Proper internal network scoping improves detection accuracy
* Wazuh rules can convert raw Zeek telemetry into SOC-ready detections
* Dashboards are the final step to make NSM operational for analysts

---

## 🌍 Why This Matters

In real SOC environments:

* Analysts need **context** to investigate incidents quickly
* Zeek gives deep network metadata that improves hunting and forensics
* SIEM visibility must go beyond endpoint logs
* Dashboards convert raw data into actionable monitoring workflows

This project helped me move from **detecting attacks** to **understanding network behavior at scale**.

---

## 🧾 Repository Structure

```
17-zeek-network-monitoring-wazuh/
├── README.md
├── commands.sh
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
├── zeek/
│   ├── configs/
│   │   ├── node.cfg
│   │   ├── networks.cfg
│   │   └── local.zeek
│   └── notes/
│       └── zeek_paths_and_logs.txt
├── wazuh/
│   ├── agent/
│   │   └── ossec.conf.snippet.xml
│   ├── decoders/
│   │   └── zeek_decoders.xml
│   └── rules/
│       └── zeek_rules.xml
├── dashboards/
│   ├── Zeek – Network Security Monitoring & Threat Hunting.ndjson
│   └── zeek-soc-dashboard-build-guide.md
└── docs/
    └── zeek-wazuh-nsm.pdf
```

---

## 📎 PDF Guide

For the full step-by-step PDF with screenshots and validation, see:
📄 **[Zeek + Wazuh NSM PDF Guide](docs/zeek-wazuh-nsm.pdf)**

---


