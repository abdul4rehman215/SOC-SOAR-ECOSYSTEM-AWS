// ================================
// GET DATA
// ================================

const alert = $items("Normalize Wazuh Alert")[0].json;
const aiRaw = $input.first().json.output || "";

// ================================
// CLEAN AI OUTPUT
// ================================

// Remove any accidental markdown artifacts
let aiResponse = aiRaw
  .replace(/```/g, "")
  .replace(/\*\*/g, "")
  .trim();

// ================================
// EXTRACT SECTIONS (FIXED)
// ================================

function extractSection(title) {
  const regex = new RegExp(
    `${title}\\s*([\\s\\S]*?)(?=\\n[A-Z_]{3,}|$)`,
    "i"
  );
  const match = aiResponse.match(regex);
  return match ? match[1].trim() : "";
}

const overview = extractSection("ALERT_OVERVIEW");
const summary = extractSection("TRIAGE_SUMMARY");
const risk = extractSection("RISK_ASSESSMENT");
const actions = extractSection("RECOMMENDED_ACTIONS");

// Try ANALYST_DECISION first
let decision = extractSection("ANALYST_DECISION");

// If empty, try NEXT_STEP
if (!decision) {
  decision = extractSection("NEXT_STEP");
}

// Final fallback
if (!decision) {
  decision = "Analyst review required.";
}

// Clean formatting artifacts
decision = decision
  .replace(/NEXT_STEP/gi, "")
  .replace(/ANALYST_DECISION/gi, "")
  .replace(/\n+/g, " ")
  .trim();


// ================================
// ALERT FIELDS
// ================================

const ruleLevel = alert.rule_level || "N/A";
const ruleId = alert.rule_id || "N/A";
const description = alert.description || "N/A";
const agentName = alert.agent_name || "Unknown";
const agentIp = alert.agent_ip || "N/A";
const log = alert.log || "N/A";
const timestamp = alert.timestamp || new Date().toISOString();
const agentId = alert.agent_id || "N/A";
const srcIp = alert.src_ip || alert.agent_ip || "N/A";
const srcPort = alert.src_port || "N/A";
const user = alert.user || "N/A";

const mitreId = Array.isArray(alert.mitre_id) ? alert.mitre_id.join(", ") : "N/A";
const mitreTactic = Array.isArray(alert.mitre_tactic) ? alert.mitre_tactic.join(", ") : "N/A";
const mitreTechnique = Array.isArray(alert.mitre_technique) ? alert.mitre_technique.join(", ") : "N/A";

// 🔥 FIXED: proper fired count fallback
const ruleFired =
  alert.rule_firedtimes ??
  alert.full_alert?.all_fields?.rule?.firedtimes ??
  "N/A";

const groups = Array.isArray(alert.groups) && alert.groups.length
  ? alert.groups.join(", ")
  : "N/A";

// ================================
// SEVERITY LOGIC
// ================================

let severityBadge = "LOW";
let severityColor = "#17a2b8";
let severityIcon = "ℹ️";

const level = Number(ruleLevel);

if (level >= 13) {
  severityBadge = "CRITICAL";
  severityColor = "#dc3545";
  severityIcon = "🚨";
} else if (level >= 10) {
  severityBadge = "HIGH";
  severityColor = "#fd7e14";
  severityIcon = "⚠️";
} else if (level >= 7) {
  severityBadge = "MEDIUM";
  severityColor = "#ffc107";
  severityIcon = "🔶";
}

// ================================
// SUBJECT
// ================================

const emailSubject = `${severityIcon} ${severityBadge} SOC Alert - Rule ${ruleId} (${agentName})`;

// ================================
// EMAIL HTML
// ================================

const emailBody = `
<!DOCTYPE html>
<html>
<body style="font-family:Segoe UI, Arial; background:#f4f6f9; padding:20px;">

<div style="max-width:800px; margin:auto; background:white; border-radius:8px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.1);">

<!-- HEADER -->
<div style="background:${severityColor}; color:white; padding:30px; text-align:center;">
<h1 style="margin:0;">${severityIcon} ${severityBadge} Security Alert</h1>
<p style="margin:5px 0 0 0;">Severity Level: ${ruleLevel}</p>
</div>

<div style="padding:30px;">

<!-- ALERT OVERVIEW -->
<h2 style="border-bottom:2px solid ${severityColor}; padding-bottom:8px;">🛡 Alert Overview</h2>

<div style="background:#f8f9fa; border:1px solid #e3e6ea; border-radius:8px; overflow:hidden;">

<table width="100%" cellpadding="10" style="border-collapse:collapse; font-size:14px;">

<tr><td style="width:30%; border-bottom:1px solid #e3e6ea;"><b>Rule ID</b></td><td style="border-bottom:1px solid #e3e6ea;">${ruleId}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>Description</b></td><td style="border-bottom:1px solid #e3e6ea;">${description}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>Severity Level</b></td><td style="border-bottom:1px solid #e3e6ea;">${ruleLevel}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>Rule Fired Count</b></td><td style="border-bottom:1px solid #e3e6ea;">${ruleFired}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>Agent Name</b></td><td style="border-bottom:1px solid #e3e6ea;">${agentName}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>Agent ID</b></td><td style="border-bottom:1px solid #e3e6ea;">${agentId}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>Source IP</b></td><td style="border-bottom:1px solid #e3e6ea;">${srcIp}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>Source Port</b></td><td style="border-bottom:1px solid #e3e6ea;">${srcPort}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>User</b></td><td style="border-bottom:1px solid #e3e6ea;">${user}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>Groups</b></td><td style="border-bottom:1px solid #e3e6ea;">${groups}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>MITRE Technique ID</b></td><td style="border-bottom:1px solid #e3e6ea;">${mitreId}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>MITRE Tactic</b></td><td style="border-bottom:1px solid #e3e6ea;">${mitreTactic}</td></tr>
<tr><td style="border-bottom:1px solid #e3e6ea;"><b>MITRE Technique</b></td><td style="border-bottom:1px solid #e3e6ea;">${mitreTechnique}</td></tr>
<tr><td><b>Timestamp</b></td><td>${timestamp}</td></tr>

</table>
</div>

<br>

<!-- LOG -->
<h2 style="border-bottom:2px solid #ccc; padding-bottom:8px;">📄 Log Details</h2>
<div style="background:#f1f3f5; padding:15px; border-radius:6px; font-family:monospace; font-size:13px;">
${log}
</div>

<br>

<!-- AI TRIAGE -->
<h2 style="border-bottom:2px solid #ccc; padding-bottom:8px;">🤖 AI Triage Report</h2>

<div style="margin-bottom:20px;">
<h3>Summary</h3>
<p style="white-space:pre-line;">${summary}</p>
</div>

<div style="margin-bottom:20px;">
<h3>Risk Assessment</h3>
<p style="white-space:pre-line;">${risk}</p>
</div>

<!-- RECOMMENDATIONS -->
<div style="background:#e7f1ff; padding:20px; border-left:6px solid #0d6efd; border-radius:6px; margin-bottom:20px;">
<h3 style="margin-top:0;">🛠 Recommended Actions</h3>
<p style="white-space:pre-line; margin:0;">${actions}</p>
</div>

<!-- DECISION -->
<div style="background:#fff3cd; padding:15px; border-left:6px solid #ffc107; border-radius:6px;">
<b>⚡ Next Step:</b> ${decision}
</div>

</div>

</div>

</body>
</html>
`;

return {
  json: {
    subject: emailSubject,
    html: emailBody
  }
};
