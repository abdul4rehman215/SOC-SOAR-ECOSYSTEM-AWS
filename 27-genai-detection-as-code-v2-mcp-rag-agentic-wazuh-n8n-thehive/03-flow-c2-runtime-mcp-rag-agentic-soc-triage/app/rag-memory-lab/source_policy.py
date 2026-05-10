from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List
DEFAULT_POLICY={'trusted_source_prefixes':['local://trusted_docs/','policy://','ticket://'],'untrusted_source_prefixes':['local://untrusted_docs/','web://untrusted/'],'approved_embedding_collections':['kb-demo','policy-demo','ticket-demo'],'allowed_memory_scopes_for_untrusted_sources':[],'allowed_memory_scopes_for_trusted_sources':['session'],'blocked_instruction_patterns':['ignore previous instructions','disregard guardrails','bypass security policy','remember this permanently','call send_external_webhook_mock','run_shell_command_mock','read_resource file://','export chat history','reveal hidden policies']}
class SourcePolicy:
    def __init__(self, repo_root: str):
        self.repo_root=Path(repo_root).resolve(); self.policy=self._load_policy()
    def _load_policy(self)->Dict[str,Any]:
        path=self.repo_root/'policies'/'rag_memory'/'rag_memory_policy_bundle.json'
        if path.exists():
            loaded=json.loads(path.read_text(encoding='utf-8')); merged=dict(DEFAULT_POLICY); merged.update(loaded); return merged
        return DEFAULT_POLICY
    def trust_level(self, source: str)->str:
        if any(source.startswith(p) for p in self.policy['trusted_source_prefixes']): return 'trusted_local'
        if any(source.startswith(p) for p in self.policy['untrusted_source_prefixes']): return 'untrusted'
        return 'unknown'
    def embedding_source_approved(self, collection: str)->bool: return collection in set(self.policy['approved_embedding_collections'])
    def content_flags(self, content: str)->List[str]:
        c=content.lower(); out=[]
        for pattern in self.policy['blocked_instruction_patterns']:
            if pattern.lower() in c:
                if pattern in {'ignore previous instructions','disregard guardrails'}: f='untrusted_instruction'
                elif pattern in {'bypass security policy','remember this permanently'}: f='persistent_policy_override'
                elif 'external_webhook' in pattern: f='external_tool_instruction'
                elif 'run_shell_command' in pattern: f='shell_tool_instruction'
                elif 'read_resource file://' in pattern: f='resource_exfiltration_instruction'
                elif 'export chat history' in pattern: f='data_exfiltration_request'
                elif 'reveal hidden policies' in pattern: f='secret_disclosure_request'
                else: f='instruction_like_content'
                if f not in out: out.append(f)
        return out
    def memory_write_allowed(self, *, source: str, scope: str, content: str):
        trust=self.trust_level(source); flags=self.content_flags(content)
        if trust!='trusted_local': return False,'memory write blocked because source is not trusted'
        if scope not in self.policy['allowed_memory_scopes_for_trusted_sources']: return False,f'memory write blocked because scope {scope} is not allowed for trusted sources'
        if flags: return False,'memory write blocked because content contains instruction-like risk flags'
        return True,'memory write allowed for trusted source and approved session scope'
