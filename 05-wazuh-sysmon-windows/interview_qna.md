# 🎯 Interview Q&A: Wazuh + Sysmon 

---

## 1️⃣ What is Sysmon and why is it used?

Sysmon is a Windows system service and driver from Sysinternals that logs detailed system activity such as:

* Process creation
* DNS queries
* Network connections
* Registry changes
* File hash logging

It enhances Windows logging and provides advanced telemetry required for threat detection.

---

## 2️⃣ Why integrate Sysmon with Wazuh?

Wazuh alone collects default Windows logs.
Sysmon provides deeper telemetry.

Integration allows:

* Better detection coverage
* MITRE ATT&CK mapping
* Command-line visibility
* DNS-based C2 detection

---

## 3️⃣ What is Event ID 22 in Sysmon?

Event ID 22 logs DNS queries.

It is critical for detecting:

* Command & Control communication
* Suspicious scripting DNS activity
* Malware beaconing

---

## 4️⃣ How does log flow work in your architecture?

1. Sysmon logs event
2. Event written to Windows Event Channel
3. Wazuh Agent reads event
4. Agent forwards to Manager
5. Manager decodes event
6. Rule engine evaluates event
7. Alert generated and indexed
8. Dashboard displays alert

---

## 5️⃣ How did you detect encoded PowerShell?

By creating a custom Wazuh rule that matches:

* "-EncodedCommand"
* "-enc"

Mapped to MITRE T1059.001

---

## 6️⃣ How do you reduce alert flooding?

Two approaches:

1. Sysmon configuration tuning (exclude noise)
2. Wazuh rule suppression (level 0 rules)

Best practice:
Disable alerts, not visibility.

---

## 7️⃣ What are LOLBins?

Living-off-the-Land binaries (LOLBins) are legitimate Windows binaries abused by attackers.

Examples:

* certutil.exe
* rundll32.exe
* mshta.exe

Detected via Sysmon Event ID 1.

---

## 8️⃣ How would you scale this in production?

* Centralized Wazuh cluster
* TLS secured agent communication
* Sigma-based rule management
* Threat intelligence integration
* Active response automation

---

## 9️⃣ What is the difference between Event ID 1 and Event ID 3?

Event ID 1:
Process creation

Event ID 3:
Network connection initiated by process

---

## 🔟 How do you validate logs are reaching the manager?

Run:

```
tail -f /var/ossec/logs/archives/archives.json
```

Check for:

```
Microsoft-Windows-Sysmon
```

---
