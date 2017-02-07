"""
A model following Quera et al (2015) and their model of collective behaviour
where instead of a boids model with attraction, repulsion, alignment, the model
operates based on satisfaction/dissatisfaction with a zone, outside of which
fish are attracted to each other and inside of which fish are repelled from
each other. Alignment becomes an emergent behaviour.

The model is based in the Flocker model example of the Mesa framework:
https://github.com/projectmesa/mesa/tree/master/examples/Flockers
and the basic MoneyModel tutorial:
http://mesa.readthedocs.io/en/latest/tutorials/intro_tutorial.html
"""

import numpy as np
import random
from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule


class Fish(Agent):
    """
    Creation of the agents/particles that will populate the model, the space
    they inhabit, and their actions per step of the model.
    """
    def __init__(self, unique_id, model, pos, heading=None,
                 vision=5, separation=1):
        """
        Create a new agent. Args:
            unique_id: Unique agent identifier.
            pos: Starting position
            heading: numpy vector for the agents' direction of movement.
            vision: Radius to look around for nearby agents.
            separation: Minimum distance to maintain from other agents.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        if heading is not None:
            self.heading = heading
        else:
            self.heading = np.random.random(2)
            self.heading /= np.linalg.norm(self.heading)
        self.vision = vision
        self.separation = separation

    def move(self):
        """
        Defines the space that the agents inhabit, in this case a grid (3D),
        and the movement of agents to a neighboring cell. Cell neighborhood is
        defined as Moore, rather than von Neumann, which means that agents can
        move to a diagonal cell. Also, the centre cell is not considered a
        neighboring cell.
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def distance(self, neighbors):
        """ Return the real distance to other agents """

    def new_position(self, neighbors):
        """
        Return position with lowest estimated dissatisfaction within
        the neighborhood by comparing real and ideal distances to other
        perceived agents.
        """

    def step(self):
        """
        Agent moves to position with lowest potential dissatisfaction then
        compares predicted real distance to its current real distance from the
        agents it perceives. Agent increases or decreases its ideal distances to
        other agents based on the previous comparison. Distance is then updated by
        """


class ShoalModel(Model):
    """
    A model with some number of agents. Sets the parameters for the running of
    the model, like the agents' initial positions on the grid. Also defines
    what data is to be collected per step of the model.
    """
    def __init__(self, N, width, height):
        self.num_agents = N  # Number of agents
        # Multiple agents allowed per grid, set dimensions
        self.grid = MultiGrid(width, height, True)
        # Activates all agents once per step, in random order
        self.schedule = RandomActivation(self)
        self.running = True

        for i in range(self.num_agents):  # Create agents
            a = Fish(i, self)
            self.schedule.add(a)  # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            # Places agent at a given set of coordinates (x, y)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector()  # What data is to be collected per step

    def step(self):
        """
        The data to be collected is a measure of coordination determined by
        "computing an index that combines the distance and difference in
        heading between the agents at each time step"
        """
        self.datacollector.collect(self)  # Collect data at each step
        self.schedule.step()


def agent_portrayal(agent):
    """
    Canvas grid loops over every cell and generates a portrayal (dictionary) of
    each agent it finds, then tells the JavaScript side how to draw each
    portrayal. In this case, one way if agents have money and different look if
    agents are broke.
    """
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}  # radius of circle
    return portrayal

# Create 10x10 grid, drawn in 500x500 pixels
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = ChartModule([{"Label": "(data to be collected",
                      "Color": "Black"}],
                    data_collector_name="datacollector")


# Launch server
server = ModularServer(ShoalModel,  # Model class to be visualized
                       [grid, chart],  # List of module objects to include
                       "Shoaling Behaviour Model",  # Title of the model
                       # Any inputs for the model: 100 agents, height & width 10
                       100, 10, 10)
server.port = 8889
server.launch()
