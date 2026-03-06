# 📘 Interview Q&A — Wazuh Dashboard Engineering & Security Visualization

## 1️⃣ What is the primary purpose of Wazuh dashboards in a SOC?

Wazuh dashboards help SOC analysts **visualize, monitor, and investigate security data more efficiently**. Instead of reviewing only raw alerts, analysts can use dashboards to identify trends, prioritize events, and understand the broader security picture faster.

---

## 2️⃣ Why are dashboards important for security analysts?

Dashboards improve analyst workflow by providing **quick visual context**. This helps reduce time spent manually parsing logs, speeds up triage, and supports better decision-making during monitoring and investigations.

---

## 3️⃣ How do dashboards reduce alert fatigue?

Dashboards reduce alert fatigue by **grouping and summarizing alerts visually** through charts, tables, and metrics. This makes it easier to spot meaningful spikes or high-priority events without treating every alert equally.

---

## 4️⃣ What kind of security value does a threat monitoring dashboard provide?

A threat monitoring dashboard helps analysts track **active alerts, severity distributions, top alerting agents, frequent rule groups, and alert trends**. It is especially useful for daily SOC monitoring and initial triage.

---

## 5️⃣ Why would a SOC team use a MITRE ATT&CK dashboard?

A MITRE ATT&CK dashboard helps analysts understand detections through an **attacker behavior framework**. It shows which tactics and techniques appear in monitoring data and helps detection engineers evaluate visibility coverage.

---

## 6️⃣ What is the benefit of a compliance and CIS benchmark dashboard?

A compliance and CIS benchmark dashboard provides visibility into **security posture, configuration assessment results, and failing benchmark-related checks**. It helps security teams identify hardening gaps and track posture improvements over time.

---

## 7️⃣ How do dashboards support detection engineering?

Dashboards help detection engineering by showing whether alerts are **useful, noisy, trending, or operationally valuable**. They make it easier to evaluate rule effectiveness and identify opportunities for tuning.

---

## 8️⃣ Why is dashboard JSON export useful in a project like this?

The JSON export allows the dashboard to be **reused, re-imported, and preserved exactly as built**. This is useful both for practical deployment and for portfolio documentation where the dashboard layout needs to be reproducible.

---

## 9️⃣ Why keep both documentation and dashboard JSON in the same project?

Keeping both together supports **two purposes at once**: learning and reuse. The documentation explains the purpose and design logic, while the JSON file preserves the actual dashboard object for import into Wazuh.

---

## 🔟 How does dashboard visualization help during investigations?

Visualization helps investigators identify **patterns, spikes, recurring alert sources, and time-based trends** more quickly than raw log review alone. It improves situational awareness before drilling into individual events.

---

## 1️⃣1️⃣ What is the difference between raw alerts and dashboard-level visibility?

Raw alerts provide event-level detail, while dashboards provide **aggregated operational visibility**. Dashboards help analysts identify what matters first, and raw alerts help them investigate deeper after prioritization.

---

## 1️⃣2️⃣ Why is this project considered part of SOC engineering and not just UI customization?

This project is part of SOC engineering because it focuses on **operational security visibility**, analyst usability, monitoring strategy, and how detections are consumed in practice. It improves how the SOC works, not just how it looks.

---

## 1️⃣3️⃣ What are the three dashboard categories organized in this project?

The three dashboard categories in this project are:

- **SOC Threat Monitoring Dashboard**
- **SOC MITRE ATT&CK Coverage Dashboard**
- **SOC Compliance & CIS Benchmark Dashboard**

Each one supports a different monitoring objective inside the SOC ecosystem.

---

## 1️⃣4️⃣ How do dashboards improve communication inside a security team?

Dashboards help communicate security findings more clearly by turning large volumes of data into **understandable visual summaries**. This helps during analyst handoffs, reporting, tuning discussions, and management updates.

---

## 1️⃣5️⃣ What did this dashboard engineering project demonstrate overall?

This project demonstrated practical understanding of **Wazuh dashboard use cases, analyst workflow improvement, security visualization planning, reusable dashboard organization, and SOC-focused documentation practices**.
