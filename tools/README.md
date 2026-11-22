Name : W3 Repository Tools — เครื่องมือปฏิบัติการและตรวจสอบ\
AM Ⅲ - BUILD : เครื่องมือ CLI สำหรับตรวจสอบ ทดสอบ และสนับสนุนเวิร์กโฟลว์ของ W3\
Log time : 2026-11-22 (Asia/Bangkok; ไม่ระบุเวลา) ; ID : W3-TOOLS-README-001\
≡ Br1ra - RAMS

## Body — บทบาทและวิธีใช้งานของพื้นที่

`tools/` เป็นพื้นที่รวมสคริปต์ปฏิบัติการของ repository `W3_HB_team_BXCGICOG` สำหรับการตรวจความสมบูรณ์ของไฟล์ การตรวจ schema/metadata การทดลอง smoke test และตัวเชื่อมเวิร์กโฟลว์ เครื่องมือแต่ละตัวทำงานตามสิทธิ์และข้อจำกัดของตัวเอง; การอยู่ร่วมโฟลเดอร์ไม่ได้หมายความว่ามีสิทธิ์แก้ส่วนอื่นของระบบ

```yaml
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - docs/governance/AMS.md
  - docs/box/AMS/AMS_README.txt
  - knowledge/philosophy/corevsstructure.md
```

รายละเอียดการเรียกใช้งานและผลลัพธ์ที่บันทึกไว้เดิม:

This directory contains utility scripts for the W3_HB_team_BXCGICOG repository: file integrity checks, schema validation, and engine smoke tests.

## W3 Document Allocator

`w3_document_allocator.py` สร้าง Markdown ตาม AM Type และโครง Head/Body/Movement/Owner โดยตรวจ lineage, portable path, ชื่อไฟล์ซ้ำ และ BOX boundary ก่อนเขียน รองรับ `dry-run`, `create`, `update` และคืน artifact receipt สำหรับ Orchestration ดูคู่มือภาษาไทยที่ [W3_DOCUMENT_ALLOCATOR_TH.md](../docs/guides/W3_DOCUMENT_ALLOCATOR_TH.md)

BOX ยังคงเป็น planner-only และไม่ให้ write authority แก่เครื่องมือนี้ การเขียนจริงต้องระบุผู้อนุญาต และโหมด create จะไม่เขียนทับไฟล์เดิม

---

## smoke_test.py — Android/Termux Smoke Test Runner

A lightweight smoke test that bootstraps the W3 engine, runs for **8 seconds**, then exits automatically with code 0.  
No OS signals required — safe for Android/Termux environments.

**Run from repo root:**
```bash
python tools/smoke_test.py
```

**Termux (Android) quickstart:**
```sh
pkg update && pkg install python git
git clone https://github.com/BBXDOO/W3_HB_team_BXCGICOG.git
cd W3_HB_team_BXCGICOG
git checkout refactor/v0.2
python tools/smoke_test.py
```

**What it does:**
1. Initializes the JSONL logger (`logs/engine/runtime.log`)
2. Runs `system_check()` — prints Python version + "W3 Hybrid Engine: ONLINE"
3. Loads engine config (fallback config if `core.config_loader` is unavailable)
4. Simulates module boot for all configured modules
5. Emits heartbeat log events for **8 seconds**
6. Logs a `shutdown` event, closes the logger, and exits with code **0**

**Exit Code:**
- `0` — Smoke test passed
- `1` — Unexpected error during test

---

# File Integrity Check Tools

This directory also contains tools for checking file integrity, validating JSON schemas, and verifying module definitions in the W3_HB_team_BXCGICOG repository.

## Dependencies

- Python 3.x (pre-installed)
- jsonschema library (required for JSON schema validation)

**Install dependencies:**
```bash
pip install jsonschema
```

## Tools

### 1. file_integrity_check.py

A comprehensive file integrity checker that validates:
- Missing directories referenced in module.json files
- Missing files
- Corrupted JSON files
- Suspicious empty files (excluding .gitkeep)
- Broken symbolic links

**Usage:**
```bash
python3 tools/file_integrity_check.py
```

**Output:**
- Console output with detailed report
- Report file saved to `tools/file_integrity_report.txt`

**Exit Code:**
- `0` - No issues found
- `1` - Issues detected

