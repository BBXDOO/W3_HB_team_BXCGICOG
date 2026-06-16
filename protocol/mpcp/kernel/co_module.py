# mpcp/kernel/co_module.py

from __future__ import annotations

from typing import Any


REQUIRED_CO_MODULE_KEYS = frozenset({
    "RESPONSIBLE_MODULE",
    "ASSIST_MODULES",
    "CROSS_FIELD",
    "REASON",
    "RETURN_TO",
    "EVENT_ID",
    "END_EVENT",
})

OPTIONAL_CO_MODULE_KEYS = frozenset({
    "ROT_TYPE",
    "PAPER_PACK_ID",
    "FIELD_SELECTED",
    "TEMP_AGREEMENT",
    "CAN_CHANGE_DIRECTION",
    "CAN_EXPAND",
    "PAPERS",
    "TRACE",
    "ENV_REF",
    "STACK_REF",
    "LRC_REF",
    "META",
})

ALLOWED_CO_MODULE_KEYS = REQUIRED_CO_MODULE_KEYS | OPTIONAL_CO_MODULE_KEYS


class CoModuleLaw:
    """
    Cooperative Module Law

    A = responsible module
    B = assisting module(s)
    C = cross field / agreement point

    This validator does not execute work.
    It only checks whether a cooperative relation is traceable.
    """

    @staticmethod
    def _require_dict(value: Any, name: str) -> dict:
        if not isinstance(value, dict):
            raise ValueError(f"CO_MODULE_FAIL: {name}_MUST_BE_DICT")
        return value

    @staticmethod
    def _require_non_empty_string(data: dict, key: str):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"CO_MODULE_FAIL: {key}_MUST_BE_NON_EMPTY_STRING")
        return value.strip()

    @staticmethod
    def validate_contract(contract: dict, *, allow_extra: bool = False):
        """
        Validate cooperative module relation.

        Required:
        - RESPONSIBLE_MODULE
        - ASSIST_MODULES
        - CROSS_FIELD
        - REASON
        - RETURN_TO
        - EVENT_ID
        - END_EVENT
        """
        contract = CoModuleLaw._require_dict(contract, "CONTRACT")

        missing = sorted(REQUIRED_CO_MODULE_KEYS - set(contract.keys()))
        if missing:
            raise ValueError(f"CO_MODULE_FAIL: MISSING_REQUIRED:{','.join(missing)}")

        if not allow_extra:
            unknown = sorted(str(key) for key in contract.keys() if key not in ALLOWED_CO_MODULE_KEYS)
            if unknown:
                raise ValueError(f"CO_MODULE_FAIL: UNKNOWN_KEYS:{','.join(unknown)}")

        for key in ("RESPONSIBLE_MODULE", "CROSS_FIELD", "REASON", "RETURN_TO", "EVENT_ID"):
            CoModuleLaw._require_non_empty_string(contract, key)

        assists = contract.get("ASSIST_MODULES")
        if not isinstance(assists, list) or not assists:
            raise ValueError("CO_MODULE_FAIL: ASSIST_MODULES_MUST_BE_NON_EMPTY_LIST")
        for idx, module in enumerate(assists):
            if not isinstance(module, str) or not module.strip():
                raise ValueError(f"CO_MODULE_FAIL: ASSIST_MODULES[{idx}]_MUST_BE_NON_EMPTY_STRING")

        if contract["RESPONSIBLE_MODULE"] in assists:
            raise ValueError("CO_MODULE_FAIL: RESPONSIBLE_MODULE_MUST_NOT_BE_LISTED_AS_ASSIST")

        if contract["RETURN_TO"] != contract["RESPONSIBLE_MODULE"]:
            raise ValueError("CO_MODULE_FAIL: RETURN_TO_MUST_MATCH_RESPONSIBLE_MODULE")

        if "PAPERS" in contract:
            papers = contract["PAPERS"]
            if not isinstance(papers, list) or not papers:
                raise ValueError("CO_MODULE_FAIL: PAPERS_MUST_BE_NON_EMPTY_LIST")

        if "TRACE" in contract and not isinstance(contract["TRACE"], list):
            raise ValueError("CO_MODULE_FAIL: TRACE_MUST_BE_LIST")

        for key in ("CAN_CHANGE_DIRECTION", "CAN_EXPAND"):
            if key in contract and not isinstance(contract[key], bool):
                raise ValueError(f"CO_MODULE_FAIL: {key}_MUST_BE_BOOL")

        return True

    @staticmethod
    def validate_event_end(contract: dict, expected_end: Any = 1):
        """
        Validate the end marker.

        In the first documented flow, End Event is 1.
        A01 is the event identity, not the end marker.
        """
        contract = CoModuleLaw._require_dict(contract, "CONTRACT")
        if contract.get("END_EVENT") != expected_end:
            raise ValueError(f"CO_MODULE_FAIL: END_EVENT_MUST_BE_{expected_end}")
        return True
