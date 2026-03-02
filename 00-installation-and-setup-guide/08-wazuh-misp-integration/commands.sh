#!/bin/bash
# ==============================================================
# WAZUH ↔ MISP FILE HASH INTEGRATION – COMMANDS
# AWS SOC LAB DEPLOYMENT
# ==============================================================

# --------------------------------------------------------------
# 1️⃣ Create Integration Script on Wazuh Manager
# --------------------------------------------------------------

cd /var/ossec/integrations/
nano custom-misp-file-hashes.py

# Paste the full Python script
# Save and exit


# --------------------------------------------------------------
# 2️⃣ Set Proper Permissions
# --------------------------------------------------------------

chmod 750 /var/ossec/integrations/custom-misp-file-hashes.py
chown root:wazuh /var/ossec/integrations/custom-misp-file-hashes.py

# Verify
ls -l /var/ossec/integrations/custom-misp-file-hashes.py


# --------------------------------------------------------------
# 3️⃣ Configure Wazuh Manager Integration Block
# --------------------------------------------------------------

nano /var/ossec/etc/ossec.conf

# Add inside <ossec_config>:

# <integration>
#   <name>custom-misp-file-hashes.py</name>
#   <hook_url>https://YOUR_MISP_IP</hook_url>
#   <api_key>YOUR_MISP_AUTHKEY</api_key>
#   <group>syscheck</group>
#   <rule_id>554</rule_id>
#   <alert_format>json</alert_format>
# </integration>


# Validate configuration before restart
/var/ossec/bin/wazuh-analysisd -t


# --------------------------------------------------------------
# 4️⃣ Create Custom Rules File
# --------------------------------------------------------------

cd /var/ossec/etc/rules/
nano misp_file_hashes.xml

# Paste the custom rules content
# Save and exit

# Validate again
/var/ossec/bin/wazuh-analysisd -t


# --------------------------------------------------------------
# 5️⃣ Restart Wazuh Manager
# --------------------------------------------------------------

systemctl restart wazuh-manager


# --------------------------------------------------------------
# 6️⃣ Configure File Integrity Monitoring (Linux Agent)
# --------------------------------------------------------------

nano /var/ossec/etc/ossec.conf

# Add monitored directories:
# <directories check_all="yes" realtime="yes">/tmp</directories>
# <directories check_all="yes" realtime="yes">/usr/bin</directories>
# <directories check_all="yes" realtime="yes">/usr/local/bin</directories>

systemctl restart wazuh-agent


# --------------------------------------------------------------
# 7️⃣ Windows Agent (PowerShell as Administrator)
# --------------------------------------------------------------

# Restart Wazuh agent
Restart-Service wazuh


# --------------------------------------------------------------
# 8️⃣ Monitor Integration Logs
# --------------------------------------------------------------

tail -f /var/ossec/logs/integrations.log

tail -f /var/ossec/logs/ossec.log

grep -i "misp" /var/ossec/logs/ossec.log


# --------------------------------------------------------------
# 9️⃣ Manual EICAR Test (Linux Endpoint)
# --------------------------------------------------------------

curl -Lo /tmp/eicar.exe https://secure.eicar.org/eicar.com
curl -Lo /tmp/eicar_test_$(date +%s).exe https://secure.eicar.org/eicar.com


# --------------------------------------------------------------
# 🔟 Expected Wazuh Rules
# --------------------------------------------------------------

# Rule 554    → File creation detected
# Rule 100800 → MISP integration triggered
# Rule 100802 → HASH MATCH (Level 12)


# --------------------------------------------------------------
# 1️⃣1️⃣ Optional – Enable Integrator Debug Mode
# --------------------------------------------------------------

nano /var/ossec/etc/internal_options.conf

# Set:
# integrator.debug=2

systemctl restart wazuh-manager


# --------------------------------------------------------------
# END OF COMMANDS
# --------------------------------------------------------------
