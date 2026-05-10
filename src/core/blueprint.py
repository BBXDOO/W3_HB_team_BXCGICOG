"""
Blueprint — Declarative Setup / Plan Model
------------------------------------------
Blueprint defines the shape and setup of a system or context unit
in the MPCP / W3Lgu ecosystem.

Core rule (from mpcp_blueprint_paper.md and W3LGU_MPCP_BLUEPRINT_PROFILE.md):
  "Blueprint defines setup, not execution."

Blueprint is:
  - declarative — describes what, not how-at-runtime
  - reusable — can be loaded and applied across environments
  - readable — KEY:VALUE format, human-readable at a glance
  - bounded — validated against required fields before use

Blueprint is NOT:
  - a runtime log
  - source code
  - a one-time command script
  - an imperative execution plan

Supported field groups (aligned with W3Lgu-MPCP-Blueprint Profile):
  NAME, TARGET, MODE       — identity / scope
  LIB, CORE, BRIDGE        — dependency declarations
  OPTIONAL, PARTITION      — optional features and structural partitions
  ROLE                     — semantic role in the system
  BOUNDARY, TRACE, ENV     — governance and environment expectations

Parsing:
  Canonical format is KEY:VALUE per line (or comma-separated inline).
  Multi-value fields use comma-separated values.
"""

from __future__ import annotations

from typing import Dict, FrozenSet, List, Optional


# ---------------------------------------------------------------------------
# Validation constants
# ---------------------------------------------------------------------------

#: Fields that MUST be present in every valid Blueprint.
REQUIRED_FIELDS: FrozenSet[str] = frozenset({"NAME"})

#: Fields whose values are treated as comma-separated lists.
LIST_FIELDS: FrozenSet[str] = frozenset({
    "LIB", "OPTIONAL", "PARTITION", "LAYERS", "READ", "DENY",
})

#: Recognised blueprint field names (checked during validation — not exhaustive).
KNOWN_FIELDS: FrozenSet[str] = frozenset({
    "NAME", "TARGET", "MODE", "LIB", "CORE", "BRIDGE",
    "OPTIONAL", "PARTITION", "ROLE", "BOUNDARY", "TRACE", "ENV",
    # Condien-oriented blueprint fields
    "LAYERS", "READ", "DENY", "CONTINUITY", "REBASE", "MEANING_MODE",
    "CONTEXT_MODE", "MODEW", "PAPER",
})


# ---------------------------------------------------------------------------
# BlueprintError
# ---------------------------------------------------------------------------

class BlueprintError(ValueError):
    """Raised when a Blueprint fails validation."""


# ---------------------------------------------------------------------------
# Blueprint class
# ---------------------------------------------------------------------------

