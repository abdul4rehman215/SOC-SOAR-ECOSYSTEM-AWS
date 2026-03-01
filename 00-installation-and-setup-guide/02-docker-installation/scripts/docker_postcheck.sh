#!/bin/bash
# ==========================================
# docker_postcheck.sh
# Purpose: Post-install validation and readiness checks for Docker
# OS: Ubuntu 22.04 / 24.04
# Output: Human-readable checks for Docker Engine + Compose plugin
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

section "System Info"
uname -a || true
cat /etc/os-release || true
whoami || true
id || true

section "Docker Service Status"
if systemctl list-unit-files | grep -q '^docker\.service'; then
  systemctl status docker --no-pager || true
else
  warn "docker.service not found. Docker may not be installed."
fi

section "Docker Version Checks"
if cmd_exists docker; then
  docker --version || true
else
  warn "docker not found in PATH."
fi

if cmd_exists docker; then
  # Docker compose plugin uses: docker compose version
  docker compose version || warn "docker compose plugin not available."
fi

section "Docker Socket Permissions"
if [[ -S /var/run/docker.sock ]]; then
  ls -l /var/run/docker.sock
else
  warn "Docker socket not found at /var/run/docker.sock"
fi

section "Docker Group Membership"
# User must be in docker group to run docker without sudo
if getent group docker >/dev/null 2>&1; then
  log "docker group exists."
  getent group docker
else
  warn "docker group not found. Docker may not be fully installed."
fi

# Check if current user is in docker group
if id -nG "$USER" | grep -qw docker; then
  log "User '$USER' is in the docker group."
else
  warn "User '$USER' is NOT in the docker group."
  warn "Fix: sudo usermod -aG docker $USER && newgrp docker (or logout/login)"
fi

section "Connectivity Check (Optional but helpful)"
# Docker needs internet to pull images
ping -c 2 8.8.8.8 || warn "Ping 8.8.8.8 failed (network issue)."
curl -I --max-time 5 https://registry-1.docker.io >/dev/null 2>&1 \
  && log "Docker registry reachable." \
  || warn "Docker registry not reachable (DNS/egress issue)."

section "Hello-World Test"
if cmd_exists docker; then
  log "Running: docker run hello-world"
  docker run hello-world || warn "hello-world failed. Check daemon or permissions."
fi

section "Docker Info (Summary)"
if cmd_exists docker; then
  docker info || warn "docker info failed. Check daemon and permissions."
fi

section "Done"
log "Docker post-check completed."
