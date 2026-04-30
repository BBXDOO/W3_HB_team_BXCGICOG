from mpcp.kernel.pillar import Pillar
from mpcp.adapter.w3_bridge import execute_with_w3


def execute(task):
    pillar = Pillar("mpcp-runtime")

    pillar.set_stage("A", lambda x, c: task)
    pillar.set_stage("D", lambda x, c: execute_with_w3(x))

    return pillar.run()


if __name__ == "__main__":
    print(execute("design"))


