import os
import sys
import random

class PRFlow:
    def __init__(self):
        self.nodes = []
        self.progress = 0
        self.log = []
        self.history = []

    def add_node(self, node_id, name):
        self.nodes.append({"id": node_id, "name": name})

    def get_choice(self, node_id):
        # priority: ENV > ARG > default
        env_key = f"IGET_{node_id}"
        if env_key in os.environ:
            return os.environ[env_key]

        if len(sys.argv) > 1:
            return sys.argv[1]

        return "1"  # default = fix

    def simulate(self):
        return {
            "green": random.randint(80, 90),
            "yellow": random.randint(50, 70),
            "red": random.randint(10, 30)
        }

    def impact(self, state):
        impact_map = {
            "green": "🟢 ไม่มีผลกระทบ",
            "yellow": "🟡 มีผลกระทบบางส่วน",
            "red": "🔴 เสี่ยงต่อระบบ"
        }
        return impact_map[state]

    def decision(self, node):
        sim = self.simulate()

        print("\n🔮 SIMULATION:")
        print(f"GREEN  → success ~{sim['green']}%")
        print(f"YELLOW → success ~{sim['yellow']}%")
        print(f"RED    → success ~{sim['red']}%")

        print("\n🧠 RECOMMEND:")
        print("→ suggest: GREEN")
        print("เหตุผล: ปลอดภัยที่สุด")

        choice = self.get_choice(node["id"])

        mapping = {
            "1": "green",
            "2": "yellow",
            "3": "red"
        }

        state = mapping.get(choice, "green")

        print(f"\nImpact: {self.impact(state)}")

        self.log.append({
            "node": node["id"],
            "state": state
        })

        self.history.append(state)

    def render_flow(self):
        bar = ""
        for h in self.history:
            if h == "green":
                bar += "🟩"
            elif h == "yellow":
                bar += "🟨"
            else:
                bar += "🟥"
        return bar

    def run(self):
        print("🚀 START FLOW\n")

        for i, node in enumerate(self.nodes):
            self.progress = ((i + 1) / len(self.nodes)) * 100

            print(f"→ {node['id']} ({node['name']})")
            print(f"Flow: {self.render_flow()}")
            print(f"Progress: {self.progress:.2f}%")

            if node["id"] in ["C", "E"]:
                print(f"\n⚠️ Node {node['id']}")
                print("1 = 🟢 fix")
                print("2 = 🟡 workaround")
                print("3 = 🔴 skip")

                self.decision(node)

        print("\n✅ FLOW END")
        print(f"LOG: {self.log}")

        self.summary()

    def summary(self):
        print("\n📊 SUMMARY\n")

        flow = " → ".join([n["id"] for n in self.nodes])
        print(f"Flow:\n{flow}\n")

        print("Issues:")
        for l in self.log:
            print(f"- {l['node']} → {l['state']}")

        print("\nImpact:")
        for l in self.log:
            print(f"- {l['node']} → {self.impact(l['state'])}")

        result = "✅ สำเร็จ"
        for l in self.log:
            if l["state"] == "red":
                result = "❌ มีความเสี่ยง"

        print(f"\nResult:\n{result}")

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
