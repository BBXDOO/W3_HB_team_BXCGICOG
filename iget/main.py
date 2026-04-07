import os
import random

class PRFlow:
    def __init__(self):
        self.nodes = []
        self.log = []
        self.history = []

    def add_node(self, node_id, name):
        self.nodes.append({"id": node_id, "name": name})

    def simulate(self):
        return {
            "green": random.randint(80, 90),
            "yellow": random.randint(50, 70),
            "red": random.randint(10, 30)
        }

    def impact_text(self, state):
        return {
            "green": "🟢 ไม่มีผลกระทบ",
            "yellow": "🟡 มีผลกระทบบางส่วน",
            "red": "🔴 เสี่ยงต่อระบบ"
        }[state]

    def bar(self, percent):
        total = 10
        filled = int(percent / 10)
        return "█" * filled + "░" * (total - filled)

    def decision_auto(self):
        # CI mode → random (no input)
        return random.choice(["green", "yellow", "red"])

    def run(self):
        pr_number = os.getenv("PR_NUMBER", "#UNKNOWN")

        output = []

        output.append(f"# 🚀 IGET PR ANALYZER")
        output.append(f"## 🧾 PR: {pr_number}\n")

        for i, node in enumerate(self.nodes):
            progress = int(((i + 1) / len(self.nodes)) * 100)

            if node["id"] in ["C", "E"]:
                state = self.decision_auto()

                self.log.append({
                    "node": node["id"],
                    "state": state
                })

                self.history.append(state)

        # ===== A + B + C =====
        output.append("## 📊 Progress")
        output.append(f"[{self.bar(progress)}] {progress}%\n")

        # ===== D + E =====
        output.append("## 📋 SUMMARY")
        output.append("Flow:")
        output.append("A → B → C → D → E → F\n")

        output.append("Issues:")
        for l in self.log:
            output.append(f"- {l['node']} → {l['state']}")

        # ===== F =====
        output.append("\nImpact:")
        for l in self.log:
            output.append(f"- {l['node']} → {self.impact_text(l['state'])}")

        # ===== G =====
        result = "✅ สำเร็จ"
        for l in self.log:
            if l["state"] == "red":
                result = "❌ มีความเสี่ยง"

        output.append(f"\n## 🎯 Result")
        output.append(result)

        # ===== FINAL FORMAT =====
        final = "\n".join(output)

        print("```")
        print(final)
        print("```")

def run():
    flow = PRFlow()

    flow.add_node("A", "commit")
    flow.add_node("B", "PR opened")
    flow.add_node("C", "check")
    flow.add_node("D", "review")
    flow.add_node("E", "decision")
    flow.add_node("F", "merge")

    flow.run()

if __name__ == "__main__":
    run()
