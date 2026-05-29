# W3 Integration Guide v0.3

This guide describes the integration-grade flow connecting EP_SIGNAL, W3DB,
Hospitication, Pilot 2 layer separation, and Semantic Router interpretation.

## Integration flow

```text
EP_SIGNAL
  -> integrations.ep_signal_w3db.store_ep_signal_to_w3db
  -> W3DB XIZ/TUF/FBD/WHB/PRX
  -> Hospitication report/signals
  -> hospitication.w3db_adapter.store_hospitication_report_to_w3db
  -> scripts/enforce_layer_separation.py --hospitication-signals report.json
  -> core.semantic_router.interpret_hospitication_report
```

## Guarantees

- EP_SIGNAL payloads are decoded and observed; they are not rewritten.
- W3DB records are appended through the existing relation flow.
- Hospitication emits immutable signals and proposal-only recovery guidance.
- Pilot 2 can use Hospitication signals as early-warning context to downgrade a
  temporary RED to YELLOW, but this is recorded as perception, not execution.
- Semantic Router interpretation creates derived references only and must not
  overwrite signals or reports.

## Component commands

```bash
python -m hospitication.cli --repo . --format json --output hospitication-report.json
python scripts/enforce_layer_separation.py --json --hospitication-signals hospitication-report.json
python examples/use_semantic_router_hospitication.py
```

## References

- `docs/standards/referencing_standard.md`
- `protocol/EP_SIGNAL/INTERPRETATION_BOUNDARY_PAPER.md`
- `hospitication/docs/ARCHITECTURE.md`
- `core/semantic_router.py`
