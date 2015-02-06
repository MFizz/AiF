""" Module for starting a game.
Every class and parameter used to get different game outcomes should be set here. Also documentation of
game execution/performance should be contained here as much as possible, till we need dedicated modules for that.
"""

import Agent, Skill, Adventure, random
from Booker import Booker

""" number of random generated Adventures"""
numAdv = 10
""" number of random generated Agents"""
numAgents = 15


if __name__ == '__main__':
    bookers = []
    for i in range(0, 10):
        seed = random.randrange(10, 500, 1)
        print("Creating {} random adventures: ".format(numAdv))
        advList = Adventure.createAdvList(numAdv, seed)

        for adv in advList:
            print("Adventure ID {}: {} gold reward, needs: {}".format(id(adv), adv.reward, adv.skillMap))

        print("\n Creating {} random adventurers: ".format(numAgents))
        agentList = Agent.createAgentList(numAgents, advList, seed)

        for a in agentList:
            print("Adventurer ID {}: Skills {}, Costs {}".format(id(a), a.skillList, [(id(x), y) for x, y in a.costs.items()]))


        print("\n Creating booker: ")
        booker = Booker(agentList, advList)
        upperBound = booker.upperBound
        closedAdventures = booker.completedAdventures
        openAdventures = booker.adventures
        booker.run(10, True)
        print("Upper Bound for this game is: {} gold".format(upperBound))
        print(booker.reward)
        print(sum(booker.reward))
        print(closedAdventures)
        print(openAdventures)
        for agent in booker.agents:
            print("{}: Income: {} Costs: {} Total: ".format(agent, agent.rewards, agent.finalCosts))
        bookers.append((booker, seed))
    for b, s in bookers:
        print("Seed: {}, UpperBound: {}, Completed {}".format(s, b.upperBound, sum(b.reward)))


