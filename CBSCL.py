"""
CBS+CL Python implementation
David Chan - 2016
"""

import copy
import Queue
import AStar

class CBSCLNode(object):
    """ Node which is a part of the CBS tree """
    def __init__(self):
        self.conflict = None
        self.agent = None
        self.parent = None
        self.paths = {}

class EnvironmentContainer(object):
    """ Class containing environments """
    def __init__(self, environment, conflicts):
        self.environment = environment
        self.conflicts = conflicts

    def __eq__(self, other):
        return self.conflicts == other.conflicts
    def __ne__(self, other):
        return not self == other
    def __lt__(self, other):
        return self.conflicts < other.conflicts
    def __gt__(self, other):
        return self.conflicts > other.conflicts

class CBSCL(object):
    """ Class containing CBS methods for an environment """
    def __init__(self, environments):
        self.agents = {}
        self.open_list = Queue.PriorityQueue()
        self.environments = environments
        self.environments.sort()
        self.tree = {}
        self.plan_finished = True
        root = CBSCLNode()
        root.parent = 0
        self.tree[0] = root
        self.best_node = 0
        self.last_created = 0

    def add_agent(self, agent):
        """ Add an agent to the CBS structure """
        self.agents[agent] = 0
        agent_optimal = AStar.astar(self.environments[0], agent.start, agent.goal)
        self.tree[0].paths[agent] = agent_optimal
        print("Added agent", len(self.agents), "with path from",
              str(agent.start), "to", str(agent.goal))
        self.plan_finished = False
        tree_root = self.tree[0]
        self.tree.clear()
        self.tree[0] = tree_root
        self.last_created = 0
        self.open_list.put((0, 0))

    def replan(self, node):
        """ Replan an internal CBS tree node """
        # Get the unit to replan
        agent_to_replan = self.tree[node].agent

        # Find the conflicts that need to be avoided
        num_conflicts = 0
        conflicts = []
        temp_location = node
        while temp_location != 0:
            if self.tree[temp_location].agent == agent_to_replan:
                conflicts.append(self.tree[temp_location].conflict)
                num_conflicts += 1
            temp_location = self.tree[temp_location].parent

        # Plan the agent
        path = AStar.astar(self.environments[self.agents[agent_to_replan]], agent_to_replan.start,
                           agent_to_replan.goal, conflicts)
        if path is None:
            return False

        # Add the path to the tree
        self.tree[node].paths[agent_to_replan] = path
        return True

    def expand_cbs_node(self):
        """ Expand a single CBS+CL node if necessary """
        # If this is the case, then no expansion is necessary
        if self.plan_finished:
            return True

        # Look for a conflict in the best node
        (conflict_l1, conflict_a1, conflict_l2, conflict_a2) = self.environments[-1].find_conflict(
            self.tree[self.best_node].paths)

        # If there are no conflicts, we don't need to keep expanding
        if conflict_a1 is None and conflict_a2 is None:
            self.plan_finished = True
            return True

        # Otherwise setup the first child node
        self.tree[self.last_created + 1] = copy.deepcopy(self.tree[self.best_node])
        self.tree[self.last_created + 1].conflict = conflict_l1
        self.tree[self.last_created + 1].agent = conflict_a1
        self.tree[self.last_created + 1].parent = self.best_node

        # Setup the next child node
        self.tree[self.last_created + 2] = copy.deepcopy(self.tree[self.best_node])
        self.tree[self.last_created + 2].conflict = conflict_l2
        self.tree[self.last_created + 2].agent = conflict_a2
        self.tree[self.last_created + 2].parent = self.best_node

        # Promote agents while they have no solutions
        satisfiable_n1 = True
        satisfiable_n2 = True
        while not self.replan(self.last_created + 1):
            if self.agents[self.tree[self.last_created + 1].agent] == len(self.environments):
                satisfiable_n1 = False
                break
            else:
                self.agents[self.tree[self.last_created + 1].agent] += 1

        while not self.replan(self.last_created + 2):
            if self.agents[self.tree[self.last_created + 2].agent] == len(self.environments):
                satisfiable_n2 = False
                break
            else:
                self.agents[self.tree[self.last_created + 2].agent] += 1

        #Figure out path costs and add to open list
        self.open_list.put((sum([self.environments[self.agents[x]].get_path_cost(
            self.tree[self.last_created + 1].paths[x])
                                 for x in self.tree[self.last_created + 1].paths.keys()]),
                            self.last_created+1) if satisfiable_n1 else float("inf")
                          )
        self.open_list.put((sum([self.environments[self.agents[x]].get_path_cost(
            self.tree[self.last_created + 2].paths[x])
                                 for x in self.tree[self.last_created + 2].paths.keys()]),
                            self.last_created+2) if satisfiable_n2 else float("inf")
                          )

        self.last_created += 2

        # Update the best node
        temp_node = self.open_list.get()[1]
        if temp_node[0] == float("inf"):
            return False
        else:
            self.best_node = temp_node[1]
            return True


    def get_plan_finished(self):
        """ Get if the CBS has a completed valid plan """
        return self.plan_finished
