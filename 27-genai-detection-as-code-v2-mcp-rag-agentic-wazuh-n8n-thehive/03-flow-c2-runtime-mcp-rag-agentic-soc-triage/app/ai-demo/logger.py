#!/usr/bin/env python3
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(os.getenv("AI_DEMO_LOG", "/var/log/ai-demo/guardrail-events.jsonl"))
_LOCK = threading.Lock()

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def write_event(event):
    event = dict(event)
    event.setdefault("schema_version", "1.0")
    event.setdefault("event_source", "ai_demo_guardrail")
    event.setdefault("created_at", utc_now_iso())

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))

    with _LOCK:
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    return event
