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

    def __init__(self, adventure, agentList):
        self.adventure = adventure
        self.agentList = agentList;

def createCoalitions(adventure, agentRequests):
    allSubSets = chain(*map(lambda x: combinations(agentRequests, x), range(1, len(agentRequests)+1)))
    completeSubSets = [x for x in list(allSubSets) if fullfillsReq(Coalition(adventure, x))]
    if not completeSubSets:
        return [Coalition(adventure, x) for x in tuple(agentRequests)]
    else:
        return [Coalition(adventure, x) for x in completeSubSets]

def fullfillsReq(coalition):
    skillReqs = copy.deepcopy(coalition.adventure.skillMap)
    for agent, skillList in coalition.agentList:
        for skill, power in skillList:
            skillReqs[skill] = skillReqs.get(skill) - power
    return reduce(lambda x, y: x and y, map(lambda x: x <= 0, list(skillReqs.values())))
