# Flow C TheHive Case Template Notes

Required templates:

## flowc-direct-prompt-injection

Used for rule 100201 / direct prompt injection.

Suggested tasks:

- Triage direct prompt injection attempt
- Validate guardrail block and app behavior
- Check repeated user/session behavior
- Tune detection and guardrail evidence
- Close case with analyst decision

## flowc-indirect-prompt-injection

Used for rule 100202 / indirect prompt injection.

Suggested tasks:

- Triage untrusted retrieved context
- Assess retrieval source and exposure
- Validate model/tool safety outcome
- Tune retrieval guardrails
- Close case with containment notes
