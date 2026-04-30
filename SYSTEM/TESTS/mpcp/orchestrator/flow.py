from mpcp.orchestrator.manager import MPCPManager

m = MPCPManager()

m.add_flow("main_pipeline", [
    "design",
    "analysis",
    "deploy"
])

print(m.execute())
