# 🎤 Interview Q&A — AI-Driven SOC Alert Triage Automation (Wazuh + n8n + Gemini)

> ✅ Focus: SOC automation, alert triage, SIEM → SOAR workflow design, AI prompt engineering, analyst-ready reporting.

---

## 1) What problem does this project solve in a SOC?
It reduces **manual alert triage time** by automatically converting raw SIEM alerts into **structured, analyst-ready intelligence** with actions and next steps.

---

## 2) Why did you integrate **n8n** with **Wazuh** instead of using Wazuh alone?
Wazuh is great for detection, but n8n adds **orchestration + automation**, letting me route alerts, apply logic, call AI services, and deliver outputs to analysts automatically.

---

## 3) How do alerts flow from Wazuh to n8n in this project?
Wazuh triggers an **integration script**, which forwards the alert JSON to an **n8n Webhook**, then the workflow normalizes → AI triage → formats → emails the analyst.

---

## 4) What is the purpose of the **severity threshold** (rule.level ≥ 7)?
It prevents noise by forwarding only **meaningful alerts**, reducing alert fatigue and ensuring analysts only receive high-signal events.

---

## 5) Why did you use a **custom Wazuh integration script** instead of only the ossec.conf level filter?
The script provides **extra control** (custom filtering + payload shaping + logging) and ensures only the right alerts are forwarded in a structured way.

---

## 6) What was the most important optimization you made in this project?
Passing the **full raw alert JSON** to the AI agent instead of only partial fields — this improved triage accuracy and reduced generic responses.

---

## 7) How did you prevent the AI from hallucinating or inventing details?
I used a **strict production prompt** with hard rules: *use only JSON*, *no assumptions*, *no scenario rewriting*, and output must follow a fixed structure.

---

## 8) What output does the SOC analyst receive, and why is it better than raw logs?
The analyst receives a **clean HTML email** containing: overview table, summary, risk assessment, recommended actions, and one clear next step — faster to act on than raw logs.

---

## 9) Why did you format the output as an email instead of only using dashboards?
Email is a direct analyst delivery channel; it reduces time-to-awareness and provides **decision-ready output** without needing to open dashboards first.

---

## 10) What role do the JavaScript nodes play inside n8n?
They handle **alert normalization**, field extraction, parsing AI output sections, and generating a professional **HTML report** with severity styling.

---

## 11) What did you learn about SOAR workflow design from this project?
SOAR requires more than tool integration — it needs **filtering, context handling, reliability, output design, and iterative troubleshooting** to be production-grade.

---

## 12) What are common SOC use cases for n8n beyond this project?
Threat intel enrichment, ticket creation (TheHive/Jira), Slack/Teams routing, automated remediation triggers, scheduled reporting, and alert correlation pipelines.

---

## 13) Why is “structured prompt engineering” important for SOC automation?
Without strict structure, AI output becomes inconsistent and unreliable; structured prompts ensure **repeatable triage reports** usable in real SOC operations.

---

## 14) How does this project improve MTTD and MTTR?
It reduces time spent reading logs by generating instant triage summaries and recommended actions, helping analysts decide faster and respond sooner.

---

## 15) What would you add next to make it more enterprise-ready?
Auto-create cases in **TheHive**, enrich IOCs (VirusTotal/OTX/AbuseIPDB), multi-channel routing (Slack/Teams), and gated active response workflows for containment.

---
