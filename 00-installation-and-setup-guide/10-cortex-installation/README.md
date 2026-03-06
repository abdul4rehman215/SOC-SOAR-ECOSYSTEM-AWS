# 🧠 Cortex 3.x – Analysis & Response Engine  
### StrangeBee | Docker Deployment on AWS EC2 (SOC-SOAR Ecosystem)

<p align="center">
  <img src="https://docs.strangebee.com/assets/images/StrangeBee_Landscape.svg" width="400"/>
   <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/cortex-logo-landscape.png" width="400"/>
</p>

---

## 🌍 Introduction

Cortex is an open-source **analysis and active response engine** developed by StrangeBee (the team behind TheHive).

It enables SOC teams, CSIRTs, and security researchers to:

- Automatically enrich observables (IP, domain, URL, hash, file)
- Run intelligence lookups against external services
- Execute automated response actions
- Integrate seamlessly with TheHive
- Scale investigations through automation

In this SOC-SOAR ecosystem:

- **Wazuh** → Detects threats  
- **TheHive** → Manages cases  
- **Cortex** → Enriches & responds  
- **MISP** → Shares intelligence  

Cortex acts as the **automation engine** of the SOC.

---

## 🔍 What Cortex Actually Does

Cortex operates using two main components:

### 🔎 Analyzers
Analyzers are scripts that:
- Query external services (VirusTotal, Shodan, AbuseIPDB, etc.)
- Normalize results into structured format
- Enrich observables with contextual intelligence
- Return machine-readable outputs to TheHive

### ⚡ Responders
Responders:
- Execute active response actions
- Block IP addresses
- Isolate compromised hosts
- Trigger automation workflows
- Integrate with firewalls, EDRs, or other security systems

Cortex dynamically spawns analyzer containers using Docker for every job execution.

---

## 🏗 Architecture Overview

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/cortex-architecture.png" width="800">
</p>

### High-Level Flow

```
Observable (IP/Hash/URL)
        ↓
     TheHive
        ↓
      Cortex
        ↓
  Analyzer Container (Docker)
        ↓
  Enriched Intelligence
        ↓
   Returned to Case
```

Cortex uses:

- Elasticsearch → Data storage
- Docker → Job execution engine
- REST API → Integration with other tools

---

## ☁️ Infrastructure Requirements (This Deployment)

For this AWS SOC deployment:

| Setting | Value |
|----------|--------|
| Instance Name | cortex |
| Instance Type | t2.xlarge |
| vCPU | 4 |
| RAM | 16GB |
| Storage | 50GB SSD |
| OS | Ubuntu 24.04 LTS |
| Deployment Method | Official StrangeBee Docker Repo |

### Why 16GB RAM?

Cortex requires significant memory for:

- Elasticsearch indexing
- Analyzer container spawning
- Concurrent job execution
- REST API load
- Background processing

Under-provisioned systems result in:

- Analyzer crashes
- Healthcheck failures
- Docker job errors
- Elasticsearch instability

---

# ✅ Prerequisites

Before installing Cortex, ensure baseline configuration is completed.

---

## 1️⃣ Baseline EC2 Setup (Timezone / NTP / Hostname)

Cortex relies on proper time synchronization and hostname resolution.

👉 **Baseline Machine Setup Guide (Time / NTP / Hostname)**  
[Open EC2 Baseline Configuration Guide](../../01-ec2-setup/README.md)

This ensures:

- Correct timezone configuration  
- NTP synchronization enabled  
- Proper hostname resolution  
- Stable container networking  

---

## 2️⃣ Docker Installed

Cortex is fully Docker-based.

It requires:

- Docker Engine  
- Docker Compose Plugin  

👉 **Docker Installation Guide**  
[Open Docker Installation Guide](../../02-docker-installation/README.md)

---

# 🚀 Cortex Installation (Official StrangeBee Docker Deployment)

---

## Step 1 – Clone Official Repository

```bash
cd /opt
sudo mkdir Cortex
cd Cortex
sudo git clone https://github.com/StrangeBeeCorp/docker.git
cd docker/prod1-cortex
```

---

## Step 2 – Run Initialization Script

```bash
bash ./scripts/init.sh
```

When prompted:

```
Define the hostname used to connect to this server:
```

Enter:

```
cortex
```

---

## Step 3 – Modify docker-compose.yml (CRITICAL FIXES)

### ✅ 1. Enable Port 9001

Find:

```yaml
# ports:
#   - '0.0.0.0:9001:9001'
```

Replace with:

```yaml
ports:
  - '0.0.0.0:9001:9001'
```

---

### ✅ 2. Disable Elasticsearch Security (Lab Deployment)

Remove:

```yaml
- xpack.security.enabled=true
- ELASTIC_PASSWORD=${elasticsearch_password}
```

