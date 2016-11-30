"""
Heuristics and costs for the airplane Environmen
David Chan - 2016
"""

import math

class AirStraightLineHeuristic(object):
    """ Contains info needed for straight line heuristic (L2) """
    def __call__(self, start, goal):
        """ Gets the straight line cost """
        return math.sqrt((start.x_loc - goal.x_loc) ** 2 +
                         (start.y_loc - goal.y_loc) ** 2 +
                         (start.z_loc - goal.z_loc) ** 2)# +
                         #(start.heading - goal.heading) ** 2 +
                         #(start.speed - goal.speed) ** 2)

class AirSimpleGCost(object):
    """ Contains a simple gcost for two states """
    SpeedTable = {1:0.0008, 2:0.0007, 3:0.0006, 4:0.0007,
                  5:0.0008}
    def __call__(self, start, goal):
        vert_difference = start.z_loc - goal.z_loc
        v_cost = 0.001 if vert_difference > 0 else -0.0005
        alpha = (1 if abs(start.x_loc - goal.x_loc) == abs(start.y_loc - goal.y_loc)
                 else math.sqrt(2))
        cost = (AirSimpleGCost.SpeedTable[start.speed]*alpha +
                (v_cost if vert_difference != 0 else 0))
        return cost

