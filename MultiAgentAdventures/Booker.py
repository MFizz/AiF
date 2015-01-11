""" Module in which the game should be managed.

The process and communication of/between game entities, e.g. Agent-Adventure, should be handled
by the Booker module.

"""
import Coalition

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
        print("Best adventures per adventurer:")
        requests = self.getRequests(self.agents, self.adventures)
        coalsForAdv = {}
        for r in requests:
            coalsForAdv[r] = Coalition.createCoalitions(r, requests[r]);

    def getRequests(self, agents, adventures):
        """ Gets all request for all adventures.

        :param agents (list of Agents): available agents
        :param adventures (list of adventures): available adventures
        :return (dict: key=adventure, value= list of (Agent, list of (Skill, int)): The applying Agents and their
                                             skill/ power for every adveture.
        """
        advRequests = {}
        for agent in self.agents:
            requests = agent.calcTopAdv(self.adventures)
            for (utility, skillList, adventure) in requests:
                if adventure in advRequests:
                    advRequests.get(adventure).append((agent, skillList))
                else:
                    advRequests[adventure] = [(agent, skillList)]
            print("Agent ID {}: {}".format(id(agent), [(x, y, id(z)) for (x, y, z) in requests]))
        return advRequests



