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
        
# From: http://stackoverflow.com/questions/6076690/verbose-level-with-argparse-and-multiple-v-options
import argparse
class VAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        if values is None:
            values='1'
        try:
            values=int(values)
        except ValueError:
            values=values.count('v')+1
        setattr(args, self.dest, values)

