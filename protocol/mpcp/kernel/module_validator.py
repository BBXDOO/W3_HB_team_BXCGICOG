# mpcp/kernel/module_validator.py

from __future__ import annotations

from typing import Any, Optional

from protocol.mpcp.kernel.co_module import CoModuleLaw
from protocol.mpcp.kernel.module_registry import DEFAULT_REGISTRY, ModuleRegistry


class ModuleValidator:
    """Validate cooperative module boundary against registry.

    This validator does not execute, route, or decide authority.
    It checks whether the requested return/assist relation is allowed and traceable.
    """

    @staticmethod
    def _get(contract: Any, upper_key: str, lower_key: str, default: Any = None) -> Any:
        if isinstance(contract, dict):
            if upper_key in contract:
                return contract[upper_key]
            return contract.get(lower_key, default)
        return getattr(contract, lower_key, default)

    @staticmethod
    def validate_return(contract: Any, *, registry: Optional[ModuleRegistry] = None) -> bool:
        active = registry or DEFAULT_REGISTRY
        source = ModuleValidator._get(contract, "RESPONSIBLE_MODULE", "responsible_module")
        target = ModuleValidator._get(contract, "RETURN_TO", "return_to")

        if not isinstance(source, str) or not source.strip():
            raise ValueError("MODULE_VALIDATOR_FAIL: RESPONSIBLE_MODULE_REQUIRED")
        if not isinstance(target, str) or not target.strip():
            raise ValueError("MODULE_VALIDATOR_FAIL: RETURN_TO_REQUIRED")

        # Return-to-self is allowed because it means the trace returns to the responsible module.
        if source == target:
            return True

        if not active.can_return_to(source, target):
            raise ValueError("MODULE_VALIDATOR_FAIL: RETURN_TO_NOT_ALLOWED_BY_REGISTRY")

        return True

    @staticmethod
    def validate_assist(contract: Any, *, registry: Optional[ModuleRegistry] = None) -> bool:
        active = registry or DEFAULT_REGISTRY
        responsible = ModuleValidator._get(contract, "RESPONSIBLE_MODULE", "responsible_module")
        assists = ModuleValidator._get(contract, "ASSIST_MODULES", "assist_modules", [])

        if not isinstance(responsible, str) or not responsible.strip():
            raise ValueError("MODULE_VALIDATOR_FAIL: RESPONSIBLE_MODULE_REQUIRED")
        if not isinstance(assists, list) or not assists:
            raise ValueError("MODULE_VALIDATOR_FAIL: ASSIST_MODULES_REQUIRED")

        for idx, module in enumerate(assists):
            if not isinstance(module, str) or not module.strip():
                raise ValueError(f"MODULE_VALIDATOR_FAIL: ASSIST_MODULES[{idx}]_INVALID")
            if not active.can_assist(responsible, module):
                raise ValueError(f"MODULE_VALIDATOR_FAIL: ASSIST_NOT_ALLOWED_BY_REGISTRY:{responsible}->{module}")

        return True

    @staticmethod
    def validate_contract(contract: Any, *, registry: Optional[ModuleRegistry] = None) -> bool:
        data = contract.to_dict() if hasattr(contract, "to_dict") else contract
        if isinstance(data, dict):
            CoModuleLaw.validate_contract(data)
        ModuleValidator.validate_return(data, registry=registry)
        ModuleValidator.validate_assist(data, registry=registry)
        return True
