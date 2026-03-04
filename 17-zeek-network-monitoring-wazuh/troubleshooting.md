# 🛠️ Troubleshooting Guide — Zeek Network Security Monitoring + Wazuh SIEM Integration

> This troubleshooting guide covers common issues encountered while installing Zeek, enabling JSON logs, deploying Zeek, ingesting logs into Wazuh, and validating detections + dashboards.


> ✅ Best practice order:
> 1) Zeek installs and runs  
> 2) Zeek logs are generated in `/opt/zeek/logs/current/`  
> 3) Logs are JSON formatted  
> 4) Wazuh agent reads the correct log path  
> 5) Wazuh manager decoders/rules load correctly  
> 6) Dashboard shows events with expected fields  

---

## 1) ❌ `zeek: command not found`

### ✅ Symptoms
- Running `zeek --version` returns `command not found`

### 🔍 Possible Causes
- Zeek binaries not added to PATH
- Zeek installed but shell not refreshed

### ✅ Fix
Add Zeek to PATH and reload shell:

```bash
echo "export PATH=\$PATH:/opt/zeek/bin" >> ~/.bashrc
source ~/.bashrc
````

### ✅ Validation

```bash
zeek --version
which zeek
```

---

## 2) ❌ Repository errors when installing Zeek

### ✅ Symptoms

* `apt update` fails for Zeek repo
* GPG signature issues / repo unreachable

### 🔍 Possible Causes

* Wrong Ubuntu version repo URL
* GPG key not installed correctly
* Network/DNS issues on EC2

### ✅ Fix

1. Confirm OS version:

```bash
lsb_release -a
```

2. Re-add repo + key (adjust version path if needed):

```bash
sudo rm -f /etc/apt/sources.list.d/security:zeek.list
echo 'deb http://download.opensuse.org/repositories/security:/zeek/Ubuntu_24.04/ /' | sudo tee /etc/apt/sources.list.d/security:zeek.list
curl -fsSL https://download.opensuse.org/repositories/security:zeek/Ubuntu_24.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null
sudo apt update -y
```

### ✅ Validation

```bash
apt-cache policy zeek
```

---

## 3) ⚠️ Postfix prompt appears during install and you’re unsure what to do

### ✅ Symptoms

* Installer prompts for Postfix configuration

### 🔍 Why it happens

* Postfix may be installed as a dependency; it does not change Zeek’s monitoring directly.

### ✅ Fix

Select:

* **Internet Site**
* Provide system mail name (hostname/FQDN)

### ✅ Validation

* Zeek should install normally and be usable after install.

---

## 4) ❌ `zeekctl check` fails

### ✅ Symptoms

* `sudo zeekctl check` returns script/config errors

### 🔍 Possible Causes

* Wrong interface name in `node.cfg`
* Syntax error in `local.zeek`
* Invalid network ranges in `networks.cfg`

### ✅ Fix

1. Confirm interface:

```bash
ip a
```

2. Fix `node.cfg`:

```bash
sudo nano /opt/zeek/etc/node.cfg
```

Ensure interface matches real NIC name.

3. Validate `local.zeek` contains correct load statement:

```bash
sudo nano /opt/zeek/share/zeek/site/local.zeek
```

Must include:

```zeek
@load policy/tuning/json-logs.zeek
```

4. Validate `networks.cfg` syntax:

```bash
sudo nano /opt/zeek/etc/networks.cfg
```

### ✅ Validation

```bash
sudo zeekctl check
```

---

## 5) ❌ `zeekctl deploy` runs, but no logs appear

### ✅ Symptoms

* Deploy succeeds, but `/opt/zeek/logs/current/` is empty or missing logs

### 🔍 Possible Causes

* Zeek not actually capturing traffic (wrong interface)
* No traffic on monitored interface
* Zeek service not running

### ✅ Fix

1. Confirm interface in node.cfg:

```bash
sudo cat /opt/zeek/etc/node.cfg
```

2. Confirm Zeek is running:

```bash
sudo zeekctl status
```

3. Generate traffic intentionally:

```bash
dig wazuh.com
curl http://example.com
```

4. Check logs again:

```bash
ls -lah /opt/zeek/logs/current/
```

### ✅ Validation

You should see files like:

* `conn.log`
* `dns.log`
* `ssl.log` (after TLS traffic)

---

## 6) ⚠️ Logs are generated but not in JSON format

### ✅ Symptoms

* `dns.log` / `conn.log` entries look like tab-separated fields, not JSON objects

### 🔍 Possible Causes

* JSON logs not enabled in `local.zeek`

### ✅ Fix

Enable JSON logging:

```bash
sudo nano /opt/zeek/share/zeek/site/local.zeek
```

Add:

```zeek
@load policy/tuning/json-logs.zeek
```

Then redeploy:

```bash
sudo zeekctl deploy
```

### ✅ Validation

```bash
head -n 3 /opt/zeek/logs/current/dns.log
```

You should see JSON-like lines.

---

## 7) ❌ Wazuh dashboard shows no Zeek alerts/events

### ✅ Symptoms

* Zeek logs exist locally
* But Wazuh Dashboard has no Zeek-related events

### 🔍 Possible Causes

* Wazuh agent not monitoring Zeek logs
* Wrong path in `<location>`
* Wazuh agent not restarted after change
* Permissions issues reading `/opt/zeek/logs/current/`

### ✅ Fix

1. Add localfile entry:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Use:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/opt/zeek/logs/current/*.log</location>
</localfile>
```

