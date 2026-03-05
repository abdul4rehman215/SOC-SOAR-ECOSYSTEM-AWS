# 🔐 Real SSH Brute Force Detection & Incident Response
### Wazuh + TheHive 5.5 + MISP  

> End-to-End SOC Incident Handling (Capstone Project)

---

## 📌 Project Overview

This project documents the detection, investigation, containment, and intelligence sharing of a **real SSH brute force attack** observed on a monitored Linux server.

Unlike simulation-only labs, this project demonstrates a **complete SOC workflow lifecycle**, following industry-standard incident response methodology using:

- Wazuh (Detection & Log Analysis)
- TheHive 5.5 (Case Management & Investigation)
- MISP (Threat Intelligence Enrichment & Sharing)

This reflects how real SOC teams handle authentication abuse incidents.

---

## 🧠 What This Project Demonstrates

- Real-time detection
- Structured alert triage
- Log validation & pivot analysis
- Case documentation
- Observable extraction
- MITRE ATT&CK mapping
- Threat intelligence enrichment
- Host-level containment
- Secure configuration hardening
- IOC publication to MISP
- Full incident lifecycle closure

This is a full Blue Team operational workflow.

---

## 🖼 SOC Workflow Diagram

<div align="center">

<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/soc_workflow.png" width="800"/>

</div>
  
---

## 🏗 Operational Architecture

| Component    | Role                         |
| ------------ | ---------------------------- |
| Wazuh        | SIEM detection & correlation |
| TheHive 5.5  | Incident case management     |
| MISP         | Threat intelligence sharing  |
| Ubuntu Linux | Target server                |
| Slack        | Alert notification           |

---

# 📊 Incident Overview

* Attack Type: SSH Brute Force
* MITRE Technique: T1110 – Brute Force
* Detection Method: Wazuh correlation rules
* Severity: Medium
* Source: External public IP (US-based)
* Outcome: Confirmed True Positive

---

# ⏱ Incident Timeline

| Time (UTC) | Action                           |
| ---------- | -------------------------------- |
| 00:48      | Slack alert received             |
| 00:53      | Alert triaged in TheHive         |
| 01:00      | Investigation confirmed in Wazuh |
| 01:10      | Case created                     |
| 01:30      | Mitigation applied               |
| 01:50      | Case closed                      |
| 02:10      | IOC shared to MISP               |

This mirrors real SOC response sequencing.

---

# 🚨 Phase 1 – Detection (Wazuh)

Wazuh generated an alert indicating:

* Multiple SSH authentication failures
* Same external source IP
* Rapid invalid username attempts
* MITRE mapping to T1110

Detection was behavior-based, not signature-only.

---

# 🔎 Phase 2 – Triage (TheHive)

* Alert reviewed
* Status changed to **In Progress**
* Assigned to analyst
* Initial summary documented

Investigation lifecycle officially began.

---

# 🔍 Phase 3 – Log Validation

Using Wazuh Discover:

* Pivoted to SSH-related rules
* Observed repeated failures
* Confirmed attack frequency pattern
* Identified source IP consistency

This validated malicious intent.

---

# 📂 Phase 4 – Case Creation

A structured case was created including:

* Detection source
* Investigation findings
* Timeline
* MITRE mapping
* Observables
* Risk classification (TLP: AMBER)

This ensures traceability and audit compliance.

---

# 🌐 Phase 5 – Threat Intelligence Enrichment (MISP)

The attacker IP was searched in MISP:

* No prior intelligence found
* IP not listed in feeds

Despite this, behavior confirmed malicious activity.

The result was documented in the case.

---

# 🛡 Phase 6 – Containment & Mitigation

## 1️⃣ Firewall Block

```bash
sudo iptables -A INPUT -s <ATTACKER_IP> -j DROP
```

Immediate containment.

---

## 2️⃣ Enable Fail2Ban

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

Automated protection against repeated attempts.

---

## 3️⃣ SSH Hardening

Edited:

```
/etc/ssh/sshd_config
```

Set:

```
PermitRootLogin no
PasswordAuthentication no
```

Restart:

```bash
sudo systemctl restart ssh
```

Reduced attack surface.

---

# 📝 Phase 7 – Documentation & Closure

* Case updated with mitigation actions
* Relevant tags added
* Impact assessed
* Case marked **True Positive**
* Status set to **Resolved**

Professional closure summary added.

---

# 🌍 Phase 8 – IOC Sharing (MISP)

Created new MISP event:

* Title: SSH Brute Force Attack – Observed via Wazuh
* Distribution: All Communities
* Threat Level: Medium
* Analysis: Completed

Added attribute:

* Category: Network Activity
* Type: ip-src
* First/Last Seen timestamps
* Contextual comment

Event published.

TheHive case updated to reflect intelligence sharing.

---

# 🔁 Complete SOC Lifecycle

1. Detection
2. Triage
3. Investigation
4. Case creation
5. Observable extraction
6. MITRE mapping
7. Threat enrichment
8. Containment
9. Hardening
10. Documentation
11. Case closure
12. Intelligence publication

This represents a full incident response cycle.

---

# 📂 Visual & Detailed Walkthrough

For full investigation screenshots and documentation:

👉 **[View the complete Incident Response PDF Guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/03-real-ssh-bruteforce-incident-response/docs/Real%20SSH%20Brute%20Force%20Incident%20Respons%20Wazuh%20TheHive%20MISP.pdf)**

This includes:

* Dashboard screenshots
* Case management steps
* Mitigation screenshots
* MISP event publication
* Timeline evidence

Also available in this folder:
`Real-SSH-Brute-Force-Incident-Response.pdf`

---

# 🧠 Skills Demonstrated

* SOC alert triage
* Log analysis & pivoting
* Incident documentation
* MITRE ATT&CK mapping
* Host-level containment
* Linux hardening
* Firewall management
* Threat intelligence publishing
* Structured SOC workflow

---

# 🎯 Why This Project Matters

This project demonstrates:

* Real operational SOC workflow
* Structured investigation
* Defensive containment
* Intelligence sharing
* Documentation discipline

It reflects how real blue teams operate — not just lab simulation.

---

# 📂 Repository Structure

```
03-real-ssh-bruteforce-incident-response/
├── README.md
├── commands.sh
├── architecture-notes.txt
├── interview_qna.md
├── troubleshooting.md
└── docs/
    └── Real SSH Brute Force Incident Respons Wazuh TheHive MISP.pdf

# 🔗 Full SOC Platform Setup

Complete installation and integration guides available here:

👉 **[View the full SOC ecosystem setup guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/tree/main/00-installation-and-setup-guide)**

---

# 🏁 Final Note

This was not a synthetic alert.

It was a real SSH brute force attack, handled end-to-end using SOC best practices.

`Detection → Investigation → Mitigation → Intelligence Sharing`

---
