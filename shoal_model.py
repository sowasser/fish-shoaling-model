"""
Original, basic shoaling model

Model of shoaling behavior based on the Boids model by Craig Reynolds in 1986,
using the basic code provided in the Flocker example of the Mesa framework for
agent-based modelling in Python. This model is based on 3 parameters that each
agent follows:
    1. Attraction to (coherence with) other agents,
    2. Avoidance of other agents,
    3. Alignment with other agents.

These rules are based on the neighbours each agent perceives within their
'vision' radius. This is a geometrical distance, rather than topological
(Mann et al. 2011). Another version of this model is being constructed
for the topological (set number of neighbours at any distance).

Data is collected on the median absolute deviation of velocity and the nearest
neighbor distance, calculated using a k-d tree, as measures of cohesion.

The model is based on an toroidal (unbounded & wrapping), 2D area. Later
versions will be 3D, bounded and include obstacles, environmental gradients,
and agents with goal-, food-, or safety-seeking behaviour.

This script also includes the code for visualizing the model using an HTML5
object. The parameters for the visualization rely on a JavaScript canvas.
This script uses the NEW version of Mesa and is currently not fully working.
"""

import numpy as np
import math  # why can't this module be found (5Dec17)?
import random
from scipy.spatial import KDTree
from statsmodels.robust.scale import mad
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

# Todo: Build an arrow-shaped avatar for the agents.
# Todo: Manipulate agent color in visualization to match degree of cohesion.


def polar(model):  # WORKS
    """
    Computes median absolute deviation (MAD) from the mean velocity of the
    group. As the value approaches 0, polarization increases.
    In order to find the MAD, the x,y coordinates are converted to radians by
    finding the arc tangent of y/x. The function used pays attention to the
    sign of the input to make sure that the correct quadrant for the angle is
    determined.
    """
    velocity_x = [agent.velocity[0] for agent in model.schedule.agents]
    velocity_y = [agent.velocity[1] for agent in model.schedule.agents]
    angle = []
    for (y, x) in zip(velocity_y, velocity_x):
        a = math.atan2(y, x)
        angle.append(a)
    return mad(np.asarray(angle), center=np.median)


def nnd(model):  # WORKS
    """
    Computes the average nearest neighbor distance for each agent as another
    measure of cohesion. Method finds & averages the nearest neighbours
    using a KDTree, a machine learning concept for clustering or
    compartmentalizing data. Right now, the 5 nearest neighbors are considered.
    """
    fish = np.asarray([agent.pos for agent in model.schedule.agents])
    fish_tree = KDTree(fish)
    means = []
    for me in fish:
        neighbors = fish_tree.query(x=me, k=6)  # includes agent @ dist = 0
        dist = list(neighbors[0])  # select dist not neighbor # from .query output
        dist.pop(0)  # removes closest agent - itself @ dist = 0
        mean_dist = sum(dist) / len(dist)
        means.append(mean_dist)
    return sum(means) / len(means)


class Fish(Agent):
    """
    A Boid-style agent. Boids have a vision that defines the radius in which
    they look for their neighbors to flock with. Their heading (a unit vector)
    and their interactions with their neighbors - cohering and avoiding -
    define their movement. Separation is their desired minimum distance from
    any other Boid.
    """
    def __init__(self, unique_id, model, pos, speed, velocity, vision,
                 separation, cohere=0.025, separate=0.25, match=0.04):
        """
        Create a new Boid (bird, fish) agent.
        Args:
            unique_id: Unique agent identifier.
            pos: Starting position
            speed: Distance to move per step.
            velocity: numpy vector for the Boid's direction of movement.
            vision: Radius to look around for nearby Boids.
            separation: Minimum distance to maintain from other Boids.
            cohere: the relative importance of matching neighbors' positions
            separate: the relative importance of avoiding close neighbors
            match: the relative importance of matching neighbors' headings
        """
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.separation = separation
        self.cohere_factor = cohere
        self.separate_factor = separate
        self.match_factor = match

    def cohere(self, neighbors):
        """
        Return the vector toward the centroid of the local neighbors.
        """
        cohere = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                cohere += self.model.space.get_heading(self.pos, neighbor.pos)
            cohere /= len(neighbors)
        return cohere

    def separate(self, neighbors):
        """
        Return a vector away rom any neighbors closer than avoidance distance.
        """
        me = self.pos
        them = (n.pos for n in neighbors)
        separate_vector = np.zeros(2)
        for other in them:
            if self.model.space.get_distance(me, other) < self.separation:
                separate_vector -= self.model.space.get_heading(me, other)
        return separate_vector

    def match_velocity(self, neighbors):
        """
        Have Boids match the velocity of neighbors.
        """
        match_vector = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                match_vector += neighbor.velocity
            match_vector /= len(neighbors)
        return match_vector

    def step(self):
        """ 
        Get the Boid's neighbors, compute the new vector, and move accordingly.
        """
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        self.velocity += (self.cohere(neighbors) * self.cohere_factor +
                          self.separate(neighbors) * self.separate_factor +
                          self.match_velocity(neighbors) * self.match_factor) / 2
        self.velocity /= np.linalg.norm(self.velocity)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, new_pos)


