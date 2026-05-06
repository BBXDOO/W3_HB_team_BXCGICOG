W3Lgu — Operational Manual
PART 1: USAGE

W3Lgu คือ language layer กลางของระบบ W3

หลักการ:
- ทุก Input / Output ต้องเป็นรูปแบบ W3Lgu
- ใช้สำหรับ communication ระหว่าง Node และ Module

รูปแบบพื้นฐาน:
KEY:VALUE

ตัวอย่าง:
TASK:build,MODE:fast
STATE:done,COLOR:Green,SYM:✓

Flow การใช้งาน:
1. รับ input → แปลงเป็น W3Lgu
2. ส่งเข้า MPCP (Modew execution)
3. รับ output → ส่งออกในรูป W3Lgu

กฎสำคัญ:
- ใช้ภาษาเดียวทั้งระบบ
- ห้ามส่ง raw data ข้าม layer
- ห้ามใช้หลาย syntax ปะปน


PART 2: EVENT / SYSTEM BEHAVIOR

เมื่อเกิดเหตุการณ์ในระบบ:

1. INPUT
→ Event ถูกแปลงเป็น W3Lgu

2. PROCESS
→ Modew ทำงาน (ไม่มี interrupt)

3. STATE OBSERVE
→ TUF บันทึกสถานะ (0 / 0.5 / 1)

4. DETECT FAILURE
→ FBD ตรวจจับจุด deviation

5. ADAPT
→ WHB สร้างกฎ IF → THEN

6. RENDER
→ PRX แสดงผล (สี + สัญลักษณ์)

ตัวอย่าง:
STATE:0.5 → COLOR:Yellow → SYMBOL:●

หมายเหตุ:
- STATE ใช้สำหรับเรียนรู้ ไม่ใช่ตัดสินใจ
- ทุก action ต้องตอบได้ว่า “ทำไม”


CORE LAW

- One Language Only
- Truth by Result
- Process must complete
- Failure = Boundary
- Structure > Everything



