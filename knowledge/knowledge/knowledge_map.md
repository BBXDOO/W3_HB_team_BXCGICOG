
---

# ⚡️ Knowledge Map Workflow (Manual/Script-based, รองรับต่อขยายทุกยุค)

## 1. แนวคิดการ Mapping

- **Nodes**: โฟลเดอร์/module (protocol/…, agent/, Cast/, Hospitals/, test/), doc (README, .md, blueprint), test suite, integration
- **Edges**: ความสัมพันธ์ (import path, from-import, includes, markdown [link], cross-ref, health check, test coverage link)
- **Cycle highlight**: ถ้า detect ว่ามี dependency วนซ้ำ (cycle) จะติ๊ก node นั้นให้ refactor ได้ภายหลัง
- **รูปแบบ output**:  
    - Table summary (nodes ↔ edges/ref)
    - Mermaid graph (สำหรับ visualize หรือฝัง markdown)
    - Annotated markdown knowledge_book.md

---

## 2. ตัวอย่าง script/manual audit (Python + bash)

### (A) Bash — สแกน cross-ref/import/reference
```bash
# สแกน import และ includes
grep -R --include="*.py" "import " . > imports.log
grep -R --include="*.py" "from " . >> imports.log

# สแกน markdown/doc link/cross-ref
grep -R --include="*.md" -e '\[.*\](.*)' . > mdlinks.log

# สแกน health/hospital reference
grep -R "hospital" . > hospital.log
grep -R "Hospitication" . >> hospital.log

# รวมเป็น knowledge map RAW
cat imports.log mdlinks.log hospital.log > knowledge_raw_map.log
```

### (B) Python — พาร์สความสัมพันธ์ (pseudo/simple)
```python
from collections import defaultdict
import re, glob

nodes = defaultdict(set)

# Parse import relationships
for pyfile in glob.glob('**/*.py', recursive=True):
    for line in open(pyfile):
        if line.startswith("import ") or line.startswith("from "):
            # crude parser: extract module
            mod = line.split()[1].split('.')[0]
            nodes[pyfile].add(mod)

# Parse markdown links
for mdfile in glob.glob('**/*.md', recursive=True):
    for line in open(mdfile):
        for m in re.finditer(r"\[.*\]\(([^)]+)\)", line):
            ref = m.group(1)
            nodes[mdfile].add(ref)

# เอา nodes (filename) ↔ edges (import/doc link/health)
for k,v in nodes.items():
    print(f"{k}:")
    for other in v:
        print(f"  → {other}")
```

---

## 3. ผลลัพธ์และคู่มือการใช้งานทีม

- นำ RAW knowledge map ที่ได้ไปวาดเป็น **mermaid graph** เช่น
    ```mermaid
    graph TD
      protocol/mpcp --> protocol/w3lgu
      Cast/context/session_summary.md --> protocol/mpcp
      README.md --> protocol/Files.void
      test/suite_X.py --> agent/Cast
      agent/Cast --> hospital/
    ```
- ทำเป็น summary table  
    | Node | Imports/Links to |  
    |------|------------------|  
    | protocol/mpcp | protocol/w3lgu, agent/Cast |  
    | Cast/context/session_summary.md | hospital/ |  
    | ... | ... |  

- อัปเดต knowledge_book.md (หรือ README) ให้ระบุกฏ network/map วันไหนใครดูต่อก็ follow ได้

---

## 4. เครื่องมือฟรีอื่น ๆ ที่รองรับ mapping/codebase graph
- **pydeps**: วาด python dependency graph (pip install pydeps)
    - ตัวอย่าง:  
    ```sh
    pydeps protocol/ --max-bacon=2 --show-deps
    ```
- **graphviz/mermaid**: วาดไดอะแกรม
- **pytest-cov**: สแกน test coverage/health network

---

## 5. ขยาย usage ในอนาคต
- ทีมสามารถนำ workflow นี้ไปรวมกับ CI หรือ pre-merge review
- ถ้ามี coding agent/automation ในอนาคต, script นี้ plug-in ได้ทันที

---

