import uuid
from typing import List, Dict, Any
from datetime import datetime

# --- Event Registry ---
class EventRegistry:
    def __init__(self):
        self.events: Dict[str, Dict[str, Any]] = {}

    def register_event(self, event: Dict[str, Any]) -> str:
        event_id = event.get("event_id", str(uuid.uuid4()))
        trace_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        record = {
            "event_id": event_id,
            "trace_id": trace_id,
            "timestamp": timestamp,
            "event": event,
            "status": "REGISTERED"
        }

        self.events[event_id] = record
        return event_id

    def update_event(self, event_id: str, result: str, state: str, confidence: float, next_event: str):
        if event_id in self.events:
            self.events[event_id]["event"]["result"] = result
            self.events[event_id]["event"]["state"] = state
            self.events[event_id]["event"]["confidence"] = confidence
            self.events[event_id]["event"]["next"] = next_event
            self.events[event_id]["status"] = "UPDATED"
            self.events[event_id]["event"]["trace"] = f"Updated at {datetime.utcnow().isoformat()}"

    def get_event(self, event_id: str) -> Dict[str, Any]:
        return self.events.get(event_id, {})

    def replay_chain(self) -> List[Dict[str, Any]]:
        return [self.events[eid] for eid in self.events]

# --- Example Usage ---
if __name__ == "__main__":
    registry = EventRegistry()

    # Register Event-1
    event1 = {
        "event_id": "Event-1",
        "source": "LOCAL, GLOBAL",
        "type_data": "source_control",
        "intent": "sync_repo",
        "logic_chain": "sync_check",
        "rooms": ["Ev", "Si", "Cu", "Re"],
        "active_systems": ["W3Lgu", "REDR", "PSP2", "PX", "Git", "LRC2"],
        "standby_systems": ["File.void", "Cross-L", "Codex"],
        "cross_state": "ACTIVE",
        "confidence": 1,
        "result": None,
        "next": None,
        "mutated": False
    }

    eid = registry.register_event(event1)

    # Update Event-1 with result
    registry.update_event(eid, result="UPDATED", state="ACTIVE", confidence=1, next_event="Event-2")

    # Replay chain
    for record in registry.replay_chain():
        print(record)
