"""
Utility classes
David Chan - 2016
"""

class Util(object):
    """ Exports utility methods """
    @staticmethod
    def get_overlap(a_val, b_val):
        """ Get the overlap between two intervals """
        return max(0, min(a_val[1], b_val[1]) - max(a_val[0], b_val[0]))

