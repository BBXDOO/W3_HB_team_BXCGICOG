from mpcp.lib.pillar import Pillar

class Flow:
    def __init__(self):
        self.pillars = []

    def add(self, pillar: Pillar):
        self.pillars.append(pillar)

    def run(self, input_data):
        result = input_data

        for p in self.pillars:
            result = p.run()

        return result

