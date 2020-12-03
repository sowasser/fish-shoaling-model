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

The 'fish' can also interact with objects (also agents) that don't move. These
obstructions can act as borders to the world (i.e. to represent a fish tank) or
elements in an open environment. Later, I plan to add moving obstructions (i.e.
a trawl).

The model is based on an toroidal (unbounded & wrapping), 2D area. Later
versions will be 3D, with environmental gradients, and agents with goal-,
food-, or safety-seeking behaviour.

The only data collected from the data_collectors.py script is position, for
creating a heatmap as a representation of shoal density for better comparisons
with acoustic data.

A visualization of the model in an HTML object is in shoal_model_viz.py. For
the visualization, the parameters in the ShoalModel class can be changed to run
based on interactive, user-settable sliders.
"""
# Todo: figure out how to turn off the torus feature for actual bounded space.


import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
from mesa.visualization.UserParam import UserSettableParameter

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

    def avoid_boundaries(self):
        """
        Returns the new (x,y) position of the agent making sure it bounces off
        the walls instead of looping around the space in a torus. This function
        assumes that the self.velocity vector has been calculated in the step()
        function. If the new x and y co-ordinates go out of bounds we flip the
        corresponding value in the velocity vector (to bounce off the wall) and
        recalculate the new_position variable.
        """
        new_position = self.pos + self.velocity * self.speed
        new_x, new_y = new_position

        # If the new position is out of bounds (min & max) on the X-axis (sides)
        # if (new_x < self.model.space.x_min) or (new_x >= self.model.space.x_max):
        #     self.velocity[0] = -self.velocity[0]  # Bounce off the wall on X axis
        #     new_position = self.pos + self.velocity * self.speed

        # If the new position is out of bounds on the Y-axis (top & bottom)
        if (new_y < self.model.space.y_min) or (new_y >= self.model.space.y_max):
            self.velocity[1] = -self.velocity[1]  # Bounce off the wall on Y axis
            new_position = self.pos + self.velocity * self.speed

        return new_position

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

        # Make self.velocity a unit vector
        self.velocity /= np.linalg.norm(self.velocity)

        # Get the new position and make sure it bounces off the walls
        new_position = self.avoid_boundaries()

        self.model.space.move_agent(self, new_position)


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
        n_fish: Initial number of "Fish" agents.
        width, height: Size of the space.
        speed: how fast the boids should move.
        vision: how far around should each Boid look for its neighbors
        separation: what's the minimum distance each Boid will attempt to
                    keep from any other
        cohere, separate, match: factors for the relative importance of
                                 the three drives.
    """
    def __init__(self,
                 n_fish=200,
                 width=50,
                 height=50,
                 speed=1,
                 vision=50,
                 separation=2,
                 cohere=0.25,
                 separate=0.025,
                 match=0.3):
        assert speed < width and speed < height, "speed can't be greater than model area dimensions"
        self.n_fish = n_fish
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, torus=True)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        # self.make_obstructions()  # Todo: un-comment this line to include obstructions
        self.make_fish()
        self.running = True

    def make_fish(self):
        """
        Create N "Fish" agents. A random position and starting velocity is
        assigned for each fish.
        Call data collectors for fish collective behaviour
        """
        for i in range(self.n_fish):
            x = random.randrange(2, (self.space.x_max - 1))
            y = random.randrange(2, (self.space.y_max - 1))
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1  # [-1.0 .. 1.0, -1.0 .. 1.0]
            fish = Fish(i, self, pos, self.speed, velocity, self.vision,
                        self.separation, **self.factors)
            self.space.place_agent(fish, pos)
            self.schedule.add(fish)

        self.datacollector = DataCollector(
            # model_reporters={"test": test})
            model_reporters={"positions": positions})


    def make_obstructions(self):
        """
        Create N "Obstruct" agents, with set positions & no movement. Borders
        are defined as coordinate points between the maximum and minimum extent
        of the width/height of the obstruction. These ranges are drawn from the
        model space limits, with a slight buffer.

        The obstruction agents are then generated for every point along the
        defined borders.
        """
        # if the space is square (i.e. y_max and x_max are the same):
        max_lim = self.space.x_max - 1
        min_lim = self.space.x_min + 1
        line = range(min_lim, max_lim)
        borders = np.asarray([(min_lim, n) for n in line] + [(n, max_lim) for n in line] +
                             [(max_lim, n) for n in line] + [(n, min_lim) for n in line])
        x_points = np.ndarray.tolist(borders[:, 0])
        y_points = np.ndarray.tolist(borders[:, 1])
        points = list(zip(x_points, y_points))

        for i in points:  # create obstruction agent for all points along the borders
            pos = np.array(i)
            obstruct = Obstruct(i, self, pos)
            self.space.place_agent(obstruct, pos)
            self.schedule.add(obstruct)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
