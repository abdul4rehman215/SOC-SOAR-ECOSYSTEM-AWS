# 🐳 Docker Installation – Troubleshooting Guide  
### SOC-SOAR Ecosystem Container Runtime Issues

---

## 📌 Overview

This document outlines common issues encountered during Docker installation on Ubuntu 22.04 / 24.04 and their resolutions.

Docker installation failures are typically caused by:

- GPG key misconfiguration
- Repository misconfiguration
- DNS / network instability
- Permission issues
- Interrupted package installation

---

# 🔐 1️⃣ NO_PUBKEY Error During apt update

## ❌ Symptoms

```bash
NO_PUBKEY XXXXXXXX
The repository is not signed.
````

---

## 🔍 Root Cause

* Docker GPG key not imported correctly
* Incorrect permissions on `/etc/apt/keyrings/docker.gpg`
* Repository pointing to wrong key location

---

## 🛠️ Diagnostics

```bash
ls -l /etc/apt/keyrings/docker.gpg
cat /etc/apt/sources.list.d/docker.list
```

---

## ✅ Fix

Re-import key properly:

```bash
sudo rm -f /etc/apt/keyrings/docker.gpg
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt update
```

---

# 🌐 2️⃣ apt update Fails (Temporary Failure Resolving)

## ❌ Symptoms

```bash
Temporary failure resolving 'download.docker.com'
```

---

## 🔍 Root Cause

* DNS not working
* Internet gateway missing
* Route table misconfigured
* Outbound traffic blocked

---

## 🛠️ Diagnostics

```bash
ping 8.8.8.8
curl https://google.com
cat /etc/resolv.conf
```

---

## ✅ Fix

Verify:

* Internet Gateway attached
* Route table contains `0.0.0.0/0 → IGW`
* DNS resolution enabled in VPC
* Security group outbound rule allows `0.0.0.0/0`

---

# 🔒 3️⃣ Permission Denied When Running Docker

## ❌ Symptoms

```bash
Got permission denied while trying to connect to the Docker daemon socket
```

---

## 🔍 Root Cause

* User not added to docker group
* Session not reloaded

---

## 🛠️ Fix

```bash
sudo usermod -aG docker $USER
newgrp docker
```

If still failing:

Logout and log back in.

Verify group:

```bash
groups
```

You should see `docker` listed.

---

# 🛑 4️⃣ Docker Service Not Starting

## ❌ Symptoms

```bash
docker: command not found
or
Failed to start docker.service
```

---

## 🔍 Root Cause

* Installation interrupted
* containerd not installed
* Service not enabled

---

## 🛠️ Diagnostics

```bash
sudo systemctl status docker
sudo journalctl -xeu docker.service
```

---

## ✅ Fix

Restart service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl enable docker
```

If still failing:

```bash
sudo apt install --reinstall docker-ce docker-ce-cli containerd.io
```

---

# 📦 5️⃣ Docker Compose Command Not Found

## ❌ Symptoms

```bash
docker-compose: command not found
```

---

## 🔍 Root Cause

Modern Docker uses:

```bash
docker compose
```

NOT:

```bash
docker-compose
```

---

## ✅ Fix

Verify plugin installed:

```bash
docker compose version
```

If missing:

```bash
sudo apt install docker-compose-plugin
```

---

# 🐳 6️⃣ hello-world Container Fails

## ❌ Symptoms

```bash
Cannot connect to the Docker daemon
```

---

## 🔍 Root Cause

* Docker daemon not running
* Network issue preventing image pull
* Permission issue

---

## 🛠️ Diagnostics

```bash
sudo systemctl status docker
docker info
```

---

## ✅ Fix

Start daemon:

```bash
sudo systemctl start docker
```

If image pull fails:

Check internet:

```bash
ping 8.8.8.8
curl https://registry-1.docker.io
```

---

# 🔄 7️⃣ Interrupted Docker GPG Key Import

## ❌ Symptoms

* apt update hangs
* repository not signed error persists

---

## 🔍 Root Cause

Key import was interrupted mid-process.

---

## ✅ Fix

Remove and re-add key:

```bash
sudo rm -f /etc/apt/keyrings/docker.gpg
sudo apt clean
sudo apt update
```

Re-import key properly.

---

# 🗄️ 8️⃣ Disk Space Issues During Installation

## ❌ Symptoms

```bash
No space left on device
```

---

## 🛠️ Diagnostics

```bash
df -h
```

---

## ✅ Fix

Clean apt cache:

```bash
sudo apt clean
sudo apt autoremove -y
```

If still low:

Resize EBS volume from AWS console.

---

# 🔥 9️⃣ Port Conflicts After Installation

## ❌ Symptoms

Containers fail to start due to port binding errors.

---

## 🛠️ Diagnostics

```bash
sudo ss -tulnp
```

---

## ✅ Fix

Stop conflicting service:

```bash
sudo systemctl stop service-name
```

Or change container port mapping.

---

# 🧠 10️⃣ Docker Consumes High Memory

## 🔍 Explanation

Docker uses:

* containerd
* overlay2 storage
* background daemon

On low RAM systems (<2GB) performance may degrade.

---

## ✅ Recommendation

Minimum recommended for SOC stack:

* 8GB RAM
* 100GB disk

---

# 🏁 Troubleshooting Strategy

Always check in this order:

1️⃣ Internet connectivity
2️⃣ DNS resolution
3️⃣ GPG key validation
4️⃣ Repository configuration
5️⃣ Docker service status
6️⃣ User group membership
7️⃣ Disk space
8️⃣ Port conflicts

---

## ✅ Final Validation Checklist

✔ docker --version works
✔ docker compose version works
✔ docker run hello-world successful
✔ docker info shows no errors
✔ docker service active and enabled

---

## 🧠 Key Takeaway

Stable Docker installation is critical for:

* TheHive deployment
* Cortex analyzers
* MISP container stack
* n8n automation workflows
* Microservice SOC architecture

Improper Docker installation leads to cascading failures across the SOC ecosystem.

---

## 📌 Status

Docker environment validated and ready for containerized SOC tool deployment.

---
