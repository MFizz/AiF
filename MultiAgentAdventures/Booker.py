""" Module in which the game should be managed.

The process and communication of/between game entities, e.g. Agent-Adventure, should be handled
by the Booker module.

"""
import Coalition
import Skill

rounds = 0.0
roundsLeft = 0.0

class Booker:
    """ Contains relevant game Information and handles Communication/game process

    Attributes:
        agents (list of Agents): All agents.
        adventures (list of Adventures): All adventures.
    """

    def __init__(self, agents, adventures):
        self.agents = agents
        self.adventures = adventures
        self.completedAdventures = []
        self.reward = []
        self.upperBound = self.getUpperBound()
        self.greedyBound = self.getGreedyBound()

    def run(self, initRounds, rL = False):
        """ Starts and controls the game process

        TODO: return evaluable data of the outcome of the game
        """
        global rounds, roundsLeft
        rounds = initRounds
        roundsLeft = initRounds
        for i in range(0, initRounds):
            self.reward.append(0)
            print("Best adventures per adventurer:")
            requests = self.getRequests(self.agents, self.adventures)
            coalsForAdv = {}
            for r in requests:
                coalsForAdv[r] = Coalition.createCoalitions(r, requests[r]);
            

            print('')
            print("Best coalition and banzhaf power per adventure:")
            for adv in self.adventures:
                if adv.coalitions:
                    print(adv)
                    print('Banzhaf powers :{}'.format(adv.banzhafPowers))
                    print('#Coalitions = {}'.format(len(adv.coalitions)))
                    bestCoal = Coalition.bestCoalition(adv.coalitions)
                    print('Best Coalition : {}'.format(bestCoal))
                    if bestCoal != None:
                        print('excess : {}'.format(Coalition.totalPower(bestCoal)-adv.totalPower()))
                        bestCoal = Coalition.removeExcess(bestCoal)
                        adv.bestCoalition = bestCoal
                        if adv.bestCoalition:
                            for agent, power in adv.bestCoalition.agentList:
                                agent.coalitions[adv] = adv.bestCoalition
                        #print ('F]lfulls exp: {}'.format(Coalition.fullfillsReq(bestCoal)))
                    print('\n')
                else:
                    print("no coalitions for {}".format(adv))
            """ Give The agents the possibility to update their preferences
                TODO: Agents should only see coalitions from adventures that they
                      applied for.
            """
            for agent in self.agents:
                agent.choseCoalitionForConfirmation()
            
            for adv in self.adventures:
                if adv.bestCoalition:
                    power = 0
                    agents = [(a,sp) for a,sp in adv.bestCoalition.agentList if a in adv.confirmedAgents]
                    for a,sp in agents:
                        for s,p in sp:
                            power += p
                        
                    print("{} Confirmed Agents: {}, Reward {}, Power Needed {}".format(adv, adv.confirmedAgents, adv.reward, (adv.totalPower() - power)/adv.totalPower()))


            for agent in self.agents:
                agent.updateGain()
                '''print('Stats for agent {}:'.format(agent))
                for adv in self.adventures:
                    features = agent.featureMap.get(adv)
                    print('{}, Util {}, Costs {}, Reward {}'.format(adv, agent.utility(adv), features.costs, features.reward))'''
                agent.choseFinalCoalition()

                agent.clean()
            
            for adv in self.adventures:
                if adv.bestCoalition:
                    print("{} Final Agents: {}".format(adv, adv.finalAgents))

            for adv in list(self.adventures):
                if adv.bestCoalition:
                    if set(adv.finalAgents).issuperset(set([a for a, s in adv.bestCoalition.agentList])):
                        adv.rewardAgents()
                        self.reward[-1] += adv.reward
                        print(adv.reward)
                        self.adventures.remove(adv)
                        self.completedAdventures.append(adv)
                    else:
                        adv.clean()
                else:
                    adv.clean()

            if rL:
                roundsLeft -= 1
                print('Completed adventures {}'.format(self.completedAdventures))
                print('Agents:')
                for agent in self.agents:
                    print ('{} {}'.format(agent, agent.skillList))
                print('Adventures:')
                for adv in self.adventures:
                    print ('{} {}'.format(adv, adv.skillMap))

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


    def getGreedyBound(self):
        """ Gets the greedy bound for the actual game.
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
    
    def getUpperBound(self):
        """ Gets the highest bound for the actual game.
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
            totalPow = 0
            for skill, value in adv.skillMap.items():
                possiblePow = min(value, skillMap.get(skill))
                totalPow += possiblePow
                skillMap[skill] -= possiblePow
            
            bound += adv.reward*(totalPow/adv.totalPower())

        return bound
