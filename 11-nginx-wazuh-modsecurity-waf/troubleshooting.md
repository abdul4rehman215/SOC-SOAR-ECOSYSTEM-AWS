# 🚨 Troubleshooting Guide- NGINX + ModSecurity v3 + OWASP CRS + Wazuh  

 This guide covers real-world issues encountered during:

- NGINX module compilation
- ModSecurity v3 build
- OWASP CRS configuration
- Log forwarding
- Wazuh alert generation

---

# 🧪 Quick Validation Checklist

Before deep troubleshooting, validate:

- NGINX running
- ModSecurity module loaded
- SecRuleEngine set to On
- CRS installed and linked
- Wazuh agent running
- Log paths correct
- Alerts visible in dashboard

---

# 1️⃣ NGINX Fails to Start After Module Enable

## 🔎 Symptoms

- `sudo systemctl restart nginx` fails
- NGINX does not start
- “module not found” error

## ✅ Check

```bash
sudo nginx -t
````

## 🛠 Common Cause

Module path incorrect.

Ensure:

```
load_module modules/ngx_http_modsecurity_module.so;
```

Check module exists:

```bash
ls /etc/nginx/modules/
```

If missing → recompile module.

---

# 2️⃣ Version Mismatch During Compilation

## 🔎 Symptoms

* Module compiles but NGINX crashes
* Unknown symbol errors

## 🛠 Root Cause

NGINX source version must match installed version.

Check installed version:

```bash
nginx -v
```

Download exact same version source.

---

# 3️⃣ ModSecurity Library Not Found

## 🔎 Symptoms

* “libmodsecurity.so not found”
* NGINX fails to load module

## 🛠 Fix

```bash
echo "/usr/local/modsecurity/lib" | sudo tee /etc/ld.so.conf.d/modsecurity.conf
sudo ldconfig
```

Verify:

```bash
ldconfig -p | grep modsecurity
```

---

# 4️⃣ SecRuleEngine Still in DetectionOnly

## 🔎 Symptoms

* Attacks logged but not blocked
* No 403 responses

## ✅ Check

```bash
sudo nano /etc/nginx/modsec/modsecurity.conf
```

Ensure:

```
SecRuleEngine On
```

Restart NGINX.

---

# 5️⃣ OWASP CRS Rules Not Triggering

## 🔎 Symptoms

* No detection
* No CRS rule IDs in logs

## 🛠 Check main.conf

Ensure:

```
Include /etc/nginx/modsec/modsecurity.conf
Include /etc/nginx/modsec/coreruleset/crs-setup.conf
Include /etc/nginx/modsec/coreruleset/rules/*.conf
```

Also ensure:

```
crs-setup.conf
```

exists.

---

# 6️⃣ curl Test Not Returning 403

## 🔎 Possible Causes

* SecRuleEngine not enabled
* Server block missing modsecurity directive
* Wrong rule path
* NGINX not restarted

Verify in server block:

```
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/main.conf;
```

---

# 7️⃣ NGINX Syntax Error

## 🔎 Symptoms

“unknown directive modsecurity”

## 🛠 Cause

Module not loaded.

Ensure first line in nginx.conf:

```
load_module modules/ngx_http_modsecurity_module.so;
```

---

# 8️⃣ Wazuh Not Receiving Logs

## 🔎 Symptoms

* 403 blocking confirmed
* No alerts in Wazuh dashboard

## ✅ Check Agent

```bash
sudo systemctl status wazuh-agent
```

## ✅ Verify ossec.conf

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Ensure correct log paths.

Restart agent:

```bash
sudo systemctl restart wazuh-agent
```

---

# 9️⃣ Alerts Visible But Not Decoded Properly

## 🔎 Symptoms

* Generic log alert
* No ModSecurity rule details

## 🛠 Cause

Wrong log_format.

Use:

```
<log_format>syslog</log_format>
```

OR tune format based on environment.

---

# 🔟 High CPU Usage

## 🔎 Symptoms

* Server slow
* High resource usage

## 🛠 Causes

* CRS paranoia level high
* Too many rules enabled
* Large request bodies inspected

## 🔧 Mitigation

* Reduce CRS paranoia level
* Tune rule exclusions
* Limit request body size

---

# 1️⃣1️⃣ Permission Issues Reading Logs

## 🔎 Symptoms

* Wazuh cannot read nginx logs

## 🛠 Fix

```bash
sudo chmod 750 /var/log/nginx
sudo chown root:adm /var/log/nginx/error.log
```

Ensure wazuh user has access.

---

# 1️⃣2️⃣ NGINX Build Errors

Common missing dependencies:

* libpcre3-dev
* libssl-dev
* libxml2-dev
* libyajl-dev

Reinstall dependencies if configure fails.

---

# 1️⃣3️⃣ CRS False Positives

## 🔎 Symptoms

* Legitimate traffic blocked

## 🛠 Solution

* Adjust CRS paranoia level
* Disable specific rule ID
* Use rule exclusion mechanism

Example:

```
SecRuleRemoveById 942100
```

---

# 1️⃣4️⃣ Wazuh Alerts Not Showing MITRE Mapping

## 🔎 Cause

* Manager rules outdated
* Decoder not matching correctly

Restart Wazuh manager:

```bash
sudo systemctl restart wazuh-manager
```

---

# 🔐 Security Hardening Tips

* Enable HTTPS
* Disable unnecessary NGINX modules
* Restrict access to modsec configs
* Use firewall rules
* Enable rate limiting
* Regularly update CRS

---

# 🧠 Final Validation Steps

- ✔ NGINX running
- ✔ Module loaded
- ✔ SecRuleEngine On
- ✔ CRS installed
- ✔ curl test returns 403
- ✔ error.log shows rule ID
- ✔ Wazuh agent forwarding logs
- ✔ Alerts visible in dashboard
- ✔ MITRE mapping working

---

# 🏁 Final Advice

Most issues come from:

* Version mismatch
* Missing dependencies
* Not restarting services
* Wrong log paths
* Incorrect rule include order

Always validate step by step.

---

End of Troubleshooting Guide.

---
