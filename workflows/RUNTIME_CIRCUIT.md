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
this method. Then call `circuit.continue_work(task)` to advance through the saved
remaining plan or close its final stage. The plan cursor, exact stage parameters,
verification state and result references are saved in the optional
`runtime_circuit` task field, covered by the task schema. Reload the task JSON
and call `continue_work` after a host restart. A completed stage is not replayed.
Entering the next execution clears the previous approval; when human review is
required, each subsequent result needs a fresh approval. The original plan and
any request corrections remain in separate evidence files.

## Multiple modules and support

Pass a finite list of task keys from `modules/registry.json`. A supplied `module`
must match the registry. The task payload is the first stage's default input.
The previous agent result is the next stage's default payload, preserving supplied W3Lgu identity and routing fields. Explicit payloads
can override this transport. Each call gets its own engine trace ID and shares
the Orchestration task ID/source ID. A module's `next` never triggers arbitrary
execution: only stages explicitly authorized in the supplied plan run.

`ACTIVE` is not assumed successful. A host-owned verifier must establish the
specific stage postcondition; verifying a preview cannot establish that a log
was saved or another module executed. Results marked for review pause at the
human gate. A bad runtime contract or failed postcondition blocks the task.

For a blocker, call `circuit.assist` with a host-selected SPECIALIST or TOOL
adapter. Resolved support returns the task to RETURNED. Explicitly retry the
same stage and then finish the saved remaining plan with `continue_work`.
The current stage's original effective request is retained on retry. Support
adapters receive deep copies and their output is saved as evidence, so they
cannot change the original task's destination through a mutable reference.

An unresolved REVIEW_REQUIRED/STOP result cannot be approved as if it succeeded.
For corrected inputs, use `revise_stage(task, request=..., actor=..., evidence=...)`
then `continue_work`. This keeps the registered job and module fixed and records
both old and new request parameters before queuing a retry. The trusted host
must reconcile any earlier side effects before authorizing a retry.

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
memory. Stored memory includes both the effective `status` and the executor's
`reported_status`, plus task and trace correlation. If memory writing fails after
execution, the FAILED response retains the executor result and artifacts so the
host can reconcile existing side effects. Contracts for non-W3Lgu modules retain
their existing validation scope.

The bridge assigns runtime `source` from the task's recorded origin, regardless
of a source claimed inside stage input. It preserves `request.target` as the subject
of work (for example W3API);
it does not replace that subject with the executor's name. Invalid stage requests
are rejected before any task state is changed or execution is attempted.

## Validation

`python -m pytest tests/test_runtime_circuit.py tests/test_runtime_circuit_review.py tests/test_orchestration.py tests/test_chatgpt_flow_artifact.py tests/test_runtime_agent_execution.py tests/test_origin_agent_runtime_contracts.py -q`

## Reconcile post-action evidence failures

An adapter may have changed a file or external system before result validation
or evidence storage fails. `ReconciliationRequired` exposes its original
in-memory response as `.result`. A durable `reconciliation_required` flag blocks
support invocation, stage execution, input revision and approval until the host
checks what actually happened. Support attempt metadata is written before the
adapter is called, so a restarted host also refuses an automatic replay.

For a returned runner envelope with unsupported diagnostics, JSON-compatible
artifact and mutation fields are preserved in the failure evidence; unsupported
values are marked by type. The task remains BLOCKED and requires reconciliation.
An evidence-write failure exposes the original response in an exception instead
of discarding it. This is not a guarantee of exactly-once external execution.

After inspecting actual effects, the trusted host calls
`reconcile(task, actor=..., evidence=...)`. For an already completed support action,
pass `support_result=error.result` to record that result and return to the owner
without calling the adapter again. Recovery is keyed by support attempt ID and
does not append the same saved response twice after a snapshot failure. With no
support result, reconciliation only clears uncertainty; retrying remains an
explicit host decision. If the response was lost during a crash, the host must
reconstruct it from actual external state, never infer success from the task ID.

Reloaded `effective_stage` must contain the task/module/request shape and match
the current plan's task and module before any lifecycle transition is made.

The schema now uses an absolute canonical `$id`, keeping nested local references
resolvable with the repository's jsonschema 4.10–4.17 dependency range without
fetching remote documents.
