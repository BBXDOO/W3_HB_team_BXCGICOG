from mpcp.lib.pillar import Pillar
from mpcp.adapter.w3_bridge import execute_with_w3

p = Pillar("demo")

p.set_stage("A", lambda x, c: "design")
p.set_stage("D", lambda x, c: execute_with_w3(x))

print(p.run())


