"""Run the two catalogued CROLL suites on a Git snapshot via Workbench isolation."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

from flow import BENCH, croll_catalog
from serve import APP, ROOT, Repo

RUN = """
from pathlib import Path
import subprocess
import sys
from w3_tool_store.agent_workbench.tools.system_inspection.runner import copy_source
source, target = map(Path, sys.argv[1:3])
copy_source(source, target)
raise SystemExit(subprocess.call([sys.executable, "-I", "-c",
    "import os, runpy, sys; sys.path.insert(0, os.getcwd()); runpy.run_module('unittest', run_name='__main__')",
    "-v", *sys.argv[3:]], cwd=target))
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--ref", default="HEAD")
    args = parser.parse_args()
    repo = Repo(args.root.resolve(), args.ref)
    _, (_, _, paths) = croll_catalog(repo.read(BENCH))
    suites = [path.removesuffix(".py").replace("/", ".") for path in paths]
    if suites != ["croll.test_contracts", "croll.test_cross_l_dispatcher"]:
        parser.error("ชุดตรวจ CROLL เปลี่ยน ต้องตรวจขอบเขตก่อนรัน")
    with tempfile.TemporaryDirectory(prefix="w3console-") as directory:
        area = Path(directory)
        archive = area / "revision.tar"
        snapshot = area / "source"
        snapshot.mkdir()
        subprocess.run(["git", "-C", str(repo.root), "archive", "--format=tar",
                        "-o", str(archive), repo.revision], check=True, timeout=30)
        with tarfile.open(archive) as source:
            members = (member for member in source if member.isfile() or member.isdir())
            source.extractall(snapshot, members=members, filter="data")
        try:
            run = subprocess.run([sys.executable, "-I", "-c",
                                  "import sys; sys.path.insert(0, sys.argv[1]);\n" + RUN,
                                  str(snapshot), str(area / "sandbox"), *suites],
                                 cwd=snapshot, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 encoding="utf-8", errors="replace", timeout=180)
            status = "PASS" if run.returncode == 0 else "FAIL"
            output = run.stdout
            exit_code = run.returncode
        except subprocess.TimeoutExpired as error:
            status, exit_code = "TIMEOUT", None
            output = (error.stdout or b"").decode("utf-8", "replace")
    result = {"kind": "w3console-croll-run/v1", "revision": repo.revision,
              "status": status, "exit_code": exit_code, "suites": suites,
              "time": datetime.now(timezone.utc).isoformat(), "output": output[-32000:]}
    destination = APP / ".local" / "run.json"
    destination.parent.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent,
                                     delete=False) as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        temporary = Path(file.name)
    temporary.replace(destination)
    print(output)
    print(f"{status} · {destination}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
