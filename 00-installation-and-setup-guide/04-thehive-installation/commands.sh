#!/bin/bash

############################################################
# TheHive 5.5 Deployment Script (Docker)
# AWS EC2 – t2.xlarge (4 vCPU / 16GB RAM)
# Ubuntu 24.04 LTS
############################################################

#############################
# 1️⃣ VERIFY SYSTEM BASELINE
#############################

echo "Checking current time configuration..."
timedatectl

echo "Setting timezone..."
sudo timedatectl set-timezone Asia/Baku

echo "Enabling NTP synchronization..."
sudo timedatectl set-ntp yes

echo "Verifying time configuration..."
timedatectl

#############################
# 2️⃣ SET HOSTNAME
#############################

echo "Setting hostname to thehive..."
sudo hostnamectl set-hostname thehive

echo "Updating /etc/hosts file..."
sudo sed -i 's/^127\.0\.1\.1.*/127.0.1.1 thehive/' /etc/hosts

echo "Verifying hostname..."
hostnamectl

#############################
# 3️⃣ VERIFY DOCKER
#############################

echo "Checking Docker version..."
docker --version

echo "Checking Docker Compose plugin..."
docker compose version

echo "Checking Docker service status..."
sudo systemctl status docker --no-pager

#############################
# 4️⃣ INSTALL GIT (IF NOT INSTALLED)
#############################

sudo apt update
sudo apt install -y git

#############################
# 5️⃣ CLONE OFFICIAL STRANGEBEE DOCKER REPO
#############################

cd /opt

sudo mkdir -p TheHive
sudo chown -R $USER:$USER TheHive

cd TheHive

git clone https://github.com/StrangeBeeCorp/docker.git

cd docker/prod1-thehive

#############################
# 6️⃣ INITIALIZE DOCKER ENVIRONMENT
#############################

bash ../scripts/init.sh

#############################
# 7️⃣ START THEHIVE STACK
#############################

docker compose up -d

#############################
# 8️⃣ VALIDATE CONTAINERS
#############################

echo "Listing running containers..."
docker ps

#############################
# 9️⃣ FOLLOW LOGS (OPTIONAL)
#############################

echo "To follow logs of any container:"
echo "docker logs <container_id> --follow"

############################################################
# TROUBLESHOOTING – Elasticsearch Permission Fix
############################################################

echo "If Elasticsearch container fails to start:"
echo "Run the following manually:"

cat <<EOF

docker compose down

sudo chown -R 1000:1000 /opt/TheHive/docker/prod1-thehive/elasticsearch
sudo chmod -R 775 /opt/TheHive/docker/prod1-thehive/elasticsearch

docker compose up -d

EOF

############################################################
# ACCESS INFORMATION
############################################################

echo "Access TheHive UI at:"
echo "http://<EC2_PUBLIC_IP>:9000/"

echo "Default Credentials:"
echo "Username: admin"
echo "Password: secret"

echo "IMPORTANT: Change default password immediately."

############################################################
# END OF SCRIPT
############################################################
