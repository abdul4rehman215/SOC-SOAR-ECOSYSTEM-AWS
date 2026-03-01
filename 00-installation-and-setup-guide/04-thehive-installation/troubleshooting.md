# 🛠️ TheHive 5.5 – Troubleshooting Guide (Docker on AWS EC2)

---

# 🧪 Validation Checklist (Run First)

Before troubleshooting, validate:

### ✅ Containers Running
```bash
docker ps
````

Expected containers:

* thehive
* cassandra
* elasticsearch

---

### ✅ Check Container Logs

```bash
docker logs <container_id> --follow
```

---

### ✅ Verify Port 9000 Listening

```bash
sudo ss -tulnp | grep 9000
```

---

### ✅ Access UI

```
http://<EC2_PUBLIC_IP>:9000/
```

---

# 🚨 Most Common Issues (Observed in Real Deployments)

---

# 1️⃣ Elasticsearch Container Fails to Start

## 🔎 Symptoms

* `docker ps` shows elasticsearch restarting
* TheHive container exits
* Logs show permission denied errors

## 📌 Root Cause

Incorrect ownership on elasticsearch data directory.

## ✅ Fix

```bash
cd /opt/TheHive/docker/prod1-thehive

docker compose down

sudo chown -R 1000:1000 elasticsearch
sudo chmod -R 775 elasticsearch

docker compose up -d
```

---

# 2️⃣ Port 9000 Not Accessible

## 🔎 Symptoms

* Browser shows timeout
* Cannot reach TheHive UI

## 📌 Root Cause

Security Group does not allow port 9000.

## ✅ Fix

In AWS Security Group:

Allow:

* Port 9000 (TCP)
* Source: Your Admin IP

---

# 3️⃣ TheHive Container Crashes After Startup

## 🔎 Symptoms

* TheHive container exits immediately
* Logs show memory-related errors

## 📌 Root Cause

Insufficient RAM (less than 16GB recommended).

## ✅ Fix

Upgrade EC2 instance:

* Minimum: 4 vCPU
* Minimum: 16GB RAM

---

# 4️⃣ Cassandra Container Fails

## 🔎 Symptoms

* Cassandra container keeps restarting
* TheHive fails to connect to DB

## 📌 Root Cause

Low memory or corrupted data volume.

## ✅ Fix

```bash
docker compose down
docker volume prune -f
docker compose up -d
```

⚠ This deletes existing data.

---

# 5️⃣ Docker Permission Denied

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

# 6️⃣ Time Synchronization Issues

## 🔎 Symptoms

* Login sessions fail
* Token/session errors

## 📌 Root Cause

Incorrect system time or timezone.

## ✅ Fix

```bash
timedatectl
sudo timedatectl set-ntp yes
```

---

# 7️⃣ Hostname Resolution Issues

## 🔎 Symptoms

* Containers cannot communicate
* Cassandra hostname errors

## 📌 Root Cause

Incorrect `/etc/hosts` configuration.

## ✅ Fix

```bash
sudo nano /etc/hosts
```

Ensure:

```
127.0.1.1 thehive
```

---

# 8️⃣ High CPU Usage

## 🔎 Symptoms

* EC2 instance becomes slow
* Containers lag

## 📌 Root Cause

Elasticsearch indexing load.

## ✅ Mitigation

* Increase instance size
* Use production-grade instance (t3.xlarge or higher)
* Allocate more RAM

---

# 🧠 Advanced Debugging Commands

Check system resources:

```bash
htop
free -h
df -h
```

Check container resource usage:

```bash
docker stats
```

Restart specific container:

```bash
docker restart <container_name>
```

---

# 🔐 Security Best Practices

After installation:

* Change default admin password
* Restrict port 9000 to VPN/Admin IP
* Do NOT expose Elasticsearch
* Enable reverse proxy + HTTPS in production
* Regularly update Docker images

---

# 📌 When to Rebuild Entire Stack

If corruption persists:

```bash
docker compose down -v
docker volume prune -f
docker compose up -d
```

⚠ This removes all stored data.

---

# 🏁 Final Advice

If something breaks:

1. Check `docker ps`
2. Check logs
3. Check memory
4. Check permissions
5. Check security group

In 90% of cases, the issue is:

* Memory shortage
* Permission misconfiguration
* Port blocked

---

End of Troubleshooting Guide.

---
