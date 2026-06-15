# wx:BOX + CN-Fold Recovery Anchor

> Status: active / recovery-anchor  
> Runtime: none  
> Mutation: false  
> Owner approval: BBX19  
> Source truth: GitHub  
> Anchor scope: BOX + CN-Fold concept only

เอกสารนี้ใช้เป็นจุดถอยกลับหลังจาก PR กลุ่ม Cross-X / E-CS / MPCP Adapter / W3Lgu operational runtime / BOX suggestion ชนกันหลายระบบพร้อมกัน

เป้าหมายคือกลับมายืนที่จุดปลอดภัย: `wx:BOX` เป็นกล่องอ้างอิง และ `CN-Fold` เป็นแนวคิด folder-as-node ภายใน BOX

---

## 1. Recovery Position

```text
Use wx:BOX as the active direction.
Use CN-Fold as folder/node behavior inside BOX.
Pause Cross-L → MPCP Adapter standardization until return contract is separated.
```

ตอนนี้แกนที่ควรรักษาคือ:

```text
wx:BOX = manifest + reference container + folder/node context
CN-Fold = host + relation + boundary + status behavior
```

---

## 2. Why we step back

PR กลุ่มล่าสุดพยายามรวมหลายแกนในครั้งเดียว:

```text
Cross-L dispatch
MPCP execution adapter
E-CS chain
W3Lgu operational runtime
BOX suggestion
W3-API integration
CI matrix
```

ผลคือเกิด cross-system collision:

```text
- CROLL tests ล้ม
- BOX / W3-API integration ล้ม
- adapter เริ่มแตะ authority / return / runtime หลายชั้นพร้อมกัน
```

จึงต้องถอยกลับมาแยกงานก่อน

---

## 3. What remains active

```text
ACTIVE:
- wx/templates/box/README.md
- wx/templates/box/USAGE_TH.md
- wx/templates/box/wx_box_minimum.md
- wx/blueprints/system/wx_box_cn_fold_integration.md
- wx/references/cn_fold_to_wx_box_mapping.md
- wx/index/by_box.md
- registry entry: BOX:WX_BOX_MINIMUM_V1
```

บทบาทของกลุ่มนี้คือเอกสาร/เทมเพลต/อ้างอิง ไม่ใช่ runtime

---

## 4. What is paused

```text
PAUSED:
- Cross-L → MPCP execution adapter
- E-CS chain as required runtime path
- W3Lgu operational runtime as dependency for CROLL
- BOX suggestion inside CROLL planner as required behavior
- W3-API response standard tied directly to BOX/W3Lgu/Cross-L
```

สิ่งเหล่านี้ยังไม่ถูกปฏิเสธ แต่ต้องแยกเป็น PR เล็กและมี contract ก่อน

---

## 5. Return Contract must come first

ก่อนเชื่อม Cross-L → MPCP Adapter ต้องมี return contract ที่เล็กมากและไม่ผูกกับ runtime ใดก่อน

ขั้นต่ำ:

```yaml
return_contract:
  state: READY | REVIEW | STOP
  result: null
  trace: null
  mutated: false
  review: true
  source: null
  boundary: reference_only
```

กฎ:

```text
Return contract ก่อน adapter
Adapter ก่อน execution
Execution ก่อน standardization
```

---

## 6. Guardrails

```text
BOX can point, describe, index, and export reference data.
BOX must not execute.
BOX must not mutate source truth.

Cross-L can dispatch and describe bounded work.
Cross-L must not self-grant execution.

MPCP Adapter can be proposed later.
MPCP Adapter must not become owner of W3Lgu, BOX, or E-CS.

W3Lgu can carry meaning and packet shape.
W3Lgu must not be reduced to parser-first 1→2→3 pipeline.
```

---

## 7. Next safe PR order

```text
PR 1: Keep BOX + CN-Fold docs and template only
PR 2: Add return_contract reference document only
PR 3: Add Cross-L → MPCP handoff as observe-only, no execute
PR 4: Add adapter tests without W3Lgu operational dependency
PR 5: Add execution adapter only after owner approval
```

---

## 8. Recovery Test Set

ใช้ชุดนี้เป็น baseline หลังถอยกลับ:

```bash
python -m pytest tests/test_cross_x_config.py tests/test_file_void_tool.py -q
python -m pytest croll/test_cross_l_dispatcher.py -q
python -m pytest wx/test_engine_index.py tests/test_box_integration.py -q
```

ถ้าชุดนี้ไม่ผ่าน ห้ามเพิ่ม adapter ใหม่

---

## 9. One-line Summary

```text
ถอยกลับมาให้ wx:BOX เป็นแกนเอกสาร/อ้างอิง และให้ CN-Fold เป็น behavior ภายใน BOX ก่อน แล้วค่อยแยก return contract และ adapter เป็นชั้นถัดไป
```
