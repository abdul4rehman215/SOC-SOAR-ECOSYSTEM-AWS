# 📘 Interview Q&A — Wazuh Threat Hunting Module Exploration

## 1️⃣ What was the main goal of this threat hunting exploration?

The main goal was to explore how the **Wazuh Threat Hunting module** helps SOC analysts investigate suspicious behavior proactively instead of relying only on triggered alerts and incident queues.

---

## 2️⃣ How is threat hunting different from normal alert monitoring?

Alert monitoring is mostly **reactive** and starts after a rule fires, while threat hunting is **proactive** and starts with analyst questions, hypotheses, suspicious patterns, or low-level behaviors that may not yet look like an incident.

---

## 3️⃣ Why is threat hunting important in a SOC?

It is important because attackers often avoid loud, obvious behavior. Threat hunting helps analysts identify:

- subtle anomalies
- repeated low-level patterns
- suspicious but non-critical activity
- behavior that bypasses traditional alert-first workflows

---

## 4️⃣ Why do many teams underuse threat hunting?

Many teams stay focused on alert queues, tickets, and severity-driven response. That makes it easy to overlook analyst-driven investigation of quieter activity, even though that is often where early attacker behavior appears.

---

## 5️⃣ What kind of data makes threat hunting possible in Wazuh?

Threat hunting in Wazuh becomes possible because the platform centralizes and makes searchable:

- event data
- rule descriptions
- timestamps
- agent activity
- authentication events
- process-related events
- MITRE ATT&CK mappings
- historical data over time

---

## 6️⃣ Why is historical event visibility important for threat hunting?

Historical visibility matters because suspicious behavior often becomes meaningful only when analysts look across time. A single event may look harmless, but repeated or correlated events across hours or days may reveal real malicious patterns.

---

## 7️⃣ What does “behavior-driven investigation” mean in this context?

It means the analyst focuses on **what the system is doing**, not just which alert fired. Instead of reacting only to severity, the analyst studies patterns, context, drift from baseline, and event relationships.

---

## 8️⃣ How does baseline understanding help in threat hunting?

Baseline understanding helps analysts decide whether activity is truly unusual. Threat hunting becomes much stronger when analysts know what is normal for a host, a user, a service, or an event pattern before labeling something suspicious.

---

## 9️⃣ What role does MITRE ATT&CK play in threat hunting?

MITRE ATT&CK adds structure to hunting by helping analysts interpret activity through attacker tactics and techniques. This makes investigations more consistent and helps connect observed behavior to known attacker tradecraft.

---

## 🔟 What kind of suspicious activity can threat hunting reveal even when severity is low?

Threat hunting can help reveal:

- repeated authentication failures
- unusual process behavior
- suspicious package manager activity
- agent outliers
- unexpected MITRE-mapped behavior
- recurring low-level events that form a larger pattern

---

## 1️⃣1️⃣ Why is event-level investigation important in hunting?

Because summary dashboards are useful for direction, but real hunting often requires analysts to drill into the raw or individual event level to understand:

- what happened
- when it happened
- on which agent it happened
- how often it happened
- whether the behavior actually makes sense

---

## 1️⃣2️⃣ How does agent-based visibility help a threat hunter?

It helps identify which systems are behaving differently from others. That makes it easier to spot high-risk endpoints, unusual event concentrations, or systems that deserve deeper investigation.

---

## 1️⃣3️⃣ How can threat hunting improve detection engineering?

Threat hunting can reveal suspicious behaviors that are not being detected clearly enough. Analysts can use those findings to improve rules, tune noisy detections, and create better future monitoring coverage.

---

## 1️⃣4️⃣ Why should a SOC not depend only on high-severity alerts?

Because many real attacks begin with quiet, normal-looking behavior. If a SOC only looks at high-severity alerts, it may miss early indicators, low-level attacker movement, or subtle behavior that becomes dangerous later.

---

## 1️⃣5️⃣ What did this exploration demonstrate overall?

This exploration demonstrated practical understanding of how the **Wazuh Threat Hunting module** supports proactive SOC analysis through event search, behavioral review, baseline comparison, MITRE context, time-based investigation, and deeper analyst-led security reasoning.
