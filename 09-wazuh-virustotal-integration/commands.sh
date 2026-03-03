#!/bin/bash

#############################################################
# WAZUH + VIRUSTOTAL INTEGRATION COMMAND REFERENCE
# Real-Time Malware Detection + Automated Removal
#############################################################

#############################################################
# PART 1 — VIRUSTOTAL INTEGRATION
#############################################################

# 1️⃣ Restart Wazuh Manager after editing ossec.conf
sudo systemctl restart wazuh-manager

# 2️⃣ Restart Wazuh Agent (Ubuntu)
sudo systemctl restart wazuh-agent

# 3️⃣ Check Wazuh Manager Status
sudo systemctl status wazuh-manager

# 4️⃣ Check Wazuh Agent Status
sudo systemctl status wazuh-agent

# 5️⃣ Verify VirusTotal Integration Script Exists
ls -lah /var/ossec/integrations/

# Expected:
# virustotal.py


#############################################################
# FIM VALIDATION
#############################################################

# 6️⃣ Confirm FIM monitored directory exists
ls -lah /media/user/software

# 7️⃣ Confirm Agent Configuration File
cat /var/ossec/etc/ossec.conf | grep syscheck -A 10


#############################################################
# MALWARE SIMULATION TEST (PART 1)
#############################################################

# 8️⃣ Download EICAR test malware
sudo curl -Lo /media/user/software/bad.exe https://secure.eicar.org/eicar.com

# 9️⃣ Verify file created
ls -lah /media/user/software/bad.exe


#############################################################
# DASHBOARD VALIDATION (Manual via GUI)
#############################################################

# Filter in Wazuh Dashboard:
# rule.groups: virustotal

# Confirm fields:
# data.virustotal.positives
# data.virustotal.permalink
# data.virustotal.sha256
# rule.level
# rule.mitre.id


#############################################################
# PART 2 — ACTIVE RESPONSE CONFIGURATION
#############################################################

# 1️⃣ Confirm Active Response directory exists on agent
ls -lah /var/ossec/active-response/bin/

# 2️⃣ Create removal script file (you will paste your script)
sudo nano /var/ossec/active-response/bin/remove-threat.sh

# 3️⃣ Set script permissions
sudo chmod 750 /var/ossec/active-response/bin/remove-threat.sh
sudo chown root:wazuh /var/ossec/active-response/bin/remove-threat.sh

# 4️⃣ Verify permissions
ls -lah /var/ossec/active-response/bin/remove-threat.sh


#############################################################
# RESTART SERVICES AFTER ACTIVE RESPONSE CONFIG
#############################################################

sudo systemctl restart wazuh-manager
sudo systemctl restart wazuh-agent


#############################################################
# MALWARE SIMULATION TEST (PART 2 - AUTOMATED REMOVAL)
#############################################################

# 1️⃣ Download EICAR again
sudo curl -Lo /media/user/software/bad.exe https://secure.eicar.org/eicar.com

# 2️⃣ Wait a few seconds

# 3️⃣ Check if file was automatically deleted
ls -lah /media/user/software/bad.exe

# Expected:
# No such file or directory


#############################################################
# VERIFY ACTIVE RESPONSE EXECUTION
#############################################################

# 4️⃣ Check Active Response log
cat /var/ossec/logs/active-responses.log

# 5️⃣ Monitor log in real-time
tail -f /var/ossec/logs/active-responses.log


#############################################################
# CHECK WAZUH ALERTS VIA CLI
#############################################################

# 6️⃣ View alerts.json for virustotal entries
sudo grep virustotal /var/ossec/logs/alerts/alerts.json | tail -n 20

# 7️⃣ View active response alerts
sudo grep active_response /var/ossec/logs/alerts/alerts.json | tail -n 20


#############################################################
# CHECK DASHBOARD FIELDS
#############################################################

# In Wazuh Dashboard filter:
# rule.groups: active_response

# Validate:
# rule.id: 100092 (successful removal)
# rule.id: 100093 (failed removal)
# data.parameters.program
# data.virustotal.source.file


#############################################################
# VIRUSTOTAL MANUAL VALIDATION
#############################################################

# Extract permalink from alert JSON
# Then open in browser:
# data.virustotal.permalink


#############################################################
# WINDOWS AGENT SERVICE RESTART (IF APPLICABLE)
#############################################################

# Run in PowerShell (Administrator):
# Restart-Service wazuh-agent


#############################################################
# TROUBLESHOOTING COMMANDS
#############################################################

# Check Manager Logs
sudo tail -f /var/ossec/logs/ossec.log

# Check Agent Logs
sudo tail -f /var/ossec/logs/ossec.log

# Check if VirusTotal script executing
sudo grep virustotal /var/ossec/logs/ossec.log

# Check if Active Response triggered
sudo grep remove-threat /var/ossec/logs/ossec.log


#############################################################
# RESOURCE MONITORING
#############################################################

# Check system memory
free -h

# Check CPU usage
htop

# Check disk usage
df -h


#############################################################
# CONFIRM FULL PIPELINE
#############################################################

# File Created
# ↓
# FIM Detects
# ↓
# VirusTotal Enriches
# ↓
# Rule 87105 Fires
# ↓
# Active Response Executes
# ↓
# File Deleted
# ↓
# SOC Alert Visible
