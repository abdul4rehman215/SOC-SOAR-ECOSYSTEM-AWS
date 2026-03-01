#!/bin/bash

###########################################################
# Wazuh → TheHive Integration Setup Script
# AWS SOC Deployment
# commands to run in wazuh server
###########################################################

echo "Installing TheHive Python client..."

sudo /var/ossec/framework/python/bin/pip3 install thehive4py==1.8.1

echo "Verifying installation..."
sudo /var/ossec/framework/python/bin/pip3 list | grep thehive4py

###########################################################
# Create Integration Directory (if not exists)
###########################################################

echo "Ensuring integrations directory exists..."

sudo mkdir -p /var/ossec/integrations

###########################################################
# Set Permissions Reminder
###########################################################

echo "IMPORTANT:"
echo "Place the following files inside /var/ossec/integrations:"
echo "  - custom-w2thive.py"
echo "  - custom-w2thive"
echo ""
echo "Then run:"
echo "chmod +x /var/ossec/integrations/custom-w2thive.py"
echo "chmod +x /var/ossec/integrations/custom-w2thive"

###########################################################
# Restart Wazuh Manager
###########################################################

echo "Restarting Wazuh Manager..."
sudo systemctl restart wazuh-manager

echo "Checking service status..."
sudo systemctl status wazuh-manager

###########################################################
# Monitoring Commands
###########################################################

echo "-------------------------------------------"
echo "To monitor integration logs:"
echo "tail -f /var/ossec/logs/integrations.log"
echo ""
echo "To monitor Wazuh logs:"
echo "tail -f /var/ossec/logs/ossec.log"
echo "-------------------------------------------"

echo "Integration setup completed."
