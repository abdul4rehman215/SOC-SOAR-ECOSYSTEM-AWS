# Supporting Workflows Interview Q&A

## Why build supporting workflows?

Because SOC automation is not only about the main alert path. You also need failure visibility, dashboard metrics, and lifecycle closure.

## Why use an event collector for dashboards?

It decouples dashboard writes from the main workflows. Each workflow emits metric events; the collector normalizes and stores them consistently.

## Why poll TheHive for closure sync?

In an MVP, polling is simpler than configuring webhooks. The design still demonstrates the lifecycle requirement: case closure should be reflected back in operational records.
