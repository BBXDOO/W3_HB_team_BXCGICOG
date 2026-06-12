# commands/

Commands are callable patterns exposed by the pack.

They should be written as intent patterns first, not direct shell/runtime execution.

Example:

```text
COMMAND: plan_w3api_gate
INPUT: W3API-GATE.w3md
OUTPUT: dispatch_plan, files_needed, review_notes
MUTATED: false
EXECUTION_ALLOWED: false
```

END
