# 🎯 Interview Q&A  
## Automated DNS Sinkholing using Wazuh Active Response

---

# 1️⃣ What was the objective of this project?

The objective was to extend a DNS detection and threat enrichment pipeline into an automated containment system.

Previously:
- DNS queries were detected.
- Suspicious domains were enriched using DNS-Stats.
- Malicious domains were validated using AlienVault OTX.
- Alerts were generated for SOC analysts.

This project adds:
- Automated Active Response
- Endpoint-level DNS sinkholing
- Threat-intel-driven enforcement
- Immediate containment without analyst intervention

It transforms detection into automated defense.

---

# 2️⃣ What is DNS sinkholing?

DNS sinkholing is a defensive technique where malicious domains are redirected to a safe IP address, usually 127.0.0.1 (localhost), instead of their real malicious server.

Instead of:
    malicious-domain.com → attacker IP

It becomes:
    malicious-domain.com → 127.0.0.1

This prevents malware from reaching command-and-control infrastructure.

---

# 3️⃣ Why is DNS sinkholing better than IP blocking?

IP blocking is reactive and limited because:
- Attackers can rotate IP addresses.
- Domains often remain constant longer than IPs.
- IP-based blocking may impact shared hosting environments.

DNS sinkholing:
- Blocks at domain level.
- Prevents C2 communication.
- Is endpoint-enforced.
- Is persistent via HOSTS file.
- Does not rely on firewall rules.

It is more resilient and proactive.

---

# 4️⃣ How does the detection pipeline work before containment?

The detection pipeline includes:

1. Sysmon logs DNS Query (Event ID 22).
2. Wazuh detects DNS event.
3. DNS-Stats evaluates:
   - Frequency score
   - First-seen status
   - Domain rarity
4. AlienVault OTX validates malicious IOC.
5. High-severity alert generated.

Only after OTX confirmation does Active Response trigger.

---

# 5️⃣ Why use DNS-Stats before threat intelligence validation?

DNS-Stats helps reduce noise.

It identifies:
- Rare domains
- Newly seen domains
- Low-frequency domains

This prevents:
- Excessive API calls to OTX
- Alert fatigue
- False positives

It acts as behavioral pre-filtering before threat intelligence validation.

---

# 6️⃣ Why use AlienVault OTX?

AlienVault OTX provides:

- Community-driven threat intelligence
- Known malicious domain validation
- Pulse-based IOC feeds
- Global threat visibility

It confirms whether a suspicious domain is actually malicious before triggering containment.

---

# 7️⃣ How does Wazuh Active Response work in this setup?

Wazuh Active Response works as follows:

1. A rule ID (e.g., 100080) is triggered.
2. Wazuh Manager sends response command to agent.
3. Agent executes local command wrapper.
4. CMD wrapper launches PowerShell script.
5. PowerShell script modifies HOSTS file.
6. Domain is sinkholed.

Active Response executes automatically when rule conditions match.

---

# 8️⃣ Why modify the HOSTS file instead of using firewall rules?

HOSTS file modification:

- Is endpoint-level.
- Does not depend on network firewall.
- Persists across reboots.
- Is simple and reliable.
- Works even if firewall policy changes.

It ensures direct resolution override before DNS lookup.

---

# 9️⃣ What security layers does this project implement?

Layer 1: Endpoint telemetry (Sysmon)  
Layer 2: SIEM detection (Wazuh rules)  
Layer 3: Behavioral enrichment (DNS-Stats)  
Layer 4: Threat intelligence validation (OTX)  
Layer 5: Automated containment (Active Response)  
Layer 6: Persistent enforcement (HOSTS modification)  

This is defense-in-depth architecture.

---

# 🔟 What MITRE ATT&CK techniques does this help detect?

This project helps detect:

- T1071 – Application Layer Protocol (C2 over DNS)
- T1568 – Dynamic Resolution
- T1036 – Masquerading (malicious domains)
- T1071.004 – DNS

It supports detection of early-stage C2 communication.

---

# 1️⃣1️⃣ What risks exist with automated containment?

Potential risks include:

- False positives blocking legitimate domains
- API rate limiting issues
- HOSTS file clutter
- Script execution failures
- Privilege escalation concerns

Mitigation:
- Proper rule tuning
- Validation thresholds
- Logging execution events
- Monitoring Active Response logs

---

# 1️⃣2️⃣ How would you improve this architecture further?

Possible enhancements:

- Centralized sinkhole DNS server instead of HOSTS file
- TTL-based automatic removal
- Automatic un-sinkholing after expiration
- Integration with firewall for layered blocking
- SOAR playbook orchestration
- Caching OTX results to reduce API calls
- Domain age validation via WHOIS/RDAP

---

# 1️⃣3️⃣ How does this reduce MTTR?

Without automation:
- Analyst receives alert
- Investigates
- Confirms malicious
- Takes manual action
- Delay occurs

With automation:
- Detection
- Validation
- Enforcement

All within seconds.

This dramatically reduces Mean Time To Respond.

---

# 1️⃣4️⃣ How would this scale in enterprise?

In enterprise:

- Replace HOSTS modification with enterprise DNS sinkhole server
- Integrate with firewall or EDR
- Use paid threat intel API tier
- Add monitoring for response failures
- Deploy via centralized configuration management

---

# 1️⃣5️⃣ What detection engineering principles were applied?

- Multi-stage correlation
- Telemetry normalization
- Behavioral anomaly detection
- IOC validation
- Automated remediation
- Persistent containment
- Defense-in-depth
- Threat-intel-driven response

---

# 1️⃣6️⃣ What makes this project advanced?

This is advanced because:

- It combines behavioral detection and threat intelligence.
- It includes custom integration scripts.
- It implements automated remediation.
- It demonstrates full detection → validation → enforcement lifecycle.
- It mirrors real-world SOC automation.

It is not just monitoring — it is automated defense engineering.

---

# 1️⃣7️⃣ What would you say in an interview summary?

"This project demonstrates how to transform DNS monitoring into an automated containment system by integrating Wazuh Active Response, DNS-Stats behavioral analysis, and AlienVault OTX threat intelligence. It reduces MTTR, blocks malicious domains at endpoint level, and mirrors enterprise-grade SOC automation workflows."

---

# END OF INTERVIEW Q&A
