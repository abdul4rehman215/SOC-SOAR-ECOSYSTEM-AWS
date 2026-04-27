# Supporting Workflows Design Notes

The support workflows are intentionally generic enough to be reused. The dashboard collector stores event-level metrics rather than trying to create a full BI dashboard. The global error handler creates a dead-letter trail. The case closure sync closes the loop with TheHive.
