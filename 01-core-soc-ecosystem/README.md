# 🛡 Core SOC Ecosystem on AWS

## Detection → Intelligence → Investigation

---

<div align="center">

<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/soc_%20tools_overview.jpeg" width="900"/>

</div>

---

# 📌 Project Overview

This capstone project demonstrates the design and deployment of a **real-world Security Operations Center (SOC) architecture** built entirely using open-source tools on AWS.

The ecosystem integrates:

* **Wazuh** – Security Monitoring & Detection (SIEM/XDR)
* **MISP** – Threat Intelligence Platform
* **TheHive** – Incident Management & Case Investigation

Together, they create a structured SOC pipeline:

> 🔍 Detect → 🧠 Enrich → 🔎 Investigate → 📂 Manage

This is not just installation.
This is an operational SOC workflow that mirrors enterprise environments.

---

# 🏗 SOC Architecture Overview

<div align="center">

<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/architect_workflow.png" width="900"/>

</div>

---

# 🎯 Objective of This Architecture

Traditional lab setups focus on tools individually.

This project focuses on:

- ✔ How alerts move across platforms
- ✔ How intelligence adds context
- ✔ How investigations are structured
- ✔ How analysts work in real SOC workflows

It answers three core questions:

1. What happened? (Detection)
2. Is it malicious? (Intelligence)
3. What are we doing about it? (Investigation)

---

# 🟦 1️⃣ Wazuh — Detection Layer

Wazuh acts as the **SOC's detection engine**.

### Capabilities:

* Log collection (servers, endpoints, cloud)
* File Integrity Monitoring (FIM)
* Rule-based alerting
* MITRE ATT&CK mapping
* Compliance monitoring
* Real-time alert generation

### In the SOC Pipeline:

Wazuh answers:

> “An event occurred. Should we care?”

It generates structured JSON alerts based on detection logic.

---

# 🟨 2️⃣ MISP — Threat Intelligence Layer

MISP acts as the **SOC’s intelligence repository**.

### Capabilities:

* Stores Indicators of Compromise (IOCs)
* Shares threat intelligence across communities
* Correlates IPs, hashes, domains
* Enriches alerts with global intelligence

### In the SOC Pipeline:

MISP answers:

> “Is this indicator known malicious?”

It adds context to detections, increasing confidence and reducing noise.

---

# 🟧 3️⃣ TheHive — Investigation & Case Management Layer

TheHive acts as the **SOC’s investigation hub**.

### Capabilities:

* Converts alerts into structured cases
* Assigns cases to analysts
* Tracks investigation progress
* Documents evidence
* Maintains audit logs
* Enables collaboration

### In the SOC Pipeline:

TheHive answers:

> “How do we investigate and manage this incident?”

It ensures investigations are structured, auditable, and repeatable.

---

# 🔁 How the Core SOC Workflow Operates

### Step 1 — Event Detection

* Endpoint logs sent to Wazuh
* Detection rules trigger alerts
* Alerts indexed and visualized

---

### Step 2 — Intelligence Enrichment

* Indicators (IP, hash, domain) checked against MISP
* Known malicious IOCs identified
* Alert severity adjusted based on intelligence

---

### Step 3 — Case Creation

* Alert forwarded to TheHive
* Case automatically created
* Observables extracted
* Analyst assigned

---

### Step 4 — Investigation

* Analyst reviews:

  * Source IP
  * Host activity
  * Timeline
  * Intelligence context
* Case updated with findings
* Resolution documented

---

# 📊 What This SOC Ecosystem Improves

## 🔽 Reduces False Positives

Alerts are intelligence-backed instead of raw detections.

---

## ⚡ Reduces MTTR (Mean Time to Respond)

Context is automatically available.
No manual IOC lookup required.

---

## 📂 Structured Incident Workflow

Instead of:

* Alerts in dashboards
* Notes in chats
* No tracking

You get:

* Assigned cases
* Evidence tracking
* Resolution status
* Audit trail

---

## 🧠 Intelligence-Driven Detection

New IOCs added to MISP enhance detection quality.

Threat detection evolves with global intelligence.

---

## 📈 SOC Maturity Increase

Without integration:

* Tools operate independently
* Manual correlation required

With integration:

* Detection → Enrichment → Investigation connected
* Analysts operate in a unified workflow

---

# 🧪 Demonstrated Use Cases

### 🔐 Brute Force Detection

