"""Pillar structure for MPCP.

A–F have a construction order while a Pillar is being formed. The order gives
each layer a place, not superior authority. After activation, runtime work may
address the relevant semantic layer directly and operations remain separate.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Callable, Iterable


class Pillar:
    VALID_STATES = frozenset({"SUCCESS", "WAIT", "STOP"})
    LAYER_NAMES = ("A", "B", "C", "D", "E", "F")

    def __init__(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("PILLAR_NAME_REQUIRED")
        self.name = name.strip()
        self.layers: dict[str, Any] = {name: None for name in self.LAYER_NAMES}
        self.phase = "construction"
        self.construction_order = self.LAYER_NAMES
        self.construction_trace: list[str] = []
        self.context: dict[str, Any] = {}
        self.operations: OrderedDict[str, Callable[[Any, dict], dict]] = OrderedDict()
        self.output: dict | None = None
        self.trace: list[dict] = []

    @property
    def stages(self) -> dict[str, Any]:
        """Compatibility view. A–F remain semantic layers, not runtime stages."""
        return self.layers

    @classmethod
    def build(cls, name: str, layer_values: dict[str, Any]) -> "Pillar":
        """Construct A–F in architectural order and activate the Pillar."""
        pillar = cls(name)
        missing = [layer for layer in cls.LAYER_NAMES if layer not in layer_values]
        if missing:
            raise ValueError(f"PILLAR_CONSTRUCTION_MISSING:{','.join(missing)}")
        for layer in cls.LAYER_NAMES:
            pillar.construct_layer(layer, layer_values[layer])
        return pillar.activate()

    def construct_layer(self, layer: str, value: Any) -> None:
        """Place one layer during construction; every layer follows the same law."""
        key = str(layer).upper()
        if key not in self.layers:
            raise ValueError(f"PILLAR_LAYER_INVALID:{layer}")
        if self.phase != "construction":
            raise RuntimeError("PILLAR_CONSTRUCTION_ALREADY_COMPLETE")
        if len(self.construction_trace) >= len(self.construction_order):
            raise RuntimeError("PILLAR_CONSTRUCTION_READY_FOR_ACTIVATION")
        expected = self.construction_order[len(self.construction_trace)]
        if key != expected:
            raise ValueError(f"PILLAR_CONSTRUCTION_EXPECTED:{expected}:GOT:{key}")
        self.layers[key] = value
        self.construction_trace.append(key)

    def activate(self) -> "Pillar":
        if tuple(self.construction_trace) != self.construction_order:
            remaining = self.construction_order[len(self.construction_trace):]
            raise RuntimeError(f"PILLAR_CONSTRUCTION_INCOMPLETE:{','.join(remaining)}")
        self.phase = "operational"
        return self

    def set_layer(self, layer: str, value: Any) -> None:
        """Adapt one related semantic layer after the structure is operational."""
        key = str(layer).upper()
        if key not in self.layers:
            raise ValueError(f"PILLAR_LAYER_INVALID:{layer}")
        if self.phase != "operational":
            raise RuntimeError("PILLAR_NOT_OPERATIONAL:USE_CONSTRUCT_LAYER")
        self.layers[key] = value

    def get_layer(self, layer: str, default: Any = None) -> Any:
        key = str(layer).upper()
        if key not in self.layers:
            raise ValueError(f"PILLAR_LAYER_INVALID:{layer}")
        value = self.layers[key]
        return default if value is None else value

    def set_stage(self, stage: str, fn: Callable[[Any, dict], dict]) -> None:
        """Register an old stage callback as an explicitly named operation."""
        key = str(stage).upper()
        if key not in self.layers:
            raise ValueError(f"PILLAR_LAYER_INVALID:{stage}")
        self.register_operation(f"layer_{key}", fn)

    def register_operation(self, name: str, fn: Callable[[Any, dict], dict]) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("PILLAR_OPERATION_NAME_REQUIRED")
        if not callable(fn):
            raise TypeError(f"PILLAR_OPERATION_NOT_CALLABLE:{name}")
        self.operations[name.strip()] = fn

    def set_context(self, key: str, value: Any) -> None:
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        return self.context.get(key, default)

    def semantic_snapshot(self) -> dict:
        return {
            "pillar": self.name,
            "phase": self.phase,
            "construction_order": list(self.construction_order),
            "construction_trace": list(self.construction_trace),
            "layers": dict(self.layers),
        }

    def run(self, operation_order: Iterable[str] | None = None) -> dict:
        if self.phase != "operational":
            return self._stop("STRUCTURE", "pillar construction is incomplete")
        order = list(operation_order) if operation_order is not None else list(self.operations)
        if not order:
            return self._stop("NO_OPERATION", "pillar has no registered operation")
        result: Any = None
        for operation_name in order:
            fn = self.operations.get(operation_name)
            if fn is None:
                return self._stop(operation_name, "operation is not registered")
            try:
                result = fn(result, self.context)
            except Exception as exc:
                return self._stop(operation_name, str(exc))
            if not isinstance(result, dict):
                return self._stop(operation_name, "invalid result type")
            state = result.get("state")
            if state not in self.VALID_STATES:
                return self._stop(operation_name, f"invalid state: {state}")
            self.trace.append({"operation": operation_name, "state": state})
            if state in {"STOP", "WAIT"}:
                self.output = result
                return result
        self.output = result
        return result

    def _stop(self, operation: str, reason: str) -> dict:
        result = {
            "state": "STOP",
            "operation": operation,
            "reason": reason,
            "error": reason,
            "semantic_layers": dict(self.layers),
            "pillar_phase": self.phase,
        }
        self.output = result
        return result
