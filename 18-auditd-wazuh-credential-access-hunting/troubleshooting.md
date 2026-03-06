# 🛠️ Troubleshooting Guide — Auditd + Wazuh (Credential Access Hunting)

# This guide covers common issues when deploying **auditd kernel auditing** and integrating it with **Wazuh SIEM** for alerting and threat hunting.

---

## 1) 🧩 Auditd service not running

### ❌ Symptoms
- `systemctl status auditd` shows **failed**
- `/var/log/audit/audit.log` not updating

### 🔍 Diagnostics
```bash
sudo systemctl status auditd --no-pager
sudo journalctl -u auditd -xe --no-pager | tail -n 80
sudo auditctl -s
````

### ✅ Fix

```bash
sudo systemctl enable --now auditd
sudo systemctl restart auditd
sudo systemctl status auditd --no-pager
```

---

## 2) 📭 `auditctl -l` shows “No rules”

### ❌ Symptoms

* `sudo auditctl -l` prints no rules
* test commands generate no events

### 🔍 Common Causes

* rules file not placed in `/etc/audit/rules.d/`
* rules not loaded using `augenrules`

### 🔍 Diagnostics

```bash
ls -l /etc/audit/rules.d/
sudo auditctl -l
```

### ✅ Fix

```bash
sudo augenrules --load
sudo systemctl restart auditd
sudo auditctl -l
```

---

## 3) 🧾 Audit rules file loads but still no events in `audit.log`

### ❌ Symptoms

* rules are present in `auditctl -l`
* `/var/log/audit/audit.log` stays quiet

### 🔍 Common Causes

* you tested with actions that don’t match your rules
* wrong path in watch rules (file doesn’t exist on that endpoint)
* permissions not allowing you to read files you are testing

### 🔍 Diagnostics

```bash
sudo tail -n 50 /var/log/audit/audit.log
sudo ausearch -k shadow_access | tail -n 20
sudo ausearch -k passwd_access | tail -n 20
```

### ✅ Fix / Confirm

Generate guaranteed events:

```bash
sudo cat /etc/shadow | head
cat /etc/passwd | head
```

---

## 4) 🧨 auditd reload fails due to syntax errors in rules

### ❌ Symptoms

* `augenrules --load` returns errors
* auditd fails to restart

### 🔍 Diagnostics

```bash
sudo augenrules --check
sudo journalctl -u auditd -xe --no-pager | tail -n 120
```

### ✅ Fix

* Open the rules file and correct formatting:

```bash
sudo nano /etc/audit/rules.d/wazuh.rules
```

Then reload:

```bash
sudo augenrules --load
sudo systemctl restart auditd
```

---

## 5) 📦 Wazuh agent is running but auditd alerts do not appear in Wazuh

### ❌ Symptoms

* auditd logs show events locally
* Wazuh dashboard shows no audit-related alerts

### 🔍 Common Causes

* missing `<localfile>` block in the agent’s `ossec.conf`
* wrong `log_format`
* wrong audit log path
* agent not restarted after config update

### 🔍 Diagnostics (Endpoint)

```bash
sudo grep -n "audit.log" -n /var/ossec/etc/ossec.conf
sudo systemctl status wazuh-agent --no-pager
sudo tail -n 120 /var/ossec/logs/ossec.log
```

### ✅ Fix (Endpoint)

Ensure this exists inside `<ossec_config>`:

```xml
<localfile>
  <log_format>audit</log_format>
  <location>/var/log/audit/audit.log</location>
</localfile>
```

Restart:

```bash
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent --no-pager
```

---

## 6) 🧱 Wazuh manager receives logs but custom rules don’t fire

### ❌ Symptoms

* audit events are visible in raw archives
* but your custom rule IDs never trigger

### 🔍 Common Causes

* rules not placed correctly (wrong file / wrong XML structure)
* rules not matching actual fields
* relying on `if_sid` that differs by version
* lists not compiled into `.cdb`

### 🔍 Diagnostics (Manager)

Check archives:

```bash
sudo tail -n 200 /var/ossec/logs/archives/archives.log
```

Check alerts:

```bash
sudo tail -n 200 /var/ossec/logs/alerts/alerts.log
```

Confirm your rules file exists and is valid XML:

```bash
sudo xmllint --noout /var/ossec/etc/rules/local_rules.xml
```

### ✅ Fix

1. Prefer stable grouping:

```xml
<if_group>audit</if_group>
```

instead of relying on `if_sid` values that may differ.

2. Restart manager after editing rules:

```bash
sudo systemctl restart wazuh-manager
```

---

## 7) 📚 CDB lists not working (rules using `<list>` never match)

### ❌ Symptoms

* rules referencing CDB lists never trigger
* `.cdb` files missing in `/var/ossec/etc/lists/`

### 🔍 Common Causes

* lists not registered in `ossec.conf`
* `wazuh-makelists` not executed
* file format mistakes (bad separators)

### 🔍 Diagnostics (Manager)

```bash
ls -l /var/ossec/etc/lists/
cat /var/ossec/etc/lists/audit-keys
cat /var/ossec/etc/lists/suspicious-programs
```

Check compiled DB:

```bash
ls -l /var/ossec/etc/lists/*.cdb
```

### ✅ Fix

Register lists inside `<ruleset>` in `/var/ossec/etc/ossec.conf`:

```xml
<list>etc/lists/audit-keys</list>
<list>etc/lists/suspicious-programs</list>
```

Compile:

```bash
sudo /var/ossec/bin/wazuh-makelists
sudo systemctl restart wazuh-manager
```

---

## 8) 🧯 “Command not found” for `wazuh-makelists` or older docs mention `ossec-makelists`

### ❌ Symptoms

* `ossec-makelists: command not found`

### ✅ Fix

Use modern Wazuh command:

```bash
sudo /var/ossec/bin/wazuh-makelists
```

---

## 9) 🔎 You see audit events in Wazuh but fields look different than expected

### ❌ Symptoms

* field names do not match your rule conditions
* example: you used `audit.command` but your event shows `data.audit.command`

### ✅ Fix (Analyst workflow)

Use **Discover** to inspect the real event fields:

* Go to **Discover**
* open one audit event
* note the exact field path (commonly under `data.audit.*`)

Then tune rules to match actual fields used by your Wazuh version.

---

## 10) 🐢 Performance issues after enabling audit rules

### ❌ Symptoms

* high CPU usage
* large growth of `/var/log/audit/audit.log`

### 🔍 Causes

* overly broad rules (watching too many paths)
* excessive syscall auditing without filters

### ✅ Fix

* reduce watch scope to only high-value files
* add filters to execve rules (e.g., limit to specific users / exclude system accounts)
* enable log rotation defaults (usually already configured)

Quick size check:

```bash
sudo du -sh /var/log/audit/
```

---

# ✅ Quick Verification Checklist

## Endpoint

```bash
sudo systemctl status auditd --no-pager
sudo auditctl -l
sudo tail -n 30 /var/log/audit/audit.log
sudo ausearch -k shadow_access | tail -n 10
sudo systemctl status wazuh-agent --no-pager
```

## Manager

```bash
sudo systemctl status wazuh-manager --no-pager
sudo ls -l /var/ossec/etc/lists/*.cdb
sudo tail -n 50 /var/ossec/logs/alerts/alerts.log
```

## Dashboard

* Threat Hunting: filter by your rule IDs (e.g., `100120`)
* Discover: validate full event context (AUID/EUID, file, command, key, rule info)

---
```
```
