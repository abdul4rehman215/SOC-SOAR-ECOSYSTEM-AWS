# 🔐 SSH Brute Force Detection & Real-Time Alerting
### Wazuh + Slack + Kali Linux (End-to-End SOC Lab)

> This project demonstrates how a real Security Operations Center (SOC) detects, correlates, and escalates SSH brute force attacks in real time.
> It simulates attacker behavior, engineers detection logic in Wazuh, and delivers instant alerts to Slack — reflecting how modern blue teams monitor authentication abuse.

---

# 🎯 Project Objective

To design and validate a SOC-style detection pipeline that:

• Simulates an SSH brute force attack  
• Detects repeated authentication failures  
• Applies threshold-based alerting logic  
• Groups events by attacker IP  
• Sends real-time alerts to Slack  
• Demonstrates practical alert engineering  

This is not just tool setup — it is detection design.

---

# 🏗 Lab Architecture

| Component | Role |
|------------|------|
| Wazuh Manager | Log ingestion & alert engine |
| Ubuntu Client | Victim system (Wazuh Agent installed) |
| Kali Linux | Attacker machine |
| Slack | Real-time SOC notification channel |

Detection Flow:

Kali → Ubuntu (SSH failures)  
Ubuntu → Wazuh Agent → Wazuh Manager  
Wazuh → Alert Trigger → Slack  

---

# 🧠 What This Project Demonstrates

✔ Event correlation  
✔ Threshold-based detection logic  
✔ Log filtering & severity tuning  
✔ Source IP grouping  
✔ Real-time alert delivery  
✔ SOC workflow simulation  

This reflects real enterprise authentication monitoring.

---

# 📊 Detection Logic Design

The detection is engineered using:

• Count of SSH authentication failures  
• 1-minute rolling time window  
• Grouping by attacker source IP  
• Severity filtering (rule.level ≥ 5)  
• Threshold trigger (count > 5)

This reduces noise while detecting true attack patterns.

---

# 📂 Visual Setup Guide (Step-by-Step Screenshots)

For full dashboard walkthrough and configuration screenshots:

👉 **View the complete visual setup guide [PDF version of this project](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/02-wazuh-ssh-bruteforce-alerting-lab/Wazuh%20Alerting%20Setup%20SSH%20Brute%20Force%20Simulation.pdf)**

This includes:

• Slack webhook setup  
• Wazuh monitor creation  
• Trigger configuration  
• Alert output validation  
• Attack simulation screenshots  

---

# 🛠 Infrastructure Setup Summary

You need:

• Wazuh Manager (Server)  
• Ubuntu Client (Victim + Wazuh Agent)  
• Kali Linux (Attacker)  
• Slack Workspace  

All systems must be reachable via private network.

---

# 🔔 Slack Integration Overview

Slack is configured via:

• Incoming Webhooks  
• Dedicated SOC channel (#soc-alerts)  
• Wazuh notification channel  
• Per-alert action trigger  

This enables immediate analyst visibility.

---

# 🚨 Attack Simulation

From Kali:

```bash
for i in {1..10}; do ssh fakeuser@CLIENT_IP; done
````

Wazuh detects:

Invalid user fakeuser from <ATTACKER_IP>

Alert triggers when:

> More than 5 failures within 1 minute from same IP.

Slack receives:

• Alert name
• Severity
• Time window
• Attacker IP
• Alert status

---

# 📈 Real-World Use Case

This detection logic applies to:

• SSH brute force attacks
• Credential stuffing attempts
• Automated bot scanning
• Internal lateral movement attempts
• Password spraying

SOC teams use similar correlation logic in production.

---

# 🔐 Why Grouping by Source IP Matters

Without grouping:
Each failed login triggers separate noise.

With grouping:
You detect patterns — not single events.

This reflects real detection engineering principles.

---

# 🏁 Final Outcome

This lab successfully demonstrates:

• Attack simulation
• Log ingestion
• Alert engineering
• Threshold tuning
• Event correlation
• Real-time SOC notification
• Blue team defensive monitoring

This mirrors practical SOC operations.

---

# 📚 Skills Demonstrated

• Wazuh SIEM configuration
• Linux log analysis
• SSH attack detection
• Alert tuning & threshold logic
• Slack webhook integration
• SOC monitoring workflow design

---

# 📌 Repository Structure

```
02-wazuh-ssh-bruteforce-alerting-lab/
├── README.md
├── commands.sh
├── architecture-notes.txt
├── interview_qna.md
├── troubleshooting.md
└── Wazuh-Alerting-Setup-SSH-Brute-Force-Simulation.pdf
```

---

# 🔗 Full Installation & Platform Setup Guides

For complete Wazuh installation and ecosystem setup:

👉 **[View the full SOC installation & integration guide here](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/tree/main/00-installation-and-setup-guide)**

---

# 🎓 Why This Project Matters

Most labs show alerts.

This project shows:

How alerts are engineered.
Why thresholds matter.
How noise is reduced.
How alerts are escalated.
How SOC teams monitor authentication abuse in production.

It demonstrates detection thinking — not just configuration.

---

# 💼 Ideal For Roles

• SOC Analyst
• Blue Team Engineer
• Detection Engineer
• Security Operations Intern
• Cybersecurity Analyst

---

# 🏁 Capstone-Level Insight

This project shows that effective detection is not about counting logs.

It is about:

Context
Patterns
Thresholds
Correlation
Escalation

That is real SOC engineering.

---
