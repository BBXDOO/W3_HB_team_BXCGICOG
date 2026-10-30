Name : Agent Workbench — Tools\
AM Ⅱ - BUILD : การจัดพื้นที่สำหรับโครงการเครื่องมือที่พัฒนาแยก\
Log time : 2026-10-24 (Asia/Bangkok; ไม่ระบุเวลา) ; ID : W3-AWB-TOOLS-README-001\
Reserved : ยังไม่เปิดเผยตามต้นแบบ AMS

## Body — บทบาทของพื้นที่

โฟลเดอร์นี้รองรับโครงการเครื่องมือที่เอเจนท์ใช้ทำงาน โดยแยกแต่ละเครื่องมือออกจาก prototype ต้นทางและจากข้อมูลของผู้ใช้เครื่องมือ

**สถานะ: มี REA MCP probe, Battle flow probe และ Android WebView layout probe แล้ว ความพร้อมและหลักฐานแยกตามเครื่องมือ ยังไม่มีสำเนา REA core ที่นำมาปรับเป็นเครื่องมือใหม่ในโฟลเดอร์นี้**

```yaml
AM_TYPE: II
ROLE: ADAPTATION
DERIVED_FROM:
  - knowledge/philosophy/corevsstructure.md
  - w3_tool_store/agent_workbench/README.md
```

เมื่อเพิ่มเครื่องมือ ให้สร้างโฟลเดอร์ของเครื่องมือนั้นพร้อม README แบบ AMS อธิบายหน้าที่ วิธีเรียก ข้อมูลเข้า/ออก dependency ผลกระทบ วิธีตรวจผล และสถานะที่มีหลักฐานจริง README ของโค้ดหรือกระบวนการปฏิบัติงานให้ระบุ AM:III ตามเนื้อหา

หากคัดลอกโค้ดจาก xrea ให้เก็บที่มา เวอร์ชันหรือ commit รายการที่คัดลอก การปรับแก้ และ license/copyright notice ไว้กับเครื่องมือปลายทาง การเป็นเจ้าของโครงการ W3 ไม่ได้เปลี่ยนผู้พัฒนาต้นฉบับ

## Movement — การนำทางในพื้นที่

### M1 — สิ่งที่มีอยู่ในโฟลเดอร์นี้

| รายการ | หน้าที่ |
|---|---|
| [README.md](README.md) | ขอบเขตของพื้นที่ tools |
| [rea_mcp_probe/](rea_mcp_probe/README.md) | เรียก REA MCP จริง เก็บผลและข้อจำกัด; การวิเคราะห์รอบแรกติด host process ownership |
| [battle_flow_probe/](battle_flow_probe/README.md) | ทดลอง logic สนาม มานา การ์ด เฟส และเทิร์นด้วย Node; ไม่ใช่ผลทดสอบ UI/APK |
| [android_webview_probe/](android_webview_probe/README.md) | ตรวจ layout ด้วย Chromium เมื่อมี dependency; ยังไม่ใช่ Android WebView/ColorOS จริง |
| [android_apk_probe/](android_apk_probe/README.md) | ตรวจลายเซ็นและ manifest ของ APK จริงด้วย Android SDK; ไม่ใช่ผลรันบนเครื่อง |
| [system_inspection/](system_inspection/README.md) | ตัวเชื่อม Orchestration ตรวจชุดจริง 7 ระบบ แยกเรื่องที่สะดุดแล้วเดินระบบอิสระถัดไป |

### M2 — เอกสารอ้างอิงนอกพื้นที่

- docs.parent : [Agent Workbench](../README.md)
- docs.core : [Core vs Structure](../../../knowledge/philosophy/corevsstructure.md)
- docs.prototype : [xrea](../../xrea/README.md)
- docs.sandbox : [คู่มือ MPCP sandbox ที่อยู่ในพาธเดิม](../../../tools/agent_sandbox/README.md)

---

OWNER : BBX19\
MAKER : ChatGPT / Codex
