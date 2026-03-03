# 🎯 Wazuh + VirusTotal Integration – Interview Q&A


# SECTION 1 – PROJECT OVERVIEW QUESTIONS

Q1: What was the goal of your Wazuh + VirusTotal project?

A:
The goal was to enhance Wazuh's File Integrity Monitoring by adding threat intelligence enrichment using VirusTotal and then automate malware containment using Wazuh Active Response. Instead of just detecting file changes, we built a system that confirms malicious intent and removes malware automatically.

---

Q2: Why did you integrate VirusTotal with Wazuh?

A:
FIM detects file changes but cannot determine whether a file is malicious. VirusTotal provides multi-engine reputation analysis using 70+ antivirus engines. By integrating it, we converted raw file change alerts into enriched, intelligence-driven malware alerts.

---

Q3: What problem does this solve in a SOC environment?

A:
It reduces manual investigation time, eliminates unnecessary tab-hopping for hash lookups, controls false positives, and enables automated containment. It significantly reduces Mean Time To Respond (MTTR).

---

# SECTION 2 – TECHNICAL IMPLEMENTATION QUESTIONS

Q4: How does Wazuh trigger VirusTotal integration?

A:
Through the `<integration>` block in ossec.conf. We specify rule IDs (100027, 100028) so only executable-related events trigger API lookups. This ensures controlled API usage and prevents rate-limit exhaustion.

---

Q5: Why did you filter only executable files?

A:
Because scanning every file change would exceed the VirusTotal public API limit (4 requests/minute). Executables are higher-risk files, so this reduces noise and preserves API quota.

---

Q6: How did you suppress clean VirusTotal results?

A:
Using a level 0 rule (ID 100029) that checks if `data.virustotal.positives` equals 0. We added `<options>no_log</options>` to suppress logging of clean files.

---

Q7: How did you decide on the malicious threshold?

A:
We escalated only when detections were ≥ 5 AV engines. Single-engine detections may be false positives. A higher threshold increases confidence and reduces accidental remediation.

---

Q8: What MITRE ATT&CK technique did you map?

A:
T1059 – Command and Scripting Interpreter. Because malicious executables and scripts typically align with execution-based tactics.

---

# SECTION 3 – ACTIVE RESPONSE QUESTIONS

Q9: How does Active Response get triggered?

A:
When rule 87105 fires (VirusTotal confirmed malicious file), the active-response block executes `remove-threat.sh` locally on the affected agent.

---

Q10: Why did you bind Active Response only to rule 87105?

A:
To avoid accidental deletion. We only want automatic removal for confirmed malicious detections, not just suspicious or low-confidence alerts.

---

Q11: How does the removal script know which file to delete?

A:
It parses the JSON alert input and extracts:
`parameters.alert.data.virustotal.source.file`

This contains the full file path.

---

Q12: How did you ensure script security?

A:
We set:
chmod 750
chown root:wazuh

This prevents unauthorized modification while allowing execution by Wazuh.

---

Q13: How do you verify Active Response executed successfully?

A:
1. Check `/var/ossec/logs/active-responses.log`
2. Check Wazuh dashboard (rule.id 100092)
3. Confirm file no longer exists
4. Verify alert in TheHive

---

# SECTION 4 – ARCHITECTURE & FLOW QUESTIONS

Q14: Explain the full detection-to-removal pipeline.

A:
1. File created
2. FIM detects change
3. Custom rule filters executable
4. VirusTotal API lookup triggered
5. Enriched alert returned
6. If ≥ threshold → rule 87105 fires
7. Active Response executes script
8. File deleted
9. Removal logged
10. Alert visible in Dashboard + TheHive

---

Q15: What would happen if VirusTotal API limit is exceeded?

A:
Lookups would fail temporarily. Alerts would still be generated but without enrichment. In production, upgrading to a premium API or adding caching logic would be recommended.

---

Q16: How would you scale this for enterprise use?

A:
- Upgrade to VirusTotal Premium
- Add YARA scanning
- Add sandbox integration
- Expand monitored directories
- Add network isolation instead of file deletion
- Integrate with SOAR platform

---

# SECTION 5 – TROUBLESHOOTING QUESTIONS

Q17: VirusTotal lookup not working. What do you check?

A:
- API key validity
- Integration block in ossec.conf
- Rule IDs matching
- Manager restart
- ossec.log for integration errors

---

Q18: Active Response not executing. What do you check?

A:
- Script path
- Script permissions
- rules_id match (87105)
- active-response block in ossec.conf
- active-responses.log
- Manager logs

---

## SECTION 6 – REAL-WORLD SCENARIOS

Q19: What if malware modifies itself repeatedly?

A:
FIM would continuously detect changes. Suppression logic or rule throttling may be needed. For advanced scenarios, we would implement quarantine instead of deletion.

---

Q20: What if VirusTotal returns mixed results (3 positives)?

A:
The rule threshold would not escalate to automatic removal. It would remain a monitored alert requiring analyst review.

---

Q21: What is the biggest risk of Active Response?

A:
False positives leading to deletion of legitimate files. That is why threshold logic and rule filtering are critical.

--- 

## SECTION 7 – HR / IMPACT QUESTIONS

Q22: What did you learn from this project?

A:
- Detection engineering
- Threat intelligence integration
- SOC automation
- API rate-limit management
- Rule logic tuning
- Active response scripting
- Incident lifecycle flow

---

Q23: How does this project align with modern SOC practices?

A:
It aligns with XDR and SOAR methodologies where detection and response are tightly integrated. It demonstrates automated containment, intelligence-driven alerts, and IR tool visibility.

---

Q24: What differentiates this from a basic Wazuh setup?

A:
A basic setup detects file changes. This project:
- Adds enrichment
- Suppresses noise
- Maps to MITRE
- Automates removal
- Integrates with TheHive
- Creates a closed-loop SOC workflow

--- 

## SECTION 8 – ADVANCED QUESTIONS

Q25: How would you prevent attackers from bypassing this?

A:
- Monitor more directories
- Use hash + behavioral detection
- Add YARA rules
- Monitor process execution events
- Add EDR-level telemetry

---

Q26: Could this cause performance impact?

A:
Minimal. FIM is lightweight. API calls limited. Script execution brief. Proper filtering prevents overload.

---

Q27: What compliance benefits does this provide?

A:
- Audit logs
- Traceable remediation
- MITRE mapping
- Incident documentation
- Automated containment evidence

# FINAL SUMMARY

This project demonstrates:

- ✔ Detection engineering
- ✔ Threat intelligence enrichment
- ✔ Automated response execution
- ✔ SOC workflow integration
- ✔ Incident response lifecycle design
- ✔ Production-style security automation

It transitions from reactive detection to proactive containment.

---

END OF INTERVIEW Q&A
