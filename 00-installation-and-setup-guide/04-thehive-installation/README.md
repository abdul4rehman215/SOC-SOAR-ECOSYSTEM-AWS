# 🐝 TheHive 5.5 – Incident Response Platform (Docker Deployment on AWS EC2)

<p align="center">

  <img src="https://docs.strangebee.com/assets/images/StrangeBee_Landscape.svg" width="400"/>
  <img src="https://docs.strangebee.com/thehive/images/overview/thehive.svg" width="400"/>
</p>

---

# 🛡️ SOC-SOAR Ecosystem Role – Case Management Core

**TheHive is the Case Management + Incident Response backbone of my SOC-SOAR ecosystem.**

In this AWS-based SOC environment, TheHive is used to:

- Convert alerts into structured **cases**
- Assign and track **tasks**
- Manage **observables** (IPs, domains, hashes)
- Maintain investigation timelines & audit trails
- Integrate with **MISP (Threat Intelligence)**
- Automate enrichment via **Cortex analyzers**
- Support end-to-end workflows (triage → investigation → response → reporting)

Integrated with:

- **Wazuh (SIEM/XDR)** → detection engine  
- **MISP** → IOC enrichment  
- **Cortex** → automated analysis  
- **AWS Cloud Monitoring** → infrastructure telemetry  
- **n8n SOAR workflows** → automation & reporting  

---

# 🎯 Objective

Deploy **TheHive 5.5** on AWS EC2 using Docker in a production-style configuration to enable structured SOC incident response workflows.

---

# ☁️ Infrastructure Requirements

| Component | Specification |
|------------|---------------|
| Instance Type | t2.xlarge |
| vCPU | 4 |
| RAM | 16 GB |
| Storage | 50+ GB |
| OS | Ubuntu 24.04 LTS |

📌 Official requirements reference:  
👉 [TheHive — System Requirements](https://docs.strangebee.com/thehive/installation/system-requirements/)

---

# 🔐 Required Security Group Ports

Keep inbound access restricted to **your Admin IP / VPN**.

| Port | Protocol | Purpose |
|------|----------|----------|
| 22 | TCP | SSH |
| 9000 | TCP | TheHive Web UI |

Outbound:
- Allow all outbound traffic (Docker image pulls & updates)

---

# ✅ Prerequisites

## 1️⃣ Baseline EC2 Setup (Time / NTP / Hostname)

Before installing TheHive, ensure the EC2 baseline configuration is correct.

👉 Refer to:  
**Baseline Machine Setup (Timezone / NTP / Hostname)**  
[Open EC2 Baseline Setup Guide](../../01-ec2-setup/README.md)

This ensures:
- Correct timezone
- NTP synchronization
- Proper hostname resolution

---

## 2️⃣ Docker Installed

TheHive requires Docker Engine + Docker Compose plugin.

👉 Refer to:  
**Docker Installation Guide**  
[Open Docker Installation Guide](../../02-docker-installation/README.md)

---

# 🧠 What is TheHive?

TheHive is a modern Security Incident Response Platform built for:

- SOC teams  
- CSIRTs  
- DFIR professionals  
- Threat Intelligence teams  

Learn more:

- 👉 [TheHive Documentation — Overview](https://docs.strangebee.com/thehive/overview/)
- 👉 [TheHive Official Product Page](https://strangebee.com/thehive/)

---

# 🏗️ Architecture Overview

<p align="center">
  <img src="https://docs.strangebee.com/thehive/images/overview/thehive-application-stack.png" width="650"/>
</p>

TheHive stack includes:

- Apache Cassandra (Database)
- Elasticsearch (Index engine)
- TheHive Application
- File storage layer

Docker orchestrates these services.

---

# 🚀 Installation Method Used

Deployment method:

👉 **Official StrangeBee Docker Repository**

Alternative installation options:

- 👉 [TheHive — Installation Methods](https://docs.strangebee.com/thehive/installation/installation-methods/)

---

# 🌐 Access TheHive

After deployment:

```
http://<EC2_PUBLIC_IP>:9000/
```

Default credentials:

- Username: `admin`
- Password: `secret`

⚠ Change the default password immediately.

---

# 📊 Key Features

Explore detailed feature breakdown:

👉 [TheHive — Key Features](https://strangebee.com/thehive-features/)

Core capabilities include:

- Alert triage
- Case lifecycle management
- Observable enrichment
- Task assignment workflows
- KPI dashboards
- Cortex automation integration
- Analyst collaboration engine

---

# 🧭 What to Explore After Installation (Documentation Navigation)

To fully understand TheHive capabilities, explore:

### 🔎 Overview & Architecture
👉 [TheHive Documentation — Overview](https://docs.strangebee.com/thehive/overview/)

### 👨‍💻 Analyst Corner (Highly Recommended)
Triage → Investigate → Convert alerts into cases  
👉 [TheHive — Analyst Corner](https://docs.strangebee.com/?_gl=1#analyst)

This section covers:
- Alerts Management
- Case Management
- Task workflows
- Observables handling
- Dashboards
- Filtering & Sorting

### ⚙ Installation Methods
👉 [TheHive — Installation Methods](https://docs.strangebee.com/thehive/installation/installation-methods/)

### 🧩 Use Cases
👉 [TheHive — Use Cases](https://strangebee.com/use-cases-thehive/)

Examples include:
- Alert triage
- Automated DFIR
- Phishing investigations
- Continuous improvement workflows

---

# 🧠 SOC Workflow Impact

TheHive transforms raw alerts into **structured incident response workflows**:

Detection → Triage → Investigation → Enrichment → Response → Reporting

Without TheHive:
Alerts remain isolated.

With TheHive:

✔ Structured investigations  
✔ Collaboration  
✔ Audit trails  
✔ Case documentation  
✔ Automation-ready IR  

---

# 📂 Repository Structure

```
04-thehive-installation/
│
├── README.md
├── commands.sh
├── interview_qna.md
├── troubleshooting.md
```

---

# 🎯 Result

- TheHive 5.5 deployed successfully on AWS EC2
- Web UI accessible on port 9000
- Containers validated via `docker ps`
- Integrated into full SOC-SOAR ecosystem

---

# 🏁 Conclusion

This deployment establishes TheHive as the **Case Management Core** of my AWS-based SOC ecosystem.

It enables:

- Structured incident response
- Analyst collaboration
- Threat intelligence enrichment
- Automation via Cortex
- Integration with Wazuh detections

TheHive bridges the gap between detection and response — turning alerts into actionable investigations.

---
