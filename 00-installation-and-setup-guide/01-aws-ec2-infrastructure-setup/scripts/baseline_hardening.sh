#!/bin/bash
# ==========================================
# baseline_hardening.sh
# Purpose: Apply safe baseline hardening on Ubuntu EC2
# Scope: Lab/portfolio environment (SOC/SOAR foundation)
# Notes:
#  - Does NOT blindly close ports; focuses on safe defaults
#  - SSH hardening is included but requires key-based access
# ==========================================

set -euo pipefail

log() { echo -e "[+] $*"; }
warn() { echo -e "[!] $*" >&2; }

require_root() {
  if [[ "${EUID}" -ne 0 ]]; then
    warn "Run as root: sudo $0"
    exit 1
  fi
}

backup_file() {
  local f="$1"
  if [[ -f "$f" ]]; then
    local ts
    ts="$(date +%Y%m%d_%H%M%S)"
    cp -a "$f" "${f}.backup_${ts}"
    log "Backup created: ${f}.backup_${ts}"
  fi
}

install_base_packages() {
  log "Updating packages and installing baseline utilities..."
  apt update -y
  apt upgrade -y

  apt install -y \
    curl wget git unzip zip \
    net-tools dnsutils jq \
    ca-certificates gnupg lsb-release \
    software-properties-common \
    build-essential \
    htop nano vim \
    ufw fail2ban \
    chrony

  log "Base packages installed."
}

configure_time_sync() {
  log "Configuring NTP time sync..."

  # Prefer timedatectl if systemd-timesyncd is present
  if command -v timedatectl >/dev/null 2>&1; then
    timedatectl set-ntp true || true
    log "timedatectl NTP enabled."
  fi

  # Chrony is reliable on servers; enable if installed
  if systemctl list-unit-files | grep -q '^chrony\.service'; then
    systemctl enable --now chrony
    log "Chrony enabled and started."
  fi

  timedatectl || true
}

configure_sysctl_baseline() {
  log "Applying sysctl baseline settings..."

  local sysctl_file="/etc/sysctl.d/99-soc-baseline.conf"
  backup_file "$sysctl_file"

  cat > "$sysctl_file" <<'EOF'
# ==========================================
# SOC EC2 Baseline Hardening (sysctl)
# ==========================================

# IP spoofing protection
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.default.accept_redirects=0
net.ipv6.conf.all.accept_redirects=0
net.ipv6.conf.default.accept_redirects=0

# Do not send ICMP redirects
net.ipv4.conf.all.send_redirects=0
net.ipv4.conf.default.send_redirects=0

# Disable source routing
net.ipv4.conf.all.accept_source_route=0
net.ipv4.conf.default.accept_source_route=0
net.ipv6.conf.all.accept_source_route=0
net.ipv6.conf.default.accept_source_route=0

# Log suspicious packets
net.ipv4.conf.all.log_martians=1
net.ipv4.conf.default.log_martians=1

# TCP SYN cookies
net.ipv4.tcp_syncookies=1

# Reasonable TCP hardening
net.ipv4.tcp_timestamps=0
net.ipv4.tcp_sack=1

# Reduce risk from kernel pointers
kernel.kptr_restrict=2

# Restrict dmesg for non-root
kernel.dmesg_restrict=1
EOF

  sysctl --system
  log "sysctl baseline applied."
}

configure_ssh_hardening() {
  log "Configuring SSH hardening (safe defaults)..."

  local sshd="/etc/ssh/sshd_config"
  if [[ ! -f "$sshd" ]]; then
    warn "sshd_config not found. Skipping SSH hardening."
    return 0
  fi

  backup_file "$sshd"

  # Ensure we do not lock the user out:
  # - We keep PasswordAuthentication as-is unless explicitly toggled.
  # - We enforce PermitRootLogin no where possible.
  #
  # If you want strict key-only login:
  # - set PasswordAuthentication no
  # - ensure your key login works first

  # Set PermitRootLogin no (idempotent)
  if grep -qE '^\s*PermitRootLogin' "$sshd"; then
    sed -i 's/^\s*PermitRootLogin.*/PermitRootLogin no/' "$sshd"
  else
    echo "PermitRootLogin no" >> "$sshd"
  fi

  # Ensure PubkeyAuthentication yes
  if grep -qE '^\s*PubkeyAuthentication' "$sshd"; then
    sed -i 's/^\s*PubkeyAuthentication.*/PubkeyAuthentication yes/' "$sshd"
  else
    echo "PubkeyAuthentication yes" >> "$sshd"
  fi

  # Reduce SSH brute force surface (reasonable defaults)
  if grep -qE '^\s*MaxAuthTries' "$sshd"; then
    sed -i 's/^\s*MaxAuthTries.*/MaxAuthTries 4/' "$sshd"
  else
    echo "MaxAuthTries 4" >> "$sshd"
  fi

  if grep -qE '^\s*LoginGraceTime' "$sshd"; then
    sed -i 's/^\s*LoginGraceTime.*/LoginGraceTime 30/' "$sshd"
  else
    echo "LoginGraceTime 30" >> "$sshd"
  fi

  if grep -qE '^\s*ClientAliveInterval' "$sshd"; then
    sed -i 's/^\s*ClientAliveInterval.*/ClientAliveInterval 300/' "$sshd"
  else
    echo "ClientAliveInterval 300" >> "$sshd"
  fi

  if grep -qE '^\s*ClientAliveCountMax' "$sshd"; then
    sed -i 's/^\s*ClientAliveCountMax.*/ClientAliveCountMax 2/' "$sshd"
  else
    echo "ClientAliveCountMax 2" >> "$sshd"
  fi

  systemctl restart ssh
  systemctl status ssh --no-pager
  log "SSH hardening applied (without forcing password disable)."
}

configure_fail2ban_baseline() {
  log "Configuring Fail2Ban baseline (sshd)..."

  local jail_local="/etc/fail2ban/jail.local"
  backup_file "$jail_local"

  cat > "$jail_local" <<'EOF'
[DEFAULT]
# Ban time in seconds
bantime  = 3600
findtime = 600
maxretry = 5

# Backend
backend = systemd

# Destination email (optional)
# destemail = root@localhost
# sender = fail2ban@localhost

[sshd]
enabled = true
port    = ssh
logpath = %(sshd_log)s
EOF

  systemctl enable --now fail2ban
  systemctl restart fail2ban
  fail2ban-client status sshd || true
  log "Fail2Ban baseline configured."
}

create_soc_directories() {
  log "Creating SOC base directory structure..."

  local base="/opt/soc-lab"
  mkdir -p "$base"/{logs,scripts,configs,reports,evidence,installers,backups}
  chmod 755 "$base"
  log "SOC directories created at: $base"
  ls -la "$base"
}

main() {
  require_root
  install_base_packages
  configure_time_sync
  configure_sysctl_baseline
  configure_ssh_hardening
  configure_fail2ban_baseline
  create_soc_directories
  log "Baseline hardening completed successfully."
}

main "$@"
