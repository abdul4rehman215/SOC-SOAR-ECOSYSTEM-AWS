# Advanced Troubleshooting Guide - TheHive ↔ Cortex Integration 
### AWS EC2 | Docker Deployment | SOC Enrichment Architecture

---

# 🧪 FIRST — Quick Validation Checklist

Before deep debugging, always validate:

### ✅ TheHive UI Accessible

`http://<THEHIVE_IP>:9000`

### ✅ Cortex UI Accessible

`http://<CORTEX_IP>:9001`

### ✅ Docker Containers Running

```bash
docker ps
```

You should see:

* thehive
* cassandra
* elasticsearch (TheHive)
* cortex
* elasticsearch (Cortex)

---

### ✅ Cortex Connector Status (In TheHive)

Go to:

Platform Management → Connectors → Cortex

Status must show:
🟢 **OK**

If not, continue below.

---

# 1️⃣ Cortex Connector Shows RED / Not Connected

## 🔎 Symptoms

* TheHive connector status is red
* Cannot see analyzers in TheHive
* “Connection refused” error

---

## 📌 Root Causes

* Incorrect API key
* Wrong Cortex URL
* Cortex container not running
* Port 9001 blocked
* SSL misconfiguration

---

## ✅ Fix

### Step 1 — Verify Cortex Port

```bash
sudo ss -tulnp | grep 9001
```

If nothing shows → Cortex not listening.

---

### Step 2 — Verify API Key

In Cortex:

Organization → Users → Create API Key
Copy immediately.