### 2. validate_json_schemas.py

Validates JSON data files against their corresponding JSON Schema definitions using Python's jsonschema library. Supports all JSON Schema versions including 2020-12.

**Requirements:**
```bash
pip install jsonschema
```

**Usage:**
```bash
python3 tools/validate_json_schemas.py
```

**Features:**
- Automatically finds all .schema.json files
- Validates corresponding .json data files
- Reports validation errors with detailed messages
- Supports JSON Schema draft 2020-12 and earlier versions

**Exit Code:**
- `0` - All validations passed
- `1` - One or more validations failed

### 3. validate_modules.py

Validates all module.json files for completeness and correctness according to the W3 module schema.

**Usage:**
```bash
python3 tools/validate_modules.py
```

**Validates:**
- Required fields: name, display_name, version, owner, input, output, scope
- Optional fields: lifecycle, contact, notes, confidence_policy, pattern_weight
- Field types (arrays for input/output)
- Version format (semver)

**Exit Code:**
- `0` - All modules valid
- `1` - One or more modules invalid

### 4. validate_metadata.py

Validates metadata fields in markdown files according to W3 governance rules.

**Usage:**
```bash
python3 tools/validate_metadata.py
```

**Validates:**
- If 'approved-by' is present, 'reason' must also be present

**Exit Code:**
- `0` - All metadata valid
- `1` - Validation errors found

### 5. send_integrity_report.py

Email notification script that sends the file integrity report via email.

**Usage:**
```bash
# Set environment variables
export SENDER_EMAIL="your-email@example.com"
export RECIPIENT_EMAIL="recipient@example.com"
export SENDER_PASSWORD="your-app-password"

# Optional: Configure SMTP server (defaults to Gmail)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export USE_TLS="true"

# Run the script
python3 tools/send_integrity_report.py
```

**Features:**
- Runs integrity check automatically
- Generates both plain text and HTML formatted reports
- Sends email with comprehensive issue details
- Falls back to file output if email configuration is incomplete

**Email Configuration:**

For Gmail:
1. Enable 2-factor authentication on your Google account
2. Generate an app password at https://myaccount.google.com/apppasswords
3. Use the app password as SENDER_PASSWORD

For other SMTP servers, adjust SMTP_SERVER and SMTP_PORT accordingly.

## Report Format

The reports include:

### 📁 Missing Directories
Directories that should exist based on module.json configuration but are not present.

### 📄 Missing Files
Files that are referenced but cannot be found.

### ⚠️ Corrupted JSON Files
JSON files that fail to parse or have syntax errors.

### 🔍 Suspicious Empty Files
Files that are empty (excluding .gitkeep files which are intentionally empty).

### 🔗 Broken Symbolic Links
Symbolic links that point to non-existent targets.

## Historical status — 2025-12-12

The following results are historical evidence from the last documented W3 Full Sanity Sweep (2025-12-12), not a new verification:

✅ **All checks passed:**
- Missing Directories: 0
- Missing Files: 0
- Corrupted JSON Files: 0
- Suspicious Empty Files: 0
- Broken Symbolic Links: 0
- Valid Modules: 7/7
- JSON Schema Validations: 2/2

## Full Sanity Sweep

Run a comprehensive validation of the entire repository:

```bash
# 1. File integrity
python3 tools/file_integrity_check.py

# 2. JSON schema validation
python3 tools/validate_json_schemas.py

# 3. Module validation
python3 tools/validate_modules.py

# 4. Metadata validation
python3 tools/validate_metadata.py
```

Or use the one-liner:
```bash
python3 tools/file_integrity_check.py && \
python3 tools/validate_json_schemas.py && \
python3 tools/validate_modules.py && \
python3 tools/validate_metadata.py && \
echo "✅ Full Sanity Sweep: ALL CHECKS PASSED"
```

## Integration

These tools can be integrated into:
- CI/CD pipelines for automated checks
- Pre-commit hooks
- Scheduled cron jobs for periodic monitoring
- GitHub Actions workflows

## Example GitHub Actions Workflow

The repository includes a GitHub Actions workflow at `.github/workflows/validate-json.yml` that:
1. Validates JSON syntax for all JSON files
2. Validates JSON data files against their schemas using the Python validator

## Notes

