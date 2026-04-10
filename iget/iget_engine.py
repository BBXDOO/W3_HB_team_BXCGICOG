IMPACT_MAP = {
    "green": "ไม่มีผลกระทบ",
    "yellow": "มีผลกระทบบางส่วน",
    "red": "เสี่ยงต่อระบบ"
}

SUCCESS_RATE = {
    "green": 0.87,
    "yellow": 0.65,
    "red": 0.25
}

class PRFlow:
    def __init__(self, pr_id="local"):
        self.pr_id = pr_id
        self.nodes = []
        self.log = []
        self.progress = 0

    def add_node(self, node_id, node_type):
        self.nodes.append({
            "id": node_id,
            "type": node_type,
            "state": None,
            "done": False
        })

    def update_progress(self):
        done = len([n for n in self.nodes if n["done"]])
        self.progress = (done / len(self.nodes)) * 100 if self.nodes else 0

    def simulate(self):
        return SUCCESS_RATE

    def recommend(self, sim):
        return max(sim, key=sim.get)

    def auto_run(self, risk_state="green"):
        for node in self.nodes:
            if node["id"] in ["C", "E"]:
                state = risk_state
                node["state"] = state
                node["done"] = True

                self.log.append({
                    "node": node["id"],
                    "state": state,
                    "impact": IMPACT_MAP[state]
                })
            else:
                node["state"] = "green"
                node["done"] = True

            self.update_progress()

    def build_markdown(self, metrics, score):
        emoji = {
            "green": "🟢",
            "yellow": "🟡",
            "red": "🔴"
        }

        states = [n["state"] for n in self.nodes]

        flow_visual = ""
        for s in states:
            if s == "green":
                flow_visual += "🟩"
            elif s == "yellow":
                flow_visual += "🟨"
            else:
                flow_visual += "🟥"

        output = []

        output.append("# 🔍 IGET PR Analysis")
        output.append(f"## 🧾 PR: {self.pr_id}")
        output.append(f"\n## 📊 Progress\n[{ '█'*10 }] {int(self.progress)}%")

        output.append("\n## 🔗 Flow")
        output.append("A → B → C → D → E → F")

        output.append("\n## 🧩 Flow State")
        output.append(flow_visual)

        output.append("\n## 📋 Issues")
        for log in self.log:
            output.append(f"- {log['node']} → {emoji[log['state']]} {log['state']}")

        output.append("\n## 🎯 Impact")
        for log in self.log:
            output.append(f"- {log['impact']}")

        output.append("\n## 🧠 Analysis")
        output.append(f"Score: {score}/100")

        output.append("\n## 📂 PR Data")
        output.append(f"- files: {metrics['total_files']}")
        output.append(f"- changes: {metrics['total_changes']}")
        output.append(f"- python: {metrics['python_files']}")
        output.append(f"- tests: {metrics['test_files']}")

        result = "✅ สำเร็จ" if "red" not in states else "❌ มีความเสี่ยง"

        output.append("\n## 🏁 Result")
        output.append(result)

        return "\n".join(output)
