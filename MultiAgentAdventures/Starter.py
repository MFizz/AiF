""" Module for starting a game.
Every class and parameter used to get different game outcomes should be set here. Also documentation of
game execution/performance should be contained here as much as possible, till we need dedicated modules for that.
"""

import Agent, Skill, Adventure
from Booker import Booker

""" number of random generated Adventures"""
numAdv = 10
""" number of random generated Agents"""
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

