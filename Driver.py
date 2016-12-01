"""
Driver/Testing class for the airplane CBS
David Chan - 2016
"""

from CBS import CBS
from AirplaneAgent import AirplaneAgent
from AirplaneEnvironment import AirplaneEnvironment

def main():
    """ Main method """
    # Generate 5 random agents
    agents = [AirplaneAgent.random_agent() for _ in range(0, 2)]

    # Make an Environment
    airplane_env = AirplaneEnvironment()

    # Make a new CBS
    main_cbs = CBS(airplane_env)

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


