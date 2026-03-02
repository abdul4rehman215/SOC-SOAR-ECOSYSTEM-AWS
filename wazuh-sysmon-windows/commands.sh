########################################
# WAZUH MANAGER - LINUX
########################################

# Install Wazuh
curl -sO https://packages.wazuh.com/4.x/wazuh-install.sh
bash wazuh-install.sh -a

# Restart manager
systemctl restart wazuh-manager

# Check agent status
/var/ossec/bin/agent_control -l

# View incoming logs
tail -f /var/ossec/logs/archives/archives.json


########################################
# WINDOWS - SYS MON INSTALL
########################################

cd C:\Sysmon
.\Sysmon64.exe -accepteula -i sysmon_config.xml

# Reconfigure
.\Sysmon64.exe -c sysmon_config.xml

# Uninstall
.\Sysmon64.exe -u


########################################
# WINDOWS - WAZUH AGENT
########################################

Restart-Service Wazuh

########################################
# TEST COMMANDS
########################################

# Normal PowerShell
powershell.exe -Command "Get-Date"

# Encoded PowerShell
$cmd = "Get-Date"
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd))
powershell.exe -EncodedCommand $encoded

# DNS Test
nslookup example.com
