# IGET Memory

IGET memory stores local witness traces for v10-preview workflows.

This folder is for human-readable and append-only evidence records such as:

- issue dispatch briefs
- BBX19 approvals
- module invocation requests
- observations and decisions

Runtime JSONL files are intentionally ignored by Git so local Termux/Codespaces
traces do not get committed accidentally.

Current local trace targets:

- `issues.jsonl` — issue brief records created by `python -m iget issue new --record-memory`
- `module_calls.jsonl` — future module invocation requests
- `approvals.jsonl` — future BBX19 approval decisions

Boundary:

- memory is evidence, not authority
- IGET may append local trace records
- IGET must not mutate repo or call modules without BBX19 approval
