# 🛡️ Project 03 — Wazuh All-in-One Installation on AWS EC2 (Manager + Indexer + Dashboard)

<div align="center">

![Wazuh Logo](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/icons/wazuh.png)

</div>

> **Goal:** Deploy a complete **Wazuh SIEM/XDR stack** on AWS EC2 (All-in-One) and apply a **SOC-stable configuration** (`ossec.conf`) ready for agent onboarding, visibility dashboards, and future integrations.

---

## 📌 Project Summary

This project documents how I installed **Wazuh (All-in-One)** on a dedicated AWS EC2 instance using the **official Wazuh installation assistant**, then applied a stable SOC configuration baseline.

✅ Installed components:
- Wazuh Manager (analysis engine + rules + agent management)
- Wazuh Indexer (search/storage)
- Wazuh Dashboard (web UI)
- Filebeat (ships alerts/events manager → indexer)

---

## 🎯 Objective

By the end of this project, I was able to:

- Deploy Wazuh all-in-one stack
- Access the dashboard securely over HTTPS
- Apply a SOC-stable production-style `ossec.conf`
- Enable:
  - JSON logging
  - vulnerability detection
  - SCA compliance checks
  - FIM monitoring
  - secure agent connection + enrollment readiness
  - lists prepared for AWS + IOC workflows
- Validate services + logs + dashboard visibility

---

## 🧠 What is Wazuh?

Wazuh is an open-source **SIEM/XDR** platform used to:
- collect and analyze security telemetry
- detect threats using rules/decoders
- monitor file integrity, configuration posture, and vulnerabilities
- support regulatory compliance and SOC operations
- manage endpoints via Wazuh agents (Windows/Linux/macOS)

---

## 🌍 Common Use Cases (SOC Context)

- Endpoint security monitoring (agents)
- Threat intelligence enrichment (IOCs)
- Incident response support (alerts + investigation)
- Compliance monitoring (CIS/SCA policies)
- Vulnerability detection and inventory visibility
- Cloud security monitoring (AWS workloads)

---

# 🌐 Deployment Architecture

## 📊 Wazuh Deployment Model

