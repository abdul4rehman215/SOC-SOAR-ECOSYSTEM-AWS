#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="${1:-.}"
LOG_FILE="${2:-/tmp/rag-memory-smoke-events.jsonl}"
cd "$REPO_ROOT"
rm -f "$LOG_FILE"
python3 scripts/runtime/run_rag_memory_scenarios.py --scenario all --repo-root . --log-file "$LOG_FILE"
echo "[OK] wrote smoke events to $LOG_FILE"
echo "[INFO] expected 6 events:"
wc -l "$LOG_FILE"
echo "[INFO] request ids:"
grep -o '"request_id":"[^"]*"' "$LOG_FILE" | sed 's/"request_id":"//;s/"//'