1. Wazuh detects repeated SSH failures.
2. Source IP checked in MISP.
3. IP found in botnet feed.
4. Case created in TheHive.
5. Investigation documented and resolved.

---

### 🦠 Malicious File Detection

1. File created on monitored endpoint.
2. Hash extracted by Wazuh.
3. Hash matched in MISP.
4. Alert escalated.
5. Case created for investigation.

---

### 🕵️ Threat Hunting

* Analyst filters high-severity alerts.
* Correlates indicators across hosts.
* Uses MISP intelligence for validation.
* Documents findings in TheHive.

---

# 🧱 Why This Is a Capstone-Level Project

This project demonstrates:

* End-to-end SOC architecture design
* Detection engineering
* Threat intelligence integration
* Incident response workflow
* Cross-platform API integration
* Structured investigation modeling
* AWS-based security infrastructure deployment
* Real-world troubleshooting

It reflects how modern SOC teams operate in enterprise environments.

---

# 📂 Installation & Integration Details

Full deployment guides, configurations, scripts, and troubleshooting documentation are available here:

[🔗 **Click to view the Full Installation & Integration Guide**](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/tree/main/00-installation-and-setup-guide)

That section includes:

* AWS infrastructure setup
* Docker installation
* Wazuh deployment
* MISP deployment
* TheHive deployment
* All integrations between tools
* Architecture notes
* Interview preparation guides
* Troubleshooting documentation

---

#### [Watch the SOC demo](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/01-core-soc-ecosystem/SOC%20Working%20System.mp4)

---

# 📌 Key Takeaway

This ecosystem transforms:

Raw alerts
→ Intelligence-enriched detections
→ Structured investigations
→ Managed incidents

It represents a practical, realistic SOC built the way real blue teams operate.

---

---

## 🌐 Project Posts on LinkedIn

I also shared this project on LinkedIn through multiple portfolio posts covering the implementation, workflow, and key outcomes.

<p align="left">
  <a href="https://www.linkedin.com/posts/abdul4rehman215_%F0%9D%90%92%F0%9D%90%8E%F0%9D%90%82-%F0%9D%90%82%F0%9D%90%9A%F0%9D%90%A9%F0%9D%90%AC%F0%9D%90%AD%F0%9D%90%A8%F0%9D%90%A7%F0%9D%90%9E-%F0%9D%90%8F%F0%9D%90%AB%F0%9D%90%A8%F0%9D%90%A3%F0%9D%90%9E%F0%9D%90%9C%F0%9D%90%AD-activity-7417785211024900096-l1VH?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU">
    <img src="https://img.shields.io/badge/Capstone-Post%2001-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 01" />
  </a>
  <a href="https://www.linkedin.com/posts/abdul4rehman215_%F0%9D%90%85%F0%9D%90%AE%F0%9D%90%A5%F0%9D%90%A5-%F0%9D%90%92%F0%9D%90%8E%F0%9D%90%82-%F0%9D%90%80%F0%9D%90%AB%F0%9D%90%9C%F0%9D%90%A1%F0%9D%90%A2%F0%9D%90%AD%F0%9D%90%9E%F0%9D%90%9C%F0%9D%90%AD%F0%9D%90%AE%F0%9D%90%AB-activity-7417966375043772416-9yEN?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU">
    <img src="https://img.shields.io/badge/Architecture-Post%2002-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 02" />
  </a>
  <a href="https://www.linkedin.com/posts/abdul4rehman215_%F0%9D%90%87%F0%9D%90%9A%F0%9D%90%A7%F0%9D%90%9D%F0%9D%90%AC-%F0%9D%90%8E%F0%9D%90%A7-%F0%9D%90%92%F0%9D%90%8E%F0%9D%90%82-%F0%9D%90%8F%F0%9D%90%AB%F0%9D%90%A8%F0%9D%90%A3%F0%9D%90%9E%F0%9D%90%9C%F0%9D%90%AD-activity-7418177814463582208-V4cH?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU">
    <img src="https://img.shields.io/badge/Recruiter-Post%2003-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 03" />
  </a>
  <a href="https://www.linkedin.com/posts/abdul4rehman215_soc-socanalyst-cyberdefense-activity-7425425642369777664-4pFN?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU">
    <img src="https://img.shields.io/badge/VideoDemo-Post%2004-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 04" />
  </a>
</p>

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
