"""
Heuristics and costs for the airplane Environmen
David Chan - 2016
"""

#TODO Add the perimeter heuristic

import math

def distance(p1,p2):
  return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Assumes a state with tuple: (name,(x,y))
class StraightLineHeuristic(object):
    """ Contains info needed for straight line heuristic (L2) """
    def __call__(self, start, goal):
        """ Gets the straight line cost """
        return distance(start[1],goal[1])

# Assumes a state with tuple: (name,(x,y))
class SimpleGCost(object):
    """ Contains a simple gcost for two states """
    def __call__(self, start, goal):
        return distance(start[1],goal[1])

