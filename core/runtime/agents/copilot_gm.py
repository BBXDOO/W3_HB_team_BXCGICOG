from collections.abc import Mapping
from typing import Dict, Any

from .base import RuntimeAgent


class CopilotGmAgent(RuntimeAgent):
    module_name = "Copilot-Gm"
    action_label = "completed governance review"
    # W3 ecosystem role: governance / structural consistency (W3LGU_MPCP_ROLE_MAPPING.md §9)
    mpcp_role = "governance"
    mpcp_concepts = ["governance", "policy", "compliance", "structural consistency"]

    @staticmethod
    def _thai_markdown_guide() -> str:
        """Return the owned draft for the registered Thai Markdown guide task."""
        return r'''คู่มือนี้อธิบาย Markdown สำหรับผู้เริ่มต้น โดยแยกสิ่งที่เป็น Markdown
มาตรฐาน, GitHub Flavored Markdown (GFM), HTML/CSS และความสามารถที่ขึ้นกับ renderer
อย่างชัดเจน

> **หลักสำคัญ:** Markdown เน้นโครงสร้างของเนื้อหา ไม่ได้กำหนดสี ขนาด หรือเส้นขอบ
> แบบระบบจัดหน้าเต็มรูปแบบ ความสามารถด้านรูปลักษณ์จึงต้องตรวจ renderer ที่ใช้งานเสมอ

## 1. รูปแบบพื้นฐาน

### หัวข้อและย่อหน้า

```md
# หัวข้อระดับ 1
## หัวข้อระดับ 2
### หัวข้อระดับ 3

ย่อหน้าแรก

ย่อหน้าที่สอง แยกด้วยบรรทัดว่าง
```

### รายการและลำดับเลข

```md
- รายการแบบจุด
  - รายการย่อย

1. ขั้นตอนแรก
2. ขั้นตอนถัดไป
```

### โค้ด

ใช้ backtick ครอบโค้ดสั้น เช่น `` `print("W3")` `` และใช้รั้วสาม backticks
สำหรับ code block:

````md
```python
print("Build. Observe. Learn. Continue.")
```
````

## 2. การสร้างตาราง

```md
| ชื่อ | สถานะ | หมายเหตุ |
|:---|:---:|---:|
| W3 | พร้อม | ขวา |
| BOX | ตรวจสอบ | ขวา |
```

- `:---` จัดซ้าย, `:---:` จัดกึ่งกลาง และ `---:` จัดขวา
- ตารางเป็นความสามารถเด่นของ GFM ไม่ใช่ CommonMark ขั้นต่ำทุกตัว
- ตาราง Markdown ไม่รองรับการรวมเซลล์ สีพื้นหลัง หรือเส้นขอบแบบละเอียดโดยตรง
- หากข้อความมี `|` ให้ escape เป็น `\|` หรือใช้ HTML ตาม renderer

## 3. สีพื้นหลังของตาราง

Markdown มาตรฐานไม่มีไวยากรณ์กำหนดสีพื้นหลัง ตารางที่ต้องการสีต้องพึ่ง HTML/CSS:

```html
<table>
  <tr style="background-color: #fff3cd;">
    <th>สถานะ</th><th>ความหมาย</th>
  </tr>
  <tr><td>รอตรวจ</td><td>WAITING_HUMAN</td></tr>
</table>
```

ตัวอย่างนี้ **ขึ้นกับ renderer** โดย GitHub อาจกรองแอตทริบิวต์ `style` จึงไม่ควรใช้สี
เป็นหลักฐานสถานะเพียงอย่างเดียว ควรมีข้อความกำกับเสมอ

## 4. สีและข้อความ

Markdown ไม่มีคำสั่งสีข้อความมาตรฐาน ตัวอย่าง fallback:

```html
<span style="color: #c62828;">ข้อความสีแดง</span>
```

HTML/CSS อาจใช้ได้ใน Obsidian หรือ renderer ที่อนุญาต แต่ GitHub อาจตัด style ออก
และ Pure Writer ขึ้นกับโหมด preview/renderer ที่เลือก จึงต้องทดลองกับปลายทางจริง

## 5. การสร้างลิงก์

```md
[ข้อความลิงก์](https://example.com)
<https://example.com>
![คำอธิบายภาพ](images/example.png)
[ไปยังหัวข้อการสร้างตาราง](#2-การสร้างตาราง)
[อ่านไฟล์ใกล้เคียง](./README.md)
[ย้อนขึ้นหนึ่งระดับ](../README.md)
```

- ใช้ relative path เมื่อไฟล์อยู่ใน repository เดียวกัน
- anchor ถูกสร้างต่างกันได้ตาม renderer โดยเฉพาะภาษาไทยและหัวข้อที่มีสัญลักษณ์
- หลีกเลี่ยง URL ติดตามและตรวจว่าไฟล์ปลายทางมีอยู่จริงก่อนเผยแพร่

## 6. ตัวหนา ตัวเอียง ขีดฆ่า และขีดเส้นใต้

```md
**ตัวหนา**
*ตัวเอียง*
***หนาและเอียง***
~~ขีดฆ่า~~
<u>ขีดเส้นใต้</u>
```

ตัวหนาและตัวเอียงเป็น Markdown ทั่วไป ส่วนขีดฆ่าเป็น GFM และ `<u>` เป็น HTML
ซึ่งขึ้นกับ renderer

## 7. เส้นแนวนอนและเส้นแนวตั้ง

เส้นแนวนอนมาตรฐานเขียนได้ดังนี้:

```md
---
```

ควรมีบรรทัดว่างก่อนเส้น เพื่อไม่ให้ `---` ถูกตีความเป็นหัวข้อแบบ Setext
Markdown ไม่มีเส้นแนวตั้งอิสระ เครื่องหมาย `|` เป็นเพียงตัวแบ่งคอลัมน์ในตาราง
หากต้องการเส้นตกแต่งให้ใช้ HTML/CSS และยอมรับว่าอาจไม่ทำงานทุก renderer:

```html
<div style="border-left: 4px solid #4a90e2; padding-left: 12px;">
  ข้อความข้างเส้นแนวตั้ง
</div>
```

## 8. การเพิ่มความหนาของเส้น

ความหนาเส้นไม่ใช่ความสามารถของ Markdown ต้องใช้ CSS เช่น:

```html
<hr style="border: 0; border-top: 6px solid #333;">
```

บน GitHub อาจถูกกรอง style ออก ทางเลือกที่เข้ากันได้ดีกว่าคือใช้ `---` แล้วปล่อยให้
ธีมหรือ renderer เป็นผู้กำหนดรูปแบบ

## 9. เทคนิคเพิ่มเติม

### Blockquote และ checklist

```md
> ข้อความอ้างอิง

- [x] ทำแล้ว
- [ ] ยังไม่ทำ
```

Checklist เป็น GFM และอาจแสดงเป็นกล่องที่คลิกไม่ได้ในบางโปรแกรม

### Details/summary

```html
<details>
<summary>แตะเพื่อดูรายละเอียด</summary>

เนื้อหาที่ซ่อนไว้
</details>
```

นี่คือ HTML fallback และขึ้นกับ renderer

### Escaping และการขึ้นบรรทัดใหม่

```md
\*ไม่ให้เป็นตัวเอียง\*
บรรทัดแรก\
บรรทัดที่สอง
```

ใช้ backslash หน้าสัญลักษณ์เพื่อแสดงตัวอักษรตามจริง การเว้นสองช่องท้ายบรรทัดสร้าง
line break ใน Markdown หลายแบบ แต่บรรทัดว่างมักอ่านและบำรุงรักษาง่ายกว่า

## 10. ตารางความเข้ากันได้

| รูปแบบ | ประเภท | GitHub | หมายเหตุ |
|:---|:---|:---:|:---|
| หัวข้อ รายการ ลิงก์ ตัวหนา ตัวเอียง | Markdown ทั่วไป | ✅ | ใช้ได้กว้าง |
| ตาราง ขีดฆ่า checklist | GFM | ✅ | renderer อื่นอาจต่างกัน |
| `<u>` และ `<details>` | HTML fallback | บางส่วน | ขึ้นกับ renderer |
| สีข้อความ/พื้นหลังผ่าน `style` | HTML/CSS | ⚠️ | GitHub อาจกรอง style |
| เส้นแนวตั้ง/ความหนาเส้นผ่าน CSS | HTML/CSS | ⚠️ | ไม่ใช่ Markdown มาตรฐาน |
| anchor ภาษาไทย | ขึ้นกับ renderer | ⚠️ | ตรวจลิงก์กับปลายทางจริง |

## แนวทางใช้งานที่ปลอดภัย

1. เริ่มจาก Markdown/GFM ที่เรียบง่ายก่อน
2. ใช้ HTML/CSS เฉพาะเมื่อทราบ renderer ปลายทาง
3. อย่าใช้สีเพียงอย่างเดียวเพื่อสื่อสถานะ
4. เปิด preview และทดสอบลิงก์ relative path ก่อน commit
5. เมื่อไม่ทราบผล ให้บันทึกว่า “ขึ้นกับ renderer” แทนการคาดเดา'''

    def _create_document(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        request_type = self.resolve_context_value(context, "request_type")
        document_kind = self.resolve_context_value(context, "document_kind")
        if request_type != "document_creation" or document_kind != "thai_markdown_guide":
            return self._review_required(
                task,
                "Document creation requires a registered document_kind and explicit request scope.",
                "unsupported_document_request",
            )
        request_id = str(self.resolve_context_value(context, "request_id") or "")
        target = str(self.resolve_context_value(context, "artifact_path") or "")
        if not request_id or not target:
            return self._review_required(task, "request_id and artifact_path are required.", "missing_document_scope")
        return {
            "contract_version": "1.2",
            "status": "BLOCKED",
            "module": self.module_name,
            "task": task,
            "role": "document_owner",
            "action": "document_content_prepared",
            "decision": "ASSIST_REQUIRED",
            "summary": "Copilot-Gm prepared the document content; an authorized artifact writer is required.",
            "reason": "Content ownership and filesystem execution are separated by the Orchestration contract.",
            "document_spec": {
                "title": "คู่มือการใช้ Markdown ฉบับภาษาไทย",
                "target": target,
                "am_type": "II",
                "group": "LEARN",
                "owner": "BBX19",
                "maker": self.module_name,
                "body": self._thai_markdown_guide(),
                "derived_from": [str(self.resolve_context_value(context, "source_request") or "")],
                "request_id": request_id,
                "note": "Copilot-Gm draft; Gemini validated; BBX19 sign-off required",
                "status": "waiting_human",
            },
            "artifacts": [],
            "mutated": False,
            "traceable": True,
            "review": True,
            "authority": {"decision_allowed": False, "merge_allowed": False, "truth_mutation_allowed": False},
        }

    def _review_required(
        self,
        task: Any,
        reason: str,
        decision: str,
        *,
        preload: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        result = {
            "contract_version": "1.2",
            "status": "REVIEW_REQUIRED",
            "module": self.module_name,
            "task": str(task or ""),
            "role": self.mpcp_role,
            "action": "governance_concept_coverage_review",
            "decision": decision,
            "summary": "Copilot-Gm did not complete the governance coverage review.",
            "reason": reason,
            "preload": preload or {
                "context_valid": False,
                "notes_count": 0,
                "decisions_count": 0,
                "expectations_count": 0,
                "has_progress": False,
            },
            "result": {
                "required_terms": list(self.mpcp_concepts),
                "found_terms": [],
                "missing_terms": list(self.mpcp_concepts),
                "coverage_ratio": 0.0,
                "min_coverage": 0.5,
            },
            "details": {
                "governance_scope": "concept_coverage_only",
                "merge_performed": False,
                "authority_granted": False,
                "evidence_supplied": False,
                "evidence_type": "none",
            },
            "artifacts": [],
            "mutated": False,
            "traceable": True,
            "review": True,
            "authority": {
                "decision_allowed": False,
                "merge_allowed": False,
                "truth_mutation_allowed": False,
            },
        }
        result["evidence"] = self.collect_evidence({}, {}, {}, result)
        result["reflection"] = self.reflect(str(task or ""), {}, {}, result)
        result["continuity"] = self.persist_continuity(
            str(task or ""), {}, {}, result, result["reflection"]
        )
        return result

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Governance executor (MVP):
        - checks concept coverage in doc_text
        - returns traceable, non-fabricated status
        - includes reflection + continuity packet
        """
        origin_result = self.execute_origin(task, plan, context)
        if origin_result is not None:
            return origin_result
        if not isinstance(plan, Mapping) or not isinstance(context, Mapping):
            return self._review_required(
                task,
                "plan and context must be mappings",
                "invalid_review_input",
            )
        plan = dict(plan)
        context = dict(context)

        if self.resolve_context_value(context, "request_type") == "document_creation":
            return self._create_document(task, plan, context)

        preload = self.preload_context(task, plan, context)
        raw_review_material = self.resolve_context_value(
            context, "doc_text", "text", "evidence", "artifacts"
        )
        doc_text = self.normalize_review_text(raw_review_material)
        target = self.resolve_context_value(context, "target") or "W3"
        responsibilities = self._responsibilities(plan)

        if not doc_text:
            return self._review_required(
                task,
                "Governance review requires explicit document text or supporting evidence.",
                "missing_governance_evidence",
                preload=preload,
            )

        required_terms = list(self.mpcp_concepts)
        found_terms = self.inspect_mpcp(doc_text)
        missing_terms = [t for t in required_terms if t not in found_terms]

        raw_min_coverage = plan.get("min_coverage", 0.5)
        try:
            min_coverage = float(raw_min_coverage)
        except (TypeError, ValueError):
            min_coverage = 0.5
        # Zero coverage must never be sufficient evidence of a completed review.
        min_coverage = max(0.25, min(1.0, min_coverage))

        coverage_ratio = (len(found_terms) / len(required_terms)) if required_terms else 1.0
        completed = coverage_ratio >= min_coverage
        status = "COMPLETED" if completed else "REVIEW_REQUIRED"

        summary = (
            f"{self.module_name} governance review on {target}: "
            f"{len(found_terms)}/{len(required_terms)} concept coverage "
            f"({coverage_ratio:.0%}, threshold={min_coverage:.0%})"
        )

        result = {
            "contract_version": "1.2",
            "status": status,
            "module": self.module_name,
            "task": task,
            "role": self.mpcp_role,
            "action": "governance_concept_coverage_review",
            "decision": "COVERAGE_ACCEPTED" if completed else "COVERAGE_INCOMPLETE",
            "summary": summary,
            "target": target,
            "responsibilities": responsibilities,
            "preload": preload,
            "result": {
                "required_terms": required_terms,
                "found_terms": found_terms,
                "missing_terms": missing_terms,
                "coverage_ratio": coverage_ratio,
                "min_coverage": min_coverage,
            },
            "details": {
                "governance_scope": "concept_coverage_only",
                "merge_performed": False,
                "authority_granted": False,
                "evidence_supplied": True,
                "evidence_type": type(raw_review_material).__name__,
            },
            "artifacts": [
                {
                    "type": "governance_review",
                    "label": f"{self.module_name} concept coverage",
                    "evidence": {
                        "terms_scanned": required_terms,
                        "terms_found": found_terms,
                        "terms_missing": missing_terms,
                    },
                }
            ],
            "mutated": False,
            "traceable": True,
            "review": not completed,
            "authority": {
                "decision_allowed": False,
                "merge_allowed": False,
                "truth_mutation_allowed": False,
            },
        }

        result["evidence"] = [
            {
                "type": "review_input",
                "evidence_class": "input_evidence",
                "label": "Normalized governance review material",
                "value_type": type(raw_review_material).__name__,
                "present": True,
            }
        ] + self.collect_evidence(task, plan, context, result)
        result["reflection"] = self.reflect(task, plan, context, result)
        result["continuity"] = self.persist_continuity(
            task, plan, context, result, result["reflection"]
        )
        return result
