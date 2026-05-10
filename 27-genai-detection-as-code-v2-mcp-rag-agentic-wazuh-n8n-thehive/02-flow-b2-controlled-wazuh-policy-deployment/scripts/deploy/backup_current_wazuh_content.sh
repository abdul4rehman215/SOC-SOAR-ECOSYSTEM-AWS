#!/usr/bin/env bash
set -euo pipefail
BACKUP_ROOT="${FLOW_B2_BACKUP_ROOT:-/opt/detection-ci/backups/flow-b2}"
RULES_DIR="${WAZUH_RULES_DIR:-/var/ossec/etc/rules}"
DECODERS_DIR="${WAZUH_DECODERS_DIR:-/var/ossec/etc/decoders}"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
DEST="$BACKUP_ROOT/$TS/wazuh"
mkdir -p "$DEST/rules" "$DEST/decoders"
for f in genai_mcp_rules.xml genai_rag_memory_rules.xml genai_agentic_rules.xml; do
  [ -f "$RULES_DIR/$f" ] && cp -a "$RULES_DIR/$f" "$DEST/rules/$f" || true
done
for f in genai_mcp_decoder.xml genai_rag_memory_decoder.xml genai_agentic_decoder.xml; do
  [ -f "$DECODERS_DIR/$f" ] && cp -a "$DECODERS_DIR/$f" "$DEST/decoders/$f" || true
done
echo "$DEST"
