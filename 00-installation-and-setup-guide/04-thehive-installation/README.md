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
- **Cortex** → automated analysis & Responders
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

---

# 🔐 Initial Web UI Configuration (CRITICAL – Do Not Skip)

After accessing TheHive for the first time, perform these mandatory security and organizational setup steps.

## 1️⃣ Change Default Admin Password (Immediate Security Action)

Login using default credentials:

```
http://<EC2_PUBLIC_IP>:9000
```

Default:

* Username: `admin`
* Password: `secret`

### 🔒 Change Password Immediately

1. Click your profile icon (top-right corner)
2. Select **Change Password**
3. Set a strong password
4. Save

⚠ Never continue using default credentials in production.

---

## 2️⃣ Create Your Organization

By default, TheHive uses a default organization.
In real-world SOC environments, you must create your own organization.

### Steps:

1. From left sidebar → Click **Organizations**
2. Click **➕ Add**
3. Fill:

| Field                    | Value                                       |
| ------------------------ | ------------------------------------------- |
| Name                     | Your organization name (e.g., abdulhiveorg) |
| Description              | SOC Production Organization                 |
| Tasks sharing rule       | manual                                      |
| Observables sharing rule | manual                                      |

4. Click **Confirm**

Your organization is now created.

---

## 3️⃣ Create an Organization Admin User (CRITICAL)

You should NOT work daily using the global super-admin account.

Instead, create an **org-admin user** inside your organization.

---

### As Super Admin:

1. Go to **Organizations**
2. Click your newly created organization
3. Open **Users** tab
4. Click **➕ Add User**

---

### Fill the User Details

| Field   | Value                                                   |
| ------- | ------------------------------------------------------- |
| Type    | Normal                                                  |
| Login   | [your-email@example.com](mailto:your-email@example.com) |
| Name    | Your Full Name                                          |
| Profile | org-admin                                               |

Profile must include:

* manageUser
* manageOrganisation
* full case permissions

Click **Confirm**

---

## 4️⃣ Set Password for New Org Admin

After creating the user:

1. Hover over the new user
2. Click the options (⋮)
3. Select **Set a new password**
4. Define a secure password
5. Confirm

---

## 5️⃣ Login Using Org Admin Account

Logout from global admin.

Login using:

* Your new org-admin email
* The password you set

You are now operating within your organization context.

---

# 🧠 Why This Matters

- ✔ Separates global administration from daily SOC work
- ✔ Enables multi-organization architecture
- ✔ Follows enterprise best practice
- ✔ Supports role-based access control
- ✔ Prepares for multi-tenant deployments

In production:

* Global admin → platform control only
* Org admin → SOC management
* Analysts → case investigation

---

# 📌 Final Working Structure

| Role                | Purpose                   |
| ------------------- | ------------------------- |
| admin (super-admin) | Platform-level management |
| org-admin           | Organization management   |
| analyst             | Case investigation        |
| service account     | API integrations          |

---

# 🔄 Flow Summary

Deployment →
Login →
Change default password →
Create organization →
Create org-admin →
Login as org-admin →
Start SOC operations

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

- ✔ Structured investigations  
- ✔ Collaboration  
- ✔ Audit trails  
- ✔ Case documentation  
- ✔ Automation-ready IR  

---

# 📂 Repository Structure

```
04-thehive-installation/
│
├── README.md
├── commands.sh
├── architecture-notes.txt
├── interview_qna.md
└── troubleshooting.md
```

---

# 🎯 Result

- TheHive 5.5 deployed successfully on AWS EC2
- Containers validated via `docker ps`
- Web UI accessible on port 9000
* Default credentials secured
* Custom SOC organization created
* Dedicated org-admin account configured
* Ready for structured SOC workflows

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