![Wazuh Deployment Architecture](https://documentation.wazuh.com/current/_images/deployment-architecture1.png)

## 🔁 Components & Data Flow

![Wazuh Components and Data Flow](https://documentation.wazuh.com/current/_images/wazuh-components-and-data-flow1.png)

---

📁 Repository Structure
03-wazuh-installation/
├── README.md
├── commands.sh
├── ossec.conf
├── troubleshooting.md
├── architecture-notes.txt
└── interview_qna.md

--

## 🖥️ EC2 Requirements

### ✅ Recommended Instance (Stable All-in-One)

| Resource | Value |
|---|---|
| Instance Type | `t2.large` / `t3.large` |
| RAM | **8 GB** |
| vCPU | **2** |
| Storage | **100 GB** (gp3 recommended) |
| OS | Ubuntu 24.04 LTS |
| Public IP | Enabled |

⚠️ Less than 8GB RAM may cause:
- Indexer instability/crash
- Dashboard instability
- High swap usage

---

## 🔐 Required Security Group Ports

> Keep ports restricted wherever possible (Admin IP/VPN or internal subnets).

| Component | Port | Protocol | Purpose |
|---|---:|---|---|
| Agent Connection | 1514 | TCP | Agent data (events) |
| Agent Enrollment | 1515 | TCP | Agent registration |
| REST API | 55000 | TCP | Wazuh API |
| Indexer API | 9200 | TCP | Indexer REST API |
| Cluster | 9300–9400 | TCP | Indexer cluster comms (cluster only) |
| Dashboard | 443 | TCP | Web UI |

### ✅ Recommended inbound rules (clean + secure)
- **443/TCP** → Admin IP only (Dashboard)
- **1514/TCP** → Agent networks/subnets only
- **1515/TCP** → Agent networks/subnets only
- **55000/TCP** → Admin IP/VPN only
- **9200/TCP** → Internal only (avoid exposing publicly)

Outbound:
- Allow all (needed for updates, threat intel APIs, package downloads)

---

# 🧠 Component Communication (Summary)

### ✅ Wazuh agent → Wazuh server
- TCP **1514** (agent event communication)
- Enrollment via TCP **1515** (authd)

### ✅ Wazuh server → Wazuh indexer
- Uses **Filebeat** with **TLS**
- Indexer listens on **9200/TCP** (default)

### ✅ Wazuh dashboard → Wazuh server API
- API on **55000/TCP** (TLS + authentication)

### ✅ Wazuh dashboard → Wazuh indexer
- Dashboard queries indexer for visualization/search

---

# 🧱 Implementation Phases

## 🟣 PHASE 1 — Wazuh Installation (Official Assistant)

### 1) Download installer
```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
````

### 2) Install all-in-one

```bash
sudo bash ./wazuh-install.sh -a
```

✅ This installs:

* Wazuh Manager
* Wazuh Indexer
* Wazuh Dashboard
* Filebeat

📌 At the end of installation:

* **Dashboard URL**
* **Username**
* **Password**
  are displayed.

⚠️ Save credentials securely — **do not commit secrets**.

---

## 🌐 PHASE 2 — Dashboard Access

Access:

```text
https://<EC2-PUBLIC-IP>
```

Steps:

* Accept SSL warning (self-signed certificate)
* Login using auto-generated credentials shown at install end

---

## 🛠️ PHASE 3 — SOC Stable Configuration

### File

```text
/var/ossec/etc/ossec.conf
```

### Purpose (What this config enables)

* Enable JSON logging
* Enable vulnerability detection
* Enable SCA compliance
* Enable FIM
* Enable AWS lists preparation
* Enable IOC list support (malware hashes, malicious IPs/domains)
* Enable secure agent connection + enrollment

✅ Configuration file included in this repo:

* `configs/ossec.conf`

### Apply config (with backup)

```bash
sudo cp /var/ossec/etc/ossec.conf /var/ossec/etc/ossec.conf.backup
sudo nano /var/ossec/etc/ossec.conf
```

Restart only manager after changes:

```bash
sudo systemctl restart wazuh-manager
```

---

## ✅ PHASE 4 — Validation Checklist

Run in this order:

```bash
systemctl status wazuh-manager
systemctl status filebeat
systemctl status wazuh-dashboard || true
systemctl status wazuh-indexer || true
```

Check logs:

```bash
tail -n 50 /var/ossec/logs/ossec.log
```

Dashboard validation:

* Agents → Active
* Vulnerabilities tab
* Security Events
* FIM alerts
* AWS logs (if integrated later)

---

## 🚨 Most Common Failures

| Problem               | Root Cause                             |
| --------------------- | -------------------------------------- |
| Dashboard down        | Port **443** blocked in Security Group |
| Indexer crash         | Low memory / high swap                 |
| Agents not connecting | **1514** blocked                       |
| Enrollment fails      | **1515** blocked                       |

---

## ✅ Result

* Wazuh all-in-one stack deployed successfully
* Dashboard accessible via HTTPS
* SOC stable config applied and validated
* Host ready for:

  * agent onboarding
  * vulnerability detection
  * compliance scanning
  * FIM monitoring
  * future SOC integrations

---

## 🌍 Why This Matters

Wazuh acts as the **core SIEM/XDR** layer of the SOC ecosystem.
A correct deployment enables real SOC workflows:

* monitoring and triage
* detection engineering
* compliance visibility
* incident investigation support
* scalable endpoint coverage

---

## 🧩 Real-World Applications

* SOC Analyst monitoring and alert triage
* SOC Engineering deployments (SIEM build + tuning)
* Threat hunting using security event telemetry
* Vulnerability management visibility
* Compliance posture validation (CIS/SCA)

---

## 🏁 Conclusion

This project established a stable Wazuh foundation on AWS EC2 using the official assistant installation method and a SOC-ready configuration baseline. This setup becomes the base for all future projects involving agents, integrations, dashboards, rule tuning, and SOC automation.

---

## 🔗 Official References 

* **Quickstart (fast deployment overview):** [Wazuh Quickstart](https://documentation.wazuh.com/current/quickstart.html)
* **Full Installation Guide (all methods):** [Wazuh Installation Guide](https://documentation.wazuh.com/current/installation-guide/index.html)
* **Deployment Options (single-node, distributed, containers):** [Wazuh Deployment Options](https://documentation.wazuh.com/current/deployment-options/index.html)

Architecture images used:

* [Deployment Architecture Diagram](https://documentation.wazuh.com/current/_images/deployment-architecture1.png)
* [Components & Data Flow Diagram](https://documentation.wazuh.com/current/_images/wazuh-components-and-data-flow1.png)


---
