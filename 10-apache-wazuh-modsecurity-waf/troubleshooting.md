# 🚨 Troubleshooting Guide - Wazuh + ModSecurity (WAF) Integration

---

## 🧪 Quick Validation Checklist

Before deep troubleshooting, validate:

- Apache running
- ModSecurity module enabled
- SecRuleEngine set to `On`
- OWASP CRS installed
- Wazuh Agent running
- Log paths correct in `ossec.conf`
- Wazuh Manager receiving logs
- Alerts visible in dashboard

Check services:

```bash
sudo systemctl status apache2
sudo systemctl status wazuh-agent
````

---

## 1️⃣ Apache Not Running

### 🔎 Symptoms

* Website not accessible
* Connection refused
* curl fails

### ✅ Check

```bash
sudo systemctl status apache2
```

### 🛠 Fix

```bash
sudo systemctl restart apache2
sudo systemctl enable apache2
```

If failing:

```bash
sudo tail -f /var/log/apache2/error.log
```

---

## 2️⃣ ModSecurity Module Not Enabled

### 🔎 Symptoms

* Attacks not blocked
* No ModSecurity logs

### ✅ Verify Module

```bash
sudo apachectl -M | grep security
```

Expected:

```
security2_module (shared)
```

### 🛠 Fix

```bash
sudo a2enmod security2
sudo systemctl restart apache2
```

---

## 3️⃣ SecRuleEngine Still in Detection Mode

### 🔎 Symptoms

* Attacks logged but not blocked
* No 403 response

### ✅ Check Configuration

```bash
sudo nano /etc/modsecurity/modsecurity.conf
```

Ensure:

```text
SecRuleEngine On
```

### 🛠 Restart Apache

```bash
sudo systemctl restart apache2
```

---

## 4️⃣ OWASP CRS Rules Not Loading

### 🔎 Symptoms

* No attack detection
* No CRS rule IDs in logs

### ✅ Verify CRS Directory

```bash
ls /usr/share/modsecurity-crs
```

### ✅ Check Log for Rule Loading

```bash
sudo tail -f /var/log/apache2/error.log
```

Look for CRS initialization entries.

### 🛠 Fix Symlink

```bash
sudo ln -s /usr/share/modsecurity-crs /etc/modsecurity/
sudo systemctl restart apache2
```

---

## 5️⃣ Attack Simulation Not Returning 403

### 🔎 Symptoms

* SQL injection returns 200 OK

### Possible Causes

* SecRuleEngine not On
* CRS not loaded
* Apache not restarted
* Attack not properly formatted

### ✅ Test Again

```bash
curl "http://localhost/?id=1' OR '1'='1"
```

Expected:

```
403 Forbidden
```

---

## 6️⃣ No ModSecurity Logs Generated

### 🔎 Symptoms

* error.log empty
* No audit entries

### ✅ Check Log Location

```bash
ls -lah /var/log/apache2/
```

### ✅ Check Audit Log Config

Open:

```bash
sudo nano /etc/modsecurity/modsecurity.conf
```

Ensure:

```text
SecAuditEngine On
```

---

## 7️⃣ Wazuh Not Receiving ModSecurity Logs

### 🔎 Symptoms

* Attacks visible in Apache logs
* No alerts in Wazuh dashboard

### ✅ Verify Agent Config

Open:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Ensure:

```xml
<localfile>
  <log_format>apache</log_format>
  <location>/var/log/apache2/error.log</location>
</localfile>
```

### 🛠 Restart Agent

```bash
sudo systemctl restart wazuh-agent
```

### ✅ Check Agent Log

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

---

## 8️⃣ Wazuh Dashboard Shows No Alerts

### 🔎 Possible Causes

* Log forwarding failure
* Decoder mismatch
* Manager not restarted

### ✅ Restart Manager

```bash
sudo systemctl restart wazuh-manager
```

### ✅ Check Manager Log

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

---

## 9️⃣ High False Positives

### 🔎 Symptoms

* Legitimate traffic blocked
* Frequent 403 errors

### 🛠 Solutions

* Adjust CRS paranoia level
* Disable specific rule ID
* Tune ModSecurity rules
* Switch to DetectionOnly temporarily for analysis

---

## 🔟 Performance Issues

### 🔎 Symptoms

* High CPU usage
* Apache slow response

### ✅ Monitor Resources

```bash
htop
free -h
```

### 🛠 Mitigation

* Reduce CRS paranoia level
* Limit audit log verbosity
* Optimize Apache configuration

---

## 1️⃣1️⃣ Log Permission Issues

### 🔎 Symptoms

* Wazuh cannot read logs

### 🛠 Fix Permissions

```bash
sudo chown -R root:adm /var/log/apache2
sudo chmod -R 750 /var/log/apache2
```

Ensure Wazuh agent user can access logs.

---

## 1️⃣2️⃣ Apache Fails After ModSecurity Install

### 🔎 Check Apache Config

```bash
sudo apachectl configtest
```

If syntax error appears → correct configuration.

---

## 🔐 Security Best Practices

* Keep OWASP CRS updated
* Avoid exposing modsec audit logs publicly
* Regularly review blocked IPs
* Tune rules before production deployment
* Monitor false positives carefully
* Integrate with firewall for automated blocking

---

## 📊 Final Operational Checklist

- ✔ Apache running
- ✔ ModSecurity enabled
- ✔ CRS loaded
- ✔ 403 blocking confirmed
- ✔ Logs generated
- ✔ Wazuh agent forwarding logs
- ✔ Alerts visible in dashboard
- ✔ MITRE mapping working

---

## 🏁 Final Advice

Most issues come from:

* Not restarting services
* Incorrect log paths
* Missing module enablement
* Rule engine not set to On
* CRS not properly linked

Always validate step by step.

---

End of Troubleshooting Guide.

---
