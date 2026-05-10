#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from phase9_common import utcnow, stable_id, read_json, write_json, boolish

def score_event(e):
    reasons = []
    risk = int(e.get('risk_score') or 0)
    if e.get('tool_allowed') is False or e.get('tool_allowlist_status') in ('not_allowlisted','blocked'):
        reasons.append('tool_not_allowlisted'); risk = max(risk, 90)
    if e.get('schema_hash_status') in ('mismatch','missing') or (e.get('schema_hash_expected') and e.get('schema_hash_observed') and e.get('schema_hash_expected') != e.get('schema_hash_observed')):
        reasons.append('schema_hash_mismatch'); risk = max(risk, 92)
    if e.get('permission_scope_status') in ('exceeds_policy','denied','broader_than_allowed'):
        reasons.append('scope_exceeds_policy'); risk = max(risk, 90)
    if e.get('approval_required') is True and e.get('approval_status') in ('missing','bypassed','denied',''):
        reasons.append('approval_missing_or_bypassed'); risk = max(risk, 98)
    if e.get('resource_scope_violation') is True:
        reasons.append('resource_scope_violation'); risk = max(risk, 97)
    if e.get('tool_result_risk_flags_csv'):
        reasons.append('tool_result_risk'); risk = max(risk, 95)
    violation = bool(reasons) or str(e.get('guardrail_action','')).lower() == 'block'
    severity = 'critical' if risk >= 95 else 'high' if risk >= 80 else 'medium' if risk >= 50 else 'low'
    return violation, risk, severity, reasons

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--event-json', required=True)
    ap.add_argument('--output-json', required=True)
    args = ap.parse_args()
    event = read_json(Path(args.event_json))
    violation, risk, severity, reasons = score_event(event)
    now = utcnow()
    monitor_event_id = stable_id('flowe', event.get('request_id','no-request'), event.get('tool_name','no-tool'), now[:10])
    row = {
      'monitor_event_id': monitor_event_id, 'timestamp': event.get('timestamp') or now,
      'request_id': event.get('request_id',''), 'session_id': event.get('session_id',''), 'user_id': event.get('user_id',''),
      'agent_id': event.get('agent_id',''), 'mcp_server_name': event.get('mcp_server_name',''), 'tool_name': event.get('tool_name',''),
      'tool_allowed': bool(event.get('tool_allowed', False)), 'schema_hash_status': event.get('schema_hash_status',''),
      'permission_scope_status': event.get('permission_scope_status',''), 'approval_required': bool(event.get('approval_required', False)),
      'approval_status': event.get('approval_status',''), 'resource_scope_violation': bool(event.get('resource_scope_violation', False)),
      'tool_result_risk': bool(event.get('tool_result_risk_flags_csv','')), 'policy_violation': violation,
      'violation_type': ','.join(reasons) if reasons else 'none', 'severity': severity, 'risk_score': risk,
      'guardrail_action': event.get('guardrail_action','block' if violation else 'allow'),
      'risk_flags_csv': ','.join(reasons) if reasons else event.get('risk_flags_csv',''),
      'slack_notified': False, 'thehive_alert_id': '', 'status': 'policy_violation' if violation else 'allowed',
      'raw_event_json': json.dumps(event, sort_keys=True)
    }
    result = {
      'flow': 'Flow E - MCP Runtime Policy Monitor', 'decision': 'violation' if violation else 'allow',
      'policy_violation': violation, 'risk_score': risk, 'severity': severity, 'reasons': reasons,
      'monitor_event_row': row,
      'slack_text': f"Flow E MCP policy monitor: {'VIOLATION' if violation else 'ALLOW'} | tool={event.get('tool_name')} | risk={risk} | reasons={','.join(reasons) or 'none'}",
      'dashboard_metric_rows': [
        {'metric_id': stable_id('metric', 'mcp_policy_events_total', now[:10]), 'window_start': now[:10]+'T00:00:00Z', 'window_end': now, 'metric_name': 'mcp_policy_events_total', 'metric_value': 1, 'dimension_key': 'flow', 'dimension_value': 'flow_e', 'source_table': 'flow_v2_mcp_policy_monitor_events', 'generated_at': now, 'notes': 'Flow E direct policy event'},
        {'metric_id': stable_id('metric', 'mcp_policy_violations_total', now[:10], str(violation)), 'window_start': now[:10]+'T00:00:00Z', 'window_end': now, 'metric_name': 'mcp_policy_violations_total', 'metric_value': 1 if violation else 0, 'dimension_key': 'flow', 'dimension_value': 'flow_e', 'source_table': 'flow_v2_mcp_policy_monitor_events', 'generated_at': now, 'notes': ','.join(reasons) or 'no violation'}
      ]
    }
    write_json(Path(args.output_json), result)
    print(json.dumps(result, indent=2))
if __name__ == '__main__': main()
