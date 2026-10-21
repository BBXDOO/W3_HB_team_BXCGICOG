# W3 Orchestrated Runtime Circuit

- AM type: III Process
- Status: explicit local execution bridge
- Owner: BBX19 / W3

`engine.py` preserves the legacy result envelope and delegates execution to
`engine_v2.py`. The legacy context now contains a trace ID; callers needing the
old memory-match context must migrate. `engine_v2` selects and invokes one local
module, validates its result, and writes execution memory. `WorkflowRuntime`
uses Orchestration to own the task lifecycle and explicit multi-stage handoffs.

## Run a real local stage

Run from the repository root. Supply an isolated runtime memory path for tests:
`W3_MEMORY_FILE=/tmp/w3-circuit-memory.json python your_runner.py`.

Example `your_runner.py`:

```python
import hashlib
from pathlib import Path
from workflows import orchestration as orc
from workflows.runtime_circuit import WorkflowRuntime

repo = Path.cwd()

def verify_flow(stage, result):
    artifacts = result.get('artifacts', [])
    passed = bool(artifacts)
    for artifact in artifacts:
        path = (repo / artifact['path']).resolve()
        passed = passed and path.is_relative_to(repo) and path.is_file()
        if passed:
            passed = hashlib.sha256(path.read_bytes()).hexdigest() == artifact['sha256']
    return {'passed': passed, 'check': 'flow files exist and match recorded hashes'}

task = orc.new_task('W3-ORC-20261021-1', 'REQUEST', 'NORMAL',
                    {'module': 'BBX19', 'tier': 0},
                    {'summary': 'prepare a local flow draft'})
circuit = WorkflowRuntime(repo / 'reports/runtime-circuit', verifier=verify_flow)
circuit.run(task, [{'task': 'design', 'module': 'ChatGPT',
                    'request': {'intent': 'prepare a flow for log intake'}}])
print(task['status'])  # WAITING_HUMAN: the module marks its draft for review
```

The real ChatGPT local executor creates a Markdown draft, not a remote model
response. The host must authenticate human identity and review evidence. After
review, call `review_stage(task, stage, human=..., evidence=...)`; it independently
runs the verifier again. An unresolved or STOP result cannot be approved through
this method. A final verified stage can then be closed with `orc.advance` and
saved with `orc.save`. For a non-final reviewed stage, queue the next explicit
stage; entering the next execution clears the previous approval.

## Multiple modules and support

Pass a finite list of task keys from `modules/registry.json`. A supplied `module`
must match the registry. The previous agent result is the next stage's default
payload, preserving supplied W3Lgu identity and routing fields. Explicit payloads
can override this transport. Each call gets its own engine trace ID and shares
the Orchestration task ID/source ID. A module's `next` never triggers arbitrary
execution: only stages explicitly authorized in the supplied plan run.

`ACTIVE` is not assumed successful. A host-owned verifier must establish the
specific stage postcondition; verifying a preview cannot establish that a log
was saved or another module executed. Results marked for review pause at the
human gate. A bad runtime contract or failed postcondition blocks the task.

For a blocker, call `circuit.assist` with a host-selected SPECIALIST or TOOL
adapter. Resolved support returns the task to RETURNED. Explicitly retry the
same stage with `execute_stage`; no automatic replay of potentially mutating
work occurs. Execute remaining stages explicitly after verification.

## Persistence and limits

Pipeline plans, local handoffs, results, verification records and task snapshots
are written under the directory passed to the bridge. Local acknowledgement
means the bridge accepted an invocation; it is not evidence that an external AI
received a message. Snapshot writes use the existing atomic Orchestration saver.
Evidence files use unique names and exclusive creation.

The trusted host supplies the verifier, adapter registration, authority context,
and authenticated human decisions. This is not a background daemon, remote AI
connector, or automatic scheduler. It does not claim that a generic evidence
string proves an external action. An interrupted IN_PROGRESS task is not
replayed automatically: inspect recorded evidence and reconcile side effects
first. Concurrent writers to the same task are not supported. A storage failure
is surfaced to the caller; do not retry execution without reconciliation.

The engine now returns FAILED for routing/context exceptions, reports secondary
memory-write errors, and downgrades invalid successful contracts before scoring
memory. Contracts for non-W3Lgu modules retain their existing validation scope.

## Validation

`python -m pytest tests/test_runtime_circuit.py tests/test_orchestration.py tests/test_chatgpt_flow_artifact.py tests/test_runtime_agent_execution.py tests/test_origin_agent_runtime_contracts.py -q`