class Blueprint:
    """
    Declarative setup/plan model for MPCP / W3Lgu system units.

    Holds a KEY:VALUE field set parsed from a canonical Blueprint declaration.
    The fields describe the desired shape of a system or execution context —
    not the runtime steps to achieve it.

    Parameters
    ----------
    fields : dict
        Raw parsed fields from a Blueprint declaration.
        Multi-value fields (LIB, PARTITION, etc.) are stored as lists.

    Usage
    -----
    >>> bp = Blueprint({"NAME": "CONDIEN_RUNTIME", "TARGET": "linux",
    ...                 "MODE": "full", "LIB": ["file", "event"]})
    >>> bp.get("NAME")
    'CONDIEN_RUNTIME'
    >>> bp.get_list("LIB")
    ['file', 'event']
    """

    def __init__(self, fields: Dict[str, object]) -> None:
        # Store a defensive copy; normalise list fields
        self._fields: Dict[str, object] = {}
        for k, v in fields.items():
            key = k.strip().upper()
            if key in LIST_FIELDS and isinstance(v, str):
                self._fields[key] = [x.strip() for x in v.split(",") if x.strip()]
            else:
                self._fields[key] = v

    # ------------------------------------------------------------------
    # Field access
    # ------------------------------------------------------------------

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Return a single-value field (raw string or first list element)."""
        val = self._fields.get(key.upper(), default)
        if isinstance(val, list):
            return val[0] if val else default
        return val  # type: ignore[return-value]

    def get_list(self, key: str) -> List[str]:
        """Return a field as a list (empty list if absent)."""
        val = self._fields.get(key.upper())
        if val is None:
            return []
        if isinstance(val, list):
            return list(val)
        return [str(val)]

    def has(self, key: str) -> bool:
        """Return True if the field is present."""
        return key.upper() in self._fields

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate this Blueprint against REQUIRED_FIELDS.

        Raises BlueprintError if any required field is missing.
        This method does NOT enforce runtime constraints — it only checks
        that the declarative plan is structurally complete.
        """
        missing = [f for f in sorted(REQUIRED_FIELDS) if not self.has(f)]
        if missing:
            raise BlueprintError(
                f"Blueprint missing required field(s): {', '.join(missing)}"
            )

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return all fields as a plain dict."""
        return dict(self._fields)

    def to_w3lgu(self) -> str:
        """
        Serialize to W3Lgu-MPCP-Blueprint canonical KEY:VALUE format.

        Multi-value fields are joined with commas.
        The output is human-readable and suitable for logging / exchange.
        """
        lines: List[str] = []
        # NAME first for readability
        if "NAME" in self._fields:
            lines.append(f"NAME:{self._fields['NAME']}")
        for key, val in self._fields.items():
            if key == "NAME":
                continue
            if isinstance(val, list):
                lines.append(f"{key}:{','.join(str(x) for x in val)}")
            else:
                lines.append(f"{key}:{val}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        name = self._fields.get("NAME", "<unnamed>")
        return f"Blueprint(name={name!r}, fields={list(self._fields.keys())})"


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_blueprint(text: str, *, validate: bool = True) -> Blueprint:
    """
    Parse a W3Lgu-style KEY:VALUE Blueprint declaration.

    Supports:
      - One KEY:VALUE pair per line
      - Inline comma-separated pairs: KEY:VALUE,KEY2:VALUE2
      - Multi-value field values: LIB:fs,store,net  (treated as a list)
      - Blank lines and lines without ':' are skipped

    Parameters
    ----------
    text : str
        Raw blueprint declaration string.
    validate : bool
        If True (default), calls Blueprint.validate() after parsing and
        raises BlueprintError if required fields are missing.

    Returns
    -------
    Blueprint
        Parsed and (optionally) validated blueprint instance.

    Raises
    ------
    BlueprintError
        If validate=True and required fields are absent.
    TypeError
        If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Blueprint text must be a str, got {type(text).__name__!r}")

    fields: Dict[str, object] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        _parse_line_into(line, fields)

    bp = Blueprint(fields)
    if validate:
        bp.validate()
    return bp


def _parse_line_into(line: str, fields: Dict[str, object]) -> None:
    """
    Parse a single Blueprint line (possibly containing multiple comma-separated
    KEY:VALUE pairs) and merge the results into `fields`.

    Supports two formats on the same line:
      - Single pair:  ``NAME:CONDIEN_CORE``
      - Multi-pair:   ``CONDIEN:CORE,MODEW:REPORT,PAPER:daily``
      - Multi-value:  ``LIB:fs,store,net``  (treated as a list for LIST_FIELDS)

    A token opening a new field must satisfy ``_is_field_name`` (first character
    alphabetic, remaining characters alpha/digit/_).  Non-conforming tokens are
    treated as additional values for the most recent field key.
    """
    parts = line.split(",")
    current_key: Optional[str] = None
    current_values: List[str] = []

    for part in parts:
        if ":" in part:
            left, right = part.split(":", 1)
            if _is_field_name(left.strip()):
                # Flush the previous accumulated key/values
                if current_key is not None:
                    _flush(current_key, current_values, fields)
                current_key = left.strip().upper()
                current_values = [right.strip()] if right.strip() else []
                continue
        # Not a new key — continuation value for the current key
        if current_key is not None:
            current_values.append(part.strip())

    # Flush the last accumulated pair
    if current_key is not None:
        _flush(current_key, current_values, fields)


def _flush(key: str, values: List[str], fields: Dict[str, object]) -> None:
    """Commit accumulated key/values to the fields dict."""
    if key in LIST_FIELDS:
        fields[key] = [v for v in values if v]
    else:
        fields[key] = ",".join(values)


def _is_field_name(s: str) -> bool:
    """Return True if s looks like a Blueprint field name.

    Rules:
      - Non-empty
      - First character must be an uppercase ASCII letter (A-Z)
      - Remaining characters may be uppercase letters, digits, or underscores
    """
    if not s:
        return False
    if not s[0].isalpha() or not s[0].isupper():
        return False
    return all(c.isalpha() or c == "_" or c.isdigit() for c in s) and s == s.upper()
