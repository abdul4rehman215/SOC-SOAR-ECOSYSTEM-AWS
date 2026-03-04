# 🛠️ Troubleshooting Guide — Snort IDS Exploration + Wazuh SIEM Integration

> This troubleshooting guide covers the most common issues while installing Snort, validating configuration, generating alerts, and ingesting Snort logs into Wazuh SIEM.

> ✅ Best practice order:
> 1) Snort installs and runs  
> 2) Snort rules validate (`snort -T`)  
> 3) Alerts appear locally (console + log file)  
> 4) Wazuh agent reads the Snort log path  
> 5) Alerts appear in Wazuh dashboard  

---

## 1) ❌ Snort says: `ERROR: Can't open /etc/snort/snort.conf`

### ✅ Symptoms
- Running Snort returns:
  - `Can't open /etc/snort/snort.conf`

### 🔍 Possible Causes
- Snort not installed correctly
- Wrong config path used
- File missing due to partial install

### ✅ Fix
1) Confirm Snort install:
```bash
snort -V
dpkg -l | grep snort
````

2. Locate config:

```bash
sudo find /etc -name "snort.conf" 2>/dev/null
```

3. Run Snort using the correct path:

```bash
sudo snort -T -c /etc/snort/snort.conf
```

### ✅ Validation

* `snort -T` should end with “successfully validated”.

---

## 2) ❌ Snort config validation fails (`snort -T` errors)

### ✅ Symptoms

* `sudo snort -T -c /etc/snort/snort.conf` fails
* Errors referencing rules, variables, or syntax

### 🔍 Possible Causes

* Rule syntax error in `local.rules`
* Incorrect `HOME_NET` definition
* Duplicate SID or invalid keyword usage

### ✅ Fix

1. Check the exact error message in output and open the referenced file:

```bash
sudo nano /etc/snort/rules/local.rules
```

2. Common rule fixes:

* Ensure every rule ends with `;)`
* Ensure `sid` is numeric and unique
* Ensure `$HOME_NET` is defined in snort.conf

3. Re-run validation:

```bash
sudo snort -T -c /etc/snort/snort.conf
```

### ✅ Validation

* Must say: `Snort successfully validated the configuration!`

---

## 3) ❌ Snort error: `No such device` or “interface not found”

### ✅ Symptoms

* Snort fails to start with:

  * `No such device`

### 🔍 Possible Causes

* Wrong interface name used with `-i`

### ✅ Fix

1. Identify correct interface:

```bash
ip a
```

2. Start Snort with correct interface:

```bash
sudo snort -q -A console -c /etc/snort/snort.conf -i <correct-interface>
```

### ✅ Validation

* Snort runs and stays active (no immediate exit).

---

## 4) ⚠️ You generate traffic but no alerts appear in console

### ✅ Symptoms

* Snort runs
* Traffic occurs (ping/ftp)
* No alert output on screen

### 🔍 Possible Causes

* Rule doesn’t match traffic
* Wrong direction in rule (`->`)
* `$HOME_NET` not matching your subnet
* Snort is listening on wrong interface

### ✅ Fix

1. Confirm `HOME_NET` matches EC2 private subnet (example):

```text
10.0.1.0/24
```

2. Confirm Snort is on the correct interface:

```bash
ip a
```

3. Use a simple known-working rule first:

```conf
alert icmp any any -> $HOME_NET any (msg:"CUSTOM ICMP Ping Detected"; sid:1000001; rev:1;)
```

4. Validate and re-run:

```bash
sudo snort -T -c /etc/snort/snort.conf
sudo snort -q -A console -c /etc/snort/snort.conf -i <interface>
```

### ✅ Validation

* Ping test produces an alert message.

---

## 5) 🧾 Snort console shows alerts but the log file is empty

### ✅ Symptoms

* Alerts show in terminal
* But `/var/log/snort/snort.alert.fast` doesn’t update

### 🔍 Possible Causes

* Fast alert output not enabled in `snort.conf`
* Permissions/log directory issues

### ✅ Fix

1. Confirm fast output plugin is enabled:

```bash
sudo nano /etc/snort/snort.conf
```

Ensure this exists and is not commented:

```conf
output alert_fast: snort.alert.fast
```

2. Check log directory:

```bash
ls -lah /var/log/snort/
```

3. Restart Snort and re-test:

```bash
sudo snort -q -A console -c /etc/snort/snort.conf -i <interface>
```

### ✅ Validation

* Alerts appear in:

```bash
tail -f /var/log/snort/snort.alert.fast
```

---

## 6) 🧨 FTP test from Kali fails, so you think rule is not working

### ✅ Symptoms

* `ftp <snort-ip> 21` fails to connect/refused
* You assume Snort won’t detect it

### ✅ Reality Check

Even a refused connection still generates traffic that can trigger a rule.

### ✅ Fix

* Keep Snort running in console mode and attempt FTP again:

```bash
ftp <SNORT_PRIVATE_IP> 21
```

### ✅ Validation

* Snort should show “FTP Authentication Attempt” alert.

---

## 7) 🧩 Wazuh dashboard shows no Snort alerts

### ✅ Symptoms

* Snort alerts exist in `/var/log/snort/snort.alert.fast`
* But Wazuh Dashboard has no Snort events

### 🔍 Possible Causes

* Wazuh agent not configured to read the Snort log
* Wrong log path in `<location>`
* Wazuh agent not restarted after config change

### ✅ Fix

1. Add correct localfile entry:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/snort/snort.alert.fast</location>
</localfile>
```

