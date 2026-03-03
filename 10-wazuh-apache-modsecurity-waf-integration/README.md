# 🛡️ Web Application Security Monitoring Using Apache, ModSecurity (OWASP CRS), and Wazuh SIEM

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/Implementing-ModSecurity-WAF-integration-with-Wazuh.png" width="700">
</p>


## 🚀 Project Overview

Modern web applications are among the most attacked assets in any infrastructure.

Common real-world attacks include:

- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Local File Inclusion (LFI)
- Remote File Inclusion (RFI)
- Directory Traversal
- Brute Force Attempts
- Automated scanners & bots
- Command Injection
- Web shell upload attempts

This project demonstrates how to build a **real-world SOC-ready Web Application Security Monitoring pipeline** by integrating:

- Apache Web Server
- ModSecurity v2 (Web Application Firewall)
- OWASP Core Rule Set (CRS)
- Wazuh Agent
- Wazuh Manager (SIEM)
- Wazuh Dashboard (SOC visibility)

---

# 🎯 Why This Project Matters

This is not just installation.

This project demonstrates:

- Detection Engineering at Web Layer
- WAF deployment and tuning
- SOC log pipeline integration
- SIEM alert engineering
- Web attack simulation & validation
- Real-time blocking + monitoring
- MITRE ATT&CK mapping of web attacks
- Enterprise-grade WAF + SIEM architecture

It adds a **Web Application Firewall monitoring layer** to your SOC ecosystem.

---

# 🌐 What is Apache?

Apache HTTP Server is an open-source web server used to host websites and applications.

In this project:

- Apache receives HTTP traffic
- ModSecurity inspects requests before application processing

