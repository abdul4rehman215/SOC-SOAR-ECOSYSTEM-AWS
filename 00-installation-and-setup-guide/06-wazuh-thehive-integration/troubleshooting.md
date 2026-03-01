# 🛠 Wazuh ↔ TheHive Integration Troubleshooting Guide

> This guide covers the most common issues observed when integrating **Wazuh Manager** with **TheHive 5.5** on AWS EC2.

---

# 🔍 1️⃣ No Alerts Appearing in TheHive

## Symptoms
- No alerts created in TheHive
- No errors shown in UI
- Integration test shows no output

## Check 1: Manual Integration Test

Run:

```bash
/var/ossec/integrations/custom-w2thive \
/var/ossec/logs/alerts/alerts.json \
YOUR_API_KEY \
http://THEHIVE_IP:9000
```

If no output → success  
If error → review message carefully

---

## Check 2: Integration Logs

```bash
tail -f /var/ossec/logs/integrations.log
```

If file does not exist:
- Logging path incorrect
- Script permissions issue

---

# 🔐 2️⃣ API Key Authentication Error (401 / 403)

## Symptoms
- 401 Unauthorized
- 403 Forbidden

## Causes
- Invalid API key
- Expired key
- Wrong user permissions in TheHive

## Fix

1. Login to TheHive
2. Go to:
   ```
   User Profile → API Key
   ```
3. Generate new key
4. Update inside:
   ```
   /var/ossec/etc/ossec.conf
   ```

Restart Wazuh:

```bash
systemctl restart wazuh-manager
```

---

# 🌐 3️⃣ Connection Refused / Timeout

## Symptoms
- Connection refused
- Timeout errors

## Root Causes

- TheHive not running
- Wrong port
- Security Group blocking port 9000
- Wrong IP used

## Fix

### Check TheHive Service

```bash
docker ps
```

Confirm container running.

### Check Port Listening

```bash
ss -tulnp | grep 9000
```

### Check AWS Security Group

Ensure:

| Port | Protocol | Source |
|------|----------|--------|
| 9000 | TCP | Wazuh Server IP |

---

# 📁 4️⃣ Script Not Executing

## Symptoms
- No logs generated
- No integration triggered

## Causes
- File not executable
- Wrong file location

## Fix

```bash
chmod +x /var/ossec/integrations/custom-w2thive
chmod +x /var/ossec/integrations/custom-w2thive.py
```

Confirm location:

```bash
ls -l /var/ossec/integrations/
```

---

# 🧠 5️⃣ thehive4py Module Not Found

## Symptoms
ImportError: No module named thehive4py

## Cause
Installed in wrong Python environment.

## Fix

Install using Wazuh embedded Python:

```bash
/var/ossec/framework/python/bin/pip3 install thehive4py==1.8.1
```

Verify:

```bash
/var/ossec/framework/python/bin/pip3 list | grep thehive4py
```

---

# 🔄 6️⃣ Integration Not Triggering on Low Severity Alerts

## Cause
Threshold filtering inside script:

```python
lvl_threshold = 0
suricata_lvl_threshold = 3
```

And in ossec.conf:

```xml
<level>9</level>
```

If alert level < threshold → alert will NOT be sent.

Adjust as required.

---

# 📄 7️⃣ ossec.conf Misconfiguration

Ensure correct block:

```xml
<integration>
  <name>custom-w2thive</name>
  <hook_url>http://THEHIVE_IP:9000</hook_url>
  <api_key>YOUR_API_KEY</api_key>
  <alert_format>json</alert_format>
  <level>9</level>
</integration>
```

After editing:

```bash
systemctl restart wazuh-manager
```

---

# 🧾 8️⃣ Debug Mode (Advanced Troubleshooting)

To enable detailed logging:

Inside `custom-w2thive.py`:

```python
debug_enabled = True
```

Restart Wazuh and monitor:

```bash
tail -f /var/ossec/logs/integrations.log
```

---

# 🚨 9️⃣ Suricata Alerts Not Appearing

The script filters Suricata alerts using:

```python
suricata_lvl_threshold = 3
```

If Suricata severity > threshold → ignored.

Adjust accordingly.

---

# 🏁 Final Validation Checklist

✔ thehive4py installed  
✔ Scripts executable  
✔ API key valid  
✔ ossec.conf configured  
✔ Wazuh restarted  
✔ Security group allows 9000  
✔ TheHive running  

---

# 🛡 Security Recommendation

- Never expose port 9000 publicly
- Restrict to Wazuh server IP
- Rotate API keys periodically
- Monitor integration logs for anomalies

---

# 🎯 Result

Once correctly configured:

- Wazuh alerts automatically appear in TheHive
- Alerts can be converted to cases
- SOC workflow becomes centralized
- Incident response becomes structured and trackable
