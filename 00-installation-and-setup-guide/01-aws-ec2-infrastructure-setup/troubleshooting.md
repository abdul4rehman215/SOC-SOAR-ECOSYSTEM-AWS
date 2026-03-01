# 🛠️ Troubleshooting Guide — Project 01: AWS EC2 Foundation Setup (SOC / SOAR Ecosystem)

> This troubleshooting guide covers the most common issues during AWS EC2 foundation setup, especially network/DNS problems and baseline OS configuration issues.

---

## 📌 Quick Diagnosis Flow (Use This First)

### ✅ Step 1 — Check routing + gateway
```bash
ip route
````

You must see a default route like:

* `default via 10.0.1.1 dev ens5`

### ✅ Step 2 — Check internet (raw IP)

```bash
ping -c 3 8.8.8.8
```

* ❌ If this fails → network routing/egress issue

### ✅ Step 3 — Check DNS (domain name)

```bash
curl -I https://google.com
```

* ❌ If `8.8.8.8` works but `google.com` fails → DNS issue

---

# 🌐 NETWORK + INTERNET ISSUES

---

## 1) ❌ No Internet Access Even With Public IP

### Symptoms

* `ping 8.8.8.8` fails
* `apt update` fails
* `curl https://google.com` fails

### Root Causes

* Missing Internet Gateway (IGW)
* Route table missing `0.0.0.0/0 → IGW`
* Public subnet not associated to correct route table
* Instance launched in wrong subnet (private subnet)
* Security Group outbound rules blocked (rare)
* NACL blocking outbound/return traffic

### Fix Checklist (AWS Console)

✅ **Internet Gateway**

* Ensure IGW exists and is attached to the correct VPC

✅ **Route Table**
Public route table MUST have:

* `0.0.0.0/0 → igw-xxxx`

✅ **Subnet Association**

* Ensure the public subnet is associated with the public route table

✅ **Public IP**

* Ensure instance has a public IPv4 assigned (or attach Elastic IP)

✅ **NACL**

* Ensure inbound + outbound allow traffic (default is OK)

### EC2 Side Commands

```bash
ip a
ip route
ping -c 3 10.0.1.1
ping -c 3 8.8.8.8
```

---

## 2) ❌ `apt update` Fails (Network OK Sometimes, But DNS Broken)

### Symptoms

* `ping 8.8.8.8` works
* `curl https://google.com` fails
* `apt update` shows errors like “Temporary failure resolving…”

### Root Causes

* VPC DNS settings disabled
* Bad resolver config
* DNS not enabled in VPC

### Fix (AWS Console)

In the VPC settings, ensure:

* ✅ DNS Resolution enabled
* ✅ DNS Hostnames enabled

### Fix (Ubuntu EC2)

Check resolver:

```bash
cat /etc/resolv.conf
resolvectl status
```

Try restarting DNS resolver:

```bash
sudo systemctl restart systemd-resolved
resolvectl status
```

Quick temporary resolver test:

```bash
sudo bash -c 'printf "nameserver 8.8.8.8\n" > /etc/resolv.conf'
```

Then test:

```bash
curl -I https://google.com
```

> Note: On Ubuntu, `/etc/resolv.conf` may be managed by systemd-resolved. Permanent fix should be VPC DNS settings + systemd-resolved.

---

## 3) ❌ Instance Has No Public IP / SSH Not Working

### Symptoms

* You cannot SSH into EC2
* EC2 shows no public IPv4

### Root Causes

* Public IP not enabled during launch
* Subnet auto-assign public IPv4 disabled
* Instance launched into private subnet

### Fix

✅ Enable subnet setting:

* Public subnet → **Auto-assign public IPv4 → YES**

✅ Re-launch instance (best clean fix), or:

* Allocate and attach an **Elastic IP**

---

## 4) ❌ SSH Timeout / Connection Refused

### Symptoms

* SSH hangs (timeout) or refused

### Root Causes

* Security Group inbound rule missing port 22
* SSH allowed but source IP is wrong (not your IP)
* NACL blocking
* Instance not running / no route to host
* Wrong username (Ubuntu = `ubuntu`)

