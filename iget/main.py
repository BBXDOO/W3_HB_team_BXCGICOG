from iget_engine import PRFlow
from iget_ui import render

def run():
    flow = PRFlow(pr_id="123")

    flow.add_node("A", "commit")
    flow.add_node("B", "PR opened")
    flow.add_node("C", "check")
    flow.add_node("D", "review")
    flow.add_node("E", "decision")
    flow.add_node("F", "merge")

    flow.auto_run()

    data = flow.export()
    render(data)

if __name__ == "__main__":
    run()
