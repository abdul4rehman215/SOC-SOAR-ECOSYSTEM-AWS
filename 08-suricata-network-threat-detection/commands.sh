#!/bin/bash

# ============================================================
# Suricata IDS + Wazuh SIEM SOC Project
# Full Command Reference
# ============================================================

# ------------------------------------------------------------
# MACHINE 1: Ubuntu Target (Suricata + Wazuh Agent Installed)
# ------------------------------------------------------------

# -------------------------
# Install Suricata
# -------------------------

sudo add-apt-repository ppa:oisf/suricata-stable -y
sudo apt update
sudo apt install suricata -y

# Verify installation
suricata -V


# -------------------------
# Download Emerging Threats Rules
# -------------------------

cd /tmp
curl -LO https://rules.emergingthreats.net/open/suricata-6.0.8/emerging.rules.tar.gz
sudo tar -xvzf emerging.rules.tar.gz -C /etc/suricata

# Verify rules
ls /etc/suricata/rules


# -------------------------
# Edit Suricata Configuration
# -------------------------

sudo nano /etc/suricata/suricata.yaml


# -------------------------
# Restart Suricata
# -------------------------

sudo systemctl restart suricata
sudo systemctl status suricata

# Monitor Suricata logs
sudo tail -f /var/log/suricata/eve.json


# -------------------------
# Configure Wazuh Agent to Read Suricata Logs
# -------------------------

sudo nano /var/ossec/etc/ossec.conf

# Add:
# <localfile>
#   <log_format>json</log_format>
#   <location>/var/log/suricata/eve.json</location>
# </localfile>

sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent



# ------------------------------------------------------------
# MACHINE 2: Wazuh Manager
# ------------------------------------------------------------

# -------------------------
# Create Custom Suricata Decoder
# -------------------------

sudo nano /var/ossec/etc/decoders/decoder-suricata-custom.xml

# Restart Manager
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager


# -------------------------
# Create Custom Suricata Rules
# -------------------------

sudo nano /var/ossec/etc/rules/100002-suricata-custom.xml
sudo nano /var/ossec/etc/rules/100050-suricata-enhanced.xml

# Validate Wazuh rule syntax
sudo /var/ossec/bin/wazuh-analysisd -t

# Restart Manager after rules
sudo systemctl restart wazuh-manager


# -------------------------
# Create Suricata Agent Group (Part 3)
# -------------------------

sudo /var/ossec/bin/agent_groups -a -g Suricata -q

# List agents
sudo /var/ossec/bin/manage_agents -l

# Add agent to Suricata group
sudo /var/ossec/bin/agent_groups -a -i 002 -g Suricata -q

# Verify group membership
sudo /var/ossec/bin/agent_groups -l


# -------------------------
# Apply Group-Level Configuration
# -------------------------

sudo nano /var/ossec/etc/shared/Suricata/agent.conf

# Add:
# <agent_config>
#   <localfile>
#     <log_format>json</log_format>
#     <location>/var/log/suricata/eve.json</location>
#   </localfile>
# </agent_config>

sudo systemctl restart wazuh-manager



# ------------------------------------------------------------
# MACHINE 3: Kali Linux (Attacker Simulation)
# ------------------------------------------------------------

# Basic Ping Test
ping <TARGET_IP>

# Basic SYN Scan
nmap -sS <TARGET_IP>

# Port-Specific Scan
nmap -sS -p 1433 <TARGET_IP>

# Vulnerability Scan
nmap --script vuln <TARGET_IP>

# Aggressive Scan
nmap -A <TARGET_IP>



# ------------------------------------------------------------
# VALIDATION COMMANDS (Any Machine as Applicable)
# ------------------------------------------------------------

# Check Suricata logs
sudo tail -f /var/log/suricata/eve.json

# Check Wazuh logs (Manager)
sudo tail -f /var/ossec/logs/ossec.log

# Test Wazuh log parsing
sudo /var/ossec/bin/wazuh-logtest

# Validate rules
sudo /var/ossec/bin/wazuh-analysisd -t


# ============================================================
# END OF COMMAND REFERENCE
# ============================================================
