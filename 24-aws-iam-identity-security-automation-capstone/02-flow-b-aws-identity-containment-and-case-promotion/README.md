# 🧯 Flow B — AWS Identity Containment and Case Promotion

Flow B operationalizes the incident. It receives an approved containment event or Security Hub custom action, disables the exposed IAM access key when appropriate, updates analyst channels, finds the matching TheHive alert from Flow A, promotes it into a case, and leaves a case comment documenting the action.

## Main workflow logic

```mermaid
flowchart LR
    A[Security Hub custom action / approved input] --> B[Parse + validate trusted topic]
    B --> C[Normalize custom action]
    C --> D{Contain action matched?}
    D -- yes --> E{Has key + principal?}
    E -- yes --> F[UpdateAccessKey -> Inactive]
    E -- no --> G[Set missing field path]
    F --> H[Extract containment result]
    G --> H
    H --> I[Build TheHive context]
    I --> J[Search matching TheHive alert]
    J --> K[Get alert detail]
    K --> L[Promote alert to case + create case comment]
    L --> M[Finalize status + Slack + DataTable update]
```

## Why it matters
This is where the project stops being notification-only and becomes operational. The workflow proves that a validated cloud identity issue can trigger a controlled response and a real case-management handoff.
