# 🎙️ Interview Q&A - GenAI Detection-as-Code V2

## Q1. What problem does this project solve?

It shows how a SOC can detect and operationalize GenAI runtime security risks across MCP tools, RAG/memory, and agentic AI workflows. It connects detection-as-code, controlled deployment, Wazuh rules, n8n automation, TheHive cases, Slack alerts, and analytics into one MVP.

## Q2. What is the strongest workflow?

Flow C2. It handles three runtime security domains in one triage workflow: MCP, RAG/memory, and agentic AI. It normalizes Wazuh alerts, enriches them, routes them to the correct DataTables, creates/updates TheHive alerts and cases, and posts analyst-ready Slack messages.

## Q3. How does this extend MVP V1?

V1 was focused on GenAI prompt/output detection CI/CD. V2 extends the same engineering model to the full AI action path: tools, resources, retrieval, memory, approval, identity, and autonomous agent plans.

## Q4. Why use Wazuh?

Wazuh gives a practical open-source detection engine for custom JSON telemetry. It also makes the project more SOC-realistic because alerts flow through a SIEM-style rule and integration path instead of only app-level logs.

## Q5. Why use n8n?

n8n lets the prototype orchestrate GitHub, Slack, TheHive, Wazuh scripts, DataTables, and custom logic in a visible workflow format. It is ideal for building and documenting SOC automation prototypes.

## Q6. What would you improve for production?

Move script execution to hardened runners, replace DataTables with a durable database, enforce vault-backed secrets, add automated unit tests for each rule, improve dedup and closure analytics, and formalize TheHive disposition taxonomy.
