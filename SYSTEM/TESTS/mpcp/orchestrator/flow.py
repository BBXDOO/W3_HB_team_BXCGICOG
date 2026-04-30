from mpcp.orchestrator.manager import MPCPManager

m = MPCPManager()

m.add_flow("main_pipeline", [
    "design",
    "analysis",
    "deploy"
])

# run ครั้งแรก
result = m.execute()
print("FIRST RUN:", result)

# ถ้ามี WAIT → ทำต่อ
resume_result = m.resume()
print("RESUME:", resume_result)
