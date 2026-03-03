#!/bin/bash

############################################################
# WAZUH + MODSECURITY (WAF) INTEGRATION PROJECT
# Apache Web Server + ModSecurity v2 + OWASP CRS
# Wazuh Agent Log Monitoring
#
# Ubuntu Server Based Setup
############################################################


echo "================================================="
echo "STEP 1 - SYSTEM UPDATE"
echo "================================================="

sudo apt update
sudo apt upgrade -y


echo "================================================="
echo "STEP 2 - INSTALL APACHE WEB SERVER"
echo "================================================="

sudo apt install apache2 -y

sudo systemctl enable apache2
sudo systemctl start apache2
sudo systemctl status apache2


echo "================================================="
echo "STEP 3 - VERIFY APACHE MODULES"
echo "================================================="

sudo apachectl -M


echo "================================================="
echo "STEP 4 - INSTALL MODSECURITY v2"
echo "================================================="

sudo apt install libapache2-mod-security2 -y

sudo apachectl -M | grep security


echo "================================================="
echo "STEP 5 - ENABLE MODSECURITY BLOCKING MODE"
echo "================================================="

# Backup original config
sudo cp /etc/modsecurity/modsecurity.conf \
/etc/modsecurity/modsecurity.conf.bak

# Enable rule engine
sudo sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' \
/etc/modsecurity/modsecurity.conf

sudo systemctl restart apache2


echo "================================================="
echo "STEP 6 - INSTALL OWASP CORE RULE SET (CRS)"
echo "================================================="

sudo apt install modsecurity-crs -y

ls -lah /usr/share/modsecurity-crs


echo "================================================="
echo "STEP 7 - ENABLE CRS RULES"
echo "================================================="

sudo ln -s /usr/share/modsecurity-crs \
/etc/modsecurity/

sudo systemctl restart apache2


echo "================================================="
echo "STEP 8 - VERIFY MODSECURITY STATUS"
echo "================================================="

sudo apachectl -M | grep security

sudo systemctl status apache2


echo "================================================="
echo "STEP 9 - CHECK MODSECURITY LOG PATH"
echo "================================================="

sudo ls -lah /var/log/apache2/


echo "================================================="
echo "STEP 10 - ATTACK SIMULATION - SQL INJECTION"
echo "================================================="

curl "http://localhost/?id=1' OR '1'='1"


echo "================================================="
echo "STEP 11 - ATTACK SIMULATION - XSS"
echo "================================================="

curl "http://localhost/?q=<script>alert(1)</script>"


echo "================================================="
echo "STEP 12 - VERIFY 403 RESPONSE"
echo "================================================="

# Should return 403 Forbidden if WAF working


echo "================================================="
echo "STEP 13 - CHECK APACHE ERROR LOG"
echo "================================================="

sudo tail -n 20 /var/log/apache2/error.log


echo "================================================="
echo "STEP 14 - CONFIGURE WAZUH AGENT LOG MONITORING"
echo "================================================="

# Backup ossec.conf
sudo cp /var/ossec/etc/ossec.conf \
/var/ossec/etc/ossec.conf.bak


echo "================================================="
echo "Add the following blocks manually inside ossec.conf:"
echo "================================================="

echo "
<localfile>
  <log_format>apache</log_format>
  <location>/var/log/apache2/error.log</location>
</localfile>

<localfile>
  <log_format>apache</log_format>
  <location>/var/log/apache2/modsec_audit.log</location>
</localfile>
"


echo "================================================="
echo "STEP 15 - RESTART WAZUH AGENT"
echo "================================================="

sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent


echo "================================================="
echo "STEP 16 - VERIFY LOG FORWARDING"
echo "================================================="

sudo tail -f /var/ossec/logs/ossec.log


echo "================================================="
echo "STEP 17 - OPTIONAL - CHECK CRS RULE LOADING"
echo "================================================="

sudo tail -f /var/log/apache2/error.log | grep ModSecurity


echo "================================================="
echo "SETUP COMPLETE"
echo "================================================="

echo "Now verify alerts in Wazuh Dashboard."
