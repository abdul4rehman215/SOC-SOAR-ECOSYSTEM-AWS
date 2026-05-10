#!/usr/bin/env bash
set -euo pipefail
STAGED_WAZUH="${1:-/tmp/flow-b2-staging/manual/wazuh}"
RULES_DIR="${WAZUH_RULES_DIR:-/var/ossec/etc/rules}"
DECODERS_DIR="${WAZUH_DECODERS_DIR:-/var/ossec/etc/decoders}"
DRY_RUN="${DRY_RUN:-true}"
if [ "$DRY_RUN" = "true" ]; then
  echo "DRY_RUN=true; would copy $STAGED_WAZUH/rules/*.xml to $RULES_DIR and decoders to $DECODERS_DIR"
  exit 0
fi
mkdir -p "$RULES_DIR" "$DECODERS_DIR"
cp -a "$STAGED_WAZUH/rules/"*.xml "$RULES_DIR/"
cp -a "$STAGED_WAZUH/decoders/"*.xml "$DECODERS_DIR/"
echo "activated_wazuh_content"
