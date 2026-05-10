#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from phase9_common import utcnow, stable_id, write_json, read_json

def add(rows, name, value, source, notes='', dim_key='aggregate', dim_val='all'):
    now = utcnow()
    rows.append({'metric_id': stable_id('metric', name, dim_key, dim_val, now[:10]), 'window_start': now[:10]+'T00:00:00Z', 'window_end': now, 'metric_name': name, 'metric_value': float(value or 0), 'dimension_key': dim_key, 'dimension_value': dim_val, 'source_table': source, 'generated_at': now, 'notes': notes})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--regression-json', default='')
    ap.add_argument('--fp-json', default='')
    ap.add_argument('--output-json', required=True)
    args = ap.parse_args()
    rows = []
    reg = read_json(Path(args.regression_json), {}) if args.regression_json else {}
    fp = read_json(Path(args.fp_json), {}) if args.fp_json else {}
    if reg:
        rr = reg.get('regression_run_row', {})
        total = float(rr.get('total_tests') or 0); passed = float(rr.get('passed_tests') or 0)
        add(rows, 'regression_pass_rate', round(passed/total,4) if total else 0, 'flow_v2_regression_runs', rr.get('notes',''))
        add(rows, 'regression_failed_tests', rr.get('failed_tests',0), 'flow_v2_regression_runs', '')
        add(rows, 'alert_volume_before', rr.get('alert_volume_before',0), 'flow_v2_regression_runs', '')
        add(rows, 'alert_volume_after', rr.get('alert_volume_after',0), 'flow_v2_regression_runs', '')
    if fp:
        for r in fp.get('dashboard_metric_rows', []): rows.append(r)
    # Always include placeholders for final posture board metrics so dashboard table has stable columns/metric names.
    for name in ['mcp_tool_calls_total','mcp_tool_calls_blocked','mcp_tool_results_sanitized','mcp_schema_drift_detected','mcp_tool_poisoning_detected','mcp_sensitive_tool_without_hitl','mcp_untrusted_server_detected','mcp_resource_exfiltration_attempts','mcp_confused_deputy_alerts','rag_untrusted_context_alerts','rag_retrieval_to_tool_escalations','memory_poisoning_attempts','memory_scope_violations','agentic_goal_hijack_alerts','agentic_tool_loop_alerts','approval_manipulation_alerts','delegated_identity_misuse_alerts','case_promotions_by_family','top_noisy_rule_family']:
        add(rows, name, 0, 'phase9_rollup_placeholder', 'Populate from n8n DataTable reads or exported runtime rows during production rollup')
    result = {'flow':'V2 Dashboard Metrics Rollup','decision':'pass','dashboard_metric_rows':rows,'slack_text':f'V2 dashboard rollup generated {len(rows)} metric rows'}
    write_json(Path(args.output_json), result)
    print(json.dumps(result, indent=2))
if __name__ == '__main__': main()
