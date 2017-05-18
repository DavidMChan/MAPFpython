"""
Graph Environment Python Implementation
David Chan - 2016

When we set up the environment, the X axis runs from -inf to inf
from West to East. The Y axis runs from inf to -inf from North
to South. The Z-Axis is the height of the aircraft. Heading is
given in 8 divisions. Distances are euclidean in time.
#TODO Update the heading table to reflect changes in the environment

"""


import copy
import json
import os

from itertools import combinations

from GraphStates import GraphConflict
from GraphAgent import GraphAgent
from GraphHeuristics import StraightLineHeuristic
from GraphHeuristics import SimpleGCost
from Util import Util
from Printer import printv


class GraphEnvironment(object):
    """ Environment class containing the graph """

    def __init__(self, params={}):
        """ Initialization:
              Set graph vertices via dict: {"vertexName1":("vertexName1",(xcoord,ycoord)),...}
              Set graph edges via dict: {"vertexName1":["vertexName2","vertexName3",...],...}s
"""
        self.heuristic = StraightLineHeuristic()
        self.distance = SimpleGCost()
        if "graphVertices" in params.keys():
          self.v = params["graphVertices"]
        elif "vertexFileJson" in params.keys():
          self.v = json.loads(open(params["vertexFileJson"]).read())

        if "graphEdges" in params.keys():
          self.e = params["graphEdges"]
        elif "edgeFileJson" in params.keys():
          self.e = json.loads(open(params["edgeFileJson"]).read())

        # Turn all lists into tuples so that they will be hashable
        for vv in self.v:
          self.v[vv]=tuple(tuple(x) if type(x) is list else x for x in self.v[vv])
        for ee in self.e:
          self.e[ee]=tuple(tuple(x) if type(x) is list else x for x in self.e[ee])

    def parse_instance_file(self, filename):
        result=[]
        printv("Decode "+filename,verbosity=2)
        val=json.loads(open(filename).read())
        for n in val:
            #result.append(GraphAgent(self.v[n["Src"]],self.v[n["Dst"]],n["Src"]+"_"+n["Dst"]))
            result.append(GraphAgent(self.v[n[0]],self.v[n[1]],'_'.join(n)))
        return result

    def parse_json_instance(self, jsonStr):
        """ Parse a list of problem instances from JSON """
        result=[]
        val=json.loads(jsonStr)
        for n in val:
            result.append(GraphAgent(self.v[n[0]],self.v[n[1]],'_'.join(n)))
        return result

    def get_actions(self, state):
        """ Get the actions that can be taken from a given vertex """
        return [self.v[n] for n in self.e[state[0]]]

    def get_neighbors(self, state, conflicts=None):
        """ Get the neighbors of a given state """
        return self.get_actions(state)

    def find_conflict(self, path_set):
        """ Returns the first conflict in a path if it exists """
        return (None,None,None,None)
