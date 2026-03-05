# 🎤 Interview Q&A — Docker Installation Guide (Ubuntu / AWS EC2)

---

## 1) Why did you install Docker using the official Docker repository instead of Ubuntu default repo?
The official Docker repo provides newer, supported versions of Docker Engine and the Compose plugin, which reduces compatibility issues during deployments.

---

## 2) Why are `ca-certificates`, `curl`, `gnupg`, and `lsb-release` required?
They are needed to securely download the GPG key, validate repository trust, and detect the Ubuntu release version for the correct Docker repository.

---

## 3) What is the purpose of `/etc/apt/keyrings/docker.gpg`?
It stores the Docker repository signing key in a secure keyring format so APT can verify the repository packages are trusted.

---

## 4) Why do you run `chmod a+r /etc/apt/keyrings/docker.gpg`?
APT must be able to read the keyring file; incorrect permissions can cause repository signature verification failures.

---

## 5) What does `NO_PUBKEY` mean during `apt update`?
It means APT cannot verify the repository signature because the correct GPG key is missing or not readable by APT.

---

## 6) What is the difference between Docker Compose plugin and old `docker-compose`?
The plugin uses `docker compose` (built into Docker CLI). The old standalone binary uses `docker-compose`. The plugin is the modern standard.

---

## 7) Why did you run `sudo usermod -aG docker $USER`?
It adds the user to the docker group so Docker commands can run without sudo, improving usability for daily SOC tool operations.

---

## 8) What does `newgrp docker` do?
It applies docker group membership changes in the current shell session without requiring logout/login.

---

## 9) Why is `docker run hello-world` important?
It confirms Docker daemon is running, image pulling works, and containers can execute successfully—validating the installation end-to-end.

---

## 10) What does it mean if `docker run hello-world` fails with permission denied?
It usually means the user is not in the docker group, the session hasn’t refreshed, or Docker socket permissions are not accessible.

---

## 11) What does it mean if Docker installs but `apt update` shows signing errors?
Repository configuration is incorrect or the GPG key/keyring permissions are wrong, so APT rejects the repo as untrusted.

---

## 12) Why do SOC/SOAR deployments benefit from Docker?
Docker reduces dependency conflicts, isolates services, enables faster redeployments, and makes multi-service stacks easier to manage.

---

## 13) Why is internet + DNS required during Docker install?
Docker repo access, package downloads, GPG key download, and container image pulls all require working internet and name resolution.

---

## 14) Which SOC tools commonly use Docker in your ecosystem?
TheHive, Cortex, n8n, and sometimes MISP are commonly deployed using Docker, especially in lab and portfolio environments.

---

## 15) What is the biggest troubleshooting lesson from Docker installation?
Most failures are not Docker itself—they come from DNS/network issues, incorrect GPG key setup, or repository misconfiguration.

---
