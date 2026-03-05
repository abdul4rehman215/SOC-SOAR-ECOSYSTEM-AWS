# 🛠 Troubleshooting & Real-World Debugging Guide - Suricata + Wazuh SOC Project  

> This document covers common issues encountered during:

- Suricata installation
- Wazuh integration
- JSON decoding
- Custom rule creation
- MITRE mapping
- Dashboard validation
- Agent grouping

This reflects real SOC troubleshooting methodology.

---

# 🔹 SECTION 1 — Suricata Issues

---

## 1️⃣ Suricata Service Not Starting

### 🔎 Symptoms

- `systemctl status suricata` shows failed
- No eve.json file generated
- Journal shows configuration errors

### 🧪 Diagnose

```bash
sudo systemctl status suricata
sudo journalctl -xe
````

### ⚠️ Common Causes

* Incorrect interface in `suricata.yaml`
* Syntax error in YAML
* Invalid HOME_NET configuration
* Missing rule path

### ✅ Fix

Validate configuration:

```bash
sudo suricata -T -c /etc/suricata/suricata.yaml
```

Correct interface:

```yaml
af-packet:
  - interface: eth0
```

Restart:

```bash
sudo systemctl restart suricata
```

---

## 2️⃣ eve.json Not Generating

### 🔎 Symptoms

* `/var/log/suricata/eve.json` missing
* No alerts even during scans

### ⚠️ Cause

EVE logging disabled.

### ✅ Fix

Ensure in `suricata.yaml`:

```yaml
outputs:
  - eve-log:
      enabled: yes
      filename: /var/log/suricata/eve.json
```

Restart Suricata.

---

## 3️⃣ No Alerts Triggering During Nmap Scan

### 🔎 Symptoms

* Nmap runs successfully
* No Suricata alerts

### ⚠️ Possible Causes

* Rules not loaded
* HOME_NET incorrectly defined
* Traffic not hitting monitored interface

### ✅ Fix

Check rules loaded:

```bash
sudo suricata -T -c /etc/suricata/suricata.yaml
```

Verify network interface:

```bash
ip a
```

Ensure correct HOME_NET:

```yaml
HOME_NET: "[192.168.1.0/24]"
```

---

# 🔹 SECTION 2 — Wazuh Integration Issues

---

## 4️⃣ Suricata Logs Not Appearing in Wazuh

### 🔎 Symptoms

* eve.json exists
* No alerts in dashboard

### 🧪 Diagnose

Check agent status:

```bash
sudo systemctl status wazuh-agent
```

Check manager logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

### ⚠️ Common Causes

* `<localfile>` block missing
* Incorrect log path
* JSON log_format not specified

### ✅ Fix

Ensure agent config includes:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
```

---

## 5️⃣ Wazuh Manager Fails After Adding Custom Rules

### 🔎 Symptoms

* Wazuh service fails to restart
* XML syntax error

### 🧪 Diagnose

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

### ⚠️ Common Causes

* Missing closing tag
* Duplicate rule ID
* Invalid nesting

### ✅ Fix

* Ensure unique rule IDs
* Validate XML structure
* Test before restart

---

# 🔹 SECTION 3 — Decoder Issues

---

## 6️⃣ Fields Not Extracted Properly

### 🔎 Symptoms

* Only full_log visible
* src_ip not parsed
* signature not searchable

### ⚠️ Cause

Decoder not matching JSON structure.

### ✅ Fix

Test decoder:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

Verify regex matches:

```xml
<regex>"src_ip":"([^"]+)"</regex>
```

Restart manager.

---

## 7️⃣ Custom Rules Not Triggering

### 🔎 Symptoms

* Alert visible
* Custom rule not firing

### ⚠️ Causes

* Incorrect `<if_sid>`
* Field name mismatch
* Wrong rule ordering

### ✅ Fix

Inspect base rule SID in Discover.

Ensure:

```xml
<if_sid>86600</if_sid>
```

Field must match exact JSON structure.

---

# 🔹 SECTION 4 — Noise Reduction Issues

---

## 8️⃣ Too Many Alerts (Alert Fatigue)

### 🔎 Symptoms

* Hundreds of informational alerts
* SOC dashboard cluttered

### ✅ Solution Strategy

* Identify frequent low-value signatures
* Suppress using level 0 rules
* Normalize severity
* Retain telemetry but reduce alert generation

Example:

```xml
<rule id="200300" level="0">
  <if_sid>86601</if_sid>
</rule>
```

---

# 🔹 SECTION 5 — MITRE Mapping Issues

---

## 9️⃣ MITRE Fields Not Appearing

### 🔎 Symptoms

* Alert triggers
* No MITRE tactic visible

### ⚠️ Cause

Missing `<mitre>` block in rule.

### ✅ Fix

```xml
<mitre>
  <id>T1595</id>
</mitre>
```

Restart manager.

---

# 🔹 SECTION 6 — Agent Group Issues (Part 3)

---

## 🔟 Agent Not Receiving Group Config

### 🔎 Symptoms

* Suricata group created
* Agent not ingesting logs

### ⚠️ Causes

* Incorrect agent ID
* Wrong agent.conf location
* Manager not restarted

### ✅ Fix

Verify group membership:

```bash
sudo /var/ossec/bin/agent_groups -l
```

Ensure config file path:

```bash
/var/ossec/etc/shared/Suricata/agent.conf
```

Restart both manager and agent.

---

# 🔹 SECTION 7 — Dashboard Issues

---

## 1️⃣1️⃣ Dashboard Panels Showing No Data

### 🔎 Symptoms

* Visualization empty
* Index pattern not matching

### ✅ Fix

Check data view:

```
wazuh-alerts-*
```

Ensure filter:

```
rule.groups: suricata
```

Verify alerts exist in Discover first.

---

# 🔹 SECTION 8 — Real SOC Troubleshooting Mindset

---

In production SOC environments:

* Always validate each layer separately
* Check log generation first
* Then forwarding
* Then decoding
* Then rule matching
* Then indexing
* Then dashboard rendering

Never assume the issue is at the top layer.

Work bottom-up.

---

# 🏁 Final Takeaway

Troubleshooting this project demonstrates:

* Real debugging capability
* Detection validation skills
* Rule engineering awareness
* Alert lifecycle understanding
* SOC operational thinking

This reflects hands-on production readiness.

---
