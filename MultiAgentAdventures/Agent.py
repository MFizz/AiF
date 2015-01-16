""" Module for Agent class and relevant functions

The Agent represents the adventurer who should enter different adventures in order to complete them.
A list of random agents is created by *createAgentlist*
"""
import random, Adventure, Skill, Coalition
import numpy as np


class Agent(object):
    """ The Agent represents the adventurer who should enter different adventures in order to complete them.

    Attributes:
        skillList (list of Skills): The skills which an adventurer can contribute to an adventure.
        costs (dict: key=Adventure, value=int): Holds the adventurer's initial costs of every adventure
        featureMap (dict: key=Adventure, value=_Features) - Holds the agent's feature vectors for every adventure
    """

    def __init__(self, skillList, advList):
        """ Initialises Agent with a given skillList, and his initial costs calculated by calcCostAdv
        Args:
            :param skillList (list of (Skill,Int)): The skills and their power which an adventurer can contribute to an
                                                    adventure.
            :param advList (list of Adventures): The available Adventures.
        """
        self.skillList = skillList
        self.costs = _calcCostsAdv(advList)
        self.featureMap = dict({})
        for adv in advList:
            self.featureMap[adv] = _Features(self, adv)


    def calcTopAdv(self, adventures):
        """ Calculates the best 4 adventures for the agent by using his utility function

        :param adventures (list of Adventures): The available Adventures.
        :return (list of (double, list of(Skill, int), Adventure): Best 4 adventures for the agent with the respective
        utility, and skill, power to achieve it.
        """
        advValues = []
        for adv in adventures:
            advValues.append(self.utility(adv) + (adv,))
        return sorted(advValues, key=lambda x: x[0], reverse=True)[0:4]

    def utility(self, adventure):
        """ Determines the utility an agent estimates for entering a given adventure.

        :param adventure (Adventure): The Adventure whose utility for the agent needs to be determined.
        :return (double, list of(Skill, int): Utility and the respective skills and power to achieve it.

        """
        features = self.featureMap.get(adventure)

        utility = 0
        utility += features.reward
        utility -= features.costs
        skillList = []
        for skill, value in self.skillList:
            if skill in adventure.skillMap:
                skillList.append((skill, min(value, adventure.skillMap.get(skill))))
        if features.coalition is None:
            utility *= 1 - ((features.timesFailed + 1.0)**2)/500
            utility *= features.roundsLeft/100.0
        elif not Coalition.fullfillsReq(features.coalition):
            a = np.linspace(1.35,1,20,endpoint=False)
            b = np.linspace(1,0.65,81)
            vals = np.concatenate((a,b))
            factor = vals[features.powerNeeded]
            factor += (np.linspace(0.15,-0.15,101))[features.skillsNeeded]
            utility *= factor
            utility *= 1 - ((features.timesFailed + 1.0)**2)/1000
            utility *= features.roundsLeft/100.0
        else:
            powerFactor = (1 - features.confirmedPowerNeeded)**2
            roundsFactor = 1+ (1 - (features.roundsLeft/100))**2
            utility *= 1+(powerFactor*roundsLeft*0.7)


        return utility, skillList


    def estimateReward(self, adventure, coalition):
        """ Determines an estimate for the reward the agent will get for comleting the adventure,
        given a certain coalition (if available).

        :param adventure (Adventure):   The Adventure for which the reward needs to be estimated.
        :param coa)ition (Coalition):   The coalition the agent for which the reward needs to be estimated.
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
        else:
            agentPower = Coalition.agentPower(self, coalition) 
            coalitionPower = Coalition.totalPower(coalition)
            vetoAgents = adventure.vetoAgents
            #if not vetoAgents or len(vetoAgents)==len(coalition.agentList.keys()):
            return (agentPower / coalitionPower) * adventure.reward
            #elif self in vetoAgents:


                



    def updateGain(self, coalsForAgent):
        """ Update the agents current estimation of the game and his expected gain

        :param coalsForAgent (list of Coalitions): The Winning coalitions for this agent for each adventure
        """

        for adv in coalsForAgent:
            """ TODO add confirmedAgents. Maybe these are only known at a
                     different point.
                TODO it is redundant to reference adventure from the feature map
                     and as an argument of the function
                TODO updateFeatures (calling estimateReward) can only handle one
                     coalition at a time
            """
            self.featureMap[adv].updateFeatures(self, adv, coalsForAgent[adv], None, False)


def _calcCostsAdv(adventures):
    """ Assigns random negative numbers to given adventures which represent a cost factor for every adventure.

    :param adventures (list of Adventures): Available Adventures.
    :return (dict: key=Adventure, value=Int): A lookup table for the costs of every Adventure.
    """
    costs = dict({})
    for adv in adventures:
        costs[adv] = -random.randint(1, 5)
    return costs

def createAgentList(t, advList):
    """ Creates 't' random Agents for testing.

    :param t (int): Number to specify how many Agents will to be created.
    :param advList (list of Adventures): Available Adventures.
    :return (list of Agents): List of random Agents with len = t.
    """
    agentList = []
    for i in range(t):
        skillList = [(x, random.randint(1, 10)) for x in random.sample(list(Skill.Skill),2)]
        agentList.append(Agent(skillList, advList))
    return agentList

class _Features:
    """ The Features class stores features relevant to the Agent for a specific Adventure

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
        roundsLeft (int):           counts how many rounds are left until the game ends
    """

    def __init__(self, agent, adventure, roundsLeft= 100):
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
        self.roundsLeft = roundsLeft

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
            self.powerNeeded /= sum(adventure.skillMap.values)
            self.powerNeeded = round(powerNeeded*100)
            self.skillsNeeded = len([p for p in coalitionPowerDiff.values() if p>0])
            self.skillsNeeded /= len(adventure.skillMap)
            self.skillsNeeded = round(skillsNeeded*100)

            self.confirmedAgents = len(confirmedAgents)/len(coalition.agentList)
            self.confirmedAgents = round(self.confirmedAgents*100)

            confirmedAgentList = [(a,sp) for a,sp in coalition.agentList if a in confirmedAgents]
            skillList = [sp for a, sp in confirmedAgentList]
            skillMap = dict({})
            for skill, power in skillList:
                if skill not in skillMap.keys():
                    skillMap[skill] = power
                else:
                    skillMap[skill] += power
            confirmedAgentsPowerDiff = []
            for skill in skillMap.keys():
                confirmedAgentsPowerDiff.append(skill,adventure.skillMap.get(skill) - skillMap.get(skill))
            self.confirmedPowerNeeded = sum([p for s,p in confirmedAgentsPowerDiff if p>0])
            self.confirmedPowerNeeded /= sum(adventure.skillMap.values())
            self.confirmedPowerNeeded /= round(self.confirmedPowerNeeded*100)
        self.roundsLeft -= 1
