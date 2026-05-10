#!/usr/bin/env bash
set -euo pipefail
COMMIT="${1:-}"
if [ -z "$COMMIT" ]; then
  echo "usage: $0 <approved_commit_sha>" >&2
  exit 2
fi
git fetch --all --prune
git checkout "$COMMIT"
git rev-parse HEAD
