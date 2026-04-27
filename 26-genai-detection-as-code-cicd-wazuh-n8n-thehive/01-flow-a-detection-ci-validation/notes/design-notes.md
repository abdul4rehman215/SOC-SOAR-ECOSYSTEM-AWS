# Flow A Design Notes

Flow A intentionally runs validation as command/script nodes instead of putting complex logic inside n8n nodes. This keeps n8n focused on orchestration and keeps validation code testable as normal Python/Bash scripts.

The workflow also supports skip logic so non-detection PRs do not create noisy CI outputs.
