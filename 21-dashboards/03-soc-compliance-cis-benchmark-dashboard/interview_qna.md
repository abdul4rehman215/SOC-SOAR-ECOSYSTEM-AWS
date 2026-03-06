# 📘 Interview Q&A — SOC Compliance & CIS Benchmark Dashboard

## 1️⃣ What was the main goal of this dashboard project?

The main goal was to build a **Wazuh-based compliance and CIS benchmark dashboard** that helps security teams monitor configuration posture, identify hardening weaknesses, and prioritize remediation more efficiently.

---

## 2️⃣ How is this dashboard different from a threat monitoring dashboard?

A threat monitoring dashboard focuses on **attacks, alerts, and suspicious activity**, while this dashboard focuses on **security posture, baseline configuration quality, and compliance-related findings**.

---

## 3️⃣ What does Wazuh SCA stand for?

SCA stands for:

```text
Security Configuration Assessment
````

It is a Wazuh capability used to evaluate endpoint configurations against security benchmarks and policy checks.

---

## 4️⃣ What kind of benchmarks can Wazuh SCA evaluate?

Wazuh SCA can evaluate systems against policies such as:

* CIS Benchmarks
* PCI-related checks
* NIST-aligned controls
* custom security configuration policies

In this project, the focus was on **CIS benchmark monitoring**.

---

## 5️⃣ Why is CIS benchmark visibility important in a SOC?

It is important because many attacks succeed through **misconfigurations and weak hardening**, not only through software vulnerabilities. CIS visibility helps reduce attack surface and improves baseline security posture.

---

## 6️⃣ Which filter was most important for isolating compliance data?

The most important filter used in this project was:

```text
rule.groups is sca
```

This filter ensures that only **Security Configuration Assessment events** are included in the dashboard.

---

## 7️⃣ Which fields were most important for this dashboard?

The most important fields were:

```text
data.sca.check.title
data.sca.check.result
data.sca.policy
timestamp
rule.groups
```

These fields support compliance status, failed-control analysis, policy-based breakdown, and trend visibility.

---

## 8️⃣ What does the “Compliance – Pass vs Fail” visualization show?

It shows the distribution of SCA result states such as:

* passed
* failed
* not applicable

This gives a quick overview of overall configuration health across monitored systems.

---

## 9️⃣ Why is the “Top Failed CIS Checks” panel useful?

It helps identify **which CIS controls fail most often**, so teams can prioritize the most common and potentially highest-impact hardening issues first.

---

## 🔟 What is the purpose of the findings timeline?

The findings timeline shows how compliance results change over time. It helps reveal:

* posture drift
* recurring failures
* remediation progress
* spikes in failed findings

---

## 1️⃣1️⃣ What does the overall score visualization represent?

It represents a **high-level posture indicator** that helps teams quickly assess whether the environment appears broadly aligned with the expected hardening baseline.

---

## 1️⃣2️⃣ Why is it important to separate compliance findings from general alerts?

Because Wazuh stores many event types, including authentication, file integrity, and network alerts. Without isolating SCA findings, the dashboard would mix unrelated data and lose its compliance focus.

---

## 1️⃣3️⃣ What kind of misconfigurations can this dashboard help highlight?

This dashboard can help highlight issues such as:

* insecure SSH settings
* weak remote access configurations
* missing logging-related controls
* poorly enforced hardening settings
* repeated failed CIS checks across systems

---

## 1️⃣4️⃣ Why keep the exported dashboard JSON in the project folder?

The exported JSON preserves the full working dashboard so it can be **re-imported exactly as built**. It also supports reuse, backup, reproducibility, and portfolio documentation.

---

## 1️⃣5️⃣ What did this project demonstrate overall?

This project demonstrated practical skills in:

* Wazuh SCA visibility
* CIS benchmark monitoring
* compliance-focused dashboard engineering
* security posture visualization
* remediation prioritization
* converting raw hardening data into actionable SOC visibility

---
