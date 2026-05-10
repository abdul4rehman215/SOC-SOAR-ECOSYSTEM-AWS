# 🧠 📊 Supporting Workflows Implementation Decisions

- Keep workflow responsibility narrow and testable.
- Write evidence to DataTables for MVP-grade auditability.
- Prefer analyst-readable Slack and GitHub/TheHive messages over raw JSON dumps.
- Keep secrets outside exported workflow JSON.
- Preserve both success and failure evidence because SOC workflows must prove controls, not only happy paths.
