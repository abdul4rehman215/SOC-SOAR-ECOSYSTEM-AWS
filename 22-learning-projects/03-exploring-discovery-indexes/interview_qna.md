# 📘 Interview Q&A — Wazuh Discover Indices Exploration

## 1️⃣ What was the main goal of this exploration?

The main goal was to explore the **different Wazuh Discover index patterns beyond `wazuh-alerts-*`** and understand how they help with investigations, telemetry validation, endpoint context, and deeper SOC analysis.

---

## 2️⃣ Why do most analysts focus mainly on `wazuh-alerts-*`?

Because alerts are the most action-oriented part of daily SOC work. They provide immediate detection results, so analysts naturally spend most of their time there.

---

## 3️⃣ Why is relying only on `wazuh-alerts-*` not enough?

Because alerts show **what triggered a rule**, but they do not always explain:

- host state
- telemetry health
- pipeline health
- raw logs that did not trigger rules
- endpoint inventory context

---

## 4️⃣ What does `wazuh-archives-*` provide?

`wazuh-archives-*` provides access to **raw logs and events**, including data that may not have triggered alerts. It is very useful for forensics, rule tuning, missed-detection review, and deeper investigations.

---

## 5️⃣ What is the value of `wazuh-monitoring-*`?

`wazuh-monitoring-*` helps analysts verify **agent health and reporting continuity**. It is useful for checking whether a monitored endpoint was online, synced, and actively sending telemetry during a specific investigation window.

---

## 6️⃣ What does `wazuh-statistics-*` help with?

`wazuh-statistics-*` helps with understanding **Wazuh pipeline and processing health**. It can reveal event drops, queue pressure, internal performance issues, and ingestion stress that may affect security visibility.

---

## 7️⃣ Why is pipeline health important for a SOC analyst?

Because if the pipeline is overloaded or dropping events, then the absence of alerts may not mean the environment is safe. It may mean the telemetry was incomplete.

---

## 8️⃣ What are `wazuh-states-*` or `wazuh-states-inventory-*` indices used for?

They are used for **point-in-time endpoint state and inventory visibility**. They can show things like:

- packages
- ports
- processes
- services
- interfaces
- hardware
- system details
- users and groups

---

## 9️⃣ Why are state and inventory indices important in investigations?

Because they help analysts understand **what existed on the endpoint** at a given time. That adds valuable context for root cause analysis, hunting, baseline definition, and host-state validation.

---

## 🔟 Why are these other indices often ignored?

They are often ignored because:

- alerts are easier to act on
- many SOC workflows are ticket-driven
- monitoring and statistics data look operational
- inventory/state data are often seen only through modules
- teams are not always trained to pivot across index families

---

## 1️⃣1️⃣ How can `wazuh-monitoring-*` help during an incident?

It can help confirm whether the affected agent was:

- online
- connected
- synced
- actively reporting

during the time the incident happened. That improves confidence in the investigation timeline.

---

## 1️⃣2️⃣ How can `wazuh-statistics-*` help detection engineering?

It helps detection engineers understand whether missing alerts may be caused by:

- dropped events
- queue pressure
- ingestion bottlenecks
- performance limitations

rather than only by weak detection logic.

---

## 1️⃣3️⃣ How do inventory indices help threat hunting?

Inventory indices help threat hunters review things like:

- installed packages
- running processes
- open ports
- active services
- endpoint interfaces

That supports anomaly detection, baseline comparison, and host-context enrichment.

---

## 1️⃣4️⃣ What is one of the biggest lessons from this exploration?

One of the biggest lessons was:

> **Alerts tell you that something happened, but the other indices often help explain why it happened, what existed around it, and whether the telemetry behind it was trustworthy.**

---

## 1️⃣5️⃣ What did this exploration demonstrate overall?

This exploration demonstrated practical understanding of how **Wazuh Discover becomes much more powerful when analysts use multiple index families**, not just alerts. It showed the value of archives, monitoring, statistics, and state/inventory data for mature SOC investigations and security operations.
