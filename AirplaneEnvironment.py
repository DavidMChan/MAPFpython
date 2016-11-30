"""
Airplane Environment Python Implementation
David Chan - 2016

When we set up the environment, the X axis runs from -inf to inf
from West to East. The Y axis runs from inf to -inf from North
to South. The Z-Axis is the height of the aircraft. Heading is
given in 8 divisions. Distances are euclidean in time.

"""


import copy
from itertools import combinations

from AirplaneStates import Heading
from AirplaneStates import AirplaneAction
from AirplaneHeuristics import AirStraightLineHeuristic
from AirplaneHeuristics import AirSimpleGCost
from Util import Util

class AirplaneEnvironment(object):
    """ Environment class describing how airplanes work """

    def __init__(self, min_speed=1, max_speed=5, min_height=5, max_height=30, grid_size=3):
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.grid_size = grid_size
        self.min_height = min_height
        self.max_height = max_height
        self.heuristic = AirStraightLineHeuristic()
        self.distance = AirSimpleGCost()

    def get_actions(self, state):
        """ Get the actions that can be taken from a given state """
        actions = []

        # We generate all legal combination of speed, heading and height
        # changes.
        for speed in range(-1, 2):
            for heading in range(-2, 3):
                for height in range(-1, 2):
                    if (state.speed + speed >= self.min_speed and
                            state.speed + speed <= self.max_speed and
                            state.z_loc + height >= self.min_height and
                            state.z_loc + height <= self.max_height):
                        actions.append(AirplaneAction(speed, height, heading))
        return actions

    def get_neighbors(self, state, conflicts=None):
        """ Get the neighbors of a given state """
        neighbors = []

        # Generate all of the neighbor states
        for action in self.get_actions(state):
            new_state = copy.copy(state)

            # First update the location using the previous heading
            new_state.y_loc += Heading.heading_location_table[state.heading % 8][0]
            new_state.x_loc += Heading.heading_location_table[state.heading % 8][1]

            # Then update the height, heading, and speed
            new_state.z_loc += action.delta_height
            new_state.heading += action.delta_heading
            new_state.heading = new_state.heading % 8
            new_state.speed += action.delta_speed

            #TODO Deal with the time
            new_state.time += 1

            neighbors.append(new_state)

        # Prune the neighbor states for the conflicts
        if conflicts is None:
            return neighbors
        else:
            # We need to check if a moving between the starting state
            # and the new state violates a conflict. If so, we prune
            # that state. For now we're going to use a for loop
            for conflict in conflicts:
                for neighbor in neighbors:
                    if conflict.edge_conflicts_with(state, neighbor):
                        neighbors.remove(neighbor)
            return neighbors

    def find_conflict(self, path_set):
        """ Returns the fisrt conflict in a path if it exists """
        # Generate each pair of paths
        for path1, path2 in combinations(list(path_set.keys()), 2):
            path1_idx = 0
            path2_idx = 0
            path1_p = path_set[path1]
            path2_p = path_set[path2]
            while path1_idx < len(path1_p) or path2_idx < len(path2_p):
                s1 = path1_p[min(path1_idx, len(path1_p)-1)]
                s1_e = path1_p[min(path1_idx + 1, len(path1_p) - 1)]

                s2 = path2_p[min(path2_idx, len(path2_p)-1)]
                s2_e = path2_p[min(path2_idx+1, len(path2_p)-1)]

                if Util.get_overlap((s1.time, s1_e.time),(s2.time,s2_e.time)) != 0:
                    if Util.get_overlap((s1.x_loc, s1_e.x_loc),(s2.x_loc, s2_e.x_loc)) != 0:
                        if Util.get_overlap((s1.y_loc, s1_e.y_loc),(s2.y_loc, s2_e.y_loc)) != 0:
                            if Util.get_overlap((s1.z_loc, s1_e.z_loc),(s2.z_loc, s2_e.z_loc)) != 0:
                                # We have a conflict here.
                                pass

                if (s1_e.time < s2_e.time):
                    path1_idx += 1
                else:
                    path2_idx += 1


        return (1, 2, 3, 4)

    #TODO Implement CBS+CL
