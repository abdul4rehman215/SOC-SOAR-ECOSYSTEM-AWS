# 🎤 NGINX + ModSecurity v3 + OWASP CRS + Wazuh SIEM  
## Interview Questions & Answers

---

# 1️⃣ What was the objective of this project?

The objective was to implement a Web Application Firewall (WAF) using NGINX and ModSecurity v3, integrate OWASP Core Rule Set (CRS), and forward logs into Wazuh SIEM for centralized detection, alerting, and SOC monitoring.

It was not just installation — it focused on:

- Detection engineering
- Layer 7 attack visibility
- Real-time blocking
- Log-based threat detection
- SOC alert investigation
- MITRE ATT&CK mapping

---

# 2️⃣ Why did you choose NGINX instead of Apache?

NGINX is:

- High-performance and event-driven
- Widely used in cloud-native environments
- Common as reverse proxy and load balancer
- More complex to integrate with ModSecurity (requires dynamic module compilation)

Using NGINX allowed deeper understanding of:

- Dynamic module compilation
- ModSecurity v3 library mode
- Advanced WAF engineering

---

# 3️⃣ What is ModSecurity v3?

ModSecurity v3 is an open-source Web Application Firewall engine that:

- Inspects HTTP traffic
- Uses rule-based detection
- Blocks OWASP Top 10 attacks
- Logs detailed forensic data

In NGINX, ModSecurity runs as a dynamic module.

---

# 4️⃣ What is OWASP CRS?

OWASP Core Rule Set (CRS):

- Community-maintained WAF rule set
- Detects SQL Injection, XSS, LFI, RCE, etc.
- Regularly updated
- Used globally in production WAF deployments

It provides predefined detection rules that ModSecurity executes.

---

# 5️⃣ How does ModSecurity work with NGINX?

Flow:

1. Client sends HTTP request
2. NGINX receives request
3. ModSecurity module intercepts request
4. OWASP CRS rules evaluate payload
5. If malicious → 403 Forbidden
6. Event logged in error.log
7. Wazuh agent collects log
8. Wazuh generates alert

---

# 6️⃣ What types of attacks did you simulate?

I simulated:

- Cross-Site Scripting (XSS)
- Local File Inclusion (LFI)
- Directory Traversal
- SQL Injection patterns
- Malicious query parameters

Using curl-based payload testing.

---

# 7️⃣ How did you verify that blocking was working?

Using curl:

```bash
curl "http://server-ip/?q=<script>alert(1)</script>"
````

Expected result:

HTTP 403 Forbidden

Then verified logs in:

/var/log/nginx/error.log

Confirmed rule ID, severity, and attack category.

---

# 8️⃣ How did you integrate logs into Wazuh?

Edited:

/var/ossec/etc/ossec.conf

Added monitoring for:

* /var/log/nginx/error.log
* /var/log/nginx/access.log

Restarted wazuh-agent.

Wazuh manager decoded ModSecurity logs and generated alerts.

---

# 9️⃣ What information did Wazuh provide in alerts?

Each alert included:

* Rule ID
* Rule level (severity)
* Source IP
* URL
* HTTP method
* Attack category
* MITRE ATT&CK technique
* Full log payload

---

# 🔟 What MITRE ATT&CK mappings did you observe?

Examples:

* T1190 – Exploit Public-Facing Application
* T1059 – Command Injection
* T1083 – File and Directory Discovery
* Initial Access tactics

Wazuh automatically mapped decoded events.

---

# 1️⃣1️⃣ What are the benefits of integrating WAF with SIEM?

Without SIEM:

* Only blocking occurs
* No centralized visibility
* No historical trend analysis

With SIEM:

* Alert classification
* Threat correlation
* MITRE mapping
* SOC dashboards
* Incident investigation
* Attack pattern tracking

Together → Block + Detect + Analyze.

---

# 1️⃣2️⃣ What challenges did you face?

* ModSecurity v3 compilation dependencies
* NGINX version mismatch during module compilation
* Library path configuration (ldconfig)
* CRS configuration file linking
* NGINX syntax validation errors
* Log format tuning for Wazuh parsing

Troubleshooting required careful step-by-step validation.

---

# 1️⃣3️⃣ What skills does this project demonstrate?

* WAF engineering
* NGINX module compilation
* Source-based software build
* Security configuration hardening
* Log engineering
* SIEM integration
* Detection validation
* SOC alert analysis
* MITRE ATT&CK interpretation

---

# 1️⃣4️⃣ How would you improve this setup in production?

* Enable HTTPS with TLS
* Add rate limiting
* Tune CRS paranoia level
* Implement Wazuh Active Response (auto IP blocking)
* Integrate threat intelligence feeds
* Deploy reverse proxy architecture
* Harden NGINX configuration

---

# 1️⃣5️⃣ How is this relevant to real-world SOC roles?

Modern SOCs:

* Monitor web-facing infrastructure
* Investigate web exploitation attempts
* Correlate WAF logs with other security telemetry
* Use MITRE mapping for reporting

This project mirrors enterprise WAF + SIEM architecture.

---

# 1️⃣6️⃣ What makes this project advanced?

* Compiled ModSecurity from source
* Built dynamic NGINX module
* Integrated CRS manually
* Performed log engineering
* Validated detection end-to-end
* Simulated real attack scenarios
* Analyzed alerts at SIEM level

It goes beyond basic installation.

---

# 🎯 Final Summary for Interview

This project demonstrates:

* Enterprise-grade Web Application Security Monitoring
* Advanced WAF engineering
* Real attack blocking
* SOC alert visibility
* SIEM integration
* Detection validation workflow

It reflects practical, production-style security architecture.

---
