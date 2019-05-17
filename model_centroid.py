"""
Instance of the shoal model with just the mean distance from the centroid data
collector.

Then the model is implemented in single and batch runs, useful for determining
mean centroid distance for the whole model.
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
from data_collectors import centroid_dist


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

        self.datacollector = DataCollector(model_reporters={"Mean Distance from Centroid": centroid_dist})

    def make_obstructions(self):
        """
        Create N "Obstruct" agents, with set positions & no movement. Borders
        are defined as coordinate points between the maximum and minimum extent
        of the width/height of the obstruction. These ranges are drawn from the
        model space limits, with a slight buffer.

        The points are then generated for every point along the defined borders.
        """
        for i in range(self.initial_obstruct):
            # x_min = self.space.x_min + 1
            # x_max = self.space.x_max - 1
            # y_min = self.space.y_min + 1
            # y_max = self.space.y_max - 1
            # left = [(x_min, n) for n in range(x_min, x_max)]
            # top = [(n, y_max) for n in range(y_min, y_max)]
            # right = [(x_max, n) for n in range(x_min, x_max)]
            # bottom = [(n, y_min) for n in range(y_min, y_max)]
            # borders = left + top + right + bottom

            # if the space is square (i.e. y_max and x_max are the same):
            max_lim = self.space.x_max - 1
            min_lim = self.space.x_min + 1
            line = range(min_lim, max_lim)
            borders = [(min_lim, n) for n in line] + [(n, max_lim) for n in line] + \
                      [(max_lim, n) for n in line] + [(n, min_lim) for n in line]

            # border_length = len(borders)  # determines number of agents

            # # start and end points for each border, moving clockwise
            # left = [[x_min, y_min], [x_min, y_max]]
            # top = [[x_min, y_max], [x_max, y_max]]
            # right = [[x_max, y_max], [x_max, y_min]]
            # bottom = [[x_max, y_min], [x_min, y_min]]

            points = [np.asarray((point[0], point[1])) for point in borders]
            for pos in points:
                obstruct = Obstruct(i, self, pos, velocity=0)
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


s = 3  # number of steps to run the model for each time


cent_data = pd.DataFrame()
for run in range(10):
    cent_data = cent_data.append(run_model(s).mean(), ignore_index=True)
# cent_data.to_csv(os.path.join(path, r"cent_runs.csv"))
