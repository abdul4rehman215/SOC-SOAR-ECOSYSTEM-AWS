#!/bin/bash

#################################################################
# SSH Brute Force Detection Commands
# Wazuh + Slack + Kali Linux
#################################################################

##############################
# 1️⃣ UBUNTU CLIENT (Victim)
##############################

# Monitor SSH authentication logs
sudo tail -f /var/log/auth.log

# Test invalid login locally
ssh invaliduser@localhost

# Check SSH service status
sudo systemctl status ssh


#########################################
# 2️⃣ KALI LINUX (Attacker)
#########################################

# Single failed attempt
ssh fakeuser@CLIENT_IP

# Simulate brute force (10 attempts)
for i in {1..10}; do ssh fakeuser@CLIENT_IP; done

# Continuous simulation (stop with CTRL+C)
while true; do ssh fakeuser@CLIENT_IP; done


#############################################################
# 3️⃣ WAZUH DASHBOARD VALIDATION (GUI Based)
#############################################################

# In Dashboard → Security Events
# Filter:
# rule.id: 100300

# In Dashboard → Alerting → Alerts
# Confirm:
# SSH Brute Force Alert triggered


#############################################################
# 4️⃣ SLACK VALIDATION
#############################################################

# Open Slack channel (#soc-alerts)

# Confirm message contains:
# - Alert Name
# - Severity
# - Attacker IP
# - Time Window
# - Alert State


#################################################################
# END OF COMMANDS
#################################################################
