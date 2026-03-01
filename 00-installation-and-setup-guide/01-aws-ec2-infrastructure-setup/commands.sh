#!/bin/bash

############################################################
# AWS EC2 Infrastructure Setup - Validation Commands
# SOC-SOAR Ecosystem Foundation
############################################################

#############################
# 1️⃣ Initial System Check
#############################

whoami
hostname
uname -a
lsb_release -a

#############################
# 2️⃣ Network Interface Check
#############################

ip a
ip addr show
ip route
ip route show
cat /etc/netplan/*.yaml

#############################
# 3️⃣ Gateway Connectivity Test
#############################

ping -c 3 10.0.1.1

#############################
# 4️⃣ External IP Connectivity Test
#############################

ping -c 3 8.8.8.8
ping -c 3 1.1.1.1

#############################
# 5️⃣ DNS Resolution Test
#############################

cat /etc/resolv.conf
nslookup google.com
dig google.com
curl -I https://google.com

#############################
# 6️⃣ Update System (ONLY After Network Validation)
#############################

sudo apt update
sudo apt upgrade -y

#############################
# 7️⃣ Install Basic Utilities
#############################

sudo apt install -y \
curl \
wget \
git \
net-tools \
vim \
htop \
unzip \
ca-certificates \
gnupg \
lsb-release \
software-properties-common

#############################
# 8️⃣ Firewall Status Check
#############################

sudo ufw status
sudo iptables -L -n -v

#############################
# 9️⃣ Open Required Ports (If Using UFW)
#############################

sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5601/tcp
sudo ufw allow 9200/tcp
sudo ufw allow 1514/tcp
sudo ufw allow 1515/tcp
sudo ufw allow 9000/tcp
sudo ufw enable

#############################
# 🔟 Time Synchronization Check
#############################

timedatectl
sudo timedatectl set-timezone UTC

#############################
# 1️⃣1️⃣ Verify Outbound HTTPS
#############################

curl -v https://api.github.com
curl -v https://google.com

#############################
# 1️⃣2️⃣ Check Open Ports
#############################

sudo ss -tulnp
sudo netstat -tulnp

#############################
# 1️⃣3️⃣ Disk & Resource Check
#############################

df -h
free -m
top

#############################
# 1️⃣4️⃣ Test AWS Metadata Service
#############################

curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/instance-id
curl http://169.254.169.254/latest/meta-data/public-ipv4

#############################
# 1️⃣5️⃣ Final Validation Summary
#############################

echo "EC2 Network Validation Completed"
echo "Ready for SOC-SOAR Tool Installation"

############################################################
# END OF FILE
############################################################
