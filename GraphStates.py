"""
Set of classes describing graph information
Thayne Walker - 2017
"""

from Util import Util

class GraphState(object):
    """ State class for 2D planar vertex """
    def __init__(self, x_loc=None, y_loc=None, time=None, loc_name=None):
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.time = time
        self.loc_name = loc_name

    def __eq__(self, other):
        return (self.x_loc == other.x_loc and self.y_loc == other.y_loc)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return (self.x_loc.__hash__() + self.y_loc.__hash__())

    def __str__(self):
        return ("(" + self.loc_name + ":" +str(self.x_loc) + "," + str(self.y_loc) + "," + str(self.time) + ")")

# TODO Use Quadratic collision detection
class GraphConflict(object):
    """ Class describing a conflict """

    def conflicts_with(self, state_from, state_to):
       """ Check for edge or vertex conflict """
       return False

