# 📘 Interview Q&A — Wazuh IT Hygiene Module Exploration

## 1️⃣ What was the main goal of this IT Hygiene exploration?

The main goal was to explore how the **Wazuh IT Hygiene module** helps SOC analysts understand endpoint context, baseline state, and operational visibility beyond alerts alone.

---

## 2️⃣ Why is the IT Hygiene module important in a SOC?

It is important because analysts often need to understand **what is normal on an endpoint** before deciding whether something is suspicious or malicious. IT Hygiene helps provide that baseline context.

---

## 3️⃣ Why do many teams overlook IT Hygiene?

Many teams focus heavily on alerts, detections, and incidents, so visibility into system inventory, software, processes, services, and endpoint state is often undervalued even though it strongly improves investigations.

---

## 4️⃣ What kind of information does the IT Hygiene module provide?

It provides visibility into multiple endpoint domains, including:

- system and hardware details
- installed software and packages
- running processes
- network ports and protocols
- identity context
- active services

---

## 5️⃣ How does IT Hygiene improve alert investigations?

It improves investigations by giving analysts surrounding context. Instead of only seeing an alert, they can also understand the host’s processes, software, services, ports, and resource profile to judge whether activity fits the normal baseline.

---

## 6️⃣ What is the value of system and hardware visibility in IT Hygiene?

System and hardware visibility helps analysts understand operating system type, CPU details, memory usage, and host characteristics. This helps build endpoint baselines and detect unusual resource or system conditions.

---

## 7️⃣ Why is software and package visibility useful from a security perspective?

Software visibility helps identify installed tools, unexpected packages, risky software, or inventory drift. It also supports vulnerability assessment, asset review, and validation of whether software is authorized.

---

## 8️⃣ Why are running processes so important in endpoint investigations?

Processes are important because they reveal what is actively executing on the endpoint. Analysts can review process names, PIDs, parent-child relationships, command lines, and start times to identify suspicious behavior or persistence clues.

---

## 9️⃣ What does the network section of IT Hygiene help analysts understand?

It helps analysts review ports, protocols, listeners, and process-linked network activity. This is useful for finding unnecessary exposed services, unusual listeners, or network-facing processes that expand attack surface.

---

## 🔟 Why are services important in IT Hygiene analysis?

Services are important because they are part of normal baseline operations, but they can also be abused for persistence or stealthy execution. Reviewing service inventory helps identify what should and should not be active on an endpoint.

---

## 1️⃣1️⃣ How does IT Hygiene support proactive security, not just reactive security?

It supports proactive security by helping teams identify weak hygiene, unnecessary services, suspicious software, and baseline drift **before** those issues become active incidents or trigger high-severity alerts.

---

## 1️⃣2️⃣ How does the IT Hygiene module support threat hunting?

It supports threat hunting by giving analysts endpoint context they can use to validate anomalies, review processes, inspect software inventory, check exposed network services, and compare systems against expected baseline behavior.

---

## 1️⃣3️⃣ What is one of the most important security questions IT Hygiene helps answer?

One of the most important questions it helps answer is:

> **What is normal on this endpoint?**

That question is critical before deciding whether a process, service, package, or port is suspicious.

---

## 1️⃣4️⃣ How does IT Hygiene fit into a larger Wazuh SOC ecosystem?

It complements other SOC functions like threat monitoring, detection engineering, threat hunting, vulnerability visibility, and incident response by providing the endpoint context that makes those workflows stronger and more accurate.

---

## 1️⃣5️⃣ What did this exploration demonstrate overall?

This exploration demonstrated practical understanding of how the **Wazuh IT Hygiene module** improves endpoint visibility, baseline understanding, anomaly recognition, process and service review, attack-surface awareness, and context-driven SOC analysis.
