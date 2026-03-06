# 📘 Interview Q&A — SOC MITRE ATT&CK Coverage Dashboard

## 1️⃣ What was the main goal of this dashboard project?

The main goal was to build a **MITRE ATT&CK-focused dashboard in Wazuh** so analysts can understand attacker behavior, attack stage, and technique patterns instead of looking only at raw alert volume.

---

## 2️⃣ Why is a MITRE ATT&CK dashboard useful in a SOC?

It is useful because it gives analysts a **structured way to interpret detections** using tactics, techniques, and ATT&CK IDs. This improves investigation context and helps standardize threat analysis.

---

## 3️⃣ What problem does this dashboard solve compared to traditional alert monitoring?

Traditional monitoring usually focuses on counts, severity, and source information. This dashboard solves the problem of **limited behavioral context** by showing what the attacker is doing in ATT&CK terms.

---

## 4️⃣ Which Wazuh fields were most important for this project?

The most important fields were:

```text
rule.mitre.tactic
rule.mitre.technique
rule.mitre.id
timestamp
rule.level
````

These fields made it possible to visualize attack stages, techniques, IDs, and their activity over time.

---

## 5️⃣ Why was `rule.level between 8 and 15` used in this dashboard?

That filter was used to focus on **medium to high severity alerts**. It helps remove lower-value noise and makes the dashboard more aligned with realistic SOC triage and investigation workflows.

---

## 6️⃣ What does the “MITRE – Tactics Distribution” chart show?

It shows the distribution of alerts across ATT&CK tactics such as:

* Initial Access
* Credential Access
* Persistence
* Defense Evasion
* Command and Control

This helps analysts understand **which stage of attacker behavior is most visible** in the environment.

---

## 7️⃣ What is the purpose of the “MITRE – Top Techniques” visualization?

This panel shows the most commonly observed ATT&CK techniques, which helps analysts identify **repeated attacker methods** such as brute force, valid accounts, or account manipulation.

---

## 8️⃣ Why is the “MITRE – Technique IDs” panel important?

It provides a **standardized ATT&CK reference layer** by showing technique IDs like `T1110` or `T1078`. That makes reporting, investigations, and communication more consistent.

---

## 9️⃣ What value does the technique timeline add?

The technique timeline shows **how attacker behavior changes over time**. It helps identify spikes, recurring techniques, multi-stage behavior, and possible persistence-related patterns.

---

## 🔟 How does this dashboard improve analyst investigations?

It helps investigators move faster from alert review to **behavioral understanding**. Instead of reading each alert individually, they can first see which tactics and techniques dominate the activity.

---

## 1️⃣1️⃣ What kind of attack activity can this dashboard help highlight?

This dashboard can help highlight activity such as:

* brute-force attempts
* valid account usage
* account manipulation
* persistence-related detections
* command-and-control related behavior
* repeated ATT&CK technique activity over time

---

## 1️⃣2️⃣ Why is ATT&CK mapping valuable in detection engineering?

ATT&CK mapping is valuable because it helps detection engineers understand **what adversary behavior a rule is covering**, where visibility is strong, and where additional detection logic may be needed.

---

## 1️⃣3️⃣ Why keep the exported dashboard JSON in the project folder?

The exported JSON is kept so the dashboard can be **re-imported exactly as built**. It preserves the working dashboard object and makes the project reusable across environments.

---

## 1️⃣4️⃣ How is this dashboard different from a normal threat monitoring dashboard?

A normal threat monitoring dashboard focuses more on severity, volume, source IPs, and attack spikes. This dashboard focuses more on **ATT&CK behavior mapping**, which makes it better for structured adversary analysis.

---

## 1️⃣5️⃣ What did this project demonstrate overall?

This project demonstrated practical skills in:

* Wazuh dashboard engineering
* MITRE ATT&CK-based alert interpretation
* tactic and technique visualization
* ATT&CK ID standardization
* time-based technique analysis
* SOC investigation context improvement
* documentation of reusable dashboard projects

---
