#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
REQUIRED = {
    'mcp': ['mcp_policy_bundle.json', 'mcp_tool_registry.json', 'mcp_resource_roots.json'],
    'rag_memory': ['rag_memory_policy_bundle.json', 'source_trust_policy.json', 'memory_write_policy.json', 'embedding_source_policy.json'],
    'agentic': ['agentic_policy_bundle.json', 'approval_prompt_policy.json', 'identity_scope_policy.json', 'loop_threshold_policy.json', 'confused_deputy_policy.json'],
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--policy-dir', default='/tmp/flow-b2-staging/manual/policies')
    args = ap.parse_args()
    root = Path(args.policy_dir)
    failures = []
    checked = []
    for subdir, names in REQUIRED.items():
        for name in names:
            p = root / subdir / name
            if not p.exists():
                failures.append(f'missing {p}')
                continue
            checked.append(str(p))
            if name.endswith('.json'):
                json.loads(p.read_text(encoding='utf-8'))
    result = {'status': 'pass' if not failures else 'fail', 'checked': checked, 'failures': failures}
    print(json.dumps(result, indent=2))
    return 0 if not failures else 2
if __name__ == '__main__':
    raise SystemExit(main())