Official Apache Website:  
[Visit Apache HTTP Server Official Documentation](https://httpd.apache.org/)

---

# 🔥 What is ModSecurity?

ModSecurity is an open-source Web Application Firewall (WAF) engine.

It:

- Inspects HTTP requests in real time
- Applies rule-based detection
- Blocks malicious payloads
- Logs full forensic attack details
- Works with OWASP Core Rule Set (CRS)

Official Website:  
[Visit ModSecurity Official Site](https://modsecurity.org/)

Apache Installation Guide Reference:  
[Apache ModSecurity Installation Guide](https://www.inmotionhosting.com/support/server/apache/install-modsecurity-apache-module/)

---

# 📚 What is OWASP Core Rule Set (CRS)?

OWASP CRS is a community-maintained set of WAF rules that detect:

- SQL Injection
- XSS
- LFI/RFI
- Command Injection
- Protocol anomalies
- Bot traffic
- Scanners

It protects against OWASP Top 10 vulnerabilities.

---

# 🧠 Why Integrate ModSecurity with Wazuh?

ModSecurity blocks attacks.

Wazuh provides:

- Centralized monitoring
- Alert generation
- SOC dashboard visibility
- Threat correlation
- MITRE ATT&CK mapping
- Investigation workflows

Official Wazuh Blog Reference:  
[Analyzing ModSecurity Events with Wazuh](https://wazuh.com/blog/analyzing-modsecurity-events-with-wazuh/)

Technical Deep Dive Reference:  
[ModSecurity Meets Wazuh – A Secure Combo](https://certbar.com/technical-blogs/mod-security-meets-wazuh-a-secure-combo)

---

# 🏗️ Architecture Overview

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/apache-modsecurity-wazuh-architecture.png" width="800">

Flow:

Attacker  
↓  
Apache Web Server  
↓  
ModSecurity (OWASP CRS)  
↓  
Apache Logs + ModSecurity Audit Logs  
↓  
Wazuh Agent  
↓  
Wazuh Manager  
↓  
Wazuh Dashboard (SOC Visibility)

</p>

---

# 🖥️ Environment Setup

Ubuntu Server  
Apache2  
ModSecurity v2  
OWASP CRS  
Wazuh Agent  
Wazuh Manager (separate)

---

# ⚙️ Step 1 – Install Apache Web Server

Update system:

```bash
sudo apt update
sudo apt upgrade -y
````

Install Apache:

```bash
sudo apt install apache2 -y
```

Enable and start service:

```bash
sudo systemctl enable apache2
sudo systemctl start apache2
```

Verify:

```bash
sudo systemctl status apache2
```

---

# 🌍 Step 2 – Verify Apache in Browser

Open:

```
http://<server-ip>
```

Expected:

Apache Default Page → "It Works!"

This confirms web server is operational.

---

# 🛡️ Step 3 – Install ModSecurity v2

Install module:

```bash
sudo apt install libapache2-mod-security2 -y
```

Verify module:

```bash
sudo apachectl -M | grep security
```

Expected:

```
security2_module (shared)
```

---

# 🔧 Step 4 – Enable Active Blocking Mode

Edit configuration:

```bash
sudo nano /etc/modsecurity/modsecurity.conf
```

Find:

```
SecRuleEngine DetectionOnly
```

Change to:

```
SecRuleEngine On
```

Restart Apache:

```bash
sudo systemctl restart apache2
```

Now WAF is actively blocking.

---

# 📜 Step 5 – Install OWASP Core Rule Set (CRS)

Install:

```bash
sudo apt install modsecurity-crs -y
```

Verify:

```bash
ls /usr/share/modsecurity-crs
```

Enable CRS:

```bash
sudo ln -s /usr/share/modsecurity-crs /etc/modsecurity/
```

Restart Apache:

```bash
sudo systemctl restart apache2
```

---

# 📡 Step 6 – Configure Wazuh Agent to Monitor Logs

Edit:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add Apache error log:

```xml
<localfile>
  <log_format>apache</log_format>
  <location>/var/log/apache2/error.log</location>
</localfile>
```

Add ModSecurity audit log:

```xml
<localfile>
  <log_format>apache</log_format>
  <location>/var/log/apache2/modsec_audit.log</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
```

---

# 🧪 Step 7 – Attack Simulation

### SQL Injection Test

```bash
curl "http://<server-ip>/?id=1' OR '1'='1"
```

### XSS Test

```bash
curl "http://<server-ip>/?q=<script>alert(1)</script>"
```

Expected:

```
403 Forbidden
```

WAF successfully blocking.

---

# 🔍 Step 8 – Raw Log Analysis

Check logs:

```bash
sudo tail -f /var/log/apache2/error.log
```

Observe:

* Rule ID
* Severity
* Attack type
* Matched payload
* CRS rule reference

---

# 📊 Step 9 – Verify Alerts in Wazuh Dashboard

Go to:

Security Events → Filter by agent

Search:

```
modsecurity
```

You will see:

* ModSecurity: Rejected a query
* SQL Injection attempt
* XSS attack attempt
* Source IP
* Rule ID
* MITRE ATT&CK mapping
* Severity level

---

# 🧠 What This Enables in Your SOC

You can now monitor:

* Web exploitation attempts
* Attack frequency
* Top attacker IPs
* Targeted URLs
* Recon scanning patterns
* OWASP categories
* Severity trends
* Repeated attacker behavior

---

# 💼 Real-World Use Cases

* Web server hardening
* PCI-DSS compliance logging
* SOC web threat monitoring
* Incident investigation
* Threat hunting for web attacks
* Forensic payload analysis
* Detect automated scanners

---

# 🚀 Future Enhancements

* Enable Wazuh Active Response to block attacker IP
* Integrate firewall (iptables)
* Add threat intelligence enrichment
* Custom ModSecurity rules
* GeoIP correlation
* Custom Wazuh dashboard visualizations

---

# ✅ Project Outcome

- ✔ Apache secured
- ✔ OWASP CRS active
- ✔ Real attacks simulated
- ✔ 403 blocking confirmed
- ✔ Logs centralized
- ✔ Alerts generated
- ✔ MITRE mapping visible
- ✔ SOC monitoring enabled

---

# 🧠 Skills Demonstrated

* Web Server Deployment
* WAF Engineering
* OWASP Rule Management
* Detection Engineering
* SIEM Integration
* SOC Monitoring
* Web Threat Analysis
* Security Log Engineering

---

# 📁 Repository Structure

```
10-wazuh-apache-modsecurity-waf-integration/
│
├── README.md
├── commands.sh
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
│
├── configs/
│   ├── ossec_modsecurity_log_config.xml
│   └── modsecurity_engine_config.txt
│
└── docs/
    └── Apache - Web Application Firewall (ModSecurity) with Wazuh Monitoring.pdf
```

---

# 📄 PDF Guide

For screenshots and step-by-step visual documentation:

👉 [Click here to view the complete PDF walkthrough guide]([YOUR_PDF_LINK_HERE](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/10-wazuh-apache-modsecurity-waf-integration/docs/Apache%20-%20Web%20Application%20Firewall%20(ModSecurity)%20with%20Wazuh%20Monitoring.pdf))

---

# 🏁 Conclusion

This project replicates enterprise-grade WAF + SIEM integration.

Apache handles traffic.
ModSecurity inspects and blocks malicious requests.
Wazuh centralizes, correlates, and alerts.

This creates a layered Web Application Security Monitoring architecture aligned with real SOC environments.

---
