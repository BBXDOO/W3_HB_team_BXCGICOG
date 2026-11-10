[ต้นฉบับ](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/repo_events/orchestration_support/README.md)

# หลักฐานการสนับสนุนการประสานงาน

AM: III — กระบวนการ | กลุ่ม: OBSERVE | ผู้รับผิดชอบ: BBX19

เครื่องมือช่วยงานเก็บผลตรวจจริงไว้ที่นี่ ไฟล์ UUID เป็นรายงาน input hash / findings ของ tools adapters; `*-validation.json` เป็นบันทึกการตรวจโค้ดและเอกสารระหว่างส่งมอบ ไม่ใช่การอนุมัติงานของมนุษย์

Source, input และขอบเขตการตรวจระบุใน receipt ผลผ่านยืนยันเฉพาะเกณฑ์ที่ตรวจ เช่น พาธ metadata และ syntax ไม่รับรองความหมายหรือคุณภาพของงานทั้งหมด Saved task และผลการช่วยในวงจรเก็บที่ `repo_events/runtime_circuit/` ส่วน Origin executor เก็บ event ของตัวเองที่ `repo_events/origin_agents/`
