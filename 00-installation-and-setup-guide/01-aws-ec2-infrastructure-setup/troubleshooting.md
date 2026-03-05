# 🚨 Troubleshooting Guide - AWS EC2 Infrastructure Setup
### SOC-SOAR Ecosystem Foundation

---

## 📌 Overview

This document outlines common real-world issues encountered during AWS EC2 infrastructure setup and their root causes, diagnostics, and resolution steps.

Most deployment failures originate from network misconfiguration — especially VPC, route tables, and security group issues.

---

# 🌐 1️⃣ No Internet Connectivity

## ❌ Symptoms

- `ping 8.8.8.8` fails
- `apt update` fails
- `curl https://google.com` fails
- Docker install fails
- Git clone fails

---

## 🔍 Possible Root Causes

| Cause | Description |
|--------|------------|
| Missing Internet Gateway | IGW not attached to VPC |
| Bad Route Table | No 0.0.0.0/0 → IGW route |
| Subnet not associated | Route table not linked to subnet |
| Public IP disabled | Instance has no public IPv4 |
| NACL blocking outbound | Return traffic blocked |
| Security group outbound restricted | Outbound not allowed |

---

## 🛠️ Diagnostics

```bash
ip route
ping -c 3 10.0.1.1
ping -c 3 8.8.8.8
````

Check in AWS Console:

* VPC → Internet Gateway attached?
* Route Table → 0.0.0.0/0 → igw-xxxx?
* Subnet → Associated Route Table?
* EC2 → Public IP enabled?

---

## ✅ Fix

* Attach IGW
* Add 0.0.0.0/0 route to IGW
* Associate route table to public subnet
* Enable public IPv4
* Ensure outbound rule allows 0.0.0.0/0

---

# 🌍 2️⃣ DNS Not Working

## ❌ Symptoms

* `ping 8.8.8.8` works
* `curl google.com` fails
* `apt update` fails with DNS error

---

## 🔍 Root Causes

| Cause                           | Description          |
| ------------------------------- | -------------------- |
| DNS Resolution disabled in VPC  | VPC DNS disabled     |
| /etc/resolv.conf corrupted      | Incorrect nameserver |
| Security group outbound blocked | DNS traffic blocked  |
| Custom DNS misconfiguration     | Wrong resolver       |

---

## 🛠️ Diagnostics

```bash
cat /etc/resolv.conf
nslookup google.com
dig google.com
```

Check VPC settings:

* DNS Resolution → Enabled
* DNS Hostnames → Enabled

---

## ✅ Fix

Enable DNS in VPC:

VPC → Edit → Enable DNS Resolution
VPC → Edit → Enable DNS Hostnames

If needed:

```bash
sudo nano /etc/resolv.conf
```

Add:

```
nameserver 8.8.8.8
nameserver 1.1.1.1
```

---

# 🔐 3️⃣ SSH Connection Refused

## ❌ Symptoms

* SSH timeout
* Permission denied
* Connection refused

---

## 🔍 Root Causes

| Cause                           | Description         |
| ------------------------------- | ------------------- |
| Security group missing SSH rule | Port 22 not allowed |
| Wrong key pair                  | Incorrect .pem file |
| File permission wrong           | Key not 400         |
| Wrong public IP                 | Instance restarted  |

---

## 🛠️ Diagnostics

Check Security Group:

Inbound Rule:

* SSH (22) → Your IP

Verify key permissions:

```bash
chmod 400 your-key.pem
```

Connect properly:

```bash
ssh -i your-key.pem ubuntu@PUBLIC_IP
```

---

## ✅ Fix

* Add SSH rule (port 22)
* Restrict to your public IP
* Correct key permissions
* Verify instance public IP

---

# 🛑 4️⃣ apt Update Fails

## ❌ Symptoms

* Repository unreachable
* Temporary failure resolving

---

## 🔍 Root Causes

| Cause              | Description                     |
| ------------------ | ------------------------------- |
| DNS issue          | Name resolution failure         |
| Outbound blocked   | Security group outbound blocked |
| Network unstable   | Packet loss                     |
| Interrupted update | Lock file issue                 |

---

## 🛠️ Diagnostics

```bash
ping 8.8.8.8
curl https://google.com
sudo lsof /var/lib/dpkg/lock
```

---

## ✅ Fix

If lock issue:

```bash
sudo rm /var/lib/dpkg/lock-frontend
sudo dpkg --configure -a
```

Then retry:

```bash
sudo apt update
```

---

# 🔥 5️⃣ Dashboard Not Accessible (Port 443 / 5601 / 9000)

## ❌ Symptoms

* Browser cannot connect
* Connection refused

---

## 🔍 Root Causes

| Cause                            | Description      |
| -------------------------------- | ---------------- |
| Security group missing port rule | Port not allowed |
| Service not running              | Service crashed  |
| Firewall blocking                | UFW active       |
| Wrong public IP                  | IP changed       |

---

## 🛠️ Diagnostics

```bash
sudo ss -tulnp
sudo ufw status
sudo systemctl status service-name
```

Check Security Group inbound rules.

---

## ✅ Fix

Add inbound rule:

* TCP 443 → Your IP
* TCP 5601 → Your IP
* TCP 9000 → Your IP

Disable UFW if required:

```bash
sudo ufw disable
```

---

# 🧠 6️⃣ AWS Metadata Service Not Working

## ❌ Symptoms

* Cloud integrations fail
* IAM role not detected

---

## 🔍 Root Causes

| Cause                             | Description           |
| --------------------------------- | --------------------- |
| No IAM role attached              | Instance role missing |
| IMDSv2 misconfigured              | Metadata blocked      |
| Firewall blocking 169.254.169.254 | Local firewall issue  |

---

## 🛠️ Diagnostics

```bash
curl http://169.254.169.254/latest/meta-data/
```

---

## ✅ Fix

* Attach IAM role to EC2
* Ensure IMDSv2 enabled
* Check firewall rules

---

# 🗄️ 7️⃣ Disk Full Errors

## ❌ Symptoms

* Install fails
* Logs not writing
* Docker failing

---

## 🛠️ Diagnostics

```bash
df -h
```

---

## ✅ Fix

Resize EBS volume in AWS → Modify Volume
Then inside instance:

```bash
sudo growpart /dev/nvme0n1 1
sudo resize2fs /dev/nvme0n1p1
```

---

# ⚠️ 8️⃣ NACL Blocking Traffic

## ❌ Symptoms

* Random connectivity failures
* Ping works but service doesn't
* Return traffic blocked

---

## 🔍 Explanation

NACLs are stateless.

Inbound AND outbound rules must allow return traffic.

---

## ✅ Fix

Allow:

Inbound:

* ALL traffic → 0.0.0.0/0

Outbound:

* ALL traffic → 0.0.0.0/0

---

# 🏁 Final Troubleshooting Strategy

Always troubleshoot in this order:

- 1️⃣ Local Interface
- 2️⃣ Gateway Reachability
- 3️⃣ External IP Reachability
- 4️⃣ DNS Resolution
- 5️⃣ Security Groups
- 6️⃣ Route Table
- 7️⃣ Internet Gateway
- 8️⃣ NACL

Never install software before network validation is 100% successful.

---

# 🧠 Key Takeaway

Cloud infrastructure reliability begins with network correctness.

If EC2 networking is stable:

* SIEM deployment becomes smooth
* Threat intelligence integrations work
* Dashboards remain accessible
* Automation pipelines remain stable

If networking is unstable:
Everything else will fail silently.

---

## ✅ Status

Infrastructure validated and ready for SOC tool deployment.

---

Next Phase → Wazuh Installation Guide

---
