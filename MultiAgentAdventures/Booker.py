""" Module in which the game should be managed.

The process and communication of/between game entities, e.g. Agent-Adventure, should be handled
by the Booker module.

"""
import Coalition
import Skill

rounds = 100

roundsLeft = rounds

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

        print('')
        print("Largest coalitions and banzhaf power per adventure:")
        for adv in self.adventures:
            if adv.coalitions:
                print(adv.coalitions[-1])
                print('Banzhaf powers :{}'.format(adv.banzhafPowers))
                print('#Coalitions = {}'.format(len(adv.coalitions)))
                print('Best Coalition : {}'.format(Coalition.bestCoalition(adv.coalitions)))
                print('\n')
            else:
                print("no coalitions for {}".format(adv))
        """ Give The agents the possibility to update their preferences
            TODO: Agents should only see coalitions from adventures that they
                  applied for.
        """
        #for a in self.agents:
        #    a.updateGain(coalsForAdv)

    def getRequests(self, agents, adventures):
        """ Gets all request for all adventures.

        :param agents (list of Agents): available agents
        :param adventures (list of adventures): available adventures
        :return (dict: key=adventure, value= list of (Agent, list of (Skill, int)): The applying Agents and their
                                             skill/ power for every adventure.
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

    def getUpperBound(self):
        """ Gets the highest bound for tha actual game.
        Relies on the creation of adventures which reward grows exponentially with required skill power.
        :return:
        """

        bound = 0

        skillMap = {}
        for skill in list(Skill.Skill):
            skillMap[skill] = 0;
        for agent in self.agents:
            for skill, value in agent.skillList:
                skillMap[skill] += value


        sortedAdv = sorted(self.adventures, key=lambda x: x.reward, reverse= True)
        for adv in sortedAdv:
            if(sum(list(skillMap.values())) == 0):
                break
            possible = True
            for skill, value in adv.skillMap.items():
                possible = possible and skillMap[skill] >= value

            if(possible):
                for skill, value in adv.skillMap.items():
                    skillMap[skill] -= value
                bound += adv.reward
        return bound
