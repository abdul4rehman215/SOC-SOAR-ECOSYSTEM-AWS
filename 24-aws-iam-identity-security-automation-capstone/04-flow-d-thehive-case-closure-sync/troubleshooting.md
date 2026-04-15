# Flow D — Troubleshooting

- In Code nodes, every returned item must look like `{ json: { ... } }`.
- `.all()` and `.first()` must match the node execution mode.
- If no output is emitted, inspect recent-lookback and project-source matching logic.
