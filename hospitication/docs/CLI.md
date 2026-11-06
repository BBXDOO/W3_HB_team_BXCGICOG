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
- `--include-prototypes`: include `w3_tool_store/xrea/`, excluded by default.

`tools/run_hospitication.py` also accepts `--repo`, `--timestamp`, and
`--include-prototypes`, and prints a concise summary with the actual measured
file count. JSON reports expose `observation_scope`, including skipped entries.
Images, binary data and symlinks are not measured as text. Scores are
single-snapshot heuristics; they do not prove runtime health or time trends.

The CLI does not perform destructive actions. Writing `--output` only writes the
rendered report to the requested path.
