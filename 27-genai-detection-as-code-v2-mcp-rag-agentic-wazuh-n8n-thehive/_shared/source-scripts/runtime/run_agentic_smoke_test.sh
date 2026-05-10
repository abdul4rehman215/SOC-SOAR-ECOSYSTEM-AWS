#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
LOG_FILE="${2:-/tmp/agentic-events-smoke.jsonl}"
rm -f "$LOG_FILE"
python3 "$REPO_ROOT/scripts/runtime/run_agentic_scenarios.py" --repo-root "$REPO_ROOT" --scenario all --log-file "$LOG_FILE"
echo "[OK] smoke log written: $LOG_FILE"
echo "[OK] event count: $(wc -l < "$LOG_FILE")"
python3 - "$LOG_FILE" <<'PY'
import json, sys
path=sys.argv[1]
ids=[]
for line in open(path, encoding='utf-8'):
    ids.append(json.loads(line)['expected_wazuh_rule_id'])
print('[OK] expected_wazuh_rule_ids=' + ','.join(str(i) for i in ids))
assert ids == [100350,100351,100352,100353,100354,100355,100356,100357,100358]
PY