Test manually:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:9001/api/user
```

If 401 → Wrong key.

---

### Step 3 — Verify URL in TheHive

Correct format inside Docker network:

```
http://cortex:9001
```

Not:

```
http://localhost:9001
```

(When both are in Docker Compose)

---

# 2️⃣ Analyzers Not Visible in TheHive

## 🔎 Symptoms

* No analyzers listed under:
  Entities Management → Analyzer Templates
* “No analyzer available” message

---

## 📌 Root Causes

* Analyzers not enabled in Cortex
* Using default Cortex organization
* Logged in with wrong org user
* API key from wrong organization

---

## ✅ Fix

### Step 1 — Login as orgAdmin in Cortex

Go to:

Organization → Analyzers

Enable required analyzers.

---

### Step 2 — Confirm User Role

User must belong to same organization that has analyzers enabled.

---

### Step 3 — Refresh Connector

In TheHive:

Platform Management → Connectors → Cortex
Save again → Confirm green status.

---

# 3️⃣ Analyzer Runs But No Output

## 🔎 Symptoms

* Analyzer job completes
* No structured result
* Raw JSON empty

---

## 📌 Root Causes

* Observable not supported by analyzer
* API quota exceeded
* Invalid external API key
* Service returned no data

---

## ✅ Fix

### Check Cortex Job History

Cortex → Jobs

Inspect:

* Execution status
* Error logs
* Response body

---

### Test External API Manually

Example (MaxMind or URLScan):

Try query directly on vendor website.

If vendor blocks or rate limits → expected.

---

# 4️⃣ Analyzer Fails Immediately

## 🔎 Symptoms

* Job fails instantly
* Error: Docker unavailable
* Error: Cannot connect to Docker daemon

---

## 📌 Root Cause

Docker socket not mounted.

---

## ✅ Fix

In `docker-compose.yml` for Cortex ensure:

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

Restart:

```bash
docker compose down
docker compose up -d
```

---

# 5️⃣ Cortex Job Containers Not Spawning

## 🔎 Symptoms

* Analyzer triggered
* No `cortex-job-xxxx` container appears

---

## Check

```bash
docker ps -a | grep cortex-job
```

---

## Possible Causes

* Docker permission issue
* Incorrect UID ownership
* Low memory
* CPU starvation

---

## Fix Permissions

```bash
sudo chown -R 1000:1000 elasticsearch cortex
sudo chmod -R 775 elasticsearch cortex
```

---

# 6️⃣ High CPU / System Slow After Running Multiple Analyzers

## 🔎 Symptoms

* EC2 becomes slow
* Docker high CPU
* Cassandra lag

---

## 📌 Root Cause

Too many analyzers running simultaneously.

Each analyzer = Docker container.

---

## ✅ Fix

* Enable only high-value analyzers
* Increase EC2 size
* Limit concurrent jobs
* Avoid bulk execution on large observable sets

---

# 7️⃣ “Unauthorized” API Errors

## 🔎 Symptoms

* 401 Unauthorized
* Bearer token rejected

---

## Root Causes

* Using superAdmin key incorrectly
* Key expired
* Typo in key
* Organization mismatch

---

## Fix

Regenerate API key:

Organization → Users → Create API Key
Copy immediately.

Update in TheHive connector.

---

# 8️⃣ Analyzer Works in Cortex But Not Visible in TheHive

## Explanation

TheHive only sees analyzers enabled under the organization tied to the API key.

If analyzer enabled under different org → not visible.

---

## Fix

Ensure:

* Analyzer enabled under same org
* API key generated from that org
* User role correct

---

# 9️⃣ Elasticsearch Errors in Cortex

## 🔎 Symptoms

* Cortex fails to start
* Healthcheck failing
* Analyzer stuck in pending

---

## Fix

Ensure Elasticsearch security disabled:

Remove:

```
xpack.security.enabled=true
```

Use:

```
xpack.security.enabled=false
```

Restart containers.

---

# 🔟 Case Timeline Does Not Show Analyzer Result

## Possible Reasons

* Analyzer still running
* Job failed
* TLP restrictions
* PAP restrictions
* Extract observables disabled

---

## Fix

In Cortex analyzer configuration:

Enable:

* Extract observables
* Allow TLP/PAP levels used in TheHive

---

# 1️⃣1️⃣ Multi-Analyzer Correlation Issues

## Symptom

Different analyzers give conflicting data.

## Explanation

This is normal.

Each service:

* Uses different databases
* Updates at different intervals
* Applies different scoring logic

SOC lesson:
Correlation improves confidence — not consistency.

---

# 1️⃣2️⃣ SSL / HTTPS Issues

If using HTTPS:

* Disable hostname verification (for lab only)
* Or configure proper reverse proxy
* Ensure certificates trusted

Never expose plain ports publicly in production.

---

# 1️⃣3️⃣ Memory Issues (Common on AWS)

Minimum recommended:

4 vCPU
16 GB RAM

If below:

* Cassandra unstable
* Analyzer jobs fail
* Elasticsearch crashes

Check:

```bash
free -h
docker stats
```

---

# 🔎 Log Locations Summary

### TheHive

```bash
docker logs thehive
```

### Cortex

```bash
docker logs cortex
```

### Cassandra

```bash
docker logs cassandra
```

### Elasticsearch

```bash
docker logs elasticsearch
```

---

# 🧠 Real-World SOC Lessons From Failures

During integration testing, common observations:

* Not all analyzers return results
* Some APIs rate-limit heavily
* Redundant analyzers increase noise
* High-value analyzers should be prioritized
* Logging & audit visibility are critical

Failure handling is part of SOC maturity.

---

# 🏁 Final Integration Health Checklist

- ✔ TheHive UI accessible
- ✔ Cortex UI accessible
- ✔ API key valid
- ✔ Connector status green
- ✔ Analyzers enabled
- ✔ Analyzer visible in TheHive
- ✔ Analyzer job container spawns
- ✔ Results visible in case
- ✔ Job recorded in Cortex
- ✔ Resource usage stable

If all above pass →
Your enrichment pipeline is production-ready.

---

# 🔐 Final Advice

Most integration problems fall into:

1. Wrong API key
2. Docker socket missing
3. Analyzer not enabled
4. Organization mismatch
5. Port blocked
6. Memory shortage

90% of issues are solved by checking those six.

---
