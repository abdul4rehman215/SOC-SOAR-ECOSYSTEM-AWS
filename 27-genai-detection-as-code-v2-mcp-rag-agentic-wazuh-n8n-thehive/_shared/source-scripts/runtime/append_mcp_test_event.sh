#!/usr/bin/env bash
set -euo pipefail

SCENARIO="${1:-tool_poisoning}"
LOG_FILE="${2:-/var/log/ai-demo/mcp-events.jsonl}"
REPO_ROOT="${3:-$(pwd)}"

python3 "$REPO_ROOT/scripts/runtime/generate_mcp_events.py" \
  --repo-root "$REPO_ROOT" \
  --scenario "$SCENARIO" \
  --log-file "$LOG_FILE"
