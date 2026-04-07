import json

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
        best = max(sim, key=sim.get)
        return best

    def apply_decision(self, node, choice):
        mapping = {"1": "green", "2": "yellow", "3": "red"}
        state = mapping.get(choice, "red")

        node["state"] = state
        node["done"] = True

        self.log.append({
            "node": node["id"],
            "state": state,
            "impact": IMPACT_MAP[state]
        })

        self.update_progress()

        return state

    def auto_run(self):
        for node in self.nodes:
            if node["id"] in ["C", "E"]:
                sim = self.simulate()
                rec = self.recommend(sim)

                # ใช้ recommendation อัตโนมัติ
                node["state"] = rec
                node["done"] = True

                self.log.append({
                    "node": node["id"],
                    "state": rec,
                    "impact": IMPACT_MAP[rec],
                    "recommend": True
                })
            else:
                node["state"] = "green"
                node["done"] = True

            self.update_progress()

    def export(self):
        return {
            "pr": self.pr_id,
            "progress": self.progress,
            "flow": [n["id"] for n in self.nodes],
            "states": [n["state"] for n in self.nodes],
            "issues": self.log
        }
