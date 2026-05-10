#!/usr/bin/env python3
import argparse
import datetime as _dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
import xml.etree.ElementTree as ET

DEFAULT_REQUIRED_LABELS = [
    'ai-security-ci-pass',
    'detection-ci-pass',
    'mcp-policy-pass',
    'rag-policy-pass',
    'agentic-policy-pass',
    'ready-to-deploy',
]
RULE_FILES = [
    'genai_mcp_rules.xml',
    'genai_rag_memory_rules.xml',
    'genai_agentic_rules.xml',
]
DECODER_FILES = [
    'genai_mcp_decoder.xml',
    'genai_rag_memory_decoder.xml',
    'genai_agentic_decoder.xml',
]
POLICY_SUBDIRS = ['mcp', 'rag_memory', 'agentic']
REQUIRED_POLICY_FILES = {
    'mcp': ['mcp_policy_bundle.json', 'mcp_tool_registry.json', 'mcp_resource_roots.json'],
    'rag_memory': ['rag_memory_policy_bundle.json', 'source_trust_policy.json', 'memory_write_policy.json', 'embedding_source_policy.json'],
    'agentic': ['agentic_policy_bundle.json', 'approval_prompt_policy.json', 'identity_scope_policy.json', 'loop_threshold_policy.json', 'confused_deputy_policy.json'],
}


def now_iso():
    return _dt.datetime.now(_dt.timezone.utc).isoformat().replace('+00:00', 'Z')


def ts_id():
    return _dt.datetime.now(_dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def read_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding='utf-8'))


def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return 'sha256:' + h.hexdigest()


def sha256_dir(path):
    p = Path(path)
    h = hashlib.sha256()
    if not p.exists():
        return 'sha256:missing'
    for file in sorted(x for x in p.rglob('*') if x.is_file()):
        rel = str(file.relative_to(p)).replace(os.sep, '/')
        h.update(rel.encode('utf-8'))
        h.update(b'\0')
        h.update(file.read_bytes())
        h.update(b'\0')
    return 'sha256:' + h.hexdigest()


def run_cmd(cmd, cwd=None, check=False):
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\nstdout={proc.stdout}\nstderr={proc.stderr}")
    return {'cmd': cmd, 'returncode': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}


def stage_result(name, passed, details='', output=None):
    return {
        'stage': name,
        'passed': bool(passed),
        'details': details,
        'output': output or {},
        'timestamp': now_iso(),
    }


def copy_if_exists(src, dst):
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def copy_tree_clean(src, dst):
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        return False
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return True


def parse_xml_files(paths):
    parsed = []
    failures = []
    for path in paths:
        p = Path(path)
        if not p.exists():
            failures.append(f'missing {p}')
            continue
        try:
            ET.parse(p)
            parsed.append(str(p))
        except Exception as exc:
            failures.append(f'{p}: {exc}')
    return parsed, failures


def find_repo_root(value=None):
    if value:
        return Path(value).resolve()
    return Path.cwd().resolve()


def safe_label_list(raw):
    if raw is None:
        return []
    if isinstance(raw, str):
        return [x.strip() for x in raw.split(',') if x.strip()]
    if isinstance(raw, list):
        out = []
        for item in raw:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict) and item.get('name'):
                out.append(str(item['name']))
        return out
    return []


def load_signal(signal_json=None):
    if signal_json and Path(signal_json).exists():
        return json.loads(Path(signal_json).read_text(encoding='utf-8'))
    return {
        'event_type': 'manual_b2_deploy_signal',
        'repo': 'local/wazuh-genai-ci',
        'pr_number': 0,
        'commit_sha': 'local-current-working-tree',
        'actor': os.environ.get('USER', 'local-user'),
        'approved': True,
        'labels': DEFAULT_REQUIRED_LABELS + ['needs-review'],
        'deploy_environment': 'lab',
        'deploy_mode': 'dry_run',
    }


def evaluate_gate(signal, required_labels=None):
    required = required_labels or DEFAULT_REQUIRED_LABELS
    labels = safe_label_list(signal.get('labels') or signal.get('observed_labels'))
    missing = [x for x in required if x not in labels]
    approved = bool(signal.get('approved') is True or str(signal.get('approval_status', '')).lower() == 'approved')
    blocked_reasons = []
    if missing:
        blocked_reasons.append('missing_labels=' + ','.join(missing))
    if not approved:
        blocked_reasons.append('approval_missing_or_false')
    return {
        'gate_passed': not blocked_reasons,
        'required_labels': required,
        'observed_labels': labels,
        'missing_labels': missing,
        'approved': approved,
        'blocked_reasons': blocked_reasons,
    }


def count_files(path, suffix=None):
    p = Path(path)
    if not p.exists():
        return 0
    files = [x for x in p.rglob('*') if x.is_file()]
    if suffix:
        files = [x for x in files if x.name.endswith(suffix)]
    return len(files)


