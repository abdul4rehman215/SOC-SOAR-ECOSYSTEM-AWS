# 📁 Detailed Repository Layout

This folder is structured as a portfolio-ready GitHub artifact. Each major workflow has its own folder with documentation, workflow JSONs, scripts, configs, DataTable schemas, artifacts, notes, troubleshooting, and interview material.

```text
27-genai-detection-as-code-v2-mcp-rag-agentic-wazuh-n8n-thehive/
├── 00-project-overview/                               # Master story, launch material, overview report
├── 01-flow-a2-ai-security-content-ci/                 # GitHub PR AI-security CI gate
├── 02-flow-b2-controlled-wazuh-policy-deployment/     # controlled Wazuh/policy deployment
├── 03-flow-c2-runtime-mcp-rag-agentic-soc-triage/     # runtime SOC triage, main star workflow
├── 04-supporting-workflows-efg-dashboard-analytics/   # Flow E/F/G and dashboard rollup
├── _shared/                                           # shared configs, workflow exports, data exports
├── notes/                                             # capstone notes, demo script, production roadmap
├── project-pdfs/                                      # all project PDFs and editable DOCX reports
└── resources/                                         # architecture prompt, LinkedIn pack, image placeholders
```

## Folder conventions

- `README.md` explains purpose and how the folder fits into the system.
- `architecture-notes.txt` explains design decisions.
- `interview_qna.md` gives portfolio/interview answers.
- `troubleshooting.md` lists common failure modes.
- `notes/` contains evidence notes, demo scripts, and operational decisions.
- `artifacts/` stores project PDFs/DOCX or evidence packs.
