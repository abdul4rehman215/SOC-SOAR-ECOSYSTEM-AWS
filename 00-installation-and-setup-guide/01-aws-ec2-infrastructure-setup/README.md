# 🛡️ AWS EC2 Infrastructure Setup Guide  
### SOC-SOAR Ecosystem Deployment Foundation

<p align="center">

  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/aws_logo.webp" width="100"/>

</p>

---

## 📌 Project Overview

This guide documents the complete AWS EC2 infrastructure setup process required before deploying the SOC-SOAR ecosystem (Wazuh, TheHive, Cortex, MISP, Suricata, Zeek, etc.).

The objective is to build a clean, controlled, production-style network foundation instead of relying blindly on AWS default networking.

⚠️ 80% of cloud deployment failures originate from improper network configuration.  
This guide eliminates those risks.

---

## 🎯 Objective

- Create a clean VPC architecture
- Configure public subnet with internet connectivity
- Properly attach Internet Gateway
- Configure route tables correctly
- Ensure Security Groups and NACLs allow required traffic
- Launch EC2 instance with validated network connectivity
- Perform mandatory connectivity validation tests before installing any SOC tools

---

## 🧱 Architecture Overview

```

Internet
│
Internet Gateway (IGW)
│
Public Route Table (0.0.0.0/0 → IGW)
│
Public Subnet (10.0.1.0/24)
│
EC2 Instance (Ubuntu 24.04 LTS)

````

---

## ☁️ AWS Environment Details

| Component | Configuration |
|------------|---------------|
| Region | us-east-1 (example) |
| VPC CIDR | 10.0.0.0/16 |
| Public Subnet | 10.0.1.0/24 |
| Instance Type | t3.small (minimum) |
| OS | Ubuntu 24.04 LTS |
| Storage | 30 GB |
| Public IP | Enabled |
| DNS Resolution | Enabled |
| DNS Hostnames | Enabled |

---

## 🧱 PHASE 0 – AWS Account Preparation (Mandatory)

Before launching EC2:

- AWS account created
- Billing enabled
- Region selected (example: us-east-1)
- Key Pair created (.pem file downloaded securely)
- IAM user configured (avoid root usage)

---

## 🌐 PHASE 1 – Network Configuration (Critical Phase)

### 1️⃣ Create Custom VPC

Do NOT rely blindly on default VPC.

**Settings:**

| Setting | Value |
|----------|-------|
| CIDR Block | 10.0.0.0/16 |
| DNS Resolution | Enabled |
| DNS Hostnames | Enabled |

📌 Why this matters:
- AWS metadata services depend on DNS
- CloudTrail logging and integrations depend on proper DNS configuration
- Internal service resolution depends on this

---

### 2️⃣ Create Subnets

#### Public Subnet

| Setting | Value |
|----------|-------|
| CIDR | 10.0.1.0/24 |
| Auto-assign Public IPv4 | Enabled |

(Optional) Private Subnet:

| Setting | Value |
|----------|-------|
| CIDR | 10.0.2.0/24 |

---

### 3️⃣ Create and Attach Internet Gateway (IGW)

- Create Internet Gateway
- Attach it to the VPC

🚨 If IGW is not attached → EC2 will NOT have internet access even with a public IP.

---

### 4️⃣ Route Table Configuration (Most Common Failure Point)

Create Public Route Table.

Routes MUST include:

| Destination | Target |
|--------------|---------|
| 10.0.0.0/16 | Local |
| 0.0.0.0/0 | Internet Gateway (igw-xxxx) |

✔ Associate this route table with the Public Subnet.

❌ If 0.0.0.0/0 has no target → no internet  
❌ If it points to NAT Gateway → wrong for public subnet  

---

### 5️⃣ Network ACL (Keep Simple Initially)

Use default NACL OR ensure:

#### Inbound Rules:
- Allow ALL traffic from 0.0.0.0/0

#### Outbound Rules:
- Allow ALL traffic to 0.0.0.0/0

📌 Important:
Network ACLs are stateless. Return traffic must be explicitly allowed.

---

### 6️⃣ Security Group (Stateful – Keep Minimal & Secure)

Inbound Rules:

| Type | Port | Source |
|------|------|--------|
| SSH | 22 | Your Public IP |
| HTTPS | 443 | Your IP or 0.0.0.0/0 (if dashboard exposure required) |

Outbound Rules:

- Allow ALL traffic → 0.0.0.0/0

📌 Security Groups are stateful. Return traffic is automatically allowed.

---

## 🖥️ PHASE 2 – EC2 Instance Launch

### Launch Configuration

| Setting | Value |
|----------|-------|
| AMI | Ubuntu 24.04 LTS |
| Instance Type | t3.small (minimum) |
| Subnet | Public Subnet |
| Public IP | Enabled |
| Storage | 30 GB |
| Security Group | Created above |

---

## 🔍 Mandatory Network Validation (DO NOT SKIP)

Immediately after SSH login:

```bash
ip a
ip route
````

