# 🎯 Interview Q&A – SSH Brute Force Detection Lab  
### Wazuh + Slack + Detection Engineering

---

## 🔹 1. What was the objective of this project?

The objective was to simulate a real-world SSH brute force attack and design a detection pipeline that identifies repeated authentication failures using threshold-based correlation logic in Wazuh, then escalates alerts to Slack in real time.

This project focuses on detection engineering, not just tool setup.

---

## 🔹 2. Why is threshold-based detection important for SSH monitoring?

A single failed login is normal behavior.

Threshold-based detection ensures that:

- Multiple failures within a short time window
- From the same source IP
- Above a defined count

are treated as malicious behavior rather than noise.

This reduces false positives and alert fatigue.

---

## 🔹 3. What rule did you use to detect SSH failures?

Wazuh rule:

- `rule.id = 100300`
- Description: SSH invalid user attempt
- Severity filter: `rule.level ≥ 5`

This rule detects invalid SSH authentication attempts from logs.

---

## 🔹 4. How did you design the detection logic?

The detection monitor was configured with:

- Metric: Count of documents
- Time Window: 1 minute
- Filter: rule.id = 100300
- Severity: rule.level ≥ 5
- Group By: data.srcip
- Trigger Condition: Count > 5

This detects behavioral patterns instead of isolated events.

---

## 🔹 5. Why did you group by `data.srcip`?

Grouping by source IP allows the monitor to:

- Correlate repeated attempts from the same attacker
- Prevent unrelated login failures from triggering alerts
- Detect brute force behavior accurately

Without grouping, every failed login would generate noise.

---

## 🔹 6. What happens in the data flow when an attack occurs?

1. Kali generates repeated SSH login attempts.
2. Ubuntu logs authentication failures.
3. Wazuh Agent forwards logs to Manager.
4. Wazuh Manager processes events.
5. Detection monitor evaluates frequency threshold.
6. Alert triggers when threshold exceeded.
7. Slack webhook sends notification.
8. Analyst receives alert.

This mirrors real SOC alert pipelines.

---

## 🔹 7. Why did you choose Slack for alerting?

Slack simulates:

- Real-time SOC alert channels
- Team-based incident visibility
- Instant escalation workflows

In enterprise environments, this could be replaced with:

- Email alerts
- PagerDuty
- Microsoft Teams
- Ticketing systems

Slack is used here to model notification workflow.

---

## 🔹 8. How does this reduce alert fatigue?

Alert fatigue occurs when every small event triggers an alert.

This project reduces fatigue by:

- Applying severity filtering
- Setting a frequency threshold
- Using short time windows
- Correlating by attacker IP

Only meaningful attack patterns trigger escalation.

---

## 🔹 9. What real-world attacks does this simulate?

This detection model applies to:

- SSH brute force attacks
- Password spraying
- Credential stuffing
- Automated scanning activity
- Internal reconnaissance attempts

It reflects real authentication abuse monitoring.

---

## 🔹 10. What challenges did you encounter?

Common challenges include:

- Slack webhook misconfiguration
- Incorrect filter queries
- Threshold too low (excessive alerts)
- Threshold too high (missed detection)
- Incorrect grouping field
- Time window misalignment

Tuning detection logic is critical.

---

## 🔹 11. How would you improve this project for enterprise deployment?

Improvements could include:

- IP reputation enrichment
- Geo-location tagging
- Integration with case management (TheHive)
- Automatic blocking via firewall rule
- Adaptive thresholds based on baseline behavior
- Alert suppression rules

---

## 🔹 12. How does this demonstrate detection engineering skills?

This project demonstrates:

- Log analysis understanding
- Rule-based filtering
- Threshold design
- Event correlation
- Alert noise reduction
- Real-time notification setup
- SOC workflow modeling

It shows understanding of how alerts should be engineered, not just enabled.

---

## 🔹 13. What is the key takeaway from this lab?

Effective detection is not about counting logs.

It is about:

- Context
- Frequency
- Pattern recognition
- Correlation
- Escalation logic

This project reflects foundational SOC detection engineering principles.

---

## 🔹 14. If asked in one sentence, how would you describe this project?

"I designed and implemented a behavior-based SSH brute force detection pipeline using Wazuh with threshold correlation logic and real-time Slack alerting to simulate enterprise SOC monitoring."

---

## 🔹 15. Which roles does this project align with?

- SOC Analyst
- Detection Engineer
- Blue Team Engineer
- Security Operations Engineer
- Cybersecurity Analyst
- Threat Monitoring Specialist

---

# 🏁 Summary

This project demonstrates:

Attack Simulation → Log Ingestion → Correlation → Threshold Alerting → Real-Time Notification

It reflects practical SOC detection design used in real-world security operations.
