# 🧹 Flow C — AWS IAM Hygiene Monitoring and Alerting

Flow C is the proactive side of the capstone. It runs on a schedule, generates the AWS IAM credential report, evaluates hygiene issues such as missing MFA or unused keys, sends a Slack digest, updates DataTable, and creates TheHive alerts for actionable hygiene findings.

## Main workflow logic

```mermaid
flowchart LR
    A[Schedule trigger] --> B[Init hygiene config]
    B --> C[Generate IAM credential report]
    C --> D[Wait for report readiness]
    D --> E[Get credential report]
    E --> F[Decode CSV report]
    F --> G[Evaluate hygiene findings]
    G --> H[Build Slack digest]
    G --> I[Explode hygiene findings]
    H --> J[Slack digest]
    I --> K[DataTable upsert]
    I --> L[Build TheHive hygiene context per finding]
    L --> M[Search matching hygiene alert]
    M --> N{Alert exists?}
    N -- no --> O[Create TheHive hygiene alert]
    N -- yes --> P[Mark alert exists]
```

## Why it matters
Flow C moves the project beyond reactive incident response into preventative identity security operations.
