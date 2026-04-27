# Repository layout

```text
26-genai-detection-as-code-cicd-wazuh-n8n-thehive/
├── README.md                                      # Main project overview, architecture summary, setup flow, and navigation
├── architecture-notes.txt                         # High-level architecture notes for GenAI detection-as-code CI/CD
├── interview_qna.md                               # Interview-focused Q&A and talking points for explaining the project
├── SECURITY_NOTES.md                              # Security considerations, safe handling notes, and operational cautions
├── FILE_INDEX.md                                  # Complete file index for quick navigation across project artifacts
│
├── data-tables/                                   # CSV evidence tables used for dashboards, validation, and workflow tracking
│   ├── exports/                                   # Exported operational data from CI, deployment, alerting, and SOAR flows
│   └── schemas/                                   # Column definitions and seed data for dashboard/reporting tables
│
├── workflows/                                     # n8n workflow exports for CI validation, deployment, triage, dashboarding, and case closure
│   ├── flow-a-detection-ci-validation-audited-dashboard-v2.n8n.json       # Flow A n8n workflow for detection CI validation and audit dashboarding
│   ├── flow-b-controlled-deployment-audited-dashboard-v1.n8n.json         # Flow B n8n workflow for controlled Wazuh deployment approval and tracking
│   ├── flow-c-runtime-genai-triage-thehive5-case-templates-comments-v5.n8n.json # Flow C n8n workflow for GenAI runtime alert triage and TheHive case creation
│   ├── flow-d-thehive-case-closure-sync-flowc-v1.n8n.json                 # Flow D n8n workflow for syncing TheHive case closure status
│   ├── flow-global-error-deadletter-v2.n8n.json                           # Global dead-letter/error workflow for failed automation events
│   └── flow-soc-dashboard-event-collector-v1.n8n.json                     # SOC dashboard event collector workflow
│
├── project-pdfs/                                  # Final PDF artifacts and visual documentation for portfolio/demo review
│   ├── GenAI_Detection_as_Code_CICD_for_Wazuh_Project_Overview.pdf        # Overall project overview PDF
│   ├── Flow_A_Detection_CI_Validation.pdf                                  # Flow A evidence/export PDF
│   ├── Flow_B_Controlled_Deployment.pdf                                    # Flow B evidence/export PDF
│   ├── Flow_C_Runtime_GenAI_Triage_TheHive5.pdf                            # Flow C evidence/export PDF
│   ├── Supporting_Workflows_Audit_Dashboard_Error_CaseClosure.pdf          # Supporting workflows evidence/export PDF
│   └── README.md                                  # Notes explaining the PDF artifact set
│
├── resources/                                     # Supporting references and reusable guidance for the project
│   └── README.md                                  # Resource notes and reference material overview
│
├── notes/                                         # Supporting notes for positioning, implementation choices, demos, and visuals
│   ├── capstone-positioning-and-usp.md            # Project positioning, USP, and portfolio framing notes
│   ├── implementation-decisions.md                # Key implementation decisions and tradeoffs
│   ├── demo-script.md                             # Demo walkthrough script for presenting the project
│   ├── architecture-image-prompt.md               # Prompt/reference text for generating architecture visuals
│   └── linkedin-links-placeholder.md              # Placeholder for portfolio and LinkedIn reference links
│
├── _shared/                                       # Reusable shared assets used across multiple flows
│   ├── README.md                                  # Shared asset overview
│   ├── source-scripts/                            # Shared CI and deployment scripts reused by flow folders
│   │   ├── ci/                                    # Detection validation scripts for CI pipeline checks
│   │   └── deploy/                                # Controlled Wazuh deployment, rollback, and smoke-test scripts
│   ├── detection-metadata/                        # Detection metadata for GenAI attack scenarios
│   ├── mappings/                                  # OWASP/ATLAS mapping files for GenAI threat classification
│   ├── schemas/                                   # JSON schema for AI application telemetry
│   ├── tests/                                     # Positive/negative test events and expected rule outputs
│   └── config-templates/                          # Example CI environment configuration templates
│
├── 00-project-overview/                           # Executive overview, architecture summary, and project-wide documentation
│   ├── README.md                                  # Overview of the complete GenAI detection-as-code project
│   ├── architecture-notes.txt                     # High-level architecture and system design notes
│   ├── troubleshooting.md                         # Common project-level issues and fixes
│   ├── interview_qna.md                           # Overall interview talking points and project explanation
│   ├── artifacts/                                 # Project overview PDF artifact
│   └── notes/                                     # Overview summary and validation evidence checklist
│
├── 01-flow-a-detection-ci-validation/             # Flow A: detection CI validation before deployment
│   ├── README.md                                  # Flow A explanation, purpose, and validation process
│   ├── architecture-notes.txt                     # Flow A architecture notes
│   ├── troubleshooting.md                         # Flow A troubleshooting guidance
│   ├── interview_qna.md                           # Flow A interview talking points
│   ├── artifacts/                                 # Flow A PDF evidence/export
│   ├── scripts/                                   # CI scripts for validating Sigma, Wazuh XML, metadata, and replay harness checks
│   ├── config/                                    # Example CI configuration file
│   └── notes/                                     # Flow A design, validation, and data model notes
│
├── 02-flow-b-controlled-wazuh-deployment/         # Flow B: controlled deployment of approved Wazuh detection content
│   ├── README.md                                  # Flow B explanation and deployment workflow notes
│   ├── architecture-notes.txt                     # Flow B architecture notes
│   ├── troubleshooting.md                         # Flow B troubleshooting guidance
│   ├── interview_qna.md                           # Flow B interview talking points
│   ├── artifacts/                                 # Flow B PDF evidence/export
│   ├── scripts/                                   # Deployment, backup, rollback, staging, XML check, logtest, and restart scripts
│   ├── config/                                    # Example deployment/CI configuration file
│   └── notes/                                     # Flow B design and validation notes
│
├── 03-flow-c-runtime-genai-triage-thehive/        # Flow C: runtime GenAI alert detection, triage, and TheHive case promotion
│   ├── README.md                                  # Flow C explanation and triage workflow overview
│   ├── architecture-notes.txt                     # Flow C architecture notes
│   ├── troubleshooting.md                         # Flow C troubleshooting guidance
│   ├── interview_qna.md                           # Flow C interview talking points
│   ├── artifacts/                                 # Flow C PDF evidence/export
│   ├── app/                                       # Demo AI application used to generate telemetry for testing
│   │   └── ai-demo/                               # Flask/demo app, guardrails logic, logger, requirements, and test event script
│   ├── wazuh/                                     # Wazuh rules, decoders, integration script, and configuration snippets
│   │   ├── rules/                                 # GenAI Wazuh detection rules
│   │   ├── decoders/                              # Wazuh decoders for AI app telemetry
│   │   ├── integrations/                          # Custom Wazuh-to-n8n integration script and install snippet
│   │   └── configs/                               # Wazuh manager and agent configuration blocks
│   ├── guardrails/                                # Runtime guardrail policy files
│   ├── metadata/                                  # GenAI detection metadata for prompt injection, indirect injection, and output handling
│   ├── mappings/                                  # OWASP/ATLAS mapping for GenAI detection scenarios
│   ├── schemas/                                   # AI app telemetry JSON schema
│   ├── tests/                                     # Positive/negative GenAI test events and expected rule outputs
│   └── notes/                                     # Flow C design, case template, and validation notes
│
└── 04-supporting-workflows-audit-dashboard-error-caseclosure/ # Supporting workflows for audit, dashboarding, errors, and case closure
    ├── README.md                                  # Supporting workflow overview
    ├── architecture-notes.txt                     # Supporting workflow architecture notes
    ├── troubleshooting.md                         # Troubleshooting for supporting automations
    ├── interview_qna.md                           # Interview talking points for audit/dashboard/error/case-closure flows
    ├── artifacts/                                 # Supporting workflow PDF evidence/export
    └── notes/                                     # Design, validation, and data-table notes
  ```
