#!/usr/bin/env python

"""
Driver/Testing class for CBS
David Chan - 2016
"""


import argparse
import random

from CBSCL import CBSCL



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
    parser.add_argument("-x", "--visual", type=bool, default=False,
                        help="Use a visual simulation. default=False")
    parser.add_argument("-v", "--verbose", type=bool, default=False,
                        help="Print verbose output. default=False")
    return parser.parse_args()

# Global argument variable 
#TODO Make this less dangerous for imports
GLOBAL_ARGS = None

def main():
    """ Main method """

    if random.seed is not None:
        random.seed(GLOBAL_ARGS.seed)

    #TODO Make this less dangerous
    exec("from %s import %s"%(GLOBAL_ARGS.agent_type, GLOBAL_ARGS.agent_type))

    # Generate random agents
    #TODO Make this less dangerous
    agents = eval("[%s.random_agent() for _ in range(0, args.num_agents)]"%GLOBAL_ARGS.agent_type)

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
            print "CBS Not solvable. No open nodes with cost <= inf"

    # Print the result
    for agent in main_cbs.tree[main_cbs.best_node].paths.keys():
        print(agent.name, [str(x) for x  in main_cbs.tree[main_cbs.best_node].paths[agent]])



if __name__ == "__main__":
    # Parse the command line arguments
    GLOBAL_ARGS = parse_args()

    # Run the main function
    main()


