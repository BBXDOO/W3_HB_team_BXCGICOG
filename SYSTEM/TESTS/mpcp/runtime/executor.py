from mpcp.lib.pillar import Pillar
from mpcp.adapter.w3_bridge import execute_with_w3
from mpcp.kernel.contract import MPCPContract


def build_pillar(task):
    p = Pillar("main")

    # Stage A: define task
    p.set_stage("A", lambda x, c: task)

    # Stage D: execution via W3
    p.set_stage("D", lambda x, c: execute_with_w3(x))

    return p


def run(task):
    MPCPContract.validate_input(task)

    pillar = build_pillar(task)
    result = pillar.run()

    MPCPContract.validate_output(result)

    return result
