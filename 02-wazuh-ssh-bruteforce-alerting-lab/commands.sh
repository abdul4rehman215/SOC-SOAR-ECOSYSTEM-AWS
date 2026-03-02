#!/bin/bash

#################################################################
# SSH Brute Force Detection Lab
# Wazuh + Slack + Kali Linux
# Commands categorized by machine
#################################################################

##############################
# 1️⃣ WAZUH MANAGER SERVER
##############################

# Download Wazuh installer
curl -sO https://packages.wazuh.com/4.x/wazuh-install.sh

# Install full Wazuh stack (Manager + Dashboard + Indexer)
sudo bash wazuh-install.sh -a

# Check Wazuh Manager status
sudo systemctl status wazuh-manager

# Access Dashboard
# https://<WAZUH_SERVER_IP>


###############################################################
# 2️⃣ UBUNTU CLIENT MACHINE (Victim - Wazuh Agent Installed)
###############################################################

# Download Wazuh agent installer
curl -sO https://packages.wazuh.com/4.x/wazuh-agent-install.sh

# Install agent
sudo bash wazuh-agent-install.sh

# Edit agent configuration
sudo nano /var/ossec/etc/ossec.conf

# Set manager IP
# <address>WAZUH_MANAGER_PRIVATE_IP</address>

# Enable and start agent
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent

# Verify agent status
sudo systemctl status wazuh-agent

# Verify SSH logs are being generated
sudo tail -f /var/log/auth.log

# Optional: test invalid login locally
ssh invaliduser@localhost


#########################################
# 3️⃣ KALI LINUX MACHINE (Attacker)
#########################################

# Single SSH attempt
ssh fakeuser@CLIENT_PRIVATE_IP

# Simulate brute force (10 attempts)
for i in {1..10}; do ssh fakeuser@CLIENT_PRIVATE_IP; done

# Continuous attempt simulation
while true; do ssh fakeuser@CLIENT_PRIVATE_IP; done


#############################################################
# 4️⃣ VALIDATION COMMANDS (Client Machine)
#############################################################

# Monitor SSH authentication failures
sudo tail -f /var/log/auth.log

# Example log output:
# Invalid user fakeuser from <ATTACKER_IP>


#############################################################
# 5️⃣ WAZUH ALERT VALIDATION (Dashboard - GUI Based)
#############################################################

# In Wazuh Dashboard:
# Go to → Security Events
# Filter:
# rule.id: 100300

# Go to → Alerting → Alerts
# Confirm:
# SSH Brute Force Alert triggered


#############################################################
# 6️⃣ SLACK VALIDATION
#############################################################

# Open Slack channel (#soc-alerts)

# Confirm alert contains:
# - Alert Name
# - Severity
# - Time Window
# - Attacker IP
# - Alert Status


#################################################################
# END OF COMMANDS
#################################################################
