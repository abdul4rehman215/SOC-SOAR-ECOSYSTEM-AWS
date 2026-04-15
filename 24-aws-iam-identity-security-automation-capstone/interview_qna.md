# AWS IAM Identity Security Automation Capstone — Interview Q&A

## What problem does this capstone solve?
It solves the fragmentation problem in cloud identity operations by connecting detection, enrichment, containment, proactive IAM hygiene, and case closure into one lifecycle.

## Why split it into four workflows instead of one giant workflow?
Each flow proves a distinct SOC capability and is easier to test, document, and maintain independently.

## Why use n8n here?
n8n acts as the orchestration layer. It makes branching, enrichment, notification, ticketing, and state updates easy to visualize and iterate.

## Why is Flow A important before Flow B?
Flow A produces the enriched alert context and stable alert reference that Flow B later promotes into a case.

## What is the value of Flow C if Flow A and Flow B already exist?
Flow C adds proactive security operations. It detects posture drift such as missing MFA or unused keys before it becomes abuse.

## Why does Flow D matter?
Many projects automate detection but never synchronize case outcomes. Flow D closes the lifecycle by reflecting TheHive closure back into tracking data and Slack reporting.

## What metrics does this improve?
Expected improvements include lower MTTD, lower MTTR, reduced alert fatigue, and better response consistency.

## Why include both TheHive and non-TheHive variants?
That keeps the prototype adaptable to other ticketing platforms and preserves workflow evolution for learning.
