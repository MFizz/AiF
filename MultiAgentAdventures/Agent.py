""" Module for Agent class and relevant functions

The Agent represents the adventurer who should enter different adventures in order to complete them.
A list of random agents is created by *createAgentlist*
"""
import random, Adventure, Skill


class Agent(object):
    """ The Agent represents the adventurer who should enter different adventures in order to complete them.

    Attributes:
        skillList (list of Skills): The skills which an adventurer can contribute to an adventure.
        costs (dict: key=Adventure, value=int): Hold the adventurer's initial costs of every adventure

    TODO:  FeatureVector needs to be implemented as Attribute
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

    def calcTopAdv(self, advetures):
        """ Calculates the best 4 adventures for the agent by using his utility function

        :param adventures (list of Adventures): The available Adventures.
        :return (list of Adventures): Best 4 adventures for the agent
        """
        advValues = []
        for adv in advetures:
            advValues.append((self.utilityFunc(adv), adv))
        return sorted(advValues, key=lambda x: x[0], reverse=True)[0:4]

    def utilityFunc(self, adventure):
        """ Determines the value an agent estimates for entering a given adventure.
        For now we calculate utility by:
        (skillpoints provided by agent / skillpoints required) * reward
        for the best case.

        :param adventure (Adveture): The Adventure whose utility for the agent needs to be determined.
        :return (double): utility

        TODO: Agent's feature vector need to be incorporated
        """
        cost = self.costs.get(adventure)
        skills = 0
        for skill, value in self.skillList:
            if skill in adventure.skillMap:
                skills += min(value, adventure.skillMap.get(skill))
        skillRatio = skills / sum(adventure.skillMap.values())
        cost += skillRatio * adventure.reward
        return cost

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

