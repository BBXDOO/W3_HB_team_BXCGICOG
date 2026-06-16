# mpcp/kernel/rot.py

from __future__ import annotations

from typing import Any


HALT_STATES = frozenset({"STOP", "fail", "block"})
VALID_STATE_ALIASES = {
    "SUCCESS", "STOP", "WAIT", "wait",
    "idle", "ready", "run", "done", "warn", "block", "fail",
}

# ROT รับข้อมูลที่ถูก normalize แล้วเท่านั้น
# ภาษา / synonym / shorthand conversion เป็นหน้าที่ชั้น W3Lgu / Paper normalizer / adapter
# ROT_TYPE เป็น marker เพื่อบอกว่ากติกาชุดไหนกำลังถูกใช้ ไม่ใช่ตัวตีความภาษา
PAPER_COMMAND_REQUIRED = frozenset({"TASK", "INTENT", "SCOPE", "BOUNDARY"})
PAPER_COMMAND_OPTIONAL = frozenset({
    "PAPER_ID",
    "PAPER_PACK_ID",
    "ROT_TYPE",
    "ROT_REF",
    "CATEGORY",
    "EVENT_ID",
    "EVENT_REF",
    "CONTENT",
    "TARGET",
    "TARGETS",
    "PX",
    "MODEW",
    "ROLE",
    "CONTEXT_REF",
    "ENV_REF",
    "STACK_REF",
    "KNOWLEDGE_BASE_REF",
    "ADAPTIVE_BASELINE",
    "TRAJECTORY_REF",
    "REDR_STATE",
    "PACKAGE_REF",
    "PSP2_STATE",
    "RETURN_CONTRACT",
    "REVIEW",
    "DENY",
    "META",
})
PAPER_COMMAND_ALLOWED = PAPER_COMMAND_REQUIRED | PAPER_COMMAND_OPTIONAL

RESULT_REQUIRED_STRICT = frozenset({"schema", "state", "cause", "action", "result", "law", "restore", "meta"})
MUTATION_FLAGS = ("source_truth_mutated", "env_mutated", "event_container_mutated")


