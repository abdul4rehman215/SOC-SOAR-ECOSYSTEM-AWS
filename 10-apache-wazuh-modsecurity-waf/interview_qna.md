# 🧠  Interview Q&A - Wazuh + ModSecurity (WAF) Integration

---

## 📌 Project Overview

### 1️⃣ What was the objective of this project?

The objective was to build a Web Application Security Monitoring pipeline by deploying Apache, securing it with ModSecurity (WAF) using OWASP Core Rule Set (CRS), and integrating its logs into Wazuh SIEM for centralized detection and SOC visibility.

This project added a **Web Application Firewall monitoring layer** to the SOC ecosystem.

---

### 2️⃣ Why is a WAF important if we already have a SIEM?

A SIEM detects and correlates logs.
A WAF actively blocks malicious traffic in real time.

* **WAF = Prevention**
* **SIEM = Detection + Monitoring + Correlation**

Together, they provide layered defense and full visibility.

---

### 3️⃣ What attacks does ModSecurity detect?

With OWASP CRS, ModSecurity detects:

* SQL Injection (SQLi)
* Cross-Site Scripting (XSS)
* Local/Remote File Inclusion
* Command Injection
* Directory Traversal
* Protocol anomalies
* Brute force attempts
* Malicious bots and scanners

---

## 🔍 ModSecurity Deep Technical Questions

### 4️⃣ What is `SecRuleEngine`?

`SecRuleEngine` controls ModSecurity behavior.

Options:

* `Off` → WAF disabled
* `DetectionOnly` → Logs only (no blocking)
* `On` → Actively blocks malicious traffic

In this project, it was set to:

```
SecRuleEngine On
```

This enabled real-time blocking.

---

### 5️⃣ What is OWASP Core Rule Set (CRS)?

OWASP CRS is a standardized rule set for ModSecurity that protects against OWASP Top 10 vulnerabilities.

It provides:

* Predefined detection rules
* Regular updates
* Community-reviewed protection
* Reduced need for custom rule creation

---

### 6️⃣ Where does ModSecurity log events?

Common log locations:

* `/var/log/apache2/error.log`
* `/var/log/apache2/modsec_audit.log`

The audit log contains:

* Rule ID
* Matched payload
* Severity
* Action taken (blocked/logged)
* Source IP
* Target URL

---

## 📡 Wazuh Integration Questions

### 7️⃣ How does Wazuh collect ModSecurity logs?

Wazuh Agent monitors log files using `<localfile>` configuration.

Flow:

Apache → ModSecurity → Log file → Wazuh Agent → Wazuh Manager → Dashboard Alert

---

### 8️⃣ What configuration was added to the Wazuh agent?

Inside `ossec.conf`, we added:

```xml
<localfile>
  <log_format>apache</log_format>
  <location>/var/log/apache2/error.log</location>
</localfile>

<localfile>
  <log_format>apache</log_format>
  <location>/var/log/apache2/modsec_audit.log</location>
</localfile>
```

This forwards WAF logs to the SIEM.

---

### 9️⃣ What happens after logs reach Wazuh Manager?

Wazuh:

* Parses logs using decoders
* Applies detection rules
* Assigns severity levels
* Maps to MITRE ATT&CK techniques
* Generates structured alerts
* Displays them in the dashboard

---

## 🧠 Detection Engineering Questions

### 🔟 How are web attacks mapped to MITRE ATT&CK?

Examples:

* SQL Injection → T1190 (Exploit Public-Facing Application)
* XSS → T1059 (Command and Scripting Interpreter)
* Brute Force → T1110 (Brute Force)
* Directory Traversal → T1083 (File and Directory Discovery)

This improves SOC reporting and threat alignment.

---

### 1️⃣1️⃣ How do you verify OWASP CRS rules are loaded?

You check Apache error logs for CRS initialization messages:

```bash
sudo tail -f /var/log/apache2/error.log
```

You should see rule loading references during Apache startup.

---

### 1️⃣2️⃣ How do you verify blocking is working?

Perform attack simulation:

```bash
curl "http://server-ip/?id=1' OR '1'='1"
```

If configured correctly, response:

```
403 Forbidden
```

That confirms active blocking.

---

## 🔐 Security & Architecture Questions

### 1️⃣3️⃣ Why not rely only on Apache logs without WAF?

Without WAF:

* Attacks reach the application
* No real-time blocking
* Limited payload inspection

With WAF:

* Payload inspected before execution
* Attacks blocked instantly
* Detailed forensic logging

---

### 1️⃣4️⃣ What are the benefits of integrating WAF logs into SIEM?

* Centralized monitoring
* Cross-correlation with other alerts
* SOC investigation capability
* Trend analysis
* Repeat attacker identification
* Compliance audit logging

---

### 1️⃣5️⃣ How does this improve SOC visibility?

The SOC can now monitor:

* Top attacker IPs
* Most attacked endpoints
* Attack frequency
* Severity trends
* OWASP category breakdown
* Web exploitation attempts in real time

---

## 🚨 Scenario-Based Questions

### 1️⃣6️⃣ What if the WAF blocks legitimate traffic?

Possible reasons:

* False positive rule
* Strict CRS sensitivity level

Solution:

* Adjust rule paranoia level
* Disable specific rule ID
* Tune ModSecurity configuration

---

### 1️⃣7️⃣ What if attacks are not appearing in Wazuh dashboard?

Check:

* Wazuh Agent status
* Log path in ossec.conf
* Correct log_format
* Manager restart
* Decoder/rule matching

---

### 1️⃣8️⃣ What would you improve in production?

* Enable Active Response to block attacker IP automatically
* Add reverse proxy architecture
* Add GeoIP enrichment
* Integrate threat intelligence
* Add custom ModSecurity rules
* Deploy load balancer with WAF

---

## 💼 Real-World & HR Questions

### 1️⃣9️⃣ What skills did this project demonstrate?

* Web server deployment
* WAF engineering
* OWASP rule management
* Detection engineering
* Log forwarding configuration
* SIEM integration
* SOC monitoring design
* Web threat simulation
* Security troubleshooting

---

### 2️⃣0️⃣ How does this align with enterprise security architecture?

Enterprise equivalent:

* F5 / Imperva / Cloudflare → WAF
* Splunk / QRadar / Elastic → SIEM

This project replicates enterprise-grade layered defense using open-source tools.

---

### 2️⃣1️⃣ What is the biggest lesson from this project?

Security must be layered.

Blocking alone is not enough.
Monitoring alone is not enough.

Prevention + Detection + Visibility = Effective SOC architecture.

---

## 🎯 Final Summary for Interviews

This project demonstrates:

* Application-layer security
* Real-time attack blocking
* Centralized SIEM monitoring
* SOC alert engineering
* MITRE ATT&CK alignment
* Production-style WAF + SIEM architecture

It shows practical experience in both **defensive engineering and SOC operations**.

---

