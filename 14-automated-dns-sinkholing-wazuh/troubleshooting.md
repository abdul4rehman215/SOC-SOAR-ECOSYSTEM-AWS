# 🚨 Troubleshooting Guide - Automated DNS Sinkholing using Wazuh Active Response

---

# 1️⃣ Overview

This document helps troubleshoot issues across the full detection → enrichment → validation → containment pipeline.

Pipeline Components:

1. Windows Endpoint (Sysmon)
2. Wazuh Agent
3. Wazuh Manager
4. DNS-Stats
5. AlienVault OTX
6. Active Response
7. HOSTS file modification

If any one layer fails, containment will not occur.

Always troubleshoot from bottom to top.

---

# 2️⃣ Quick Health Checklist

Before deep debugging, verify:

- [ ] Sysmon installed and logging Event ID 22
- [ ] Wazuh Agent connected
- [ ] DNS-Stats running on port 5730
- [ ] OTX API key valid
- [ ] Rule ID 100080 exists
- [ ] Active Response configured in ossec.conf
- [ ] PowerShell script exists and executable
- [ ] CMD wrapper in correct directory

---

# 3️⃣ Windows Endpoint Troubleshooting

---

## ❌ DNS Query Not Logged in Sysmon

Check:

Event Viewer  
→ Applications and Services Logs  
→ Microsoft  
→ Windows  
→ Sysmon  
→ Operational  

Look for Event ID 22.

If missing:

Reinstall Sysmon with proper config:

```powershell
Sysmon64.exe -c
Sysmon64.exe -i sysmonconfig.xml
````

Ensure DNS logging enabled in configuration file.

---

## ❌ Wazuh Agent Not Connected

On Windows:

```cmd
sc query wazuh
```

Restart:

```cmd
net stop wazuh-agent
net start wazuh-agent
```

On Manager:

```bash
/var/ossec/bin/agent_control -l
```

Agent must show as Active.

---

## ❌ PowerShell Script Not Executing

Check log file:

```powershell
type C:\Windows\Temp\sinkhole.log
```

If no log created:

Test manually:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Windows\PowerShell\malicious_domains.ps1
```

Check execution policy:

```powershell
Get-ExecutionPolicy
```

If Restricted:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope LocalMachine
```

---

## ❌ HOSTS File Not Modified

Check file:

```
C:\Windows\System32\drivers\etc\hosts
```

Ensure:

* Script running as Administrator
* File not locked
* No permission errors

Test manual append:

```powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "`n127.0.0.1 test.com"
```

If fails → permission issue.

---

# 4️⃣ Wazuh Manager Troubleshooting

---

## ❌ Rule 100080 Not Triggering

Test rule with:

```bash
/var/ossec/bin/wazuh-logtest
```

Paste sample alert JSON.

Check rule file:

```bash
sudo nano /var/ossec/etc/rules/local_otx.xml
```

Restart manager after changes:

```bash
sudo systemctl restart wazuh-manager
```

---

## ❌ Active Response Not Triggering

Check ossec.conf:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Verify:

```
<command>
  <name>malicious_domains</name>
  <executable>domains.cmd</executable>
</command>
```

And:

```
<active-response>
  <command>malicious_domains</command>
  <rules_id>100080</rules_id>
</active-response>
```

Restart Wazuh:

```bash
sudo systemctl restart wazuh-manager
```

---

## ❌ Integration Script Failing

Check permissions:

```bash
ls -l /var/ossec/integrations/
```

Should be:

Owner: root
Group: wazuh
Permission: 750

Fix:

```bash
sudo chown root:wazuh custom-alienvault.py
sudo chmod 750 custom-alienvault.py
```

---

# 5️⃣ DNS-Stats Troubleshooting

---

## ❌ DNS-Stats Not Running

Check port:

```bash
sudo ss -lntp | grep 5730
```

If not listening:

Restart manually:

```bash
gunicorn --bind 127.0.0.1:5730 domain_stats.server:config_app\('/opt/domain-stats-data'\)
```

Test API:

```bash
curl http://127.0.0.1:5730/google.com
```

---

## ❌ Slow DNS-Stats Response

Possible causes:

* High CPU load
* Large SQLite database
* Insufficient RAM

Mitigation:

* Restart service
* Allocate more memory
* Run as systemd service
* Monitor with top command

---

# 6️⃣ AlienVault OTX Troubleshooting

---

## ❌ OTX API Not Responding

Test manually:

```bash
curl -H "X-OTX-API-KEY: YOUR_KEY" \
https://otx.alienvault.com/api/v1/indicators/domain/acmetoy.com/general
```

If 401 → Invalid API key
If 429 → Rate limit exceeded

Mitigation:

* Regenerate API key
* Reduce API calls
* Cache results locally

---

## ❌ OTX Not Marking Domain as Malicious

Check:

```
pulse_info.count
```

If 0 → domain not in OTX.

Choose known malicious test domain from OTX pulses.

---

# 7️⃣ Dashboard Troubleshooting

---

## ❌ Alerts Not Appearing

Check alerts file:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json
```

If alerts present but not visible:

* Refresh index pattern
* Ensure rule level >= 3
* Confirm dashboard filters

---

## ❌ Active Response Alert Not Visible

Search in dashboard:

```
rule.id:100080
```

If missing:

Check manager logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

---

# 8️⃣ End-to-End Validation Checklist

Full pipeline working if:

1. DNS query generated
2. Sysmon logs Event ID 22
3. Wazuh detects DNS query
4. DNS-Stats enrichment visible
5. OTX alert generated
6. Active Response triggered
7. HOSTS file modified
8. Re-test resolves to 127.0.0.1
9. Sysmon logs localhost resolution

---

# 9️⃣ Common Real-World Failure Points

| Issue                   | Root Cause                  |
| ----------------------- | --------------------------- |
| No containment          | Rule ID mismatch            |
| Script not executing    | Permission error            |
| No enrichment           | Integration not linked      |
| High false positives    | DNS-Stats threshold too low |
| OTX failures            | API rate limit              |
| Duplicate HOSTS entries | No duplication check        |

---

# 🔟 Security Hardening Recommendations

* Store API key as environment variable
* Restrict script permissions
* Monitor Active Response logs
* Implement automatic un-sinkholing policy
* Log all containment actions
* Periodically review HOSTS file entries

---

# 1️⃣1️⃣ Debug Strategy

Always debug in this order:

1. Windows DNS event
2. Agent connectivity
3. Manager detection
4. DNS-Stats enrichment
5. OTX validation
6. Active Response execution
7. Endpoint modification

Layer-by-layer debugging prevents confusion.

---

# 1️⃣2️⃣ Final Notes

This is a multi-stage automated defense system.

If containment fails:

It is almost always one of:

* Rule misconfiguration
* Permission issue
* Integration mismatch
* Incorrect field extraction in script

Always validate JSON structure carefully.

---

# END OF TROUBLESHOOTING GUIDE