### Fix

✅ Security Group inbound should include:

* SSH 22 → **your IP/32**

✅ Confirm your IP:

* Use a “what is my IP” check on your network
* If your IP changes, update SG rule

✅ Use correct username:

```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

✅ Confirm SSH daemon status (if you can access via EC2 serial console / SSM):

```bash
sudo systemctl status ssh --no-pager
```

---

# 🖥️ BASELINE OS ISSUES (TIME / HOSTNAME)

---

## 5) ❌ Wrong Time / Time Drift (SOC Correlation Problems Later)

### Symptoms

* Logs show incorrect timestamps
* SOC alerts later have confusing timelines
* `timedatectl` shows NTP disabled

### Fix

```bash
timedatectl
sudo timedatectl set-ntp yes
timedatectl
```

If Chrony is installed:

```bash
sudo systemctl enable --now chrony
sudo systemctl status chrony --no-pager
```

---

## 6) ❌ Hostname Changed But Doesn’t Resolve Properly

### Symptoms

* Some services show old hostname
* Local apps fail resolving hostname
* `sudo` warnings about hostname lookup

### Root Cause

* `/etc/hosts` still references old hostname

### Fix

Set hostname:

```bash
sudo hostnamectl set-hostname "thehive"
```

Update hosts file:

```bash
sudo nano /etc/hosts
```

Change:

```text
127.0.1.1 old-hostname
```

To:

```text
127.0.1.1 thehive
```

Verify:

```bash
hostnamectl
hostname -f
```

---

# 🔐 SECURITY GROUP + PORT ISSUES (SOC TOOL READINESS)

---

## 7) ❌ SOC Dashboards Not Reachable Later (Ports Not Open)

### Symptoms

* You install tools later (Wazuh/TheHive/MISP)
* Services run locally but not accessible externally

### Root Cause

* Security Group inbound rules not opened for required tool ports

### Fix (Best Practice)

✅ Keep ports closed by default, open only when needed:

* Wazuh Dashboard: 443/5601 (depends on setup)
* TheHive: 9000
* Cortex: 9001
* MISP: 443 (or 80/443 depending)
* n8n: 5678

Also ensure:

* Source = your IP / VPN IP (not 0.0.0.0/0 unless absolutely required)

---

# 🧩 AWS-SPECIFIC SOC ISSUES (COMMON LATER, BUT IMPORTANT)

---

## 8) ❌ No CloudTrail Events / Monitoring Doesn’t Work

### Symptoms

* CloudTrail not generating logs
* SIEM ingest later shows nothing

### Root Causes

* CloudTrail not enabled
* Wrong region selected
* IAM role missing permissions
* Logs delivered to wrong destination (S3/CloudWatch)

### Fix Checklist

* Ensure CloudTrail enabled in correct region
* Validate delivery target (S3 bucket or CloudWatch)
* Ensure IAM permissions exist for delivery + reading

---

## 9) ❌ AWS S3 Wazuh Wodle Silent (No Data)

### Symptoms

* Integration configured but nothing appears

### Root Causes

* Wrong bucket name
* Missing permissions / wrong IAM role
* Wrong region
* Bucket policy blocks access

### Fix Checklist

* Confirm bucket name and region
* Confirm IAM role permissions (list/get)
* Check bucket policy
* Confirm trail is delivering logs to that bucket

---

# 🧾 FINAL QUICK COMMANDS (COPY/PASTE DIAGNOSTICS)

Run these and check outputs:

```bash
ip a
ip route
ping -c 2 10.0.1.1
ping -c 2 8.8.8.8
curl -I https://google.com
cat /etc/resolv.conf
resolvectl status
timedatectl
hostnamectl
ss -tuln
df -h
free -h
```

---

## ✅ Final Advice

* Never rush networking.
* Fix IGW + route table + subnet association first.
* Don’t install tools until **ping + DNS + apt update** work.
* Time and hostname must be correct for SOC correlation later.

---
