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
2. **Detect** — identify drift, spikes, oscillation, or divergence.
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

- `semantic_pressure` — overloaded W3 governance/replay vocabulary pressure.
- `dependency_fatigue` — import breadth and repeated coupling points.
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
