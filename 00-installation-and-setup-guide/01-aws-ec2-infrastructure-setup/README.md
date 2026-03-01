# ☁️ Project 01 — AWS EC2 Infrastructure Setup Guide  
### SOC-SOAR Ecosystem Deployment Foundation

<p align="center">

  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/icons/aws_logo.webp" width="100"/>

</p>
  
> **Goal:** Launch an EC2 instance where **network works + internet works**, then apply baseline system setup (timezone/NTP/hostname) so the machine is ready for SOC/SOAR deployments.

---

## 📌 Project Overview

This project documents the **AWS foundation setup** I used before installing any SOC stack tools (Wazuh, TheHive, MISP, Cortex, Suricata, Zeek, n8n, etc.).

The key principle is:

✅ **Do not install anything until network + internet + DNS are verified.**  
Most failures in SOC lab deployments are caused by **VPC/subnet/route table/security group** misconfiguration.

---

## 🎯 Objectives

By the end of this setup, I was able to:

- Build a clean VPC network (instead of blindly using the default)
- Launch an EC2 in the correct subnet with a public IP
- Confirm routing + internet + DNS are working
- Apply host baseline setup (timezone, NTP, hostname)
- Establish a stable starting point for SOC tool installations

---

## ✅ Prerequisites

### AWS Account Requirements
- AWS account with **Billing enabled**
- Region selected (example: `us-east-1`)
- Permissions to create/manage:
  - VPC, Subnets, IGW, Route Tables
  - Security Groups
  - EC2 instances
  - Key pairs
  - IAM roles (optional but recommended)

### Local Requirements
- SSH client (Linux/macOS terminal or Windows PowerShell)
- Your public IP address for SSH allowlist rule

---

## 🧪 Lab Environment

| Component | Value |
|---|---|
| Cloud | AWS |
| Service | EC2 |
| OS | Ubuntu 24.04 LTS |
| Instance (min) | t3.small |
| Storage | 30 GB (minimum) |
| Access | SSH key-based |
| First rule | Network must work before installs |

---

# 🧱 PHASE 0 — BEFORE YOU TOUCH EC2 (Mandatory)

✅ Confirm:
- Billing enabled
- Correct region selected
- You will use a **new VPC** for clarity and control

---

# 🌐 PHASE 1 — NETWORK (80% ISSUES ARE HERE)

## 1️⃣ Create a VPC (Do not rely blindly on default)

**VPC Settings**

| Setting | Value |
|---|---|
| VPC CIDR | `10.0.0.0/16` |
| DNS Resolution | ✅ Enabled |
| DNS Hostnames | ✅ Enabled |

📌 **Why this matters:**  
AWS metadata, internal DNS, and name resolution depend on DNS settings.

---

## 2️⃣ Create Subnets

### Public Subnet

| Setting | Value |
|---|---|
| CIDR | `10.0.1.0/24` |
| Auto-assign public IPv4 | ✅ YES |

### (Optional) Private Subnet

| Setting | Value |
|---|---|
| CIDR | `10.0.2.0/24` |

---

## 3️⃣ Internet Gateway (IGW)

- Create an **Internet Gateway**
- Attach it to the VPC

🚨 If IGW is missing → **NO internet**, even with a public IP.

---

## 4️⃣ Route Table (Most common failure point)

### Public Route Table routes MUST include:

| Destination | Target |
|---|---|
| `10.0.0.0/16` | Local |
| `0.0.0.0/0` | Internet Gateway (igw-xxxx) |

✅ Associate this route table to your **public subnet**.

❌ If `0.0.0.0/0` points to nothing → no internet  
❌ If `0.0.0.0/0` points to NAT → wrong for public subnet

---

## 5️⃣ Network ACL (Keep it simple)

Use default NACL or ensure:

### Inbound
- Allow ALL traffic from `0.0.0.0/0`

### Outbound
- Allow ALL traffic to `0.0.0.0/0`

📌 NACL is **stateless** → return traffic must be allowed.

---

## 6️⃣ Security Group (Stateful — keep minimal)

### Inbound rules (minimum)

| Type | Port | Source |
|---|---:|---|
| SSH | 22 | Your IP only |
| HTTPS | 443 | Your IP / (0.0.0.0/0 only if needed later) |

