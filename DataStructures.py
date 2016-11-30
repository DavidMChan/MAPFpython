"""
Graph Data Structures in Python
David Chan - 2016
"""

import collections

class SimpleGraph(object):
    """ Simple adjacency matrix graph class """
    def __init__(self):
        self.graph = {}
    def neighbors(self, vertex):
        """ Get the neighbors of the vertex """
        return self.graph[vertex]

class Queue(object):
    """ Simple queue class """
    def __init__(self):
        self.elements = collections.deque()
    def empty(self):
        """ Check if the queue is empty """
        return len(self.elements)
    def put(self, element):
        """ Put an element in the queue """
        self.elements.append(element)
    def get(self):
        """ Pop the top element from the queue """
        return self.elements.popleft()
