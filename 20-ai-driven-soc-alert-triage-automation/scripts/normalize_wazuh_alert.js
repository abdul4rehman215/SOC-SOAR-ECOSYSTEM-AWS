const alert = $json.body;

// Extract important nested fields safely
const rule = alert.all_fields?.rule || {};
const agent = alert.all_fields?.agent || {};
const mitre = rule.mitre || {};
const data = alert.all_fields?.data || {};

return [{
  rule_level: rule.level || "N/A",
  rule_id: alert.rule_id || rule.id || "N/A",
  description: alert.title || rule.description || "N/A",
  log: alert.text || alert.all_fields?.full_log || "N/A",

  // Core Agent Info
  agent_name: agent.name || "Unknown",
  agent_id: agent.id || "N/A",
  agent_ip: agent.ip || "N/A",

  // Network / Source
  src_ip: data.srcip || "N/A",
  src_port: data.srcport || "N/A",
  user: data.dstuser || data.user || "N/A",

  // MITRE
  mitre_id: mitre.id || [],
  mitre_tactic: mitre.tactic || [],
  mitre_technique: mitre.technique || [],

  // Rule Metadata
  rule_firedtimes: alert.all_fields?.firedtimes || 0,
  groups: alert.all_fields?.groups || [],

  timestamp: alert.timestamp || alert.all_fields?.timestamp || new Date().toISOString(),

  // PASS FULL RAW ALERT FOR AI CONTEXT
  full_alert: alert
}];
