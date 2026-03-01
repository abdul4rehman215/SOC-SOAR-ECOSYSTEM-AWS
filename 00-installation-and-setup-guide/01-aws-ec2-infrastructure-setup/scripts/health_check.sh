#!/bin/bash
# ==========================================
# health_check.sh
# Purpose: Quick validation checks for EC2 readiness
# Output: Human-readable status + key network checks
# ==========================================

set -euo pipefail

log() { echo -e "[+] $*"; }
warn() { echo -e "[!] $*" >&2; }

section() {
  echo
  echo "============================================================"
  echo "$1"
  echo "============================================================"
}

cmd_exists() { command -v "$1" >/dev/null 2>&1; }

section "System Identity"
whoami || true
hostnamectl || true
uname -a || true
cat /etc/os-release || true

section "Time / NTP"
if cmd_exists timedatectl; then
  timedatectl || true
else
  warn "timedatectl not found"
fi

if systemctl list-unit-files | grep -q '^chrony\.service'; then
  systemctl status chrony --no-pager || true
fi

section "Network Interfaces"
ip a || true
ip route || true

section "Connectivity Tests"
# Default gateway test (AWS typical)
GW_IP="$(ip route | awk '/default/ {print $3; exit}')"
if [[ -n "${GW_IP}" ]]; then
  log "Default gateway detected: ${GW_IP}"
  ping -c 2 "${GW_IP}" || warn "Gateway ping failed: ${GW_IP}"
else
  warn "No default gateway detected."
fi

ping -c 2 8.8.8.8 || warn "Ping to 8.8.8.8 failed (routing/egress issue)."

# DNS test
if cmd_exists getent; then
  getent hosts google.com >/dev/null 2>&1 && log "DNS resolution OK (google.com)" || warn "DNS resolution failed (google.com)"
else
  warn "getent not found; skipping DNS check"
fi

# HTTP(S) test
if cmd_exists curl; then
  curl -I --max-time 5 https://google.com >/dev/null 2>&1 && log "HTTPS connectivity OK (google.com)" || warn "HTTPS connectivity failed (google.com)"
else
  warn "curl not installed"
fi

section "Open Ports / Listening Services"
if cmd_exists ss; then
  ss -tuln || true
else
  warn "ss not found"
fi

section "Disk / Memory"
df -h || true
free -h || true

section "Firewall Status"
if cmd_exists ufw; then
  ufw status verbose || true
else
  warn "ufw not installed"
fi

section "Fail2Ban Status"
if cmd_exists fail2ban-client; then
  fail2ban-client status sshd || true
else
  warn "fail2ban-client not installed"
fi

section "Done"
log "Health check completed."
