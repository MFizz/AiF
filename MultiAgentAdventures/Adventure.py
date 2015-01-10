import random, Skill

class Adventure:

    def __init__(self, skillMap, reward):
        self.skillMap = skillMap
        self.reward = reward


def createAdvList(t):
    advList = []
    for i in range(t):
        skillMap = {x : random.randint(1, 10) for x in random.sample(list(Skill.Skill), random.randint(1, 3))}
        advList.append(Adventure(skillMap, random.randint(1, 20)))
    return advList