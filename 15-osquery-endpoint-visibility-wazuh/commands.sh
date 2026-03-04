# ================================
# SYSTEM UPDATE
# ================================

sudo apt update
sudo apt upgrade -y


# ================================
# INSTALL REQUIRED DEPENDENCIES
# ================================

sudo apt install curl gnupg lsb-release apt-transport-https -y


# ================================
# ADD OSQUERY REPOSITORY KEY
# ================================

curl -L https://pkg.osquery.io/deb/pubkey.gpg | sudo apt-key add -


# ================================
# ADD OSQUERY REPOSITORY
# ================================

sudo add-apt-repository "deb [arch=amd64] https://pkg.osquery.io/deb deb main"


# ================================
# UPDATE REPOSITORY LIST
# ================================

sudo apt update


# ================================
# INSTALL OSQUERY
# ================================

sudo apt install osquery -y


# ================================
# VERIFY OSQUERY INSTALLATION
# ================================

osqueryi --version


# ================================
# START OSQUERY INTERACTIVE SHELL
# ================================

osqueryi


# ================================
# EXPLORE OSQUERY SCHEMA
# ================================

.schema


# ================================
# QUERY LOCAL USERS
# ================================

SELECT * FROM users;


# ================================
# VIEW LISTENING PORTS
# ================================

SELECT pid, port, protocol, address FROM listening_ports;


# ================================
# VIEW INSTALLED PACKAGES
# ================================

SELECT name, version FROM deb_packages LIMIT 10;


# ================================
# VIEW OPEN NETWORK CONNECTIONS
# ================================

SELECT pid, local_address, remote_address, remote_port FROM process_open_sockets LIMIT 10;


# ================================
# VIEW SCHEDULED TASKS (CRON JOBS)
# ================================

SELECT * FROM crontab;


# ================================
# EXIT OSQUERY INTERACTIVE SHELL
# ================================

.exit


# ================================
# CREATE OSQUERY CONFIG DIRECTORY
# ================================

sudo mkdir -p /etc/osquery


# ================================
# CREATE OSQUERY CONFIG FILE
# ================================

sudo nano /etc/osquery/osquery.conf


# ================================
# RESTART OSQUERY SERVICE
# ================================

sudo systemctl restart osqueryd


# ================================
# CHECK OSQUERY SERVICE STATUS
# ================================

sudo systemctl status osqueryd


# ================================
# VERIFY OSQUERY LOG GENERATION
# ================================

sudo tail -f /var/log/osquery/osqueryd.results.log


# ================================
# CONFIGURE WAZUH AGENT FOR OSQUERY
# ================================

sudo nano /var/ossec/etc/ossec.conf


# ================================
# RESTART WAZUH AGENT
# ================================

sudo systemctl restart wazuh-agent


# ================================
# CREATE OSQUERY RULES FILE
# ================================

sudo nano /var/ossec/etc/rules/osquery_rules.xml


# ================================
# RESTART WAZUH MANAGER
# ================================

sudo systemctl restart wazuh-manager


# ================================
# VERIFY OSQUERY EVENTS IN WAZUH
# ================================

sudo tail -f /var/ossec/logs/ossec.log


# ================================
# CHECK WAZUH AGENT STATUS
# ================================

sudo systemctl status wazuh-agent


# ================================
# CHECK WAZUH MANAGER STATUS
# ================================

sudo systemctl status wazuh-manager
