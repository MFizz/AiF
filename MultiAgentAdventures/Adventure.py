""" Module for Adventure class and relevant functions

Adventures require different skills from agents to be completed and return a reward.
A list of random adventurers is created by *createAdvlist*
"""
import random, Skill, Coalition
import numpy as np

class Adventure:
    """ Adventures require different skills from agents to be completed and return a reward.

    Attributes:
        skillMap (dict: key=Skill, value=Int): A dictionary of the needed skills and their respective power.
        reward (int): The reward in gold.
    """
    def __init__(self, skillMap, reward):
        """
        :param skillMap (dict: key=Skill, value=Int): A dictionary of the needed skills and their respective power.
        :param reward (int): The reward in gold.
        """
        self.skillMap = skillMap
        self.reward = reward
        self.vetoAgents = []
        self.coalitions = []

    def addVetoAgents(self, vetoAgents):
        self.vetoAgents = vetoAgents

    def addCoalitions(self, coalitions):
        self.coalitions = coalitions
        self.vetoAgents = Coalition.getVetoAgents(coalitions)


def createAdvList(t):
    """ Creates 't' random Adventures for testing.

    :param t (int): Number to specify how many Adventures will to be created.
    :return (list of Adventures): List of random Adventures with len = t.
    :return (int): Sum of total power of all Adventures
    """
    advList = []
    powerDist = np.round(100*np.random.beta(2.3,4.6,t))
    for p in powerDist:
        numSkills = 0
        if p <= 15:
            numSkills = 1
        elif p <=35:
            numSkills = 2
        else:
            numSkills = 3
        skills = random.sample(list(Skill.Skill), numSkills)
        skillsProb = np.random.rand(numSkills)
        skillsProb = skillsProb/sum(skillsProb)
        skillsPow = np.round(skillsProb*p)
        if sum(skillsPow) != p:
            skillsPow[0] = p - sum(skillsPow[1:])
        skillMap = dict(zip(skills,skillsPow))
        reward = round(p**1.5) + random.randint(1,10) 
        
        advList.append(Adventure(skillMap, reward))
    return advList
