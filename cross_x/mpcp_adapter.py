"""Governed Cross -> MPCP execution adapter.

Cross remains the planner/coordinator.  MPCP remains the execution structure.
This adapter validates the handoff and explicit approval, invokes exactly one
MPCP Modew task, and binds its return value into a new immutable E-CS chain.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from cross_x.event_chain import (
    EventChain,
    bind_event_return,
    freeze_ecs_mapping,
    normalize_ecs_identifier,
    thaw_ecs_mapping,
)

CROSS_MPCP_ADAPTER_VERSION = "1.0"
EXECUTION_CAPABILITY = "cross.mpcp.execute"
MPCPExecutor = Callable[[str], Mapping[str, Any]]
_SUCCESS_STATES = frozenset({"SUCCESS", "done", "ready"})
_WAIT_STATES = frozenset({"WAIT", "wait", "warn", "run", "idle"})
_STOP_STATES = frozenset({"STOP", "fail", "block"})


def _safe_mpcp_value(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"Cross-MPCP {field} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"Cross-MPCP {field} must be non-empty")
    if any(delimiter in normalized for delimiter in (",", ":", "\n", "\r")):
        raise ValueError(f"Cross-MPCP {field} contains an MPCP delimiter")
    return normalized


@dataclass(frozen=True)
class MPCPExecutionApproval:
    """Human/governance approval scoped to exactly one chain event and task."""

    chain_id: str
    event_id: str
    task: str
    approved_by: str
    capabilities: tuple[str, ...] = (EXECUTION_CAPABILITY,)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "chain_id",
            normalize_ecs_identifier(self.chain_id, field="approval.chain_id"),
        )
        object.__setattr__(
            self,
            "event_id",
            normalize_ecs_identifier(self.event_id, field="approval.event_id"),
        )
        object.__setattr__(
            self,
            "task",
            normalize_ecs_identifier(self.task, field="approval.task"),
        )
        object.__setattr__(
            self,
            "approved_by",
            normalize_ecs_identifier(self.approved_by, field="approval.approved_by"),
        )
        capabilities = tuple(
            normalize_ecs_identifier(value, field="approval.capability")
            for value in self.capabilities
        )
        if len(set(capabilities)) != len(capabilities):
            raise ValueError("Cross-MPCP approval capabilities must be unique")
        object.__setattr__(self, "capabilities", capabilities)


@dataclass(frozen=True)
class CrossMPCPResult:
    """One governed Modew result and the new E-CS chain containing it."""

    chain: EventChain
    event_id: str
    task: str
    state: str
    return_value: Mapping[str, Any]
    executed: bool

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "return_value",
            freeze_ecs_mapping(self.return_value),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_version": CROSS_MPCP_ADAPTER_VERSION,
            "event_id": self.event_id,
            "task": self.task,
            "state": self.state,
            "executed": self.executed,
            "return_value": thaw_ecs_mapping(self.return_value),
            "event_chain": self.chain.to_dict(),
        }


def build_cross_mpcp_handoff(
    cross_envelope: Mapping[str, Any],
    *,
    task: str,
    context: Mapping[str, Any] | None = None,
    review_approved: bool = False,
) -> dict[str, Any]:
    """Normalize a Cross-Code envelope into the canonical MPCP handoff."""

    if not isinstance(cross_envelope, Mapping):
        raise ValueError("Cross-MPCP cross_envelope must be a mapping")
    if cross_envelope.get("kind") != "cross-code-dispatch":
        raise ValueError("Cross-MPCP requires a cross-code-dispatch envelope")
    if cross_envelope.get("state") in {"inactive", "review"}:
        raise ValueError("Cross-MPCP envelope is not ready for execution")
    if cross_envelope.get("execution_allowed") is not False:
        raise ValueError("Cross-MPCP source envelope must remain planner-only")
    return {
        "contract_version": CROSS_MPCP_ADAPTER_VERSION,
        "kind": "cross-mpcp-handoff",
        "chain_id": normalize_ecs_identifier(
            cross_envelope.get("chain_id"),
            field="handoff.chain_id",
        ),
        "event_id": normalize_ecs_identifier(
            cross_envelope.get("event_id"),
            field="handoff.event_id",
        ),
        "task": normalize_ecs_identifier(task, field="handoff.task"),
        "context": dict(context or {}),
        "review_approved": bool(review_approved),
        "execution_allowed": False,
        "mutated": False,
    }


def execute_cross_handoff(
    chain: EventChain,
    handoff: Mapping[str, Any],
    approval: MPCPExecutionApproval,
    *,
    executor: MPCPExecutor | None = None,
) -> CrossMPCPResult:
    """Execute one approved Cross handoff and immutably bind the MPCP return.

    ``executor`` defaults to the repository MPCP runtime.  Dependency injection
    remains available for tests and alternate MPCP-compatible runtimes.
    """

    if not isinstance(chain, EventChain):
        raise TypeError("chain must be an EventChain")
    if not isinstance(handoff, Mapping):
        raise ValueError("Cross-MPCP handoff must be a mapping")

    chain_id = normalize_ecs_identifier(
        handoff.get("chain_id"),
        field="handoff.chain_id",
    )
    event_id = normalize_ecs_identifier(
        handoff.get("event_id"),
        field="handoff.event_id",
    )
    task = normalize_ecs_identifier(
        handoff.get("task"),
        field="handoff.task",
    )
    if chain.chain_id != chain_id:
        raise ValueError("Cross-MPCP handoff chain_id does not match EventChain")
    if (approval.chain_id, approval.event_id, approval.task) != (
        chain_id,
        event_id,
        task,
    ):
        raise PermissionError("Cross-MPCP approval scope does not match handoff")
    if EXECUTION_CAPABILITY not in approval.capabilities:
        raise PermissionError(
            f"Cross-MPCP approval requires capability {EXECUTION_CAPABILITY}"
        )

    event = next((item for item in chain.events if item.event_id == event_id), None)
    if event is None:
        raise ValueError(f"Cross-MPCP event_id not found in chain: {event_id}")
    if event.status != "planned" or event.return_value is not None:
        raise ValueError("Cross-MPCP event is not available for execution")
    if handoff.get("review_approved") is not True:
        raise PermissionError("Cross-MPCP handoff must complete human review")
    if handoff.get("execution_allowed") is True:
        raise ValueError(
            "Cross planner must not self-grant execution; approval grants authority"
        )

    context = handoff.get("context", {})
    if not isinstance(context, Mapping):
        raise ValueError("Cross-MPCP handoff context must be a mapping")
    fields = {"TASK": task}
    for raw_key, raw_value in context.items():
        key = normalize_ecs_identifier(raw_key, field="handoff.context_key").upper()
        if key == "TASK":
            raise ValueError("Cross-MPCP context must not override TASK")
        fields[key] = _safe_mpcp_value(raw_value, field=f"handoff.context.{key}")
    mpcp_text = ",".join(f"{key}:{value}" for key, value in fields.items())

    active_executor = executor or _default_mpcp_executor()
    try:
        raw_result = active_executor(mpcp_text)
    except Exception as exc:
        raw_result = {
            "state": "STOP",
            "cause": task,
            "error": f"MPCP_EXECUTOR_ERROR:{type(exc).__name__}:{exc}",
        }
    if not isinstance(raw_result, Mapping):
        raw_result = {
            "state": "STOP",
            "cause": task,
            "error": "MPCP_EXECUTOR_RETURNED_NON_MAPPING",
        }
    result = dict(raw_result)
    state = str(result.get("state", "STOP"))
    event_status = _event_status_for_mpcp_state(state)
    if event_status == "stopped" and not result.get("error"):
        result["error"] = "MPCP_STOP_WITHOUT_ERROR"
    return_value = {
        "adapter_version": CROSS_MPCP_ADAPTER_VERSION,
        "handled": True,
        "executed": True,
        "task": task,
        "approved_by": approval.approved_by,
        "state": state,
        "mpcp": result,
    }
    updated_chain = bind_event_return(
        chain,
        event_id=event_id,
        return_value=return_value,
        status=event_status,
        execute_allowed=True,
        mutated=bool(result.get("mutated", False)),
    )
    return CrossMPCPResult(
        chain=updated_chain,
        event_id=event_id,
        task=task,
        state=state,
        return_value=return_value,
        executed=True,
    )


def _event_status_for_mpcp_state(state: str) -> str:
    if state in _SUCCESS_STATES:
        return "completed"
    if state in _WAIT_STATES:
        return "waiting"
    if state in _STOP_STATES:
        return "stopped"
    return "stopped"


def _default_mpcp_executor() -> MPCPExecutor:
    from protocol.mpcp.runtime.executor import run

    return run
