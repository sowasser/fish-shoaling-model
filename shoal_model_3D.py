"""
Model of shoaling behavior based on the Boids model by Craig Reynolds in 1986,
using the basic code provided in the Flocker example of the Mesa framework for
agent-based modelling in Python. This model is based on 3 parameters that each
agent follows:
    1. Attraction to (coherence with) other agents,
    2. Avoidance of other agents,
    3. Alignment with other agents.
The direction in which the agents swim is determined by the "speed" parameter
and can be either positive (towards the upper, left corner) or negative
(towards the lower, right corner). Therefore, the overall direction of the
group is not random, but their starting position and heading is.

Data is collected on the median absolute deviation of heading and the nearest
neighbor distance, calculated using a k-d tree, as measures of cohesion.

The model is based on a bounded, 3D area. Later additions
will include obstacles, environmental gradients, and agents with goal-, food-,
or safety-seeking behaviour.

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

# Todo: Make the model run in 3 dimensions! Difficult part: need to change ContinuousSpace


def polar(model):  # WORKS
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


def nnd(model):  # WORKS
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
    define their movement. Avoidance is their desired minimum distance from
    any other Boid.
    """
    def __init__(self, unique_id, model, pos, speed=1, velocity=None,
                 vision=5, avoidance=2):
        """
        Create a new Boid (bird, fish) agent. Args:
            unique_id: unique agent identifier.
            pos: starting position
            speed: distance to move per step. Since it's positive, boids move
                in a positive direction.
            velocity: randomly generated. Velocity can then be normalized to
                create the heading - the scalar version w/ no magnitude.
            vision: Radius to look around for nearby Boids.
            avoidance: Minimum distance to maintain from other Boids.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.speed = speed
        if velocity is not None:
            self.velocity = velocity
            self.heading = self.velocity / np.linalg.norm(self.velocity)
        else:
            self.velocity = np.random.uniform(2) - 0.5
            self.heading /= np.linalg.norm(self.velocity)
        self.vision = vision
        self.avoidance = avoidance

    def cohere(self, neighbors):
        """
        Return the vector toward the center of mass of the local neighbors.
        """
        coh_vector = np.array([0.0, 0.0])
        their_pos = [neighbor.pos for neighbor in neighbors]
        their_pos = np.asarray(their_pos)
        center = ndimage.measurements.center_of_mass(their_pos)
        coh_vector += np.subtract(center, self.pos)  # both are tuples
        if np.linalg.norm(coh_vector) > 0:  # when there is already a magnitude
            return coh_vector / np.linalg.norm(coh_vector)
        else:
            return coh_vector

    def avoid(self, neighbors):
        """
        Return a vector away rom any neighbors closer than avoidance distance.
        """
        my_pos = np.array(self.pos)
        avoid_vector = np.array([0, 0])
        for neighbor in neighbors:
            their_pos = np.array(neighbor.pos)
            dist = np.linalg.norm(my_pos - their_pos)
            if dist <= self.avoidance:
                avoid_vector -= np.int64(their_pos - my_pos)  # tuples
        if np.linalg.norm(avoid_vector) > 0:
            return avoid_vector / np.linalg.norm(avoid_vector)
        else:
            return avoid_vector

    def match_velocity(self, neighbors):
        """
        Have Boids match the velocity of neighbors.
        """
        mean_velocity = np.array([0.0, 0.0])
        for neighbor in neighbors:
            mean_velocity += neighbor.velocity / len(neighbors)
        return mean_velocity
        # Not checking for an normalizing this function because we want to
        # retain the magnitude.

    def step(self):
        """ 
        Get the Boid's neighbors, compute the new vector, normalize that
        vector, and move accordingly.
        """
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        if len(neighbors) > 0:
            cohere_vector = self.cohere(neighbors)
            avoid_vector = self.avoid(neighbors)
            velocity = self.match_velocity(neighbors)
            match_heading = velocity / np.linalg.norm(velocity)
            self.heading += (cohere_vector +
                             avoid_vector +
                             match_heading)
        rate = np.linalg.norm(self.heading)
        self.heading /= rate
        new_pos = np.array(self.pos) + self.heading * self.speed
        new_x, new_y = new_pos
        self.model.space.move_agent(self, (new_x, new_y))


class ShoalModel(Model):
    """ Shoal model class. Handles agent creation, placement and scheduling. """

    def __init__(self, n, width, height, speed, vision, avoidance):
        """
        Create a new Flockers model. Args:
            N: Number of Boids
            width, height: Size of the space.
            speed: how fast the boids should move.
            vision: how far around should each Boid look for its neighbors
            avoidance: what's the minimum distance each Boid will attempt to
                keep from any other
        """
        self.n = n
        self.speed = speed
        self.vision = vision
        self.avoidance = avoidance
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, torus=True,
                                     grid_width=100, grid_height=100)
        self.make_agents()
        self.running = True

    def make_agents(self):
        """ 
        Create N agents, with random positions and starting velocities. 
        """
        for i in range(self.n):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = (x, y)
            velocity = np.random.random(2) * 2 - np.array((1, 1))  # Doesn't include upper #, 2d array
            fish = Fish(unique_id=i, model=self, pos=pos, speed=self.speed, velocity=velocity,
                        vision=self.vision, avoidance=self.avoidance)
            self.space.place_agent(fish, pos)
            self.schedule.add(fish)

        self.datacollector = DataCollector(
            model_reporters={"Polarization": polar,
                             "Nearest Neighbour Distance": nnd})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
