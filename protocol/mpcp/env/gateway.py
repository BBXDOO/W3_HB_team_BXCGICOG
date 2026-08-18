"""High-level Cross-L / ENV / MPCP gateway."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from ..runtime.executor import run_packet
from .boundary import CrossLEnvironmentBoundary
from .models import ExecutionAgreement, MPCPWorkUnit


class MPCPEnvironmentGateway:
    """Prepare and execute bounded work without granting Cross-L authority."""

    def __init__(self, boundary: CrossLEnvironmentBoundary | None = None) -> None:
        self.boundary = boundary or CrossLEnvironmentBoundary()

    def prepare(self, envelope: Mapping[str, Any], **inputs: Any) -> MPCPWorkUnit:
        return self.boundary.ingress(envelope, **inputs)

    def execute(
        self,
        work: MPCPWorkUnit,
        *,
        agreement: ExecutionAgreement | None,
        executor: Callable[[Mapping[str, Any]], Mapping[str, Any]] = run_packet,
    ) -> dict:
        """Run only after an explicit authority decision outside Cross-L."""

        if agreement is None or not agreement.permits(work):
            return self.boundary.egress(
                work,
                {
                    "state": "WAIT",
                    "reason": "execution_agreement_required",
                    "trace": ["CROSS_L", "ENV", "MPCP_WAIT"],
                    "mutated": False,
                    "review": True,
                },
            )
        packet = work.to_mpcp_packet()
        packet["EXECUTION_AGREEMENT"] = agreement.to_dict()
        result = executor(packet)
        return self.boundary.egress(work, result)
