# 🐝 TheHive 5.5 – Incident Response Platform (Docker Deployment on AWS EC2)

<p align="center">

  <img src="https://docs.strangebee.com/assets/images/StrangeBee_Landscape.svg" width="400"/>
  <img src="https://docs.strangebee.com/thehive/images/overview/thehive.svg" width="400"/>
</p>

---

# 🛡️ SOC-SOAR Ecosystem – Case Management Core

TheHive is a powerful **Security Incident Response Platform** designed for SOC teams, CSIRTs, CERTs, and DFIR professionals.

In this project, TheHive 5.5 was deployed on AWS EC2 using Docker as part of a full SOC ecosystem integration with:

- Wazuh (SIEM/XDR)
- MISP (Threat Intelligence)
- Cortex (Analyzers & Responders)
- AWS Cloud Monitoring
- Automation workflows

---

# 🎯 Objective

Deploy TheHive 5.5 in a production-ready Docker environment on AWS EC2 to enable:

- Incident case management
- Alert triage workflows
- Observable enrichment
- Analyst collaboration
- Integration with SIEM & Threat Intelligence platforms

---

# 🖥️ Infrastructure Requirements

### ☁️ AWS EC2 Configuration

| Component | Specification |
|------------|---------------|
| Instance Type | t2.xlarge |
| vCPU | 4 |
| RAM | 16 GB |
| Storage | Minimum 50 GB |
| OS | Ubuntu 24.04 LTS |

📌 Why 16GB RAM?  
TheHive depends on Elasticsearch and Cassandra. Both are memory-intensive. Less RAM may cause container crashes or unstable indexing.

---

# 🔐 Security Group Requirements

| Port | Purpose |
|------|---------|
| 22 | SSH |
| 9000 | TheHive Web UI |
| 443 (optional) | Reverse Proxy / SSL |
| 9200 | Elasticsearch (Do NOT expose publicly) |

🚨 IMPORTANT:
- Never expose Elasticsearch to the public internet.
- Restrict port 9000 to your IP if not using reverse proxy.
- Docker must be installed prior (see installation guide below).

---

# 🧠 What is TheHive?

TheHive is a 4-in-1 Security Incident Response platform that provides:

- Case Management
- Alert Triage
- Observable Enrichment
- Collaboration Engine

It integrates seamlessly with:

- MISP (Threat Intelligence)
- Cortex (Automated analyzers)
- SIEM tools (like Wazuh)
- Email ingestion pipelines

---

# 🏗️ Architecture Overview

<p align="center">
  <img src="https://docs.strangebee.com/thehive/images/overview/thehive-application-stack.png" width="600"/>
</p>

Core Components:

- Apache Cassandra (Database)
- Elasticsearch (Indexing Engine)
- TheHive Application Layer
- File Storage (Local/NFS/S3-compatible)

Docker deployment handles orchestration of these services internally.

---

# 🔄 Time & Host Configuration (MANDATORY BEFORE INSTALLATION)

📌 Refer to:

[time and hostname setup guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/tree/main/00-installation-and-setup-guide/01-aws-ec2-infrastructure-setup#-post-launch-server-standardization)

---

# 🐳 Docker Requirement

Docker must be installed before proceeding.

📌 Refer to:

[Docker Installation Guide](./00-installation-and-setup-guide/02-docker-installation)

---

# 🚀 Installation Method Used

Docker Official Deployment (StrangeBee GitHub Repository)

Directory used:
```

/opt/TheHive/

```

---

# 🌐 Access TheHive

```
http://<EC2-PUBLIC-IP>:9000
```

Default Credentials:

- Username: admin
- Password: secret

⚠️ Change default password immediately after login.

---

# 📊 Key Features

- Real-time alert triage
- Case lifecycle management
- Observable enrichment
- MISP integration
- Cortex automation
- KPI dashboards
- Collaboration workflows

Explore official documentation:

- [Overview](https://docs.strangebee.com/thehive/overview/)
- [Analyst Corner](https://docs.strangebee.com/?_gl=1#analyst)
- [Installation Methods](https://docs.strangebee.com/thehive/installation/installation-methods/)
- [System Requirements](https://docs.strangebee.com/thehive/installation/system-requirements/)
- [Official Website](https://strangebee.com/thehive/)
- [Features](https://strangebee.com/thehive-features/)
- [Use Cases](https://strangebee.com/use-cases-thehive/)

---

# 🎯 Real-World SOC Relevance

TheHive transforms alerts into structured cases and allows:

- Evidence documentation
- Task assignment
- Timeline tracking
- Observable correlation
- Integration with threat intelligence feeds
- Automated DFIR workflows

It bridges the gap between detection (SIEM) and response (IR).

---

# 🏁 Result

Successfully deployed TheHive 5.5 on AWS EC2 using Docker as part of a unified SOC ecosystem.

Enabled:

- Centralized case management
- SOC workflow automation
- Threat intelligence integration
- Scalable IR operations

---

# 📂 Repository Structure

```

04-thehive-installation/
│
├── README.md
├── commands.sh
├── interview_qna.md
├── architecture-notes.txt
├── troubleshooting.md

```

---

# 🐝 Why TheHive Matters

In a mature SOC environment:

Detection without structured response leads to chaos.

TheHive introduces:

✔ Standardized case workflow  
✔ Collaborative investigation  
✔ Automation-ready architecture  
✔ SOC scalability  

It is a critical backbone for modern DFIR and SOAR operations.

---

End of README.

