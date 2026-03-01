# 🐳 Project 02 — Docker Installation Guide (Ubuntu / AWS EC2 Ready)

<p align="center">

  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/icons/docker_logo.png" width="300"/>

</p>
  

> **Goal:** Install Docker Engine + Docker Compose Plugin on Ubuntu (AWS EC2 or any VM) using the official Docker repository, verify installation, and prepare the host for SOC/SOAR tool deployments (TheHive, Cortex, n8n, etc.).

---

## 📌 Project Overview

Many SOC/SOAR components in this portfolio (especially **TheHive**, **Cortex**, **n8n**, and sometimes **MISP**) run cleanly using Docker.

This project provides a **standard, reusable Docker installation guide** that can be applied to:
- AWS EC2 Ubuntu instances
- Local Ubuntu VMs
- Cloud lab machines

It follows the **official Docker installation method**:
- install prerequisites
- import Docker GPG key into `/etc/apt/keyrings`
- add official Docker repository
- install Docker engine + compose plugin
- validate with `hello-world`

---

## 🎯 Objectives

By completing this project, I ensured:

- Docker Engine is installed from the official Docker repository
- Docker GPG key is properly added (no `NO_PUBKEY` errors)
- Docker Compose plugin is installed and working (`docker compose ...`)
- Docker service is enabled and starts automatically
- The user can run Docker without `sudo` (docker group configured)
- Installation is validated using the official `hello-world` test image

---

## ✅ Prerequisites

### OS Requirements
- Ubuntu 22.04 LTS or Ubuntu 24.04 LTS (recommended)
- Working internet + DNS resolution
- Sudo privileges

### Recommended Pre-checks
Before installing Docker, confirm:
- internet works
- DNS works
- apt works

```bash
ping -c 2 8.8.8.8
curl -I https://google.com
sudo apt update
````

---

## 🧪 Lab Environment

| Component      | Value                                  |
| -------------- | -------------------------------------- |
| OS             | Ubuntu 24.04 LTS (works for 22.04 too) |
| Platform       | AWS EC2 / VM / Cloud                   |
| Install Method | Official Docker APT Repo               |
| Compose        | Docker Compose Plugin                  |
| Validation     | `docker run hello-world`               |

---

## 🧱 Task Overview (What Was Done)

### ✅ Task 1 — Install prerequisites

Installed required packages for secure repository setup:

* `ca-certificates`
* `curl`
* `gnupg`
* `lsb-release`

### ✅ Task 2 — Add Docker GPG key (trusted keyring method)

* Created `/etc/apt/keyrings`
* Downloaded Docker GPG key
* Converted key to `.gpg` format using `gpg --dearmor`
* Set correct permissions
* Verified key exists

### ✅ Task 3 — Add Docker repository

Added the official Docker APT repository for the detected Ubuntu release.

### ✅ Task 4 — Update package index (ensure repo trust)

* Cleaned apt cache
* Updated apt index
* Verified no trust/signing errors occurred

### ✅ Task 5 — Install Docker + Compose

Installed:

* Docker Engine (`docker-ce`)
* Docker CLI
* containerd
* buildx plugin
* compose plugin

### ✅ Task 6 — Enable and verify

* Enabled and started Docker service
* Added user to docker group
* Verified:

  * Docker version
  * Docker compose version
  * `hello-world` container output

---

## 📂 Repository Structure

```text
00-installation-setup/
└── project02-docker-installation-guide/
    ├── README.md
    ├── commands.sh
    ├── scripts/
    │   └── docker_postcheck.sh
    ├── reports/
    │   └── executive_summary.md
    ├── evidence/
    │   └── hello-world-output.txt
    ├── troubleshooting.md
    ├── interview_qna.md
    └── architecture-notes.txt
```

> Notes:
>
> * `evidence/hello-world-output.txt` can contain the final expected output text.
> * Scripts are optional but useful for quick health checks.

---

## ✅ Expected Final Output (Validation)

When running the test container:

```bash
docker run hello-world
```

You should see a message starting with:

> **Hello from Docker!**
> This message shows that your installation appears to be working correctly.

This confirms:

* Docker daemon is running
* Docker can pull images
* Containers can run successfully

---

## 🔍 Verification Checklist

Before using Docker to deploy tools:

* [ ] `docker --version` works
* [ ] `docker compose version` works
* [ ] `docker run hello-world` prints success message
* [ ] `systemctl status docker` shows active/running
* [ ] User can run docker commands without sudo (after group apply)

---

## 🧠 What I Learned

* Proper Docker installation should use keyring-based GPG trust (`/etc/apt/keyrings`)
* Most Docker install failures come from:

  * DNS issues
  * incorrect GPG key permissions
  * wrong repository configuration
* Installing Docker correctly once saves hours of tool deployment failures later
* Docker Compose plugin (`docker compose`) is now the standard (instead of old `docker-compose`)

---

## 🌍 Why This Matters

Many SOC/SOAR tools deploy faster and cleaner with Docker:

* avoids dependency conflicts
* reduces setup time
* enables faster troubleshooting
* supports repeatable deployments

For a SOC lab on AWS, Docker is a major enabler for:

* rapid deployment
* isolated services
* clean upgrades/rebuilds

---

## 🧩 Real-World Applications

* Deploying SOAR tools using containers
* Running SOC stacks in lab and staging environments
* Reproducible security tool deployments
* Blue-team test environments
* Standardizing installations across multiple servers

---

## 🏁 Conclusion

This project provides a reliable, reusable Docker installation method for Ubuntu systems used in this SOC/SOAR portfolio.

With Docker installed and verified, future deployments (TheHive, Cortex, n8n, etc.) become faster, consistent, and easier to manage.

---
