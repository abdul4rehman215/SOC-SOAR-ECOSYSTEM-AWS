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

⚠️ Change password immediately.

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

✔ MISP deployed on AWS EC2  
✔ SSL enabled  
✔ Database initialized  
✔ API-ready  
✔ SOC integration-ready  

---

# 📌 Conclusion

MISP is the intelligence layer of this SOC-SOAR ecosystem.

It transforms isolated indicators into **actionable, shareable threat intelligence** and bridges detection with collaborative defense.
