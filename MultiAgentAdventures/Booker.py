class Booker:

    def __init__(self, agents, adventures):
        self.agents = agents
        self.adventures = adventures

    def run(self):
        for a in self.agents:
            print("Best adventures per adventurer")
            print("Agent ID {}: {}".format(id(a),[(x, id(y)) for (x, y) in a.calcTopAdv(self.adventures)]))


