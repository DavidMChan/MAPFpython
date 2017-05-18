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
import sys, json
import os.path



def parse_args():
    """ Parse the command line arguments for the driver """
    parser = argparse.ArgumentParser(description="Solve MAPF Instance")
    parser.add_argument("-n", "--num-agents", type=int, default=5,
                        help="Number of agents to simulate. default=5")
    parser.add_argument("-s", "--seed", type=int, default=None,
                        help="Seed for random number generator. default=None")
    parser.add_argument("-e", "--environments", default="AirplaneEnvironment",
                        help="Comma-delim list of environment names. default=AirplaneEnvironment")
    parser.add_argument("-p", "--environment-params", default=None,
                        help="List of environment params as a json string.\n\tex: '[{\"min_speed\":1,\"max_speed\":5,\"min_height\":5,\"max_height\":30,\"grid_size\":3},{...},{...}]'\n\tdefault=None")
    parser.add_argument("-a", "--agent-type", default="AirplaneAgent",
                        help="Agent type name. default=AirplaneAgent")
    parser.add_argument("-x", "--visual", action='store_true',
                        help="Display simulation. default=off")
    parser.add_argument("-v", nargs='?', action=Util.VAction, dest='verbose',
                        help="Print verbose output. default=off")
    parser.add_argument("-i", "--problem-instances", default=None,
                        help="JSON string containing a problem instances, or a file or directory containing files with MAPF problem instances. default=None~generate one random instance")
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

    env_names = GLOBAL_ARGS.environments.split(",")
    env_params = json.loads(GLOBAL_ARGS.environment_params) if GLOBAL_ARGS.environment_params is not None else [None]*len(env_names)

    if len(env_names)!=len(env_params):
      print "ERROR: number of envs must match number of params"
      sys.exit(1)

    envs = []
    for environment,param in zip(env_names,env_params):
        printv('Loading: '+environment+' - '+json.dumps(param),verbosity=2)
        #TODO Make this less dangerous
        exec("from %s import %s"%(environment, environment))
        # Make an Environment
        #TODO Make this less dangerous
        if param is None:
          envs.append(eval("%s()"%environment))
        else:
          envs.append(eval("%s(json.loads('%s'))"%(environment,json.dumps(param))))

    instances=[]
    # Generate random agents
    #TODO Make this less dangerous
    if GLOBAL_ARGS.problem_instances is None:
      instances.append(eval("[%s.random_agent(envs[0]) for _ in range(0, GLOBAL_ARGS.num_agents)]"%GLOBAL_ARGS.agent_type))
    else:
      if os.path.exists(GLOBAL_ARGS.problem_instances):
        if os.path.isdir(GLOBAL_ARGS.problem_instances):
          for f in os.listdir(GLOBAL_ARGS.problem_instances):
            if os.path.isfile(f):
              instances.append(envs[0].parse_instance_file(f))
        elif os.path.isfile(GLOBAL_ARGS.problem_instances):
          instances.append(envs[0].parse_instance_file(GLOBAL_ARGS.problem_instances))
      else:
        instances.append(envs[0].parse_json_instance(GLOBAL_ARGS.problem_instances))

    # Make a new CBS
    main_cbs = CBSCL(envs)

    # Add them to the CBS
    for instance in instances:
      for agent in instance:
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


