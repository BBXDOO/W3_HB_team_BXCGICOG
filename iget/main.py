import os

class PRFlow:
    def __init__(self):
        self.nodes = []
        self.log = []
        self.history = []

    # ----------------------
    # SETUP
    # ----------------------
    def add_node(self, node_id, name):
        self.nodes.append({"id": node_id, "name": name})

    # ----------------------
    # DETERMINISTIC DECISION
    # ----------------------
    def decision_auto(self, node_id):
        # logic พื้นฐาน (พร้อมต่อ real PR)
        if node_id == "C":
            return "yellow"
        if node_id == "E":
            return "red"
        return "green"

    # ----------------------
    # VISUAL HELPERS
    # ----------------------
    def emoji(self, state):
        return {
            "green": "🟢",
            "yellow": "🟡",
            "red": "🔴"
        }[state]

    def impact_text(self, state):
        return {
            "green": "ไม่มีผลกระทบ",
            "yellow": "มีผลกระทบบางส่วน",
            "red": "เสี่ยงต่อระบบ"
        }[state]

    def render_flow(self):
        bar = ""
        for h in self.history:
            if h == "green":
                bar += "🟩"
            elif h == "yellow":
                bar += "🟨"
            else:
                bar += "🟥"
        return bar if bar else "⬜"

    def render_progress(self):
        percent = int((len(self.history) / len(self.nodes)) * 100) if self.nodes else 0
        total = 10
        filled = int(percent / 10)
        bar = "█" * filled + "░" * (total - filled)
        return bar, percent

    # ----------------------
    # RUN
    # ----------------------
    def run(self):
        pr_number = os.getenv("PR_NUMBER", "UNKNOWN")

        output = []

        # ===== A =====
        output.append("# 🚀 IGET PR ANALYZER")
        output.append(f"## 🧾 PR: {pr_number}\n")

        # ===== PROCESS =====
        for node in self.nodes:
            if node["id"] in ["C", "E"]:
                state = self.decision_auto(node["id"])
            else:
                state = "green"

            self.history.append(state)

            if state != "green":
                self.log.append({
                    "node": node["id"],
                    "state": state
                })

        # ===== B + C =====
        bar, percent = self.render_progress()
        output.append("## 📊 Progress")
        output.append(f"[{bar}] {percent}%\n")

        # ===== D =====
        output.append("## 🔗 Flow")
        flow_ids = " → ".join([n["id"] for n in self.nodes])
        output.append(flow_ids)

        # ===== F =====
        output.append("\n## 🧩 Flow State")
        output.append(self.render_flow())

        # ===== E =====
        output.append("\n## 📋 Issues")
        if self.log:
            for l in self.log:
                output.append(f"- {l['node']} → {self.emoji(l['state'])} {l['state']}")
        else:
            output.append("🟢 ไม่มีปัญหา")

        # ===== G =====
        output.append("\n## 🎯 Impact")
        if self.log:
            for l in self.log:
                output.append(f"- {l['node']} → {self.impact_text(l['state'])}")
        else:
            output.append("🟢 ไม่มีผลกระทบ")

        # ===== RESULT =====
        result = "✅ สำเร็จ"
        if any(l["state"] == "red" for l in self.log):
            result = "❌ มีความเสี่ยง"

        output.append("\n## 🏁 Result")
        output.append(result)

        # ===== FINAL OUTPUT =====
        final = "\n".join(output)

        print("```")
        print(final)
        print("```")


# ----------------------
# ENTRY
# ----------------------
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
