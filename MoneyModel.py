"""
This is the tutorial from Mesa: a simple agent-based economic model with the
following rules:

    1. There are some number of agents.
    2. All agents begin with 1 unit of money
    3. At every step of the model, an agent gives 1 unit of money (if they have
    it) to some other agent.

"""

from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
from mesa.space import MultiGrid
import matplotlib.pyplot as plt


def compute_gini(model):
    """
    Collects Gini Coefficient, a measure of wealth inequality, to be measured
    at every step of the model

    """
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N-i) for i, xi in enumerate(x)) / (N*sum(x))
    return 1 + (1/N) - 2*B


class MoneyAgent(Agent):
    """
    Creates the agents - individuals with fixed initial wealth,
    includes unique identifier

    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1  # Starting wealth of the agent is 1

    def move(self):
        """
        Defines the space that the agents inhabit, in this case a grid, and the
        movement of agents to a neighboring cell

        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            # Moore cell neighborhood means agents can move to diagonal cells
            # vs. Von-Neumann
            include_center=False)  # Center cell is not considered a neighboring cell
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        """ Finds all the agents present in a cell and gives one some money """
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:  # if there is more than one cellmate
            other = random.choice(cellmates)
            # defines the 'other' random agent that will receive money
            other.wealth += 1  # other agent gets +1 money
            self.wealth -= 1  # original agent -1 money

    def step(self):
        """
        The step(s) the agent takes, if the agent has money (>0), calls the
        give_money method

        """
        self.move()
        if self.wealth > 0:
            self.give_money()


class MoneyModel(Model):
    """ A model with some number of agents. """
    def __init__(self, N, width, height):
        self.num_agents = N  # Number of agents
        self.grid = MultiGrid(width, height, True)
        # Multiple agents allowed per grid, set dimensions
        self.schedule = RandomActivation(self)
        # Activates all agents once per step, in random order
        self.running = True

        for i in range(self.num_agents):  # Create agents
            a = MoneyAgent(i, self)
            self.schedule.add(a)  # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            # Places agent at a given set of coordinates (x, y)

        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": lambda a: a.wealth})

    def step(self):
        self.datacollector.collect(self)  # Collect data at each step
        self.schedule.step()


"""
Set up and run the BatchRunner, which runs the model multiple times with fixed
parameters to determine the overall distributions of the model - automated by Mesa

"""
parameters = {"width": 10,  # Width of the cell
              "height": 10,  # Height of the cell
              "N": range(10, 500, 10)}  # Vary # of agents from 10 to 500 in units of 10

batch_run = BatchRunner(MoneyModel,
                        parameters,
                        iterations=5,
                        # 5 instantiations of the model with each number of agents
                        max_steps=100,  # Run each for 100 steps
                        model_reporters={"Gini": compute_gini})  # Collect Gini value

batch_run.run_all()


# Data collection methods
# Extract data as a DataFrame
run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.Gini)
