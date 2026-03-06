# 🛡️ MISP Threat Intelligence Platform Deployment (AWS EC2)

<p align="center">
  <img src="https://www.misp-project.org/img/logo.png" width="200">
</p>

### SOC-SOAR Ecosystem – Threat Intelligence Core

MISP (Malware Information Sharing Platform) is the **threat intelligence backbone** of this AWS-based SOC ecosystem.

It enables:
- Centralized IOC storage
- Threat intelligence correlation
- Sharing across organizations
- Automated exports to detection tools
- Integration with TheHive, Wazuh, Cortex, Suricata

In this deployment, MISP functions as the **intelligence enrichment and IOC distribution engine**.

---

# 🌍 What is MISP?

MISP is an open-source threat intelligence platform designed to:

- Share Indicators of Compromise (IOCs)
- Correlate attributes and events
- Automate export to IDS/SIEM
- Support structured intelligence workflows
- Enable collaborative analysis

It supports:

- STIX
- OpenIOC
- Snort / Suricata rules
- JSON / XML exports
- API-based integrations

Official project page:  

👉 **[MISP Official Website](https://www.misp-project.org/)**

---

# 🧠 Why MISP in a SOC?

In a modern SOC:

- Wazuh detects
- TheHive manages cases
- Cortex enriches
- **MISP shares and correlates intelligence**

MISP transforms raw indicators into **structured intelligence** that can be shared across teams and organizations.

---

# 📂 Repository Structure
```
05-misp-installation/
├── README.md
├── commands.sh
├── troubleshooting.md
├── architecture-notes.txt
└── interview_qna.md
```
---

# 🏗 Architecture Overview

<p align="center">
  <img src="https://raw.githubusercontent.com/MISP/MISP/1ebb4fe60ee17790a1b6b869de95024ad7345e29/INSTALL/logos/diagram/misp-flows.svg" width="800">
</p>

### Core Stack (LAMP-Based)

| Component | Purpose |
|------------|----------|
| Linux | OS layer |
| Apache | Web server |
| MariaDB | Relational database |
| PHP | Application logic |
| Redis | Caching & background jobs |
| Python | Modules & integrations |

MISP scales horizontally and integrates via REST APIs.

---

# ☁️ Infrastructure Requirements

For this AWS SOC deployment, MISP was installed on:

| Setting | Value |
|----------|--------|
| Instance Name | misp |
| Instance Type | t2.xlarge |
| vCPU | 4 |
| RAM | 16 GB |
| Storage | 50+ GB SSD |
| OS | Ubuntu 24.04 LTS |
| Cloud | AWS EC2 |

⚠️ Why this sizing?

MISP performs:
- Database-heavy operations (MariaDB)
- Correlation engine processing
- Redis background jobs
- Attribute indexing
- Large event storage

Under-provisioned instances cause:
- Slow correlation
- Worker timeouts
- Redis queue backlog
- Apache/PHP execution failures

For production-grade SOC environments, 16GB RAM ensures stable performance.

---

# ✅ Prerequisites

Before installing MISP, ensure baseline EC2 configuration is completed:

### 1️⃣ Time / NTP / Hostname Setup

Refer to:

👉 **[Baseline EC2 Machine Setup Guide (Timezone / NTP / Hostname)](../../01-aws-ec2-infrastructure-setup/README.md)**

This ensures:
- Correct timezone
- NTP synchronization
- Proper hostname resolution

---

# 🚀 MISP Installation (Ubuntu 24.04 – Official Script Method)

## 1️⃣ System Preparation

```bash
sudo apt update
sudo apt install -y git curl unzip gnupg-agent software-properties-common
```

---

## 2️⃣ Create Dedicated MISP User

```bash
sudo adduser misp --gecos "MISP,,," --disabled-password
echo "misp:OctaSec123!" | sudo chpasswd
sudo usermod -aG sudo,staff,www-data misp
```

Verify:

```bash
id misp
```

---

## 3️⃣ Run Official Installer

```bash
sudo -i -u misp bash
cd /tmp
wget --no-cache -O INSTALL.sh https://raw.githubusercontent.com/MISP/MISP/2.5/INSTALL/INSTALL.ubuntu2404.sh
chmod +x INSTALL.sh
sudo bash INSTALL.sh
```

When prompted:

```
Password: OctaSec123!
```

⏳ Takes 20–40 minutes  
☕ Do not interrupt

After completion:

```bash
exit
```

---

# 🔎 Post-Installation Validation

## Check services

```bash
systemctl status apache2 mariadb redis-server
```

## Verify database configuration file

```bash
ls /var/www/MISP/app/Config/database.php
```

If file exists → Database initialized correctly ✅

---

# 🌐 BaseURL Fix (AWS Specific)

Default installer uses `misp.local` which will NOT work in AWS.

Get Public IP:

```bash
curl -s http://169.254.169.254/latest/meta-data/public-ipv4
```

Set base URL:

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Admin setSetting MISP.baseurl "https://<EC2_PUBLIC_IP>"
```

---

# 🔐 Enable SSL

```bash
sudo a2enmod ssl
sudo systemctl reload apache2
```

Access:

```
https://EC2_PUBLIC_IP
```

Default credentials:

- Username: admin@admin.test
- Password: Provided after installer completes

⚠️ Change password immediately after login.

---

# 📁 Logs Location

```bash
sudo tail -f /var/www/MISP/app/tmp/logs/error.log
```

Main directory:

```
/var/www/MISP/app/tmp/logs
```

---

# 🧠 Post-Installation: Configure Threat Intelligence Feeds (CRITICAL)

After fresh MISP installation:

- ✔ You can log in
- ✔ Base URL works
- ✔ Apache / MariaDB / Redis running
- ✔ Administration menu visible

Now you must configure threat intelligence feeds properly.

Without feeds, MISP contains **no threat data**.

---

# 🟢 Step 1 — Load Default Feed Metadata (One-Time Action)

📍 Go to:

```
Administration → Feeds
```

Click:

```
Load default feed metadata
```

### What This Does

* Registers known public OSINT feeds
* Does NOT import IOCs
* Safe to run
* Required only once

After clicking, you should see feeds such as:

* CIRCL OSINT
* Botvrij.eu
* Abuse.ch
* Other OSINT providers

---

# 🟢 Step 2 — Enable Only High-Quality Feeds (Do NOT Enable All)

⚠ Never enable all feeds blindly.

For AWS t2.xlarge (16GB RAM) recommended minimal setup:

- ✔ CIRCL OSINT
- ✔ Botvrij.eu
- ✔ Abuse.ch (optional)

---

### To Enable a Feed

1. Click ✔ in the Actions column
2. Confirm Enabled column shows ✔

Feed is now active but not cached yet.

---

# 🟢 Step 3 — Configure Feed Filtering (VERY IMPORTANT)

This prevents database explosion and keeps SOC noise low.

---

### Click Edit (✏️) on CIRCL feed

Configure:

* Enabled ✔
* Caching enabled ✔
* Lookup visible ✔
* Distribution: Your Organization

---

### Set Pull Filters

Click:

```
Modify → Set PULL rules
```

Add Allowed Tags:

```
tlp:white
confidence:high
```

---

### Add Timestamp Limiting (SOC Best Practice)

Under Additional sync parameters:

```json
{"timestamp":"30d"}
```

Meaning:

* Only last 30 days of events imported
* Reduces noise
* Prevents DB overload
* Enterprise best practice

Click:

```
Update → Submit
```

Repeat similar filtering for other feeds.

---

# 🟢 Step 4 — Cache Feeds (Safe Operation)

Now feeds show:

```
Not cached (red)
```

You must cache them.

---

## GUI Method

Click:

```
Cache MISP feeds
```

OR

```
Cache all feeds
```

This:

* Downloads feed metadata
* Builds index
* Does NOT import full events

After success:

Red "Not cached" disappears.

---

## CLI Method (Recommended for AWS)

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Server cacheFeed all
```

Or specific feed:

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Server cacheFeed 1
```

(Replace 1 with feed ID)

---

# 🟢 Step 5 — Fetch & Store Events (Controlled Import)

⚠ This imports real events into database.

Only do AFTER filtering.

---

## GUI Method

Click:

```
Fetch and store all feed data
```

⚠ Do NOT click if filters are not configured.

---

## CLI Method (Safer for Production)

Fetch single feed:

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Server fetchFeed 1
```

Fetch all:

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Server fetchFeed all
```

---

# 🟢 Step 6 — Verify Feed Data

Go to:

```
Events → List Events
```

You should now see:

* CIRCL events
* OSINT intelligence
* Recent timestamps

Open an event to confirm:

* IPs
* Domains
* Hashes
* Tags

MISP is now operational.

---

# 🟢 Step 7 — Verify Feed Health

In Feeds page check:

- ✔ Enabled = ✔
- ✔ Caching = ✔
- ✔ Not cached NOT red
- ✔ Feed hits column shows numbers

---

# 🟢 Step 8 — Automate Feed Updates (Production SOC)

Never manually click daily.

Add cron jobs:

```bash
sudo crontab -u www-data -e
```

Add:

```bash
0 * * * * /var/www/MISP/app/Console/cake Server cacheFeed all
30 * * * * /var/www/MISP/app/Console/cake Server fetchFeed all
```

Meaning:

* Cache hourly
* Fetch hourly

Production-ready.

---

# 🟢 What Each Button Does (Quick Summary)

| Button                     | Function                | Safe?        |
| -------------------------- | ----------------------- | ------------ |
| Load default feed metadata | Registers feed list     | ✅ Yes        |
| Cache all feeds            | Downloads metadata only | ✅ Yes        |
| Cache MISP feeds           | Cache structured feeds  | ✅ Yes        |
| Cache freetext/CSV         | Cache text feeds        | ✅ Yes        |
| Fetch and store            | Imports events into DB  | ⚠ Controlled |

---

# 🚫 What NOT To Do

- ❌ Enable every feed
- ❌ Fetch without timestamp filter
- ❌ Skip filtering rules
- ❌ Export raw feed directly to Wazuh
- ❌ Ignore feed health status

---

# 🧠 Real-World SOC Workflow

1. Load metadata once
2. Enable trusted feeds
3. Apply TLP + timestamp filters
4. Cache feeds
5. Fetch selectively
6. Verify events
7. Automate via cron
8. Export curated attributes to detection tools

---

# 🔥 Minimal Setup for Small AWS Instances

For t2.micro / t3.small:

Enable only:

* CIRCL
* Botvrij

Apply:

* tlp:white
* 30d timestamp

Cache → Fetch → Done.

---

# 🔗 What to Explore After Installation

To fully understand MISP capabilities:

### 📘 Features Overview

👉 **[MISP Features Page](https://www.misp-project.org/features/)**

### 🏗 Installation Alternatives

👉 **[Official MISP Install Methods](https://github.com/MISP/MISP/tree/2.5/INSTALL)**

### 🧩 Use Cases

👉 **[Threat Intelligence Use Cases](https://www.misp-project.org/use-cases/)**

---

# 🔄 How This Integrates in the SOC Ecosystem

This deployment connects to:

- Wazuh (SIEM alerts → IOC enrichment)
- TheHive (Case observables → MISP correlation)
- Cortex (Automated enrichment workflows)
- Suricata (Exported rules)
- IDS/SIEM via STIX/OpenIOC exports

---

# 💡 Why MISP Matters

MISP enables:

- Collaborative intelligence sharing
- Automated IOC distribution
- Correlation of threat campaigns
- Structured reporting
- Faster detection and response

It is not just software.

It is a **community-driven intelligence exchange platform**.

---

# 🏁 Result

- ✔ MISP deployed on AWS EC2
- ✔ SSL enabled
- ✔ Database initialized
- ✔ BaseURL configured
- ✔ High-quality OSINT feeds enabled
- ✔ Filters applied (TLP + 30d timestamp)
- ✔ Feeds cached
- ✔ Events imported
- ✔ Cron automation configured
- ✔ Ready for SOC enrichment workflows

---

# 📌 Conclusion

MISP is the intelligence layer of this SOC-SOAR ecosystem.

It transforms isolated indicators into **actionable, shareable threat intelligence** and bridges detection with collaborative defense.

---

## 🌐 Project Post on LinkedIn

I also shared this project on LinkedIn with a concise portfolio summary, key highlights, and implementation context.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-View%20Project%20Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/abdul4rehman215_soc-threatintelligence-misp-activity-7417456444364746752-36gc?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU)

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
