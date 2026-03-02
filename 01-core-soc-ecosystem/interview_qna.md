# 🎯 Interview Q&A – Core SOC Ecosystem (AWS)

### Detection → Intelligence → Investigation  
### Wazuh + MISP + TheHive Integration


---

# 🔹 1. What was the goal of this project?

The goal was to design and deploy a complete open-source SOC architecture on AWS that connects:

- Detection (Wazuh)
- Threat Intelligence (MISP)
- Investigation & Case Management (TheHive)

Instead of running tools independently, I built a structured SOC workflow where alerts are enriched with intelligence and managed through a formal investigation lifecycle.


---

# 🔹 2. Why integrate Wazuh, MISP, and TheHive?

Individually:

- Wazuh detects activity.
- MISP stores threat intelligence.
- TheHive manages incidents.

When integrated:

- Alerts gain intelligence context automatically.
- False positives decrease.
- Investigations become structured.
- SOC operations become auditable.
- Analysts work within a unified workflow.

It transforms raw alerts into actionable investigations.


---

# 🔹 3. What role does each tool play in the SOC ecosystem?

Wazuh:
Detection engine (SIEM/XDR).  
Generates structured alerts from logs and endpoint activity.

MISP:
Threat intelligence repository.  
Provides IOC correlation and enrichment.

TheHive:
Case management platform.  
Tracks investigations, assigns analysts, and maintains documentation.

Together:
Detection → Enrichment → Investigation → Resolution


---

# 🔹 4. Walk me through the data flow.

1. Endpoint generates logs.
2. Wazuh agent forwards logs to Wazuh Manager.
3. Wazuh applies detection rules.
4. Alert generated.
5. Indicator (IP/hash/domain) checked in MISP.
6. If malicious → context attached.
7. Alert forwarded to TheHive.
8. Case created.
9. Analyst investigates and documents findings.

This mirrors enterprise SOC workflow.


---

# 🔹 5. How does this architecture reduce false positives?

Without intelligence:
All alerts look equal.

With MISP:
- Known malicious indicators increase confidence.
- Unknown indicators remain lower priority.
- Context-driven triage reduces noise.

The intelligence layer improves alert quality.


---

# 🔹 6. What AWS components were involved?

- EC2 instances for Wazuh, MISP, TheHive
- Security Groups controlling communication
- HTTPS-based API integrations
- Proper resource allocation for performance stability

This was deployed in a cloud-native environment, not just local lab simulation.


---

# 🔹 7. What challenges did you face?

- API authentication failures
- SSL certificate issues
- Rule tuning to reduce noise
- Integration debugging
- Log format mismatches
- Event forwarding validation

Troubleshooting was a key part of the project.


---

# 🔹 8. How did you validate the system?

I simulated:

- Brute force attacks
- Malicious file drops (hash-based detection)
- Suspicious IP activity

Verified:

- Detection triggered in Wazuh
- IOC matched in MISP
- Case created in TheHive
- Investigation workflow completed


---

# 🔹 9. How does this architecture improve SOC maturity?

Without integration:
- Alerts isolated in dashboards
- Manual IOC lookups
- No structured case tracking

With integration:
- Automated enrichment
- Structured investigations
- Audit trails
- Intelligence feedback loop
- Reduced MTTR

This represents a higher SOC maturity level.


---

# 🔹 10. What security controls were implemented?

- API key authentication
- HTTPS communication
- Restricted directory monitoring
- Rule-based integration filtering
- Role-based access control
- Audit logging in TheHive

Security was considered in integration design.


---

# 🔹 11. How scalable is this architecture?

In enterprise deployment:

- Wazuh agents scale horizontally
- Wazuh managers can be clustered
- MISP can serve as central intelligence hub
- TheHive can operate in distributed teams

The architecture supports multi-team SOC environments.


---

# 🔹 12. What makes this a capstone-level project?

It demonstrates:

- SOC architecture design
- Cross-platform integration
- API-based automation
- Detection engineering
- Threat intelligence usage
- Incident workflow modeling
- AWS security deployment
- Production-style troubleshooting

This is closer to real SOC engineering than simple tool setup.


---

# 🔹 13. How would you explain this project in one sentence?

"I designed and deployed a complete open-source SOC architecture on AWS that integrates detection, threat intelligence, and structured investigation into a unified operational workflow."


---

# 🔹 14. What did you learn from this project?

- Alerts without context create noise.
- Intelligence dramatically improves detection quality.
- Investigation workflow is as important as detection.
- Integration and troubleshooting are core SOC skills.
- Security architecture requires structured thinking.


---

# 🔹 15. If you were to improve it further, what would you add?

- Alert correlation rules for multi-stage attacks
- High-availability deployment
- Additional threat feeds in MISP
- Advanced rule tuning
- Role-based analyst segmentation
- Performance monitoring metrics


---

# 🔹 16. Which roles does this project align with?

- SOC Analyst
- Blue Team Engineer
- Detection Engineer
- Threat Intelligence Analyst
- Security Operations Engineer


---

# 🔹 Final Summary

This project showcases:

Detection (Wazuh)  
+ Intelligence (MISP)  
+ Investigation (TheHive)  

Working together in a structured SOC ecosystem deployed on AWS.

It reflects how modern security operations teams manage real-world incidents.
