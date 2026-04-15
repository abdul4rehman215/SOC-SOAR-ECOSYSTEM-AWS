# ✅ Flow D — TheHive Case Closure Sync

Flow D closes the lifecycle loop. It polls TheHive for recently closed or resolved cases, normalizes the closure record, maps it back to tracked findings, updates DataTable, and posts a Slack closure sync notification.

## Main workflow logic

```mermaid
flowchart LR
    A[Schedule / manual trigger] --> B[Init Flow D config]
    B --> C[Search TheHive cases]
    C --> D[Select recently closed project cases]
    D --> E[Normalize closed case record]
    E --> F[Build DataTable update]
    E --> G[Build Slack message]
    F --> H[Upsert final state]
    G --> I[Slack closure notify]
```

## Why it matters
When the final case outcome never returns to the tracking layer, metrics and evidence trails stay incomplete. Flow D proves that closure is part of the automation lifecycle, not an afterthought.
