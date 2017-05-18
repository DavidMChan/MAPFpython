"""
Classes describing graph agents
Thayne Walker - 2017
"""
from random import randint
from random import choice
import string
from GraphStates import GraphState


class GraphAgent(object):
    """ Class describing a simple agent with a start and goal"""

    def __init__(self, start, goal, name):
        self.start = start
        self.goal = goal
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    @staticmethod
    def random_agent(env):
        """ Generate a random agent """
        s=env.v[env.v.keys()[randint(0,len(env.v)-1)]]
        g=env.v[env.v.keys()[randint(0,len(env.v)-1)]]
        name = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return GraphAgent(s, g, name)
