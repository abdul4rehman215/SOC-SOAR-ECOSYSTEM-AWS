#!/bin/bash

#############################################################
# NGINX + ModSecurity v3 + OWASP CRS + Wazuh Integration
# Ubuntu Server Deployment Script
# Full WAF + SIEM Monitoring Stack
#############################################################

echo "==============================="
echo "Updating System..."
echo "==============================="

sudo apt update && sudo apt upgrade -y

#############################################################
# Install NGINX
#############################################################

echo "==============================="
echo "Installing NGINX..."
echo "==============================="

sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx

#############################################################
# Install Build Dependencies
#############################################################

echo "==============================="
echo "Installing Build Dependencies..."
echo "==============================="

sudo apt install -y \
git gcc make build-essential \
libpcre3 libpcre3-dev \
libssl-dev \
libxml2 libxml2-dev \
libyajl-dev \
liblmdb-dev \
libgeoip-dev \
pkgconf \
libtool \
autoconf \
automake \
curl \
wget

#############################################################
# Install ModSecurity v3 (Library Mode)
#############################################################

echo "==============================="
echo "Cloning ModSecurity..."
echo "==============================="

cd /opt
sudo git clone --depth 1 https://github.com/SpiderLabs/ModSecurity
cd ModSecurity

sudo git submodule init
sudo git submodule update

echo "Building ModSecurity..."
sudo ./build.sh
sudo ./configure
sudo make
sudo make install

#############################################################
# Update Linker Configuration
#############################################################

echo "==============================="
echo "Updating Linker..."
echo "==============================="

echo "/usr/local/modsecurity/lib" | sudo tee /etc/ld.so.conf.d/modsecurity.conf
sudo ldconfig

#############################################################
# Clone ModSecurity-NGINX Connector
#############################################################

echo "==============================="
echo "Cloning ModSecurity-NGINX Connector..."
echo "==============================="

cd /opt
sudo git clone https://github.com/SpiderLabs/ModSecurity-nginx.git

#############################################################
# Download NGINX Source
#############################################################

echo "==============================="
echo "Downloading NGINX Source..."
echo "==============================="

cd /opt
NGINX_VERSION=$(nginx -v 2>&1 | cut -d/ -f2)

sudo wget http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz
sudo tar -xzf nginx-$NGINX_VERSION.tar.gz
cd nginx-$NGINX_VERSION

#############################################################
# Compile Dynamic Module
#############################################################

echo "==============================="
echo "Compiling ModSecurity Module..."
echo "==============================="

./configure --with-compat \
--add-dynamic-module=../ModSecurity-nginx

make modules

sudo cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/

#############################################################
# Enable Module in nginx.conf
#############################################################

echo "==============================="
echo "Enabling Module in NGINX..."
echo "==============================="

if ! grep -q "ngx_http_modsecurity_module.so" /etc/nginx/nginx.conf; then
  sudo sed -i '1iload_module modules/ngx_http_modsecurity_module.so;' /etc/nginx/nginx.conf
fi

#############################################################
# Configure ModSecurity
#############################################################

echo "==============================="
echo "Configuring ModSecurity..."
echo "==============================="

sudo mkdir -p /etc/nginx/modsec

sudo cp /opt/ModSecurity/modsecurity.conf-recommended \
/etc/nginx/modsec/modsecurity.conf

sudo sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' \
/etc/nginx/modsec/modsecurity.conf

#############################################################
# Install OWASP CRS
#############################################################

echo "==============================="
echo "Installing OWASP CRS..."
echo "==============================="

cd /opt
sudo git clone https://github.com/coreruleset/coreruleset.git

sudo cp -r coreruleset /etc/nginx/modsec/
cd /etc/nginx/modsec/coreruleset
sudo cp crs-setup.conf.example crs-setup.conf

#############################################################
# Create Main ModSecurity Config
#############################################################

echo "==============================="
echo "Creating Main WAF Config..."
echo "==============================="

sudo bash -c 'cat > /etc/nginx/modsec/main.conf <<EOF
Include /etc/nginx/modsec/modsecurity.conf
Include /etc/nginx/modsec/coreruleset/crs-setup.conf
Include /etc/nginx/modsec/coreruleset/rules/*.conf
EOF'

#############################################################
# Attach WAF to Default Server Block
#############################################################

echo "==============================="
echo "Attaching WAF to NGINX Server..."
echo "==============================="

sudo sed -i '/server_name _;/a \
    modsecurity on;\
    modsecurity_rules_file /etc/nginx/modsec/main.conf;' \
/etc/nginx/sites-available/default

#############################################################
# Validate NGINX
#############################################################

echo "==============================="
echo "Validating NGINX Configuration..."
echo "==============================="

sudo nginx -t

if [ $? -eq 0 ]; then
  sudo systemctl restart nginx
  echo "NGINX Restarted Successfully."
else
  echo "NGINX configuration error. Please check manually."
fi

#############################################################
# Integrate Logs with Wazuh
#############################################################

echo "==============================="
echo "Configuring Wazuh Log Monitoring..."
echo "==============================="

sudo bash -c 'cat >> /var/ossec/etc/ossec.conf <<EOF

<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/nginx/error.log</location>
</localfile>

<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/nginx/access.log</location>
</localfile>

EOF'

sudo systemctl restart wazuh-agent

#############################################################
# Final Message
#############################################################

echo "============================================"
echo "NGINX + ModSecurity + OWASP CRS Setup Done"
echo "============================================"
echo "Test with:"
echo 'curl "http://<server-ip>/?q=<script>alert(1)</script>"'
echo 'curl "http://<server-ip>/?file=../../etc/passwd"'
echo "Check logs: /var/log/nginx/error.log"
echo "Check Wazuh dashboard for alerts."
echo "============================================"
