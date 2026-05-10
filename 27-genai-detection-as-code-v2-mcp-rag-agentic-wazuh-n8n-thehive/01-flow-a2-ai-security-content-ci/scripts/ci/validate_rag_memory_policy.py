#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, load_json, require_files

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    required = [
      "policies/rag_memory/rag_memory_policy_bundle.json",
      "policies/rag_memory/source_trust_policy.json",
      "policies/rag_memory/memory_write_policy.json",
      "policies/rag_memory/embedding_source_policy.json"
    ]
    present, missing = require_files(root, required); failures, warnings = [], []
    if missing: failures.append("Missing RAG/memory policy files: " + ", ".join(missing))
    for rel in present:
        data = load_json(root/rel)
        if not isinstance(data, dict): failures.append(f"{rel}: policy must be JSON object")
    bundle = root/"policies/rag_memory/rag_memory_policy_bundle.json"
    if bundle.exists():
        data = load_json(bundle)
        for key in ["trusted_sources", "untrusted_sources", "allowed_memory_scopes"]:
            if key not in data: warnings.append(f"{bundle.relative_to(root)} missing optional key {key}")
    print_result("validate_rag_memory_policy", "fail" if failures else "pass", files_present=present, failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
