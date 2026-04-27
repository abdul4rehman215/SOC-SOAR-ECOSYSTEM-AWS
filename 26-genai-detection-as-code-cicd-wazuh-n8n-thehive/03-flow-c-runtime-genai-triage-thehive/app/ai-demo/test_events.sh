#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:8008}"

echo "[1/4] Direct prompt injection -> expected Wazuh rule 100201"
curl -sS -X POST "$BASE_URL/demo/direct-prompt-injection" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"student-user-demo"}'
echo
echo

sleep 1

echo "[2/4] Indirect injection -> expected Wazuh rule 100202"
curl -sS -X POST "$BASE_URL/demo/indirect-injection" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"student-user-demo"}'
echo
echo

sleep 1

echo "[3/4] Improper output handling -> expected Wazuh rule 100203"
curl -sS -X POST "$BASE_URL/demo/improper-output-handling" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"student-user-demo"}'
echo
echo

sleep 1

echo "[4/4] Benign event -> should not trigger 100201/100202/100203"
curl -sS -X POST "$BASE_URL/demo/benign" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"student-user-demo"}'
echo
echo

echo "Last 5 JSONL events:"
tail -n 5 /var/log/ai-demo/guardrail-events.jsonl
