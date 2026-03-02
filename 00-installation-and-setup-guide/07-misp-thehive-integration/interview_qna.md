# 🎯 MISP ↔ TheHive Integration – Interview Q&A

---

# 1️⃣ What is the purpose of integrating MISP with TheHive?

**Answer:**

The integration enables bidirectional intelligence sharing between:

* **MISP** → Threat Intelligence Platform
* **TheHive** → Incident Response Platform

It allows:

* Automatic import of MISP events as alerts in TheHive
* Automatic enrichment of observables using threat intelligence
* Exporting confirmed IOCs from TheHive cases back to MISP

This creates a closed intelligence lifecycle inside the SOC.

---

# 2️⃣ How does TheHive authenticate to MISP?

**Answer:**

TheHive authenticates using a **MISP API key**.

Steps:

1. Generate API key in MISP (Administration → Auth Keys)
2. Configure it in TheHive:

   * Platform Management → Connectors → MISP
3. TheHive uses REST API over HTTPS to communicate.

---

# 3️⃣ What are the possible integration modes in TheHive?

**Answer:**

Three modes:

1. **Import Only**

   * Pull MISP events as alerts

2. **Export Only**

   * Push TheHive case observables to MISP

3. **Import & Export (Recommended)**

   * Full bidirectional integration

---

# 4️⃣ What happens when MISP imports events into TheHive?

**Answer:**

* MISP event becomes a TheHive alert
* Attributes become observables
* Tags (including MITRE ATT&CK galaxy tags) are preserved
* Source is marked as `misp`
* Alert can be converted into a case

---

# 5️⃣ How does observable enrichment work?

**Answer:**

When an observable (IP, domain, hash) is added to a case:

* TheHive queries connected MISP server
* If match found:

  * Enrichment details attached
  * Related events shown
  * Threat context provided

This improves investigation accuracy and speed.

---

# 6️⃣ What type of data is typically imported from MISP?

**Answer:**

* IP addresses
* Domains
* URLs
* File hashes (MD5, SHA1, SHA256)
* Email addresses
* MITRE ATT&CK mappings
* Threat actor tags
* Malware families

---

# 7️⃣ Why should you not use admin API keys for integration?

**Answer:**

Using admin keys violates least privilege principle.

Risks:

* Excessive permissions
* Accidental modification of MISP data
* Harder audit tracking
* Larger blast radius if compromised

Best practice:

Create dedicated integration user with minimal required permissions.

---

# 8️⃣ How can you reduce alert fatigue when importing from MISP?

**Answer:**

Use filter settings:

* Maximum age (import only recent events)
* Allowed tag list
* Prohibited tag list
* Limit maximum number of attributes
* Restrict specific organizations

This prevents importing noisy or irrelevant feeds.

---

# 9️⃣ What happens when exporting a case to MISP?

**Answer:**

TheHive:

* Creates new MISP event
* Exports observables marked as IOCs
* Adds case title as event info
* Preserves tags
* Optionally includes TheHive case URL

This enables intelligence sharing with other organizations.

---

# 🔟 What are the security considerations for this integration?

**Answer:**

* Use HTTPS only
* Restrict API key by IP
* Rotate API keys periodically
* Monitor connector logs
* Avoid disabling SSL validation in production
* Use dedicated integration user

---

# 1️⃣1️⃣ How does this integration improve MTTR?

**Answer:**

Without integration:

* Analysts manually search MISP
* Copy/paste IOCs
* Switch tools frequently

With integration:

* Automatic enrichment
* Alerts auto-created
* One-click export
* Faster triage
* Faster decision making

This significantly reduces Mean Time To Respond.

---

# 1️⃣2️⃣ What permission is required in TheHive to manage MISP connectors?

**Answer:**

User must have:

```
managePlatform
```

Without it, user cannot configure connectors.

---

# 1️⃣3️⃣ What happens if the API key expires?

**Answer:**

* Connector test will fail
* No new events imported
* Export will fail
* Error logs appear in TheHive

Solution:

* Generate new API key in MISP
* Update connector settings
* Test connection

---

# 1️⃣4️⃣ Can TheHive connect to multiple MISP servers?

**Answer:**

Yes.

However:

* Multiple MISP servers require paid license
* Each server can have different filtering rules
* Useful for multi-org or MSSP environments

---

# 1️⃣5️⃣ What is the difference between alert and case in this integration?

**Answer:**

**Alert**

* Raw imported event
* Requires triage

**Case**

* Investigation container
* Tasks assigned
* Observables analyzed
* Evidence documented

MISP events become alerts → analyst converts alert to case.

---

# 1️⃣6️⃣ How does this integration support Threat Intelligence Lifecycle?

**Answer:**

1. Collect (MISP)
2. Analyze (TheHive)
3. Act (Case response)
4. Share (Export back to MISP)
5. Improve detection

It supports the full intelligence cycle.

---

# 1️⃣7️⃣ What is a real-world scenario for using Export Only mode?

**Answer:**

When:

* Organization consumes private intel
* But only shares confirmed IOCs
* Or wants to manually curate exported data

Example:

SOC confirms malware hash → exports to MISP for community sharing.

---

# 1️⃣8️⃣ What are common integration troubleshooting steps?

**Answer:**

* Test server connection
* Verify API key
* Check HTTPS certificate
* Validate MISP user permissions
* Check TheHive logs
* Verify firewall rules

---

# 1️⃣9️⃣ How would you explain this integration to a non-technical manager?

**Answer:**

This integration ensures:

* Threat intelligence automatically supports investigations
* Confirmed threats are shared with partners
* Security tools work together instead of in isolation
* Analysts work faster and more accurately

It increases SOC efficiency and collaboration.

---

# 2️⃣0️⃣ What makes this integration powerful in enterprise SOC?

**Answer:**

* Automation
* Context-aware investigations
* Community threat sharing
* Reduced manual effort
* Faster detection-to-response pipeline
* Intelligence-driven defense

---

# 🎤 Advanced Technical Question

## Q: What protocol does TheHive use to communicate with MISP?

**Answer:**

* HTTPS
* REST API
* JSON-based communication
* Authenticated using API key

---

# 🧠 Portfolio-Level Answer Summary

If interviewer asks:

> "Explain your MISP–TheHive integration project."

You can answer:

"I implemented a bidirectional integration between MISP and TheHive using native GUI connectors. I configured API-based authentication, applied filtering policies to reduce alert fatigue, enabled automatic observable enrichment, and implemented export workflows to share confirmed IOCs back to MISP. This created a full intelligence lifecycle in my SOC lab, improving MTTR and investigation efficiency."

---

# 🏁 End of Interview Guide

This prepares you for:

✔ SOC Analyst interviews
✔ Threat Intelligence roles
✔ IR Engineer interviews
✔ Blue Team discussions
✔ Security Engineer technical rounds

---
