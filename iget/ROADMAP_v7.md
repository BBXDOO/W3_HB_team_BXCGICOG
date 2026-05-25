# IGET Roadmap v7.0 (Ontology-Aligned, Proof-Ready)

## เป้าหมาย

- รองรับ semantic trace, proof, recovery, self-introspection
- สอดคล้องกับมาตรฐาน MPCP และแนวทาง semantic governance
- อัปเกรด documentation และ test suite ให้ง่ายต่อ onboarding/extension

## ขั้นตอน/ฟีเจอร์ใหม่

1. [ ] Annotate semantic state และ causal proof ในทุกโมดูลหลัก
2. [ ] เพิ่ม interface รับ/คืน MPCP claim/result/trace
3. [ ] โครงสร้าง recovery/resilience: checkpoint, rollback, retry, error_proof
4. [ ] Test suite ครอบคลุม “semantic event”, replay/fault lineage
5. [ ] Document class/method พร้อม tag ontology/ความหมายทุกหน่วย (docstring, README)
6. [ ] CI/checklist enforce semantic DoD

## ตัวอย่าง DoD (Definition of Done)

- ทุก event + output ต้องมี proof entry + semantic annotation
- ทุก error ต้องมี recovery/fail-safe handler
- README, Usage, Docstring update
