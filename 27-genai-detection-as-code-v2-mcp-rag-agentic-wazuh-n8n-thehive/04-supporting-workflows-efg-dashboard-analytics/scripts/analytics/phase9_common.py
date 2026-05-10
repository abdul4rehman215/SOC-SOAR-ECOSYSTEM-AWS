#!/usr/bin/env python3
from __future__ import annotations
import csv, json, os, re, sys, hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

RULE_FAMILY_DEFAULTS = {
    100301: 'mcp_tool_poisoning', 100302: 'mcp_schema_drift', 100303: 'mcp_overprivileged_tool',
    100304: 'mcp_sensitive_tool_without_hitl', 100305: 'mcp_tool_argument_injection', 100306: 'mcp_resource_exfiltration',
    100401: 'rag_context_poisoning', 100402: 'memory_poisoning_attempt', 100403: 'memory_scope_violation',
    100404: 'unapproved_embedding_source', 100405: 'retrieval_to_tool_escalation',
    100351: 'agent_goal_hijack', 100352: 'agent_plan_drift_tool_chain_escalation', 100353: 'agent_tool_loop_unbounded_consumption',
    100354: 'agent_approval_manipulation', 100355: 'agent_identity_permission_mismatch', 100356: 'agent_confused_deputy_multi_server',
    100357: 'agent_excessive_agency_rogue_action', 100358: 'agent_continued_action_after_blocked_risk'
}

def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def stable_id(prefix: str, *parts: Any) -> str:
    raw = '|'.join(str(p) for p in parts)
    return f"{prefix}-{hashlib.sha256(raw.encode()).hexdigest()[:16]}"

def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        if default is not None: return default
        raise

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')

def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not fieldnames:
        keys = []
        for row in rows:
            for k in row.keys():
                if k not in keys: keys.append(k)
        fieldnames = keys or ['empty']
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, '') for k in fieldnames})

def parse_expected_rule_from_event(path: Path) -> Optional[int]:
    try:
        obj = read_json(path)
    except Exception:
        return None
    val = obj.get('expected_wazuh_rule_id') or obj.get('rule_id')
    try: return int(val)
    except Exception: return None

def load_simple_yml_mapping(path: Path) -> Dict[str, int]:
    mapping: Dict[str, int] = {}
    if not path.exists(): return mapping
    for line in path.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if not s or s.startswith('#') or ':' not in s: continue
        k, v = s.split(':', 1)
        k = k.strip().strip('"\'')
        m = re.search(r'\d{6}', v)
        if m: mapping[k] = int(m.group(0))
    return mapping

def family_for_rule(rule_id: int, fallback: str='unknown') -> str:
    return RULE_FAMILY_DEFAULTS.get(int(rule_id or 0), fallback)

def boolish(v: Any) -> bool:
    if isinstance(v, bool): return v
    if v is None: return False
    return str(v).strip().lower() in ('true','1','yes','y','missing','bypassed','denied','exceeds_policy','mismatch')
