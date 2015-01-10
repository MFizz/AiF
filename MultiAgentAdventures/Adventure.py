""" Module for Adventure class and relevant functions

Adventures require different skills from agents to be completed and return a reward.
A list of random adventurers is created by *createAdvlist*
"""
import random, Skill

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


def createAdvList(t):
    """ Creates 't' random Adventures for testing.

    :param t (int): Number to specify how many Adventures will to be created.
    :return (list of Adventures): List of random Adventures with len = t.
    """
    advList = []
    for i in range(t):
        skillMap = {x : random.randint(1, 10) for x in random.sample(list(Skill.Skill), random.randint(1, 3))}
        advList.append(Adventure(skillMap, random.randint(1, 20)))
    return advList