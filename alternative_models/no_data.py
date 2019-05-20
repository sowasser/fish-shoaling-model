"""
Model of shoaling behavior based on the Boids model by Craig Reynolds in 1986,
using the basic code provided in the Flocker example of the Mesa framework for
agent-based modelling in Python. This model is based on 3 parameters that each
agent follows:
    1. Attraction to other agents (cohere),
    2. Avoidance of other agents (separation),
    3. Alignment with other agents (match_velocity).

These rules are based on the neighbours each agent perceives within their
'vision' radius. This is a geometrical distance, rather than topological
(Mann et al. 2011). Another version of this model is being constructed
for the topological (set number of neighbours at any distance).

The 'fish' also interact with objects (also agents) that don't move. These
obstructions can act as borders to the world (i.e. to represent a fish tank) or
elements in an open environment. Later, I plan to add moving obstructions (i.e.
a trawl).

The model is based on an toroidal (unbounded & wrapping), 2D area. Later
versions will be 3D, with environmental gradients, and agents with goal-,
food-, or safety-seeking behaviour.

Data are collected in the data_collectors.py script and are:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest neighbour distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal Area: convex hull
    4. Mean Distance From Centroid

A visualization of the model in an HTML object is in shoal_model_viz.py. For
the visualization, the parameters in the ShoalModel class can be changed to run
based on interactive, user-settable sliders.
"""
# Todo: figure out how to differentiate between fish and obstructions


import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule

from data_collectors import *


class Fish(Agent):
    """
    A Boid-style agent. Boids have a vision that defines the radius in which
    they look for their neighbors to flock with. Their heading (a unit vector)
    and their interactions with their neighbors - cohering and avoiding -
    define their movement. Separation is their desired minimum distance from
    any other Boid.
    """
    def __init__(self, unique_id, model, pos, speed, velocity, vision,
                 separation, tag="fish", cohere=0.025, separate=0.25, match=0.04):
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
            tag: indicator that these are "fish" agents for the data collectors.
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
        self.tag = tag

    def cohere(self, neighbors):
        """
        Return the vector toward the centroid of the local neighbors.
        """
        cohere = np.zeros(2)
        other_fish = [n for n in neighbors if n.tag == "fish"]
        if other_fish:
            for f in other_fish:
                cohere += self.model.space.get_heading(self.pos, f.pos)
            cohere /= len(other_fish)
        return cohere

    def separate(self, neighbors):
        """
        Return a vector (inverse of the heading towards a neighbor) away from any
        neighbors closer than separation distance.
        """
        me = self.pos
        my_neighbors = (n.pos for n in neighbors)
        separate_vector = np.zeros(2)
        for my_neighbor in my_neighbors:
            if self.model.space.get_distance(me, my_neighbor) < self.separation:
                separate_vector -= self.model.space.get_heading(me, my_neighbor)
        return separate_vector

    def match_velocity(self, neighbors):
        """
        Have Boids match the velocity of neighbors.
        """
        match_vector = np.zeros(2)
        other_fish = [n for n in neighbors if n.tag == "fish"]
        if other_fish:
            for f in other_fish:
                match_vector += f.velocity
            match_vector /= len(other_fish)
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


class Obstruct(Agent):
    """
    Immobile objects/obstructions. These agents can be used to create borders
    or other static aspects of the model environment for the "Fish" agents to
    interact with.
    """
    def __init__(self, unique_id, model, pos, tag="obstruct"):
        """
        Create a new Boid (bird, fish) agent.
        Args:
            unique_id: Unique agent identifier.
            pos: Starting position
            tag: indicator that these are "obstruction" agents.
        """
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.tag = tag

    def step(self):
        """Make obstruction agents do nothing."""
        pass


# Interactive sliders for model arguments.
# Todo: Change "value" argument for initial or testing conditions
n_slider = UserSettableParameter(param_type='slider', name='Number of Agents',
                                 value=100, min_value=10, max_value=200, step=1)
