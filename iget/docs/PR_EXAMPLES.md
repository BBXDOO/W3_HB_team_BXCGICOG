# PR Examples

ตัวอย่าง Pull Request และผลที่ IGET ควรตีความ

## Example A — Docs Only PR

### สถานการณ์

```text
2 files
20 lines
เฉพาะ .md / docs
```

### ลอจิกที่เกี่ยวข้อง

- classify เป็น docs
- mode = docs_only
- มี bonus docs-only
- ความเสี่ยงต่ำ

### สิ่งที่คาดหวัง

```text
Result: Green
```

### ข้อสังเกต

ยังควรอ่านเนื้อหา docs ว่าถูกต้องหรือไม่ แต่ความเสี่ยง runtime ต่ำ

---

## Example B — Code Without Test

### สถานการณ์

```text
5 files
300 lines
มี code change
ไม่มี test
```

### ลอจิกที่เกี่ยวข้อง

- classify code files
- test_count = 0
- หักคะแนน missing test
- อาจยังไม่ถึง Red ถ้า PR ไม่ใหญ่มาก

### สิ่งที่คาดหวัง

```text
Result: Yellow
```

### ข้อสังเกต

ต้อง review logic มากขึ้น หรือขอ test เพิ่มเมื่อเหมาะสม

---

## Example C — Large Risk PR

### สถานการณ์

```text
18 files
1200 lines
มี workflow change
พบ secret keyword หรือ risky filename
```

### ลอจิกที่เกี่ยวข้อง

- total_files > large threshold
- total_changes > large threshold
- workflow_count > 0
- risky_count > 0
- semantic_state มีแนวโน้ม critical

### สิ่งที่คาดหวัง

```text
Result: Red
```

### ข้อสังเกต

ควรหยุดก่อน merge และตรวจ security / workflow / permission / token path ให้ละเอียด

---

## การนำไปใช้

ตัวอย่างเหล่านี้ใช้เป็น baseline สำหรับอ่านผล IGET ว่าเหตุผลสีและคะแนนสัมพันธ์กับสถานการณ์จริงอย่างไร
