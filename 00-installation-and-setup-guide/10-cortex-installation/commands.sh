#!/bin/bash

############################################################
# Cortex 3.x Deployment Script (StrangeBee Docker Method)
# AWS EC2 – Ubuntu 24.04
# Instance: t2.xlarge (4 vCPU / 16GB RAM)
############################################################

echo "=================================================="
echo "Cortex Deployment Starting..."
echo "=================================================="

############################################################
# System Update (Optional but Recommended)
############################################################

echo "[1/8] Updating system packages..."
sudo apt update -y

############################################################
# Create Installation Directory
############################################################

echo "[2/8] Creating Cortex directory..."
cd /opt || exit
sudo mkdir -p Cortex
cd Cortex || exit

############################################################
# Clone Official StrangeBee Docker Repository
############################################################

echo "[3/8] Cloning official Cortex Docker repository..."
sudo git clone https://github.com/StrangeBeeCorp/docker.git

cd docker/prod1-cortex || exit

############################################################
# Run Initialization Script
############################################################

echo "[4/8] Running initialization script..."
echo "IMPORTANT: When prompted for hostname, enter: cortex"
bash ./scripts/init.sh

############################################################
# IMPORTANT MANUAL STEP
############################################################
# At this point you MUST manually edit docker-compose.yml
#
# 1) Enable port 9001:
#    ports:
#      - '0.0.0.0:9001:9001'
#
# 2) Disable Elasticsearch security:
#    Remove:
#      - xpack.security.enabled=true
#      - ELASTIC_PASSWORD=${elasticsearch_password}
#
#    Add:
#      - xpack.security.enabled=false
#
# 3) Replace Elasticsearch healthcheck
# 4) Replace Cortex healthcheck
#
# 5) Ensure Docker socket is mounted:
#      volumes:
#        - /var/run/docker.sock:/var/run/docker.sock
#
############################################################

echo "=================================================="
echo ">>> STOP HERE <<<"
echo "Edit docker-compose.yml before continuing."
echo "Press ENTER after modifications are complete."
read -r

############################################################
# Fix Permissions (CRITICAL STEP)
############################################################

echo "[5/8] Fixing permissions for Elasticsearch and Cortex..."

sudo chown -R 1000:1000 elasticsearch cortex
sudo chmod -R 775 elasticsearch cortex

############################################################
# Start Cortex
############################################################

echo "[6/8] Starting Cortex containers..."
docker compose up -d

############################################################
# Verify Containers
############################################################

echo "[7/8] Verifying running containers..."
docker ps

############################################################
# Check Logs (Optional)
############################################################

echo "[8/8] To monitor logs, run:"
echo "docker logs <container_id> --follow"

echo "=================================================="
echo "Cortex Deployment Script Completed"
echo "=================================================="

############################################################
# ACCESS INFORMATION
############################################################

PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo ""
echo "Access Cortex at:"
echo "http://$PUBLIC_IP:9001"
echo ""
echo "On first login:"
echo "1) Click 'Update Database'"
echo "2) Create SuperAdmin account"
echo ""
echo "No default credentials exist."
echo ""
echo "Deployment Complete."
echo "=================================================="