speed_slider = UserSettableParameter(param_type='slider', name='Speed',
                                     value=2, min_value=0, max_value=10, step=1)
vision_slider = UserSettableParameter(param_type='slider', name='Vision Radius',
                                      value=10, min_value=0, max_value=20, step=1)
sep_slider = UserSettableParameter(param_type='slider', name='Separation Distance',
                                   value=2, min_value=0, max_value=10, step=1)


class ShoalModel(Model):
    """
    Shoal model class. Handles agent creation, placement and scheduling.
    Parameters are interactive, using the user-settable parameters defined
    above.

    Parameters:
        initial_fish: Initial number of "Fish" agents.
        initial_obstruct: Initial number of "Obstruct" agents.
        width, height: Size of the space.
        speed: how fast the boids should move.
        vision: how far around should each Boid look for its neighbors
        separation: what's the minimum distance each Boid will attempt to
                    keep from any other
        cohere, separate, match: factors for the relative importance of
                                 the three drives.
    """
    def __init__(self,
                 initial_fish=50,
                 initial_obstruct=192,  # This is always len(borders)
                 width=50,
                 height=50,
                 speed=2,
                 vision=10,
                 separation=2,
                 cohere=0.025,
                 separate=0.25,
                 match=0.04):

        self.initial_fish = initial_fish
        self.initial_obstruct = initial_obstruct
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, torus=True)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        self.make_fish()
        self.make_obstructions()
        self.running = True

    def make_fish(self):
        """
        Create N "Fish" agents. A random position and starting velocity is
        assigned for each fish.
        Call data collectors for fish collective behaviour
        """
        for i in range(self.initial_fish):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            fish = Fish(i, self, pos, self.speed, velocity, self.vision,
                        self.separation, **self.factors)
            self.space.place_agent(fish, pos)
            self.schedule.add(fish)

    def make_obstructions(self):
        """
        Create N "Obstruct" agents, with set positions & no movement. Borders
        are defined as coordinate points between the maximum and minimum extent
        of the width/height of the obstruction. These ranges are drawn from the
        model space limits, with a slight buffer.

        The points are then generated for every point along the defined borders.
        """
        for i in range(self.initial_obstruct):
            # if the space is square (i.e. y_max and x_max are the same):
            max_lim = self.space.x_max - 1
            min_lim = self.space.x_min + 1
            line = range(min_lim, max_lim)
            borders = [(min_lim, n) for n in line] + [(n, max_lim) for n in line] + \
                      [(max_lim, n) for n in line] + [(n, min_lim) for n in line]

            # border_length = len(borders)  # determines number of agents

            points = [np.asarray((point[0], point[1])) for point in borders]
            for pos in points:
                obstruct = Obstruct(i, self, pos)
                self.space.place_agent(obstruct, pos)
                self.schedule.add(obstruct)

    def step(self):
        self.schedule.step()


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


def agent_draw(agent):
    """
    Defines how the agents (the fish & the obstructions/borders) are drawn in
    the model visualization.
    """
    portrayal = None

    if isinstance(agent, Fish):
        portrayal = {
            "Shape": "arrowhead",
            "Filled": "True",
            "Color": "Blue",
            "heading_x": agent.velocity[0],
            "heading_y": agent.velocity[1],
            "scale": 3
        }

    elif isinstance(agent, Obstruct):
        portrayal = {
            "Shape": "rect",
            "Filled": "True",
            "Color": "Red",
            "w": 0.02,
            "h": 0.02
        }

    return portrayal


# Create canvas, 500x500 pixels
shoal_canvas = SimpleCanvas(agent_draw)
model_params = {
    "speed": speed_slider,
    "vision": vision_slider,
    "separation": sep_slider
}


# Launch server
server = ModularServer(ShoalModel,
                       [shoal_canvas],
                       "Boids Model of Shoaling Behavior",
                       model_params)
server.launch()
