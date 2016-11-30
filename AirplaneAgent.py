"""
Classes describing airplane agents
David Chan - 2016
"""
from random import randint
from random import choice
import string
from AirplaneStates import AirplaneState


class AirplaneAgent(object):
    """ Class describing a simple agent with a start and goal"""

    def __init__(self, start, goal, name):
        self.start = start
        self.goal = goal
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    @staticmethod
    def random_agent():
        """ Generate a random agent """
        start_state = AirplaneState(randint(0, 200), randint(0, 200),
                                    randint(10, 20), 0, randint(0, 7), randint(1, 5))
        goal_state = AirplaneState(randint(0, 200), randint(0, 200),
                                   randint(10, 20), 0, randint(0, 7), randint(1, 5))
        name = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return AirplaneAgent(start_state, goal_state, name)
