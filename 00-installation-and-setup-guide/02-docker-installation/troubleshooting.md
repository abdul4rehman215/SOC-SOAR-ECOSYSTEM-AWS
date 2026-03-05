# 🛠️ Troubleshooting Guide — Docker Installation Guide (Ubuntu / AWS EC2)

> This guide covers common Docker installation and runtime issues on Ubuntu (especially on AWS EC2).  
> Focus is on **GPG key issues, repository issues, daemon issues, permissions, and network/DNS problems**.

---

## 📌 Quick Fix Flow (Use This First)

### 1) Check internet + DNS
```bash
ping -c 2 8.8.8.8
curl -I https://google.com
````

### 2) Check Docker service status

```bash
sudo systemctl status docker --no-pager
```

### 3) Check if user is in docker group

```bash
id -nG $USER
getent group docker
```

### 4) Test Docker quickly

```bash
docker --version
docker compose version
docker run hello-world
```

---

# 🔑 GPG KEY / REPOSITORY ISSUES

---

## 1) ❌ `apt update` shows `NO_PUBKEY` (Docker repo not trusted)

### Symptoms

* During `sudo apt update`, errors like:

  * `NO_PUBKEY ...`
  * `The following signatures couldn't be verified`
  * `repository is not signed`

### Root Causes

* GPG key not saved to correct location
* Key permissions incorrect (APT can’t read it)
* Repository file references wrong keyring path

### Fix (Reinstall key properly)

```bash
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

ls -l /etc/apt/keyrings/docker.gpg
```

Then re-add repository:

```bash
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null <<EOF
deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable
EOF
```

Update again:

```bash
sudo apt clean
sudo apt update
```

---

## 2) ❌ `repository is not signed` / APT refuses Docker repo

### Symptoms

* APT blocks repo and refuses packages

### Root Causes

* Wrong repo line format
* Keyring path mismatch
* Broken repo file content

### Fix (Inspect the repo file)

```bash
cat /etc/apt/sources.list.d/docker.list
```

It should look like:

```text
deb [arch=<arch> signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu <codename> stable
```

Check codename:

```bash
lsb_release -cs
```

Then:

```bash
sudo apt update
```

---

## 3) ❌ `GPG error` / `docker.gpg` exists but still fails

### Root Causes

* File permissions wrong
* Corrupted key file due to interrupted download

### Fix

Recreate the key file:

```bash
sudo rm -f /etc/apt/keyrings/docker.gpg

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt update
```

---

# 🐳 DOCKER INSTALLATION / SERVICE ISSUES

---

## 4) ❌ Docker installed but daemon not running

### Symptoms

* `docker ps` fails
* error: `Cannot connect to the Docker daemon`

### Fix

Start and enable Docker:

```bash
sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl status docker --no-pager
```

Check logs if failing:

```bash
sudo journalctl -u docker --no-pager -n 200
```

---

## 5) ❌ `Cannot connect to the Docker daemon` even though service is running

### Root Causes

* Permissions issue accessing `/var/run/docker.sock`
* User not in docker group
* Session not refreshed

### Fix

Check socket permissions:

```bash
ls -l /var/run/docker.sock
```

Add user to docker group:

```bash
sudo usermod -aG docker $USER
```

Apply group changes:

```bash
newgrp docker
```

Test:

```bash
docker ps
docker run hello-world
```

If still failing, log out and log back in.

---

## 6) ❌ `permission denied` when running docker commands

### Symptoms

* `permission denied while trying to connect to the Docker daemon socket`

### Fix

```bash
sudo usermod -aG docker $USER
newgrp docker
id -nG $USER
```

Ensure docker group exists:

```bash
getent group docker
```

---

# 🌐 NETWORK / DNS / AWS EC2 SPECIFIC ISSUES

---

## 7) ❌ Docker GPG download fails / curl fails

### Symptoms

* `curl: (6) Could not resolve host`
* `curl: (7) Failed to connect`
* timeouts

### Root Causes

* No internet (IGW/route table issue)
* DNS not working (VPC DNS disabled)
* Outbound restricted (SG/NACL)

### Fix (EC2 network validation)

```bash
ip route
ping -c 2 8.8.8.8
curl -I https://google.com
```

If 8.8.8.8 fails → check VPC + route table + IGW.
If 8.8.8.8 works but google fails → DNS issue (enable VPC DNS).

---

## 8) ❌ `docker run hello-world` fails due to image pull issues

### Symptoms

* Cannot pull from registry
* DNS resolution issues
* TLS handshake errors

### Fix

Check connectivity to Docker registry:

```bash
curl -I https://registry-1.docker.io
```

Try a different network test:

```bash
ping -c 2 1.1.1.1
```

Restart Docker:

```bash
sudo systemctl restart docker
```

Retry:

```bash
docker run hello-world
```

---

# 🧩 COMPOSE ISSUES

---

## 9) ❌ `docker compose` not found

### Symptoms

* `docker: 'compose' is not a docker command`

### Root Causes

* Compose plugin not installed
* Older Docker packages

### Fix

Install the compose plugin:

```bash
sudo apt update
sudo apt install -y docker-compose-plugin
```

Verify:

```bash
docker compose version
```

---

# ✅ FINAL DIAGNOSTIC COMMANDS (COPY/PASTE)

Run these and inspect outputs:

```bash
ping -c 2 8.8.8.8
curl -I https://google.com
sudo apt update
ls -l /etc/apt/keyrings/docker.gpg
cat /etc/apt/sources.list.d/docker.list
sudo systemctl status docker --no-pager
docker --version
docker compose version
id -nG $USER
ls -l /var/run/docker.sock
docker run hello-world
```

---

## ✅ Final Notes

* Most Docker install failures come from:

  * DNS/network issues on EC2
  * GPG key not readable by APT
  * repository file not correctly configured
  * user permissions not applied (docker group)

Once Docker is stable, SOC/SOAR tools can be deployed reliably with fewer dependency issues.

---
