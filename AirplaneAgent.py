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
    def random_agent(env):
        """ Generate a random agent """
        start_state = AirplaneState(randint(0, env.grid_size), randint(0, env.grid_size),
                                    randint(10, env.max_height), 0, randint(0, 7), randint(env.min_speed, env.max_speed))
        goal_state = AirplaneState(randint(0, env.grid_size), randint(0, env.grid_size),
                                   randint(10, env.max_height), 0, randint(0, 7), randint(env.min_speed, env.max_speed))
        name = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return AirplaneAgent(start_state, goal_state, name)
