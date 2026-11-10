---
request_id: YOUR_REQUEST_ID
request_type: runtime_circuit
task_keyword: log_analysis
target_module: LRC2
requester: BBX19
priority: NORMAL
final_signoff_required: true
desired_outcome: ระบุผลที่ต้องการให้สังเกตและตรวจรับได้
---
# ใบมอบหมายงาน

เจตนา: ระบุว่าอยากให้เกิดอะไรและเพราะอะไร
ขอบเขต: ระบุข้อมูล/พื้นที่ที่มอบหมาย
ข้อจำกัด: ระบุสิ่งที่ต้องรักษา
ผลที่ต้องส่ง: ระบุผลงานและเกณฑ์ตรวจรับ

ตัวอย่างด้านล่างเป็นโฟลว log_analysis ที่มี executor จริงอยู่แล้ว
แก้ข้อมูลต้นทางให้ตรงงาน หากเป็นงานอื่นให้เลือก workflow หรือ stages
ที่มีตัวทำงานและตัวตรวจผลรองรับ ห้ามเปลี่ยนเพียงชื่อแล้วอ้างว่าทำได้

```w3-circuit
{
  "workflow": "log_analysis",
  "input": {
    "payload": {
      "source_file": "core/memory/memory_store.json",
      "min_samples": 20,
      "window_size": 20
    }
  }
}
```
