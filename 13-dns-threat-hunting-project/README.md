# 🛡️ Hunting Malicious DNS Queries from Windows Endpoints

## Using Wazuh + DNS-Stats + AlienVault OTX

### Enterprise SOC DNS Threat Hunting & Enrichment Pipeline

---

# 📌 1. Introduction

DNS is one of the **earliest and most reliable indicators of compromise (IOC)** in any environment.

Before malware performs:

* Command & Control (C2) communication
* Payload downloads
* Data exfiltration
* Phishing callbacks
* Lateral movement beaconing

It must resolve a domain.

This project builds a **real-world SOC-grade DNS threat hunting and enrichment pipeline** that transforms raw DNS logs into:

```
Raw DNS Telemetry → Context → Threat Intelligence → Enriched Alert → SOC Action
```

This implementation integrates:

* **Wazuh SIEM**
* **Sysmon (Event ID 22 – DNS Query)**
* **DNS-Stats (Domain frequency & reputation engine)**
* **AlienVault OTX (Threat Intelligence enrichment)**
* Optional Active Response
* SOC dashboard visualization

This is a **fully terminal-based implementation** except for minimal API key generation in AlienVault.

---

# 🎯 2. Project Objective

This project detects and enriches:

* First-time-seen domains
* Low-frequency domains
* Newly registered domains
* Rare domains
* Suspicious/random domains
* Known malicious domains (via OTX threat intel)

Then it:

* Generates structured enriched alerts in Wazuh
* Maps alerts to MITRE ATT&CK
* Provides analyst-ready context
* Supports automated response if required

---

# 🧠 3. Why DNS Monitoring is Critical in SOC

Traditional SIEM alerts fail because:

* DNS logs are noisy
* Many domains are benign
* Context is missing
* Reputation is unknown
* Analysts must manually pivot to external tools

This project solves that by:

* Enriching DNS telemetry automatically
* Validating against threat intelligence
* Reducing false positives
* Providing investigation-ready alerts

This mirrors enterprise SOC detection engineering practices.

---

# 🧠 4. What is DNS-Stats?

DNS-Stats is a **domain analysis engine** created by Mark Baggett (SANS Instructor).

