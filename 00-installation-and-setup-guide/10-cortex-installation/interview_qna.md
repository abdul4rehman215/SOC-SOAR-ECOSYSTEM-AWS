# 🎓 Interview Questions & Answers - Cortex

> StrangeBee Analysis & Response Engine  
> AWS SOC-SOAR Ecosystem Deployment

---

# 🧠 Basic Conceptual Questions

---

## 1️⃣ What is Cortex?

Cortex is an open-source analysis and response engine developed by StrangeBee (the creators of TheHive).  

It is designed to automate threat intelligence enrichment and active response actions by running analyzers and responders on observables such as IP addresses, domains, URLs, hashes, and files.

Cortex integrates natively with TheHive and exposes a REST API for automation.

---

## 2️⃣ What problem does Cortex solve in a SOC?

Without Cortex:
- Analysts manually check every IOC.
- Intelligence enrichment is slow.
- No automation exists for response actions.

With Cortex:
- Observables are automatically enriched.
- Results are normalized.
- Intelligence is structured.
- Response actions can be automated.

Cortex reduces analyst fatigue and scales investigations.

---

## 3️⃣ What is the difference between an Analyzer and a Responder?

### Analyzer
- Queries external or internal data sources.
- Enriches observables.
- Returns structured JSON output.
- Example: VirusTotal lookup.

### Responder
- Executes an action.
- Performs remediation or automation.
- Example: Block IP in firewall.

Analyzers provide intelligence.  
Responders take action.

---

# 🏗 Architecture Questions

---

## 4️⃣ What are the main components of Cortex?

1. Cortex Application (Web UI + REST API)
2. Elasticsearch backend
3. Docker runtime (for analyzer execution)

Cortex uses Elasticsearch for storing job results and Docker for spawning isolated analyzer containers.

---

## 5️⃣ Why does Cortex require Docker socket mounting?

Cortex dynamically spawns analyzer containers when jobs are executed.

To do this, it needs access to the Docker daemon via:

```

/var/run/docker.sock

```

Without this:
- Analyzers cannot run.
- Jobs fail silently.
- No enrichment occurs.

Docker socket allows Cortex to:
- Start containers
- Stop containers
- Monitor job execution

---

## 6️⃣ Why does Cortex use Elasticsearch?

Elasticsearch is used for:

- Storing analysis jobs
- Indexing results
- Searching historical enrichment
- Managing organization metadata

It provides fast indexing and query capabilities for structured intelligence data.

---

## 7️⃣ How does Cortex isolate analyzer execution?

Each analyzer runs in a separate Docker container.

This ensures:

- Dependency isolation
- Security isolation
- Clean runtime environment
- No cross-contamination between jobs

Containers are destroyed after execution.

---

# 🔐 Security Questions

---

## 8️⃣ What are the Cortex user roles?

### superAdmin
- Global control
- Creates organizations
- Cannot configure analyzers in operational org

### orgAdmin
- Manages users
- Generates API keys
- Enables analyzers
- Configures responders

### analyze
- Can run analyzers

### read
- Can only view reports

Operational work is done inside a dedicated organization.

---

## 9️⃣ Why cannot the default organization be used for operations?

The default organization is reserved for system administration and global management.

It is not designed for operational analyzer configuration.

Best practice:
- Create a dedicated organization.
- Create an orgAdmin.
- Operate within that org.

---

## 🔟 How do you integrate Cortex with TheHive?

Steps:

1. Generate API key in Cortex.
2. Configure Cortex URL inside TheHive.
3. Add API key in TheHive configuration.
4. Test connectivity.

Communication occurs over REST API.

Header format:

```

Authorization: Bearer <API_KEY>

```

---

# ⚙ Operational Questions

---

## 1️⃣1️⃣ How do you verify analyzers are working?

Method 1:
Run analyzer from UI and check:

```

docker ps

```

You should see:

```

cortex-job-xxxxxxxx

```

Method 2:
Check Cortex logs:

```

docker logs cortex --follow

```

If Docker socket is properly mounted, jobs will spawn containers.

---

## 1️⃣2️⃣ What happens if Docker socket is not mounted?

Symptoms:
- Analyzer jobs remain pending.
- No container spawned.
- No enrichment output.

Root cause:
Cortex cannot communicate with Docker daemon.

---

## 1️⃣3️⃣ What happens if Elasticsearch fails?

Symptoms:
- Cortex UI loads partially.
- Jobs cannot be stored.
- Healthcheck failures.

Fix:
- Check Elasticsearch container.
- Verify memory allocation.
- Check permissions.

---

## 📈 Performance & Scaling Questions

---

## 1️⃣4️⃣ Why does Cortex require high RAM?

Because:

- Elasticsearch is memory-intensive.
- Analyzer containers consume memory.
- Multiple concurrent jobs increase load.

Recommended minimum for lab:
16GB RAM.

Production may require more depending on job volume.

---

## 1️⃣5️⃣ How can Cortex scale?

### Vertical Scaling
Increase CPU and RAM.

### Horizontal Scaling
- Multiple Cortex nodes
- Shared Elasticsearch cluster
- Load balancer in front

Enterprise deployments separate:
- Application node
- Analyzer workers
- Elasticsearch cluster

---

# 🔄 Practical SOC Scenario Questions

---

## 1️⃣6️⃣ In a real SOC, how is Cortex used during an investigation?

Example:

1. Wazuh detects suspicious IP.
2. Alert sent to TheHive.
3. Analyst clicks observable.
4. Cortex runs:
   - VirusTotal
   - Shodan
   - AbuseIPDB
5. Results appear in case.
6. If malicious:
   - Responder blocks IP automatically.

This entire process can be automated.

---

## 1️⃣7️⃣ Why is Cortex important for SOAR?

Cortex provides:

- Structured outputs
- API-driven automation
- Modular enrichment
- Response automation

It acts as the execution engine in a SOAR architecture.

---

# 🧠 Advanced Questions

---

## 1️⃣8️⃣ How would you secure Cortex in production?

- Enable Elasticsearch security
- Restrict network exposure
- Use HTTPS
- Rotate API keys
- Protect Docker socket
- Place behind reverse proxy
- Use firewall restrictions

---

## 1️⃣9️⃣ What risks exist with Docker socket mounting?

Docker socket grants control over Docker daemon.

If compromised:
- Attackers could spawn containers
- Modify runtime environment
- Escalate privileges

Mitigation:
- Secure host
- Restrict access
- Monitor Docker activity

---

## 2️⃣0️⃣ Is Cortex a SIEM?

No.

Cortex is:
- Not a log aggregator
- Not a detection engine

It is an:
- Enrichment engine
- Automation engine
- Active response engine

It complements SIEM and case management tools.

---

# 🏁 Final Summary

Cortex enables:

- Automated enrichment
- Active response
- Scalable investigations
- Structured intelligence
- SOC automation workflows

It transforms manual intelligence lookups into automated, repeatable workflows.

In a modern SOC:
Cortex is the automation brain.

---
