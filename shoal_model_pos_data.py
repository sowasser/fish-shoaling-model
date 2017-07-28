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

The model is based on a bounded, 3D area. Later additions will include
obstacles, environmental gradients, and agents with goal-, food-, or
safety-seeking behaviour.

This script also includes the code for visualizing the model using an HTML5
object. The parameters for the visualization rely on a JavaScript canvas.

This file is for creating a dataframe containing the position of each agent at
each step, using the data collector. The dataframe can then be exported as a
.csv file, or graphed using matplotlib.
"""

import numpy as np
import pandas as pd
import itertools
import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
# import os
import matplotlib.pyplot as plt
from matplotlib import animation


def positions(model):
    """
    Extracts xy coordinates for each agent to be used in the data collector,
    creates lists of tuples (for each agent) per step, which is then flattened
    into a simple list and made into a pandas series.
    """
    pos = [(agent.pos[0], agent.pos[1]) for agent in model.schedule.agents]
    pos = list(itertools.chain(*pos))
    return pos


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
            model_reporters={"Position (x, y)": positions})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(population=100, width=100, height=100, speed=1, vision=10, separation=2)
for i in range(100):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

# Get DataFrame into a form that can be exported as .csv
data = np.asarray(data)
data = data.flatten()  # one set of brackets removed....
df = pd.DataFrame(data)
output = df[0].apply(pd.Series)  # removed another set of brackets
output[0].apply(pd.Series)  # removed last brackets
np_output = np.asarray(output)

# Use the following code for column names - harder as population increases
# colnames = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'x5', 'y5',
#             'x6', 'y6', 'x7', 'y7', 'x8', 'y8', 'x9', 'y9', 'x10', 'y10']
# output.columns = colnames

# Export data as .csv
# path = "/Users/user/Desktop/Dropbox/Mackerel/Mackerel_Data"
# output.to_csv(os.path.join(path, r"position_data.csv"))


# Visualization in matplotlib
plt.style.use('dark_background')

# Set up figure, axes, and plot element
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
scatter,  = ax.plot([], [], markersize=2)


# Initialization function - background of frames
def init():
    scatter.set_data([], [])
    return scatter,


# Animation function - called sequentially
def animate(i):
    x = output[i, ::2]
    y = output[i, 1::2]
    scatter.set_data(x, y)
    return scatter,

# Call the animator
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=20)
plt.show()

# Save the animation - need FFmpeg to save as mp4
# anim.save('basic_animation.mp4', fps=30)

