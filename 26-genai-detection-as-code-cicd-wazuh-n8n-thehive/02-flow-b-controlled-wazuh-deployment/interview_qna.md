# Flow B Interview Q&A

## What is Flow B's core value?

It turns detection deployment into a controlled release process instead of manual copying into Wazuh.

## Why require labels and approval?

Detection content can break monitoring or create false positives. Flow B ensures only reviewed and CI-passed content reaches the manager.

## Why include rollback?

Rollback is the safety net for postdeploy failure. Even in an MVP, showing rollback design demonstrates operational thinking.

## Why record deployment runs?

Deployment history is important for auditability. The DataTable row captures both gate decisions and deployment stage outcomes.
