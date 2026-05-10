from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict
class LocalMemoryStore:
    def __init__(self, repo_root: str): self.path=Path(repo_root).resolve()/'app'/'rag-memory-lab'/'.local_memory_store.json'
    def read_all(self)->Dict[str,Any]: return json.loads(self.path.read_text(encoding='utf-8')) if self.path.exists() else {}
    def write(self, scope: str, key: str, value: str)->Dict[str,Any]:
        data=self.read_all(); data.setdefault(scope,{})[key]=value; self.path.write_text(json.dumps(data,indent=2),encoding='utf-8'); return {'scope':scope,'key':key,'written':True}
