#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone, timedelta
from phase9_common import utcnow, stable_id, read_csv, write_json, family_for_rule

def norm_reason(r: str) -> str:
    s = (r or '').strip().lower().replace('_',' ')
    if 'false' in s: return 'false_positive'
    if 'benign' in s: return 'benign_positive'
    if 'true' in s: return 'true_positive'
    return s or 'unknown'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--runtime-events-csv', default='')
    ap.add_argument('--closure-sync-csv', default='')
    ap.add_argument('--window-days', type=int, default=7)
    ap.add_argument('--output-json', required=True)
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    runtime_csv = Path(args.runtime_events_csv) if args.runtime_events_csv else repo/'tests/fixtures/runtime_events_sample.csv'
    closure_csv = Path(args.closure_sync_csv) if args.closure_sync_csv else repo/'tests/fixtures/thehive_closure_sync_sample.csv'
    runtime = read_csv(runtime_csv) if runtime_csv.exists() else []
    closures = read_csv(closure_csv) if closure_csv.exists() else []
    now_dt = datetime.now(timezone.utc).replace(microsecond=0)
    window_end = now_dt.isoformat().replace('+00:00','Z')
    window_start = (now_dt - timedelta(days=args.window_days)).isoformat().replace('+00:00','Z')
    by_rule = defaultdict(lambda: {'alerts':0,'cases':set(),'closures':Counter(),'family':''})
    for row in runtime:
        try: rid = int(row.get('rule_id') or row.get('wazuh_rule_id') or 0)
        except Exception: rid = 0
        if rid == 0: continue
        family = row.get('rule_family') or row.get('detection_family') or family_for_rule(rid)
        by_rule[rid]['alerts'] += 1
        by_rule[rid]['family'] = family
        cid = row.get('thehive_case_id') or row.get('case_id') or ''
        if cid: by_rule[rid]['cases'].add(cid)
    for row in closures:
        try: rid = int(row.get('rule_id') or row.get('wazuh_rule_id') or 0)
        except Exception: rid = 0
        if rid == 0: continue
        family = row.get('rule_family') or row.get('detection_family') or family_for_rule(rid)
        by_rule[rid]['family'] = family
        by_rule[rid]['closures'][norm_reason(row.get('closure_reason') or row.get('status') or '')] += 1
        cid = row.get('case_id') or row.get('thehive_case_id') or ''
        if cid: by_rule[rid]['cases'].add(cid)
    rows = []
    recommendations = []
    for rid, data in sorted(by_rule.items()):
        alerts = data['alerts']; cases = len(data['cases'])
        fp = data['closures']['false_positive']; tp = data['closures']['true_positive']; bp = data['closures']['benign_positive']
        closed_total = fp + tp + bp
        fp_rate = round(fp / closed_total, 4) if closed_total else 0.0
        family = data['family'] or family_for_rule(rid)
        if fp_rate >= 0.5:
            action = 'High FP rate: review rule logic, tighten conditions, add allowlist or context filter.'; priority='critical'
        elif fp_rate >= 0.25:
            action = 'Moderate FP rate: review sample alerts and add tuning note.'; priority='high'
        elif alerts >= 10:
            action = 'High alert volume: review for noisy rule behavior even if FP rate is low.'; priority='medium'
        else:
            action = 'No immediate tuning required; continue monitoring.'; priority='low'
        aid = stable_id('fp', rid, window_start, window_end)
        rows.append({'analytics_id': aid, 'window_start': window_start, 'window_end': window_end, 'rule_id': rid, 'rule_family': family, 'alert_count': alerts, 'case_count': cases, 'closed_false_positive_count': fp, 'closed_true_positive_count': tp, 'closed_benign_positive_count': bp, 'fp_rate': fp_rate, 'recommended_action': action, 'tuning_priority': priority, 'owner': '', 'status': 'open' if priority in ('critical','high') else 'monitoring', 'created_at': window_end, 'notes': f'closure_counts={dict(data["closures"])}'})
        if priority in ('critical','high','medium'):
            recommendations.append({'recommendation_id': stable_id('tune', rid, window_end), 'created_at': window_end, 'rule_id': rid, 'rule_family': family, 'priority': priority, 'reason': f'fp_rate={fp_rate}; alerts={alerts}', 'recommended_action': action, 'fp_rate': fp_rate, 'alert_count': alerts, 'owner': '', 'status': 'open', 'notes': ''})
    dashboard_rows = []
    if rows:
        avg_fp = round(sum(float(r['fp_rate']) for r in rows) / len(rows), 4)
        dashboard_rows.append({'metric_id': stable_id('metric','false_positive_rate_by_rule', window_end), 'window_start': window_start, 'window_end': window_end, 'metric_name': 'false_positive_rate_by_rule', 'metric_value': avg_fp, 'dimension_key': 'aggregate', 'dimension_value': 'all_rules', 'source_table': 'flow_v2_false_positive_analytics', 'generated_at': window_end, 'notes': 'Average FP rate across rules in window'})
        dashboard_rows.append({'metric_id': stable_id('metric','rules_needing_tuning', window_end), 'window_start': window_start, 'window_end': window_end, 'metric_name': 'rules_needing_tuning', 'metric_value': len(recommendations), 'dimension_key': 'priority', 'dimension_value': 'medium_or_higher', 'source_table': 'flow_v2_rule_tuning_recommendations', 'generated_at': window_end, 'notes': 'Rules with tuning recommendations'})
    result = {'flow': 'Flow G - False Positive Analytics', 'decision': 'pass', 'window_start': window_start, 'window_end': window_end, 'false_positive_rows': rows, 'tuning_recommendation_rows': recommendations, 'dashboard_metric_rows': dashboard_rows, 'slack_text': f'Flow G FP analytics: rules={len(rows)}, recommendations={len(recommendations)}. ' + '; '.join([f"{r['rule_id']} fp={r['fp_rate']} action={r['tuning_priority']}" for r in rows])}
    write_json(Path(args.output_json), result)
    print(json.dumps(result, indent=2))
if __name__ == '__main__': main()
