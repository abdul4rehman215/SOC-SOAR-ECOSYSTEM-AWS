# 🎯 DNS Threat Hunting Project – Interview Questions & Answers  
## Wazuh + DNS-Stats + AlienVault OTX Integration

---

# 1️⃣ Project Overview

### Q1: Can you explain this DNS threat hunting project in simple terms?

This project builds a DNS-based detection and enrichment pipeline inside a SOC.  

Instead of only logging DNS queries, we:

- Detect DNS queries via Sysmon Event ID 22
- Enrich them using DNS-Stats (frequency & reputation)
- Validate suspicious domains against AlienVault OTX
- Generate context-rich alerts in Wazuh
- Optionally trigger active response

It transforms:

Raw DNS Logs → Context → Intelligence → High-Confidence Alert

---

# 2️⃣ Why DNS Monitoring?

### Q2: Why is DNS telemetry important in threat detection?

DNS is one of the earliest indicators of compromise. Before malware:

- Establishes C2
- Downloads payloads
- Exfiltrates data
- Performs phishing callbacks

It must resolve a domain.

Monitoring DNS allows early-stage infection detection.

---

### Q3: What are examples of suspicious DNS behavior?

- First-time-seen domains
- Rare or low-frequency domains
- Newly registered domains
- Random-looking domains (DGA-like)
- Domains known in threat intelligence feeds

---

# 3️⃣ DNS-Stats Deep Dive

### Q4: What is DNS-Stats and why did you use it?

DNS-Stats is a domain analysis engine created by Mark Baggett.

It provides:

- Domain frequency scoring
- First-seen tracking
- RDAP data
- Domain age
- Historical presence

I used it to reduce false positives and detect rare or anomalous DNS behavior.

---

### Q5: What problem does DNS-Stats solve?

Without enrichment:

- All DNS queries look equal.
- Analysts must manually check reputation.
- Alert fatigue increases.

DNS-Stats automates domain rarity and reputation evaluation.

---

# 4️⃣ Wazuh Integration

### Q6: How did you integrate DNS-Stats into Wazuh?

I created a custom integration script:

1. Wazuh detects Sysmon Event ID 22.
2. The integration script extracts the queried domain.
3. It sends the domain to DNS-Stats API.
4. DNS-Stats returns JSON analysis.
5. Wazuh parses and enriches the alert.

---

### Q7: How does Wazuh trigger integrations?

Wazuh uses `<integration>` blocks in `ossec.conf`.

When a rule ID matches, Wazuh:

- Executes the integration script
- Sends alert JSON via STDIN
- Receives enriched JSON via STDOUT

---

# 5️⃣ AlienVault OTX Integration

### Q8: Why did you integrate AlienVault OTX?

DNS-Stats detects suspicious domains based on rarity.

But rarity does not equal malicious.

OTX validates:

- Whether domain appears in threat intelligence pulses
- Whether known malicious infrastructure exists

This increases confidence and alert severity.

---

### Q9: How did the OTX script determine malicious status?

The script checks:

`pulse_info.count`

If > 0:

- Domain exists in threat intelligence feeds
- Alert severity increases
- MITRE ATT&CK mapping applied

---

# 6️⃣ Detection Logic

### Q10: How does the alert chain work?

1. Sysmon logs DNS query.
2. Wazuh detects Event ID 22.
3. DNS-Stats enrichment runs.
4. Rule checks:
   - Suspicious category
   - Low frequency score
5. If suspicious → dnsstat_alert group.
6. OTX integration triggers.
7. If IOC match → High severity alert.

---

### Q11: How did you reduce false positives?

- Frequency-based detection
- First-seen tracking
- External IOC validation
- Selective rule thresholds

Only rare + suspicious + threat intel validated domains escalate.

---

# 7️⃣ MITRE ATT&CK Mapping

### Q12: How does this map to MITRE ATT&CK?

DNS-based detection aligns with:

- T1071 – Application Layer Protocol
- T1036 – Masquerading
- T1568 – Dynamic Resolution
- Command & Control techniques

OTX IOC matches are mapped in Wazuh rules.

---

# 8️⃣ Active Response

### Q13: What is Active Response in this project?

Active Response allows Wazuh to:

- Trigger local scripts
- Execute PowerShell commands
- Automate containment

For example:

- Run OTX lookup on endpoint
- Log enrichment locally
- Trigger containment logic

---

# 9️⃣ Enterprise SOC Value

### Q14: What SOC value does this project provide?

Before:

- Raw DNS logs
- Manual reputation checks
- No context

After:

- Automated enrichment
- Threat intelligence validation
- Reduced analyst pivoting
- Faster triage
- Improved MTTD and MTTR

---

# 🔟 Performance & Scalability

### Q15: What are scalability concerns?

- OTX API rate limits
- DNS-Stats local performance
- Integration execution frequency
- Wazuh rule optimization

In production:

- Use caching
- Set rate thresholds
- Tune alert severity carefully

---

# 1️⃣1️⃣ Security Considerations

### Q16: What security risks exist in this integration?

- API key exposure
- Script permission misconfiguration
- Excessive API calls
- Overly aggressive detection thresholds

Mitigations:

- Secure file permissions
- Restrict execution rights
- Use environment variables for API keys
- Implement threshold tuning

---

# 1️⃣2️⃣ Real-World SOC Scenarios

### Q17: How would this detect real malware?

Example:

Malware resolves:
random-subdomain.evilc2.com

Pipeline:

- Sysmon logs DNS
- DNS-Stats marks low frequency
- OTX shows malicious pulse
- High severity alert triggered
- Analyst sees enriched context immediately

---

# 1️⃣3️⃣ Lessons Learned

### Q18: What did you learn from this project?

- Custom Wazuh integration development
- Detection engineering design
- Threat intelligence correlation
- Rule tuning to reduce noise
- Multi-stage alert pipelines
- SOC workflow optimization

---

# 1️⃣4️⃣ Advanced Questions

### Q19: How would you improve this in production?

- Add domain entropy detection (DGA detection)
- Implement caching layer
- Add passive DNS source enrichment
- Correlate DNS with network traffic logs
- Add automatic blocking via firewall

---

### Q20: How does this differ from simple DNS logging?

Simple DNS logging:

- Stores queries only

This project:

- Detects anomalies
- Enriches automatically
- Validates against global threat intel
- Escalates severity intelligently
- Supports automated response

---

# 1️⃣5️⃣ Final Interview Summary Answer

If asked:

"What makes this project advanced?"

You can answer:

This project demonstrates detection engineering by combining:

- Endpoint telemetry (Sysmon)
- Behavioral anomaly detection (DNS-Stats)
- External threat intelligence (OTX)
- SIEM integration (Wazuh)
- Automated enrichment
- Optional response automation

It transforms raw DNS logs into SOC-ready intelligence.

That mirrors enterprise-grade threat detection architecture.

---
