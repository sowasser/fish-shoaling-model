"""
Model of shoaling behavior based on the Boids model by Craig Reynolds in 1986,
using the basic code provided in the Flocker example of the Mesa framework for
agent-based modelling in Python. This model is based on 2 parameters that each
agent follows:
    1. Attraction to other agents,
    2. Avoidance of other agents.

Heading, though recorded for each agent, is not included in the parameters that
determine an agents' movement. Therefore, polarization becomes an emergent
behaviour and can be analyzed as a measure of cohesion, along with the nearest
neighbour distance. The model is based on a bounded, 3D area. Later additions
will include obstacles, environmental gradients, and agents with goal-, food-,
or safety-seeking behaviour.

This script also includes the code for visualizing the model using an HTML5
object. The parameters for the visualization rely on a JavaScript canvas.
"""

import numpy as np
import math
import random
from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule

# Todo: Constrain space to the canvas so behaviors can be more easily understood.
# Todo: Build an arrow-shaped avatar for the agents.
# Todo: Manipulate agent color in visualization to match degree of cohesion.


def polar(model):
    """
    Computes standard deviation from the mean heading of the group. As the
    value approaches 0, polarization increases.

    Heading is a unit vector, meaning the magnitude is 1 and the direction is
    given as x,y coordinates. In order to find the mean & stdev, the x,y
    (Cartesian) coordinates are converted to angle degrees in radians by
    finding the arc tangent of y/x. The function used to do this is arctan2
    from the math package, which pays attention to the sign of the input to
    make sure that the correct quadrant for the angle is determined. Then, the
    standard deviation is calculated from these values.
    """
    heading_x = [agent.heading[0] for agent in model.schedule.agents]
    heading_y = [agent.heading[1] for agent in model.schedule.agents]
    angle = []
    for (y, x) in zip(heading_y, heading_x):
        a = math.atan2(y, x)
        angle.append(a)
    stdev_h = np.std(angle, axis=None)

    return stdev_h

# def nnd(model):
    # """
    # Computes the average nearest neighbor distance for each agent as another
    # measure of cohesion.
    # """


class Boid(Agent):
    """
    A Boid-style flocker agent. Boids have a vision that defines the radius in
    which they look for their neighbors to flock with. Their heading (a unit
    vector) and their interactions with their neighbors - cohering and avoiding -
    define their movement. Avoidance is their desired minimum distance from
    any other Boid.
    """
    def __init__(self, unique_id, model, pos, heading,
                 vision=10, avoidance=2):
        """
        Create a new Boid (bird, fish) agent. Args:
            unique_id: Unique agent identifier.
            pos: Starting position
            heading: randomly generated then transformed into the unit vector
                     of Boid's movement - no magnitude.
            velocity: Speed of the Boid, calculated as the Euclidean distance
                      (vector norm) of the Boid's heading.
            vision: Radius to look around for nearby Boids.
            avoidance: Minimum distance to maintain from other Boids.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        if heading is not None:
            # Heading is defined within the model. Here, a unit vector is
            # created by dividing it by its magnitude so velocity can be
            #  defined as the magnitude of the heading.
            self.heading = heading
            self.velocity = np.linalg.norm(heading)
            self.heading /= self.velocity
        else:
            # Does not include the upper number, returns array of 2 values
            self.heading = np.random.uniform(-1, 1, 2)
            self.heading /= np.linalg.norm(self.heading)
        self.vision = vision
        self.avoidance = avoidance

    def cohere(self, neighbors):
        """
        Add the vector (direction, not speed) toward the center of mass of the
        local neighbors to the position of each agent to return a new vector
        towards neighbors.
        """
        my_pos = np.array(self.pos)
        coh_vector = np.array([0.0, 0.0])
        for neighbor in neighbors:
            center = np.array(neighbor.pos) / len(neighbors)
            # Vector calculation uses the Head-Minus-Tail rule
            coh_vector += (my_pos - center)
        return coh_vector

    def avoid(self, neighbors):
        my_pos = np.array(self.pos)
        avoid_vector = np.array([0.0, 0.0])
        for neighbor in neighbors:
            if abs(np.linalg.norm(my_pos - neighbor.pos)) > self.avoidance:
                avoid_vector -= (my_pos - neighbor.pos)
            return avoid_vector

    def match_velocity(self, neighbors):
        """
        Have Boids match the velocity (magnitude/Euclidean distance of heading)
        of neighbors.
        """
        my_velocity = self.velocity
        mean_velocity = 0
        for neighbor in neighbors:
            mean_velocity += np.int64(neighbor.velocity)
            mean_velocity /= len(neighbors)
            if my_velocity < mean_velocity:
                my_velocity += mean_velocity - my_velocity
            elif my_velocity > mean_velocity:
                my_velocity -= mean_velocity - my_velocity
        return mean_velocity

    def step(self):
        """ Get the Boid's neighbors, compute the new vector, and move accordingly."""
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        if len(neighbors) > 0:
            cohere_vector = self.cohere(neighbors)
            avoid_vector = self.avoid(neighbors)
            self.heading += (cohere_vector +
                             avoid_vector)
            self.heading /= np.linalg.norm(self.heading)
        new_pos = np.array(self.pos) + self.heading * self.velocity
        new_x, new_y = new_pos
        self.model.space.move_agent(self, (new_x, new_y))


