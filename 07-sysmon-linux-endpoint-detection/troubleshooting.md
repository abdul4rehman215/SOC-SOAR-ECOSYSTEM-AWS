# 🛠 Troubleshooting & Detection Engineering Guide - Sysmon for Linux + Wazuh  

> This document covers real-world issues encountered during:

- Sysmon deployment
- Wazuh integration
- Decoder creation
- Rule tuning
- Noise reduction
- Detection validation

---

# 1️⃣ Sysmon Service Not Running

## 🔎 Symptoms

- `systemctl status sysmon` shows inactive
- No Sysmon logs in `journalctl`
- No events reaching Wazuh

## 🧪 Diagnosis

```bash
systemctl status sysmon
sysmon -?
````

Check kernel version:

```bash
uname -r
```

## ⚠️ Common Causes

* Invalid `config.xml`
* Kernel incompatibility
* eBPF not supported
* Sysmon not installed properly

## ✅ Fix

Reinstall configuration:

```bash
sudo sysmon -u
sudo sysmon -accepteula -i /opt/config.xml
```

Ensure modern Linux kernel (5.x+ recommended).

---

# 2️⃣ Sysmon Logs Not Appearing in Journal

## 🔎 Symptoms

```bash
journalctl | grep sysmon
```

Returns nothing.

## 🧪 Diagnosis

```bash
journalctl -xe
```

## ⚠️ Causes

* Sysmon service not restarted
* Invalid XML config
* Permission issues

## ✅ Fix

Validate config:

```bash
sudo sysmon -c
```

Reinstall if needed:

```bash
sudo sysmon -accepteula -i /opt/config.xml
```

---

# 3️⃣ Logs Not Appearing in Wazuh Dashboard

## 🔎 Symptoms

* Sysmon running locally
* No alerts in Wazuh

## 🧪 Diagnosis

Check agent:

```bash
systemctl status wazuh-agent
```

Check manager logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

Verify syslog monitoring exists in:

```
/var/ossec/etc/ossec.conf
```

## ✅ Fix

Ensure this block exists:

```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/syslog</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
```

---

# 4️⃣ Decoder Not Working

## 🔎 Symptoms

* Events appear as generic logs
* No structured fields like `system.eventID`

## 🧪 Diagnosis

Test decoder:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

Check decoder file:

```
/var/ossec/etc/decoders/decoder-linux-sysmon.xml
```

## ⚠️ Common Issues

* Incorrect `<program_name>`
* XML formatting errors
* Missing closing tags

## ✅ Correct Decoder Example

```xml
<decoder name="sysmon-linux">
  <program_name>sysmon</program_name>
</decoder>
```

Restart manager:

```bash
sudo systemctl restart wazuh-manager
```

---

# 5️⃣ Rules Not Triggering

## 🔎 Symptoms

* Event visible in dashboard
* No alert generated

## 🧪 Diagnosis

Validate rules:

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

Check:

* Incorrect `<if_sid>`
* Wrong field names
* Rule ID conflicts

## ⚠️ Common Mistake

Using:

```
eventID
```

Instead of:

```
system.eventID
```

Field names must match decoded structure exactly.

---

# 6️⃣ Too Many Alerts (Noise Problem)

## 🔎 Symptoms

* Hundreds of alerts per hour
* Alert fatigue

## 🧪 Observed Noise

* `nano`
* `bash`
* `cron`
* `apt`
* `systemd`

## ✅ Solution Strategy

Lower base rule severity:

```xml
<rule id="200300" level="0">
  <if_sid>200150</if_sid>
  <field name="eventdata.image">nano$|systemd$|cron$|bash$|apt$</field>
  <options>no_full_log</options>
</rule>
```

### Result

* Telemetry preserved
* Alerts drastically reduced
* SOC signal improved

---

# 7️⃣ LOLBins Detection Not Triggering

## 🔎 Symptoms

* Executed `curl | bash`
* No alert triggered

## 🧪 Diagnosis

Check:

```
eventdata.commandLine
```

in Wazuh Discover.

## ⚠️ Cause

Regex mismatch.

## ✅ Correct Regex

```
curl.*bash|wget.*bash
```

Avoid advanced regex unsupported by Wazuh.

---

# 8️⃣ MITRE Mapping Not Visible

## 🔎 Symptoms

* Alert triggered
* No MITRE section displayed

## ⚠️ Cause

Missing `<mitre>` block.

## ✅ Fix

```xml
<mitre>
  <id>T1059</id>
</mitre>
```

Restart manager afterward.

---

# 9️⃣ Wazuh Fails to Restart (Rule Syntax Error)

## 🔎 Symptoms

* Wazuh service fails
* XML error in logs

## 🧪 Diagnosis

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

## ⚠️ Common Errors

* Missing closing tags
* Duplicate rule IDs
* Invalid nesting

Always validate before restarting.

---

# 🔟 Field Extraction Not Matching

## 🔎 Symptoms

* Event ID parsed
* CommandLine missing

## ⚠️ Cause

Decoder not extracting nested XML correctly.

## ✅ Fix

Extend decoder to parse nested fields using proper regex or child decoders.

---

# 1️⃣1️⃣ Alert Triggered with Wrong Severity

## ⚠️ Cause

Base rule overriding detection rule.

## ✅ Fix

Ensure detection rule:

* Has higher severity level
* References correct `<if_sid>`
* Comes after base rule

---

# 1️⃣2️⃣ SOC-Level Noise Tuning Scenario

### Scenario:

Alert volume spikes after deployment.

### SOC Response:

1. Identify top noisy processes
2. Validate business criticality
3. Suppress only benign patterns
4. Never suppress persistence directories
5. Revalidate detections after tuning

This mirrors real detection engineering lifecycle.

---

# 1️⃣3️⃣ Production Hardening Recommendations

* Harden Sysmon configuration
* Add correlation rules
* Integrate with TheHive
* Implement Slack notifications
* Track rule performance metrics
* Add anomaly detection layer

---

# 🧠 Detection Engineering Philosophy

Effective detection is iterative:

Collect → Decode → Tune → Suppress → Detect → Validate → Improve

Never deploy high-volume rules without validation.

Always simulate attacker behavior to confirm detection accuracy.

---

# ✅ Final Takeaway

This project demonstrates:

* Real-world troubleshooting methodology
* Detection tuning workflow
* Noise reduction engineering
* SOC-level incident validation

It reflects production-ready detection engineering practice.

---
