import numpy as np
from mesa import Agent
import random
from scipy import ndimage
from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.ModularVisualization import ModularServer

# Todo: Constrain the space so that behaviors are more immediately recognizable.
# Todo: Vision is a positive number - constraining movement to a particular direction


class Boid(Agent):
    """
    A Boid-style flocker agent. Boids have a vision that defines the radius in
    which they look for their neighbors to flock with. Their heading (a unit
    vector) and their interactions with their neighbors - cohering and avoiding -
    define their movement. Avoidance is their desired minimum distance from
    any other Boid.
    """
    def __init__(self, unique_id, model, pos, speed=3, heading=None,
                 vision=5, avoidance=1):
        """
        Create a new Boid (bird, fish) agent. Args:
            unique_id: Unique agent identifier.
            pos: Starting position
            heading: randomly generated then transformed into the unit vector
                     of Boid's movement - no magnitude.
            velocity: Speed of the Boid, calculated as the Euclidean distance
                      (vector norm) of the Boid's heading.
            vision: Radius to look around for nearby Boids.
            avoidance: Minimum distance to maintain from other Boids.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.speed = speed
        if heading is not None:
            self.heading = heading
        else:
            # Does not include the upper number, returns array of 2 values
            self.heading = np.random.uniform(2) - 0.5
            self.heading /= np.linalg.norm(self.heading)
        self.vision = vision
        self.avoidance = avoidance

    def cohere(self, neighbors):
        """
        Add the vector (direction, not speed) toward the center of mass of the
        local neighbors to the position of each agent to return a new vector
        towards neighbors.
        """
        coh_vector = np.array([0.0, 0.0])
        their_pos = [neighbor.pos for neighbor in neighbors]
        their_pos = np.asarray(their_pos)
        center = ndimage.measurements.center_of_mass(their_pos)
        coh_vector += np.subtract(center, self.pos)  # both are tuples
        if np.linalg.norm(coh_vector) > 0:
            return coh_vector / np.linalg.norm(coh_vector)
        else:
            return coh_vector

    def avoid(self, neighbors):
        """
        Return a vector away rom any neighbors closer than separation distance.
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

    def match_heading(self, neighbors):
        """
        Have Boids match the velocity (magnitude/Euclidean distance of heading)
        of neighbors.
        """
        mean_heading = np.array([0.0, 0.0])
        for neighbor in neighbors:
            mean_heading += (neighbor.heading / len(neighbors)) * neighbor.speed
        return mean_heading

    def step(self):
        """ Get the Boid's neighbors, compute the new vector, and move accordingly."""
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        if len(neighbors) > 0:
            cohere_vector = self.cohere(neighbors)
            avoid_vector = self.avoid(neighbors)
            match_heading = self.match_heading(neighbors)
            self.heading += (cohere_vector +
                             avoid_vector +
                             match_heading)
            self.heading /= np.linalg.norm(self.heading)
        new_pos = np.array(self.pos) + self.heading * self.speed
        new_x, new_y = new_pos
        self.model.space.move_agent(self, (new_x, new_y))


class BoidsModel(Model):
    """ Flocker model class. Handles agent creation, placement and scheduling. """

    def __init__(self, N, width, height, speed, vision, avoidance):
        """
        Create a new Flockers model. Args:
            N: Number of Boids
            width, height: Size of the space.
            vision: How far around should each Boid look for its neighbors
            avoidance: What's the minimum distance each Boid will attempt to
                       keep from any other
        """
        self.N = N
        self.speed = speed
        self.vision = vision
        self.avoidance = avoidance
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, torus=True,
                                     grid_width=100, grid_height=100)
        self.make_agents()
        self.running = True

    def make_agents(self):
        """ Create N agents, with random positions and starting headings. """
        for i in range(self.N):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = (x, y)
            heading = np.random.random(2) * 2 - np.array((1, 1))  # Doesn't include upper #, 2d array
            boid = Boid(unique_id=i, model=self, pos=pos, speed=self.speed, heading=heading,
                        vision=self.vision, avoidance=self.avoidance)
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

    def step(self):
        self.schedule.step()


class SimpleCanvas(VisualizationElement):
    local_includes = ["simple_continuous_canvas.js"]
    portrayal_method = None
    canvas_height = 700
    canvas_width = 700

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        """
        Instantiate a new SimpleCanvas
        """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Simple_Continuous_Module({}, {})".
                       format(self.canvas_width, self.canvas_height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
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


def boid_draw(agent):
    return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "Blue"}

boid_canvas = SimpleCanvas(boid_draw, 700, 700)
server = ModularServer(BoidsModel, [boid_canvas], "Boids",
                       N=100, width=100, height=100, speed=3, vision=5, avoidance=2)
server.launch()
