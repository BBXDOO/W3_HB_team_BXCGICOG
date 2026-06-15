from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Logic27Slot:
    """Local W3Lgu MFC logic slot.

    This is a reference registry entry. It is not a required slot model for
    other W3 systems.
    """

    slot_id: str
    layer: int
    coordinate: int
    name: str
    purpose: str
    default_status: str
    next_modules: tuple[str, ...]
    standby_modules: tuple[str, ...]
    proposal_only: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "slot_id": self.slot_id,
            "layer": self.layer,
            "coordinate": self.coordinate,
            "name": self.name,
            "purpose": self.purpose,
            "default_status": self.default_status,
            "next_modules": list(self.next_modules),
            "standby_modules": list(self.standby_modules),
            "proposal_only": self.proposal_only,
        }


_SLOT_DATA = [
    (1, 1, "input_clear", "clear input can enter REDR/PSP2 flow", "ACTIVE", ("REDR", "PSP2"), ("DTML", "LRC2")),
    (1, 2, "input_unclear", "unclear input waits for more context", "WAIT", ("REDR",), ("PSP2", "DTML", "LRC2")),
    (1, 3, "input_conflict", "conflicting input moves toward review", "REVIEW_REQUIRED", ("REDR", "DTML"), ("PSP2", "LRC2")),
    (1, 4, "input_route", "input contains route intent", "ACTIVE", ("REDR", "PSP2"), ("DTML", "LRC2")),
    (1, 5, "input_memory", "input contains memory or checkpoint intent", "ACTIVE", ("REDR", "LRC2"), ("PSP2", "DTML")),
    (1, 6, "input_signal", "input contains signal or transport intent", "ACTIVE", ("REDR", "DTML"), ("PSP2", "LRC2")),
    (1, 7, "input_external", "input comes from external gateway", "ACTIVE", ("REDR", "PSP2"), ("DTML", "LRC2")),
    (1, 8, "input_low_context", "input lacks enough context", "WAIT", ("REDR",), ("PSP2", "DTML", "LRC2")),
    (1, 9, "input_shadow", "input should be carried as shadow context", "WAIT", ("LRC2",), ("REDR", "PSP2", "DTML")),
    (2, 1, "route_decision", "select route from event-field weight", "ACTIVE", ("PSP2", "DTML"), ("REDR", "LRC2")),
    (2, 2, "route_wait", "route cannot be selected yet", "WAIT", ("PSP2",), ("REDR", "DTML", "LRC2")),
    (2, 3, "route_review", "route requires review trace", "REVIEW_REQUIRED", ("DTML", "LRC2"), ("REDR", "PSP2")),
    (2, 4, "logic_continue", "logic can continue with current field", "ACTIVE", ("PSP2", "DTML"), ("REDR", "LRC2")),
    (2, 5, "logic_memory", "logic should checkpoint current field", "ACTIVE", ("LRC2",), ("REDR", "PSP2", "DTML")),
    (2, 6, "logic_signal", "logic should preserve signal path", "ACTIVE", ("DTML", "LRC2"), ("REDR", "PSP2")),
    (2, 7, "borrow_candidate", "field may use another system field as context", "WAIT", ("Cross-X", "LRC2"), ("REDR", "PSP2", "DTML")),
    (2, 8, "borrow_field", "field is requesting borrowed context", "WAIT", ("Cross-X", "LRC2"), ("REDR", "PSP2", "DTML")),
    (2, 9, "logic_shadow", "logic should pass shadow context forward", "WAIT", ("LRC2",), ("REDR", "PSP2", "DTML")),
    (3, 1, "result_clear", "result is clear enough to checkpoint", "ACTIVE", ("LRC2",), ("REDR", "PSP2", "DTML")),
    (3, 2, "shadow_copy", "result stays visible as shadow context", "WAIT", ("LRC2",), ("REDR", "PSP2", "DTML")),
    (3, 3, "result_review", "result should be reviewed before becoming pattern", "REVIEW_REQUIRED", ("LRC2",), ("REDR", "PSP2", "DTML")),
    (3, 4, "result_route", "result proposes next route", "ACTIVE", ("PSP2", "LRC2"), ("REDR", "DTML")),
    (3, 5, "result_memory", "result is memory-ready", "ACTIVE", ("LRC2",), ("REDR", "PSP2", "DTML")),
    (3, 6, "result_signal", "result keeps signal trace visible", "ACTIVE", ("DTML", "LRC2"), ("REDR", "PSP2")),
    (3, 7, "result_learning", "result may become a learned pattern later", "WAIT", ("LRC2",), ("REDR", "PSP2", "DTML")),
    (3, 8, "result_borrowed", "result came from borrowed field context", "WAIT", ("LRC2",), ("REDR", "PSP2", "DTML")),
    (3, 9, "result_stop", "result should stop local MFC flow", "STOP", (), ("REDR", "PSP2", "DTML", "LRC2")),
]

LOGIC27_SLOTS: dict[str, Logic27Slot] = {
    f"L{layer}-C{coordinate}": Logic27Slot(
        slot_id=f"L{layer}-C{coordinate}",
        layer=layer,
        coordinate=coordinate,
        name=name,
        purpose=purpose,
        default_status=status,
        next_modules=tuple(next_modules),
        standby_modules=tuple(standby_modules),
    )
    for layer, coordinate, name, purpose, status, next_modules, standby_modules in _SLOT_DATA
}


def get_logic_slot(slot_id: str) -> Logic27Slot:
    try:
        return LOGIC27_SLOTS[slot_id]
    except KeyError as exc:
        raise ValueError(f"unknown logic27 slot: {slot_id}") from exc


def iter_logic_slots() -> Iterable[Logic27Slot]:
    return tuple(LOGIC27_SLOTS.values())
