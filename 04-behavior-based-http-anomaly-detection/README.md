# 🛡️ Behavior-Based HTTP Anomaly Detection & Incident Response

### Wazuh + OpenSearch ML + Slack + TheHive (End-to-End SOC Workflow)

> This project demonstrates real-world SOC detection engineering using **machine learning–based anomaly detection** instead of static rule matching.
> It covers the complete lifecycle: anomaly detection → alerting → investigation → MITRE mapping → incident response → mitigation → case closure.

---

# 🎯 Project Objective

To design and validate a behavior-based SOC detection pipeline that:

* Learns baseline HTTP behavior
* Detects abnormal spikes in HTTP errors (404 flood)
* Triggers real-time Slack alerts
* Escalates into TheHive for case handling
* Maps activity to MITRE ATT&CK
* Applies host-level containment
* Verifies mitigation
* Closes the case formally

This is detection engineering + incident response combined.

---

# 🧠 Why Behavior-Based Detection?

Traditional rule-based detection:

* Only detects known patterns
* Misses new or low-signal reconnaissance

Behavior-based ML detection:

* Learns normal traffic baseline
* Detects deviations automatically
* Identifies reconnaissance / scanning early
* Reduces dependency on static rules

As shown in the project documentation , anomaly detection identifies unusual behavior such as sudden spikes in HTTP 404 errors and abnormal request rates.

---

# 🏗 Architecture Overview

<div align="center">

<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/behaviour-based_http_anomaly_architect_diagram.png" width="800"/>

</div>

### Detection Flow
```
Kali Attacker
⬇
Apache Web Server (access.log)
⬇
Wazuh Agent
⬇
Wazuh Manager
⬇
OpenSearch (wazuh-alerts-*)
⬇
OpenSearch ML Anomaly Detector
⬇
Alerting Monitor
⬇
Slack Notification
⬇
TheHive Case
⬇
iptables Mitigation
```
---

# ⚙️ Detection Engineering – ML Setup

## 1️⃣ Create Anomaly Detector

As documented on page 2 of your project PDF :

* Index: `wazuh-alerts-*`
* Filter: `rule.groups = web`
* Timestamp: `@timestamp`
* Feature name: `http_error_count`
* Aggregation: `value_count`
* Field: `rule.id`
* Interval: 1 minute
* Shingle size: 8

This trains the model on web-related rule activity.

---

## 2️⃣ Enable Baseline Learning

Enabled:

* Historical analysis
* Real-time detection

(Shown in Step 2 of the PDF )

This allows the model to understand normal HTTP error behavior.

---

# 🚨 Alerting & Slack Integration

Monitor Type:

```
Anomaly Detector
```

Trigger:

```
Anomaly Grade > 0.7
AND
Confidence > 0.7
```

Severity:

```
High
```

Slack webhook action:

```
Notify_SOC_HTTP_Anomaly
```

(As shown in Step 3 of the PDF )

---

# ⚔️ Attack Simulation (Kali)

From attacker machine:

```bash
for i in {1..300}; do
  curl http://TARGET_IP/test$i > /dev/null
done
```

This caused:

* Large spike in HTTP 404 responses
* Baseline deviation
* Anomaly grade reached 1.00 (as shown in Step 5 )

---

# 📊 Detection Verification

In OpenSearch:

* Red anomaly bar visible
* Grade near 1.0
* Confidence elevated

Confirmed ML detected abnormal behavior.

---

# 🔍 Investigation in Discover

Filters applied:

```
rule.groups: web
```

Findings (Step 6 ):

* Repeated requests from single source IP
* URL enumeration pattern
* Excessive 404 responses
* High request frequency

Conclusion:
Behavior matches reconnaissance / scanning.

---

# 🧭 MITRE ATT&CK Mapping

As documented (Step 7 ):

Tactic:

```
Reconnaissance
```

Techniques:

```
T1595 – Active Scanning
T1046 – Network Service Discovery
```

---

# 🐝 TheHive Incident Response

## Case Created

Title:

```
HTTP Error Flood – Web Enumeration Activity
```

Added:

* Attacker IP (observable)
* Target host
* Service: Apache
* MITRE mapping
* Detection source: ML anomaly

Tasks assigned:

* Analysis
* Containment
* Mitigation

(See Step 8 in PDF )

---

# 🛡 Mitigation & Containment

Blocked attacker:

```bash
sudo iptables -A INPUT -s ATTACKER_IP -j DROP
```

Restarted Apache:

```bash
sudo systemctl restart apache2
```

Optional hardening:

```bash
sudo a2enmod ratelimit
sudo a2enmod security2
sudo systemctl restart apache2
```

(Shown in Step 9 )

---

# ✅ Verification

Retried attack from Kali.

Result:

```
Connection refused / blocked
```

No further anomalies observed (Step 10 )

Case marked:

```
Resolved
Closed
```

---

# 📈 Project Outcome

✔ ML-based anomaly detection engineered
✔ Baseline learned
✔ Real-time Slack alert triggered
✔ Logs investigated
✔ MITRE mapping performed
✔ Incident documented in TheHive
✔ Host-level mitigation applied
✔ Case formally closed

As summarized in the final section of the project PDF , this demonstrates a full end-to-end SOC workflow.

---

# 🧠 Skills Demonstrated

* ML-based detection engineering
* OpenSearch anomaly tuning
* SOC alert design
* Behavioral investigation
* MITRE ATT&CK mapping
* TheHive case management
* Linux host mitigation
* End-to-end SOC workflow execution

---

# 📄 Full Visual Walkthrough

👉 **[View the complete step-by-step project PDF with screenshots](Insert your GitHub PDF link here)**

---

# 🎯 Why This Project Matters

Most labs demonstrate rule alerts.

This project demonstrates:

* Baseline modeling
* Behavioral deviation detection
* Analyst investigation
* Structured incident handling
* Real containment validation

This reflects modern enterprise SOC practice.

---
