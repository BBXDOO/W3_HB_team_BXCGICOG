# Hospitication

Structural Recovery & Signal Stability Framework for the W3 ecosystem.

> Do not rewrite truth. Recover structural integrity.

Hospitication is a production-oriented health observer for W3 repositories. It is
not a linter and it is not a demo monitor. It observes structural pressure across
memory, governance, protocol, replay, outcome, and coordination surfaces, emits
immutable signals, and produces non-mutating recovery proposals.

## Scope

Hospitication separates the pipeline into explicit layers:

1. **Observe** — read repository structure without mutation.
2. **Detect** — apply single-snapshot pressure thresholds and compare metric spread.
3. **Emit** — convert detections into immutable signal envelopes.
4. **Evaluate** — compute health/burden metrics.
5. **Recover** — propose mitigation only; never apply changes by default.
6. **Report** — render deterministic Markdown or JSON without changing state.

## Production Guarantees

- Uses Python standard library only.
- Truth/signal/report contracts use immutable dataclasses where appropriate.
- Reports are deterministic by sorted ordering and configurable fixed timestamp.
- Recovery proposals are non-destructive and have `destructive=False`.
- Existing W3 memory/governance/replay files are observed but not rewritten.
- Signal detection never diagnoses root cause.
- Detector modules never call recovery modules.
- Reporter modules never mutate repository state.

## Package Layout

```text
hospitication/
├── core/          # contracts, config, registry
├── signal/        # observer, detector, emitter, envelope helpers
├── analysis/      # structural burden analyzers
├── recovery/      # non-mutating proposals and mitigation catalog
├── reporter/      # deterministic markdown/json renderers
├── docs/          # design notes and integration guidance
└── cli.py         # command-line entrypoint
```

## CLI Usage

Run a Markdown report against the current repository:

```bash
python -m hospitication.cli --repo . --format markdown
```

Write deterministic JSON:

```bash
python -m hospitication.cli --repo . --format json --output hospitication-report.json
```

Use a concrete timestamp for replayable CI output:

```bash
python -m hospitication.cli --repo . --format json --timestamp 2026-05-28T00:00:00Z
```

## Analyzer Coverage

### Observation scope — v0.2.0

The default scan excludes the reference prototype at `w3_tool_store/xrea/`.
Use `--include-prototypes` on either CLI to explicitly include it. This changes
the measurement scope; a lower score is not evidence of a healthier runtime.

Only supported UTF-8 text files are measured. Images, unsupported formats,
binary content, symbolic links, oversized files and unreadable entries are
skipped. Ignored/excluded directories are pruned before traversal. JSON reports
include `observation_scope` with observer version, extension lists, exclusions,
size limit, measured file count and skip counts. Directory skip counts count
directories, not the unknown number of files within them. `.mjs` and `.cjs`
are recognized as code, but import analysis remains Python-only and reports
other code files as unmeasured rather than using them to dilute Python scores.

Scores are structural heuristics, not diagnoses, runtime test results, or
proof of health. The legacy `drift` type means a threshold in one snapshot;
there is no historical baseline. `oscillation` is no longer emitted by this
detector because alternating scores for different metrics do not prove a
time trend. Historical signal types and stored reports remain unchanged.
Vocabulary coverage now includes all terms used by the semantic/replay analyzers.
Both that correction and the scope changes make v0.1 and v0.2 scores unsuitable
for direct trend comparison. Compare runs only with the same version and scope.
The default epoch timestamp remains a reproducibility setting; pass
`--timestamp` to label an actual observation date.

```bash
python tools/run_hospitication.py --repo . --timestamp 2026-11-06T00:00:00Z
python -m hospitication.cli --repo . --format json --include-prototypes
```

- `semantic_pressure` — overloaded W3 governance/replay vocabulary pressure.
- `dependency_fatigue` — Python import-root breadth and repeated import roots (not a dependency graph).
- `replay_complexity` — event/outcome/ledger/checkpoint/replay surfaces.
- `recovery_resistance` — large files with limited test/doc counterweight.
- `cognitive_cost` — file count, line breadth, and configuration surface.

## W3 Integration Notes

Hospitication is intentionally read-only over W3 surfaces such as:

- `core/memory/`
- `core/governance/`
- `core/events/`
- `core/runtime/`
- `iget/`
- `docs/`

It can be wired into CI or agent coordination as a health report generator. If a
future integration writes to the W3 memory bus or outcome ledger, that integration
should add a new derived record rather than mutate existing truth.

## Development

Run tests:

```bash
python -m pytest tests/test_hospitication_core.py tests/test_hospitication_cli.py
```

Run syntax checks:

```bash
python -m compileall hospitication tests
```