2. Restart agent:

```bash
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent
```

3. Check agent logs:

```bash
sudo tail -n 100 /var/ossec/logs/ossec.log
```

### ✅ Validation

* Trigger an alert and verify it appears in dashboard.

---

## 8) ⚠️ Wazuh ingests Snort logs but fields are messy/unstructured

### ✅ Symptoms

* Alerts appear as raw strings
* Hard to filter by SID, src/dst ip, ports, etc.

### 🔍 Possible Causes

* No custom decoder for Snort fast alert format

### ✅ Fix (Optional Enhancement)

Use custom decoder:

* `wazuh/decoders/snort_decoders.xml`

And rules:

* `wazuh/rules/snort_rules.xml`

After adding, restart Wazuh components:

```bash
sudo systemctl restart wazuh-agent
sudo systemctl restart wazuh-manager
```

### ✅ Validation

* Wazuh events now contain parsed fields like:

  * `snort.sid`, `snort.msg`, `srcip`, `dstip`, `srcport`, `dstport`

---

## 9) ❌ Wazuh manager fails after adding decoder/rules

### ✅ Symptoms

* `wazuh-manager` won’t restart
* Errors in `/var/ossec/logs/ossec.log`

### 🔍 Possible Causes

* XML syntax error in decoder/rules file
* Duplicate rule IDs

### ✅ Fix

1. Check log:

```bash
sudo tail -n 200 /var/ossec/logs/ossec.log
```

2. Temporarily disable the new files:

```bash
sudo mv /var/ossec/etc/decoders/snort_decoders.xml /var/ossec/etc/decoders/snort_decoders.xml.bak
sudo mv /var/ossec/etc/rules/snort_rules.xml /var/ossec/etc/rules/snort_rules.xml.bak
sudo systemctl restart wazuh-manager
```

3. Fix XML and re-enable.

### ✅ Validation

* Manager must return to `active (running)`.

---

## 10) 🧯 Quick Recovery Checklist (When Things Break)

Run:

```bash
# Snort
snort -V
sudo snort -T -c /etc/snort/snort.conf
tail -n 20 /var/log/snort/snort.alert.fast

# Wazuh agent
sudo systemctl status wazuh-agent
sudo tail -n 50 /var/ossec/logs/ossec.log

# Wazuh manager (if applicable)
sudo systemctl status wazuh-manager
sudo tail -n 50 /var/ossec/logs/ossec.log
```

Then in Wazuh Dashboard, confirm ingestion by searching and filtering around the agent.

---
