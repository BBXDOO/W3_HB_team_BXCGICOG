# CROLL examples

ตัวอย่างเหล่านี้เป็นข้อมูลสาธิตที่ตรวจได้ ไม่ใช่สิทธิ์ให้ execute:

- `boundary.w3-internal.json` — boundary manifest สำหรับการเชื่อม WHUB แบบ planner-only
- `paper-context.json` — context ขั้นต่ำที่ส่งให้ CROLL
- `workset.rock.json` — ผล Table-X lookup สำหรับ `PX:[1,1]`
- `dispatch-plan.jazz.json` — dispatch plan สำหรับ `PX:[2,1]`

ตรวจตัวอย่างด้วย:

```sh
python -m croll validate boundary croll/examples/boundary.w3-internal.json
python -m croll validate workset croll/examples/workset.rock.json
python -m croll validate plan croll/examples/dispatch-plan.jazz.json
```
