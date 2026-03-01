#!/bin/bash
# ==============================================================
# WAZUH INSTALLATION – AWS EC2 (Ubuntu 24.04)
# SOC-SOAR Ecosystem Core SIEM Deployment
# ==============================================================
# Recommended Instance:
# t2.large / t3.large
# 8GB RAM
# 2 vCPU
# 30GB disk
# Ubuntu 24.04 LTS
# ==============================================================

# ==============================
# SYSTEM PREPARATION
# ==============================

sudo apt update -y
sudo apt upgrade -y

sudo apt install -y curl unzip gnupg apt-transport-https lsb-release software-properties-common

# -------------------------------
# (Optional) Pre-checks
# -------------------------------
whoami
hostname
uname -a
cat /etc/os-release

# Verify internet + DNS before installing anything
ping -c 2 8.8.8.8
curl -I https://google.com

# ==============================
# DOWNLOAD WAZUH INSTALLER
# ==============================

curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh

ls -l wazuh-install.sh


# ==============================
# RUN ALL-IN-ONE INSTALLATION
# ==============================

sudo bash ./wazuh-install.sh -a


# ==============================================================
# INSTALLATION NOTES:
# This installs:
# - Wazuh Manager
# - Wazuh Indexer
# - Wazuh Dashboard
# - Filebeat
# ==============================================================
# At the end of installation:
# Username: admin
# Password: Auto-generated (SAVE IT)
# ==============================================================


# ==============================
# CHECK SERVICE STATUS
# ==============================

sudo systemctl status wazuh-manager
sudo systemctl status wazuh-indexer
sudo systemctl status wazuh-dashboard
sudo systemctl status filebeat


# ==============================
# ENABLE SERVICES ON BOOT
# ==============================

sudo systemctl enable wazuh-manager
sudo systemctl enable wazuh-indexer
sudo systemctl enable wazuh-dashboard
sudo systemctl enable filebeat


# ==============================
# VERIFY OPEN PORTS
# ==============================

sudo ss -tulnp | grep -E "1514|1515|55000|9200|443"


# ==============================
# BACKUP DEFAULT CONFIG BEFORE EDITING
# ==============================

sudo cp /var/ossec/etc/ossec.conf /var/ossec/etc/ossec.conf.backup


# ==============================
# EDIT CONFIG FILE
# ==============================

sudo nano /var/ossec/etc/ossec.conf


# ==============================
# AFTER EDITING CONFIG
# RESTART ONLY MANAGER
# ==============================

sudo systemctl restart wazuh-manager


# ==============================
# VERIFY MANAGER LOG
# ==============================

sudo tail -n 50 /var/ossec/logs/ossec.log


# ==============================
# VERIFY INDEXER HEALTH
# ==============================

curl -k -u admin:YOUR_PASSWORD https://localhost:9200


# ==============================
# VERIFY API
# ==============================

curl -k -u admin:YOUR_PASSWORD https://localhost:55000


# ==============================
# FIREWALL CHECK (IF UFW USED)
# ==============================

sudo ufw status

# If using UFW, allow:
# sudo ufw allow 1514/tcp
# sudo ufw allow 1515/tcp
# sudo ufw allow 55000/tcp
# sudo ufw allow 9200/tcp
# sudo ufw allow 443/tcp


# ==============================
# CHECK MEMORY USAGE
# ==============================

free -h
htop


# ==============================
# FINAL DASHBOARD ACCESS
# ==============================

# Open browser:
# https://<EC2-PUBLIC-IP>

# Login with:
# Username: admin
# Password: (Generated at install)


# ==============================================================
# END OF WAZUH INSTALLATION COMMANDS
# ==============================================================