2. Restart agent:

```bash
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent
```

3. Check agent log:

```bash
sudo tail -n 120 /var/ossec/logs/ossec.log
```

4. Fix permissions if needed:

```bash
sudo chmod -R 755 /opt/zeek/logs
sudo chmod -R 755 /opt/zeek/logs/current
```

### ✅ Validation

Trigger traffic and search in dashboard for the agent.

---

## 8) ⚠️ Events appear in Wazuh but fields like `dnsquery`/`ssl_validation_status` are missing

### ✅ Symptoms

* Zeek logs ingested
* But custom fields are not extracted properly

### 🔍 Possible Causes

* Decoders not loaded or decoder regex doesn’t match JSON format
* JSON keys differ from expected (Zeek version differences)

### ✅ Fix

1. Confirm decoders file exists on manager:

```bash
sudo ls -lah /var/ossec/etc/decoders/zeek_decoders.xml
```

2. Restart manager:

```bash
sudo systemctl restart wazuh-manager
```

3. Compare actual log structure:

```bash
head -n 5 /opt/zeek/logs/current/dns.log
head -n 5 /opt/zeek/logs/current/ssl.log
```

4. Adjust decoder regex if JSON keys differ.

### ✅ Validation

* Check Wazuh event details and confirm extracted fields.

---

## 9) ❌ Wazuh manager fails after adding Zeek decoders/rules

### ✅ Symptoms

* `wazuh-manager` fails to restart
* Errors appear in `/var/ossec/logs/ossec.log`

### 🔍 Possible Causes

* XML formatting errors in decoder/rules file
* Duplicate rule IDs
* Invalid rule syntax

### ✅ Fix

1. Check manager log:

```bash
sudo tail -n 200 /var/ossec/logs/ossec.log
```

2. Temporarily disable the new files:

```bash
sudo mv /var/ossec/etc/decoders/zeek_decoders.xml /var/ossec/etc/decoders/zeek_decoders.xml.bak
sudo mv /var/ossec/etc/rules/zeek_rules.xml /var/ossec/etc/rules/zeek_rules.xml.bak
sudo systemctl restart wazuh-manager
```

3. Fix XML syntax, then re-enable.

### ✅ Validation

```bash
sudo systemctl status wazuh-manager
```

---

## 10) 🧨 Port scan test doesn’t trigger scan rule (100904)

### ✅ Symptoms

* You see rejected connections (100903)
* But scan escalation rule (100904) doesn’t trigger

### 🔍 Possible Causes

* Not enough rejected connections in timeframe
* Wrong target/ports not generating REJ state
* Traffic not hitting Zeek sensor interface

### ✅ Fix

1. Ensure you trigger 5+ rejected connections within 20 seconds:

```bash
for port in {5555..5565}; do nc -zv <TARGET_IP> $port || true; done
```

2. Confirm Zeek sees REJ in conn.log:

```bash
tail -n 50 /opt/zeek/logs/current/conn.log
```

### ✅ Validation

* In Wazuh dashboard, search:

  * `rule.id: 100904`

---

## 11) 🔐 TLS anomaly alerts don’t trigger (100906/100907)

### ✅ Symptoms

* You browse HTTPS sites, but no TLS anomaly alerts

### 🔍 Possible Causes

* You didn’t generate the specific anomaly conditions
* SSL logs not being generated (traffic not captured)
* Key names differ in Zeek log output

### ✅ Fix

1. Generate known anomalies:

```bash
curl -k https://self-signed.badssl.com/
curl -k https://expired.badssl.com/
```

2. Confirm ssl.log updates:

```bash
tail -n 30 /opt/zeek/logs/current/ssl.log
```

3. Check the exact string used in `ssl_validation_status` and align the rule accordingly.

### ✅ Validation

* Wazuh dashboard search:

  * `rule.id: 100906 OR rule.id: 100907`

---

## 12) 📊 Dashboards are empty even though events exist

### ✅ Symptoms

* Events appear in Discover
* Dashboard visuals show “No results”

### 🔍 Possible Causes

* Wrong index pattern used
* Missing global filter `rule.groups: zeek`
* Time range set incorrectly (too narrow)

### ✅ Fix

1. Confirm index pattern:

* Use `wazuh-alerts-*`

2. Confirm time range:

* Expand to “Last 24 hours” while testing

3. Confirm filters:

* Add global filter:

  * `rule.groups : zeek`

### ✅ Validation

* Refresh dashboard panels and confirm data appears.

---

## ✅ Quick Recovery Checklist (When Things Break)

# Zeek sensor health
```
zeek --version
sudo zeekctl status
sudo zeekctl check
```

# Zeek logs
```
ls -lah /opt/zeek/logs/current/
tail -n 20 /opt/zeek/logs/current/dns.log
tail -n 20 /opt/zeek/logs/current/conn.log
tail -n 20 /opt/zeek/logs/current/ssl.log
```

# Wazuh agent
```
sudo systemctl status wazuh-agent
sudo tail -n 100 /var/ossec/logs/ossec.log
```

# Wazuh manager
```
sudo systemctl status wazuh-manager
sudo tail -n 100 /var/ossec/logs/ossec.log
```

Then validate in Wazuh Dashboard by filtering:

* `rule.groups : zeek`

---

```
```
