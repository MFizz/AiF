""" Module for Agent class and relevant functions

The Agent represents the adventurer who should enter different adventures in order to complete them.
A list of random agents is created by *createAgentlist*
"""
import random, Adventure, Skill, Coalition, Booker
import numpy as np
import Starter


class Agent(object):
    """ The Agent represents the adventurer who should enter different adventures in order to complete them.

    Attributes:
        skillList (list of Skills): The skills which an adventurer can contribute to an adventure.
        costs (dict: key=Adventure, value=int): Holds the adventurer's initial costs of every adventure
        featureMap (dict: key=Adventure, value=_Features) - Holds the agent's feature vectors for every adventure
    """

    def __init__(self, skillList, advList,seed):
        """ Initialises Agent with a given skillList, and his initial costs calculated by calcCostAdv
        Args:
            :param skillList (list of (Skill,Int)): The skills and their power which an adventurer can contribute to an
                                                    adventure.
            :param advList (list of Adventures): The available Adventures.
        """
        self.skillListBegin = list(skillList)
        self.skillList = skillList
        self.costs = _calcCostsAdv(advList,seed)
        self.featureMap = dict()
        for adv in advList:
            self.featureMap[adv] = _Features(self, adv)
        self.coalitions = {}
        self.rewards = [0]
        self.finalCosts = [0]
        self.earnings = [0]
        self.closedAdvs = []
        self.chosenAdvs = []


    def clean(self):
        self.coalitions = {}

    def calcTopAdv(self, adventures):
        """ Calculates the best 4 adventures for the agent by using his utility function

        :param adventures (list of Adventures): The available Adventures.
        :return (list of (double, list of(Skill, int), Adventure): Best 4 adventures for the agent with the respective
        utility, and skill, power to achieve it.
        """
        advValues = []
        #print('Stats for agent {}:'.format(self))
        for adv in adventures:
            features = self.featureMap.get(adv)
            #print('{}, Util {}, Costs {}, Reward {}'.format(adv, self.utility(adv), features.costs, features.reward))
            if self.utility(adv)[0] > 0:
                advValues.append(self.utility(adv) + (adv,))
        finalAdv = sorted(advValues, key=lambda x: x[0], reverse=True)[0:4]
        self.chosenAdvs = [x[2] for x in finalAdv]
        return finalAdv

    def utility(self, adventure):
        """ Determines the utility an agent estimates for entering a given adventure.

        :param adventure (Adventure): The Adventure whose utility for the agent needs to be determined.
        :return (double, list of(Skill, int): Utility and the respective skills and power to achieve it.

        """
        features = self.featureMap.get(adventure)
        utility = 0
        utility += features.reward
        utility += features.costs
        skillList = []
        if utility > 0:
            for skill, value in self.skillList:
                if skill in adventure.skillMap:
                    skillList.append((skill, min(value, adventure.skillMap.get(skill))))
            if features.coalition is None:
                utility *= 1 - ((features.timesFailed)**2)/((Booker.rounds)**2)
                utility *= Booker.roundsLeft/Booker.rounds
            elif not Coalition.fullfillsReq(features.coalition):
                a = np.linspace(1.35, 1, 20, endpoint=False)
                b = np.linspace(1, 0.65, 81)
                vals = np.concatenate((a, b))
                factor = vals[features.powerNeeded]
                factor += (np.linspace(0.15, -0.15, 101))[features.skillsNeeded]
                utility *= factor
                utility *= 1 - ((features.timesFailed)**2)/((Booker.rounds)**2)

                utility *= Booker.roundsLeft/Booker.rounds
            else:
                roundsFactor = 1 + 20*(1 - (Booker.roundsLeft/Booker.rounds))**2
                powerFactor = 1 + (1 - features.confirmedPowerNeeded)**4
                powerFactor = powerFactor**roundsFactor
                utility *= powerFactor
        else:
            utility = 0
        return utility, skillList


    def estimateReward(self, adventure, coalition):
        """ Determines an estimate for the reward the agent will get for completing the adventure,
        given a certain coalition (if available).

        :param adventure (Adventure):   The Adventure for which the reward needs to be estimated.
        :param coalition (Coalition):   The coalition the agent for which the reward needs to be estimated.
                                            If there is no coalition then the value of this parameter can be None.
        :return (float) - an estimate for the reward the agent will get for completing the adventure
        """
        """ TODO: More accurate estimation based on veto agents """
        if coalition is None:
            skillPower = 0
            for skill, value in self.skillList:
                if skill in adventure.skillMap:
                    skillPower +=  min(value, adventure.skillMap.get(skill))
            return skillPower / sum(adventure.skillMap.values()) * adventure.reward
        elif not Coalition.fullfillsReq(coalition):
            agentPower = Coalition.agentPower(self, coalition)
            coalitionPower = Coalition.totalPower(coalition)
            return (agentPower / coalitionPower) * adventure.reward
        else:
            agentBP = adventure.banzhafPowers.get(self)
            coalitionBP = Coalition.totalBanzhafPower(coalition)
            return (agentBP/coalitionBP) * adventure.reward




    def updateGain(self):
        """ Update the agents current estimation of the game and his expected gain

        :param coalsForAgent (list of Coalitions): The Winning coalitions for this agent for each adventure
        """

        for adv in self.chosenAdvs:
            """ TODO add confirmedAgents. Maybe these are only known at a
                     different point.
                TODO it is redundant to reference adventure from the feature map
                     and as an argument of the function
                TODO updateFeatures (calling estimateReward) can only handle one
                     coalition at a time
            """
            if adv in self.coalitions:
                self.featureMap[adv].updateFeatures(self, adv, self.coalitions[adv], adv.confirmedAgents)
            else:
                self.featureMap[adv].updateFeatures(self, adv, None, adv.confirmedAgents)

    def choseCoalitionForConfirmation(self):
        bestCol = None
        bestColReward = 0
        for col in self.coalitions.values():
            if self.estimateReward(col.adventure, col)-self.costs.get(col.adventure) > bestColReward:
                bestCol = col
                bestColReward = self.estimateReward(col.adventure, col)-self.costs.get(col.adventure)
        if bestCol:
            bestCol.adventure.confirmedAgents.append(self)

    def choseFinalCoalition(self):
        bestCol = None
        bestColUtility = 0
        for col in self.coalitions.values():
            u, s = self.utility(col.adventure)
            if u  > bestColUtility:
                bestCol = col
                bestColUtility = u
        if bestCol:
            bestCol.adventure.finalAgents.append(self)


    def __str__(self):
        return "Agent ID {}".format(id(self))

    def __repr__(self):
        return self.__str__()


