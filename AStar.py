"""
Graph Simple AStar Algorithm
David Chan - 2016
"""

import Queue
from collections import defaultdict

from Printer import printv


def reconstruct_path(trace, start, goal):
    """ Reconstruct a path from a search trace """
    if start == goal:
        return []
    else:
        return reconstruct_path(trace, start, trace[goal]) + [goal]

def astar(environment, start, goal, conflicts=None, maxDeviation=2.0):
    """ Perform A* Search on an environment from a start to a goal """
    # Set the closed set to null
    closed_set = []
    # Setup the open set and enqueue the start at cost 0
    open_set = Queue.PriorityQueue()
    # Set up dictionary for recording the paths
    came_from = {}
    # Setup G-Score table
    gscore = defaultdict(lambda: float('inf'))
    gscore[start] = 0

    # Setup F-Score table
    fscore = defaultdict(lambda: float('inf'))
    best = fscore[start] = environment.heuristic(start, goal)
    open_set.put((fscore[start], start))

    printv("Planning from", str(start), "to", str(goal),verbosity=1)
    examined_nodes = 0
    generated_nodes = 1

    while not open_set.empty():
        # Get the open node
        current_node = open_set.get()
        examined_nodes += 1
        #print("Looking at ", str(current_node[1]), "with cost",
        #      str(current_node[0]), "target", str(goal))
        #if examined_nodes % 1000 == 0:
        #    print(current_node[0])

        # If equality, return the reconstructed path
        if current_node[1] == goal:
            printv("Expanded Nodes:", examined_nodes, "Generated Nodes:", generated_nodes,verbosity=2)
            return reconstruct_path(came_from, start, current_node[1])

        if current_node[1] in closed_set:
            continue
        closed_set.append(current_node[1])

        for node in environment.get_neighbors(current_node[1], conflicts):
            generated_nodes += 1
            if node in closed_set:
                continue

            new_gscore = gscore[current_node[1]] + environment.distance(current_node[1], node)
            if new_gscore < gscore[node]:
                came_from[node] = current_node[1]
                gscore[node] = new_gscore
                fscore[node] = gscore[node] + environment.heuristic(node, goal)
                if fscore[node] < maxDeviation*best:
                  open_set.put((fscore[node], node))
    return [[]]
