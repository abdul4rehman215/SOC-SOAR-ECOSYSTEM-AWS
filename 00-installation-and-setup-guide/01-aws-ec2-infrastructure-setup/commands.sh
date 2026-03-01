#!/bin/bash
# ==========================================
# Project 01 — AWS EC2 Foundation Setup
# Commands Executed (Sequential / Paste-ready)
# ==========================================

# -------------------------------
# 0) Connect to EC2 (Run locally)
# -------------------------------
# chmod 400 your-key.pem
# ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>

# -------------------------------
# 1) Initial System Verification
# -------------------------------
whoami
hostname
uname -a
cat /etc/os-release

# -------------------------------
# 2) Network Verification (DO NOT SKIP)
# -------------------------------
ip a
ip route
ping -c 3 10.0.1.1
ping -c 3 8.8.8.8
curl -I https://google.com

# If DNS fails but 8.8.8.8 works:
# cat /etc/resolv.conf
# resolvectl status

# -------------------------------
# 3) Update & Base Tools
# -------------------------------
sudo apt update
sudo apt upgrade -y

sudo apt install -y \
  curl wget git unzip zip \
  net-tools dnsutils jq \
  ca-certificates gnupg lsb-release \
  software-properties-common \
  build-essential \
  htop nano vim \
  ufw

# -------------------------------
# 4) Timezone / NTP Setup
# -------------------------------
timedatectl

# Example timezone (change if needed)
sudo timedatectl set-timezone Asia/Baku

# Enable NTP sync
sudo timedatectl set-ntp yes

# Verify
timedatectl

# -------------------------------
# 5) Hostname Setup (Example: thehive)
# -------------------------------
hostnamectl

sudo hostnamectl set-hostname "thehive"

# Update /etc/hosts for local resolution
sudo nano /etc/hosts
# Change:
# 127.0.1.1 old-hostname
# To:
# 127.0.1.1 thehive

# Verify
hostnamectl
hostname -f

# -------------------------------
# 6) Create SOC Base Directory Layout (Optional but recommended)
# -------------------------------
mkdir -p ~/soc-ecosystem/{logs,scripts,configs,reports,evidence,installers,backups}
ls -la ~/soc-ecosystem

# -------------------------------
# 7) Basic Port/Service Visibility Checks
# -------------------------------
ss -tuln
df -h
free -h

# -------------------------------
# 8) Optional: Basic Firewall Baseline (UFW)
# -------------------------------
sudo ufw status verbose

# Allow SSH (IMPORTANT: do this before enabling UFW)
sudo ufw allow OpenSSH

# Enable firewall
sudo ufw enable

# Verify
sudo ufw status verbose

# -------------------------------
# 9) Optional: Create a Non-Root Admin User (Recommended)
# -------------------------------
# Replace "socadmin" with your preferred username
sudo adduser socadmin
sudo usermod -aG sudo socadmin

# Setup SSH directory for new user (if you want key-based login)
sudo mkdir -p /home/socadmin/.ssh
sudo chmod 700 /home/socadmin/.ssh

# Copy authorized_keys from current user (Ubuntu default user)
sudo cp ~/.ssh/authorized_keys /home/socadmin/.ssh/authorized_keys
sudo chown -R socadmin:socadmin /home/socadmin/.ssh
sudo chmod 600 /home/socadmin/.ssh/authorized_keys

# Test switching user
su - socadmin
exit

# -------------------------------
# 10) Optional: SSH Hardening (Key-only recommended)
# -------------------------------
# Backup config first
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Edit SSH config (manual edits)
sudo nano /etc/ssh/sshd_config

# Suggested settings (ensure you have key access before disabling password auth):
# PasswordAuthentication no
# PermitRootLogin no
# PubkeyAuthentication yes

# Restart SSH
sudo systemctl restart ssh
sudo systemctl status ssh --no-pager

# -------------------------------
# 11) Final Validation Checklist
# -------------------------------
ping -c 3 8.8.8.8
curl -I https://google.com
timedatectl
hostnamectl
ss -tuln
sudo ufw status verbose
