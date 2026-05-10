#!/usr/bin/env bash
set -euo pipefail
BACKUP_ROOT="${FLOW_B2_BACKUP_ROOT:-/opt/detection-ci/backups/flow-b2}"
ACTIVE_DIR="${AI_SECURITY_POLICY_ACTIVE_DIR:-/opt/ai-demo-v2/policies}"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
DEST="$BACKUP_ROOT/$TS/policies"
mkdir -p "$DEST"
if [ -d "$ACTIVE_DIR" ]; then
  cp -a "$ACTIVE_DIR/." "$DEST/"
fi
echo "$DEST"
