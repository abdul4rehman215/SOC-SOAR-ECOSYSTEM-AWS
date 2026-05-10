#!/usr/bin/env bash
set -euo pipefail
STAGED_POLICIES="${1:-/tmp/flow-b2-staging/manual/policies}"
ACTIVE_DIR="${AI_SECURITY_POLICY_ACTIVE_DIR:-/opt/ai-demo-v2/policies}"
DRY_RUN="${DRY_RUN:-true}"
if [ "$DRY_RUN" = "true" ]; then
  echo "DRY_RUN=true; would copy $STAGED_POLICIES to $ACTIVE_DIR"
  exit 0
fi
mkdir -p "$ACTIVE_DIR"
for d in mcp rag_memory agentic; do
  rm -rf "$ACTIVE_DIR/$d"
  cp -a "$STAGED_POLICIES/$d" "$ACTIVE_DIR/$d"
done
echo "activated_policy_bundles"
