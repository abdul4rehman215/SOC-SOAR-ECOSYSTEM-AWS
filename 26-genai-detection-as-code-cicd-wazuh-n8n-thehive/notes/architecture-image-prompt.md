# Architecture Image Prompt

Use this prompt in an image generator to create the GitHub README architecture image.

```text
Create a premium dark-mode cybersecurity architecture diagram for a capstone project titled "GenAI Detection-as-Code CI/CD for Wazuh".

Style:
- Modern SOC engineering dashboard aesthetic
- Dark navy / charcoal background
- Neon blue, green, orange, and purple accents
- Clean vector diagram, no clutter, readable labels
- Wide 16:9 landscape layout
- Professional portfolio-ready visual

Main pipeline:
1. GitHub Pull Request and detection content repository
2. n8n Flow A: Detection CI Validation
   - changed file classification
   - Wazuh XML validation
   - Sigma validation
   - metadata validation
   - replay harness
   - GitHub comment and labels
3. n8n Flow B: Controlled Wazuh Deployment
   - deployment gate
   - backup
   - stage
   - XML/smoke checks
   - activate and restart Wazuh
   - postdeploy and rollback
4. Wazuh Manager and Wazuh Agent
5. AI Demo App writing guardrail JSONL telemetry
6. n8n Flow C: Runtime GenAI Triage
   - normalize Wazuh alert
   - OWASP LLM and ATLAS enrichment
   - risk scoring
   - Slack alert
   - TheHive alert and case
   - audit tables
7. Supporting workflows:
   - SOC Dashboard Event Collector
   - Global Error Dead-Letter Handler
   - TheHive Case Closure Sync

Show integrations:
- Slack notification icon
- TheHive alert/case icon
- DataTable audit/dashboard storage
- OWASP LLM and ATLAS mapping badges

Text labels should be crisp and minimal. Include a small footer text: "Built by abdul4rehman215".
```
