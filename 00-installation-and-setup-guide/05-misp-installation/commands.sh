#!/bin/bash

#############################################
# MISP 2.5 Installation – Ubuntu 24.04
# AWS EC2 Deployment
# Instance: t2.xlarge (4 vCPU / 16GB RAM)
#############################################

echo "Updating system..."
sudo apt update

echo "Installing required base packages..."
sudo apt install -y git curl unzip gnupg-agent software-properties-common

#############################################
# Create Dedicated MISP User
#############################################

echo "Creating misp user..."
sudo adduser misp --gecos "MISP,,," --disabled-password

echo "Setting password for misp user..."
echo "misp:OctaSec123!" | sudo chpasswd

echo "Adding misp to required groups..."
sudo usermod -aG sudo,staff,www-data misp

echo "Verifying user..."
id misp

#############################################
# Run Official MISP Installer
#############################################

echo "Switching to misp user..."
sudo -i -u misp bash << 'EOF'

cd /tmp

echo "Downloading official MISP install script..."
wget --no-cache -O INSTALL.sh https://raw.githubusercontent.com/MISP/MISP/2.5/INSTALL/INSTALL.ubuntu2404.sh

chmod +x INSTALL.sh

echo "Starting MISP installation..."
sudo bash INSTALL.sh

EOF

#############################################
# Service Verification
#############################################

echo "Checking core services..."
systemctl status apache2
systemctl status mariadb
systemctl status redis-server

#############################################
# Verify Database Initialization
#############################################

echo "Checking database configuration file..."
ls /var/www/MISP/app/Config/database.php

#############################################
# AWS BaseURL Fix
#############################################

echo "Retrieving public IP..."
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo "Setting MISP base URL..."
sudo -u www-data /var/www/MISP/app/Console/cake Admin setSetting MISP.baseurl "https://$PUBLIC_IP"

#############################################
# Enable SSL
#############################################

echo "Enabling SSL module..."
sudo a2enmod ssl
sudo systemctl reload apache2

#############################################
# Show Access Information
#############################################

echo "----------------------------------------"
echo "MISP Installation Complete"
echo "Access URL: https://$PUBLIC_IP"
echo "Default user: admin@admin.test"
echo "Password: (Displayed after installer completes)"
echo "----------------------------------------"

echo "To monitor logs:"
echo "sudo tail -f /var/www/MISP/app/tmp/logs/error.log"
