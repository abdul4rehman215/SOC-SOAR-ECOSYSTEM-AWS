# 🛠 Troubleshooting Guide - Wazuh ↔ MISP File Hash Integration  
### AWS SOC Lab Deployment

---

# 🔎 1. Integration Not Triggering

### ❌ Symptom
- Rule 554 appears
- No Rule 100800
- No integration output

### ✅ Checks

### 1️⃣ Verify integration block

File:
```

/var/ossec/etc/ossec.conf

````

Ensure:

```xml
<integration>
  <name>custom-misp-file-hashes.py</name>
  <group>syscheck</group>
  <rule_id>554</rule_id>
  <alert_format>json</alert_format>
</integration>
````

⚠ Common mistake:

* Wrong script name
* Missing `.py`
* Wrong rule_id
* Using `<group>` incorrectly

---

### 2️⃣ Check script permissions

```bash
ls -l /var/ossec/integrations/custom-misp-file-hashes.py
```

Must show:

```
-rwxr-x--- root wazuh
```

Fix if needed:

```bash
chmod 750 /var/ossec/integrations/custom-misp-file-hashes.py
chown root:wazuh /var/ossec/integrations/custom-misp-file-hashes.py
```

---

### 3️⃣ Restart Wazuh

```bash
systemctl restart wazuh-manager
```

---

# 🔎 2. Hash Not Being Queried

### ❌ Symptom

Integration runs but no enrichment.

### ✅ Check

Ensure syscheck contains hash fields:

```json
"md5_after"
"sha1_after"
"sha256_after"
```

If missing:

* Ensure `<directories check_all="yes" realtime="yes">` is set
* Restart agent

Linux agent restart:

```bash
systemctl restart wazuh-agent
```

---

# 🔎 3. MISP API Authentication Error (403)

### ❌ Symptom

Rule 100803 triggered.

### Cause

Invalid API key.

### Fix

1️⃣ Verify API key in MISP:

* MISP → Automation → Auth Keys

2️⃣ Update in:

```
/var/ossec/etc/ossec.conf
```

3️⃣ Restart manager.

---

# 🔎 4. MISP Rate Limit Error (429)

### ❌ Symptom

Rule 100804 triggered.

### Cause

Too many API requests.

### Fix

* Restrict monitored directories
* Reduce high file churn paths
* Limit integration to Rule 554 only
* Consider increasing timeout

---

# 🔎 5. MISP Server Not Responding

### ❌ Symptom

No enrichment
No match
No error

### Test connectivity

From Wazuh server:

```bash
curl -k https://YOUR_MISP_IP
```

If fails:

* Check firewall
* Check Security Group (AWS)
* Verify port 443 open
* Verify MISP service running

---

# 🔎 6. SSL Certificate Error

### ❌ Symptom

Script fails silently.

### Cause

Self-signed certificate.

Your script uses:

```
verify=False
```

For production:

* Install trusted certificate
* Remove insecure bypass

---

# 🔎 7. Rules Not Loading

### ❌ Symptom

Custom rules not triggering.

### Validate syntax

```bash
/var/ossec/bin/wazuh-analysisd -t
```

### Check logs

```bash
grep -i misp /var/ossec/logs/ossec.log
```

---

# 🔎 8. Integration Logs

Check integrator log:

```bash
tail -f /var/ossec/logs/integrations.log
```

Check Wazuh log:

```bash
tail -f /var/ossec/logs/ossec.log
```

---

# 🔎 9. Debug Mode

To enable debug logging:

Add in integration block:

```xml
<options>{"debug": true}</options>
```

Restart:

```bash
systemctl restart wazuh-manager
```

---

# 🔎 10. EICAR Test Not Triggering Match

### Checklist:

- ✔ Hash added in MISP
- ✔ Attribute marked `to_ids=1`
- ✔ Event distribution allows your user
- ✔ API key user has event visibility
- ✔ Hash type correct (md5)
- ✔ MISP event saved

---

# 🔎 11. Script Execution Test (Manual)

You can test manually:

```bash
/var/ossec/integrations/custom-misp-file-hashes.py \
/var/ossec/logs/alerts/alerts.json \
YOUR_API_KEY \
https://YOUR_MISP_IP
```

If no output and no error → script working.

---

# 🔎 12. Common Configuration Mistakes

- ❌ Using wrong integration name
- ❌ Not restarting manager
- ❌ Wrong file permissions
- ❌ Wrong rule_id
- ❌ API key with insufficient privileges
- ❌ Monitoring too many directories
- ❌ MISP event not marked IDS

---

# 🔎 13. AWS-Specific Issues
-
If deployed on AWS EC2:

- ✔ Security Group allows HTTPS
- ✔ MISP EC2 reachable from Wazuh EC2
- ✔ No NACL blocking
- ✔ Correct private/public IP usage
- ✔ Proper DNS resolution

---

# 📊 Quick Health Checklist

- ✔ Script permissions correct
- ✔ Integration block correct
- ✔ Custom rules loaded
- ✔ API key valid
- ✔ HTTPS reachable
- ✔ EICAR test successful
- ✔ Rule 100802 triggered

---

# 🧠 Final Diagnostic Logic

If Rule 554 exists → Agent OK
If 100800 exists → Integration executed
If 100802 exists → Hash match confirmed
If 100803/100804/100805 → Operational issue

This layered rule structure makes troubleshooting systematic and fast.

---

# ✅ Expected Final State

You should see:

* Rule 554 (File created)
* Rule 100800 (Integration triggered)
* Rule 100802 (Hash matched – Level 12)

If all three appear → Integration fully operational.

---

End of Troubleshooting Guide

---