def _calcCostsAdv(adventures,seed):
    """ Assigns random negative numbers to given adventures which represent a cost factor for every adventure.

    :param adventures (list of Adventures): Available Adventures.
    :return (dict: key=Adventure, value=Int): A lookup table for the costs of every Adventure.
    """
    random.seed(seed)
    costs = dict()
    for adv in adventures:
        costs[adv] = -random.randint(1, 15)
    return costs

def createAgentList(t, advList,seed):
    """ Creates 't' random Agents for testing.

    :param t (int): Number to specify how many Agents will to be created.
    :param advList (list of Adventures): Available Adventures.
    :return (list of Agents): List of random Agents with len = t.
    """
    random.seed(seed)
    np.random.seed(seed)
    agentList = []
    skillMap = dict()
    for adv in advList:
        for skill in adv.skillMap.keys():
            if skill in skillMap:
                skillMap[skill] += adv.skillMap.get(skill)
            else:
                skillMap[skill] = adv.skillMap.get(skill)

    print('skillMap: ', skillMap)

    numAgents = dict(skillMap)
    for skill in numAgents.keys():
        numAgents[skill] /= sum(skillMap.values())
        numAgents[skill] *= t
        numAgents[skill] = round(numAgents.get(skill))


    if sum(numAgents.values()) != t:
        skills = list(numAgents.keys())
        random.shuffle(skills)
        for i in range(len(skills)):
            agentNum = t - sum([numAgents.get(s) for s in skills[:i]+skills[i+1:]])
            if agentNum > 0:
                numAgents[skills[i]] = agentNum
                break


    print ('#Agents per skill: {}'.format(numAgents))

    for skill in sorted(numAgents.keys(),key=numAgents.get):
        power = round(skillMap.get(skill)*(0.1*random.random() + 0.4))
        print('Power {}'.format(power))
        agentsProb = np.random.rand(numAgents.get(skill))
        #print ('Agents Prob {}'.format(agentsProb))
        agentsProb /= sum(agentsProb)
        agentsPow = agentsProb*power
        agentsPow = np.ceil(agentsProb*power)
        print('Agents Power {}'.format(sum(agentsPow)))

        for p in agentsPow:
            skillList = []
            skillList.append((skill,p))

            agentList.append(Agent(skillList,advList,seed))


    return agentList

