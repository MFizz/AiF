""" Module for starting a game.
Every class and parameter used to get different game outcomes should be set here. Also documentation of
game execution/performance should be contained here as much as possible, till we need dedicated modules for that.
"""
from threading import Thread
import threading
import Agent, Skill, Adventure, random, Plot, logging, datetime, time, sys
from Booker import Booker
import numpy as np

""" number of random generated Adventures"""
numAdv = 10
""" number of random generated Agents"""
numAgents = 10
iters = 50
plays = 100
maxCurThreads = 10

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
logger.propagate = False

streamLogger = logging.StreamHandler(stream= sys.stdout)
streamLogger.setLevel(logging.INFO)
streamLogger.setFormatter(formatter)

current_time = time.strftime("%m.%d.%y_%H_%M", time.localtime())
handler = logging.FileHandler('MultiAgents_ag{}_adv{}_it{}_pl{}_{}.log'.format(numAgents,numAdv,iters,plays,current_time))
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger.addHandler(streamLogger)
logger.addHandler(handler)
times = []
bookers = []
activeThreads = []

def timedelta_milliseconds(td):
    return td.days*86400000 + td.seconds*1000 + td.microseconds/1000

def startMaxThreads(threads):
    while(threads):
        if threading.activeCount() < maxCurThreads:
            activeThreads.append(threads[-1])
            threads[-1].start()
            del threads[-1]


def compPlay(seed, i):
    global  times, bookers, activeThreads
    start = datetime.datetime.now()
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
    end = datetime.datetime.now()
    dur = timedelta_milliseconds(end-start)
    bookers.append((booker, seed))
    logger.info("Iteration %i in %i milliseconds"%(i,dur))
    times.append(dur)

if __name__ == '__main__':
    global times, bookers
    start = datetime.datetime.now()
    threadPool = []
    seed = random.randrange(10, 30000, 1)

    for iteration in range(0, plays):
        seed += 1
        seedArgs = [seed,iteration]
        try:
            threadPool.append(Thread(target=compPlay, args=seedArgs))
        except:
            logger.warn("Could not start Thread %i"%plays)

    threadArgs = [threadPool]
    startThread = Thread(target=startMaxThreads, args=threadArgs)
    startThread.start()

    while(len(bookers) != plays):
        pass
    end = datetime.datetime.now()
    upperRatio = 0
    greedyRatio = 0
    for b, s in bookers:
        logger.debug("Seed: {}, UpperBound: {}, GreedyBound {}, Completed {}, Upper Ratio {}, Greedy Ratio {}".format(s, b.upperBound, b.greedyBound, sum(b.reward),
            sum(b.reward)/b.upperBound, sum(b.reward)/b.greedyBound))
        upperRatio += sum(b.reward)/b.upperBound
        greedyRatio += sum(b.reward)/b.greedyBound
    logger.info('#Agents: {}, #Adventures: {}, #Games: {}, #Iterations: {}, average computation time for iteration: {}ms,'
                ' total time: {}ms'.format(numAgents, numAdv, plays, iters, round(np.mean(times)), round(sum(times))))
    logger.info('Average Upper Ratio = {}'.format(upperRatio/plays))
    logger.info('Average Greedy Ratio = {}'.format(greedyRatio/plays))
    logger.info("Total time {} ms".format(timedelta_milliseconds(end-start)))

    Plot.plot(bookers,times)
