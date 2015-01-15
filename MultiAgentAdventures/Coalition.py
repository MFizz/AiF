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
        bestSubSets = [x for x in completeSubSets if skillsLeftToFill(maxReqFilled) <= x]
        coalitions = [Coalition(adventure, x) for x in bestSubSets]
        adventure.addCoalitions(coalitions)
        return coalitions
    else:
        coalitions = [Coalition(adventure, x) for x in completeSubSets]
        adventure.addCoalitions(coalitions)
        return coalitions

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
    return sum([x for x in list(skillReqs.values()) if x > 0])

def excess(coalition):
    skillReqs = copy.deepcopy(coalition.adventure.skillMap)
    for agent, skillList in coalition.agentList:
        for skill, power in skillList:
            skillReqs[skill] = skillReqs.get(skill) - power
    return [x for x in list(skillReqs) if skillReqs[x] < 0]


def powerDiff(coalition):
    """ Returs a map containing the power difference between the adventure 
    and coalition, for each skill needed by the adventure (replaces both excess and 
    skillsLeftToFill)

    :param coalition (Coalition): The Coaltion whose power difference should be calculated
    :return (dict: key = skill, value=int) The map containing the power difference for each skill
    """
    skillReqs = copy.deepcopy(coalition.adventure.skillMap)
    for agent, skillList in coalition.agentList:
        for skill, power in skillList:
            skillReqs[skill] = skillReqs.get(skill) - power
    return skillReqs

def getVetoAgents(coalitions):
    if not coalitions:
        return []
    vetoAgents = []
    for agent in coalitions[0].agentList:
        inAll = True
        for coal in coalitions:
            if agent in coal.agentList:
                break
            inAll = inAll and coal.agentList.contains(agent)
        if inAll:
            vetoAgents.append(agent)


def agentPower(agent, coalition):
    """ Calculates the power an agent has in a coalition

    :param agent (Agent): the agent the power is calculated for
    :param coalition (Coalition): the coalition the power is calculated for
    :return (int): The total power of 'agent' in 'coalition'
    """
    power = 0
    for a, skillList in coalition.agentList:
        if a == agent:
            power = sum([p for s,p in skillList])
    return power

def totalPower(coalition):
    """ Calculates the total power of all agents in a coalition

    :param coalition (Coalition): the coalition the power is calculated for
    :return (int): The total power all agents in 'coalition'
    """
    power = 0
    for agent, skillList in coalition.agentList:
        power += sum([p for s,p in skillList])
    return power
