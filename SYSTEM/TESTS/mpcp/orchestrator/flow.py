from mpcp.orchestrator.manager import MPCPManager

m = MPCPManager()

# Steps must use MPCP format (KEY:VALUE) so that executor.run() can parse them.
m.add_flow("main_pipeline", [
    "TASK:design",
    "TASK:analysis",
    "TASK:deploy"
])

print(m.execute())
