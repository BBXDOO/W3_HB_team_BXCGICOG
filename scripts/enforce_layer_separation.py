"""Pilot 2 layer separation enforcement.

This checker is intentionally conservative. It emits observations and optional
W3DB records; it never rewrites source files or changes historical truth.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.w3db.flow import run_flow
from src.w3db.store import W3DBStore

REFERENCE_DOCS = (
    "docs/standards/referencing_standard.md",
    "protocol/EP_SIGNAL/INTERPRETATION_BOUNDARY_PAPER.md",
    "core/governance/rules/w3_ruleset.yml",
    "hospitication/docs/ARCHITECTURE.md",
)

EXCEPTION_ZONES = (
    "SYSTEM",
    "TESTS",
    "EP_SIGNAL",
)

DEFAULT_PATHS = (
    "core",
    "protocol",
    "hospitication",
    "integrations",
    "scripts",
)


@dataclass(frozen=True)
class LayerViolation:
    path: str
    severity: str
    rule: str
    message: str
    references: tuple[str, ...]
    adjusted_by_signal: bool = False


def evaluate_paths(
    paths: tuple[str, ...],
    *,
    hospitication_signals: tuple[dict[str, Any], ...] = (),
) -> tuple[LayerViolation, ...]:
    """Evaluate layer-boundary pressure for paths without mutating files."""

    violations: list[LayerViolation] = []
    signal_bridge_active = bool(hospitication_signals)
    for raw_path in sorted(paths):
        path = Path(raw_path)
        if not path.exists():
            continue
        if _is_exception_zone(path):
            continue
        if path.is_dir():
            files = sorted(item for item in path.rglob("*") if item.is_file())
        else:
            files = [path]
        for file_path in files:
            if any(part in {".git", "__pycache__", ".pytest_cache"} for part in file_path.parts):
                continue
            if file_path.as_posix().endswith("scripts/enforce_layer_separation.py"):
                continue
            text = _read_text(file_path)
            if _is_code_path(file_path) and _has_authority_leakage(text):
                severity = "YELLOW" if signal_bridge_active else "RED"
                violations.append(
                    LayerViolation(
                        path=file_path.as_posix(),
                        severity=severity,
                        rule="authority_leakage",
                        message="Execution/authority wording found outside exception zones.",
                        references=REFERENCE_DOCS,
                        adjusted_by_signal=signal_bridge_active,
                    )
                )
            elif _has_interpretation_pressure(text):
                violations.append(
                    LayerViolation(
                        path=file_path.as_posix(),
                        severity="YELLOW",
                        rule="interpretation_pressure",
                        message="Interpretation language should reference source truth/report artifacts.",
                        references=REFERENCE_DOCS,
                    )
                )
    return tuple(violations)


def load_hospitication_signals(path: str | None) -> tuple[dict[str, Any], ...]:
    """Load Hospitication report/signals JSON for severity bridge input."""

    if not path:
        return ()
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        signals = payload.get("signals", [])
    else:
        signals = payload
    return tuple(signal for signal in signals if isinstance(signal, dict))


def record_violations_to_w3db(
    violations: tuple[LayerViolation, ...],
    *,
    store: W3DBStore | None = None,
) -> tuple[dict[str, Any], ...]:
    """Append violation observations to W3DB and return compact outputs."""

    outputs: list[dict[str, Any]] = []
    for index, violation in enumerate(violations):
        confidence = 0.9 if violation.severity == "RED" else 0.5
        flow = run_flow(
            input_event=f"Layer separation {violation.severity}:{violation.path}:{violation.rule}",
            cix_id="PILOT2_LAYER_SEPARATION",
            confidence=confidence,
            xiz_id=f"XIZ-LAYER-{index:04d}",
            tuf_id=f"TUF-LAYER-{index:04d}",
            fbd_id=f"FBD-LAYER-{index:04d}",
            whb_id=f"WHB-LAYER-{index:04d}",
            prx_id=f"PRX-LAYER-{index:04d}",
            store=store,
        )
        outputs.append(flow["output"])
    return tuple(outputs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Enforce W3 layer separation boundaries.")
    parser.add_argument("paths", nargs="*", default=list(DEFAULT_PATHS))
    parser.add_argument("--ci-mode", action="store_true", help="Exit non-zero on RED violations")
    parser.add_argument("--dry-run", action="store_true", help="Do not record W3DB observations")
    parser.add_argument("--w3db-store", action="store_true", help="Record violations to in-memory W3DB")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument("--hospitication-signals", help="Path to Hospitication JSON report or signals list")
    args = parser.parse_args(argv)

    signals = load_hospitication_signals(args.hospitication_signals)
    violations = evaluate_paths(tuple(args.paths), hospitication_signals=signals)
    w3db_outputs: tuple[dict[str, Any], ...] = ()
    if args.w3db_store and not args.dry_run:
        w3db_outputs = record_violations_to_w3db(violations)

    payload = {
        "violations": [asdict(violation) for violation in violations],
        "w3db_outputs": w3db_outputs,
        "references": REFERENCE_DOCS,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        _print_human(violations)

    if args.ci_mode and any(v.severity == "RED" for v in violations):
        return 1
    return 0


def _is_exception_zone(path: Path) -> bool:
    parts = {part.upper() for part in path.parts}
    if "TESTS" in parts or "EP_SIGNAL" in parts:
        return True
    return path.as_posix().startswith("SYSTEM/")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _is_code_path(path: Path) -> bool:
    return path.suffix.lower() in {".py", ".js", ".ts", ".tsx", ".sh"}


def _has_authority_leakage(text: str) -> bool:
    lower = text.lower()
    return "overwrite truth" in lower or "mutate truth" in lower or "execute recovery" in lower


def _has_interpretation_pressure(text: str) -> bool:
    lower = text.lower()
    return "interpret" in lower and "references" not in lower and "reference" not in lower


def _print_human(violations: tuple[LayerViolation, ...]) -> None:
    if not violations:
        print("Layer separation: OK")
        return
    for violation in violations:
        marker = "🔴" if violation.severity == "RED" else "🟡"
        print(f"{marker} {violation.severity} {violation.path} {violation.rule}: {violation.message}")


if __name__ == "__main__":
    raise SystemExit(main())
