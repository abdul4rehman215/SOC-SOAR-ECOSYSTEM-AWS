# ==============================
# Apache Setup (Client Machine)
# ==============================

sudo apt update
sudo apt install apache2 -y
sudo systemctl enable apache2
sudo systemctl start apache2
sudo systemctl status apache2

# ==============================
# Restart Wazuh Agent
# ==============================

sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent

# ==============================
# Attack Simulation (Kali)
# ==============================

for i in {1..300}; do
  curl http://TARGET_IP/test$i > /dev/null
done

# ==============================
# Log Monitoring
# ==============================

sudo tail -f /var/log/apache2/access.log

# ==============================
# Mitigation - Block Attacker
# ==============================

sudo iptables -A INPUT -s ATTACKER_IP -j DROP
sudo iptables -L -n --line-numbers

# ==============================
# Apache Hardening
# ==============================

sudo a2enmod ratelimit
sudo a2enmod security2
sudo systemctl restart apache2
