# 🐳 Docker Installation Guide (Ubuntu 24.04 LTS)
### SOC-SOAR Ecosystem Standard Container Runtime Setup

---

## 📌 Project Overview

Docker is the foundational container runtime used throughout the SOC-SOAR ecosystem for deploying:

- TheHive
- Cortex
- n8n
- Supporting services
- Optional microservices components

This guide provides a clean, secure, and standard Docker installation procedure for Ubuntu-based AWS EC2 instances.

It is written as a reusable installation blueprint for any Linux instance.

---

## 🎯 Objective

- Install Docker Engine securely using official repository
- Add Docker GPG key properly
- Configure Docker repository correctly
- Install Docker Compose plugin
- Enable Docker service
- Add non-root user access
- Validate installation with container test

---

## 🖥️ Environment Requirements

| Requirement | Minimum |
|-------------|----------|
| OS | Ubuntu 22.04 / 24.04 LTS |
| RAM | 2GB minimum |
| Disk | 20GB minimum |
| Internet Access | Required |
| User Privileges | sudo access |

---

## 🏗️ Why Use Official Docker Repository?

Using Ubuntu’s default Docker package may:
- Install outdated versions
- Lack latest Compose plugin
- Cause compatibility issues with TheHive/MISP

Official Docker repository ensures:
- Latest stable release
- Verified packages
- Secure GPG validation
- Better container compatibility

---

## 🔐 Installation Phases

---

### 1️⃣ Install Prerequisites

Install required system packages:

- ca-certificates
- curl
- gnupg
- lsb-release

---

### 2️⃣ Add Docker GPG Key (Secure Method)

Instead of deprecated `apt-key`, modern keyring method is used:

- Create `/etc/apt/keyrings`
- Import Docker GPG key
- Convert to binary format
- Set read permissions

This ensures:
- Proper repository signing validation
- No `NO_PUBKEY` errors
- Secure package installation

---

### 3️⃣ Add Docker Official Repository

Repository configuration dynamically adjusts based on:

- Architecture (`dpkg --print-architecture`)
- Ubuntu codename (`lsb_release -cs`)

This ensures compatibility with:
- amd64
- arm64

---

### 4️⃣ Update Package Index

Run:

- `apt clean`
- `apt update`

You should NOT see:

- NO_PUBKEY errors
- Repository not signed warnings

If you see those errors → GPG import failed.

---

### 5️⃣ Install Docker Engine & Plugins

Install:

- docker-ce
- docker-ce-cli
- containerd.io
- docker-buildx-plugin
- docker-compose-plugin

This ensures:
- Modern Docker architecture
- Compose v2 support
- Buildx support

---

### 6️⃣ Add User to Docker Group

By default Docker requires root.

To avoid using `sudo` every time:

- Add current user to docker group
- Reload group session

---

### 7️⃣ Enable & Start Docker

Ensure Docker:

- Starts automatically at boot
- Runs immediately
- Verified via test container

---

## 🔎 Validation Steps

Run:

```bash
docker --version
docker compose version
docker run hello-world
````

Expected Output:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

If this message appears → Docker environment is fully operational.

---

## 📁 Repository Structure

```text
00-installation-and-setup-guide/
└── 02-docker-installation/
    ├── README.md
    ├── commands.sh
    ├── troubleshooting.md
    └── architecture-notes.txt
```

---

## 🧠 What I Learned

* Secure repository key management prevents GPG issues
* Docker group permissions simplify container management
* Proper version control avoids compatibility problems
* Clean Docker setup prevents future deployment instability

---

## 🌍 Why This Matters

Docker is the container foundation of:

* Case management (TheHive)
* Threat intelligence platforms (MISP)
* Automation tools (n8n)
* Analyzer engines (Cortex)

Without stable Docker:

* SOC tools fail to start
* Integrations break
* Containers crash silently

---

## 🏢 Real-World Relevance

Docker is widely used in:

* DevSecOps pipelines
* Cloud-native deployments
* Security automation platforms
* Microservice-based SOC infrastructures

Mastering Docker installation is a core infrastructure engineering skill.

---

## ✅ Result

Docker installed securely using official repository, Compose plugin verified, test container executed successfully.

System is ready for container-based SOC tool deployment.

---

> Next Step → Deploy TheHive / Cortex or any tools using Docker.

---
