# OPPO Android probe — Blueprint + File.void

AM Ⅲ - BUILD · OWNER: BBX19 · MAKER: ChatGPT/Codex · 2026-10-27

## Body

คำขอทดลองใน `agent_workbench` ที่ใช้ MPCP Blueprint แบบ `TARGET:local` สร้างโครงพื้นที่ แล้วใช้ Paper Runtime เรียก `FileVoidTextModew` เพื่อสร้างข้อความโปรไฟล์เครื่องและแผน Playtest ผ่าน File.void persistence handoff กับ external writer ของ host

Blueprint เป็นข้อมูลประกาศ ไม่เรียกเครื่องมือเอง `--execute` ให้สิทธิ์เฉพาะ local sandbox ที่ผู้รันเลือก ไม่ได้อนุมัติ deployment หรือแตะ APK

ข้อมูล OPPO มาจากบทสนทนา ไม่อ่านค่าจริงจากอุปกรณ์ ค่า viewport เป็นสมมุติฐาน; การทดสอบ logic กับ browser probe และการทดสอบ WebView บนเครื่องจริงเป็นคนละชั้น

## Movement

จาก root รีโป้ ใช้พาธผลลัพธ์ใหม่ใน `w3_tool_store/agent_workbench/runs/` แต่ละครั้ง:

```sh
python tools/mpcp_sandbox.py --request w3_tool_store/agent_workbench/profiles/oppo_android_probe/blueprint_request.json --output w3_tool_store/agent_workbench/runs/oppo-setup --execute
python tools/mpcp_papers.py --request w3_tool_store/agent_workbench/profiles/oppo_android_probe/paper_pack.json --output w3_tool_store/agent_workbench/runs/oppo-papers --execute
```

อ่าน `oppo-setup/result.json`, `oppo-setup/workspace/artifacts/setup.json`, `oppo-papers/result.json` และ `oppo-papers/artifacts/*.md` ส่วนการทดสอบหน้าจอใช้ [android_webview_probe](../../tools/android_webview_probe/README.md) เมื่อมี Chromium

ขอบเขต: ไม่มี Android emulator ที่ติดตั้งใน host นี้, ไม่มีการรัน APK/ColorOS, ไม่มีข้อมูลผู้ใช้หรือการเชื่อมเครื่องจริง ผล SUCCESS หมายถึง setup/เอกสารสอง Paper ที่ verifier ตรวจได้เท่านั้น
