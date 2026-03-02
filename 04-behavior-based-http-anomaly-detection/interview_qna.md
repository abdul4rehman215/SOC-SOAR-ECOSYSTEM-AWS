# 🎤 Interview Q&A - Behavior-Based HTTP Anomaly Detection & SOC Response

---

## 1️⃣ Why did you use ML instead of static rules?

Static rules detect known patterns only.

ML anomaly detection learns normal web behavior and detects deviations, enabling detection of unknown scanning or enumeration behavior.

---

## 2️⃣ What exactly was the anomaly feature?

Feature:
value_count of rule.id

Filtered by:
rule.groups = web

This measured frequency of web-related rule triggers per minute.

---

## 3️⃣ What does anomaly grade represent?

Anomaly grade (0–1) measures severity of deviation from baseline.

1.0 indicates extreme deviation.

---

## 4️⃣ Why use both grade and confidence thresholds?

Grade = how abnormal  
Confidence = model certainty  

Using both reduces false positives.

---

## 5️⃣ What behavior was detected?

Large spike in HTTP 404 errors caused by rapid URL enumeration using curl loop.

This matched reconnaissance scanning behavior.

---

## 6️⃣ How did you validate it wasn’t a false positive?

- Verified request frequency
- Confirmed repeated 404 responses
- Identified single attacker IP
- Confirmed enumeration pattern
- Retested after mitigation

---

## 7️⃣ What MITRE techniques did you map?

Tactic: Reconnaissance  
Techniques:
- T1595 Active Scanning
- T1046 Network Service Discovery

---

## 8️⃣ How is this different from a normal lab?

This project includes:

- ML baseline training
- Anomaly threshold tuning
- Real-time alert integration
- SOC investigation
- Case management
- Host mitigation
- Verification testing
- Case closure

It simulates enterprise SOC operations.

---

## 9️⃣ What improvements would you add in production?

- Enable Wazuh Active Response
- Add GeoIP enrichment
- Implement WAF rules
- Enable automated blocking
- Add dashboard reporting

---

## 🔟 What is the key takeaway?

Modern SOC teams must combine:

Rule-based detection
+ Behavior-based anomaly detection
+ Structured incident response

Detection alone is not enough.
