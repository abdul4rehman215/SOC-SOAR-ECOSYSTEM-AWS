#!/bin/bash
# ============================================================
# Project: Snort IDS Exploration + Custom Rule Development + Wazuh SIEM Integration
# File: commands.sh
#
# Rules:
# - Only commands executed (no explanations)
# - Sequential order
# - Clean and paste-ready
# ============================================================


# ------------------------------------------------------------
# Step 0 - Identify Interface / IP / Subnet
# ------------------------------------------------------------
ip a


# ------------------------------------------------------------
# Step 1 - Install Required Dependencies
# ------------------------------------------------------------
sudo apt update
sudo apt install -y \
  build-essential \
  libpcap-dev \
  libpcre3-dev \
  libdumbnet-dev \
  zlib1g-dev \
  liblzma-dev \
  openssl \
  libssl-dev


# ------------------------------------------------------------
# Step 2 - Install Snort (HOME_NET prompt during install)
# ------------------------------------------------------------
sudo apt install -y snort


# ------------------------------------------------------------
# Step 3 - Verify Snort Installation
# ------------------------------------------------------------
snort -V


# ------------------------------------------------------------
# Step 4 - Inspect Snort Paths
# ------------------------------------------------------------
ls -lah /etc/snort/
ls -lah /etc/snort/rules/
ls -lah /var/log/snort/


# ------------------------------------------------------------
# Step 5 - Create / Edit Custom Rules (ICMP + FTP etc.)
# ------------------------------------------------------------
sudo nano /etc/snort/rules/local.rules


# ------------------------------------------------------------
# Step 6 - Validate Snort Configuration
# ------------------------------------------------------------
sudo snort -T -c /etc/snort/snort.conf


# ------------------------------------------------------------
# Step 7 - Run Snort in IDS Mode (replace <interface>)
# ------------------------------------------------------------
sudo snort -q -A console -c /etc/snort/snort.conf -i <interface>


# ------------------------------------------------------------
# Step 8 - Generate ICMP Traffic (test from local/other host)
# ------------------------------------------------------------
ping -c 3 8.8.8.8


# ------------------------------------------------------------
# Step 9 - Re-edit local.rules for ICMP request/reply split
# ------------------------------------------------------------
sudo nano /etc/snort/rules/local.rules
sudo snort -T -c /etc/snort/snort.conf


# ------------------------------------------------------------
# Step 10 - Add Snorpy-generated FTP rule into local.rules
# ------------------------------------------------------------
sudo nano /etc/snort/rules/local.rules
sudo snort -T -c /etc/snort/snort.conf


# ------------------------------------------------------------
# Step 11 - View Snort Logs
# ------------------------------------------------------------
ls -lah /var/log/snort/
tail -f /var/log/snort/snort.alert.fast


# ------------------------------------------------------------
# Step 12 - Ensure fast alert output is enabled in snort.conf
# ------------------------------------------------------------
sudo nano /etc/snort/snort.conf


# ------------------------------------------------------------
# Step 13 - Simulate FTP attempt from Kali (run on Kali)
# ------------------------------------------------------------
# ftp <SNORT_PRIVATE_IP> 21
# ftp 10.0.1.214 21


# ------------------------------------------------------------
# Step 14 - Configure Wazuh Agent to Monitor Snort fast alert log
# ------------------------------------------------------------
sudo nano /var/ossec/etc/ossec.conf
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent


# ------------------------------------------------------------
# Step 15 - Optional: Add Wazuh Snort Decoder + Rules (manager/agent)
# ------------------------------------------------------------
sudo nano /var/ossec/etc/decoders/snort_decoders.xml
sudo nano /var/ossec/etc/rules/snort_rules.xml


# ------------------------------------------------------------
# Step 16 - Restart Wazuh Components After Changes (where applicable)
# ------------------------------------------------------------
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent

sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager


# ------------------------------------------------------------
# Step 17 - Local Verification (logs)
# ------------------------------------------------------------
tail -f /var/log/snort/snort.alert.fast
sudo tail -n 100 /var/ossec/logs/ossec.log