Add instead:

```yaml
- xpack.security.enabled=false
```

---

### ✅ 3. Replace Elasticsearch Healthcheck

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -f -s http://elasticsearch:9200/_cat/health || exit 1"]
  start_period: 40s
  interval: 5s
  timeout: 2s
  retries: 10
```

---

### ✅ 4. Relax Cortex Healthcheck

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -s http://localhost:9001 || exit 1"]
  interval: 30s
  timeout: 5s
  retries: 10
  start_period: 180s
```

---

# 🔐 Fix Permissions (MANDATORY)

```bash
sudo chown -R 1000:1000 elasticsearch cortex
sudo chmod -R 775 elasticsearch cortex
```

---

# ▶ Start Cortex

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Access UI:

```
http://<EC2_PUBLIC_IP>:9001
```

---

# 🧠 First-Time Setup (IMPORTANT)

On first launch:

---

## Step 1 – Update Database

Click:

**Update Database**

This initializes Elasticsearch and prepares the backend.

---

## Step 2 – Create SuperAdmin Account

There is **NO default username or password**.

You must manually create:

- Login
- Password
- SuperAdmin user

This user has global administrative privileges.

---

# 🏢 Create Dedicated Organization (REQUIRED)

The default organization cannot be used for operational configuration.

1. Login as SuperAdmin  
2. Navigate to → Organizations  
3. Click → Add Organization  
4. Enter:
   - Organization Name
   - Description  
5. Save  

---

# 👤 Create Org Admin User

Inside your organization:

1. Go to → Users  
2. Click → Add User  
3. Assign role: `orgAdmin`  
4. Set:
   - Email  
   - Password  
5. Save  

Logout and login using this orgAdmin account.

---

# 🔑 Generate API Key (For Integrations)

1. Login as orgAdmin  
2. Go to → Users  
3. Select user  
4. Click → Create API Key  
5. Click → Reveal  
6. Copy immediately  

Use this header format:

```
Authorization: Bearer <API_KEY>
```

This is required for:

- TheHive integration  
- SOAR workflows  
- Automation scripts  

---

# ⚙ Enable and Configure Analyzers

Navigate to:

Organization → Analyzers

Enable required analyzers:

- VirusTotal
- Shodan
- AbuseIPDB
- GeoIP
- MISP

Each analyzer requires:

- API key
- Rate limits configuration

---

# 🐳 Required for Analyzer Execution

Ensure docker-compose.yml contains:

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

This allows Cortex to spawn analyzer containers.

---

## ✅ Verification Test

Run an analyzer from UI.

Then check:

```bash
docker ps
```

You should see:

```
cortex-job-xxxxxxxx
```

This confirms Docker socket integration is working.

---

# 📚 Official Documentation & Further Exploration

👉 **Cortex Official Website**  
[Visit StrangeBee Cortex Page](https://strangebee.com/cortex/)

👉 **Full Cortex Documentation Portal**  
[Open Cortex Documentation](https://docs.strangebee.com/cortex/)

👉 **Quick Start Guide (First Launch Setup)**  
[Open Cortex First Start Guide](https://docs.strangebee.com/cortex/user-guides/first-start/)

👉 **Installation & Configuration Methods**  
[Explore All Installation Options](https://docs.strangebee.com/cortex/installation-and-configuration/)

👉 **Official GitHub Repository**  
[View Cortex GitHub Repository](https://github.com/TheHive-Project/Cortex)

---

# 🧠 Why Cortex Is Critical in a Modern SOC

Without Cortex:
- Analysts manually check every IOC
- No structured enrichment
- No automated response
- No scalable investigations

With Cortex:
- Observables enriched instantly
- Intelligence normalized automatically
- Automation reduces analyst workload
- SOC scales horizontally
- TheHive becomes fully automated

Cortex is the **automation brain** of this SOC-SOAR ecosystem.

---

# 📂 Repository Structure

```
10-cortex-strangebee/
│
├── README.md
├── commands.sh
├── troubleshooting.md
├── interview_qna.md
└── architecture-notes.txt
```

---

# 🏁 Final Deployment Checklist

✔ Docker running  
✔ Port 9001 accessible  
✔ Database updated  
✔ SuperAdmin created  
✔ Organization created  
✔ OrgAdmin created  
✔ API key generated  
✔ Analyzers enabled  
✔ Docker socket mounted  
✔ Analyzer jobs spawning  

If all above passes → Cortex is production-ready.

---
---

## 🌐 Project Post on LinkedIn

I also shared this project on LinkedIn with a concise portfolio summary, key highlights, and implementation context.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-View%20Project%20Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/abdul4rehman215_soc-cortex-soar-activity-7422895754379227136-AkcE?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU)

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
