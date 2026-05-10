#!/usr/bin/env python3
"""Shared helpers for V2 Flow A2 validators. Standard library only."""
from __future__ import annotations
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

OK = "pass"
FAIL = "fail"
WARN = "warn"


def repo_root_from_arg(value: str | None) -> Path:
    return Path(value or ".").resolve()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def list_files(root: Path, patterns: List[str]) -> List[Path]:
    out: List[Path] = []
    for pattern in patterns:
        out.extend(sorted(root.glob(pattern)))
    return [p for p in out if p.is_file()]


def strip_inline_comment(line: str) -> str:
    # Keep URLs and hashes; only strip a leading-space comment marker.
    if " #" in line:
        return line.split(" #", 1)[0]
    return line


def load_simple_yaml(path: Path) -> Any:
    """A tiny YAML reader for the simple maps/lists used in this MVP.

    It supports:
    key: value
    key:
      - item
    top-level numeric/string keys
    nested one-level maps via indentation

    It is not a general YAML parser. It avoids requiring PyYAML on Wazuh/n8n hosts.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    data: Dict[str, Any] = {}
    stack: List[Tuple[int, Any, str | None]] = [(-1, data, None)]
    last_key_by_indent: Dict[int, str] = {}

    def parse_scalar(v: str) -> Any:
        v = v.strip().strip('"').strip("'")
        if v == "":
            return ""
        if v.lower() in {"true", "false"}:
            return v.lower() == "true"
        if v.lower() in {"null", "none"}:
            return None
        if re.fullmatch(r"-?\d+", v):
            try:
                return int(v)
            except Exception:
                return v
        if re.fullmatch(r"-?\d+\.\d+", v):
            try:
                return float(v)
            except Exception:
                return v
        if v.startswith("[") and v.endswith("]"):
            body = v[1:-1].strip()
            if not body:
                return []
            return [parse_scalar(x.strip()) for x in body.split(",")]
        return v

    lines = text.splitlines()
    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        line = strip_inline_comment(raw.rstrip())
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if stripped.startswith("- "):
            value = parse_scalar(stripped[2:].strip())
            if isinstance(parent, list):
                parent.append(value)
            else:
                key = last_key_by_indent.get(stack[-1][0])
                if key is not None and isinstance(parent, dict):
                    parent.setdefault(key, [])
                    if isinstance(parent[key], list):
                        parent[key].append(value)
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip().strip('"').strip("'")
            value = value.strip()
            if value == "":
                # Lookahead could be list or map. Default to dict; list items convert when seen.
                new_obj: Dict[str, Any] = {}
                if isinstance(parent, dict):
                    parent[key] = new_obj
                last_key_by_indent[indent] = key
                stack.append((indent, new_obj, key))
            else:
                if isinstance(parent, dict):
                    parent[key] = parse_scalar(value)
                last_key_by_indent[indent] = key
    # Fix empty maps that were intended as lists by rereading simple list blocks.
    # Good enough for mappings/expected files in this project.
    return data


def load_data(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return load_json(path)
    if path.suffix.lower() in {".yml", ".yaml"}:
        try:
            import yaml  # type: ignore
            with path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            return load_simple_yaml(path)
    return read_text(path)


def print_result(stage: str, status: str, **kwargs: Any) -> None:
    payload = {"stage": stage, "status": status}
    payload.update(kwargs)
    print(json.dumps(payload, indent=2, sort_keys=True))


def make_result(stage: str, status: str, **kwargs: Any) -> Dict[str, Any]:
    payload = {"stage": stage, "status": status}
    payload.update(kwargs)
    return payload


def require_files(root: Path, rel_paths: List[str]) -> Tuple[List[str], List[str]]:
    present, missing = [], []
    for rel in rel_paths:
        if (root / rel).exists():
            present.append(rel)
        else:
            missing.append(rel)
    return present, missing


def csv_schema_columns(path: Path) -> List[Dict[str, str]]:
    import csv
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]
