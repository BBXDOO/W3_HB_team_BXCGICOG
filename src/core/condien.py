"""
Condien — Adaptive Meaning / State / Context Layer
---------------------------------------------------
Condien is the meaning/state/context carrier in the MPCP system.
It is NOT a plain storage bag — it provides:
  - bounded, layer-aware access (READ/DENY)
  - continuity and rebase semantics (carry-forward, bounded)
  - governance through ROT boundary constraints
  - extensible design without heavy schema

Concept alignment (W3Lgu-Condien Profile):
  - CONDIEN / ROLE / POSITION   → identity
  - MEANING_MODE / CONTEXT_MODE → meaning / context access model
  - LAYER / LAYERS / READ / DENY → layer-aware access
  - CONTINUITY / REBASE         → temporal / context continuity
  - BOUNDARY / ENV              → governance
  - MODEW / PAPER               → binding anchors

Design rule: structure before detail — Condien defines context shape,
not the runtime action itself.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Optional, Set


# ---------------------------------------------------------------------------
# Controlled vocabularies (minimal — extensible)
# ---------------------------------------------------------------------------

MEANING_MODES: FrozenSet[str] = frozenset({
    "adaptive",
    "bounded-adaptive",
    "contextual",
})

CONTEXT_MODES: FrozenSet[str] = frozenset({
    "dynamic",
    "paper-guided",
    "continuity-aware",
})

CONTINUITY_MODES: FrozenSet[str] = frozenset({
    "none",
    "bounded-carry",
    "carry-forward",
    "trace-linked",
})

REBASE_MODES: FrozenSet[str] = frozenset({
    "disabled",
    "bounded",
    "enabled",
})

BOUNDARY_MODES: FrozenSet[str] = frozenset({
    "strict",
    "paper-strict",
    "rot-governed",
})

ENV_MODES: FrozenSet[str] = frozenset({
    "preserve",
    "non-reduced",
})


# ---------------------------------------------------------------------------
# CondienLayer — one layer slot in a Condien's layer stack
# ---------------------------------------------------------------------------

@dataclass
class CondienLayer:
    """
    Represents a single named layer slot within a Condien context.

    Fields:
      name      — layer identifier (e.g. "A", "LAYER_B")
      readable  — True when this layer is readable in the current access scope
      data      — arbitrary key/value payload carried by the layer
      read      — optional key whitelist inside this layer
      deny      — key deny-list inside this layer; deny always wins

    The `read` / `deny` keyword names are kept for compatibility with the
    original MPCP Condien foundation tests.
    """
    name: str
    readable: bool = True
    data: Dict[str, object] = field(default_factory=dict)
    read: Optional[Set[str]] = None
    deny: Set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if self.read is not None and not isinstance(self.read, set):
            self.read = set(self.read)
        if self.deny is None:
            self.deny = set()
        elif not isinstance(self.deny, set):
            self.deny = set(self.deny)

    def can_read(self, key: str) -> bool:
        """Return True when `key` can be read from this layer."""

        if not self.readable:
            return False
        if key in self.deny:
            return False
        if self.read is not None:
            return key in self.read
        return key in self.data

    def read_key(self, key: str) -> object:
        """Read a key from this layer or fail closed with KeyError."""

        if key not in self.data or not self.can_read(key):
            raise KeyError(key)
        return self.data[key]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "readable": self.readable,
            "data": dict(self.data),
            "read": sorted(self.read) if self.read is not None else "all",
            "deny": sorted(self.deny),
        }


# ---------------------------------------------------------------------------
# Condien — core class
# ---------------------------------------------------------------------------

class Condien:
    """
    Condien: adaptive meaning/state/context layer.

    Condien carries meaning, state, and context across execution units
    (Modew, Paper, ROT) in a bounded, layer-aware, and continuity-supporting way.

    It is declarative at the identity level — its shape is defined up-front —
    but allows controlled updates through explicit access semantics.
    """

    def __init__(
        self,
        name: str,
        role: str = "meaning_state_layer",
        layers: Optional[List[str]] = None,
        read_layers: Optional[List[str]] = None,
        deny_layers: Optional[List[str]] = None,
        meaning_mode: str = "bounded-adaptive",
        context_mode: str = "dynamic",
        continuity: str = "bounded-carry",
        rebase: str = "bounded",
        boundary: str = "rot-governed",
        env: str = "preserve",
        modew: Optional[str] = None,
        paper: Optional[str] = None,
    ) -> None:
        if not name or not name.strip():
            raise ValueError("Condien name must be a non-empty string")
        if meaning_mode not in MEANING_MODES:
            raise ValueError(
                f"meaning_mode must be one of {sorted(MEANING_MODES)}, got {meaning_mode!r}"
            )
        if context_mode not in CONTEXT_MODES:
            raise ValueError(
                f"context_mode must be one of {sorted(CONTEXT_MODES)}, got {context_mode!r}"
            )
        if continuity not in CONTINUITY_MODES:
            raise ValueError(
                f"continuity must be one of {sorted(CONTINUITY_MODES)}, got {continuity!r}"
            )
        if rebase not in REBASE_MODES:
            raise ValueError(
                f"rebase must be one of {sorted(REBASE_MODES)}, got {rebase!r}"
            )
        if boundary not in BOUNDARY_MODES:
            raise ValueError(
                f"boundary must be one of {sorted(BOUNDARY_MODES)}, got {boundary!r}"
            )
        if env not in ENV_MODES:
            raise ValueError(
                f"env must be one of {sorted(ENV_MODES)}, got {env!r}"
            )

        self.name = name.strip()
        self.role = role
        self.meaning_mode = meaning_mode
        self.context_mode = context_mode
        self.continuity = continuity
        self.rebase = rebase
        self.boundary = boundary
        self.env = env
        self.modew = modew
        self.paper = paper

        # Build internal layer registry from declared names.
        _layer_names: List[str] = layers or []
        self._layers: Dict[str, CondienLayer] = {
            n: CondienLayer(name=n) for n in _layer_names
        }

        # Access control sets (resolved against declared layers if provided).
        self._read_set: Optional[Set[str]] = (
            set(read_layers) if read_layers is not None else None
        )
        self._deny_set: Set[str] = set(deny_layers) if deny_layers else set()

        # Active layer cursor. The historical foundation test expects the first
        # declared layer to be active by default when it is readable.
        self._active_layer: Optional[str] = None
        for layer_name in self._layers:
            if self.can_read(layer_name):
                self._active_layer = layer_name
                break

        # Continuity carry-forward store (minimal: key→value pairs).
        self._carry: Dict[str, object] = {}
        self.previous: Optional["Condien"] = None
        self.history: List[str] = []

    # ------------------------------------------------------------------
    # Layer access
    # ------------------------------------------------------------------

    def layers(self) -> List[str]:
        """Return declared layer names in order."""
        return list(self._layers.keys())

    def can_read(self, layer_name: str) -> bool:
        """
        Return True if `layer_name` is readable in the current access scope.

        Logic (aligned with W3Lgu-Condien profile):
          - DENY always takes precedence
          - If a READ list is declared, only those layers are readable
          - Otherwise all declared layers are readable
        """
        if layer_name in self._deny_set:
            return False
        if self._read_set is not None:
            return layer_name in self._read_set
        return layer_name in self._layers

    def set_active_layer(self, layer_name: str) -> None:
        """Set the currently active layer cursor."""
        if layer_name not in self._layers:
            raise KeyError(f"Layer {layer_name!r} is not declared in this Condien")
        if not self.can_read(layer_name):
            raise PermissionError(f"Layer {layer_name!r} is not readable (DENY or READ restriction)")
        self._active_layer = layer_name

    @property
    def active_layer(self) -> Optional[str]:
        """Return the name of the currently active layer, or None."""
        return self._active_layer

    def get_layer(self, layer_name: str) -> CondienLayer:
        """Return the CondienLayer object for the given name."""
        if layer_name not in self._layers:
            raise KeyError(f"Layer {layer_name!r} not found in Condien {self.name!r}")
        if not self.can_read(layer_name):
            raise PermissionError(f"Read access denied for layer {layer_name!r}")
        return self._layers[layer_name]

    def add_layer(self, layer_name: str, data: Optional[Dict[str, object]] = None) -> None:
        """Add or replace a layer slot with optional data."""

        if not layer_name or not layer_name.strip():
            raise ValueError("layer_name must be a non-empty string")
        normalized = layer_name.strip()
        self._layers[normalized] = CondienLayer(name=normalized, data=dict(data or {}))
        if self._active_layer is None and self.can_read(normalized):
            self._active_layer = normalized

    def read_from_layer(self, layer_name: str, key: str) -> object:
        """Read a key from a named layer."""

        return self.get_layer(layer_name).read_key(key)

    def write_layer(self, layer_name: str, key: str, value: object) -> None:
        """Write a key/value pair into a layer's data store."""
        if layer_name not in self._layers:
            raise KeyError(f"Layer {layer_name!r} not declared in Condien {self.name!r}")
        self._layers[layer_name].data[key] = value

    # ------------------------------------------------------------------
    # Continuity / Rebase
    # ------------------------------------------------------------------

    def carry(self, key: str, value: object) -> None:
        """
        Store a value in the carry-forward store.

        Only valid when continuity mode supports carrying:
          - "carry-forward"
          - "bounded-carry"
          - "trace-linked"
        """
        if self.continuity == "none":
            raise RuntimeError(
                f"Condien {self.name!r} continuity=none — carry-forward not allowed"
            )
        self._carry[key] = value

    def recall(self, key: str, default: object = None) -> object:
        """Retrieve a value from the carry-forward store."""
        return self._carry.get(key, default)

    def carry_forward_from(self, source: "Condien") -> None:
        """Keep a bounded reference to the previous Condien context."""

        if not isinstance(source, Condien):
            raise TypeError("source must be a Condien")
        if self.continuity == "none":
            raise RuntimeError(
                f"Condien {self.name!r} continuity=none — carry-forward not allowed"
            )
        self.previous = source
        self.history.append(source.name)
        self._carry.update(source._carry)

    def rebase_from(self, source: "Condien") -> None:
        """
        Import carry-forward values from another Condien (rebase).

        Constraints:
          - self.rebase must not be "disabled"
          - For "bounded" rebase: only keys already in self._carry are updated
          - For "enabled" rebase: all source carry keys are imported
        """
        if self.rebase == "disabled":
            raise RuntimeError(
                f"Condien {self.name!r} rebase=disabled — rebase not allowed"
            )
        if self.rebase == "bounded":
            # Bounded: only update keys already established in this Condien.
            for k in list(self._carry.keys()):
                if k in source._carry:
                    self._carry[k] = source._carry[k]
        else:
            # enabled: import all.
            self._carry.update(source._carry)

    def rebase_layer(self, layer_name: str, data: Dict[str, object]) -> None:
        """Replace one layer payload in bounded form."""

        if self.rebase == "disabled":
            raise RuntimeError(
                f"Condien {self.name!r} rebase=disabled — layer rebase not allowed"
            )
        if layer_name not in self._layers:
            raise KeyError(layer_name)
        self._layers[layer_name].data = dict(data)

    # ------------------------------------------------------------------
    # Representation / inspection
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a structured dict representation of this Condien."""
        return {
            "CONDIEN": self.name,
            "ROLE": self.role,
            "MEANING_MODE": self.meaning_mode,
            "CONTEXT_MODE": self.context_mode,
            "LAYERS": list(self._layers.keys()),
            "READ": (
                sorted(self._read_set) if self._read_set is not None else "all"
            ),
            "DENY": sorted(self._deny_set),
            "ACTIVE_LAYER": self._active_layer,
            "CONTINUITY": self.continuity,
            "REBASE": self.rebase,
            "BOUNDARY": self.boundary,
            "ENV": self.env,
            "MODEW": self.modew,
            "PAPER": self.paper,
        }

    def to_w3lgu(self) -> str:
        """
        Serialize to W3Lgu-Condien profile canonical representation.

        Format: KEY:VALUE per line, aligned with the Condien Canonical Syntax.
        This is the representation layer — it does not replace the Condien object.
        """
        lines = [
            f"CONDIEN:{self.name}",
            f"ROLE:{self.role}",
            f"MEANING_MODE:{self.meaning_mode}",
            f"CONTEXT_MODE:{self.context_mode}",
        ]
        if self._layers:
            lines.append(f"LAYERS:{','.join(self._layers.keys())}")
        if self._read_set is not None:
            lines.append(f"READ:{','.join(sorted(self._read_set))}")
        if self._deny_set:
            lines.append(f"DENY:{','.join(sorted(self._deny_set))}")
        if self._active_layer:
            lines.append(f"LAYER:{self._active_layer}")
        lines += [
            f"CONTINUITY:{self.continuity}",
            f"REBASE:{self.rebase}",
            f"BOUNDARY:{self.boundary}",
            f"ENV:{self.env}",
        ]
        if self.modew:
            lines.append(f"MODEW:{self.modew}")
        if self.paper:
            lines.append(f"PAPER:{self.paper}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"Condien(name={self.name!r}, role={self.role!r}, "
            f"layers={list(self._layers.keys())}, "
            f"continuity={self.continuity!r}, rebase={self.rebase!r})"
        )
