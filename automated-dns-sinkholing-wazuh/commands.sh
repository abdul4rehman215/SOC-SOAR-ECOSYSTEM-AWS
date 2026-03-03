#!/bin/bash

#############################################################
# Automated DNS Sinkholing – Wazuh Active Response
# Manager-Side Commands
#############################################################

echo "===== STEP 1: Verify Wazuh Manager Status ====="
sudo systemctl status wazuh-manager

echo "===== STEP 2: Edit ossec.conf ====="
sudo nano /var/ossec/etc/ossec.conf

# Add the following blocks inside ossec.conf:

# <command>
#   <name>malicious_domains</name>
#   <executable>domains.cmd</executable>
#   <timeout_allowed>no</timeout_allowed>
# </command>

# <active-response>
#   <disabled>no</disabled>
#   <command>malicious_domains</command>
#   <location>local</location>
#   <rules_id>100080</rules_id>
# </active-response>

echo "===== STEP 3: Restart Wazuh Manager ====="
sudo systemctl restart wazuh-manager

echo "===== STEP 4: Verify Manager Logs ====="
sudo tail -f /var/ossec/logs/ossec.log

echo "===== STEP 5: Validate Rule Loaded ====="
sudo /var/ossec/bin/wazuh-logtest

echo "===== STEP 6: Confirm Active Agents ====="
sudo /var/ossec/bin/agent_control -l

echo "===== STEP 7: Monitor Alerts in Real-Time ====="
sudo tail -f /var/ossec/logs/alerts/alerts.json

#############################################################
# DNS-Stats Validation (Pre-Requirement Check)
#############################################################

echo "===== Verify DNS-Stats Running ====="
sudo ss -lntp | grep 5730

echo "===== Test DNS-Stats API ====="
curl http://127.0.0.1:5730/google.com

#############################################################
# AlienVault OTX API Manual Validation
#############################################################

echo "===== Test OTX API Manually ====="
echo "Replace YOUR_API_KEY and DOMAIN"

# Example:
# curl -H "X-OTX-API-KEY: YOUR_API_KEY" \
# https://otx.alienvault.com/api/v1/indicators/domain/acmetoy.com/general

#############################################################
# Windows Endpoint Commands (Run Manually on Windows)
#############################################################

echo "===== WINDOWS COMMANDS ====="

echo "1. Restart Wazuh Agent:"
echo "   net stop wazuh-agent"
echo "   net start wazuh-agent"

echo "2. Trigger Malicious DNS Query:"
echo "   ping acmetoy.com"

echo "3. Check Sysmon DNS Logs:"
echo "   Event Viewer -> Sysmon -> Event ID 22"

echo "4. Re-Test After Sinkholing:"
echo "   ping acmetoy.com"

#############################################################
# Validation Workflow Commands
#############################################################

echo "===== Pre-Sinkhole DNS Check ====="
echo "ping acmetoy.com"
echo "Expect: external malicious IP"

echo "===== Post-Sinkhole DNS Check ====="
echo "ping acmetoy.com"
echo "Expect: 127.0.0.1"

#############################################################
# Debug Integration Testing
#############################################################

echo "===== Test Active Response Script Manually (Windows) ====="
echo "powershell -ExecutionPolicy Bypass -File C:\Windows\PowerShell\malicious_domains.ps1"

echo "===== Monitor Sinkhole Log ====="
echo "type C:\Windows\Temp\sinkhole.log"

#############################################################
# Cleanup (If Needed)
#############################################################

echo "===== Remove Sinkhole Entry (Manual Cleanup) ====="
echo "Open hosts file and remove malicious domain entry manually."

#############################################################
echo "===== END OF COMMANDS.SH ====="
#############################################################
