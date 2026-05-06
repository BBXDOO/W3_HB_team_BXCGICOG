W3Lgu — Operational Manual (v2)
PART 1: USAGE

W3Lgu = Language Layer ของ W3

หลักการ:
- ใช้ภาษาเดียว (One Language)
- ทุก Input / Output ต้องเป็น MPCP/W3Lgu
- ใช้ KEY:VALUE

ตัวอย่าง:
TASK:build,MODE:fast
STATE:done,COLOR:Green,SYM:✓
STATE:run,COLOR:Blue,SYM:⟳
STATE:block,COLOR:Red,SYM:✕

Flow:
INPUT → MPCP → Modew → OUTPUT → MPCP


PART 2: EVENT / SYSTEM BEHAVIOR

Flow จริงของระบบ:

1. INPUT
→ แปลงเป็น W3Lgu

2. PROCESS
→ Modew ทำงาน (⟳)

3. STATE OBSERVE (TUF)
0 = fail
0.5 = uncertain
1 = true

4. DETECT (FBD)
→ หา First Deviation

5. ADAPT (WHB)
IF ... THEN ...

6. RENDER (PRX)
▲ RED = FORCE / CRITICAL
● YELLOW = UNCERTAIN / CHECK
■ GREEN = STABLE / RESULT
◆ BLUE = EXTERNAL

ตัวอย่าง:
STATE:0.5,COLOR:Yellow,SYM:●
STATE:1,COLOR:Green,SYM:■
STATE:0,COLOR:Red,SYM:▲


CORE LAW

- One Language Only
- Process must complete
- State ≠ Decision
- Failure = Boundary
- Truth by Result



