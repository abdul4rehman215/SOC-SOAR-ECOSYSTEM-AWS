# 🎯 NGINX + ModSecurity + Fail2Ban + Wazuh  
## Interview Questions & Detailed Answers

---

# 1️⃣ Explain the Architecture of Your Project

This project implements a multi-layer web application defense architecture combining:

- NGINX (Web Server)
- ModSecurity v3 (Web Application Firewall)
- OWASP Core Rule Set (CRS)
- Fail2Ban (Intrusion Prevention System)
- Wazuh SIEM (Detection & Correlation)
- TheHive (Incident Management)

Attack Flow:

1. Attacker sends malicious HTTP payload.
2. NGINX receives request.
3. ModSecurity inspects traffic using OWASP CRS.
4. Malicious payload blocked (HTTP 403).
5. ModSecurity logs event.
6. Fail2Ban reads audit log.
7. Fail2Ban bans attacker IP via firewall.
8. Wazuh collects both detection and ban logs.
9. SIEM generates correlated alerts.
10. TheHive creates incident case.

This creates automated detection + containment + monitoring.

---

# 2️⃣ Why Is Blocking at WAF Level Not Enough?

WAF blocks malicious payloads, not attacker IPs.

Without Fail2Ban:

- Attacker can retry indefinitely.
- Log volume increases.
- Alert fatigue grows.
- No real containment occurs.

With Fail2Ban:

- Repeated attempts trigger IP ban.
- Attacker is stopped at network layer.
- Resource usage is reduced.
- SOC moves from passive monitoring to active defense.

---

# 3️⃣ What Is ModSecurity and How Does It Work?

ModSecurity is an open-source Web Application Firewall engine.

It:

- Inspects HTTP traffic in real time.
- Applies rule-based detection.
- Uses OWASP CRS for known attack patterns.
- Blocks requests with 403.
- Logs detailed attack metadata.

It works as a dynamic module integrated into NGINX.

---

# 4️⃣ What Is OWASP CRS?

OWASP Core Rule Set is a community-maintained rule collection that detects:

- SQL Injection
- XSS
- RCE
- LFI
- Protocol violations
- Anomaly scoring

It standardizes detection logic across environments.

---

# 5️⃣ What Is Fail2Ban and Why Did You Use It?

Fail2Ban is a log-based intrusion prevention tool.

It:

- Monitors log files.
- Detects repeated malicious patterns.
- Automatically inserts firewall rules.
- Temporarily bans attacker IPs.

In this project, Fail2Ban:

- Reads ModSecurity logs.
- Matches 403 denial patterns.
- Bans attacker IP after threshold.

This converts detection into containment.

---

# 6️⃣ What Is the Difference Between WAF and IPS?

WAF:
- Layer 7 protection.
- Blocks malicious payloads.
- Application-focused.

IPS (Fail2Ban in this case):
- Host-level firewall enforcement.
- Blocks attacker IP.
- Network-level containment.

This project combines both.

---

# 7️⃣ How Does Wazuh Add Value in This Architecture?

Wazuh provides:

- Centralized log ingestion.
- Alert generation.
- Rule correlation.
- MITRE ATT&CK mapping.
- Dashboard visualization.
- Custom rule capability.
- Integration with case management.

It gives SOC visibility into:

- Attack detection
- Ban actions
- IP tracking
- Timeline correlation

---

# 8️⃣ What Problem Does This Architecture Solve?

It solves:

- Repeated attack attempts.
- Alert fatigue.
- Lack of containment.
- Lack of visibility.
- Manual investigation delays.

It creates automated active response.

---

# 9️⃣ How Does Fail2Ban Extract Attacker IP?

Using regex filter:

```

ModSecurity: Access denied with code 403

```

Fail2Ban:

- Parses audit log.
- Extracts <HOST>.
- Applies maxretry threshold.
- Inserts firewall DROP rule.

---

# 🔟 What Is maxretry, findtime, bantime?

maxretry:
Number of failed attempts before ban.

findtime:
Time window in seconds for counting failures.

bantime:
Duration of IP ban.

Example:
5 attempts in 300 seconds → ban for 3600 seconds.

---

# 1️⃣1️⃣ How Would You Reduce False Positives?

- Tune OWASP CRS paranoia level.
- Exclude specific rule IDs.
- Adjust Fail2Ban thresholds.
- Analyze legitimate traffic patterns.
- Whitelist trusted IP ranges.

---

# 1️⃣2️⃣ What Logs Are Collected?

- /var/log/nginx/access.log
- /var/log/nginx/error.log
- /var/log/modsec_audit.log
- /var/log/fail2ban.log

All forwarded to Wazuh agent.

---

# 1️⃣3️⃣ How Does Correlation Work in Wazuh?

Wazuh:

- Uses decoders to parse logs.
- Applies rules to generate alerts.
- Assigns rule IDs and severity.
- Maps events to MITRE ATT&CK.
- Allows custom rule creation.

Correlation shows:

Attack → Ban → Host response

---

# 1️⃣4️⃣ What MITRE ATT&CK Techniques Can Be Mapped?

Examples:

- T1190 – Exploit Public-Facing Application
- T1059 – Command Execution
- T1190 – Web Application Attack
- T1083 – File and Directory Discovery

Mapping helps SOC understand attack intent.

---

# 1️⃣5️⃣ How Is This Different from Wazuh Active Response?

Fail2Ban:
- Log-based.
- Firewall-level enforcement.
- Application-triggered containment.

Wazuh Active Response:
- SIEM-triggered.
- Can execute scripts remotely.
- Broader orchestration capability.

This project uses Fail2Ban for host-level containment.

---

# 1️⃣6️⃣ What Real-World Use Case Does This Represent?

Enterprise web server protection:

- E-commerce site
- Public API server
- Banking portal
- SaaS application

Prevents:

- Bot abuse
- Automated scanning
- Brute force attempts
- Persistent exploitation

---

# 1️⃣7️⃣ How Would You Scale This Architecture?

- Deploy behind load balancer.
- Use centralized log aggregation.
- Add reverse proxy layer.
- Integrate SOAR automation.
- Add IP reputation feeds.
- Implement rate limiting.

---

# 1️⃣8️⃣ What Security Model Does This Represent?

Defense-in-depth:

Layer 7 → WAF  
Layer 4 → Firewall  
Monitoring → SIEM  
Response → Automated Ban  
Investigation → Case Management  

---

# 1️⃣9️⃣ What Skills Does This Project Demonstrate?

- WAF engineering
- IPS configuration
- Regex log parsing
- Firewall rule validation
- SIEM rule creation
- Decoder writing
- SOC workflow understanding
- Detection engineering
- Blue-team automation

---

# 2️⃣0️⃣ How Would You Explain This Project in One Sentence?

"I designed and implemented an automated web attack detection and containment pipeline that integrates WAF-level blocking, host-level IP banning, SIEM correlation, and SOC case management."

---

# 2️⃣1️⃣ What Is the Biggest Security Improvement Here?

Moving from:

Detection-only security

To:

Automated containment security

This is the difference between passive logging and active defense.

---

End of Interview Q&A Document.

---