- The checker validates against the structure defined in module.json files
- Wildcard paths (containing '*') are intentionally skipped
- .gitkeep files are excluded from empty file checks as they are intentionally empty
- The .git directory is excluded from all checks
- Python jsonschema library supports all JSON Schema versions including 2020-12

## Origin / Orchestration tool support

`origin_support.py` เป็น adapter ให้ Orchestration เรียกเครื่องมือเดิมใน tools/
เพื่อช่วยตรวจผลงาน Origin ตามขอบเขต ไม่ใช่การให้สิทธิแก้ไฟล์ทุกพาธ
ดู [คู่มือภาษาไทย](../docs/guides/ORIGIN_TOOLS_SUPPORT_TH.md) สำหรับเครื่องมือที่เชื่อมแล้ว หลักฐาน และสถานะงานค้าง


## Movement — การนำทางในพื้นที่

### M1 — รายการในโฟลเดอร์ `tools/`

| รายการ | บทบาท |
|---|---|
| [README.md](README.md) | ขอบเขตและคู่มือเครื่องมือในพื้นที่นี้ |
| [agent_sandbox/](agent_sandbox/README.md) | เอกสารและหลักฐานการตั้งค่า MPCP sandbox |
| [w3_document_allocator.py](w3_document_allocator.py) | จัดสรรและสร้างเอกสารตาม AMS พร้อมการตรวจเงื่อนไข |
| [smoke_test.py](smoke_test.py), [smoke_api_ecs_orchestration.py](smoke_api_ecs_orchestration.py) | เครื่องมือ smoke test สำหรับ engine และ API/orchestration |
| [file_integrity_check.py](file_integrity_check.py), [file_integrity_report.txt](file_integrity_report.txt), [send_integrity_report.py](send_integrity_report.py) | ตรวจสอบไฟล์ เก็บรายงาน และส่งรายงาน |
| [validate_json_schemas.py](validate_json_schemas.py), [validate_modules.py](validate_modules.py), [validate_metadata.py](validate_metadata.py), [validate_runtime_log.py](validate_runtime_log.py) | ตรวจ schema, module, metadata และ runtime log |
| [origin_support.py](origin_support.py), [origin_collaboration.py](origin_collaboration.py), [origin_cycle.py](origin_cycle.py), [orchestration_support.py](orchestration_support.py) | ตัวเชื่อมและวงจรสนับสนุน Origin/Orchestration |
| [w3_toolbox.py](w3_toolbox.py), [w3run.py](w3run.py), [w3api.py](w3api.py), [w3_agent_ci.py](w3_agent_ci.py) | จุดเรียกและสนับสนุนงานเครื่องมือ/CI ของ W3 |
| [สคริปต์อื่นใน tools/](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/tree/refactor/v0.2/tools) | เครื่องมือเฉพาะด้านอื่นในพื้นที่เดียวกัน; ตรวจหน้าที่จากโค้ดก่อนใช้งาน |

### M2 — เอกสารที่สัมพันธ์กันนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.ams-readme | [AMS README template](../docs/box/AMS/AMS_README.txt) | โครง Head / Body / Movement และ OWNER / MAKER |
| docs.ams-governance | [Architecture Mapping Standard](../docs/governance/AMS.md) | กฎ AM Type, lineage และรหัส Gradation |
| docs.core | [Core vs Structure](../knowledge/philosophy/corevsstructure.md) | ความหมายต้นทางที่ต้องตามรอยได้ |
| docs.allocator | [คู่มือ W3 Document Allocator](../docs/guides/W3_DOCUMENT_ALLOCATOR_TH.md) | วิธีใช้ตัวจัดสรรเอกสาร |
| docs.origin | [คู่มือ Origin tools support](../docs/guides/ORIGIN_TOOLS_SUPPORT_TH.md) | ขอบเขตและหลักฐานของตัวเชื่อม Origin |
| docs.workbench | [Agent Workbench](../w3_tool_store/agent_workbench/README.md) | พื้นที่สร้างเครื่องมือแยกจาก prototype; ไม่ใช่โฟลเดอร์เดียวกับ tools/ นี้ |

---

OWNER : BBX19\
MAKER : ChatGPT / Codex — ปรับรูปแบบ README ตาม AMS โดยรักษาคู่มือเดิม
