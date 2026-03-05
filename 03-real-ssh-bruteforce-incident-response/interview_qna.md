# 🎤 Interview Q&A - Real SSH Brute Force Incident Response  

### Wazuh + TheHive + MISP

---

## 1️⃣ Was this a simulated attack?

No. This was a real SSH brute force attack observed in logs, detected in real time by Wazuh, investigated in TheHive, mitigated on the host, and shared via MISP.

---

## 2️⃣ How did you confirm it was malicious?

I validated:

- Multiple authentication failures
- Same external source IP
- Short time window
- Multiple invalid usernames
- Credential access behavior (MITRE T1110)

The pattern confirmed brute force activity.

---

## 3️⃣ Why was it marked True Positive even though MISP had no record?

Threat intelligence feeds enhance context but do not replace behavioral validation.

Even without prior MISP intelligence, the activity matched brute force attack behavior. Therefore it was classified as malicious based on evidence.

---

## 4️⃣ What mitigation steps did you apply?

1. Blocked attacker IP via iptables  
2. Installed and enabled Fail2Ban  
3. Hardened SSH configuration  
   - Disabled root login  
   - Disabled password authentication  

This provided layered containment.

---

## 5️⃣ Why add the IOC to MISP?

Even if not previously reported, sharing confirmed malicious IPs:

- Strengthens community intelligence
- Improves future detections
- Closes the SOC intelligence loop

---

## 6️⃣ What MITRE technique did you map this to?

T1110 – Brute Force  
Tactic: Credential Access

---

## 7️⃣ How does this differ from a basic detection lab?

This project includes:

- Real incident
- Structured triage
- Full documentation
- Mitigation actions
- Intelligence sharing
- Case closure workflow

It demonstrates operational SOC practice, not just alert creation.

---

## 8️⃣ What SOC skills does this prove?

- Alert triage
- Log validation
- Incident documentation
- Threat classification
- Linux security hardening
- Firewall management
- Threat intelligence contribution

---

## 9️⃣ What would you improve in production?

- Add geo-location enrichment
- Implement MFA
- Configure SSH key-only access
- Add centralized firewall rules
- Automate IP blocking via Wazuh Active Response

---

## 🔟 What was the most important learning?

Detection alone is not enough.

True SOC maturity includes:

Detection → Investigation → Containment → Documentation → Intelligence Sharing