### Outbound rules
- Allow ALL traffic to `0.0.0.0/0`

✅ Best practice: start with **SSH only** and open other ports later per tool.

---

# 🖥️ PHASE 2 — EC2 INSTANCE (Do this exactly)

## 1️⃣ Launch EC2

| Setting | Value |
|---|---|
| AMI | Ubuntu 24.04 LTS |
| Instance type | t3.small (minimum) |
| Subnet | Public subnet |
| Public IP | ✅ Enabled |
| Storage | 30 GB (minimum) |
| Key Pair | Create/select (required for SSH) |

✅ Optional but recommended:
- Allocate an **Elastic IP** if you want stable public IP (otherwise IP may change after stop/start)

---

## 2️⃣ First network test (DO NOT SKIP)

Run these on EC2 immediately after connecting:

```bash
ip a
ip route
````

You must see:

* Interface: `ens5` (or similar)
* Private IP like: `10.0.1.x`
* Default route via: `10.0.1.1`

### Connectivity tests

```bash
ping -c 3 10.0.1.1
ping -c 3 8.8.8.8
curl -I https://google.com
```

Interpretation:

* ❌ If **8.8.8.8 fails** → routing/network problem
* ❌ If **8.8.8.8 works** but **google.com fails** → DNS issue

✅ Rule:

> **Do not install anything until this works.**

---

# ⏱️ Baseline Machine Setup (Timezone + NTP + Hostname)

## Display current time/date/timezone

```bash
timedatectl
```

## Change timezone (example)

```bash
sudo timedatectl set-timezone Asia/Baku
```

## Enable NTP time sync

```bash
sudo timedatectl set-ntp yes
```

---

## Set hostname (example: thehive)

```bash
sudo hostnamectl set-hostname "thehive"
```

### Update `/etc/hosts` (important)

```bash
sudo nano /etc/hosts
```

Update this line:

FROM:

```
127.0.1.1 old-hostname
```

TO:

```
127.0.1.1 thehive
```

Save and exit (`Ctrl+O`, Enter, `Ctrl+X`).

### Verify hostname

```bash
hostnamectl
```

---

# 🚨 Most Common Failures (From Practical Experience)

| Problem              | Root Cause                                |
| -------------------- | ----------------------------------------- |
| No internet          | Missing IGW / bad route table association |
| `apt update` fails   | DNS broken / outbound blocked             |
| Docker GPG error     | Interrupted key import / wrong repo steps |
| Wazuh dashboard down | Ports not allowed / service not running   |
| No CloudTrail events | IAM role not attached / wrong region      |
| aws-s3 wodle silent  | Wrong bucket name / IAM permission issue  |

---

# ✅ Verification Checklist (Before Installing SOC Tools)

Before moving to Wazuh/TheHive/MISP:

* [ ] `ping 8.8.8.8` works
* [ ] `curl -I https://google.com` works
* [ ] `timedatectl` shows correct timezone
* [ ] NTP enabled
* [ ] `hostnamectl` shows correct hostname
* [ ] Security Group inbound rules are minimal (SSH restricted)

---

## 🧠 What I Learned

* Most SOC lab failures come from **network misconfigurations**, not tool installs
* Route tables + IGW + subnet association are the true “internet switch”
* Correct hostname + time sync prevents weird service issues later
* A clean baseline makes deployments faster and troubleshooting easier

---

## ✅ Result

* AWS network built cleanly (VPC/subnet/IGW/routes)
* EC2 launched with verified internet + DNS
* Host baseline applied (timezone, NTP, hostname)
* Instance ready for SOC ecosystem tool installations

---

## 🌍 Why This Matters

SOC platforms expose dashboards and APIs.
If the baseline isn’t correct, deployments become unstable and insecure.

This project sets the foundation for **everything else** in the SOC/SOAR portfolio.

---

## 🏁 Conclusion

This EC2 foundation setup ensures:
- ✅ stable networking
- ✅ correct DNS + internet access
- ✅ clean system identity (hostname/time sync)

Next step: install SOC tools, guide is in separate project folders (Wazuh, TheHive, MISP, Cortex, Suricata, Zeek, etc.).

---
