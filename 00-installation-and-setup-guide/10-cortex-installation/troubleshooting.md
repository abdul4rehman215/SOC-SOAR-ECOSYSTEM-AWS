# 🛠️ Cortex – Troubleshooting Guide

> StrangeBee Analysis & Response Engine
> Docker Deployment on AWS EC2

---

# 🧪 Initial Validation Checklist (Run First)

Before deep troubleshooting, verify:

### ✅ Containers Running

```bash
docker ps
````

Expected containers:

* cortex
* elasticsearch

---

### ✅ Check Cortex Logs

```bash
docker logs cortex --follow
```

---

### ✅ Check Elasticsearch Logs

```bash
docker logs elasticsearch --follow
```

---

### ✅ Verify Port 9001 Listening

```bash
sudo ss -tulnp | grep 9001
```

---

### ✅ Access Web UI

```
http://<EC2_PUBLIC_IP>:9001
```

If all above passes, Cortex should be operational.

---

# 🚨 Common Issues & Fixes

---

# 1️⃣ Elasticsearch Container Keeps Restarting

## 🔎 Symptoms

* `docker ps` shows elasticsearch restarting
* Cortex container unhealthy
* Healthcheck failing
* Logs show permission denied

## 📌 Root Cause

Incorrect ownership of elasticsearch directory.

## ✅ Fix

```bash
cd /opt/Cortex/docker/prod1-cortex

docker compose down

sudo chown -R 1000:1000 elasticsearch
sudo chmod -R 775 elasticsearch

docker compose up -d
```

---

# 2️⃣ Cortex Healthcheck Fails

## 🔎 Symptoms

* Cortex container shows "unhealthy"
* UI not accessible
* docker ps shows restarting

## 📌 Root Cause

Default healthcheck too strict.

## ✅ Fix

Edit docker-compose.yml and replace Cortex healthcheck with:

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -s http://localhost:9001 || exit 1"]
  interval: 30s
  timeout: 5s
  retries: 10
  start_period: 180s
```

Restart:

```bash
docker compose down
docker compose up -d
```

---

# 3️⃣ Port 9001 Not Accessible

## 🔎 Symptoms

* Browser timeout
* Cannot reach Cortex UI

## 📌 Root Cause

Security Group not allowing port 9001.

## ✅ Fix

In AWS Security Group:

Allow:

* Port 9001 (TCP)
* Source: Your Admin IP

---

# 4️⃣ Analyzer Jobs Not Running

## 🔎 Symptoms

* Analyzer stuck in "Waiting"
* No Docker container spawned
* No enrichment result

## 📌 Root Cause

Docker socket not mounted.

## ✅ Fix

Ensure docker-compose.yml contains:

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

Restart containers:

```bash
docker compose down
docker compose up -d
```

---

# 5️⃣ Docker Permission Denied Error

## 🔎 Symptoms

```
permission denied while trying to connect to Docker daemon
```

## 📌 Root Cause

User not added to docker group.

## ✅ Fix

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

# 6️⃣ Database Update Button Not Working

## 🔎 Symptoms

* Update Database button fails
* UI stuck on maintenance page

## 📌 Root Cause

Elasticsearch not ready.

## ✅ Fix

Check Elasticsearch container:

```bash
docker logs elasticsearch
```

If unhealthy:

* Fix permissions
* Increase memory
* Restart containers

---

# 7️⃣ High Memory Usage

## 🔎 Symptoms

* EC2 instance becomes slow
* Containers crash
* OOM errors

## 📌 Root Cause

Insufficient RAM.

## ✅ Fix

Minimum recommended:

* 4 vCPU
* 16GB RAM

Check memory:

```bash
free -h
```

---

# 8️⃣ Analyzer Returns Error (API Failure)

## 🔎 Symptoms

* Analyzer runs but shows failed
* API error returned

## 📌 Root Cause

Missing or invalid API key.

## ✅ Fix

Go to:
Organization → Analyzers

Verify:

* API key configured
* Rate limit correct
* Key valid

---

# 9️⃣ Elasticsearch Healthcheck Fails

## 🔎 Symptoms

* Container unhealthy
* Healthcheck timeout

## 📌 Fix

Replace Elasticsearch healthcheck with:

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -f -s http://elasticsearch:9200/_cat/health || exit 1"]
  start_period: 40s
  interval: 5s
  timeout: 2s
  retries: 10
```

Restart stack.

---

# 🔟 Cannot Create Organization

## 🔎 Symptoms

* Organization tab inaccessible
* Permission denied

## 📌 Root Cause

Logged in with wrong role.

## ✅ Fix

Login with superAdmin account.
Only superAdmin can create organizations.

---

# 1️⃣1️⃣ API Key Not Working with TheHive

## 🔎 Symptoms

* TheHive cannot connect
* 401 Unauthorized

## 📌 Fix

Verify header format:

```
Authorization: Bearer <API_KEY>
```

Ensure:

* No extra spaces
* Key copied correctly
* Using orgAdmin key

---

# 1️⃣2️⃣ Analyzer Container Not Spawning

## 🔎 Test

Run analyzer from UI.

Then:

```bash
docker ps
```

You should briefly see:

```
cortex-job-xxxxxxx
```

If not:

* Docker socket issue
* Permission issue
* Docker not running

---

# 🧠 Advanced Debug Commands

Check system resources:

```bash
htop
free -h
df -h
```

Check Docker resource usage:

```bash
docker stats
```

Restart specific container:

```bash
docker restart cortex
docker restart elasticsearch
```

---

# 🔐 Security Hardening Recommendations

After successful deployment:

* Restrict port 9001 to Admin IP
* Do not expose Elasticsearch
* Rotate API keys regularly
* Use HTTPS via reverse proxy
* Monitor Docker activity
* Secure Docker socket

---

# 🏁 When to Rebuild Entire Stack

If corruption persists:

```bash
docker compose down -v
docker volume prune -f
docker compose up -d
```

⚠ WARNING: This deletes stored data.

---

# 🧠 Final Troubleshooting Logic

When Cortex fails:

1. Check docker ps
2. Check logs
3. Check Elasticsearch
4. Check permissions
5. Check Docker socket
6. Check memory
7. Check Security Group

In 90% of cases, the issue is:

* Permission misconfiguration
* Insufficient RAM
* Docker socket not mounted
* Port blocked

---

END OF TROUBLESHOOTING GUIDE

---
