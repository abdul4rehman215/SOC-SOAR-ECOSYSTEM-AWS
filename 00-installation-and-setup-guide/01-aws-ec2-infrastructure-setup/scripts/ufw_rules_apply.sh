#!/bin/bash
# ==========================================
# ufw_rules_apply.sh
# Purpose: Apply a minimal UFW firewall baseline
# Default: Allow SSH, deny inbound by default, allow outbound
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

main() {
  require_root

  log "Resetting UFW to a clean state..."
  ufw --force reset

  log "Setting defaults: deny incoming, allow outgoing..."
  ufw default deny incoming
  ufw default allow outgoing

  log "Allowing SSH (OpenSSH profile)..."
  ufw allow OpenSSH

  # Optional: allow HTTPS if this host will expose dashboards later
  # ufw allow 443/tcp

  log "Enabling UFW..."
  ufw --force enable

  log "UFW status:"
  ufw status verbose
}

main "$@"