You MUST see:

* Network interface (usually `ens5`)
* Private IP like `10.0.1.x`
* Default route via `10.0.1.1`

### Test Internal Gateway:

```bash
ping -c 3 10.0.1.1
```

### Test External IP Connectivity:

```bash
ping -c 3 8.8.8.8
```

### Test DNS Resolution:

```bash
curl -I https://google.com
```

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

### Interpretation:

| Result                         | Meaning                      |
| ------------------------------ | ---------------------------- |
| 8.8.8.8 fails                  | Routing / IGW issue          |
| 8.8.8.8 works but google fails | DNS issue                    |
| apt update fails               | Outbound blocked             |
| SSH works but curl fails       | Route table misconfiguration |

🚨 DO NOT INSTALL ANY SOC TOOL until all tests pass.

---

## 🚨 Most Common Real-World Failures

| Problem                     | Root Cause                   |
| --------------------------- | ---------------------------- |
| No internet                 | Missing IGW or bad route     |
| apt update fails            | DNS misconfigured            |
| Docker GPG error            | Interrupted key import       |
| Wazuh dashboard not loading | Port 443 not allowed         |
| No CloudTrail logs          | IAM role missing             |
| aws-s3 wodle silent         | Wrong bucket name            |
| Cannot access EC2           | Security group misconfigured |

---

## 💻 Recommended Hardware (For Full SOC Stack)

| Deployment Size      | Recommended                           |
| -------------------- | ------------------------------------- |
| Minimal Testing      | t3.small (2GB RAM)                    |
| Multi-tool SOC Stack | t3.large (8GB RAM)                    |
| Production-like Lab  | t3.xlarge (16GB RAM)                  |
| Storage              | Minimum 50–100GB recommended for logs |

---

## 📁 Repository Structure

```
00-installation-and-setup-guide/
└── 01-aws-ec2-infrastructure-setup/
    ├── README.md
    ├── commands.sh
    ├── scripts/
    |   ├── baseline_hardening.sh
    |   ├── health_check.sh
    |   └── ufw_rules_apply.sh
    ├── interview_qna.md
    ├── troubleshooting.md
    └── architecture-notes.txt
```

---

## 🏁 Final Advice

* Never rush networking
* Always validate route tables
* Never expose SSH to 0.0.0.0/0
* Always verify connectivity before installing software
* Document your network architecture

---

## 🧠 What I Learned

* Cloud networking is the foundation of SOC deployments
* Most failures originate from routing and IGW misconfiguration
* DNS resolution is critical for SIEM integrations
* Controlled VPC architecture improves security posture
* Validation before installation saves hours of troubleshooting

---

## 🌍 Why This Matters

A SOC ecosystem relies on:

* External threat intelligence APIs
* Log ingestion pipelines
* Dashboard accessibility
* Agent communication
* CloudTrail integration

If networking is misconfigured, detection engineering fails before it begins.

---

## 🏢 Real-World Relevance

This mirrors real cloud security engineering tasks:

* VPC design
* Internet gateway routing
* Secure SSH configuration
* Controlled exposure of services
* Cloud infrastructure validation

These are core responsibilities of:

* Cloud Security Engineers
* SOC Engineers
* DevSecOps Engineers
* Security Architects

---

## ✅ Result

Successfully deployed a stable AWS EC2 environment with verified internet, DNS, and routing functionality ready for SOC-SOAR tool deployment.

---

## 🏁 Conclusion

This infrastructure foundation enables reliable deployment of Wazuh, TheHive, MISP, Cortex, Suricata, Zeek, and automation workflows.

A properly designed VPC eliminates 80% of deployment issues and provides a secure baseline for advanced detection engineering.

---

Next Step → Install Core SOC Tools.

---
