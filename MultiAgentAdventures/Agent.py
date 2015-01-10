import Skill
import random, heapq
import Adventure


class Agent(object):
    def __init__(self, skillList, advList):
        self.skillList = skillList
        self.costs = _calcCostsAdv(self, advList)

    def calcTopAdv(self, advetures):
        advValues = []
        for adv in advetures:
            advValues.append((self.utilityFunc(adv), adv))
        return sorted(advValues, key=lambda x: x[0], reverse=True)[0:4]

    def utilityFunc(self, adventure):
        cost = self.costs.get(adventure)
        skills = 0
        for skill, value in self.skillList:
            if skill in adventure.skillMap:
                skills += min(value, adventure.skillMap.get(skill))
        skillRatio = skills / sum(adventure.skillMap.values())
        cost += skillRatio * adventure.reward
        return cost

def _calcCostsAdv(self, adventures):
    costs = dict({})
    for adv in adventures:
        costs[adv] = -random.randint(1, 5)
    return costs

def createAgentList(t, advList):
    agentList = []
    for i in range(t):
        skillList = [(x,random.randint(1, 10)) for x in random.sample(list(Skill.Skill),2)]
        agentList.append(Agent(skillList, advList))
    return agentList

