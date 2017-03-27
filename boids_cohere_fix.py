import numpy as np
from mesa import Agent
import random
from mesa import Model
import math
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.ModularVisualization import ModularServer

# Todo: Constrain the space so that behaviors are more immediately recognizable.
# Todo: Radius is a positive number - constraining movement to the bottom-right


class Boid(Agent):
    """
    A Boid-style flocker agent. Boids have a vision that defines the radius in
    which they look for their neighbors to flock with. Their heading (a unit
    vector) and their interactions with their neighbors - cohering and avoiding -
    define their movement. Avoidance is their desired minimum distance from
    any other Boid.
    """
    def __init__(self, unique_id, model, pos, heading,
                 vision=10, avoidance=2):
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
        if heading is not None:
            # Heading is defined within the model. Here, a unit vector is
            # created by dividing it by its magnitude so velocity can be
            #  defined as the magnitude of the heading.
            self.heading = heading
            self.velocity = np.linalg.norm(heading)
            self.heading /= self.velocity
        else:
            # Does not include the upper number, returns array of 2 values
            self.heading = np.random.uniform(-1, 1, 2)
            self.heading /= np.linalg.norm(self.heading)
        vision *= 2 * math.pi
        self.vision = vision
        self.avoidance = avoidance

    def cohere(self, neighbors):
        """
        Add the vector (direction, not speed) toward the center of mass of the
        local neighbors to the position of each agent to return a new vector
        towards neighbors.
        """
        my_pos = np.array(self.pos)
        coh_vector = np.array([0.0, 0.0])
        for neighbor in neighbors:
            center = np.array(neighbor.pos) / len(neighbors)
            # Vector calculation uses the Head-Minus-Tail rule
            coh_vector += (my_pos - center)
        return coh_vector

    def avoid(self, neighbors):
        my_pos = np.array(self.pos)
        avoid_vector = np.array([0.0, 0.0])
        for neighbor in neighbors:
            if abs(np.linalg.norm(my_pos - neighbor.pos)) > self.avoidance:
                avoid_vector -= (my_pos - neighbor.pos)
            return avoid_vector

    def match_velocity(self, neighbors):
        """
        Have Boids match the velocity (magnitude/Euclidean distance of heading)
        of neighbors.
        """
        my_velocity = self.velocity
        mean_velocity = 0
        for neighbor in neighbors:
            mean_velocity += np.int64(neighbor.velocity)
            mean_velocity /= len(neighbors)
            if my_velocity < mean_velocity:
                my_velocity += mean_velocity - my_velocity
            elif my_velocity > mean_velocity:
                my_velocity -= mean_velocity - my_velocity
        return mean_velocity

    def step(self):
        """ Get the Boid's neighbors, compute the new vector, and move accordingly."""
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        if len(neighbors) > 0:
            cohere_vector = self.cohere(neighbors)
            avoid_vector = self.avoid(neighbors)
            self.heading += (cohere_vector +
                             avoid_vector)
            self.heading /= np.linalg.norm(self.heading)
        new_pos = np.array(self.pos) + self.heading * self.velocity
        new_x, new_y = new_pos
        self.model.space.move_agent(self, (new_x, new_y))


class BoidsModel(Model):
    """ Flocker model class. Handles agent creation, placement and scheduling. """

    def __init__(self, N, width, height, vision, avoidance):
        """
        Create a new Flockers model. Args:
            N: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            avoidance: What's the minimum distance each Boid will attempt to
                       keep from any other
        """
        self.N = N
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
            # Does not include the upper number, returns array of 2 values
            heading = np.random.uniform(-1, 1, 2)
            # heading /= np.linalg.norm(heading)
            boid = Boid(unique_id=i, model=self, pos=pos, heading=heading, vision=self.vision,
                        avoidance=self.avoidance)
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
                       N=100, width=100, height=100, vision=10, avoidance=2)
server.launch()
