# Wazuh Content for Flow C

This folder contains the Wazuh runtime content used by Flow C.

## Rules and decoder

- `decoders/genai_ai_app_decoder.xml`
- `rules/genai_ai_app_rules.xml`

Target rules:

- 100201 - direct prompt injection
- 100202 - indirect prompt injection / untrusted retrieved context
- 100203 - improper output handling risk

## Integration

- `integrations/custom-n8n-genai.py` forwards target alerts to the n8n Flow C webhook.
- `configs/wazuh-manager-integration-block.xml.txt` shows the `<integration>` block for the Wazuh manager.
- `configs/wazuh-agent-localfile-block.xml.txt` shows the Wazuh agent localfile monitor for the AI demo JSONL log.