class ShoalModel(Model):
    """ Shoal model class. Handles agent creation, placement and scheduling. """

    def __init__(self,
                 population=100,
                 width=100,
                 height=100,
                 speed=1,
                 vision=10,
                 separation=2,
                 cohere=0.025,
                 separate=0.25,
                 match=0.04):
        """
        Create a new Boids model. Args:
            N: Number of Boids
            width, height: Size of the space.
            speed: how fast the boids should move.
            vision: how far around should each Boid look for its neighbors
            separation: what's the minimum distance each Boid will attempt to
                        keep from any other
            cohere, separate, match: factors for the relative importance of
                                     the three drives.
        """
        self.population = population
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, torus=True,
                                     grid_width=10, grid_height=10)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        self.make_agents()
        self.running = True

    def make_agents(self):
        """ 
        Create N agents, with random positions and starting velocities. 
        """
        for i in range(self.population):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            fish = Fish(i, self, pos, self.speed, velocity, self.vision,
                        self.separation, **self.factors)
            self.space.place_agent(fish, pos)
            self.schedule.add(fish)

        self.datacollector = DataCollector(
            model_reporters={"Polarization": polar,
                             "Nearest Neighbour Distance": nnd})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


###############################################################################


# Create canvas for visualization
class SimpleCanvas(VisualizationElement):
    """ Uses JavaScript file for a simple, continuous canvas. """
    local_includes = ["simple_continuous_canvas.js"]

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        """ Instantiate a new SimpleCanvas """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Simple_Continuous_Module({}, {})"
                       .format(self.canvas_width, self.canvas_height))
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
    portrayal = {"Shape": "circle",
                 "Color": "Blue",
                 "Filled": "true",
                 "r": 3}
    return portrayal


# Create slider for interactive parameter
# Todo: make other model parameters interactive
n_slider = UserSettableParameter(param_type='slider', name='Number of Agents',
                                 value=100, min_value=2, max_value=200, step=1)
speed_slider = UserSettableParameter(param_type='slider', name='Speed',
                                     value=2, min_value=0, max_value=10, step=1)
vision_slider = UserSettableParameter(param_type='slider', name='Vision Radius',
                                      value=10, min_value=0, max_value=20, step=1)
sep_slider = UserSettableParameter(param_type='slider', name='Separation Distance',
                                   value=2, min_value=0, max_value=10, step=1)

# Create canvas, 500x500 pixels
shoal_canvas = SimpleCanvas(fish_draw, 500, 500)
model_params = {
    "population": n_slider,
    "width": 50,
    "height": 50,
    "speed": speed_slider,
    "vision": vision_slider,
    "separation": sep_slider
}

# Create charts for the data collectors
# Todo: include chart titles & improve charts
polar_chart = ChartModule([{"Label": "Polarization", "Color": "Black"}],
                          data_collector_name="datacollector")
#                         chart_title="Polarization")

neighbor_chart = ChartModule([{"Label": "Nearest Neighbour Distance", "Color": "Black"}],
                             data_collector_name="datacollector")
#                            chart_title="Nearest Neighbour Distance")

# Launch server
server = ModularServer(ShoalModel,
                       [shoal_canvas, polar_chart, neighbor_chart],
                       "Boids Model of Shoaling Behavior",
                       model_params)
server.launch()
