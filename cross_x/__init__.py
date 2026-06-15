"""Cross-X ecosystem coordination package."""

from cross_x.core import CrossXPlan, CrossXRequest, build_cross_x_plan
from cross_x.audit import audit_cross_systems
from cross_x.event_chain import (
    EventChain,
    EventChainRecord,
    bind_event_return,
    build_event_chain,
    freeze_ecs_mapping,
    normalize_ecs_identifier,
    thaw_ecs_mapping,
)
from cross_x.mpcp_adapter import (
    CROSS_MPCP_ADAPTER_VERSION,
    EXECUTION_CAPABILITY,
    CrossMPCPResult,
    MPCPExecutionApproval,
    build_cross_mpcp_handoff,
    execute_cross_handoff,
)

__all__ = [
    "CrossXPlan",
    "CrossXRequest",
    "EventChain",
    "EventChainRecord",
    "CrossMPCPResult",
    "MPCPExecutionApproval",
    "CROSS_MPCP_ADAPTER_VERSION",
    "EXECUTION_CAPABILITY",
    "bind_event_return",
    "build_cross_mpcp_handoff",
    "freeze_ecs_mapping",
    "build_cross_x_plan",
    "build_event_chain",
    "audit_cross_systems",
    "normalize_ecs_identifier",
    "thaw_ecs_mapping",
    "execute_cross_handoff",
]
