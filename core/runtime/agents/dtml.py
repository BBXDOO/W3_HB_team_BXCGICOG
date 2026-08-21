from __future__ import annotations

"""DTML Agent — Decision Trace Mapping with anomaly-driven inspection modes.

DTML ("หัวหน้าวิศวกร" จากต้นฉบับ W3Lgu) ทำหน้าที่ trace การตัดสินใจในเชน
ปกติแล้วมันเดินตาม trace_decision() ของชั้น mfc logic ที่มีอยู่เดิม
(ไม่ทับ ไม่แก้ของเก่า — ใช้ต่อโดยตรง)

ส่วนขยายของไฟล์นี้คือ "โหมดการอ่าน" 2 แบบจากต้นฉบับ W3Lgu
ที่จะเปิดเมื่อพบความผิดปกติหรือต้องตรวจข้อสงสัย:

    • Chaos Area  (พื้นที่โกลาหล)  — วิเคราะห์แบบไม่เป็นเส้นตรง
                                     หาความสัมพันธ์ที่ซ่อนอยู่ใน event
    • Matrix Layer (แมทริคเลเยอร์) — วาง event ลงหลายแกนพร้อมกัน
                                     ตรวจ cross-reference

ทั้งสองโหมดออกแบบเป็น "extension point" — มี interface ชัดเจน
ให้ต่อยอด logic จริงภายหลังได้ โดยไม่ต้องแก้เชนหรือ contract
ค่า return ทุกเส้นทางเป็น W3LguLogicResult shape เดียวกับทั้งระบบ
"""

from typing import Any, Dict, Mapping, Optional, Protocol

from .base import RuntimeAgent
from ..w3lgu_mfc_logic.dtml_mfc_logic import trace_decision
from ..w3lgu_mfc_logic.contracts import (
    ACTIVE,
    REVIEW_REQUIRED,
    WAIT,
    make_result,
    normalize_text,
)


# ───────────────────────────────────────────────────────────────────
# Anomaly detection — ตัวกระตุ้นให้ DTML เปิดโหมดตรวจสอบพิเศษ
# ───────────────────────────────────────────────────────────────────

# สัญญาณที่บอกว่า event "ผิดปกติ" พอที่จะเปิด Chaos Area
ANOMALY_MARKERS = {
    "anomaly", "irregular", "unexpected", "contradiction", "conflict",
    "inconsistent", "drift", "diverge", "loop", "deadlock", "paradox",
}

# สัญญาณที่บอกว่าต้องตรวจ "หลายมิติ" พอที่จะเปิด Matrix Layer
MULTIDIM_MARKERS = {
    "cross", "multi", "matrix", "grid", "layer", "intersect",
    "correlate", "dependency", "relation", "px", "coordinate",
}


def _as_payload(decision_input: Any) -> Dict[str, Any]:
    if isinstance(decision_input, Mapping):
        return dict(decision_input)
    return {"text": normalize_text(decision_input)}


def _scan(text: str, words) -> list[str]:
    lowered = text.lower()
    return sorted(w for w in words if w in lowered)


# ───────────────────────────────────────────────────────────────────
# Extension Point 1 — CHAOS AREA  (พื้นที่โกลาหล)
# ───────────────────────────────────────────────────────────────────

class ChaosAreaResolver(Protocol):
    """Interface สำหรับ logic การวิเคราะห์แบบ non-linear.

    ผู้ implement รับ event payload + markers ที่พบ
    คืน dict ที่อธิบาย 'ความสัมพันธ์ที่ซ่อนอยู่' ที่ค้นพบ
    DTML จะนำผลนี้ใส่ลง details และตัดสิน status ตามนั้น
    """

    def resolve(
        self,
        payload: Mapping[str, Any],
        anomaly_markers: list[str],
    ) -> Dict[str, Any]:
        ...


class _DefaultChaosArea:
    """Default stub — ยังไม่วิเคราะห์จริง แต่เปิดพื้นที่ไว้ครบ

    คืนโครงผลลัพธ์มาตรฐานให้ผู้ต่อยอดเติม logic จริงภายหลัง
    โดยไม่ทำให้ DTML พังถ้ายังไม่มี implementation
    """

    def resolve(
        self,
        payload: Mapping[str, Any],
        anomaly_markers: list[str],
    ) -> Dict[str, Any]:
        return {
            "mode": "chaos_area",
            "engaged": True,
            "implemented": False,
            "anomaly_markers": anomaly_markers,
            "observations": [],          # ← logic จริงเติมความสัมพันธ์ที่นี่
            "hypotheses": [],            # ← สมมติฐานที่ค้นพบ
            "note": "chaos area opened; non-linear analysis pending implementation",
        }


# ───────────────────────────────────────────────────────────────────
# Extension Point 2 — MATRIX LAYER  (แมทริคเลเยอร์)
# ───────────────────────────────────────────────────────────────────

class MatrixLayerResolver(Protocol):
    """Interface สำหรับ logic การตรวจหลายมิติพร้อมกัน.

    ผู้ implement รับ event payload + markers
    คืน dict ที่อธิบาย cross-reference ระหว่างแกนต่างๆ
    (เช่น PX coordinate, dependency, relation)
    """

    def project(
        self,
        payload: Mapping[str, Any],
        multidim_markers: list[str],
    ) -> Dict[str, Any]:
        ...


class _DefaultMatrixLayer:
    """Default stub — เปิด layer ไว้ครบ พร้อมให้เติม projection จริง"""

    def project(
        self,
        payload: Mapping[str, Any],
        multidim_markers: list[str],
    ) -> Dict[str, Any]:
        return {
            "mode": "matrix_layer",
            "engaged": True,
            "implemented": False,
            "multidim_markers": multidim_markers,
            "axes": [],                  # ← logic จริงกำหนดแกนที่นี่
            "cells": [],                 # ← จุดตัด/cross-reference
            "note": "matrix layer opened; multi-axis projection pending implementation",
        }


