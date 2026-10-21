---
request_id: RQ-LRC2-LOG-ANALYSIS-001
request_type: runtime_circuit
task_keyword: log_analysis
target_module: LRC2
requester: BBX19
final_signoff_required: true
priority: NORMAL
---

# วิเคราะห์ประวัติจริงผ่าน LRC2 → Gemini → Human Review

## บริบทและเป้าหมาย

เริ่มสะสมความเข้าใจประวัติของ W3 จากข้อมูลที่มีอยู่จริง โดยใช้
`core/memory/memory_store.json` เป็นข้อมูลต้นทาง ไม่สร้างเหตุการณ์สมมุติเพื่อเติมผล

## งานของ LRC2

- แยกประเภทสถานะที่พบ โดยเก็บประเภทที่ยังไม่ทราบไว้ชัดเจน
- แบ่งกลุ่มตามโมดูลและประเภทงาน
- หา error signature ที่เกิดซ้ำพร้อมอ้างอิงรายการที่พบ
- คำนวณการสะสมความเสี่ยงจากรายการล่าสุด 20 รายการต่อกลุ่ม
- แสดงอัตราสำเร็จที่บันทึกไว้ พร้อมจำนวนตัวอย่างที่ใช้
- ประมาณแบบ historical frequency เฉพาะกลุ่มที่มีผลสำเร็จ/ล้มเหลวอย่างน้อย 20 ตัวอย่าง
  ระบุเงื่อนไขความเทียบเคียงและช่วง Wilson 95% ไม่อ้างว่าผ่านการพิสูจน์พยากรณ์อนาคต
- เขียนรายงานผลจริงใน `modules/LRC2/reports/log_analysis/`

## งานของ Gemini

อ่านไฟล์รายงานและ snapshot ต้นทาง ตรวจ hash จำนวนรายการ การอ้างอิง trace
และตรวจผลคำนวณซ้ำจากข้อมูลต้นทาง หากไม่ตรงต้องไม่ผ่าน

## การจบงาน

เก็บแหล่งข้อมูลและผลแต่ละขั้นไว้ตรวจสอบ หยุดที่ `WAITING_HUMAN`
เพื่อให้ BBX19 ตรวจผลก่อนปิดใบงาน ไม่ถือว่าการมีไฟล์อย่างเดียวทำให้ใบงานจบ

```w3-circuit
{
  "stages": [
    {
      "task": "log_analysis",
      "module": "LRC2",
      "request": {
        "intent": "วิเคราะห์ประวัติ W3 ตามงานและเกณฑ์ในใบงานนี้",
        "payload": {
          "source_file": "core/memory/memory_store.json",
          "min_samples": 20,
          "window_size": 20
        }
      }
    },
    {
      "task": "verify",
      "module": "Gemini",
      "request": {
        "intent": "ตรวจรายงาน LRC2 เทียบกับ snapshot ของข้อมูลต้นทาง"
      }
    }
  ]
}
```