Official repository:
👉 [Mark Baggett Domain Stats Repository](https://github.com/MarkBaggett/domain_stats)

DNS-Stats provides:

* Domain frequency scoring
* First-seen timestamps
* Domain age analysis
* RDAP lookups
* Historical domain presence
* Reputation categorization

It answers key SOC questions:

> Has this domain ever been seen in our environment?
> Is this domain rare?
> Is it newly registered?
> Is it suspicious?

This dramatically reduces alert fatigue.

---

# 🌐 5. Why AlienVault OTX?

AlienVault OTX (Open Threat Exchange) is a community-based threat intelligence platform.

Official platform:
👉 [AlienVault OTX Threat Intelligence Platform](https://otx.alienvault.com)

OTX provides:

* Malicious domain indicators
* IOC pulses
* Threat actor associations
* Malware infrastructure mapping
* Reputation tagging

In this project, OTX:

* Validates suspicious domains
* Confirms malicious matches
* Adds intelligence context
* Increases alert severity

---

# 🏗️ 6. High-Level Architecture

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/advanced-dns-threat-monitoring-architecture.png">
</p>

### Flow:

```
Windows Endpoint
    │
    ├── Sysmon Event ID 22 (DNS Query)
    │
    ▼
Wazuh Agent
    │
    ▼
Wazuh Manager
    │
    ├── DNS-Stats Integration (Frequency + Reputation)
    │
    ├── Custom Detection Rules
    │
    ├── AlienVault OTX Integration (IOC validation)
    │
    ▼
Wazuh Dashboard
    │
    └── Enriched SOC Alerts
```

---

# 🧱 7. What This Adds to Your SOC Ecosystem

After implementation, your SOC can:

- ✔ Detect rare DNS activity
- ✔ Detect first-time-seen domains
- ✔ Identify suspicious low-frequency domains
- ✔ Validate domains against global threat intel
- ✔ Automatically enrich alerts
- ✔ Map to MITRE ATT&CK
- ✔ Trigger automated actions
- ✔ Reduce analyst triage time
- ✔ Improve MTTD and MTTR

This transforms Wazuh from log collection into a detection engineering platform.

---

# 🛠️ 8. Environment Requirements

## 🖥 Wazuh Manager (Linux)

* Ubuntu 22.04 recommended
* Python 3.10+
* Internet access (for OTX)
* Wazuh installed and running

## 🖥 Windows Endpoint

* Windows 10/11
* Sysmon installed for guide refer link (https)
* Wazuh Agent installed
* DNS logging enabled (Event ID 22)

---

# 📂 9. Repository Structure

```
13-dns-threat-hunting-project/
│
├── README.md
├── commands.sh
├── interview_qna.md
├── troubleshooting.md
│
├── wazuh/
│   ├── ossec.conf_snippets/
│   │   ├── dnsstats_integration.xml
│   │   ├── alienvault_integration.xml
│   │   └── active_response.xml
│   │
│   ├── rules/
│   │   ├── local_dnsstats.xml
│   │   └── local_otx.xml
│   │
│   └── integrations/
│       ├── custom-dnsstats.py
│       ├── custom-dnsstats
│       └── custom-alienvault.py
│
├── windows/
│   ├── otx.ps1
│   └── otx.cmd
│
└── docs/
    └── Hunting Malicious DNS with Wazuh DNS-stats AlienVault OTX.pdf
```

---

# 📘 10. Full Implementation Guide (Step-by-Step)

Now we begin complete implementation.

---

# 🔵 PART 1 — Install DNS-Stats on Wazuh Manager

---

## Step 1 — Install Dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

---

## Step 2 — Clone DNS-Stats

```bash
cd /opt
sudo git clone https://github.com/MarkBaggett/domain_stats.git
cd domain_stats
```

---

## Step 3 — Install DNS-Stats

```bash
sudo pip3 install .
```

This installs:

* Flask
* Gunicorn
* Requests
* RDAP libraries
* SQLite engine

---

## Step 4 — Initialize Database

```bash
sudo mkdir /opt/domain-stats-data
domain_stats --init /opt/domain-stats-data
```

This creates:

* SQLite DB
* Cache files
* Configuration

---

## Step 5 — Start DNS-Stats Service

```bash
cd /opt/domain_stats
gunicorn --bind 127.0.0.1:5730 domain_stats.server:config_app\('/opt/domain-stats-data'\)
```

Expected output:

```
Listening at: http://127.0.0.1:5730
```

---

## Step 6 — Validate Service

```bash
sudo ss -lntp | grep 5730
```

---

## Step 7 — Test API

```bash
curl http://127.0.0.1:5730/google.com
```

Expected JSON response with:

* category
* freq_score
* seen_by_you
* seen_by_web

DNS-Stats is now operational.

---

# 🔵 PART 2 — Wazuh Integration (DNS-Stats)

---

## Step 8 — Create Integration Script

Location:

```
/var/ossec/integrations/custom-dnsstats.py
```

Paste full script (from repo integration folder).

---

## Step 9 — Set Permissions

```bash
sudo chown root:wazuh /var/ossec/integrations/custom-dnsstats.py
sudo chmod 750 /var/ossec/integrations/custom-dnsstats.py
```

---

## Step 10 — Add Integration Block

Edit:

```
/var/ossec/etc/ossec.conf
```

Add:

```xml
<integration>
  <name>custom-dnsstats</name>
  <rule_id>101100</rule_id>
  <alert_format>json</alert_format>
</integration>
```

---

## Step 11 — Add DNS Detection Rules

Create:

```
/var/ossec/etc/rules/local_dnsstats.xml
```

Add full rules (as previously defined).

---

## Step 12 — Restart Wazuh

```bash
sudo systemctl restart wazuh-manager
```

DNS enrichment now active.

---

# 🔵 PART 3 — AlienVault OTX Integration

---

## Step 13 — Create OTX Account

Go to:

👉 [AlienVault OTX Portal](https://otx.alienvault.com)

* Register account
* Login
* Go to Settings
* Copy API Key

---

## Step 14 — Create OTX Integration Script

Location:

```
/var/ossec/integrations/custom-alienvault.py
```

Paste integration script from repository folder.

---

## Step 15 — Set Permissions

```bash
sudo chown root:wazuh /var/ossec/integrations/custom-alienvault.py
sudo chmod 750 /var/ossec/integrations/custom-alienvault.py
```

---

## Step 16 — Add Integration Block

Add in `ossec.conf`:

```xml
<integration>
  <name>custom-alienvault</name>
  <group>dnsstat_alert</group>
  <alert_format>json</alert_format>
</integration>
```

---

## Step 17 — Add OTX Detection Rules

Create:

```
/var/ossec/etc/rules/local_otx.xml
```

Add full rules mapping to MITRE.

---

## Step 18 — Restart Wazuh

```bash
sudo systemctl restart wazuh-manager
```

Full enrichment chain now active.

---

# 🔵 PART 4 — Windows Endpoint Setup

---

## Step 19 — Install Sysmon

Download from:

👉 [Microsoft Sysmon Official Page](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)

Install with DNS logging enabled:

```powershell
Sysmon64.exe -i sysmonconfig.xml
```

Verify Event ID 22 is enabled.

---

## Step 20 — Install Wazuh Agent

Download from:

👉 [Wazuh Official Downloads](https://wazuh.com/downloads)

Install and register with manager.

Verify on manager:

```bash
/var/ossec/bin/agent_control -l
```

Agent must show Active.

---

# 🔵 PART 5 — Testing the Pipeline

---

## Step 21 — Generate DNS Queries

```powershell
Resolve-DnsName suspicious-domain.com
Resolve-DnsName malicious-domain.org
```

---

## Step 22 — Verify Sysmon Event

Check Event Viewer:

Applications and Services Logs
→ Microsoft
→ Windows
→ Sysmon
→ Operational

Confirm Event ID 22 exists.

---

## Step 23 — Observe in Wazuh Dashboard

Expected alert chain:

1. DNS Query detected
2. DNS-Stats enrichment alert
3. OTX IOC validation (if match)

---

# 📊 SOC Analyst View

Alerts now include:

* Domain queried
* Frequency score
* First-seen timestamp
* Reputation category
* OTX pulse count
* MITRE ATT&CK mapping

This is analyst-ready intelligence.

---

# 🏆 Project Outcome

- ✔ Real-world DNS detection pipeline
- ✔ Automatic threat enrichment
- ✔ Threat intelligence validation
- ✔ SOC workflow optimization
- ✔ Reduced manual pivoting
- ✔ Enterprise-grade SOC capability

---

# 📄 PDF Guide Reference

Full illustrated implementation guide available in project PDF: 

👉 **[Click here to view the complete PDF walkthrough guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/13-dns-threat-hunting-project/docs/Hunting%20Malicious%20DNS%20with%20Wazuh%20DNS-stats%20AlienVault%20OTX.pdf)**



This includes:

* Analyzer screenshots
* Dashboard validation
* Case testing workflow
* Multi-analyzer enrichment model

---

# 🏁 Conclusion

This project transforms DNS telemetry into:

* Context-aware alerts
* Intelligence-enriched events
* SOC-ready investigations

It mirrors real enterprise detection engineering practices and significantly enhances your SOC ecosystem.

---

## 🌐 Project Post on LinkedIn

I also shared this project on LinkedIn with a concise portfolio summary, key highlights, and implementation context.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-View%20Project%20Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/abdul4rehman215_hunting-malicious-dns-with-wazuh-dns-stats-activity-7428098163745607680-z3hv?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU)

---

## ⭐ Final Note

This project reflects **real hands-on implementation** focused on practical security workflow execution, technical depth, and portfolio-grade documentation.

It demonstrates the ability to:

> **Build → Validate → Investigate → Document → Present**

If this project adds value, consider starring the repository ⭐

---

## 👨‍💻 Author

**Abdul Rehman**  
SOC • SIEM • Detection Engineering • Incident Response • Threat Intelligence • Security Automation

---

### 📧 Reach Out

  <a href="https://github.com/abdul4rehman215">
    <img src="https://img.shields.io/badge/Follow-181717?style=for-the-badge&logo=github&logoColor=white" alt="Follow" />
  </a>
  <a href="https://linkedin.com/in/abdul4rehman215">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&v=1" alt="LinkedIn" />
  </a>
  <a href="mailto:abdul4rehman215@gmail.com">
    <img src="https://img.shields.io/badge/Email-EE0000?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>

---
