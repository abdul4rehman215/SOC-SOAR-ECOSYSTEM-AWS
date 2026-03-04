#!/usr/bin/env bash
# ============================================================
# Project: Hunting Linux Credential Access Attacks using Auditd + Wazuh
# File: commands.sh
# Purpose: Full command history (clean, sequential, paste-ready)
# Notes:
# - Run sections on the correct host (Endpoint vs Wazuh Manager).
# - Replace placeholders like <ENDPOINT_IP> where needed.
# ============================================================

set -euo pipefail

# ------------------------------------------------------------
# SECTION 0 — (OPTIONAL) BASIC HOST CHECKS (ENDPOINT)
# ------------------------------------------------------------

whoami
hostname
uname -a
lsb_release -a || cat /etc/os-release
ip a
date

# ------------------------------------------------------------
# SECTION 1 — INSTALL & ENABLE AUDITD (LINUX ENDPOINT)
# ------------------------------------------------------------

sudo apt update
sudo apt -y install auditd audispd-plugins

sudo systemctl enable --now auditd
sudo systemctl status auditd --no-pager

# Verify audit subsystem is active
sudo auditctl -s

# ------------------------------------------------------------
# SECTION 2 — CREATE PERSISTENT AUDIT RULES (LINUX ENDPOINT)
# ------------------------------------------------------------

# Create rules file used for Wazuh SOC detections
sudo nano /etc/audit/rules.d/wazuh.rules

# Load persistent rules (preferred) and restart auditd
sudo augenrules --load
sudo systemctl restart auditd

# Verify loaded rules
sudo auditctl -l

# ------------------------------------------------------------
# SECTION 3 — LOCAL VALIDATION (ENDPOINT)
# ------------------------------------------------------------

# Generate test events (credential access + recon behaviors)
cat /etc/passwd | head
sudo cat /etc/shadow | head

# SSH key inspection (may not exist for every user; adjust path if needed)
cat ~/.ssh/authorized_keys 2>/dev/null || true

# Bash history access (may not exist; adjust if needed)
cat ~/.bash_history 2>/dev/null || true
sudo cat /root/.bash_history 2>/dev/null || true

# Credential hunting style commands
grep -i login /etc/passwd || true
grep -i password /etc/passwd || true

# View raw kernel audit log stream
sudo tail -n 50 /var/log/audit/audit.log
sudo tail -f /var/log/audit/audit.log

# Search events by keys
sudo ausearch -k passwd_access | tail -n 30
sudo ausearch -k shadow_access | tail -n 30
sudo ausearch -k bash_history | tail -n 30
sudo ausearch -k audit-wazuh-c | tail -n 30

# (Optional) Summary reports
sudo aureport -x --summary | head -n 50 || true
sudo aureport -f --summary | head -n 50 || true

# ------------------------------------------------------------
# SECTION 4 — WAZUH AGENT CONFIG (LINUX ENDPOINT)
# ------------------------------------------------------------

# Confirm Wazuh agent is installed and running
sudo systemctl status wazuh-agent --no-pager || true

# Add audit.log collection to agent config
sudo nano /var/ossec/etc/ossec.conf

# Restart agent to apply changes
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent --no-pager

# (Optional) Check agent logs for collection hints/errors
sudo tail -n 80 /var/ossec/logs/ossec.log || true

# ------------------------------------------------------------
# SECTION 5 — CREATE CDB LISTS (WAZUH MANAGER)
# ------------------------------------------------------------
# IMPORTANT: Run this section on the Wazuh Manager host

whoami
hostname
date

# Create audit key classification list
sudo nano /var/ossec/etc/lists/audit-keys

# Create suspicious programs classification list
sudo nano /var/ossec/etc/lists/suspicious-programs

# Register lists in Wazuh manager config
sudo nano /var/ossec/etc/ossec.conf

# Compile CDB lists
sudo /var/ossec/bin/wazuh-makelists

# Verify compiled CDBs exist
ls -l /var/ossec/etc/lists/
ls -l /var/ossec/etc/lists/*.cdb

# Restart manager
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager --no-pager

# ------------------------------------------------------------
# SECTION 6 — CREATE CUSTOM WAZUH RULES (WAZUH MANAGER)
# ------------------------------------------------------------
# IMPORTANT: Run this section on the Wazuh Manager host

# Edit local rules
sudo nano /var/ossec/etc/rules/local_rules.xml

# Restart manager to apply rules
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager --no-pager

# (Optional) Tail alerts for live validation
sudo tail -f /var/ossec/logs/alerts/alerts.log

# ------------------------------------------------------------
# SECTION 7 — ATTACK SIMULATION (ENDPOINT) + VALIDATION (MANAGER)
# ------------------------------------------------------------

# ---- On ENDPOINT (generate events again) ----
cat /etc/passwd | head
sudo cat /etc/shadow | head
cat ~/.ssh/authorized_keys 2>/dev/null || true
cat ~/.bash_history 2>/dev/null || true
grep -i login /etc/passwd || true

# Try suspicious tool executions (depends on what's installed)
gdb --help 2>/dev/null || true
tcpdump --help 2>/dev/null || true
strace -V 2>/dev/null || true
nc -h 2>/dev/null || true

# ---- On MANAGER (confirm alerts) ----
sudo tail -n 120 /var/ossec/logs/alerts/alerts.log

# (Optional) Confirm archives show raw events
sudo tail -n 120 /var/ossec/logs/archives/archives.log

# ------------------------------------------------------------
# SECTION 8 — TROUBLESHOOTING QUICK COMMANDS (BOTH)
# ------------------------------------------------------------

# Endpoint: auditd health
sudo systemctl status auditd --no-pager || true
sudo auditctl -s || true
sudo auditctl -l || true

# Endpoint: audit log location
ls -lah /var/log/audit/ || true

# Agent: health + logs
sudo systemctl status wazuh-agent --no-pager || true
sudo tail -n 120 /var/ossec/logs/ossec.log || true

# Manager: health + alerts
sudo systemctl status wazuh-manager --no-pager || true
sudo tail -n 120 /var/ossec/logs/alerts/alerts.log || true

echo "✅ commands.sh completed (sections run as needed)."
