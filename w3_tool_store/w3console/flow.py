"""Source-backed map of the CROLL inspection lane."""
import ast
import json
from pathlib import PurePosixPath
import re

import yaml

WORKFLOW = ".github/workflows/main-agent-readiness.yml"
BENCH_TEST = "tests/test_system_inspection.py"
BENCH = "w3_tool_store/agent_workbench/tools/system_inspection/runner.py"
CONTRACT_TEST = "croll/test_contracts.py"
CONTRACT = "croll/contracts.py"
SCHEMA = "croll/schema/dispatch-plan.schema.json"


def source(path, line):
    return {"path": path, "line": line}


def python_line(text, kind, name):
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, kind):
            if isinstance(node, ast.Call):
                symbol = getattr(node.func, "id", getattr(node.func, "attr", None))
            else:
                symbol = node.name
            if symbol == name:
                return node.lineno
    raise ValueError(f"ไม่พบ {name}")


def croll_catalog(text):
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "CATALOG" for target in node.targets
        ) and isinstance(node.value, ast.Tuple):
            for item in node.value.elts:
                row = ast.literal_eval(item)
                if row[0] == "CROLL":
                    return item.lineno, row
    raise ValueError("ไม่พบ CROLL ใน CATALOG")


def workflow_line(text):
    model = yaml.compose(text, Loader=yaml.SafeLoader)
    job = yaml_key(yaml_key(model, "jobs"), "verify-main-agents")
    for step in yaml_key(job, "steps").value:
        node = yaml_key(step, "run", required=False)
        if not isinstance(node, yaml.ScalarNode):
            continue
        for offset, command in enumerate(node.value.splitlines()):
            if re.fullmatch(r"python -m pytest tests/test_system_inspection\.py(?:\s+.*)?",
                            command.strip()):
                return node.start_mark.line + (2 if node.style in ("|", ">") else 1) + offset
    raise ValueError("ไม่พบคำสั่งตรวจ Workbench ใน workflow")


def yaml_key(node, key, *, required=True):
    if isinstance(node, yaml.MappingNode):
        for name, value in node.value:
            if isinstance(name, yaml.ScalarNode) and name.value == key:
                return value
    if required:
        raise ValueError(f"ไม่พบ {key} ใน workflow")
    return None


def build_flow(repo):
    """Resolve anchors from the chosen revision; keep missing links visible."""
    rows = []

    def step(label, relation, path, locate):
        try:
            line = locate(repo.read(path))
            rows.append({"label": label, "relation": relation, "source": source(path, line)})
        except (KeyError, ValueError, SyntaxError, OSError, StopIteration, TypeError, AttributeError, yaml.YAMLError) as error:
            rows.append({"label": label, "relation": relation, "unknown": str(error) or "หาแหล่งอ้างอิงไม่พบ"})

    step("Workflow", "คำสั่ง CI เรียกชุดทดสอบของ Workbench", WORKFLOW, workflow_line)
    step("ชุดตรวจ Workbench", "ในชุดทดสอบมีการเรียก run_suite", BENCH_TEST,
         lambda text: python_line(text, ast.Call, "run_suite"))

    def catalog_anchor(text):
        line, (_, entry, suites) = croll_catalog(text)
        if entry != CONTRACT or CONTRACT_TEST not in suites:
            raise ValueError("รายการ CROLL ใน CATALOG เปลี่ยนไป")
        return line

    step("รายการ CROLL", "Workbench ระบุไฟล์เข้าและชุดตรวจของ CROLL", BENCH, catalog_anchor)
    step("ตรวจ schema", "เทสต์อ่าน schema และตรวจว่าไฟล์อ้างอิงมีอยู่", CONTRACT_TEST,
         lambda text: python_line(text, ast.FunctionDef, "test_dispatch_schema_reference_exists"))
    step("ตรวจข้อมูลตัวอย่าง", "เทสต์เรียกตัวตรวจ Python กับ dispatch plan ตัวอย่าง", CONTRACT_TEST,
         lambda text: python_line(text, ast.Call, "validate_dispatch_plan"))
    step("ตัวตรวจ Python", "ตรวจเงื่อนไขของ dispatch plan", CONTRACT,
         lambda text: python_line(text, ast.FunctionDef, "validate_dispatch_plan"))

    def schema_anchor(text):
        model = json.loads(text)
        reference = model["properties"]["workset"]["$ref"]
        if reference != "workset.schema.json":
            raise ValueError("workset อ้างถึง schema อื่น")
        repo.read(str(PurePosixPath(SCHEMA).parent / reference))
        return next(i for i, line in enumerate(text.splitlines(), 1)
                    if '"$ref"' in line and reference in line)

    step("JSON Schema", "dispatch plan ประกาศ $ref ไปยัง workset.schema.json", SCHEMA, schema_anchor)
    return rows
