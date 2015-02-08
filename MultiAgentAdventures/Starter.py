""" Module for starting a game.
Every class and parameter used to get different game outcomes should be set here. Also documentation of
game execution/performance should be contained here as much as possible, till we need dedicated modules for that.
"""

import Agent, Skill, Adventure, random, Plot, logging
from Booker import Booker

""" number of random generated Adventures"""
numAdv = 10
""" number of random generated Agents"""
numAgents = 10
iters = 10
plays= 10

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    bookers = []

    for i in range(0, plays):
        logger = logging.getLogger(__name__)
        seed = random.randrange(10, 500, 1)
        logger.debug("Creating {} random adventures: ".format(numAdv))
        advList = Adventure.createAdvList(numAdv, seed)

        for adv in advList:
            logger.debug("Adventure ID {}: {} gold reward, needs: {}".format(id(adv), adv.reward, adv.skillMap))

        logger.debug("\n Creating {} random adventurers: ".format(numAgents))
        agentList = Agent.createAgentList(numAgents, advList, seed)

        for a in agentList:
            logger.debug("Adventurer ID {}: Skills {}, Costs {}".format(id(a), a.skillList, [(id(x), y) for x, y in a.costs.items()]))


        logger.debug("\n Creating booker: ")
        booker = Booker(agentList, advList)
        upperBound = booker.upperBound
        greedyBound = booker.greedyBound
        logger.debug("Upper Bound for this game is: {} gold".format(upperBound))
        logger.debug("Greedy Bound for this game is: {} gold".format(greedyBound))
        closedAdventures = booker.completedAdventures
        openAdventures = booker.adventures
        booker.run(iters, True)
        logger.debug(booker.reward)
        logger.debug(sum(booker.reward))
        logger.debug('Closed Adventures {}'.format(closedAdventures))
        logger.debug('Open Adventures {}'.format(openAdventures))
        for agent in booker.agents:
            logger.debug("{}: Income: {} Costs: {} Total: ".format(agent, agent.rewards, agent.finalCosts))
        bookers.append((booker, seed))
    upperRatio = 0
    greedyRatio = 0
    for b, s in bookers:
        logger.debug("Seed: {}, UpperBound: {}, GreedyBound {}, Completed {}, Upper Ratio {}, Greedy Ratio {}".format(s, b.upperBound, b.greedyBound, sum(b.reward),
            sum(b.reward)/b.upperBound, sum(b.reward)/b.greedyBound))
        upperRatio += sum(b.reward)/b.upperBound
        greedyRatio += sum(b.reward)/b.greedyBound
    logger.info('#Agents: {}, #Adventures: {}, #Games: {}, #Iterations: {}'.format(numAgents, numAdv, plays, iters))
    logger.info('Average Upper Ratio = {}'.format(upperRatio/iters))
    logger.info('Average Greedy Ratio = {}'.format(greedyRatio/iters))
    
    Plot.plot(bookers)
