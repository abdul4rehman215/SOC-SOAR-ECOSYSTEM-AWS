# 🛠️ Troubleshooting Guide — Project 03: Wazuh All-in-One Installation (AWS EC2)

> This guide covers the most common Wazuh installation and access issues encountered in an AWS EC2 environment, including dashboard availability, indexer stability, agent connectivity, enrollment failures, and configuration mistakes.

---

## 📌 Quick Diagnosis Flow (Use This First)

### 1) Check core services
```bash
sudo systemctl status wazuh-manager --no-pager
sudo systemctl status filebeat --no-pager || true
sudo systemctl status wazuh-dashboard --no-pager || true
sudo systemctl status wazuh-indexer --no-pager || true
````

### 2) Check listening ports locally

```bash
sudo ss -tuln | grep -E ':(443|1514|1515|55000|9200)\b' || true
```

### 3) Check Wazuh manager logs

```bash
sudo tail -n 80 /var/ossec/logs/ossec.log
```

---

# 🌐 DASHBOARD ACCESS ISSUES

---

## 1) ❌ Wazuh Dashboard Not Accessible (Browser can’t open https://<PUBLIC-IP>)

### Symptoms

* Browser shows:

  * "This site can’t be reached"
  * timeout / connection refused
* You cannot load login page on:

  * `https://<EC2_PUBLIC_IP>`

### Root Causes

* Security Group does not allow inbound **443/TCP**
* Instance does not have a public IP / Elastic IP
* Dashboard service down
* Local firewall blocking 443

### Fix (AWS Side)

✅ Ensure Security Group inbound includes:

* 443/TCP → Your IP (recommended)
* 443/TCP → 0.0.0.0/0 (not recommended, only if absolutely required)

✅ Ensure instance has:

* Public IPv4 enabled OR Elastic IP

### Fix (Server Side)

Check dashboard service:

```bash
sudo systemctl status wazuh-dashboard --no-pager || true
sudo systemctl restart wazuh-dashboard || true
sudo systemctl status wazuh-dashboard --no-pager || true
```

Check if port 443 is listening:

```bash
sudo ss -tuln | grep ':443' || true
```

If UFW is enabled:

```bash
sudo ufw status verbose
sudo ufw allow 443/tcp
sudo ufw reload
```

---

## 2) ⚠️ Browser SSL Warning (Certificate Not Trusted)

### Symptoms

* Browser warning about insecure/self-signed certificate

### Root Cause

* Wazuh uses a self-signed certificate by default

### Fix

* Proceed/accept the warning (expected for lab)
* Optionally replace cert later (not required for portfolio lab)

---

# 🧠 INDEXER ISSUES (MOSTLY MEMORY / DISK RELATED)

---

## 3) ❌ Indexer Crash / Dashboard Unstable / High Swap

### Symptoms

* Dashboard loads slowly or stops responding
* Indexer service fails or restarts
* System becomes slow (high memory usage)
* `wazuh-indexer` fails to start

### Root Causes

* Instance RAM too low (< 8GB for All-in-One)
* Disk space low
* Heavy indexing load / background tasks

### Fix

Check memory and swap:

```bash
free -h
swapon --show
```

Check disk:

```bash
df -h
```

Check indexer status/logs:

```bash
sudo systemctl status wazuh-indexer --no-pager || true
sudo journalctl -u wazuh-indexer --no-pager -n 200 || true
```

Recommended fix (AWS):

* Upgrade instance type to `t2.large` / `t3.large` (8GB)
* Increase EBS volume (100GB+ recommended)

---

# 🔌 AGENT CONNECTIVITY ISSUES

---

## 4) ❌ Agents Not Connecting (No active agents in dashboard)

### Symptoms

* Agents appear disconnected
* No agent events received
* "Never connected" or no heartbeat

### Root Causes

* Port **1514/TCP** blocked in Security Group
* Agent configured to wrong manager IP/hostname
* Network path blocked between endpoint and server

### Fix (AWS Security Group)

Allow inbound:

* 1514/TCP → from agent network range (or your lab IPs)

### Fix (Server checks)

Confirm port listening:

```bash
sudo ss -tuln | grep ':1514' || true
```

Confirm manager running:

```bash
sudo systemctl status wazuh-manager --no-pager
```

---

## 5) ❌ Enrollment Fails (Agent cannot register)

### Symptoms

* Agent enrollment fails
* Agents cannot request enrollment
* authd/enrollment errors

### Root Causes

* Port **1515/TCP** blocked in Security Group
* Enrollment not enabled / authd service misconfigured
* Wrong enrollment method used

### Fix (AWS Security Group)

Allow inbound:

* 1515/TCP → agent networks/subnets

### Fix (Server checks)

Confirm port listening:

```bash
sudo ss -tuln | grep ':1515' || true
```

Confirm auth section exists in `/var/ossec/etc/ossec.conf`:

* `<auth> ... <port>1515</port> ... </auth>`

Restart manager after config change:

```bash
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager --no-pager
```

---

# 🔑 API / INTERNAL SERVICE ISSUES

---

## 6) ❌ Wazuh API Not Reachable (Dashboard shows API issues)

### Symptoms

* Dashboard loads but some sections fail
* API-related errors appear

### Root Causes

* Port 55000 blocked locally or SG restricted incorrectly
* Manager API service issues

### Fix

Check local listening:

```bash
sudo ss -tuln | grep ':55000' || true
```

If you need remote API access:

* Restrict 55000/TCP to Admin IP/VPN only

Restart manager:

```bash
sudo systemctl restart wazuh-manager
```

---

## 7) ⚠️ Indexer API (9200) exposed publicly (Security Risk)

### Symptoms

* 9200 open to internet in Security Group

### Root Cause

* Overly permissive SG inbound rules

### Fix

* Remove 9200 from public inbound
* Keep it internal only (localhost/VPC security group reference)

Verify local only use is fine:

```bash
sudo ss -tuln | grep ':9200' || true
```

---

# ⚙️ CONFIGURATION ISSUES (`ossec.conf`)

---

## 8) ❌ Wazuh Manager Fails After Editing `ossec.conf`

### Symptoms

* `wazuh-manager` fails to start after config changes
* Errors in `ossec.log`

### Root Causes

* XML syntax error (missing closing tags)
* Invalid module config
* Incorrect nesting

### Fix

Restore from backup:

```bash
sudo cp /var/ossec/etc/ossec.conf.backup /var/ossec/etc/ossec.conf
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager --no-pager
```

Check logs:

```bash
sudo tail -n 120 /var/ossec/logs/ossec.log
```

✅ Best practice:

* Edit config carefully
* Restart only `wazuh-manager` after changes
* Keep backups per change set

---

# 🧪 VALIDATION FAILURES (DASHBOARD SHOWS NO DATA)

---

## 9) ❌ No Security Events / Vulnerabilities Not Showing

### Symptoms

* Dashboard loads but data seems empty
* Vulnerability tab shows nothing

### Root Causes

* No agents connected (no endpoint telemetry)
* Inventory not populated yet (syscollector timing)
* Vulnerability feeds still updating
* Filebeat/indexer issues

### Fix

Confirm at least one agent exists (later project):

* Agent must connect to generate endpoint data

Check manager + filebeat:

```bash
sudo systemctl status wazuh-manager --no-pager
sudo systemctl status filebeat --no-pager || true
```

Check logs:

```bash
sudo tail -n 80 /var/ossec/logs/ossec.log
```

Be patient for initial feed sync (few minutes), then refresh.

---

# ✅ FINAL DIAGNOSTIC COMMANDS (COPY/PASTE)

```bash
sudo systemctl status wazuh-manager --no-pager
sudo systemctl status filebeat --no-pager || true
sudo systemctl status wazuh-dashboard --no-pager || true
sudo systemctl status wazuh-indexer --no-pager || true

sudo ss -tuln | grep -E ':(443|1514|1515|55000|9200)\b' || true

free -h
df -h

sudo tail -n 120 /var/ossec/logs/ossec.log
```

---

## ✅ Final Notes

* Dashboard access issues are usually **443 blocked**
* Agent issues are usually **1514/1515 blocked**
* Indexer issues are usually **low RAM / high swap**
* Always backup `ossec.conf` before edits and restart only `wazuh-manager`

---