class MPCPRot:
    """
    ROT = Rule / Relation / Runtime Order Trace

    หน้าที่หลัก:
    - ตรวจความสัมพันธ์ Cause -> Action -> Result
    - กัน event / paper command ที่ลอย ไม่มี boundary
    - กำหนด result envelope ขั้นต่ำให้ระบบอื่นใช้ตรงกัน
    - ไม่แปลภาษา ไม่ตีความ synonym และไม่ execute

    ROT ไม่ใช่ตัวเดียวของทั้งระบบใหญ่
    ROT เป็นตระกูลกติกาตาม type / context เช่น ROT:MPCP, ROT:Lgu, ROT:CR-L,X
    ไฟล์นี้คือแกนตรวจขั้นต่ำของ MPCP-side ROT เท่านั้น
    """

    # =========================
    # INTERNAL HELPERS
    # =========================
    @staticmethod
    def _require_dict(value: Any, name: str) -> dict:
        if not isinstance(value, dict):
            raise ValueError(f"ROT_FAIL: {name}_MUST_BE_DICT")
        return value

    @staticmethod
    def _require_non_empty_string(data: dict, key: str):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"ROT_FAIL: {key}_MUST_BE_NON_EMPTY_STRING")
        return value.strip()

    @staticmethod
    def _unknown_keys(data: dict, allowed: frozenset[str]) -> list[str]:
        return sorted(str(key) for key in data.keys() if str(key) not in allowed)

    # =========================
    # ROT TYPE LAW
    # =========================
    @staticmethod
    def validate_rot_type(marker: dict):
        """
        ตรวจ ROT_TYPE แบบ marker เท่านั้น

        ROT_TYPE ไม่ใช่ enum ปิด เพราะระบบยังปรับตัวได้
        เช่น ROT:MPCP, ROT:Lgu, ROT:CR-L,X สามารถเกิดตามบริบทระบบได้
        """
        marker = MPCPRot._require_dict(marker, "ROT_TYPE_MARKER")
        if "ROT_TYPE" in marker:
            MPCPRot._require_non_empty_string(marker, "ROT_TYPE")
        if "ROT_REF" in marker:
            MPCPRot._require_non_empty_string(marker, "ROT_REF")
        return True

    # =========================
    # ROT READER LAW
    # =========================
    @staticmethod
    def validate_reader_request(request: dict, *, allow_extra: bool = False):
        """
        ตรวจ request จากระบบที่เข้ามาอ่าน ROT

        ระบบที่อ่าน ROT ต้องระบุหมวดกติกา (CATEGORY) และอาจระบุ ROT_TYPE
        แล้วส่ง Paper หรือ Paper Pack พร้อม event/context marker ได้
        แต่ ROT จะไม่เลือกหน่วยปฏิบัติงานให้
        """
        request = MPCPRot._require_dict(request, "ROT_READER_REQUEST")
        category = request.get("CATEGORY")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("ROT_FAIL: READER_CATEGORY_MUST_BE_NON_EMPTY_STRING")

        MPCPRot.validate_rot_type(request)

        has_paper = "PAPER" in request
        has_pack = "PAPER_PACK" in request
        if has_paper == has_pack:
            raise ValueError("ROT_FAIL: READER_REQUEST_MUST_HAVE_EXACTLY_ONE_OF_PAPER_OR_PAPER_PACK")

        allowed = frozenset({
            "ROT_TYPE",
            "ROT_REF",
            "CATEGORY",
            "PAPER",
            "PAPER_PACK",
            "EVENT",
            "EVENT_REF",
            "CONTEXT_REF",
            "ENV_REF",
            "STACK_REF",
            "ADAPTIVE_BASELINE",
            "TRAJECTORY_REF",
            "META",
        })
        if not allow_extra:
            unknown = MPCPRot._unknown_keys(request, allowed)
            if unknown:
                raise ValueError(f"ROT_FAIL: READER_REQUEST_UNKNOWN_KEYS:{','.join(unknown)}")

        if has_paper:
            MPCPRot.validate_paper_command(request["PAPER"], allow_extra=allow_extra)
        else:
            MPCPRot.validate_paper_pack(request["PAPER_PACK"], allow_extra=allow_extra)

        if "EVENT" in request and not isinstance(request["EVENT"], dict):
            raise ValueError("ROT_FAIL: READER_EVENT_MUST_BE_DICT")

        return True

    # =========================
    # PAPER COMMAND LAW
    # =========================
    @staticmethod
    def validate_paper_command(command: dict, *, allow_extra: bool = False):
        """
        ตรวจคำสั่งจาก Paper แบบสั้น แต่ต้องไม่กำกวม

        Required keys:
        - TASK      : งานที่ต้องการให้ทำ
        - INTENT    : เจตนา/ประเภทการทำงาน
        - SCOPE     : ขอบเขตที่อนุญาต
        - BOUNDARY  : boundary manifest id / inline boundary marker

        Optional keys ถูกสงวนไว้สำหรับ Paper Pack, event, stack, PX, Modew และ return contract
        ROT ไม่แปลภาษา ไม่เดา key ให้เอง และไม่ระบุหน่วยที่ต้องทำงาน
        """
        command = MPCPRot._require_dict(command, "PAPER_COMMAND")
        MPCPRot.validate_rot_type(command)

        missing = sorted(PAPER_COMMAND_REQUIRED - set(command.keys()))
        if missing:
            raise ValueError(f"ROT_FAIL: PAPER_COMMAND_MISSING_REQUIRED:{','.join(missing)}")

        for key in PAPER_COMMAND_REQUIRED:
            MPCPRot._require_non_empty_string(command, key)

        if not allow_extra:
            unknown = MPCPRot._unknown_keys(command, PAPER_COMMAND_ALLOWED)
            if unknown:
                raise ValueError(f"ROT_FAIL: PAPER_COMMAND_UNKNOWN_KEYS:{','.join(unknown)}")

        if "TARGET" in command and "TARGETS" in command:
            raise ValueError("ROT_FAIL: PAPER_COMMAND_AMBIGUOUS_TARGET_USE_TARGET_OR_TARGETS")

        if "TARGETS" in command:
            targets = command["TARGETS"]
            if not isinstance(targets, list) or not targets:
                raise ValueError("ROT_FAIL: TARGETS_MUST_BE_NON_EMPTY_LIST")
            for idx, target in enumerate(targets):
                if not isinstance(target, str) or not target.strip():
                    raise ValueError(f"ROT_FAIL: TARGETS[{idx}]_MUST_BE_NON_EMPTY_STRING")

        return True

    @staticmethod
    def validate_paper_pack(pack: dict, *, allow_extra: bool = False):
        """
        Paper Pack = ชุดคำสั่ง Paper หลายใบภายใต้ governance เดียว

        Required:
        - PAPER_PACK_ID
        - PAPERS: list[paper_command]

        Pack สามารถส่ง ROT_TYPE / SCOPE / BOUNDARY ระดับ pack ให้ paper ลูก inherit ได้
        เพื่อรองรับอนาคตที่ยิงกำกับดูแลหลายแห่งพร้อมกัน
        """
        pack = MPCPRot._require_dict(pack, "PAPER_PACK")
        MPCPRot.validate_rot_type(pack)

        pack_id = pack.get("PAPER_PACK_ID")
        if not isinstance(pack_id, str) or not pack_id.strip():
            raise ValueError("ROT_FAIL: PAPER_PACK_ID_MUST_BE_NON_EMPTY_STRING")

        papers = pack.get("PAPERS")
        if not isinstance(papers, list) or not papers:
            raise ValueError("ROT_FAIL: PAPER_PACK_PAPERS_MUST_BE_NON_EMPTY_LIST")

        inherited = {
            key: pack[key]
            for key in (
                "ROT_TYPE",
                "ROT_REF",
                "CATEGORY",
                "SCOPE",
                "BOUNDARY",
                "CONTEXT_REF",
                "ENV_REF",
                "STACK_REF",
                "KNOWLEDGE_BASE_REF",
                "ADAPTIVE_BASELINE",
                "TRAJECTORY_REF",
            )
            if key in pack
        }

        for idx, paper in enumerate(papers):
            if not isinstance(paper, dict):
                raise ValueError(f"ROT_FAIL: PAPER_PACK_PAPER[{idx}]_MUST_BE_DICT")
            merged = {**inherited, **paper, "PAPER_PACK_ID": pack_id}
            try:
                MPCPRot.validate_paper_command(merged, allow_extra=allow_extra)
            except ValueError as exc:
                raise ValueError(f"ROT_FAIL: PAPER_PACK_PAPER[{idx}]:{exc}") from exc

        return True

    # =========================
    # CORE LAW
    # =========================
    @staticmethod
    def validate_core(event: dict, result: dict):
        """
        CAUSE -> ACTION -> RESULT

        Backward-compatible baseline:
        - event ต้องเป็น dict และมี TASK
        - result ต้องเป็น dict และมี state

        Strict result envelope ให้ใช้ validate_result_envelope(..., strict=True)
        """
        event = MPCPRot._require_dict(event, "EVENT")
        result = MPCPRot._require_dict(result, "RESULT")

        if "TASK" not in event:
            raise ValueError("ROT_FAIL: NO_CAUSE (missing TASK)")
        MPCPRot._require_non_empty_string(event, "TASK")

        state = result.get("state")
        if state not in VALID_STATE_ALIASES:
            raise ValueError(f"ROT_FAIL: INVALID_OR_MISSING_RESULT_STATE:{state}")

        return True

    # =========================
    # TRACE LAW
    # =========================
    @staticmethod
    def validate_trace(result: dict, *, strict: bool = False):
        """
        ตรวจ trace ความสัมพันธ์

        non-strict: ต้องมี cause/action
        strict: ต้องมี cause/action/result และ trace ต้องเป็น list ถ้าระบุมา
        """
        result = MPCPRot._require_dict(result, "RESULT")

        for key in ("cause", "action"):
            if key not in result:
                raise ValueError(f"ROT_FAIL: MISSING_{key.upper()}_TRACE")

        if strict and "result" not in result:
            raise ValueError("ROT_FAIL: MISSING_RESULT_TRACE")

        if "trace" in result and not isinstance(result["trace"], list):
            raise ValueError("ROT_FAIL: TRACE_MUST_BE_LIST")

        return True

    # =========================
    # BOUNDARY LAW
    # =========================
    @staticmethod
    def validate_boundary(event: dict):
        """
        กัน event ลอย

        event ที่ดีต้องมี boundary/context/scope/paper/pack อย่างน้อยหนึ่งอย่าง
        ไม่ใช่มีแค่ TASK แล้วให้ระบบเดาเอง
        """
        event = MPCPRot._require_dict(event, "EVENT")

        if len(event.keys()) <= 1:
            raise ValueError("ROT_FAIL: NO_CONTEXT")

        boundary_markers = (
            "BOUNDARY",
            "SCOPE",
            "CONTEXT",
            "CONTEXT_REF",
            "ENV_REF",
            "PAPER_ID",
            "PAPER_PACK_ID",
            "ROT_TYPE",
            "ROT_REF",
            "EVENT_ID",
            "EVENT_REF",
            "STACK_REF",
        )
        if not any(marker in event for marker in boundary_markers):
            raise ValueError("ROT_FAIL: NO_BOUNDARY_MARKER")

        return True

    # =========================
    # RESULT ENVELOPE LAW
    # =========================
    @staticmethod
    def validate_result_envelope(result: dict, *, strict: bool = False):
        """
        ตรวจ MPCP result envelope

        non-strict:
        - dict
        - state ถูกต้อง
        - halt state ต้องมี error

        strict:
        - ต้องมี schema/state/cause/action/result/law/restore/meta
        - schema ต้องเป็น mpcp.result.*
        - mutation flags ถ้ามี ต้องเป็น bool
        - law/restore/meta ต้องเป็น dict
        """
        result = MPCPRot._require_dict(result, "RESULT")

        state = result.get("state")
        if state not in VALID_STATE_ALIASES:
            raise ValueError(f"ROT_FAIL: INVALID_OR_MISSING_RESULT_STATE:{state}")

        if state in HALT_STATES and "error" not in result:
            raise ValueError(f"ROT_FAIL: HALT_STATE_{state}_MISSING_ERROR")

        if strict:
            missing = sorted(RESULT_REQUIRED_STRICT - set(result.keys()))
            if missing:
                raise ValueError(f"ROT_FAIL: RESULT_ENVELOPE_MISSING_REQUIRED:{','.join(missing)}")

            schema = result.get("schema")
            if not isinstance(schema, str) or not schema.startswith("mpcp.result."):
                raise ValueError("ROT_FAIL: RESULT_SCHEMA_MUST_START_WITH_mpcp.result")

            for key in ("law", "restore", "meta"):
                if not isinstance(result.get(key), dict):
                    raise ValueError(f"ROT_FAIL: RESULT_{key.upper()}_MUST_BE_DICT")

            for key in MUTATION_FLAGS:
                if key in result and not isinstance(result[key], bool):
                    raise ValueError(f"ROT_FAIL: {key.upper()}_MUST_BE_BOOL")

        return True

    # =========================
    # STACK / KNOWLEDGE BASE LAW
    # =========================
    @staticmethod
    def validate_stack(stack: list[dict]):
        """
        ตรวจ execution / governance stack แบบขั้นต่ำ

        Stack ยังไม่ตีความงาน แต่บังคับว่าแต่ละ frame ต้องระบุตัวตนพอให้ย้อนรอยได้
        """
        if not isinstance(stack, list):
            raise ValueError("ROT_FAIL: STACK_MUST_BE_LIST")

        for idx, frame in enumerate(stack):
            if not isinstance(frame, dict):
                raise ValueError(f"ROT_FAIL: STACK_FRAME[{idx}]_MUST_BE_DICT")
            if not any(key in frame for key in ("EVENT_ID", "PAPER_ID", "TASK", "STATE", "RESULT")):
                raise ValueError(f"ROT_FAIL: STACK_FRAME[{idx}]_MISSING_TRACE_MARKER")

        return True

    @staticmethod
    def validate_minimum_knowledge_base(kb: dict):
        """
        ตรวจฐานความรู้ขั้นต่ำที่ ROT ใช้อ้างอิง

        ROT ไม่ต้องแบกความรู้ทั้งหมด แต่ต้องรู้ว่าใช้ baseline ไหนอยู่
        """
        kb = MPCPRot._require_dict(kb, "KNOWLEDGE_BASE")

        baseline = kb.get("BASELINE") or kb.get("baseline")
        if not isinstance(baseline, str) or not baseline.strip():
            raise ValueError("ROT_FAIL: KNOWLEDGE_BASE_MISSING_BASELINE")

        return True

    # =========================
    # FAIL CONDITION CHECK
    # =========================
    @staticmethod
    def validate_fail_condition(event: dict, result: dict):
        """
        ใช้ detect system invalid state
        - STOP / fail / block ต้องมี error field
        - result ต้องผ่าน envelope ขั้นต่ำ
        """
        if not result:
            raise ValueError("ROT_FAIL: EMPTY_RESULT")

        MPCPRot.validate_result_envelope(result, strict=False)
        return True