class ShoalModel(Model):
    """ Shoal model class. Handles agent creation, placement and scheduling. """

    def __init__(self, n, width, height, vision, avoidance):
        """
        Create a new Boids model. Args:
            N: Number of agents
            width, height: Size of the space.
            vision: Radius for how far agents look for their neighbors.
            avoidance: The minimum distance each agent will attempt to keep
                       from others.

        Also includes data collection for analysis of the model.
        """
        self.n = n
        self.vision = vision
        self.avoidance = avoidance
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, torus=True,
                                     grid_width=100, grid_height=100)
        self.make_agents()
        self.running = True

    def make_agents(self):
        """ Create N agents, with random positions and starting headings. """
        for i in range(self.n):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = (x, y)
            # Does not include the upper number, returns array of 2 values
            heading = np.random.uniform(-1, 1, 2)
            # heading /= np.linalg.norm(heading)
            boid = Boid(unique_id=i, model=self, pos=pos, heading=heading, vision=self.vision,
                        avoidance=self.avoidance)
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

        # Creating the data collector, which reports the output of a function
        # (polar, the average agent heading) for each step. This is a "model-
        # level" reporter, but agent-level is also available.
        self.datacollector = DataCollector(
            model_reporters={"Polarization": polar})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


###############################################################################


# Create canvas for visualization
class SimpleCanvas(VisualizationElement):
    """ Uses JavaScript file for a simple, continuous canvas. """
    local_includes = ["simple_continuous_canvas.js"]
    portrayal_method = None
    canvas_height = 700
    canvas_width = 700

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        """ Instantiate a new SimpleCanvas """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Simple_Continuous_Module({}, {})".
                       format(self.canvas_width, self.canvas_height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        """ Creates the space in which the agents exist. """
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
    # return {"Shape": "rect", "w": 0.02, "h": 0.02, "Filled": "true", "Color": "Blue"}
    # return {"Shape": "triangle", "w": 4, "h": 4, "Filled": False, "Color": "Blue", "heading": }


# Create canvas, 500x500 pixels
shoal_canvas = SimpleCanvas(fish_draw, 500, 500)

# Create chart of polarization
polarization_chart = ChartModule([{"Label": "Polarization", "Color": "Black"}],
                                 data_collector_name="datacollector")

# Launch server
server = ModularServer(ShoalModel, [shoal_canvas, polarization_chart],
                       "Boid Model of Shoaling Behavior",
                       n=100, width=100, height=100, vision=10, avoidance=2)
server.launch()
