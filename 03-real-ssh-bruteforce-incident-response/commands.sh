#!/bin/bash

# =========================
# REAL SSH BRUTE FORCE IR
# =========================

# -------------------------
# 1. Validate SSH logs
# -------------------------
sudo tail -f /var/log/auth.log

# -------------------------
# 2. Identify attacker IP
# -------------------------
grep "Invalid user" /var/log/auth.log

# -------------------------
# 3. Block attacker IP
# -------------------------
sudo iptables -A INPUT -s <ATTACKER_IP> -j DROP

# Verify rule
sudo iptables -L -n --line-numbers

# -------------------------
# 4. Install Fail2Ban
# -------------------------
sudo apt update
sudo apt install fail2ban -y

sudo systemctl enable fail2ban
sudo systemctl start fail2ban

sudo systemctl status fail2ban

# -------------------------
# 5. Harden SSH Configuration
# -------------------------
sudo nano /etc/ssh/sshd_config

# Modify:
# PermitRootLogin no
# PasswordAuthentication no

sudo systemctl restart ssh

# -------------------------
# 6. Verify SSH service
# -------------------------
sudo systemctl status ssh

# -------------------------
# 7. Optional: Remove test rule
# -------------------------
# sudo iptables -D INPUT <rule_number>

# =========================
# End of Incident Response Commands
# =========================
