from __future__ import annotations
import json, os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

def utc_now() -> str: return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent: os.makedirs(parent, exist_ok=True)
def csv(value: Any) -> str:
    if value is None: return ''
    if isinstance(value, str): return value
    if isinstance(value, (list,tuple,set)): return ','.join(str(v) for v in value)
    return str(value)
def base_event(*, event_type: str, request_id: str, detection_family: str, severity: str, risk_score: int, expected_wazuh_rule_id: Optional[int], risk_flags: Optional[Iterable[str]]=None, scenario: str='') -> Dict[str, Any]:
    flags=list(risk_flags or [])
    return {'schema_version':'2.0','timestamp':utc_now(),'event_source':'ai_demo_rag_memory_guardrail','event_type':event_type,'request_id':request_id,'session_id':'sess-ragmem-demo-001','user_id':'student-user-demo','agent_id':'agent-demo-001','model':'demo-llm','policy_bundle_version':'v2.0.0-phase5-rag-memory','policy_bundle_hash':'sha256:rag-memory-policy-bundle-v1','environment':'lab','app_name':'ai-demo-v2','scenario':scenario,'retrieval_query':'','retrieval_source':'','retrieval_source_type':'','source_trust_level':'','retrieval_rank':0,'embedding_collection':'kb-demo','embedding_source_approved':True,'retrieved_context_excerpt':'','content_risk_flags_csv':'','memory_scope':'session','memory_write_requested':False,'memory_write_allowed':False,'memory_write_reason':'','memory_key':'','memory_value_excerpt':'','proposed_tool_name':'','proposed_tool_category':'','proposed_tool_args_summary':'','approval_required':False,'approval_status':'not_required','guardrail_action':'allow','detection_family':detection_family,'severity':severity,'confidence':0.0,'risk_score':risk_score,'risk_flags':flags,'risk_flags_csv':csv(flags),'owasp_category':'none','mcp_risk_category':'none','agentic_risk_category':'none','atlas_techniques':[],'expected_wazuh_rule_id':expected_wazuh_rule_id}
def write_event(log_file: str, event: Dict[str, Any]) -> None:
    ensure_parent(log_file)
    with open(log_file,'a',encoding='utf-8') as f: f.write(json.dumps(event,separators=(',',':'),ensure_ascii=False)+'\n')
def write_events(log_file: str, events: List[Dict[str, Any]]) -> None:
    for event in events: write_event(log_file,event)
