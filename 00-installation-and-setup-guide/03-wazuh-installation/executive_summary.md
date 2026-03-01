# 📄 Executive Summary — Wazuh All-in-One Installation (AWS EC2)

## Project Title
**Wazuh SIEM/XDR All-in-One Deployment on AWS EC2 (Manager + Indexer + Dashboard)**

---

## 📌 Summary
In this project, I deployed a complete **Wazuh SIEM/XDR** stack on a dedicated AWS EC2 instance using the **official Wazuh installation assistant**. The deployment was built as an **All-in-One** node (Manager + Indexer + Dashboard + Filebeat), then stabilized using a SOC-ready baseline configuration (`ossec.conf`) to support future SOC operations, endpoint onboarding, and ecosystem integrations.

---

## 🎯 Objective
- Install Wazuh All-in-One on AWS EC2 using an official supported method  
- Ensure secure and reliable dashboard access over HTTPS  
- Apply a stable SOC baseline configuration to support:
  - JSON logging and full event visibility
  - vulnerability detection
  - compliance scanning (SCA)
  - file integrity monitoring (FIM)
  - agent enrollment readiness
  - future AWS + IOC list preparation

---

## 🧱 Environment & Requirements
- **Cloud:** AWS EC2  
- **OS:** Ubuntu 24.04 LTS  
- **Instance:** `t2.large` / `t3.large` recommended  
- **Resources Used (stable):**
  - **2 vCPU**
  - **8 GB RAM**
  - **100 GB storage** (gp3 recommended)
- **Network Access:**
  - SSH (22) restricted to admin IP  
  - Dashboard (443) restricted to admin IP/VPN  
  - Agent ports (1514/1515) planned for trusted subnets only

---

## ✅ Work Completed
### 1) Deployment
- Downloaded and executed:
  - `wazuh-install.sh -a`
- Installed components:
  - Wazuh Manager
  - Wazuh Indexer
  - Wazuh Dashboard
  - Filebeat forwarding pipeline

### 2) SOC Baseline Configuration
- Backed up default config
- Applied stable `ossec.conf` baseline including:
  - JSON output enabled
  - Rootcheck enabled (with Docker directory ignores)
  - Syscollector inventory enabled
  - SCA compliance enabled
  - Vulnerability detection enabled (Canonical/Debian/MSU/NVD)
  - FIM (syscheck) enabled
  - Authd enrollment enabled on port 1515
  - Ruleset lists staged for AWS + IOC workflows

### 3) Validation
- Verified core services running:
  - `wazuh-manager`
  - `filebeat`
  - dashboard/indexer services (where applicable)
- Verified logs:
  - `/var/ossec/logs/ossec.log`
- Verified dashboard access via HTTPS:
  - login successful using installer-generated credentials

---

## 🧪 Validation Checklist (Completed)
- ✅ Dashboard reachable at `https://<EC2_PUBLIC_IP>`
- ✅ Wazuh Manager running (`systemctl status wazuh-manager`)
- ✅ Filebeat running (`systemctl status filebeat`)
- ✅ Wazuh logs active (`tail /var/ossec/logs/ossec.log`)
- ✅ Ports locally available (443, 1514, 1515, 55000, 9200 as applicable)

---

## 📈 Result
A stable Wazuh SIEM/XDR environment was successfully deployed on AWS EC2 and prepared as the core component of the SOC ecosystem. This Wazuh instance is now ready for the next portfolio projects including:
- agent onboarding (Windows Sysmon / Linux telemetry)
- AWS CloudTrail ingestion and monitoring
- integration with TheHive, Cortex, and MISP
- IDS/NSM pipeline integration (Suricata/Zeek/Snort)
- rule tuning and alert fatigue reduction workflows

---

## 🌍 Why This Matters
Wazuh provides the central SOC capability for:
- detection and alerting
- endpoint visibility
- compliance posture monitoring
- vulnerability insights
- investigation support with searchable indexed telemetry

A correct deployment and stable configuration is essential before building any advanced SOC workflows or integrations.

---

## 🔜 Next Steps
- Deploy TheHive (case management) and integrate with Wazuh
- Deploy MISP and enable threat intel-based detection
- Add endpoint agents (Windows Sysmon + Linux telemetry)
- Begin custom rule engineering and alert tuning
- Add CloudTrail monitoring and network IDS integrations

---
