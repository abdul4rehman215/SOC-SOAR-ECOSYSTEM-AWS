#!/bin/bash
# ============================================================
# Project: Zeek Network Security Monitoring + Threat Detection Integrated with Wazuh SIEM
# File: commands.sh
#
# Rules:
# - Only commands executed (no explanations)
# - Sequential order
# - Clean and paste-ready
# ============================================================


# ------------------------------------------------------------
# Step 0 - Identify Interface / IP / Subnet (Zeek Sensor)
# ------------------------------------------------------------
ip a


# ------------------------------------------------------------
# Step 1 - Add Zeek Repository + GPG Key (Ubuntu 24.04)
# ------------------------------------------------------------
echo 'deb http://download.opensuse.org/repositories/security:/zeek/Ubuntu_24.04/ /' | sudo tee /etc/apt/sources.list.d/security:zeek.list
curl -fsSL https://download.opensuse.org/repositories/security:zeek/Ubuntu_24.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null
sudo apt update -y


# ------------------------------------------------------------
# Step 2 - Install Zeek
# ------------------------------------------------------------
sudo apt install zeek -y


# ------------------------------------------------------------
# Step 3 - Add Zeek to PATH + Verify
# ------------------------------------------------------------
echo "export PATH=\$PATH:/opt/zeek/bin" >> ~/.bashrc
source ~/.bashrc
zeek --version


# ------------------------------------------------------------
# Step 4 - Configure Zeek Node Settings (interface)
# ------------------------------------------------------------
sudo nano /opt/zeek/etc/node.cfg


# ------------------------------------------------------------
# Step 5 - Configure Internal Networks Scope
# ------------------------------------------------------------
sudo nano /opt/zeek/etc/networks.cfg


# ------------------------------------------------------------
# Step 6 - Enable JSON Log Output
# ------------------------------------------------------------
sudo nano /opt/zeek/share/zeek/site/local.zeek


# ------------------------------------------------------------
# Step 7 - Validate Zeek Configuration
# ------------------------------------------------------------
sudo zeekctl check


# ------------------------------------------------------------
# Step 8 - Deploy and Start Zeek
# ------------------------------------------------------------
sudo zeekctl deploy


# ------------------------------------------------------------
# Step 9 - Verify Zeek Logs Are Generated
# ------------------------------------------------------------
ls -lah /opt/zeek/logs/current/
tail -n 20 /opt/zeek/logs/current/conn.log
tail -n 20 /opt/zeek/logs/current/dns.log
tail -n 20 /opt/zeek/logs/current/ssl.log


# ------------------------------------------------------------
# Step 10 - Configure Wazuh Agent to Monitor Zeek Logs
# ------------------------------------------------------------
sudo nano /var/ossec/etc/ossec.conf
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent


# ------------------------------------------------------------
# Step 11 - Create Wazuh Decoders for Zeek (on Wazuh Manager)
# ------------------------------------------------------------
sudo nano /var/ossec/etc/decoders/zeek_decoders.xml


# ------------------------------------------------------------
# Step 12 - Create Wazuh Rules for Zeek Alerts (on Wazuh Manager)
# ------------------------------------------------------------
sudo nano /var/ossec/etc/rules/zeek_rules.xml


# ------------------------------------------------------------
# Step 13 - Restart Wazuh Manager After Decoder/Rule Changes
# ------------------------------------------------------------
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager


# ------------------------------------------------------------
# Step 14 - DNS Query Activity Test (Zeek Sensor)
# ------------------------------------------------------------
dig wazuh.com
dig virustotal.com


# ------------------------------------------------------------
# Step 15 - Recon / Port Scan Test (run from Kali Attacker)
# ------------------------------------------------------------
# for port in {5555..5559}; do nc -zv <TARGET_IP> $port || true; done


# ------------------------------------------------------------
# Step 16 - SSL/TLS Anomaly Tests (Zeek Sensor)
# ------------------------------------------------------------
curl -k https://self-signed.badssl.com/
curl -k https://expired.badssl.com/


# ------------------------------------------------------------
# Step 17 - Local Log Checks (Zeek + Wazuh Agent)
# ------------------------------------------------------------
tail -n 50 /opt/zeek/logs/current/dns.log
tail -n 50 /opt/zeek/logs/current/conn.log
tail -n 50 /opt/zeek/logs/current/ssl.log
sudo tail -n 100 /var/ossec/logs/ossec.log
