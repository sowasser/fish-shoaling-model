"""
This file is for creating dataframes containing the results from the data
collectors in the model. These are currently polarization: a function returning
the median absolute deviation of agent heading from the mean heading of the
group, and nearest neighbour distance: the mean distance of the 5 nearest
agents determined using a k-distance tree.

Two dataframes are created in this file:
    1. The model run for X number of steps with set variables
    2. The model run for X times with X number of steps with set variables.
These dataframes can then be exported as .csv files, or graphed using matplotlib.
"""

import numpy as np
import math
import random
from scipy import ndimage
from scipy.spatial import KDTree
from statsmodels.robust.scale import mad
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
import os
from mesa.batchrunner import BatchRunner


def polar(model):
    """
    Computes median absolute deviation (MAD) from the mean heading of the
    group. As the value approaches 0, polarization increases.
    In order to find the MAD, the x,y coordinates are converted to radians by
    finding the arc tangent of y/x. The function used pays attention to the
    sign of the input to make sure that the correct quadrant for the angle is
    determined.
    """
    heading_x = [agent.heading[0] for agent in model.schedule.agents]
    heading_y = [agent.heading[1] for agent in model.schedule.agents]
    angle = []
    for (y, x) in zip(heading_y, heading_x):
        a = math.atan2(y, x)
        angle.append(a)
    return mad(np.asarray(angle), center=np.median)


def nnd(model):
    """
    Computes the average nearest neighbor distance for each agent as another
    measure of cohesion. Method finds & averages the nearest neighbours
    using a KDTree, a machine learning concept for clustering or
    compartmentalizing data. Right now, the 5 nearest neighbors are considered.
    """
    # Todo: figure out how to find neighbors within vision radius
    fish = np.asarray([agent.pos for agent in model.schedule.agents])
    fish_tree = KDTree(fish)
    means = []
    for me in fish:
        neighbors = fish_tree.query(x=me, k=6)  # includes agent @ dist = 0
        dist = list(neighbors[0])
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
        self.space = ContinuousSpace(width, height, True,
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


# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(population=100, width=100, height=100, speed=1, vision=10, separation=2)
for i in range(100):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

path = "/Users/user/Desktop/Dropbox/Mackerel/Mackerel_Data"
data.to_csv(os.path.join(path, r"shoal_data.csv"), index=",")


# Set up and run the BatchRunner, which runs the model multiple times with
# fixed parameters to determine the overall distributions of the model -
# automated by Mesa
parameters = {"n": 100,
              "width": 100,
              "height": 100,
              "speed": 1,
              "vision": 5,
              "avoidance": 2}

batch_run = BatchRunner(ShoalModel,
                        parameters,
                        iterations=1,
                        # 5 instantiations of the model
                        max_steps=100,  # Run each for 100 steps
                        model_reporters={"Polarization": polar,
                                         "NND": nnd})
batch_run.run_all()


# Data collection methods
# Extract data as a DataFrame
batch_data = batch_run.get_model_vars_dataframe()
batch_data.head()
