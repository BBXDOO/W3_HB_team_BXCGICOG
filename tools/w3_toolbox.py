#!/usr/bin/env python3
import json, sys, csv
from pathlib import Path
from datetime import datetime

ROOT = Path("w3_tool_store")
NOTES = ROOT / "notes"
SHEETS = ROOT / "sheets"
COMPILED = ROOT / "compiled"
REFS = ROOT / "refs"

for p in [NOTES, SHEETS, COMPILED, REFS]:
    p.mkdir(parents=True, exist_ok=True)

def now():
    return datetime.now().isoformat(timespec="seconds")

def out(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))

def save_note(key, title, body):
    path = NOTES / f"{key}.md"
    text = f"# {title}\n\ncreated: {now()}\nkey: {key}\n\n---\n\n{body}\n"
    path.write_text(text, encoding="utf-8")
    return {"ok": True, "type": "note", "path": str(path)}

def save_sheet(key, rows):
    path = SHEETS / f"{key}.csv"
    if isinstance(rows, str):
        rows = json.loads(rows)
    if not rows:
        rows = [{"empty": ""}]
    fields = sorted({k for r in rows for k in r.keys()})
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return {"ok": True, "type": "sheet", "path": str(path), "rows": len(rows)}

def compile_doc(key, sources):
    if isinstance(sources, str):
        sources = sources.split(",")
    parts = []
    for src in sources:
        src = src.strip()
        for base in [NOTES, COMPILED, REFS]:
            p = base / src
            if p.exists():
                parts.append(f"\n\n<!-- SOURCE: {p} -->\n\n" + p.read_text(encoding="utf-8"))
                break
        else:
            p = NOTES / f"{src}.md"
            if p.exists():
                parts.append(f"\n\n<!-- SOURCE: {p} -->\n\n" + p.read_text(encoding="utf-8"))
            else:
                parts.append(f"\n\n<!-- MISSING: {src} -->\n")
    path = COMPILED / f"{key}.md"
    path.write_text(f"# COMPILED: {key}\n\ncreated: {now()}\n" + "".join(parts), encoding="utf-8")
    return {"ok": True, "type": "compiled", "path": str(path)}

def list_all():
    return {
        "notes": sorted(p.name for p in NOTES.glob("*")),
        "sheets": sorted(p.name for p in SHEETS.glob("*")),
        "compiled": sorted(p.name for p in COMPILED.glob("*")),
        "refs": sorted(p.name for p in REFS.glob("*")),
    }

def read_item(name):
    for base in [NOTES, SHEETS, COMPILED, REFS]:
        p = base / name
        if p.exists():
            return {"ok": True, "path": str(p), "content": p.read_text(encoding="utf-8")}
    return {"ok": False, "error": "not found", "name": name}

def selftest():
    a = save_note("AI_SELF_REFERENCE", "AI Self Reference", "อ่านของจริงก่อนตอบ\nไม่สร้างของเล่นก่อนตรวจ repo\nใช้ tool นี้แทนการเขียนซ้ำ")
    b = save_note("USER_COPY", "User Copy", "เครื่องมือกลางสำหรับเก็บ note / sheet / compiled document")
    c = save_sheet("tool_map", [
        {"tool": "save_note", "use": "เก็บโน๊ต"},
        {"tool": "save_sheet", "use": "เก็บตาราง"},
        {"tool": "compile_doc", "use": "รวมเอกสาร"},
        {"tool": "list", "use": "ดูของที่มี"},
    ])
    d = compile_doc("BOOTSTRAP_REFERENCE", ["AI_SELF_REFERENCE", "USER_COPY"])
    return {"ok": True, "selftest": [a, b, c, d]}

def main():
    if len(sys.argv) < 2:
        out({"usage": [
            "python tools/w3_toolbox.py selftest",
            "python tools/w3_toolbox.py list",
            "python tools/w3_toolbox.py note KEY TITLE BODY",
            "python tools/w3_toolbox.py sheet KEY '[{\"a\":\"b\"}]'",
            "python tools/w3_toolbox.py compile KEY source1,source2",
            "python tools/w3_toolbox.py read FILE.md"
        ]})
        return

    cmd = sys.argv[1]

    if cmd == "selftest":
        out(selftest())
    elif cmd == "list":
        out(list_all())
    elif cmd == "note":
        out(save_note(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:])))
    elif cmd == "sheet":
        out(save_sheet(sys.argv[2], " ".join(sys.argv[3:])))
    elif cmd == "compile":
        out(compile_doc(sys.argv[2], sys.argv[3]))
    elif cmd == "read":
        out(read_item(sys.argv[2]))
    else:
        out({"ok": False, "error": "unknown command", "cmd": cmd})

if __name__ == "__main__":
    main()
