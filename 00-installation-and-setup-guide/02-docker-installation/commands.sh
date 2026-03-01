#!/bin/bash
# ==========================================
# Project 02 — Docker Installation Guide
# commands.sh (Sequential / Paste-ready)
# OS: Ubuntu 22.04 / 24.04
# ==========================================

# -------------------------------
# 0) (Optional) Pre-checks
# -------------------------------
ping -c 2 8.8.8.8
curl -I https://google.com

# -------------------------------
# 1) Install prerequisites
# -------------------------------
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

# -------------------------------
# 2) Download Docker GPG Key (Keyrings method)
# -------------------------------
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set correct permissions
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Verify key exists
ls -l /etc/apt/keyrings/docker.gpg

# -------------------------------
# 3) Add Docker Repository
# -------------------------------
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null <<EOF
deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable
EOF

# -------------------------------
# 4) Update Package Index (Ensure repo trust)
# -------------------------------
sudo apt clean
sudo apt update

# ✅ You should NOT see:
# - NO_PUBKEY
# - repository is not signed

# -------------------------------
# 5) Install Docker & Docker Compose Plugin
# -------------------------------
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# -------------------------------
# 6) Enable & Verify Docker
# -------------------------------
sudo systemctl enable docker
sudo systemctl start docker

# Add user to docker group (so you can run docker without sudo)
sudo usermod -aG docker $USER

# Apply group change in current session
newgrp docker

# Verify versions
docker --version
docker compose version

# Test container run
docker run hello-world

# -------------------------------
# ✅ Expected Final Output
# -------------------------------
# "Hello from Docker!"
# "This message shows that your installation appears to be working correctly."
