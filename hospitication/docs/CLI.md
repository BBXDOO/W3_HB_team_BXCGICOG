# Hospitication CLI

```bash
python -m hospitication.cli --repo . --format markdown
python -m hospitication.cli --repo . --format json --output report.json
```

Options:

- `--repo`: repository root to observe.
- `--format`: `markdown` or `json`.
- `--output`: optional output path.
- `--timestamp`: explicit deterministic timestamp for replayable reports.

The CLI does not perform destructive actions. Writing `--output` only writes the
rendered report to the requested path.
