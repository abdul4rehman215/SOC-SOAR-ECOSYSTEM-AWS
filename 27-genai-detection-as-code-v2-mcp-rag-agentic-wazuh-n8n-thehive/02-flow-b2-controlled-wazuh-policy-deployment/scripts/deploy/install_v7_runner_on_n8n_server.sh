#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="${1:-/opt/detection-ci/wazuh-genai-ci}"
SCRIPT_SRC="$(cd "$(dirname "$0")" && pwd)/run_flow_b2_local_deploy.py"
SCRIPT_DST="$REPO_ROOT/scripts/deploy/run_flow_b2_local_deploy.py"
if [ ! -f "$SCRIPT_SRC" ]; then
  echo "missing $SCRIPT_SRC" >&2
  exit 1
fi
sudo mkdir -p "$(dirname "$SCRIPT_DST")"
sudo cp "$SCRIPT_SRC" "$SCRIPT_DST"
sudo chmod 755 "$SCRIPT_DST"
sudo chown root:root "$SCRIPT_DST" 2>/dev/null || true
sudo mkdir -p /tmp/flowb/worktrees /tmp/flowb/stage /tmp/flowb/policy-backups /tmp/flowb/active-policies
sudo chmod -R 777 /tmp/flowb
printf '[OK] installed Flow B2 V7 deploy runner to %s\n' "$SCRIPT_DST"
printf '[OK] fixed remote ssh bash -lc quoting and kept isolated worktree checkout\n'
