# W3 Integration Guide v0.3

This guide describes the integration-grade flow connecting EP_SIGNAL, W3DB,
Hospitication, Pilot 2 layer separation, and Semantic Router interpretation.

## Integration flow

```text
EP_SIGNAL
  -> integrations.ep_signal_w3db.store_ep_signal_to_w3db
  -> W3DB XIZ/TUF/FBD/WHB/PRX
  -> Hospitication report/signals
  -> hospitication.w3db_adapter.store_hospitication_report_to_w3db
  -> scripts/enforce_layer_separation.py --hospitication-signals report.json
  -> core.semantic_router.interpret_hospitication_report
```

## Guarantees

- EP_SIGNAL payloads are decoded and observed; they are not rewritten.
- W3DB records are appended through the existing relation flow.
- Hospitication emits immutable signals and proposal-only recovery guidance.
- Pilot 2 can use Hospitication signals as early-warning context to downgrade a
  temporary RED to YELLOW, but this is recorded as perception, not execution.
- Semantic Router interpretation creates derived references only and must not
  overwrite signals or reports.

## Component commands

```bash
python -m hospitication.cli --repo . --format json --output hospitication-report.json
python scripts/enforce_layer_separation.py --json --hospitication-signals hospitication-report.json
python examples/use_semantic_router_hospitication.py
```

## References

- `docs/standards/referencing_standard.md`
- `protocol/EP_SIGNAL/INTERPRETATION_BOUNDARY_PAPER.md`
- `hospitication/docs/ARCHITECTURE.md`
- `core/semantic_router.py`

## Cross-X coordination

Cross-X adds an ecosystem-level planning layer above the existing adapters:

```text
Intent -> Cross-X -> W3Lgu -> PX -> W3DB append envelope -> EP_SIGNAL preview
```

- Config map: `config/environment.json`, `config/ecosystem.json`, `config/cross_system.json`, `config/paths.json`
- Coordinator: `cross_x/core.py`
- PX pointer: `protocol/w3lgu/px.py`
- Append envelope: `src/w3db/append_flow.py`

Cross-X plans do not persist records by default. They describe what should cross
what, why, and which append envelope can be used after Human Review and
Governance Gate.


## บันทึกการใช้งานบน Termux / Android

การบันทึก intent ของ `BBEX-Core` ใช้การสร้างไฟล์แบบ exclusive
(`O_CREAT | O_EXCL`) เพื่อรักษากฎ append-only โดยไม่พึ่ง `os.link()`
ซึ่งอาจไม่มีให้ใช้ใน Python บน Android/Termux บางชุด

หลักการยังเหมือนเดิม:

- ถ้าไฟล์เดิมมีเนื้อหาเดียวกัน ให้คืน path เดิมโดยไม่เขียนทับ
- ถ้าไฟล์เดิมมีเนื้อหาต่างกัน ให้หยุดด้วย `FileExistsError`
- การแก้ไขนี้เป็น portability fix ไม่ได้เพิ่มสิทธิ execution ให้ BBEX

สำหรับ Hospitication Semantic Router การเลือก agent ถูกจำกัดกลับเข้า
ขอบเขตที่ประกาศไว้คือ Gemini/Cast โดยใช้ concept ของ validation/verification
และ continuity/reasoning แทนคำกว้างอย่าง interpretation/context ซึ่งสามารถ
ไปตรงกับ Grok ได้

ผลที่ต้องการคือ report จาก Hospitication จะไม่หลุดไปยัง Grok เพียงเพราะ
concept overlap ขณะที่ source signal/report ยังคงไม่ถูกแก้ไขตาม boundary เดิม
