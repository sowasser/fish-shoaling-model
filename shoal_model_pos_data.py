"""
Model of shoaling behavior based on the Boids model by Craig Reynolds in 1986,
using the basic code provided in the Flocker example of the Mesa framework for
agent-based modelling in Python. This model is based on 3 parameters that each
agent follows:
    1. Attraction to (coherence with) other agents,
    2. Avoidance of other agents,
    3. Alignment with other agents.

The model is based on a toroidal, 2D area.

This file is for creating a dataframe containing the position of each agent at
each step, using the data collector. The dataframe can then be exported as a
.csv file, or graphed using matplotlib.
"""

import numpy as np
import pandas as pd
import itertools
import random
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
import os

from shoal_model import Fish
# import matplotlib.pyplot as plt
# from matplotlib import animation


def positions(model):
    """
    Extracts xy coordinates for each agent to be used in the data collector,
    creates lists of tuples (for each agent) per step, which is then flattened
    into a simple list and made into a pandas series.
    """
    pos = [(agent.pos[0], agent.pos[1]) for agent in model.schedule.agents]
    pos = list(itertools.chain(*pos))
    return pos


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
            model_reporters={"Position (x, y)": positions})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(population=7, width=30, height=30, speed=1, vision=10, separation=2)
for i in range(100):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

# Get DataFrame into a form that can be exported as .csv - remove nesting
data = np.asarray(data)
data = data.flatten()  # one set of brackets removed....
df = pd.DataFrame(data)
output = df[0].apply(pd.Series)  # removed another set of brackets
output[0].apply(pd.Series)  # removed last brackets
np_output = np.asarray(output)

# Column headers: x1, y1, x2, y2, etc.
nums = range(1, 8)  # list same length as # of agents (end value is num + 1)
list_x = ["x" + str(i) for i in nums]  # creates x1, x2, etc.
list_y = ["y" + str(j) for j in nums]  # same for y

# iterate between lists and assign as column names
output.columns = [item for sublist in zip(list_x, list_y) for item in sublist]

# Export data as .csv
path = "/Users/user/Desktop/Local/Mackerel/Mackerel_Data"
output.to_csv(os.path.join(path, r"position_data.csv"))


# # Visualization in matplotlib
# plt.style.use('dark_background')
#
# # Set up figure, axes, and plot element
# fig = plt.figure()
# ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
# scatter,  = ax.plot([], [], markersize=2)
#
#
# # Initialization function - background of frames
# def init():
#     scatter.set_data([], [])
#     return scatter,
#
#
# # Animation function - called sequentially
# def animate(i):
#     x = output[i, ::2]
#     y = output[i, 1::2]
#     scatter.set_data(x, y)
#     return scatter,
#
#
# # Call the animator
# anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=100, interval=20)
# plt.show()
#
# # Save the animation - need FFmpeg to save as mp4
# # anim.save('basic_animation.mp4', fps=30)

