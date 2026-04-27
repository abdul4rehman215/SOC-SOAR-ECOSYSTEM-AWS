# Flow A Data Model Notes

## flow_a_ci_runs
One row per PR/SHA. Stores the summary state and counts.

## flow_a_ci_changed_files
One row per changed file. Stores path and artifact type.

## flow_a_ci_stage_results
One row per validation stage. Stores stage status, checked/passed/failed counts, and notes.