def discover_policy_bundle_version(repo_root):
    candidates = [
        repo_root / 'policies' / 'mcp' / 'mcp_policy_bundle.json',
        repo_root / 'policies' / 'rag_memory' / 'rag_memory_policy_bundle.json',
        repo_root / 'policies' / 'agentic' / 'agentic_policy_bundle.json',
    ]
    versions = []
    for p in candidates:
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding='utf-8'))
                versions.append(str(data.get('policy_bundle_version') or data.get('version') or 'unknown'))
            except Exception:
                versions.append('unknown')
    return ','.join(sorted(set(versions))) if versions else 'unknown'


def verify_policy_files(repo_root):
    failures = []
    found = []
    base = repo_root / 'policies'
    for subdir, names in REQUIRED_POLICY_FILES.items():
        for name in names:
            p = base / subdir / name
            if p.exists():
                found.append(str(p.relative_to(repo_root)))
            else:
                failures.append(f'missing {p.relative_to(repo_root)}')
    return found, failures


def validate_expected_repo_layout(repo_root):
    failures = []
    required_paths = [
        repo_root / 'detections' / 'wazuh' / 'rules',
        repo_root / 'detections' / 'wazuh' / 'decoders',
        repo_root / 'policies' / 'mcp',
        repo_root / 'policies' / 'rag_memory',
        repo_root / 'policies' / 'agentic',
        repo_root / 'scripts' / 'ci' / 'run_flow_a2_local_ci.py',
    ]
    for p in required_paths:
        if not p.exists():
            failures.append(f'missing required path {p}')
    return failures


def stage_content(repo_root, staging_dir):
    staging_dir = Path(staging_dir)
    rules_src = repo_root / 'detections' / 'wazuh' / 'rules'
    decoders_src = repo_root / 'detections' / 'wazuh' / 'decoders'
    policies_src = repo_root / 'policies'
    rules_dst = staging_dir / 'wazuh' / 'rules'
    decoders_dst = staging_dir / 'wazuh' / 'decoders'
    policies_dst = staging_dir / 'policies'
    for d in [rules_dst, decoders_dst, policies_dst]:
        d.mkdir(parents=True, exist_ok=True)
    copied_rules = []
    copied_decoders = []
    for name in RULE_FILES:
        if copy_if_exists(rules_src / name, rules_dst / name):
            copied_rules.append(name)
    for name in DECODER_FILES:
        if copy_if_exists(decoders_src / name, decoders_dst / name):
            copied_decoders.append(name)
    copied_policies = []
    for subdir in POLICY_SUBDIRS:
        if copy_tree_clean(policies_src / subdir, policies_dst / subdir):
            copied_policies.append(subdir)
    # Copy mappings for case template and family maps as policy-adjacent deployment content.
    mappings_src = repo_root / 'mappings'
    if mappings_src.exists():
        copy_tree_clean(mappings_src, staging_dir / 'mappings')
    return {
        'staging_dir': str(staging_dir),
        'rules_path': str(rules_dst),
        'decoders_path': str(decoders_dst),
        'policies_path': str(policies_dst),
        'copied_rules': copied_rules,
        'copied_decoders': copied_decoders,
        'copied_policy_subdirs': copied_policies,
    }


def backup_current_content(backup_root, wazuh_rules_dir, wazuh_decoders_dir, policy_active_dir, dry_run=False):
    backup_root = Path(backup_root)
    backup_id = ts_id() + '-' + uuid.uuid4().hex[:8]
    backup_dir = backup_root / backup_id
    wazuh_backup = backup_dir / 'wazuh'
    policy_backup = backup_dir / 'policies'
    if dry_run:
        return {
            'backup_id': backup_id,
            'backup_dir': str(backup_dir),
            'wazuh_backup_path': str(wazuh_backup),
            'policy_backup_path': str(policy_backup),
            'dry_run': True,
        }
    (wazuh_backup / 'rules').mkdir(parents=True, exist_ok=True)
    (wazuh_backup / 'decoders').mkdir(parents=True, exist_ok=True)
    policy_backup.mkdir(parents=True, exist_ok=True)
    for name in RULE_FILES:
        copy_if_exists(Path(wazuh_rules_dir) / name, wazuh_backup / 'rules' / name)
    for name in DECODER_FILES:
        copy_if_exists(Path(wazuh_decoders_dir) / name, wazuh_backup / 'decoders' / name)
    if Path(policy_active_dir).exists():
        copy_tree_clean(policy_active_dir, policy_backup / 'active')
    return {
        'backup_id': backup_id,
        'backup_dir': str(backup_dir),
        'wazuh_backup_path': str(wazuh_backup),
        'policy_backup_path': str(policy_backup),
        'dry_run': False,
    }
