# 🧠 TheHive ↔ Cortex Integration – Interview Q&A

This section prepares you for:

* SOC Analyst interviews
* DFIR interviews
* SOC Architect interviews
* Threat Intelligence Engineer interviews
* SOAR / Automation Engineer interviews

This is not basic-level Q&A.

These are real-world, architecture-level explanations.

---

# 🔹 BASIC CONCEPTUAL QUESTIONS

---

## 1️⃣ What is Cortex?

**Answer:**

Cortex is an open-source analyzer and responder engine developed by StrangeBee (TheHive Project).

It is used to:

* Enrich observables (IP, domain, hash, URL)
* Query external intelligence services
* Execute automated response actions

Cortex does not manage cases — it processes and enriches data.

---

## 2️⃣ What is TheHive?

**Answer:**

TheHive is a case management and incident response platform designed for SOC teams.

It allows:

* Alert triage
* Case lifecycle management
* Observable tracking
* Collaboration
* Timeline audit trail
* Integration with Cortex for enrichment

TheHive is the brain.
Cortex is the execution engine.

---

## 3️⃣ Why integrate TheHive with Cortex?

**Answer:**

Without integration:

* Analysts manually check VirusTotal, URLScan, WHOIS, etc.
* Context is lost between tabs.
* No structured audit trail.

With integration:

* One-click enrichment
* Centralized intelligence
* Structured reports inside case
* Full audit logging
* Faster triage
* Reduced analyst fatigue

This eliminates tab-hopping in SOC workflows.

---

# 🔹 ARCHITECTURE QUESTIONS

---

## 4️⃣ Explain how TheHive and Cortex communicate.

**Answer:**

TheHive communicates with Cortex via REST API.

Flow:

1. TheHive sends observable + analyzer ID
2. Uses API key (Bearer token authentication)
3. Cortex launches Docker analyzer job
4. Analyzer queries external service
5. Results returned in JSON
6. TheHive stores structured + raw output in case

Authentication model:
Authorization: Bearer <API_KEY>

---

## 5️⃣ How does Cortex execute analyzers?

**Answer:**

Cortex uses Docker containers.

When an analyzer is triggered:

* A temporary container (cortex-job-xxxx) is created
* Analyzer script runs
* Queries external API
* Formats results
* Container exits
* Results stored in job history

This makes analyzers isolated and scalable.

---

## 6️⃣ What happens if an analyzer fails?

**Answer:**

Possible reasons:

* API rate limit exceeded
* External service downtime
* Incorrect API key
* Docker permission issue

Cortex logs failure in Job History.
TheHive displays error status in case timeline.

Failure does not break case workflow.

---

# 🔹 SECURITY QUESTIONS

---

## 7️⃣ How is security handled in this integration?

**Answer:**

Security mechanisms include:

* API key authentication
* Organization-level isolation
* Role-based access control
* Docker container isolation
* Audit logging in both platforms

Best practices:

* Restrict ports 9000 & 9001
* Use reverse proxy + HTTPS
* Rotate API keys
* Disable Elasticsearch exposure

---

## 8️⃣ Why is Docker socket required in Cortex?

**Answer:**

Cortex must access Docker to:

* Spin up analyzer containers
* Execute jobs
* Destroy containers after completion

Without `/var/run/docker.sock` mount:
Analyzers will not execute.

---

# 🔹 SOC WORKFLOW QUESTIONS

---

## 9️⃣ What are analyzers vs responders?

**Answer:**

Analyzers:

* Read-only
* Enrich observables
* Query external data
* Return intelligence

Responders:

* Take action
* Block IP
* Disable account
* Quarantine host
* Trigger automation

Analyzers = Intelligence
Responders = Action

---

## 🔟 What is multi-analyzer correlation?

**Answer:**

Running multiple analyzers on same observable to:

* Compare results
* Identify overlap
* Measure signal quality
* Detect redundancy
* Evaluate service reliability

This helps SOC teams choose production-worthy analyzers.

---

# 🔹 PRACTICAL SCENARIO QUESTIONS

---

## 1️⃣1️⃣ Walk me through real investigation using this integration.

**Answer:**

Scenario: Suspicious IP from SSH brute-force alert.

Steps:

1. Alert converted to case in TheHive
2. IP added as observable
3. Run:

   * MaxMind GeoIP
   * URLScan
   * MISP
   * Passive DNS
4. Cortex executes jobs
5. Results appear inside case
6. Confirm malicious infrastructure
7. Run responder to block IP (optional)
8. All actions logged

Outcome:

* Fast triage
* Evidence-backed decision
* Full audit trail

---

## 1️⃣2️⃣ What are the benefits of this integration in a SOC?

**Answer:**

* Faster investigations
* Reduced manual lookup
* Centralized intelligence
* Consistent workflow
* Compliance-ready documentation
* Foundation for SOAR

It transforms reactive SOC into automated SOC.

---

# 🔹 ADVANCED QUESTIONS

---

## 1️⃣3️⃣ How would you scale Cortex in production?

**Answer:**

Scaling options:

* Increase CPU & RAM
* Separate analyzer worker nodes
* Use multiple Cortex instances
* Connect multiple Cortex servers to TheHive

Cortex scales horizontally.
TheHive scales independently.

---

## 1️⃣4️⃣ Can TheHive connect to multiple Cortex instances?

**Answer:**

Yes.

TheHive supports multiple Cortex connectors.
This enables:

* Environment separation
* Load distribution
* Analyzer grouping

---

## 1️⃣5️⃣ What are common integration mistakes?

**Answer:**

* Not generating API key
* Using superAdmin instead of orgAdmin key
* Not enabling analyzers in Cortex
* Docker socket not mounted
* Ports blocked in security group
* Elasticsearch security misconfiguration

---

# 🔹 BEHAVIORAL / PROJECT QUESTIONS

---

## 1️⃣6️⃣ What did you learn from implementing this?

**Answer:**

* Analyzer lifecycle management
* Docker job orchestration
* API-based integration design
* SOC enrichment architecture
* Correlation strategy
* Audit traceability model
* Production analyzer selection logic

---

## 1️⃣7️⃣ How does this reflect real enterprise SOC design?

**Answer:**

Enterprise SOCs require:

* Centralized case management
* Automated enrichment
* Audit logging
* Role separation
* Scalable execution engines

TheHive + Cortex mirrors this architecture.

It is a realistic SOC enrichment pipeline.

---

# 🔹 SHORT SUMMARY FOR INTERVIEW

If asked to summarize:

> "TheHive manages incidents. Cortex enriches observables and executes responses using Docker-based analyzers. The integration allows analysts to run multi-source threat intelligence queries directly inside case management, reducing manual effort and maintaining full audit traceability."

---

# 🏁 Final Interview Tip

Do not say:
"I installed it."

Say:
"I designed and implemented a centralized SOC enrichment architecture using TheHive and Cortex, enabling automated observable enrichment, Docker-based analyzer execution, API-based integration, and full audit traceability aligned with real enterprise SOC practices."

That changes everything.

---
