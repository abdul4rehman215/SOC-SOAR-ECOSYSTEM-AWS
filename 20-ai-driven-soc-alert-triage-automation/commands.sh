#!/bin/bash
# ============================================================
# Project: AI-Driven SOC Alert Triage Automation (Wazuh + n8n + Gemini)
# File: commands.sh
# Purpose: Commands executed (sequential, paste-ready)
# Notes:
# - Replace <EC2_PUBLIC_IP> with your instance public IP
# - Run "newgrp docker" OR log out/in after adding user to docker group
# - Some steps open editors (nano). Those are included as-is.
# ============================================================


# ------------------------------------------------------------
# 0) System Prep (AWS EC2 Ubuntu)
# ------------------------------------------------------------
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git jq


# ------------------------------------------------------------
# 1) Install Docker + Docker Compose (Ubuntu)
# ------------------------------------------------------------
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl status docker --no-pager

# Allow current user to run docker without sudo
sudo usermod -aG docker $USER
newgrp docker

# Verify docker works
docker version
docker compose version || docker-compose version


# ------------------------------------------------------------
# 2) Run n8n (Self-hosted via Docker)
# ------------------------------------------------------------

# Option A: Run n8n in foreground (for quick testing)
# docker run -it --rm \
#   --name n8n \
#   -p 5678:5678 \
#   -v ~/.n8n:/home/node/.n8n \
#   n8nio/n8n

docker run -d \
  --name n8n \
  -p 127.0.0.1:5678:5678 \
  -v /home/ubuntu/.n8n:/home/node/.n8n \
  -e N8N_HOST=54.210.89.104 \
  -e N8N_PORT=5678 \
  -e N8N_PROTOCOL=http \
  -e N8N_SECURE_COOKIE=false \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=StrongPassword123 \
  --restart unless-stopped \
  n8nio/n8n

# Option B: Run n8n in detached mode (recommended)
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v /home/ubuntu/.n8n:/home/node/.n8n \
  -e N8N_HOST=54.210.89.104 \
  -e N8N_PORT=5678 \
  -e N8N_PROTOCOL=http \
  -e N8N_SECURE_COOKIE=false \
  --restart unless-stopped \
  n8nio/n8n

# Verify container status
docker ps
docker logs n8n --tail 50

# (Browser Step) Open:
# http://<EC2_PUBLIC_IP>:5678
#
# (GUI Step) Create workflow -> Webhook Node -> POST -> path: custom-n8n-ai
# Production URL will be:
# http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai


# ------------------------------------------------------------
# 3) Ensure AWS Security Group allows n8n port (5678)
# ------------------------------------------------------------
# (AWS Console Step) Add inbound rule:
# TCP 5678 -> Your IP OR 0.0.0.0/0 (only for testing)
#
# Local verification:
sudo ss -tulnp | grep 5678 || true


# ------------------------------------------------------------
# 4) Wazuh Manager: Add Custom Integration Script (custom-n8n-ai)
# ------------------------------------------------------------

# Go to integrations directory
cd /var/ossec/integrations

# Create / edit the integration script file
# (Paste the script content from repo: scripts/custom-n8n-ai)
sudo nano custom-n8n-ai

# Set ownership & permissions so wazuh can execute it
sudo chown root:wazuh /var/ossec/integrations/custom-n8n-ai
sudo chmod 750 /var/ossec/integrations/custom-n8n-ai

# Verify permissions
ls -l /var/ossec/integrations/custom-n8n-ai


# ------------------------------------------------------------
# 5) Configure ossec.conf Integration Block (Wazuh -> n8n Webhook)
# ------------------------------------------------------------

# Edit Wazuh manager configuration
sudo nano /var/ossec/etc/ossec.conf

# Add inside <ossec_config>:
# <integration>
#   <name>custom-n8n-ai</name>
#   <hook_url>http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai</hook_url>
#   <level>7</level>
#   <alert_format>json</alert_format>
# </integration>

# Restart Wazuh Manager
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager --no-pager


# ------------------------------------------------------------
# 6) Validate Wazuh Integration Execution + Forwarding
# ------------------------------------------------------------

# Watch integration logs live
sudo tail -f /var/ossec/logs/integrations.log

# (Optional) In another terminal, validate Wazuh alerts file exists (varies)
sudo ls -lah /var/ossec/logs/alerts/ || true
sudo ls -lah /var/ossec/logs/alerts/alerts.json || true


# ------------------------------------------------------------
# 7) Quick Webhook Connectivity Test (Optional)
# ------------------------------------------------------------
# Use this ONLY to confirm n8n webhook reachable from Wazuh server:
# (Ensure workflow is ACTIVE in n8n; use production URL)

curl -i -X POST "http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai" \
  -H "Content-Type: application/json" \
  -d '{"test":"wazuh_to_n8n_connectivity","rule_level":9,"description":"test event"}'


# ------------------------------------------------------------
# 8) n8n Workflow Build (GUI Steps)
# ------------------------------------------------------------
# (GUI Step) Build node chain:
# 1) Webhook (POST /custom-n8n-ai)
# 2) Code (JavaScript) -> "Normalize Wazuh Alert"
#    - paste from repo: scripts/normalize_wazuh_alert.js
# 3) AI Agent (Gemini) -> "AI SOC Triage Engine"
#    - paste prompt from repo: scripts/ai_soc_prompt.txt
#    - configure Gemini credentials
# 4) Code (JavaScript) -> "Format SOC Email Report"
#    - paste from repo: scripts/format_soc_email_report.js
# 5) Send Email (SMTP) -> "Send SOC Alert Email"
#    - Subject: {{$json.subject}}
#    - HTML Body: {{$json.html}}
#
# (GUI Step) Activate workflow (Production mode)


# ------------------------------------------------------------
# 9) Gmail SMTP (App Password) Notes (GUI)
# ------------------------------------------------------------
# (Google Account Step)
# - Enable 2FA -> create App Password (e.g., "n8n-automation")
#
# (n8n GUI Step) Create SMTP credential:
# Host: smtp.gmail.com
# Port: 465
# SSL/TLS: ON
# User: yourgmail@gmail.com
# Password: <Gmail App Password>


# ------------------------------------------------------------
# 10) Operational Checks (n8n)
# ------------------------------------------------------------
# Verify n8n is up after reboot:
docker ps | grep n8n || true
docker logs n8n --tail 50

# Restart n8n if needed:
docker restart n8n
docker logs n8n --tail 50
