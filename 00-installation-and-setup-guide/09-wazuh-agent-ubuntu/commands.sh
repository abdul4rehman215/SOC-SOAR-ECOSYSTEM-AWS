#!/bin/bash

#############################################
# Wazuh Agent Installation – Ubuntu 24.04
#############################################

WAZUH_MANAGER="WAZUH_SERVER_IP"

echo "Downloading Wazuh Agent..."
curl -sO https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.x.x-1_amd64.deb

echo "Installing Agent..."
sudo WAZUH_MANAGER="$WAZUH_MANAGER" dpkg -i wazuh-agent_4.x.x-1_amd64.deb

echo "Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent

echo "Checking service status..."
sudo systemctl status wazuh-agent
