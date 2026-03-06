# 🧠 TheHive ↔ Cortex Integration
### Centralized Threat Intelligence Enrichment for Real-World SOC Workflows

<p align="center">
  <img src="https://docs.strangebee.com/thehive/images/overview/thehive.svg" width="300"/>
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/cortex-logo-landscape.png" width="300"/>
</p>

---

## 🎯 What This Integration Solves

In real SOC environments:

- Analysts switch between 5–10 browser tabs
- Context is lost between enrichment steps
- Evidence becomes scattered across tools
- Audit trails become incomplete
- Manual verification slows down triage

By integrating **TheHive (Case Management)** with **Cortex (Analyzer & Responder Engine)**:

✔ Observables are enriched directly inside cases  
✔ Multiple analyzers run in parallel  
✔ Results appear in structured & raw format  
✔ Full job traceability is maintained  
✔ Responders can execute response actions  
✔ Investigation becomes single-pane-of-glass  

This transforms TheHive into a **centralized investigation & enrichment hub**.

---

# 🏗 Architecture Overview

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/cortex-thehive-architecture.png" />

</p>  

### How It Works

1. Analyst adds observable in TheHive
2. TheHive sends observable to Cortex via API Key
3. Cortex launches analyzer Docker jobs
4. External intelligence services are queried
5. Results are returned to TheHive
6. Output appears in:
   - Case timeline
   - Structured report
   - Raw JSON
   - Analyzer status view

All enrichment stays inside TheHive.

---

# 🚀 What This Integration Enables

## 🔎 1. One-Click Observable Enrichment

From inside a case:

- Run URLScan
- Run MaxMind GeoIP
- Run MISP lookup
- Run Passive DNS
- Run WHOIS
- Run 250+ available analyzers

Without leaving TheHive.

---

## ⚡ 2. Automated & Asynchronous Analysis

Cortex runs analyzers in background containers.

TheHive:
- Tracks job status
- Shows success/failure
- Maintains timestamps
- Records triggering user

Perfect for audit and compliance.

---

## 🛡 3. Responder Execution (SOAR Foundation)

From TheHive:

- Block IP
- Quarantine endpoint
- Disable user
- Take action via responders

Cortex becomes the “execution engine”.

---

## 📊 4. Multi-Analyzer Correlation

Run multiple analyzers on the same observable:

- Compare GeoIP vs MISP vs Passive DNS
- Identify redundancy
- Identify high-signal analyzers
- Understand intelligence overlap

This mirrors real SOC investigation behavior.

---

# 📘 Prerequisites

Before integration:

### 1️⃣ TheHive Installed

👉 Refer to  
[Open TheHive Installation Guide](../09-thehive-installation/README.md)

---

### 2️⃣ Cortex Installed

