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
from math import atan2
import random
from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule


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
        a = atan2(y, x)
        angle.append(a)
    stdev_h = np.std(angle, axis=None)

    return stdev_h

# def nnd(model):
    # """
    # Computes the average nearest neighbor distance for each agent as another
    # measure of cohesion.
    # """


class Fish(Agent):
    """
    A Boid-style agent. Boids have a vision that defines the radius in which
    they look for their neighbors to flock with. The units of this vision are
    unclear, however. Their speed (a scalar) and heading (a unit vector) define
    their movement. Avoidance is their desired minimum distance from any other agent.
    """
    def __init__(self, unique_id, model, pos, speed=5, heading=None,
                 vision=5, avoidance=1):
        """
        Create a new Boid agent. Args:
            unique_id: Unique agent identifier.
            pos: Starting position
            speed: Distance to move per step.
            heading: numpy vector for the Boid's direction of movement.
            vision: Radius to look around for nearby Boids.
            avoidance: Minimum distance to maintain from other Boids.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.speed = speed
        if heading is not None:
            self.heading = heading
        else:
            self.heading = np.random.random(2)
            # Heading is then divided by the 2-, or Euclidean, norm, the
            # straight-line distance between two points. As far as I understand
            self.heading /= np.linalg.norm(self.heading)
        self.vision = vision
        self.avoidance = avoidance

    def cohere(self, neighbors):
        """ Return the vector for each individual agent toward the center of
        mass of the local neighbors. This is done by finding the center of the
        neighbors and then creating a vector towards it. To calculate the
        vector needed to add to the heading of the agent to find the coherence
        vector, the "head-minus-tail" rule is applied: vSourcetoDestination =
        vSource - VDestination.
        """
        my_pos = np.array(self.pos)
        coh_vector = np.array([0, 0])
        dist = np.array([0.0, 0.0])
        for neighbor in neighbors:
            center = np.array(neighbor.pos) / len(neighbors)
            dist = np.linalg.norm(my_pos - center)
            return dist
        coh_vector += np.int64(dist - self.heading)
        return coh_vector

    def separate(self, neighbors):
        """ Return a vector away from any neighbors closer than avoidance dist. """
        my_pos = np.array(self.pos)
        sep_vector = np.array([0, 0])
        for neighbor in neighbors:
            their_pos = np.array(neighbor.pos)
            dist = np.linalg.norm(my_pos - their_pos)
            if dist < self.avoidance:
                sep_vector -= np.int64(their_pos - my_pos)
        return sep_vector

    def step(self):
        """
        Get the Boid's neighbors, compute the new vector, and move accordingly,
        but the agents no longer attempt to match their heading to others.
        Their new heading is dependent on their desire ot cohere & to separate.
        """
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        if len(neighbors) > 0:
            cohere_vector = self.cohere(neighbors)
            separate_vector = self.separate(neighbors)
            self.heading += (cohere_vector +
                             separate_vector)
            self.heading /= np.linalg.norm(self.heading)
        new_pos = np.array(self.pos) + self.heading * self.speed
        new_x, new_y = new_pos
        self.model.space.move_agent(self, (new_x, new_y))


class ShoalModel(Model):
    """ Shoal model class. Handles agent creation, placement and scheduling. """

    def __init__(self, n, width, height, speed, vision, avoidance):
        """
        Create a new Flockers model. Args:
            N: Number of agents
            width, height: Size of the space.
            speed: How fast should the agents move.
            vision: How far around should each agent should look for its
                    neighbors
            avoidance: What's the minimum distance each agent will attempt to
                       keep from any other

        Also includes data collection for analysis of the model.
        """
        self.num_agents = n
        self.vision = vision
        self.speed = speed
        self.avoidance = avoidance
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True,
                                     grid_width=10, grid_height=10)
        self.running = True

        for i in range(self.num_agents):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = (x, y)
            heading = np.random.random(2) * 2 - np.array((1, 1))
            heading /= np.linalg.norm(heading)
            fish = Fish(i, self, pos, self.speed, heading, self.vision,
                        self.avoidance)
            self.space.place_agent(fish, pos)
            self.schedule.add(fish)

        # Creating the data collector, which reports the output of a function
        # (polar, the average agent heading) for each step of the model. This
        # is a "model-level" reporter, but agent-level is also available.
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
    canvas_height = 500
    canvas_width = 500

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
    """
    Right now, the only option for shape is circle or rectangle (rect).
    Working on creating a triangle or arrow option so the agents' heading
    is explicit in the visualization. Future improvements will hopefully also
    include changes in color with degrees of cohesion and a dot for the
    centroid/center of mass.
    """
    return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "Blue"}
    # return {"Shape": "rect", "w": 0.02, "h": 0.02, "Filled": "true", "Color": "Blue"}
    # return {"Shape": "triangle", "w": 4, "h": 4, "Filled": False, "Color": "Blue", "heading": }


# Create canvas, 500x500 pixels
shoal_canvas = SimpleCanvas(fish_draw, 500, 500)

# Create chart of polarization
polarization_chart = ChartModule([{"Label": "Polarization", "Color": "Black"}],
                                 data_collector_name="datacollector")

# Launch server
server = ModularServer(ShoalModel,  # Model class to be visualized
                       [shoal_canvas, polarization_chart],  # List of objects to include
                       "Boid Model of Shoaling Behavior",  # Title of the model
                       # Input agent #, width, height, vision, speed, avoidance
                       100, 100, 100, 5, 5, 2)
server.launch()
