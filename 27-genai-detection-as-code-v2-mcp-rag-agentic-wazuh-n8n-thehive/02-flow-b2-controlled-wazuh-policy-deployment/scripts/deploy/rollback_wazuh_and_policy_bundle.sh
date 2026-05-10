#!/usr/bin/env bash
set -euo pipefail
BACKUP_DIR="${1:-}"
if [ -z "$BACKUP_DIR" ]; then
  echo "usage: $0 <backup_dir_containing_wazuh_and_policies>" >&2
  exit 2
fi
RULES_DIR="${WAZUH_RULES_DIR:-/var/ossec/etc/rules}"
DECODERS_DIR="${WAZUH_DECODERS_DIR:-/var/ossec/etc/decoders}"
ACTIVE_POLICY_DIR="${AI_SECURITY_POLICY_ACTIVE_DIR:-/opt/ai-demo-v2/policies}"
DRY_RUN="${DRY_RUN:-true}"
if [ "$DRY_RUN" = "true" ]; then
  echo "DRY_RUN=true; would restore Wazuh XML and policies from $BACKUP_DIR"
  exit 0
fi
if [ -d "$BACKUP_DIR/wazuh/rules" ]; then cp -a "$BACKUP_DIR/wazuh/rules/"*.xml "$RULES_DIR/" || true; fi
if [ -d "$BACKUP_DIR/wazuh/decoders" ]; then cp -a "$BACKUP_DIR/wazuh/decoders/"*.xml "$DECODERS_DIR/" || true; fi
if [ -d "$BACKUP_DIR/policies/active" ]; then
  rm -rf "$ACTIVE_POLICY_DIR"
  mkdir -p "$(dirname "$ACTIVE_POLICY_DIR")"
  cp -a "$BACKUP_DIR/policies/active" "$ACTIVE_POLICY_DIR"
fi
sudo /var/ossec/bin/wazuh-analysisd -t
sudo systemctl restart wazuh-manager
echo "rollback_complete"
