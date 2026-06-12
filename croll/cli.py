"""Dependency-free, cross-platform command-line interface for Cross-L."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

from . import __version__
from .contracts import ContractError, VALIDATORS, validate_artifact
from .cross_l_dispatcher import dispatch_workset
from .table_x import get_workset_from_px, list_px


def _configure_utf8_stdio() -> None:
    """Use UTF-8 for JSON and errors even on legacy Windows console code pages."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="backslashreplace")


def _context(value: Optional[str]) -> Optional[Mapping[str, Any]]:
    if value is None:
        return None

    source = value
    if value.startswith("@"):
        path = Path(value[1:]).expanduser()
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise argparse.ArgumentTypeError(f"cannot read context file {path}: {exc}") from exc

    try:
        context = json.loads(source)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"context must be valid JSON: {exc.msg}") from exc

    if not isinstance(context, dict):
        raise argparse.ArgumentTypeError("context must be a JSON object")
    return context


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="croll",
        description="Build safe, non-executing Cross-L worksets and dispatch plans.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--compact",
        action="store_true",
        help="write compact JSON instead of indented JSON",
    )

    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("lookup", "look up a Table-X workset"),
        ("plan", "build a safe dispatch plan"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("px", help='PX coordinate, for example "1,1" or "PX:[1,1]"')
        command.add_argument(
            "--context",
            type=_context,
            metavar="JSON|@FILE",
            help="Paper context as a JSON object or UTF-8 JSON file",
        )

    commands.add_parser("list", help="list registered Table-X coordinates")
    validate = commands.add_parser("validate", help="validate a CROLL JSON artifact")
    validate.add_argument("kind", choices=sorted(VALIDATORS), help="artifact contract")
    validate.add_argument("file", type=Path, help="UTF-8 JSON artifact path")
    return parser


def _write_json(payload: Any, compact: bool) -> None:
    indent = None if compact else 2
    separators = (",", ":") if compact else None
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=indent, separators=separators)
    sys.stdout.write("\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    _configure_utf8_stdio()
    parser = _parser()
    args = parser.parse_args(argv)

    if args.command == "lookup":
        payload = get_workset_from_px(args.px, paper_context=args.context)
    elif args.command == "plan":
        payload = dispatch_workset(args.px, paper_context=args.context)
    elif args.command == "validate":
        try:
            artifact = json.loads(args.file.read_text(encoding="utf-8"))
            validate_artifact(args.kind, artifact)
        except (OSError, json.JSONDecodeError, ContractError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        payload = {
            "contract_version": "1.0",
            "valid": True,
            "kind": args.kind,
            "file": str(args.file),
        }
    else:
        payload = {"contract_version": "1.0", "coordinates": list_px()}

    _write_json(payload, args.compact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
