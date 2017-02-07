"""
Model of shoaling behavior based on the Boids model by Craig Reynolds in 1986,
using the basic code provided in the Flocker example of the Mesa framework for
agent-based modelling in Python. This model is based on 3 parameters that each
agent follows:
    1. Attraction to other agents,
    2. Separation from other agents,
    3. Alignment between agents (polarization).
The model is based on a bounded, 3D area. Later additions will include
obstacles, environmental gradients, and agents with a goal - food-seeking, or
safety-seeking.
"""

import numpy as np
import random
from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
# from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
# from mesa.visualization.modules import ChartModule


# def cohesion(model):  # How cohesion is computed, collected as the model runs


# def nnd(model):  # Nearest neighbor distance, collected as the model runs


class Fish(Agent):
    """
    A Boid-style agent. Boids have a vision that defines the radius in which
    they look for their neighbors to flock with. Their speed (a scalar) and
    heading (a unit vector) define their movement. Separation is their desired
    minimum distance from any other Boid.
    """
    def __init__(self, unique_id, model, pos, speed=5, heading=None,
                 vision=5, separation=1):
        """
        Create a new Boid agent. Args:
            unique_id: Unique agent identifier.
            pos: Starting position
            speed: Distance to move per step.
            heading: numpy vector for the Boid's direction of movement.
            vision: Radius to look around for nearby Boids.
            separation: Minimum distance to maintain from other Boids.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.speed = speed
        if heading is not None:
            self.heading = heading
        else:
            self.heading = np.random.random(2)
            self.heading /= np.linalg.norm(self.heading)
        self.vision = vision
        self.separation = separation

    def cohere(self, neighbors):
        """ Return the vector toward the center of mass of the local neighbors. """
        center = np.array([0.0, 0.0])
        for neighbor in neighbors:
            center += np.array(neighbor.pos)
        return center / len(neighbors)

    def separate(self, neighbors):
        """ Return a vector away from any neighbors closer than separation dist. """
        my_pos = np.array(self.pos)
        sep_vector = np.array([0, 0])
        for neighbor in neighbors:
            their_pos = np.array(neighbor.pos)
            dist = np.linalg.norm(my_pos - their_pos)
            if dist < self.separation:
                sep_vector -= np.int64(their_pos - my_pos)
        return sep_vector

    def match_heading(self, neighbors):
        """ Return a vector of the neighbors' average heading. """
        mean_heading = np.array([0, 0])
        for neighbor in neighbors:
            mean_heading += np.int64(neighbor.heading)
        return mean_heading / len(neighbors)

    def step(self):
        """ Get the Boid's neighbors, compute the new vector, and move accordingly."""
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        if len(neighbors) > 0:
            cohere_vector = self.cohere(neighbors)
            separate_vector = self.separate(neighbors)
            match_heading_vector = self.match_heading(neighbors)
            self.heading += (cohere_vector +
                             separate_vector +
                             match_heading_vector)
            self.heading /= np.linalg.norm(self.heading)
        new_pos = np.array(self.pos) + self.heading * self.speed
        new_x, new_y = new_pos
        self.model.space.move_agent(self, (new_x, new_y))


class ShoalModel(Model):
    """ Shoal model class. Handles agent creation, placement and scheduling. """

    def __init__(self, N, width, height, speed, vision, separation):
        """
        Create a new Flockers model. Args:
            N: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            separation: What's the minimum distance each Boid will attempt to
                       keep from any other
        """
        self.N = N
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True,
                                     grid_width=10, grid_height=10)
        self.make_agents()
        self.running = True

    def make_agents(self):
        """ Create N agents, with random positions and starting headings. """
        for i in range(self.N):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = (x, y)
            heading = np.random.random(2) * 2 - np.array((1, 1))
            heading /= np.linalg.norm(heading)
            fish = Fish(i, self, pos, self.speed, heading, self.vision,
                        self.separation)
            self.space.place_agent(fish, pos)
            self.schedule.add(fish)

        # self.datacollector = DataCollector(
            # model_reporters={"Cohesion": cohesion},  # Measure of cohesion
            # agent_reporters={"NND": nnd})  # Nearest neighbor distance

    def step(self):
        # self.datacollector.collect(self)  # Collect data at each step
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
                 "r": 3,
                 "Color": "Blue"}  # radius of circle
    return portrayal


# chart = ChartModule([{"Label": "(data to be collected",
                      # "Color": "Black"}],
                    # data_collector_name="datacollector")


class SimpleCanvas(VisualizationElement):
    local_includes = ["simple_continuous_canvas.js"]
    portrayal_method = None
    canvas_height = 500
    canvas_width = 500

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        """
        Instantiate a new SimpleCanvas
        """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Simple_Continuous_Module({}, {})".
                       format(self.canvas_width, self.canvas_height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []
        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)
            x, y = obj.pos
            x = ((x - model.space.x_min) /
                 (model.space.x_max - model.space.x_min))
            y = ((y - model.space.y_min) /
                 (model.space.y_max - model.space.y_min))
            portrayal["x"] = x
            portrayal["y"] = y
            space_state.append(portrayal)
        return space_state


def fish_draw(agent):
    return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "Blue"}

shoal_canvas = SimpleCanvas(fish_draw, 500, 500)
server = ModularServer(ShoalModel, [shoal_canvas],  # [chart]
                       "Boid Model of Shoaling Behavior",
                       100, 100, 100, 5, 10, 2)
server.launch()
