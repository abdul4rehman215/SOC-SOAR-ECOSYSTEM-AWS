# 🛡️ Wazuh SIEM/XDR Installation Guide (AWS EC2)
### SOC-SOAR Ecosystem Core Detection Engine

<div align="center">

![Wazuh Logo](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/wazuh.png)

</div>

---

# 📌 What is Wazuh?

Wazuh is an open-source XDR (Extended Detection & Response) and SIEM platform designed for:

- Threat detection
- Log analysis
- File integrity monitoring
- Vulnerability detection
- Compliance monitoring (PCI-DSS, CIS, GDPR, HIPAA)
- Cloud workload protection
- Endpoint security monitoring

Wazuh provides unified visibility across:

- Endpoints (Linux / Windows / macOS)
- Cloud (AWS, Azure, GCP)
- Containers
- Network devices
- Applications

---

# 🏗️ Wazuh Core Components

Wazuh consists of:

1️⃣ **Wazuh Server (Manager)**  
- Receives agent logs  
- Applies decoders and rules  
- Generates alerts  

2️⃣ **Wazuh Indexer**  
- Stores alerts and events  
- Based on OpenSearch  
- Provides search & analytics  

3️⃣ **Wazuh Dashboard**  
- Web UI  
- Data visualization  
- SOC dashboards  

4️⃣ **Wazuh Agents**  
- Installed on monitored endpoints  
- Collect logs & telemetry  

---

# 🌐 Deployment Architecture

## 📊 Wazuh Deployment Model

![Wazuh Deployment Architecture](https://documentation.wazuh.com/current/_images/deployment-architecture1.png)

## 🔄 Components & Data Flow

![Wazuh Components and Data Flow](https://documentation.wazuh.com/current/_images/wazuh-components-and-data-flow1.png)

---

# 🎯 Objective

- Deploy Wazuh all-in-one stack
- Configure SOC-stable production configuration
- Enable vulnerability detection
- Enable FIM
- Enable compliance monitoring
- Enable AWS integration
- Validate services
- Prepare for agent onboarding

---

# 🖥️ EC2 Requirements

## Recommended Instance

| Resource | Value |
|----------|-------|
| Instance Type | t2.large / t3.large |
| RAM | 8 GB |
| vCPU | 2 |
| Storage | 100 GB |
| OS | Ubuntu 24.04 LTS |
| Public IP | Enabled |

⚠️ Less than 8GB RAM may cause:
- Indexer crash
- Dashboard instability
- High memory swap usage

---

# 🔐 Required Security Group Ports

| Component | Port | Protocol | Purpose |
|------------|------|----------|---------|
| Agent Connection | 1514 | TCP | Agent data |
| Agent Enrollment | 1515 | TCP | Agent registration |
| REST API | 55000 | TCP | Wazuh API |
| Indexer API | 9200 | TCP | OpenSearch |
| Cluster | 9300-9400 | TCP | Indexer cluster |
| Dashboard | 443 | TCP | Web UI |

Inbound rules required:

- 1514 TCP → Agent networks
- 1515 TCP → Agent networks
- 55000 TCP → Local/VPN
- 9200 TCP → Internal only
- 443 TCP → Admin IP only

Outbound:
- Allow all

---

# 🧠 PHASE 1 – WAZUH INSTALLATION

# 🔄 Time & Host Configuration (MANDATORY BEFORE INSTALLATION)

📌 Refer to:

[time and hostname setup guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/tree/main/00-installation-and-setup-guide/01-aws-ec2-infrastructure-setup#-post-launch-server-standardization)


## 1️⃣ Install Wazuh Using Official Assistant

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
sudo bash ./wazuh-install.sh -a
````

This installs:

* Wazuh Manager
* Wazuh Indexer
* Wazuh Dashboard
* Filebeat

At the end of installation, credentials are displayed:

- Username: admin

- Password: auto-generated

- Save securely.

---

# 🌐 PHASE 2 – Dashboard Access

Access:

```
https://<EC2-PUBLIC-IP>
```

* Accept SSL warning
* Login using generated credentials

---

# ⚙️ PHASE 3 – SOC Stable Configuration

File:

```
/var/ossec/etc/ossec.conf
```

Purpose:

* Enable JSON logging
* Enable vulnerability detection
* Enable SCA compliance
* Enable FIM
* Enable AWS lists
* Enable IOC lists
* Enable secure agent connection

Configuration file included separately in this repository as:

```
ossec.conf
```

---

# 🧪 PHASE 4 – Validation Checklist

Run in this order:

```bash
systemctl status wazuh-manager
systemctl status wazuh-indexer
systemctl status wazuh-dashboard
systemctl status filebeat
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
* AWS logs (if integrated)

---

# 🚨 Most Common Failures

| Problem               | Root Cause       |
| --------------------- | ---------------- |
| Dashboard down        | Port 443 blocked |
| Indexer crash         | Low memory       |
| Agents not connecting | 1514 blocked     |
| Enrollment fails      | 1515 blocked     |
| API unreachable       | 55000 blocked    |

---

# 🏁 Final Advice

* Backup ossec.conf before editing
* Restart only wazuh-manager after config changes
* Never edit indexer config without backup
* Monitor RAM usage regularly

---

# 🏢 Real-World Use Cases

* SOC monitoring
* Threat hunting
* Cloud workload monitoring
* Compliance reporting
* Malware detection
* File integrity monitoring
* Log centralization

---

# 🌍 Why This Matters

Wazuh is the core detection engine in this SOC ecosystem.

Everything integrates with it:

* MISP
* TheHive
* Cortex
* Suricata
* Zeek
* AWS CloudTrail
* VirusTotal
* n8n automation

Without stable Wazuh deployment:
No SOC.

---

## 🧩 Real-World Applications

* SOC Analyst monitoring and alert triage
* SOC Engineering deployments (SIEM build + tuning)
* Threat hunting using security event telemetry
* Vulnerability management visibility
* Compliance posture validation (CIS/SCA)

---

# 📁 Repository Structure

```
03-wazuh-installation/
├── README.md
├── commands.sh
├── ossec.conf
├── troubleshooting.md
├── architecture-notes.txt
└── interview_qna.md
```

---

# ✅ Result

* Wazuh all-in-one stack deployed successfully on AWS EC2
* SOC-ready configuration applied
* Dashboard accessible via HTTPS
* Services validated

Host Ready for integration with:

  * agent onboarding
  * vulnerability detection
  * compliance scanning
  * FIM monitoring
  * future SOC SOAR integrations

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
