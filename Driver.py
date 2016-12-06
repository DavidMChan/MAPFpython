#!/usr/bin/env python

"""
Driver/Testing class for CBS
David Chan - 2016
"""

import __builtin__
import argparse
import random

import Util

from CBSCL import CBSCL
from Printer import printv



def parse_args():
    """ Parse the command line arguments for the driver """
    parser = argparse.ArgumentParser(description="Solve MAPF Instance")
    parser.add_argument("-n", "--num-agents", type=int, default=5,
                        help="Number of agents to simulate. default=5")
    parser.add_argument("-s", "--seed", type=int, default=None,
                        help="Seed for random number generator. default=None")
    parser.add_argument("-e", "--environments", default="AirplaneEnvironment",
                        help="Comma-delim list of environment names. default=AirplaneEnvironment")
    parser.add_argument("-a", "--agent-type", default="AirplaneAgent",
                        help="Agent type name. default=AirplaneAgent")
    parser.add_argument("-x", "--visual", action='store_true',
                        help="Display simulation. default=off")
    parser.add_argument("-v", nargs='?', action=Util.VAction, dest='verbose',
                        help="Print verbose output. default=off")
    args = parser.parse_args()
    if args.verbose is None:
        args.verbose = 0
    return args


def main():
    """ Main method """

    if random.seed is not None:
        random.seed(GLOBAL_ARGS.seed)

    #TODO Make this less dangerous
    exec("from %s import %s"%(GLOBAL_ARGS.agent_type, GLOBAL_ARGS.agent_type))

    # Generate random agents
    #TODO Make this less dangerous
    agents = eval("[%s.random_agent() for _ in range(0, GLOBAL_ARGS.num_agents)]"%GLOBAL_ARGS.agent_type)

    env_names = GLOBAL_ARGS.environments.split(",")

    envs = []
    for environment in env_names:
        #TODO Make this less dangerous
        exec("from %s import %s"%(environment, environment))
        # Make an Environment
        #TODO Make this less dangerous
        envs.append(eval("%s()"%environment))

    # Make a new CBS
    main_cbs = CBSCL(envs)

    # Add them to the CBS
    for agent in agents:
        main_cbs.add_agent(agent)

    # Solve the CBS
    while not main_cbs.plan_finished:
        if not main_cbs.expand_cbs_node():
            printv("CBS Not solvable. No open nodes with cost <= inf")

    # Print the result
    for agent in main_cbs.tree[main_cbs.best_node].paths.keys():
        printv(agent.name, [str(x) for x  in main_cbs.tree[main_cbs.best_node].paths[agent]])



if __name__ == "__main__":
    # Parse the command line arguments
    __builtin__.GLOBAL_ARGS = parse_args()
    printv(GLOBAL_ARGS,verbosity=3)

    # Run the main function
    main()


