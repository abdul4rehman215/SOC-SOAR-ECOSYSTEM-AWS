#!/bin/bash

#############################################################
# Automated IP Blocking Extension
# NGINX + ModSecurity + Fail2Ban + Wazuh Integration
#
# This script:
# 1. Installs Fail2Ban
# 2. Configures Jail for ModSecurity
# 3. Creates ModSecurity filter
# 4. Restarts Fail2Ban
# 5. Integrates Fail2Ban logs with Wazuh Agent
#############################################################

echo "=============================================="
echo "Starting Fail2Ban Automated Blocking Setup"
echo "=============================================="

#############################################
# Update System
#############################################

echo "[+] Updating system..."
sudo apt update -y

#############################################
# Install Fail2Ban
#############################################

echo "[+] Installing Fail2Ban..."
sudo apt install fail2ban -y

echo "[+] Enabling and starting Fail2Ban..."
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

echo "[+] Checking Fail2Ban status..."
sudo systemctl status fail2ban --no-pager

#############################################
# Create Jail for ModSecurity
#############################################

echo "[+] Creating Fail2Ban jail for ModSecurity..."

sudo tee /etc/fail2ban/jail.d/modsecurity.conf > /dev/null <<EOF
[modsecurity]
enabled  = true
filter   = modsecurity
logpath  = /var/log/modsec_audit.log
backend  = polling
maxretry = 5
findtime = 300
bantime  = 3600
EOF

#############################################
# Create Filter for ModSecurity
#############################################

echo "[+] Creating Fail2Ban filter for ModSecurity..."

sudo tee /etc/fail2ban/filter.d/modsecurity.conf > /dev/null <<EOF
[Definition]
failregex = ^.*ModSecurity: Access denied with code 403.*hostname "<HOST>".*$
ignoreregex =
EOF

#############################################
# Test Filter (Optional Check)
#############################################

echo "[+] Testing filter against ModSecurity logs..."
sudo fail2ban-regex /var/log/modsec_audit.log /etc/fail2ban/filter.d/modsecurity.conf

#############################################
# Restart Fail2Ban
#############################################

echo "[+] Restarting Fail2Ban..."
sudo systemctl restart fail2ban

echo "[+] Checking Jail Status..."
sudo fail2ban-client status
sudo fail2ban-client status modsecurity

#############################################
# Integrate Fail2Ban Logs with Wazuh Agent
#############################################

echo "[+] Configuring Wazuh Agent to monitor Fail2Ban logs..."

sudo sed -i '/<\/ossec_config>/i \
<localfile>\n\
  <log_format>syslog</log_format>\n\
  <location>/var/log/fail2ban.log</location>\n\
</localfile>\n' /var/ossec/etc/ossec.conf

#############################################
# Restart Wazuh Agent
#############################################

echo "[+] Restarting Wazuh Agent..."
sudo systemctl restart wazuh-agent

echo "[+] Wazuh Agent Status:"
sudo systemctl status wazuh-agent --no-pager

#############################################
# Final Verification
#############################################

echo "=============================================="
echo "Setup Complete"
echo "=============================================="
echo "Next Steps:"
echo "1. Simulate attack from Kali:"
echo '   for i in {1..6}; do curl "http://SERVER_IP/?test=<script>alert(1)</script>"; done'
echo "2. Verify ban:"
echo "   sudo fail2ban-client status modsecurity"
echo "3. Check firewall:"
echo "   sudo iptables -L -n"
echo "4. Verify alerts in Wazuh Dashboard (rule.id:100200)"
echo "=============================================="
