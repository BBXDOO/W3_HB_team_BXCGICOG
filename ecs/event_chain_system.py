from enum import Enum
from typing import List, Dict, Any, Optional

# --- Core Enums ---
class Confidence(Enum):
    UNCLEAR = 0
    AMBIGUOUS = 0.5
    CLEAR = 1

class CrossState(Enum):
    STANDBY = "STANDBY"
    ACTIVE = "ACTIVE"
    REVIEW = "REVIEW"

class EventResult(Enum):
    FINAL = "FINAL"
    NEXT = "NEXT"
    REVIEW = "REVIEW"
    STANDBY = "STANDBY"
    STOP = "STOP"
    WAIT = "WAIT"
    RECOVERY = "RECOVERY"
    ERROR = "ERROR"

# --- Event Frame ---
class EventFrame:
    def __init__(self,
                 event_id: str,
                 source: str,
                 type_data: str,
                 intent: str,
                 logic_chain: str,
                 rooms: List[str],
                 active_systems: List[str],
                 standby_systems: List[str],
                 cross_state: CrossState,
                 confidence: Confidence,
                 result: Optional[str] = None,
                 next_event: Optional[str] = None,
                 mutated: bool = False):
        self.event_id = event_id
        self.source = source
        self.type_data = type_data
        self.intent = intent
        self.logic_chain = logic_chain
        self.rooms = rooms
        self.active_systems = active_systems
        self.standby_systems = standby_systems
        self.cross_state = cross_state
        self.confidence = confidence
        self.result = result
        self.next_event = next_event
        self.mutated = mutated

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "source": self.source,
            "type_data": self.type_data,
            "intent": self.intent,
            "logic_chain": self.logic_chain,
            "rooms": self.rooms,
            "active_systems": self.active_systems,
            "standby_systems": self.standby_systems,
            "cross_state": self.cross_state.value,
            "confidence": self.confidence.value,
            "result": self.result,
            "next": self.next_event,
            "mutated": self.mutated
        }

# --- Event Chain System ---
class EventChainSystem:
    def __init__(self):
        self.chain: List[EventFrame] = []

    def add_event(self, event: EventFrame):
        self.chain.append(event)

    def process_event(self, event: EventFrame) -> EventFrame:
        # Confidence handling
        if event.confidence == Confidence.CLEAR:
            event.result = "CONTINUE"
            event.next_event = f"{event.event_id}_NEXT"
        elif event.confidence == Confidence.AMBIGUOUS:
            event.result = "UNCLEAR"
            event.next_event = "REVIEW_OR_OBSERVE"
            event.cross_state = CrossState.REVIEW
        elif event.confidence == Confidence.UNCLEAR:
            event.result = "STOP"
            event.next_event = "WAIT"
            event.cross_state = CrossState.STANDBY
        return event

    def run_chain(self):
        for event in self.chain:
            processed = self.process_event(event)
            print(f"[E-CS] Processed Event: {processed.to_dict()}")

# --- Example Usage ---
if __name__ == "__main__":
    ecs = EventChainSystem()

    # Example: Termux git pull
    event1 = EventFrame(
        event_id="Event-1",
        source="LOCAL, GLOBAL",
        type_data="source_control",
        intent="sync_repo",
        logic_chain="sync_check",
        rooms=["Ev", "Si", "Cu", "Re"],
        active_systems=["W3Lgu", "REDR", "PSP2", "PX", "Git", "LRC2"],
        standby_systems=["File.void", "Cross-L", "Codex"],
        cross_state=CrossState.ACTIVE,
        confidence=Confidence.CLEAR
    )

    ecs.add_event(event1)
    ecs.run_chain()
