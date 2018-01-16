"""
Model of shoaling behavior based on the Boids model by Craig Reynolds in 1986,
using the basic code provided in the Flocker example of the Mesa framework for
agent-based modelling in Python. This model is based on 3 parameters that each
agent follows:
    1. Attraction to (coherence with) other agents,
    2. Avoidance of other agents,
    3. Alignment with other agents.

Data is collected on the median absolute deviation of velocity and the nearest
neighbor distance, calculated using a k-d tree, as measures of cohesion.

The model is based on a toroidal, 2D area. Unlike the original shoal_model,
this script finds a set # of closest neighbours, instead of those within a
radius (vision).

This script also includes the code for visualizing the model using an HTML5
object. The parameters for the visualization rely on a JavaScript canvas.

Whereas in the original shoaling model bases agent movement off of all
neighbours within a radius (vision), this version of the model selects a set
number of neighbours to inform movements.
"""

import numpy as np
import random
from scipy.spatial import KDTree
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace

from data_collectors import *


# Todo: Change neighbours from defined by radius to simply nearest x number


def neighbours(model):
    """
    Finds 6 nearest neighbours to the target agent, used instead of vision
    to circumvent the polarity issue and follow newer research suggesting
    that a topological, rather than geometric, approach to neighbour selection
    is more accurate (Mann 2011).
    """
    fish = np.asarray([agent.pos for agent in model.schedule.agents])
    fish_tree = KDTree(fish)
    for target in fish:
        nb = fish_tree.query(x=target, k=6)  # includes target agent @ dist = 0
        dist = list(nb[0])  # select dist not neighbor # from .query output
        dist.pop(0)  # removes closest - target agent @ dist = 0
    return nb


class Fish(Agent):
    """
    A Boid-style agent. Their heading (a unit vector) and their interactions
    with their neighbors - cohering and avoiding - define their movement.
    Separation is their desired minimum distance from any other Boid.
    """
    def __init__(self, unique_id, model, pos, speed, velocity, neighborhood,
                 separation, cohere=0.025, separate=0.25, match=0.04):
        """
        Create a new Boid (bird, fish) agent.
        Args:
            unique_id: Unique agent identifier.
            pos: Starting position
            speed: Distance to move per step.
            velocity: numpy vector for the Boid's direction of movement.
            neighborhood: how many neighbours too look for.
            separation: Minimum distance to maintain from other Boids.
            cohere: the relative importance of matching neighbors' positions
            separate: the relative importance of avoiding close neighbors
            match: the relative importance of matching neighbors' headings
        """
        # Todo: figure out how to integrate neighbours instead of vision
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.neighborhood = neighborhood
        self.separation = separation
        self.cohere_factor = cohere
        self.separate_factor = separate
        self.match_factor = match

    def cohere(self, neighbors):
        """
        Return the vector toward the center of mass of the local neighbors.
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
        # Todo: change to draw from neighbours function
        neighbors = self.model.space.get_neighbors(self.pos, False)
        self.velocity += (self.cohere(neighbors) * self.cohere_factor +
                          self.separate(neighbors) * self.separate_factor +
                          self.match_velocity(neighbors) * self.match_factor) / 2
        self.velocity /= np.linalg.norm(self.velocity)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, new_pos)


class ShoalModel(Model):
    """ Shoal model class. Handles agent creation, placement and scheduling. """
    # Todo: removed vision. Do neighbours need to be included here too?

    def __init__(self,
                 population=100,
                 width=100,
                 height=100,
                 speed=1,
                 separation=2,
                 cohere=0.025,
                 separate=0.25,
                 match=0.04):
        """
        Create a new Boids model. Args:
            N: Number of Boids
            width, height: Size of the space.
            speed: how fast the boids should move.
            separation: what's the minimum distance each Boid will attempt to
                        keep from any other
            cohere, separate, match: factors for the relative importance of
                                     the three drives.
        """
        self.population = population
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True,
                                     grid_width=10, grid_height=10)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        self.make_agents()
        self.running = True

    def make_agents(self):
        """
        Create N agents, with random positions and starting velocities.
        """
        # Todo: fix issue with "1 missing required positional argument: 'separation'
        for i in range(self.population):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            fish = Fish(i, self, pos, self.speed, velocity, self.separation, **self.factors)
            self.space.place_agent(fish, pos)
            self.schedule.add(fish)

        self.datacollector = DataCollector(
            model_reporters={"Polarization": polar,
                             "Nearest Neighbour Distance": nnd})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
