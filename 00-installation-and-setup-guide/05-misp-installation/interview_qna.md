# 🎤 MISP Deployment – Interview Q&A
### AWS EC2 | Ubuntu 24.04 | Threat Intelligence Core | Feed-Enabled SOC

---

# 1️⃣ What is MISP?

MISP (Malware Information Sharing Platform) is an open-source threat intelligence platform used to collect, store, correlate, and share Indicators of Compromise (IOCs) across organizations.

It transforms raw indicators into structured, machine-readable intelligence.

---

# 2️⃣ Why did you deploy MISP in your SOC architecture?

In my SOC ecosystem:

- Wazuh detects threats
- TheHive manages cases
- Cortex enriches observables
- MISP acts as the intelligence correlation and distribution layer

MISP centralizes threat data and enables structured sharing and automated enrichment.

---

# 3️⃣ What infrastructure did you use and why?

I deployed MISP on:

- AWS EC2
- Instance type: t2.xlarge
- 4 vCPU
- 16GB RAM
- Ubuntu 24.04

Reason:

MISP performs:
- Heavy database operations (MariaDB)
- Correlation indexing
- Background worker processing
- Redis queue handling
- Feed ingestion

16GB RAM ensures stable performance during feed import and correlation.

---

# 4️⃣ What stack does MISP use?

MISP runs on a LAMP stack:

- Linux
- Apache
- MariaDB
- PHP
- Redis
- Python modules

Redis handles caching and background workers.
MariaDB stores events and attributes.

---

# 5️⃣ What are MISP Events and Attributes?

Event:
A container representing a threat incident or intelligence report.

Attribute:
An individual IOC such as:
- IP address
- Domain
- Hash
- URL
- Email

Events contain multiple attributes.

---

# 6️⃣ How does MISP correlation work?

MISP automatically correlates attributes across events.

If two events contain the same IOC:
- MISP links them
- Displays correlation graph
- Shows campaign relationships

Correlation is powered by Redis and background workers.

---

# 7️⃣ What is the purpose of enabling feeds?

Feeds allow MISP to ingest external OSINT intelligence.

Without feeds:
MISP contains no external threat data.

Feeds provide:
- Public IOCs
- Campaign intelligence
- Malware hashes
- Botnet indicators

---

# 8️⃣ Why should you NOT enable all feeds?

Enabling all feeds causes:

- Database explosion
- High CPU usage
- Memory exhaustion
- Redis queue overload
- Slow correlation

Best practice:
Enable only high-quality feeds like CIRCL and Botvrij.

---

# 9️⃣ What filtering did you apply and why?

I applied:

Allowed tags:
- tlp:white
- confidence:high

Timestamp filter:
{"timestamp":"30d"}

Reason:

- Limits events to last 30 days
- Reduces noise
- Prevents database overload
- Follows SOC best practice

---

# 🔟 What does caching a feed do?

Caching:

- Downloads metadata
- Indexes feed
- Does NOT import full events

It prepares feed for safe ingestion.

---

# 1️⃣1️⃣ What does "Fetch and Store" do?

Fetch and Store:

- Imports actual events
- Writes to MariaDB
- Triggers correlation

This should only be done after filtering.

---

# 1️⃣2️⃣ How did you automate feed updates?

I configured cron jobs:

0 * * * * cacheFeed all
30 * * * * fetchFeed all

This ensures:

- Hourly caching
- Hourly fetch
- No manual intervention

Production-ready automation.

---

# 1️⃣3️⃣ How does MISP integrate with TheHive?

When an observable is added in TheHive:

- TheHive queries MISP
- MISP returns correlated intelligence
- Analysts see enrichment automatically

This speeds up investigation.

---

# 1️⃣4️⃣ How does MISP integrate with Wazuh?

MISP exports IOCs in:

- STIX
- JSON
- Snort/Suricata format

These can be consumed by SIEM or IDS for detection.

In my SOC:

MISP feeds intelligence → Wazuh consumes enriched indicators.

---

# 1️⃣5️⃣ What are MISP workers?

Workers handle:

- Correlation
- Feed import
- Email notifications
- Scheduled tasks
- Background processing

If Redis stops, workers fail.

---

# 1️⃣6️⃣ What are common MISP deployment issues?

- Apache not running
- MariaDB failure
- Redis stopped
- BaseURL misconfigured
- Feed overload
- No filtering applied

---

# 1️⃣7️⃣ Why is BaseURL important in AWS?

Default installer sets misp.local.

In AWS:
We must configure public IP or DNS.

Otherwise:
- Redirect errors occur
- SSL mismatch happens
- API calls fail

---

# 1️⃣8️⃣ How would you scale MISP in enterprise?

- Dedicated DB server
- Separate Redis instance
- Load-balanced Apache nodes
- Increased RAM (32GB+)
- Optimized MariaDB configuration
- Worker queue tuning

---

# 1️⃣9️⃣ What security precautions did you implement?

- Restricted Security Group access
- SSL enabled
- Strong admin password
- Feed filtering
- Controlled fetch
- Cron automation

---

# 2️⃣0️⃣ What is a Galaxy in MISP?

A Galaxy is a taxonomy cluster.

Examples:
- MITRE ATT&CK
- Threat Actor groups
- Malware families
- Campaign classifications

Galaxies help structure intelligence.

---

# 2️⃣1️⃣ Why is MISP better than storing IOCs in Excel?

Excel:
- No correlation
- No automation
- No API
- No sharing control

MISP:
- Structured intelligence
- Correlation engine
- Role-based access
- API integrations
- Automated exports

---

# 2️⃣2️⃣ What happens if Redis stops?

- Correlation stops
- Workers fail
- Feed caching fails
- Scheduled jobs break

Redis is critical.

---

# 2️⃣3️⃣ What makes your deployment production-ready?

✔ Proper instance sizing  
✔ Feed filtering applied  
✔ Timestamp restriction  
✔ Cron automation  
✔ SSL enabled  
✔ BaseURL configured  
✔ Workers verified  

---

# 🏁 Final Interview Summary

MISP in my SOC acts as:

- Intelligence ingestion layer
- Correlation engine
- IOC distribution platform
- Enrichment provider for TheHive
- Detection enhancer for SIEM/IDS

It bridges detection and collaborative intelligence sharing.
