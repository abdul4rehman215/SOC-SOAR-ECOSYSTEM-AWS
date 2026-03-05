# 🛠️ Troubleshooting Guide - TheHive 5.5

### Docker Deployment on AWS EC2 | SOC-SOAR Case Management Core

---

# 🧪 Validation Checklist (Run First)

Before troubleshooting anything, validate these:

### ✅ Containers Running

```bash
docker ps
```

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

# 🚨 Most Common Issues (Real Deployment Scenarios)

---

# 1️⃣ Elasticsearch Container Fails to Start

## 🔎 Symptoms

* elasticsearch restarting continuously
* thehive container exits
* Permission denied in logs

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

* Browser timeout
* Cannot reach TheHive

## 📌 Root Cause

AWS Security Group not allowing port 9000.

## ✅ Fix

Allow in Security Group:

* Port: 9000 (TCP)
* Source: Your Admin IP or VPN only

---

# 3️⃣ TheHive Container Crashes (Memory Issue)

## 🔎 Symptoms

* Container exits
* Logs show JVM memory errors

## 📌 Root Cause

Insufficient RAM.

## ✅ Required Minimum

* 4 vCPU
* 16GB RAM

Upgrade EC2 if below this.

---

# 4️⃣ Cassandra Container Fails

## 🔎 Symptoms

* Cassandra restarting
* TheHive cannot connect

## 📌 Root Cause

Low memory or corrupted volume.

## ✅ Fix

```bash
docker compose down
docker volume prune -f
docker compose up -d
```

⚠ This deletes stored data.

---

# 5️⃣ Cannot Login After First Login

## 🔎 Symptoms

* Password rejected
* Login loops
* Session expired

## 📌 Root Cause

Default password not changed properly
OR
Timezone mismatch

## ✅ Fix

Check time sync:

```bash
timedatectl
sudo timedatectl set-ntp yes
```

Restart containers:

```bash
docker compose restart
```

---

# 6️⃣ Org-Admin User Cannot See Cases

## 🔎 Symptoms

* Login successful
* No cases visible
* Dashboard empty

## 📌 Root Cause

Logged into wrong organization
OR
Permission profile incorrect

## ✅ Fix

1. Check active organization (top-right corner)
2. Verify profile = `org-admin`
3. Ensure profile includes:

   * manageCase
   * manageTask
   * manageObservable

---

# 7️⃣ Organization Not Visible

## 🔎 Symptoms

* Only default org visible
* Cannot switch organizations

## 📌 Root Cause

User not assigned to organization.

## ✅ Fix (As Super Admin)

1. Go to **Users**
2. Edit user
3. Add organization
4. Assign profile
5. Set as default org

Logout and login again.

---

# 8️⃣ Cannot Create New User

## 🔎 Symptoms

* Add user button disabled
* Permission denied

## 📌 Root Cause

User does not have `manageUser` permission.

## ✅ Fix

Use:

* Global admin
  OR
* Org-admin with manageUser profile

---

# 9️⃣ Elasticsearch High CPU Usage

## 🔎 Symptoms

* EC2 slow
* docker stats shows high CPU

## 📌 Root Cause

Heavy indexing or insufficient RAM.

## ✅ Mitigation

* Increase RAM
* Restart Elasticsearch container
* Avoid large bulk imports

---

# 🔟 Docker Permission Denied

## 🔎 Symptoms

```
permission denied while trying to connect to Docker daemon
```

## 📌 Root Cause

User not in docker group.

## ✅ Fix

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

# 1️⃣1️⃣ Hostname Issues (Container Communication Failure)

## 🔎 Symptoms

* Cassandra hostname errors
* Internal service resolution fails

## 📌 Root Cause

Incorrect /etc/hosts

## ✅ Fix

```bash
sudo nano /etc/hosts
```

Ensure:

```
127.0.1.1 thehive
```

---

# 1️⃣2️⃣ Session Token Errors

## 🔎 Symptoms

* Random logout
* Invalid session
* API auth failures

## 📌 Root Cause

Time skew between host and containers.

## ✅ Fix

```bash
timedatectl set-ntp yes
docker compose restart
```

---

# 🧠 Advanced Debugging

Check system:

```bash
htop
free -h
df -h
```

Check container usage:

```bash
docker stats
```

Restart specific container:

```bash
docker restart thehive
```

---

# 🔐 Security Validation After Deployment

- ✔ Default password changed
- ✔ Organization created
- ✔ Org-admin user created
- ✔ Port 9000 restricted
- ✔ Docker group permissions set
- ✔ Time synchronization enabled

---

# 🏗 When to Rebuild Entire Stack

If corrupted beyond recovery:

```bash
docker compose down -v
docker volume prune -f
docker compose up -d
```

⚠ All cases will be deleted.

---

# 🏁 Final Diagnostic Order

When something breaks:

1. docker ps
2. docker logs
3. Check memory
4. Check permissions
5. Check security group
6. Check organization & user role

90% of issues are:

* Memory shortage
* Permission misconfiguration
* Wrong org role
* Port blocked

---
