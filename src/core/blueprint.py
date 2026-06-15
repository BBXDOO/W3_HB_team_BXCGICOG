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

Supported field groups:
  BLUEPRINT / NAME, TARGET, MODE       — identity / scope
  INPUT, OUTPUT, CONSTRAINT            — structured IO and boundary notes
  LIB, CORE, BRIDGE                    — dependency declarations
  OPTIONAL, PARTITION                  — optional features and structural partitions
  ROLE                                 — semantic role in the system
  BOUNDARY, TRACE, ENV                 — governance and environment expectations

Parsing:
  Canonical format is KEY:VALUE per line (or comma-separated inline).
  INPUT/OUTPUT/CONSTRAINT can use KEY:subkey=value.
"""

from __future__ import annotations

from typing import Dict, FrozenSet, List, Mapping, Optional


# ---------------------------------------------------------------------------
# Validation constants
# ---------------------------------------------------------------------------

#: Fields whose values are treated as comma-separated lists.
LIST_FIELDS: FrozenSet[str] = frozenset({
    "LIB", "OPTIONAL", "PARTITION", "LAYERS", "READ", "DENY",
})

#: Non-executing modes accepted by the foundation model.
ALLOWED_MODES: FrozenSet[str] = frozenset({
    "observe", "plan", "review", "cross", "reference", "draft", "template",
})

#: Recognised blueprint field names (checked during parsing — intentionally light).
KNOWN_FIELDS: FrozenSet[str] = frozenset({
    "BLUEPRINT", "NAME", "TARGET", "MODE", "INPUT", "OUTPUT", "CONSTRAINT",
    "LIB", "CORE", "BRIDGE", "OPTIONAL", "PARTITION", "ROLE", "BOUNDARY",
    "TRACE", "ENV", "LAYERS", "READ", "DENY", "CONTINUITY", "REBASE",
    "MEANING_MODE", "CONTEXT_MODE", "MODEW", "PAPER",
})


# ---------------------------------------------------------------------------
# BlueprintError
# ---------------------------------------------------------------------------

class BlueprintError(ValueError):
    """Raised when a Blueprint fails validation."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _normalize_mapping(value: Optional[Mapping[str, object]]) -> Dict[str, object]:
    return {str(key): item for key, item in dict(value or {}).items()}


def _split_key_value(value: str) -> tuple[str, str]:
    if "=" not in value:
        return value.strip(), ""
    left, right = value.split("=", 1)
    return left.strip(), right.strip()


# ---------------------------------------------------------------------------
# Blueprint class
# ---------------------------------------------------------------------------

