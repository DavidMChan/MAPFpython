"""
Set of classes describing important airplane information
David Chan - 2016
"""

from Util import Util

class Heading(object):
    """ Describes the heading of the agent """
    North = 0
    North_East = 1
    East = 2
    South_East = 3
    South = 4
    South_West = 5
    West = 6
    North_West = 7

    heading_location_table = {0:(0, 1), 1:(1, 1), 2:(1, 0), 3:(1, -1), 4:(0, -1),
                              5:(-1, -1), 6:(-1, 0), 7:(-1, 1)}

class AirplaneState(object):
    """ State class for an airplane """
    def __init__(self, x_loc=None, y_loc=None, z_loc=None, time=None, heading=None, speed=None):
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.z_loc = z_loc
        self.speed = speed
        self.heading = heading
        self.time = time

    def __eq__(self, other):
        return (self.x_loc == other.x_loc and self.y_loc == other.y_loc and
                self.z_loc == other.z_loc)# and self.speed == other.speed and
                #self.heading == other.heading) # States are equal regardless of time

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return (self.x_loc.__hash__() + self.y_loc.__hash__() + self.z_loc.__hash__() +
                self.speed.__hash__() + self.heading.__hash__()).__hash__()

    def __str__(self):
        return ("(" + str(self.x_loc) + "," + str(self.y_loc) + "," + str(self.z_loc) +
                "," + str(self.speed) + "," + str(self.heading) + "," + str(self.time) + ")")

class AirplaneAction(object):
    """ Class describing an airplane action that can be taken """
    def __init__(self, delta_speed=0, delta_height=0, delta_heading=0):
        self.delta_speed = delta_speed
        self.delta_height = delta_height
        self.delta_heading = delta_heading


class AirplaneConflict(object):
    """ Class describing a conflict """
    def __init__(self, x_bounds, y_bounds, z_bounds, t_bounds):
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.z_bounds = z_bounds
        self.t_bounds = t_bounds

    def edge_conflicts_with(self, state_from, state_to):
        """ Check if a from/to state conflicts on the edge with this """
        state_x_interval = (min(state_from.x_loc, state_to.x_loc),
                            max(state_from.x_loc, state_to.x_loc))
        state_y_interval = (min(state_from.y_loc, state_to.y_loc),
                            max(state_from.y_loc, state_to.y_loc))
        state_z_interval = (min(state_from.z_loc, state_to.z_loc),
                            max(state_from.z_loc, state_to.z_loc))
        state_t_interval = (min(state_from.time, state_to.time),
                            max(state_from.time, state_to.time))
        if (Util.get_overlap(state_t_interval, self.t_bounds) == 0 or
                Util.get_overlap(state_x_interval, self.x_bounds) == 0 or
                Util.get_overlap(state_y_interval, self.y_bounds) == 0 or
                Util.get_overlap(state_z_interval, self.z_bounds) == 0):
            return True
        return False

    def point_conflicts_with(self, state):
        """ Check if a state conflicts pointwise with a particular state """
        return AirplaneConflict.edge_conflicts_with(self, state, state)

