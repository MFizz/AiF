""" An enum class used to represent different skills """
class Skill(Enum):
    strength = 1
    stealth = 2
    persuasion = 3

""" Used to repersent the multiple features of an Adventure relevant to the Agent """
class Features:
    pass

""" The adventure class """
class Adventure:
    """ A list of skills and correspoding power needed to complete the adventure """
    requirements = []
    """ Reward awarded upon completion of the adventure """ 
    reward = 0
    
    
    def __init__(self, reqs, reward):
        """Initialize the class
        
        reqs - list of requirements
        reward - amount of reward for completion
        """
        self.requirements = reqs
        self.reward = reward


""" The agent class """
class Agent:
    """ Skill and corresponding power of the Agent of the form (Skill,power)"""
    skill = None
    """ Feature vectors of adventures of the form {Adventure:Features} """ 
    feat_vectors = {}
    
    def __init__(self, skill, feat_vectors):
        """Initialize the class
        
        skill - skill and power of the agent
        feat_vector - feature vectors of adventures
        """
        self.skill = skill
        self.feat_vectors = feat_vectors

    def estimateValue(adventure, coalition):
        pass

    def utility(adventure):
        pass

    def chooseAdventures():
        pass