class Blueprint:
    """Declarative setup/plan model for MPCP / W3Lgu system units.

    The class supports two compatible construction styles:

    - structured foundation style:
      ``Blueprint(name="REPORT", target="daily_summary", mode="observe")``
    - raw field style:
      ``Blueprint({"BLUEPRINT": "REPORT", "TARGET": "daily_summary"})``

    It remains declarative. It does not execute, run, or mutate runtime state.
    """

    def __init__(
        self,
        fields: Optional[Dict[str, object]] = None,
        *,
        name: Optional[str] = None,
        target: Optional[str] = None,
        mode: str = "observe",
        inputs: Optional[Mapping[str, object]] = None,
        outputs: Optional[Mapping[str, object]] = None,
        constraints: Optional[Mapping[str, object]] = None,
        **extra_fields: object,
    ) -> None:
        raw_fields: Dict[str, object] = {}

        if fields is not None:
            if not isinstance(fields, Mapping):
                raise TypeError("Blueprint fields must be a mapping")
            raw_fields.update(dict(fields))

        if name is not None:
            raw_fields["BLUEPRINT"] = name
        if target is not None:
            raw_fields["TARGET"] = target
        if mode is not None:
            raw_fields["MODE"] = mode
        if inputs is not None:
            raw_fields["INPUTS"] = _normalize_mapping(inputs)
        if outputs is not None:
            raw_fields["OUTPUTS"] = _normalize_mapping(outputs)
        if constraints is not None:
            raw_fields["CONSTRAINTS"] = _normalize_mapping(constraints)
        raw_fields.update(extra_fields)

        self._fields: Dict[str, object] = {}
        self.inputs: Dict[str, object] = {}
        self.outputs: Dict[str, object] = {}
        self.constraints: Dict[str, object] = {}

        for key, value in raw_fields.items():
            normalized = str(key).strip().upper()
            if normalized == "NAME":
                normalized = "BLUEPRINT"
            if normalized == "INPUTS" and isinstance(value, Mapping):
                self.inputs.update(_normalize_mapping(value))
                continue
            if normalized == "OUTPUTS" and isinstance(value, Mapping):
                self.outputs.update(_normalize_mapping(value))
                continue
            if normalized == "CONSTRAINTS" and isinstance(value, Mapping):
                self.constraints.update(_normalize_mapping(value))
                continue
            if normalized == "INPUT":
                if isinstance(value, Mapping):
                    self.inputs.update(_normalize_mapping(value))
                else:
                    subkey, subvalue = _split_key_value(str(value))
                    if subkey:
                        self.inputs[subkey] = subvalue
                continue
            if normalized == "OUTPUT":
                if isinstance(value, Mapping):
                    self.outputs.update(_normalize_mapping(value))
                else:
                    subkey, subvalue = _split_key_value(str(value))
                    if subkey:
                        self.outputs[subkey] = subvalue
                continue
            if normalized == "CONSTRAINT":
                if isinstance(value, Mapping):
                    self.constraints.update(_normalize_mapping(value))
                else:
                    subkey, subvalue = _split_key_value(str(value))
                    if subkey:
                        self.constraints[subkey] = subvalue
                continue
            if normalized in LIST_FIELDS and isinstance(value, str):
                self._fields[normalized] = [item.strip() for item in value.split(",") if item.strip()]
            else:
                self._fields[normalized] = value

        self.validate()

    # ------------------------------------------------------------------
    # Structured properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        return str(self._fields.get("BLUEPRINT", ""))

    @property
    def target(self) -> str:
        return str(self._fields.get("TARGET", ""))

    @property
    def mode(self) -> str:
        return str(self._fields.get("MODE", "observe"))

    # ------------------------------------------------------------------
    # Field access
    # ------------------------------------------------------------------

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Return a single-value field (raw string or first list element)."""
        normalized = key.upper()
        if normalized == "NAME":
            normalized = "BLUEPRINT"
        val = self._fields.get(normalized, default)
        if isinstance(val, list):
            return val[0] if val else default
        return val  # type: ignore[return-value]

    def get_list(self, key: str) -> List[str]:
        """Return a field as a list (empty list if absent)."""
        val = self._fields.get(key.upper())
        if val is None:
            return []
        if isinstance(val, list):
            return [str(item) for item in val]
        return [str(val)]

    def has(self, key: str) -> bool:
        """Return True if the field is present."""
        normalized = key.upper()
        if normalized == "NAME":
            normalized = "BLUEPRINT"
        return normalized in self._fields

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """Validate identity and boundary fields without enforcing execution."""

        if not str(self._fields.get("BLUEPRINT", "")).strip():
            raise BlueprintError("Blueprint missing required field: name")
        if "TARGET" in self._fields and not str(self._fields.get("TARGET", "")).strip():
            raise BlueprintError("Blueprint missing required field: target")
        mode = str(self._fields.get("MODE", "observe")).strip()
        if not mode:
            raise BlueprintError("Blueprint missing required field: mode")
        if mode not in ALLOWED_MODES:
            raise BlueprintError(f"Blueprint invalid mode: {mode}")

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return all fields as a plain dict in the structured foundation shape."""

        result = dict(self._fields)
        result["BLUEPRINT"] = self.name
        if self.target:
            result["TARGET"] = self.target
        result["MODE"] = self.mode
        if self.inputs:
            result["INPUTS"] = dict(self.inputs)
        if self.outputs:
            result["OUTPUTS"] = dict(self.outputs)
        if self.constraints:
            result["CONSTRAINTS"] = dict(self.constraints)
        return result

    def to_w3lgu(self) -> str:
        """Serialize to W3Lgu-MPCP-Blueprint canonical KEY:VALUE format."""

        lines: List[str] = [f"BLUEPRINT:{self.name}"]
        if self.target:
            lines.append(f"TARGET:{self.target}")
        lines.append(f"MODE:{self.mode}")

        for key, value in self.inputs.items():
            lines.append(f"INPUT:{key}={value}")
        for key, value in self.outputs.items():
            lines.append(f"OUTPUT:{key}={value}")
        for key, value in self.constraints.items():
            lines.append(f"CONSTRAINT:{key}={value}")

        for key, val in self._fields.items():
            if key in {"BLUEPRINT", "TARGET", "MODE"}:
                continue
            if isinstance(val, list):
                lines.append(f"{key}:{','.join(str(x) for x in val)}")
            else:
                lines.append(f"{key}:{val}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Blueprint(name={self.name!r}, target={self.target!r}, mode={self.mode!r})"


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_blueprint(text: str, *, validate: bool = True) -> Blueprint:
    """Parse a W3Lgu-style KEY:VALUE Blueprint declaration."""

    if not isinstance(text, str):
        raise TypeError(f"Blueprint text must be a str, got {type(text).__name__!r}")

    fields: Dict[str, object] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        _parse_line_into(line, fields)

    if validate:
        return Blueprint(fields)
    try:
        return Blueprint(fields)
    except BlueprintError:
        bp = object.__new__(Blueprint)
        bp._fields = fields
        bp.inputs = {}
        bp.outputs = {}
        bp.constraints = {}
        return bp


def _parse_line_into(line: str, fields: Dict[str, object]) -> None:
    """Parse one Blueprint line and merge the results into `fields`."""

    tokens = line.split()
    if len(tokens) > 1 and all(":" in token for token in tokens):
        for token in tokens:
            _parse_line_into(token, fields)
        return

    parts = line.split(",")
    current_key: Optional[str] = None
    current_values: List[str] = []

    for part in parts:
        if ":" in part:
            left, right = part.split(":", 1)
            if _is_field_name(left.strip()):
                if current_key is not None:
                    _flush(current_key, current_values, fields)
                current_key = left.strip().upper()
                current_values = [right.strip()] if right.strip() else []
                continue
        if current_key is not None:
            current_values.append(part.strip())

    if current_key is not None:
        _flush(current_key, current_values, fields)


def _flush(key: str, values: List[str], fields: Dict[str, object]) -> None:
    """Commit accumulated key/values to the fields dict."""

    normalized = "BLUEPRINT" if key == "NAME" else key
    if normalized in LIST_FIELDS:
        fields[normalized] = [value for value in values if value]
    elif normalized in {"INPUT", "OUTPUT", "CONSTRAINT"}:
        value = ",".join(values)
        if normalized in fields and isinstance(fields[normalized], dict):
            subkey, subvalue = _split_key_value(value)
            if subkey:
                fields[normalized][subkey] = subvalue  # type: ignore[index]
        else:
            subkey, subvalue = _split_key_value(value)
            fields[normalized] = {subkey: subvalue} if subkey else value
    else:
        fields[normalized] = ",".join(values)


def _is_field_name(value: str) -> bool:
    """Return True if value looks like a Blueprint field name."""

    if not value:
        return False
    if not value[0].isalpha() or not value[0].isupper():
        return False
    return all(char.isalpha() or char == "_" or char.isdigit() for char in value) and value == value.upper()
