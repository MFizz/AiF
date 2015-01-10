import Agent, Skill, Adventure
from Booker import Booker
numAdv = 10
numAgents = 4


if __name__ == '__main__':
    print("Creating {} random adventures: ".format(numAdv))
    advList = Adventure.createAdvList(numAdv)

    for adv in advList:
        print("Adventure ID {}: {} gold reward, needs: {}".format(id(adv), adv.reward, adv.skillMap))

    print()
    print("Creating {} random adventurers: ".format(numAgents))
    agentList = Agent.createAgentList(numAgents, advList)

    for a in agentList:
        print("Adventurer ID {}: Skills {}, Costs {}".format(id(a), a.skillList, [(id(x), y) for x, y in a.costs.items()]))

    print()
    print("Creating booker: ")
    booker = Booker(agentList, advList)
    booker.run()

