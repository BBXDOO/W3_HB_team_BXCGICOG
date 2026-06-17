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
    "TRIGGER",
    "EXPECTED_GAIN",
    "RISK_FLAGS",
    "DISTRIBUTION_MODE",
    "MAX_ASSIST_ROUTES",
    "REJOIN_STRATEGY",
    "QUALITY_CHECK",
    "PAPERS",
    "TRACE",
    "ENV_REF",
    "STACK_REF",
    "LRC_REF",
    "TRACE_ID",
    "TIMESTAMP",
    "META",
})

ALLOWED_CO_MODULE_KEYS = REQUIRED_CO_MODULE_KEYS | OPTIONAL_CO_MODULE_KEYS

VALID_TRIGGERS = frozenset({
    "uncertain",
    "abnormal",
    "malformed",
    "incomplete",
    "not_enough_confidence",
    "needs_more_variables",
    "other_path_faster",
    "other_path_more_precise",
    "risk_distribution_needed",
    "parallel_check_needed",
})


class CoModuleLaw:
    """
    Cooperative Module Law

    A = responsible module
    B = assisting module(s)
    C = flexible cross / assist field, not command center

    This validator does not execute work.
    It only checks whether a cooperative relation is traceable and necessary.
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

        This law is for necessary assist/cross work, not every task.
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

        if "TRACE" in contract and not isinstance(contract["TRACE"], (dict, list)):
            raise ValueError("CO_MODULE_FAIL: TRACE_MUST_BE_DICT_OR_LIST")

        for key in ("CAN_CHANGE_DIRECTION", "CAN_EXPAND"):
            if key in contract and not isinstance(contract[key], bool):
                raise ValueError(f"CO_MODULE_FAIL: {key}_MUST_BE_BOOL")

        if "MAX_ASSIST_ROUTES" in contract:
            routes = contract["MAX_ASSIST_ROUTES"]
            if not isinstance(routes, int) or routes < 1:
                raise ValueError("CO_MODULE_FAIL: MAX_ASSIST_ROUTES_MUST_BE_POSITIVE_INT")
            if routes < len(assists):
                raise ValueError("CO_MODULE_FAIL: MAX_ASSIST_ROUTES_LESS_THAN_ASSIST_MODULES")

        if "RISK_FLAGS" in contract:
            flags = contract["RISK_FLAGS"]
            if not isinstance(flags, list):
                raise ValueError("CO_MODULE_FAIL: RISK_FLAGS_MUST_BE_LIST")

        CoModuleLaw.validate_need_for_assist(contract)
        return True

    @staticmethod
    def validate_need_for_assist(contract: dict):
        """
        Validate why assist is used.

        Assist should be used only when it gives enough value:
        uncertainty, abnormality, incomplete input, faster route, stronger route,
        extra variables, parallel check, or risk distribution.
        """
        contract = CoModuleLaw._require_dict(contract, "CONTRACT")

        trigger = contract.get("TRIGGER")
        expected_gain = contract.get("EXPECTED_GAIN")

        if trigger is None and expected_gain is None:
            raise ValueError("CO_MODULE_FAIL: ASSIST_REQUIRES_TRIGGER_OR_EXPECTED_GAIN")

        if trigger is not None:
            if isinstance(trigger, str):
                if not trigger.strip():
                    raise ValueError("CO_MODULE_FAIL: TRIGGER_MUST_BE_NON_EMPTY")
            elif isinstance(trigger, list):
                if not trigger:
                    raise ValueError("CO_MODULE_FAIL: TRIGGER_LIST_MUST_BE_NON_EMPTY")
                for idx, item in enumerate(trigger):
                    if not isinstance(item, str) or not item.strip():
                        raise ValueError(f"CO_MODULE_FAIL: TRIGGER[{idx}]_MUST_BE_NON_EMPTY_STRING")
            else:
                raise ValueError("CO_MODULE_FAIL: TRIGGER_MUST_BE_STRING_OR_LIST")

        if expected_gain is not None:
            if isinstance(expected_gain, str):
                if not expected_gain.strip():
                    raise ValueError("CO_MODULE_FAIL: EXPECTED_GAIN_MUST_BE_NON_EMPTY")
            elif isinstance(expected_gain, list):
                if not expected_gain:
                    raise ValueError("CO_MODULE_FAIL: EXPECTED_GAIN_LIST_MUST_BE_NON_EMPTY")
                for idx, item in enumerate(expected_gain):
                    if not isinstance(item, str) or not item.strip():
                        raise ValueError(f"CO_MODULE_FAIL: EXPECTED_GAIN[{idx}]_MUST_BE_NON_EMPTY_STRING")
            else:
                raise ValueError("CO_MODULE_FAIL: EXPECTED_GAIN_MUST_BE_STRING_OR_LIST")

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
