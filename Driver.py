#!/usr/bin/env python

"""
Driver/Testing class for CBS
David Chan - 2016
"""

from CBS import CBS
from CBSCL import CBSCL
from AirplaneAgent import AirplaneAgent
import argparse
import random

def parse_args():
    parser = argparse.ArgumentParser(description="Solve MAPF Instance")
    parser.add_argument("-n", "--num-agents", type=int, default=5, help="Number of agents to simulate. default=5")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Seed for random number generator. default=None")
    parser.add_argument("-e", "--environments", default="AirplaneEnvironment", help="Comma-delimited list of environment names. default=AirplaneEnvironment")
    parser.add_argument("-a", "--agent-type", default="AirplaneAgent", help="Agent type name. default=AirplaneAgent")
    return parser.parse_args()


def main():
    """ Main method """
    # Parse arguments
    args = parse_args()

    if random.seed is not None:
        random.seed(args.seed) 

    exec("from %s import %s"%(args.agent_type,args.agent_type))
    # Generate random agents
    agents = eval("[%s.random_agent() for _ in range(0, args.num_agents)]"%args.agent_type)

    env_names=args.environments.split(",")
    
    envs=[]
    for e in env_names:
        exec("from %s import %s"%(e,e))
        # Make an Environment
        envs.append(eval("%s()"%e))

    print envs
    # Make a new CBS
    main_cbs = CBSCL(envs)

    # Add them to the CBS
    for agent in agents:
        main_cbs.add_agent(agent)

    # Solve the CBS
    while not main_cbs.plan_finished:
        main_cbs.expand_cbs_node()

    # Print the result
    for agent in main_cbs.tree[main_cbs.best_node].paths.keys():
        print(agent.name, [str(x) for x  in main_cbs.tree[main_cbs.best_node].paths[agent]])



if __name__ == "__main__":
    main()


