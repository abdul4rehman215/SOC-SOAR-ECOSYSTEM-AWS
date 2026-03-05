# 🎤 Interview Q&A - TheHive 5.5 Deployment
### Docker on AWS EC2 | SOC-SOAR Case Management Core

---

# 1️⃣ What is TheHive?

TheHive is an open-source Security Incident Response Platform used for managing alerts, investigations, cases, tasks, and observables in a SOC environment.

It converts raw alerts into structured investigation workflows.

---

# 2️⃣ Why did you deploy TheHive in your SOC architecture?

In my SOC ecosystem:

- Wazuh → Detects threats
- MISP → Provides threat intelligence
- Cortex → Performs enrichment
- TheHive → Manages incident lifecycle

TheHive acts as the case management backbone.

---

# 3️⃣ What infrastructure did you use?

AWS EC2 deployment:

- Instance type: t2.xlarge
- 4 vCPU
- 16GB RAM
- Ubuntu 24.04
- Docker-based deployment

16GB RAM is required because:

- Elasticsearch indexing consumes memory
- Cassandra requires heap allocation
- TheHive JVM needs stable memory

---

# 4️⃣ Why Docker instead of manual installation?

Docker ensures:

- Environment consistency
- Easy service orchestration
- Faster deployment
- Simplified troubleshooting
- Isolation between services

It is production-aligned for SOC stacks.

---

# 5️⃣ What components run inside TheHive Docker stack?

- TheHive application
- Cassandra (database)
- Elasticsearch (index engine)

All run as containers and communicate internally.

---

# 6️⃣ Why is Cassandra used?

Cassandra is used for:

- Storing cases
- Storing observables
- Storing tasks
- Maintaining audit trails

It supports distributed, scalable storage.

---

# 7️⃣ Why is Elasticsearch required?

Elasticsearch is used for:

- Fast search indexing
- Querying observables
- Filtering alerts
- Dashboard performance

Without Elasticsearch, searching becomes slow.

---

# 8️⃣ Why must default credentials be changed immediately?

Default:

- admin / secret

If left unchanged:

- Anyone accessing port 9000 could compromise the SOC
- API misuse risk
- Case data exposure

Changing default password is mandatory.

---

# 9️⃣ Why create a new organization instead of using default?

Best practice:

- Separate global admin from operational users
- Enable multi-tenant capability
- Maintain RBAC (Role-Based Access Control)
- Support future team expansion

Global admin should not be used for daily operations.

---

# 🔟 What is an org-admin in TheHive?

An org-admin:

- Manages users within the organization
- Creates cases
- Assigns tasks
- Manages observables
- Controls organization-level permissions

Super-admin controls platform.
Org-admin controls SOC operations.

---

# 1️⃣1️⃣ What are observables?

Observables are indicators attached to cases.

Examples:

- IP addresses
- Domains
- File hashes
- Email addresses
- URLs

They can be enriched via Cortex or correlated with MISP.

---

# 1️⃣2️⃣ How does TheHive integrate with MISP?

When an observable is added:

- TheHive queries MISP
- MISP returns related intelligence
- Analyst sees enrichment data

This speeds up investigation.

---

# 1️⃣3️⃣ How does TheHive integrate with Cortex?

Cortex provides:

- Automated analyzers
- Threat intelligence lookups
- Malware scanning
- Reputation scoring

TheHive triggers Cortex analyzers automatically or manually.

---

# 1️⃣4️⃣ What is the incident workflow in TheHive?

Typical workflow:

Alert → Triage → Convert to Case → Assign Tasks → Add Observables → Enrich → Investigate → Close Case → Report

---

# 1️⃣5️⃣ Why restrict port 9000 in AWS?

Port 9000 exposes the case management interface.

If open publicly:

- Attackers could brute force login
- Data leakage risk
- SOC compromise

Security Group should restrict access to Admin IP or VPN.

---

# 1️⃣6️⃣ What are common deployment failures?

- Elasticsearch permission errors
- Cassandra memory issues
- Port 9000 blocked
- Docker permission denied
- Time synchronization problems
- Incorrect organization role setup

---

# 1️⃣7️⃣ Why is time synchronization important?

TheHive uses token-based sessions.

If system time is incorrect:

- Session invalidation
- Login failures
- API authentication errors

NTP must be enabled.

---

# 1️⃣8️⃣ What happens if Elasticsearch fails?

- Case search becomes unavailable
- Observables cannot be indexed
- UI may crash
- Investigation speed drops

Elasticsearch is critical for performance.

---

# 1️⃣9️⃣ What happens if Cassandra fails?

- Case data unavailable
- TheHive cannot start
- Data loss risk if volumes corrupted

Cassandra is primary datastore.

---

# 2️⃣0️⃣ How would you scale TheHive?

Enterprise scaling:

- Separate Cassandra cluster
- Separate Elasticsearch cluster
- Dedicated reverse proxy (NGINX)
- TLS termination
- Increased RAM (32GB+)
- Multi-node deployment

---

# 2️⃣1️⃣ What security controls did you implement?

✔ Changed default password  
✔ Created organization-based RBAC  
✔ Restricted Security Group access  
✔ Docker isolation  
✔ Time sync enabled  

---

# 2️⃣2️⃣ Why is TheHive important in SOC maturity?

Without TheHive:

- Alerts remain disconnected
- No case tracking
- No structured investigation
- No audit trail

With TheHive:

- Structured workflows
- Collaboration
- Task assignment
- Intelligence enrichment
- Reporting capability

---

# 🏁 Final Interview Summary

TheHive in my SOC:

- Converts detection into investigation
- Centralizes incident lifecycle
- Integrates with MISP and Cortex
- Enables structured case management
- Provides auditability and collaboration

It is the operational heart of the SOC-SOAR ecosystem.
