"""
Instance of the shoal model with just the polarization data collector.

Then the model is implemented a specified number of times for a specified
number of steps, with the data exported for analysis in R or elsewhere.
"""

import random
import numpy as np
import pandas as pd
import os
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace

from shoal_model import Fish, Obstruct
from data_collectors import polar


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

        self.datacollector = DataCollector(model_reporters={"Polarization": polar})

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


path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"
# path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop


def run_model(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel()
    for j in range(steps):
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    return data


polar_data = pd.DataFrame()
for run in range(100):  # number of times to run the model
    polar_data = polar_data.append(run_model(100).mean(), ignore_index=True)  # for x steps
# polar_data.to_csv(os.path.join(path, r"polar_runs.csv"))