👉 Refer to  
[Open Cortex Installation & API Guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/tree/main/00-installation-and-setup-guide/10-cortex-installation#-generate-api-key-for-integrations)

Ensure:
- Organization created
- orgAdmin user created
- API key generated
- Analyzers enabled

---

# 🔐 Step 1 – Generate API Key in Cortex

Login to Cortex as **orgAdmin**

Go to:

Organization → Users → Select User → Create API Key → Reveal → Copy Immediately

Use header format:

Authorization: Bearer <API_KEY>

⚠ Key cannot be viewed again.

---

# 🔗 Step 2 – Connect Cortex in TheHive (GUI Only)

Login to TheHive as Administrator.

Navigate to:

Platform Management → Connectors → Cortex

Click “Add Server”

Fill:

- Server Name: Cortex
- Server URL: http://<CORTEX_IP>:9001
- API Key: (Paste from Cortex)
- Proxy Settings: Default
- SSL Settings: Disable verification if internal lab

Click Save.

If correct:
Status will show GREEN (OK).

---

# ✅ Step 3 – Verify Connection

Go to:

Platform Management → Status

You should see:

Cortex – OK

Version displayed  
Connection active  

---

# 🧩 Step 4 – Verify Analyzer Visibility

Go to:

Entities Management → Analyzer Templates

You should see:

- Urlscan_io_Search
- MaxMind_GeoIP
- MISP_2_1
- CERTatPassiveDNS
- Other enabled analyzers

If visible → Integration successful.

---

# 🧪 Step 5 – Real Observable Testing (SOC Scenario)

## Scenario

Attacker IP detected via SSH brute-force attempt.

### Actions

1. Create New Case
2. Add Observable (IP)
3. Click Run Analyzer
4. Select:
   - Urlscan
   - MaxMind GeoIP
   - MISP
   - Passive DNS
5. Execute

---

# 📊 Step 6 – Analyze Results

Inside case:

You will see:

✔ Structured report  
✔ Raw JSON output  
✔ External links  
✔ Infrastructure details  
✔ Country, ASN, Hosting provider  
✔ Threat verdict  

All inside case timeline.

---

# 🔎 Step 7 – External Validation (Learning Phase)

Click analyzer link (e.g., URLScan result).

Verify:

- Malicious verdict
- Domain relationships
- Infrastructure mapping

Confirms:
Cortex output matches real external intelligence.

---

# 📜 Step 8 – Job Tracking & Audit Trail

In Cortex:

Go to Job History

Verify:
- Job status
- Observable value
- Timestamp
- Triggering user

In TheHive:
- Same job visible
- Full timeline maintained

Audit-ready SOC workflow.

---

# 🧠 Step 9 – Multi-Analyzer Correlation

Run multiple analyzers on same observable.

Observe:

- Some analyzers return no data
- Some fail due to rate limits
- Some provide high-signal intelligence

This teaches:
Analyzer redundancy vs unique value.

Important SOC lesson:
Enable selectively for production.

---

# 📈 Benefits to SOC Teams

- ✔ Faster triage  
- ✔ Less tab hopping  
- ✔ Better context  
- ✔ Centralized evidence  
- ✔ Improved collaboration  
- ✔ Audit compliance  
- ✔ SOAR readiness foundation  

---

# 📂 Repository Structure

```
11-thehive-cortex-integration/
│
├── README.md
├── commands.sh
├── troubleshooting.md
├── architecture-notes.txt
├── interview_qna.md
└── docs/
    └── Cortex TheHive Threat Intelligence Enrichment Project.pdf

```

---

# 📄 Full Project PDF

Complete detailed project walkthrough available here:

👉 [View SOC Enrichment Project PDF](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/00-installation-and-setup-guide/11-thehive-cortex-integration/docs/Cortex%20TheHive%20Threat%20Intelligence%20Enrichment%20Project.pdf)

---

# 🌐 Official References (Recommended Exploration)

Explore Cortex Documentation:

👉 [Open Cortex Official Documentation](https://docs.strangebee.com/cortex/)

Quick Start Guide:

👉 [Open Cortex First Start Guide](https://docs.strangebee.com/cortex/user-guides/first-start/)

Installation Methods:

👉 [Explore Cortex Installation Options](https://docs.strangebee.com/cortex/installation-and-configuration/)

Official GitHub:

👉 [View Cortex GitHub Repository](https://github.com/TheHive-Project/Cortex)

---

# 🏁 Final Outcome

✔ Seamless TheHive ↔ Cortex integration  
✔ Real-world observable enrichment  
✔ Centralized SOC investigation pipeline  
✔ Demonstrated SOAR readiness  
✔ Production-ready architecture pattern  

This integration forms the intelligence backbone of your SOC ecosystem.


---

## 🌐 Project Post on LinkedIn

I also shared this project on LinkedIn with a concise portfolio summary, key highlights, and implementation context.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-View%20Project%20Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/abdul4rehman215_cortex-thehive-threat-intelligence-enrichment-activity-7423251199363108864-6LR1?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU)

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
