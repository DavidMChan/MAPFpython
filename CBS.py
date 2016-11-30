"""
CBS Python implementation
David Chan - 2016
"""

import copy
import Queue
import AStar


class CBSNode(object):
    """ Node which is a part of the CBS tree """
    def __init__(self):
        self.conflict = None
        self.agent = None
        self.parent = None
        self.paths = {}

class CBS(object):
    """ Class containing CBS methods for an environment """
    def __init__(self, environment):
        self.agents = []
        self.open_list = Queue.PriorityQueue()
        self.environment = environment
        self.tree = {}
        self.plan_finished = True
        root = CBSNode()
        root.parent = 0
        self.tree[0] = root
        self.best_node = 0
        self.last_created = 0

    def add_agent(self, agent):
        """ Add an agent to the CBS structure """
        self.agents.append(agent)
        agent_optimal = AStar.astar(self.environment, agent.start, agent.goal)
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

        # Set the environment conflicts
        self.environment.set_conflicts(conflicts)

        # Plan the agent
        path = AStar.astar(self.environment, agent_to_replan.start, agent_to_replan.goal)

        # Add the path to the tree
        self.tree[node].paths[agent_to_replan] = path

    def expand_cbs_node(self):
        """ Expand a single CBS node if necessary """
        if self.plan_finished:
            return

        (conflict_l1, conflict_a1, conflict_l2, conflict_a2) = self.environment.find_conflict(
            self.tree[self.best_node].paths)
        if conflict_a1 is None and conflict_a2 is None:
            self.plan_finished = True
            return

        # Setup the first child node
        self.tree[self.last_created + 1] = copy.deepcopy(self.tree[self.best_node])
        self.tree[self.last_created + 1].conflict = conflict_l1
        self.tree[self.last_created + 1].agent = conflict_a1
        self.tree[self.last_created + 1].parent = self.best_node

        # Setup the next child node
        self.tree[self.last_created + 2] = copy.deepcopy(self.tree[self.best_node])
        self.tree[self.last_created + 2].conflict = conflict_l2
        self.tree[self.last_created + 2].agent = conflict_a2
        self.tree[self.last_created + 2].parent = self.best_node

        self.replan(self.last_created + 1)
        self.replan(self.last_created + 2)

        #Figure out path costs and add to open list
        self.open_list.put((sum([self.environment.get_path_cost(x)
                                 for x in self.tree[self.last_created + 1].paths]),
                            self.last_created+1)
                          )
        self.open_list.put((sum([self.environment.get_path_cost(x)
                                 for x in self.tree[self.last_created + 2].paths]),
                            self.last_created+2)
                          )

        self.last_created += 2

        # Update the best node
        self.best_node = self.open_list.get()[1]


    def get_plan_finished(self):
        """ Get if the CBS has a completed valid plan """
        return self.plan_finished
