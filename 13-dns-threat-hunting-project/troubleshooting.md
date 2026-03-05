# 🚨 Troubleshooting Guide - DNS Threat Hunting Pipeline
## Wazuh + DNS-Stats + AlienVault OTX

---

# 1️⃣ Overview

This document provides structured troubleshooting for the full detection pipeline:

Windows Sysmon  
→ Wazuh Agent  
→ Wazuh Manager  
→ DNS-Stats  
→ AlienVault OTX  
→ Wazuh Dashboard  
→ Active Response  

Use this guide when alerts are not appearing, enrichment fails, or integrations break.

---

# 2️⃣ Quick Health Checklist

Before deep troubleshooting, verify:

- [ ] Sysmon installed and logging Event ID 22  
- [ ] Wazuh Agent connected and active  
- [ ] DNS-Stats service running on port 5730  
- [ ] Integration scripts executable  
- [ ] API key valid  
- [ ] Wazuh rules loaded  
- [ ] No syntax errors in XML config  

---

# 3️⃣ Windows Endpoint Issues

---

## ❌ Problem: DNS queries not appearing in Wazuh

### Step 1: Verify Sysmon DNS Logging

On Windows:

Event Viewer →  
Applications and Services Logs →  
Microsoft → Windows → Sysmon → Operational  

Look for:

Event ID: 22

If not present:

Reinstall Sysmon with proper config:

```powershell
Sysmon64.exe -c
Sysmon64.exe -i sysmonconfig.xml
````

Ensure DNS logging is enabled inside config file.

---

## ❌ Problem: Agent not sending logs

On Windows:

Check agent service:

```powershell
Get-Service wazuh
```

Restart if needed:

```powershell
Restart-Service wazuh
```

On Wazuh Manager:

```bash
/var/ossec/bin/agent_control -l
```

Agent must show:
Active

---

# 4️⃣ Wazuh Manager Issues

---

## ❌ Problem: Rule not triggering for Event ID 22

Check logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

Verify rule file:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

Paste sample Sysmon log to confirm matching.

If rule not matching:

* Confirm rule ID correct
* Confirm field name correct (`win.system.eventID`)
* Confirm decoder working

---

## ❌ Problem: Integration script not executing

Check permissions:

```bash
ls -l /var/ossec/integrations/
```

Expected:

* Owner: root
* Group: wazuh
* Permission: 750

Fix:

```bash
sudo chown root:wazuh custom-dnsstats.py
sudo chmod 750 custom-dnsstats.py
```

---

# 5️⃣ DNS-Stats Troubleshooting

---

## ❌ Problem: DNS-Stats not responding

Check if running:

```bash
sudo ss -lntp | grep 5730
```

If not listening:

Restart manually:

```bash
gunicorn --bind 127.0.0.1:5730 domain_stats.server:config_app\('/opt/domain-stats-data'\)
```

---

## ❌ Problem: Integration timeout

Test manually:

```bash
curl http://127.0.0.1:5730/google.com
```

If slow:

* Check system load
* Check Python process CPU usage
* Consider running as systemd service

---

## ❌ Problem: DNS-Stats returns empty results

Possible causes:

* Domain never seen before
* Database not initialized
* Cache directory permissions incorrect

Reinitialize:

```bash
domain_stats --init /opt/domain-stats-data
```

---

# 6️⃣ AlienVault OTX Issues

---

## ❌ Problem: OTX script not returning malicious result

Test manually:

```bash
curl -H "X-OTX-API-KEY: YOUR_KEY" \
https://otx.alienvault.com/api/v1/indicators/domain/example.com/general
```

Check:

* pulse_info.count > 0 ?

If 0:

Domain not in OTX pulses.

---

## ❌ Problem: API rate limit

Symptoms:

* 429 HTTP error
* Script fails randomly

Solution:

* Reduce integration trigger frequency
* Cache OTX responses
* Use paid API tier if needed

---

## ❌ Problem: Invalid API Key

Error:

401 Unauthorized

Fix:

* Regenerate API key
* Replace in script
* Restart Wazuh

---

# 7️⃣ Wazuh Dashboard Issues

---

## ❌ Problem: Alerts not visible in dashboard

Check:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json
```

If alerts exist but not visible:

* Check index pattern
* Refresh dashboard
* Verify rule level >= 3

---

## ❌ Problem: Fields missing in alert

Cause:

Integration output not formatted correctly.

Ensure integration prints valid JSON:

```python
print(json.dumps(output))
```

No extra print statements allowed.

---

# 8️⃣ Active Response Issues

---

## ❌ Problem: Script not executing on Windows

Check:

Location:

```
C:\Program Files (x86)\ossec-agent\active-response\bin\
```

Verify:

* File exists
* Execution policy allows PowerShell

Test manually:

```powershell
powershell.exe -ExecutionPolicy Bypass -File "C:\Scripts\otx.ps1" testdomain.com
```

---

## ❌ Problem: Active Response not triggering

Check:

* Rule level >= configured threshold
* `<rules_group>` matches
* Wazuh restarted after config change

---

# 9️⃣ Performance Optimization

---

## 🟢 Optimize DNS-Stats

* Run as systemd service
* Allocate sufficient memory
* Monitor CPU usage

---

## 🟢 Optimize OTX Integration

* Cache results locally
* Avoid repeated lookups
* Limit to suspicious domains only

---

## 🟢 Optimize Wazuh Rules

* Avoid excessive regex
* Use targeted conditions
* Tune frequency thresholds

---

# 🔟 Advanced Debugging

---

## Enable Debug Mode

Edit:

```
/var/ossec/etc/ossec.conf
```

Set:

```xml
<logall>yes</logall>
<logall_json>yes</logall_json>
```

Restart Wazuh.

---

## Test Integration Directly

Simulate alert input:

```bash
echo '{"data":{"win":{"eventdata":{"queryName":"google.com"}}}}' \
| python3 custom-dnsstats.py
```

Verify JSON output.

---

# 1️⃣1️⃣ Security Hardening Recommendations

* Store API keys as environment variables
* Restrict integration script permissions
* Use firewall rules to restrict 5730 access
* Monitor integration logs
* Avoid exposing DNS-Stats publicly

---

# 1️⃣2️⃣ Common Real-World Failure Points

| Issue            | Root Cause                |
| ---------------- | ------------------------- |
| No enrichment    | Integration not triggered |
| False positives  | Threshold too low         |
| API failures     | Rate limit or key invalid |
| Slow performance | Excessive DNS queries     |
| Script errors    | Invalid JSON formatting   |

---

# 1️⃣3️⃣ Final Validation Checklist

Full pipeline is working if:

1. DNS query generated
2. Sysmon logs Event ID 22
3. Wazuh detects DNS event
4. DNS-Stats enriches successfully
5. Suspicious rule triggers
6. OTX validates IOC (if malicious)
7. Dashboard shows enriched alert
8. Active response executes (optional)

---

# 1️⃣4️⃣ When Escalating to Production

Before deploying in enterprise:

* Tune thresholds
* Monitor API usage
* Implement caching
* Validate performance under load
* Document API key handling
* Test failure handling

---

# 🏁 Final Note

This project builds a multi-stage detection pipeline.

If any single component fails:

The chain breaks.

Always debug from the bottom up:

1. Endpoint
2. Agent
3. Manager
4. Integration
5. Dashboard

Layer-by-layer validation is the key.

---
