""" Module in which the game should be managed.

The process and communication of/between game entities, e.g. Agent-Adventure, should be handled
by the Booker module.

"""
class Booker:
    """ Contains relevant game Information and handles Communication/game process

    Attributes:
        agents (list of Agents): All agents.
        adventures (list of Adventures): All adventures.
    """

    def __init__(self, agents, adventures):
        self.agents = agents
        self.adventures = adventures

    def run(self):
        """ Starts and controls the game process

        TODO: return evaluable data of the outcome of the game
        """
        print("Best adventures per adventurer")
        for a in self.agents:
            print("Agent ID {}: {}".format(id(a), [(x, y, id(z)) for (x, y, z) in a.calcTopAdv(self.adventures)]))



