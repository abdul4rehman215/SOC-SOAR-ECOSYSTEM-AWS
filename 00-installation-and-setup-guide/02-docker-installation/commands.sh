#!/bin/bash

############################################################
# Docker Installation Script - Ubuntu 24.04 LTS
# SOC-SOAR Ecosystem Standard Container Runtime Setup
############################################################

#############################
# 1️⃣ Update System
#############################

sudo apt update

#############################
# 2️⃣ Install Prerequisites
#############################

sudo apt install -y ca-certificates curl gnupg lsb-release

#############################
# 3️⃣ Add Docker GPG Key
#############################

sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

ls -l /etc/apt/keyrings/docker.gpg

#############################
# 4️⃣ Add Docker Repository
#############################

sudo tee /etc/apt/sources.list.d/docker.list > /dev/null <<EOF
deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable
EOF

#############################
# 5️⃣ Update Package Index
#############################

sudo apt clean
sudo apt update

#############################
# 6️⃣ Install Docker Engine & Plugins
#############################

sudo apt install -y \
docker-ce \
docker-ce-cli \
containerd.io \
docker-buildx-plugin \
docker-compose-plugin

#############################
# 7️⃣ Enable & Start Docker
#############################

sudo systemctl enable docker
sudo systemctl start docker

#############################
# 8️⃣ Add Current User to Docker Group
#############################

sudo usermod -aG docker $USER
newgrp docker

#############################
# 9️⃣ Verify Installation
#############################

docker --version
docker compose version

#############################
# 🔟 Run Test Container
#############################

docker run hello-world

############################################################
# END OF FILE
############################################################