# ───────────────────────────────────────────────────────────────────
# DTML Agent
# ───────────────────────────────────────────────────────────────────

class DTMLAgent(RuntimeAgent):
    module_name = "DTML"
    action_label = "completed decision trace mapping"
    mpcp_role = "decision_trace"
    mpcp_concepts = ["decision", "trace", "timeline", "memory"]

    def __init__(
        self,
        chaos_area: Optional[ChaosAreaResolver] = None,
        matrix_layer: Optional[MatrixLayerResolver] = None,
    ) -> None:
        # ฉีด resolver ได้จากภายนอก (dependency injection)
        # ถ้าไม่ฉีด ใช้ default stub ที่เปิดพื้นที่ไว้แต่ยังไม่วิเคราะห์
        self._chaos_area: ChaosAreaResolver = chaos_area or _DefaultChaosArea()
        self._matrix_layer: MatrixLayerResolver = matrix_layer or _DefaultMatrixLayer()

    # --- โหมดปกติ: เดินตาม trace_decision เดิม (ไม่ทับของเก่า) ---

    def trace(self, decision_input: Any) -> Dict[str, Any]:
        """เส้นทางหลักของ DTML — decision trace ปกติ"""
        return trace_decision(decision_input).as_dict()

    def execute(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Inspect a decision boundary and return a traceable continuation state."""
        decision_input: Dict[str, Any] = {"text": task}
        if isinstance(context, Mapping):
            request = context.get("request")
            if isinstance(request, Mapping):
                decision_input.update(request)
            decision_input.update({key: value for key, value in context.items() if key != "request"})

            # Promote routing evidence from the previous MFC stage so the
            # authoritative DTML core receives the same decision context no
            # matter which runtime entry invoked this agent.
            upstream = context.get("payload")
            if isinstance(upstream, Mapping):
                upstream_details = (
                    upstream.get("details")
                    if isinstance(upstream.get("details"), Mapping)
                    else {}
                )
                for key in (
                    "route_scope",
                    "unknown_routes",
                    "cross_routes",
                    "bridge_contract",
                    "review_required",
                    "status",
                    "risk",
                    "stop_required",
                ):
                    value = upstream.get(key, upstream_details.get(key))
                    if value not in (None, "", [], {}):
                        decision_input.setdefault(key, value)
        result = self.inspect(decision_input)
        result.update(
            {
                "contract_version": "1.0", "task": task,
                "action": "inspect_decision_trace",
                "summary": (
                    f"DTML decision={result.get('decision')} "
                    f"status={result.get('status')} next={result.get('next', [])}."
                ),
                "artifacts": [],
            }
        )
        return result

    # --- โหมดพิเศษ: เปิดเมื่อพบความผิดปกติ/ข้อสงสัย ---

    def inspect(self, decision_input: Any) -> Dict[str, Any]:
        """ตรวจ event แล้วเลือกโหมด:

            ปกติ            → trace_decision เดิม
            พบ anomaly      → เปิด Chaos Area
            พบ multi-dim    → เปิด Matrix Layer
            พบทั้งคู่         → เปิดทั้งสอง (REVIEW_REQUIRED)

        ทุกเส้นทางส่งสำเนาให้ LRC2 (บันทึกก่อนจบ)
        """
        payload = _as_payload(decision_input)
        text = normalize_text(payload)

        if not text:
            return make_result(
                module=self.module_name,
                status=WAIT,
                confidence=0.0,
                input_type="inspect:empty",
                decision="wait_for_inspectable_input",
                reason="no inspectable decision input",
                next_modules=["LRC2"],
                standby=["REDR", "PSP2"],
                details={"payload": payload},
            ).as_dict()

        anomaly = _scan(text, ANOMALY_MARKERS)
        multidim = _scan(text, MULTIDIM_MARKERS)

        # ไม่ผิดปกติ ไม่ซับซ้อน → ใช้ trace ปกติ
        if not anomaly and not multidim:
            return self.trace(decision_input)

        modes: Dict[str, Any] = {}
        if anomaly:
            modes["chaos_area"] = self._chaos_area.resolve(payload, anomaly)
        if multidim:
            modes["matrix_layer"] = self._matrix_layer.project(payload, multidim)

        # Chaos/Matrix are observation providers only.  They never make the
        # final continuation decision; every path returns to the MFC core.
        payload["inspection"] = modes
        payload["anomaly_markers"] = anomaly
        payload["multidim_markers"] = multidim
        return self.trace(payload)

    # --- run(): entry point ของ agent ในเชน ---

    def run(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        # รวม task + context เป็น input ให้ inspect ตัดสินโหมดเอง
        decision_input: Dict[str, Any] = {"text": task}
        if isinstance(context, Mapping):
            decision_input.update(
                {k: v for k, v in context.items() if k != "text"}
            )

        result = self.inspect(decision_input)

        modes = result.get("details", {}).get("modes", {})
        engaged = sorted(modes.keys()) if modes else []

        return (
            f"{self.module_name} ({plan.get('role', 'engineer')}) "
            f"{self.action_label}: {task} | "
            f"status: {result.get('status')} | "
            f"type: {result.get('input_type')} | "
            f"decision: {result.get('decision')} | "
            f"modes: {engaged or '-'} | "
            f"next: {result.get('next')} | "
            f"mutated: False"
        )


__all__ = [
    "DTMLAgent",
    "ChaosAreaResolver",
    "MatrixLayerResolver",
]
