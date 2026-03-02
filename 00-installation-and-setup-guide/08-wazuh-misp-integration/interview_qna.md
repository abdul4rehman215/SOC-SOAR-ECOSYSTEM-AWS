# 🎯 Interview Q&A – Wazuh ↔ MISP Integration

### Real-Time Threat Intelligence Driven Malware Detection  
### AWS SOC Lab Deployment

---

# 🔹 1. What was the objective of this project?

The objective was to integrate Wazuh with MISP to enable real-time threat intelligence correlation of file hashes.

Instead of generating basic file creation alerts, the system automatically checks file hashes (MD5, SHA1, SHA256) against known malicious indicators stored in MISP.

If a match is found, the alert is enriched and escalated, producing high-confidence detections.


---

# 🔹 2. Why integrate Wazuh with MISP?

Without MISP:
- Wazuh generates file creation alerts.
- No threat intelligence context.
- Higher false positives.
- Manual hash lookup required.

With MISP:
- Hash reputation lookup is automated.
- Alerts are backed by global intelligence feeds.
- SOC confidence increases.
- False positives reduce significantly.

This transforms detection from reactive to intelligence-driven.


---

# 🔹 3. What triggers the MISP integration in Wazuh?

The integration is triggered by:

- Syscheck (File Integrity Monitoring)
- Rule ID 554 (File created)

When Rule 554 is triggered, the Wazuh Integrator module executes the custom Python script.


---

# 🔹 4. How does the integration technically work?

Step-by-step flow:

1. File created on monitored endpoint
2. Wazuh Agent extracts hashes
3. Wazuh Manager receives event (Rule 554)
4. Custom script is executed
5. Script queries MISP REST API (/attributes/restSearch)
6. If hash match found → JSON enrichment returned
7. Custom rule 100802 triggers (Level 12)

The script uses:

- HTTPS POST request
- API key authentication
- JSON payload
- REST API search filtering


---

# 🔹 5. What hashes are checked?

The integration extracts:

- MD5
- SHA1
- SHA256

From the syscheck event fields:

- md5_after
- sha1_after
- sha256_after


---

# 🔹 6. What custom rules did you create?

Rules implemented:

- 100800 → Base integration rule
- 100801 → Hash not found
- 100802 → Hash matched (Level 12 escalation)
- 100803 → Invalid API key (403)
- 100804 → Rate limiting (429)
- 100805 → Server error (500)

This separates detection logic from operational failures.


---

# 🔹 7. How did you validate the integration?

Used EICAR malware test file.

Steps:
1. Added EICAR MD5 hash to MISP
2. Downloaded EICAR file on monitored endpoint
3. Wazuh generated Rule 554
4. MISP returned hash match
5. Rule 100802 triggered (Level 12)

This validated:
- API authentication
- Hash correlation
- Rule escalation
- End-to-end detection pipeline


---

# 🔹 8. What security considerations did you implement?

- Dedicated MISP integration user
- Restricted API key usage
- HTTPS communication
- Rule ID filtering (only syscheck)
- Directory restriction to high-risk paths
- Monitoring integrations.log

Avoided:
- Admin-level API keys
- Broad directory monitoring


---

# 🔹 9. What performance challenges can occur?

Potential issues:

- High file churn → many API calls
- MISP rate limiting (429)
- Network latency
- Large attribute database

Mitigation strategies:

- Monitor only high-risk directories
- Limit integration to Rule 554
- Use to_ids=1 filter
- Limit API response to 1 result


---

# 🔹 10. What is the SOC impact of this integration?

Before:
- Noisy file alerts
- Manual hash checking
- Slower investigations

After:
- Intelligence-backed alerts
- Reduced false positives
- Faster triage
- Higher detection confidence
- Enterprise-grade alert pipeline


---

# 🔹 11. How does this integrate with the broader SOC-SOAR ecosystem?

Pipeline:

Wazuh → MISP → TheHive

Detection → Intelligence Correlation → Incident Response

This forms a complete SOC loop:

- Detection Layer (Wazuh)
- Intelligence Layer (MISP)
- Case Management Layer (TheHive)

It mirrors real-world enterprise SOC architectures.


---

# 🔹 12. What makes this implementation production-ready?

- Proper rule separation
- Error handling rules
- API error detection
- Rate limit handling
- Security hardening
- Structured enrichment output
- Clear escalation logic


---

# 🔹 13. If you had to improve it further, what would you add?

Possible enhancements:

- Caching layer to reduce duplicate API calls
- Async execution for high-volume environments
- MISP sightings push-back
- Multi-MISP redundancy
- SOAR auto-response (block hash, isolate host)


---

# 🔹 14. What role does this project demonstrate?

This project demonstrates skills in:

- Detection engineering
- Threat intelligence integration
- Python scripting
- Wazuh rule tuning
- SOC architecture design
- API integration
- Security hardening
- Blue team automation


---

# 🔹 15. In one sentence, how would you explain this project in an interview?

"I engineered a real-time intelligence-driven malware detection pipeline by integrating Wazuh File Integrity Monitoring with MISP, enabling automatic hash reputation checks and high-confidence alert escalation in a SOC environment."
