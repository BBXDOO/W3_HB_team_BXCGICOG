"""W3Lgu signal mapping."""

from __future__ import annotations

from dataclasses import dataclass

from protocol.w3lgu.core import W3LguPacket, W3LguPair


@dataclass(frozen=True)
class W3LguSignal:
    state: str
    color: str
    symbol: str
    meaning: str

    def to_packet(self, *, confidence: float | None = None) -> W3LguPacket:
        pairs = [
            W3LguPair("EVENT", "signal"),
            W3LguPair("STATE", self.state),
            W3LguPair("COLOR", self.color),
            W3LguPair("SYM", self.symbol),
        ]
        if confidence is not None:
            pairs.append(W3LguPair("CONF", f"{confidence:.3f}".rstrip("0").rstrip(".")))
        return W3LguPacket(tuple(pairs))


SIGNALS: dict[str, W3LguSignal] = {
    "idle": W3LguSignal("idle", "gray", "·", "standing by"),
    "ready": W3LguSignal("ready", "blue", "◆", "prepared / external handoff possible"),
    "run": W3LguSignal("run", "blue", "⟳", "active execution"),
    "WAIT": W3LguSignal("WAIT", "yellow", "◌", "pending dependency"),
    "wait": W3LguSignal("wait", "yellow", "◌", "pending dependency"),
    "done": W3LguSignal("done", "green", "■", "completed"),
    "warn": W3LguSignal("warn", "yellow", "●", "caution / review"),
    "block": W3LguSignal("block", "orange", "■!", "blocked by rule or dependency"),
    "fail": W3LguSignal("fail", "red", "▲", "failed"),
    "STOP": W3LguSignal("STOP", "red", "⛔", "hard stop"),
    "SUCCESS": W3LguSignal("SUCCESS", "green", "✓", "confirmed success"),
}


def signal_for_state(state: str, *, confidence: float | None = None) -> W3LguPacket:
    signal = SIGNALS.get(state) or SIGNALS.get(state.lower()) or SIGNALS["warn"]
    if confidence == 0.5 and signal.state in {"SUCCESS", "done"}:
        signal = SIGNALS["warn"]
    return signal.to_packet(confidence=confidence)
