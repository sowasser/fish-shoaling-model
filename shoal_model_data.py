"""
Model of shoaling behavior based on the Boids model by Craig Reynolds in 1986,
using the basic code provided in the Flocker example of the Mesa framework for
agent-based modelling in Python. This model is based on 3 parameters that each
agent follows:
    1. Attraction to (coherence with) other agents,
    2. Avoidance of other agents,
    3. Alignment with other agents.

The model is based on a toroidal, 2D area.

This file is for creating dataframes containing the results from the data
collectors in the model. These are:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest neighbour distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal area: convex hull
    4. Mean distance from centroid

These parameters all produce a single value per step in the model. The
dataframes created in this file are:
    1. The model run for X number of steps with set variables
    2. The model run for X times with X number of steps with set variables.
These dataframes can then be exported as .csv files to be further examined in R
or graphed with matplotlib.
"""


import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
import os
from mesa.batchrunner import BatchRunner

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
                             "Nearest Neighbour Distance": nnd,
                             "Shoal Area": area,
                             "Mean Distance from Centroid": centroid_dist})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


# Data collection for debugging purposes
# model = ShoalModel(population=100, width=50, height=50, speed=1, vision=10, separation=2)
# for i in range(100):
#     model.step()
# data1 = model.datacollector.get_model_vars_dataframe()


# Collect the data from a single run with x number of steps into a dataframe
path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
# path_laptop = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"

# 100 agents
model100 = ShoalModel(population=100, width=50, height=50, speed=1, vision=10, separation=2)
for i in range(500):
    model100.step()
data100 = model100.datacollector.get_model_vars_dataframe()
data100.to_csv(os.path.join(path, r"shoal_data_100.csv"), index=",")

# 50 agents
model50 = ShoalModel(population=50, width=50, height=50, speed=1, vision=10, separation=2)
for j in range(500):
    model50.step()
data50 = model50.datacollector.get_model_vars_dataframe()
data50.to_csv(os.path.join(path, r"shoal_data_50.csv"), index=",")

# # 200 agents
model200 = ShoalModel(population=200, width=50, height=50, speed=1, vision=10, separation=2)
for k in range(500):
    model200.step()
data200 = model200.datacollector.get_model_vars_dataframe()
data200.to_csv(os.path.join(path, r"shoal_data_200.csv"), index=",")

# Set up and run the BatchRunner, which runs the model multiple times with
# fixed parameters to determine the overall distributions of the model -
# automated by Mesa
# parameters = {"population": 100,
#               "width": 100,
#               "height": 100,
#               "speed": 1,
#               "vision": 10,
#               "separation": 2}
#
# batch_run = BatchRunner(ShoalModel,
#                         parameters,
#                         iterations=1,
#                         # 5 instantiations of the model
#                         max_steps=100,  # Run each for 100 steps
#                         model_reporters={"Polarization": polar,
#                                          "NND": nnd})
# batch_run.run_all()
#
#
# # Data collection methods
# # Extract data as a DataFrame
# batch_data = batch_run.get_model_vars_dataframe()
# print(batch_data)
