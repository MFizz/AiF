""" This coalition module contains classes and functions concerning
coalitions and coalition
buildung.
"""
from itertools import chain, combinations
from functools import reduce
import copy

class Coalition:
    """ A coalition contains everything

    Attributes:
        adventure (Adventure): A coalition belongs to one adventure and to this only.
        agentList (list of tuples of (Agent, list of (Skill, int))): Combination
    """

    def __init__(self, adventure, agentList, vetoAgents=None):
        self.adventure = adventure
        self.agentList = agentList

    def setVetoAgents(self, vetoAgents):
        self.vetoAgents = vetoAgents

    def appendVetoAgents(self, vetoAgents):
        self.vetoAgents.append(vetoAgents)

def createCoalitions(adventure, agentRequests):
    """ Creates all possible coalitions for every adventure and their requests from agents.
    It returns all coalitions which complete an adventure or if those don't exist, the great
    coalition of all agent requests.

    :param adventure (Adventure): The adventure from which the coalitions shall be created.
    :param agentRequests (list of (Agent, list of (Skill, int)): List of Agents and their skills and power, which
                                                                 applied for that adventure
    :return (list of Coalitions): List of coalitions for that Adventure.
    """
    allSubSets = chain(*map(lambda x: combinations(agentRequests, x), range(1, len(agentRequests)+1)))
    completeSubSets = [x for x in list(allSubSets) if fullfillsReq(Coalition(adventure, x))]
    if not completeSubSets:
        maxReqFilled = skillsLeftToFill(Coalition(adventure, tuple(agentRequests)))
        bestSubSets = [x for x in completeSubSets if maxSkillsLeftToFill(x, maxReqFilled)]
        coalitions = [Coalition(adventure, x) for x in bestSubSets]
        vetoAgents = [x for]
    else:
        return [Coalition(adventure, x) for x in completeSubSets]

def fullfillsReq(coalition):
    """ Checks if the Coalition completes the adventure

    :param coalition (Coalition): The examined Coaltion
    :return (bool): True if every requirement is met.
    """
    skillReqs = copy.deepcopy(coalition.adventure.skillMap)
    for agent, skillList in coalition.agentList:
        for skill, power in skillList:
            skillReqs[skill] = skillReqs.get(skill) - power
    return reduce(lambda x, y: x and y, map(lambda x: x <= 0, list(skillReqs.values())))

def skillsLeftToFill(coalition):
    skillReqs = copy.deepcopy(coalition.adventure.skillMap)
    for agent, skillList in coalition.agentList:
        for skill, power in skillList:
            skillReqs[skill] = skillReqs.get(skill) - power
    return sum(skillReqs.values())

def maxSkillsLeftToFill(coalition,t):
    skillReqs = copy.deepcopy(coalition.adventure.skillMap)
    for agent, skillList in coalition.agentList:
        for skill, power in skillList:
            skillReqs[skill] = skillReqs.get(skill) - power
    return t >= sum([x for x in list(skillReqs.values()) if x > 0])

def getVetoAgents(Coalitions):