class _Features:
    """ The Features class stores features relevant to the Agent for a specific Adventure
)
    Attributes:
        costs (int):                the adventurer's initial costs for this adventure
        reward (float):             the expected reward the adventurer will get for this adventure
        coalition (Coalition):      None if the agent is not in the winning coalition
        powerNeeded (float):        percentage of power needed to complete adventure, compared to the full power
                                        needed to complete adventure    
        confirmedAgents (float):    percentage of agents that have decided to stay in the coalition
                                        each skill, only taking confirmed agents into account
        timesFailed (int):          counts how many times the agent applied for the adventure without getting
                                        in the winning coalition
    """

    def __init__(self, agent, adventure):
        """ Initialises Features with a given agent and adventure
        Args:
            :param agent (Agent):   The agent this feature vector belongs to
            :param adventure (Adventures):  The adventure this feature vector is for
        """
        self.costs = agent.costs.get(adventure)
        self.reward = agent.estimateReward(adventure, None)
        self.coalition = None
        self.powerNeeded = 0
        self.skillsNeeded = 0
        self.confirmedPowerNeeded = 0
        self.confirmedAgents = 0
        self.timesFailed = 0

    def updateFeatures(self, agent, adventure, coalition, confirmedAgents):
        """ Updates Features with the given arguments
        Args:
            :param agent (Agent):   The agent this feature vector belongs to
            
            :param adventure (Adventures):  The adventure this feature vector is for
            :param coalition (Coalition):   The winning coalition the agent is in for this adventure (None if not in coalition)
            :param confirmedAgents ([Agent]):   list of agents that have decided to stay in the coalition after negotiations

        """
        self.costs = agent.costs.get(adventure)
        self.reward = agent.estimateReward(adventure, coalition)
        self.coalition = coalition

        if coalition is None:
            self.timesFailed += 1
        else:
            coalitionPowerDiff = Coalition.powerDiff(coalition)
            self.powerNeeded = sum([p for p in coalitionPowerDiff.values() if p>0])
            self.powerNeeded /= sum(adventure.skillMap.values())
            self.powerNeeded = round(self.powerNeeded*100)
            self.skillsNeeded = len([p for p in coalitionPowerDiff.values() if p>0])
            self.skillsNeeded /= len(adventure.skillMap)
            self.skillsNeeded = round(self.skillsNeeded*100)

            self.confirmedAgents = len(confirmedAgents)/len(coalition.agentList)
            self.confirmedAgents = round(self.confirmedAgents*100)

            confirmedAgentList = [(a,sp) for a,sp in coalition.agentList if a in confirmedAgents]
            skillList = [sk for a, sp in confirmedAgentList for sk in sp]
            skillMap = dict()
            for skill, power in skillList:#

                if skill not in skillMap.keys():
                    skillMap[skill] = power
                else:
                    skillMap[skill] += power
            confirmedAgentsPowerDiff = []
            for skill in skillMap.keys():
                confirmedAgentsPowerDiff.append((skill, adventure.skillMap[skill] - skillMap[skill]))
            self.confirmedPowerNeeded = adventure.totalPower()
            agents = [(a,sp) for a,sp in coalition.agentList if a in confirmedAgents]
            for a,sp in agents:
                for s,p in sp:
                    self.confirmedPowerNeeded -= p
            self.confirmedPowerNeeded /= sum(adventure.skillMap.values())
