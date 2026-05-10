from __future__ import annotations
from pathlib import Path
from typing import Dict
SOURCE_TO_FILE={'local://trusted_docs/security_policy.txt':'trusted_docs/security_policy.txt','local://trusted_docs/ticket_guidance.txt':'trusted_docs/ticket_guidance.txt','local://untrusted_docs/poisoned_context.txt':'untrusted_docs/poisoned_context.txt','local://untrusted_docs/memory_poison.txt':'untrusted_docs/memory_poison.txt','local://untrusted_docs/tool_escalation.txt':'untrusted_docs/tool_escalation.txt','local://unapproved_sources/rogue_embedding_source.txt':'unapproved_sources/rogue_embedding_source.txt'}
class LocalRAGDemo:
    def __init__(self, repo_root: str): self.doc_root=Path(repo_root).resolve()/'app'/'rag-memory-lab'
    def retrieve(self, query: str, source: str)->Dict[str,str]:
        rel=SOURCE_TO_FILE.get(source)
        if not rel: return {'query':query,'source':source,'content':'Unknown source. No approved document mapping exists.','source_type':'unknown'}
        content=(self.doc_root/rel).read_text(encoding='utf-8').strip()
        st='trusted_local' if '/trusted_docs/' in source else 'untrusted_local'
        if 'unapproved_sources' in source: st='unapproved_source'
        return {'query':query,'source':source,'content':content,'source_type':st}
