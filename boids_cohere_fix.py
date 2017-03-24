import numpy as np
from mesa import Agent
import random
from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.ModularVisualization import ModularServer


class Boid(Agent):
    """
    A Boid-style flocker agent. Boids have a vision that defines the radius in
    which they look for their neighbors to flock with. Their speed (a scalar) and
    heading (a unit vector) define their movement. Separation is their desired
    minimum distance from any other Boid.
    """
    def __init__(self, unique_id, model, pos, h=None, heading=None, velocity=None,
                 vision=5, separation=2):
        """
        Create a new Boid (bird, fish) agent. Args:
            unique_id: Unique agent identifier.
            pos: Starting position
            h: numpy vector for the Boid's direction of movement.
            heading: unit vector of Boid's movement - no magnitude.
            velocity: Speed of the Boid, calculated as the Euclidean distance
                      of the Boid's heading.
            vision: Radius to look around for nearby Boids.
            separation: Minimum distance to maintain from other Boids.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        if heading is not None:
            self.h = h
            self.heading = heading
            self.velocity = velocity
        else:
            self.h = np.random.random(2)
            self.heading = self.h / np.linalg.norm(self.h)
            self.velocity = np.linalg.norm(self.h)
        self.vision = vision
        self.separation = separation

    def cohere(self, neighbors):
        """
        Add the vector (direction, not speed) toward the center of mass of the
        local neighbors to the position of each agent to return a new vector
        towards neighbors.
        """
        my_pos = np.array(self.pos)
        coh_vector = np.array([0.0, 0.0])  # create empty list for new vector
        for neighbor in neighbors:
            # Calculate center of neighbors
            center = np.array(neighbor.pos) / len(neighbors)
            # Find the new vector towards the center using Head-Minus-Tail rule
            coh_vector += [my_pos[0] - center[0],
                           my_pos[1] - center[1]]
        return coh_vector

    def separate(self, neighbors):
        """
        Subtract the position of neighboring agents from the position of each
        agent.
        """
        my_pos = np.array(self.heading)
        sep_vector = np.array([0.0, 0.0])
        for neighbor in neighbors:
            their_pos = np.array(neighbor.pos)
            away = -their_pos
            dist = np.linalg.norm(my_pos - their_pos)
            if dist < self.separation:
                sep_vector += [my_pos[0] - away[0],
                               my_pos[1] - away[1]]
        return sep_vector

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
            separate_vector = self.separate(neighbors)
            self.heading = [(cohere_vector[0] + separate_vector[0]),
                            (cohere_vector[1] + separate_vector[1])]
            self.heading /= np.linalg.norm(self.heading)
        new_pos = np.array(self.pos) + self.heading * self.velocity
        new_x, new_y = new_pos
        self.model.space.move_agent(self, (new_x, new_y))


class BoidsModel(Model):
    """ Flocker model class. Handles agent creation, placement and scheduling. """

    def __init__(self, N, width, height, vision, separation):
        """
        Create a new Flockers model. Args:
            N: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            separation: What's the minimum distance each Boid will attempt to
                       keep from any other
        """
        self.N = N
        self.vision = vision
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True,
                                     grid_width=10, grid_height=10)
        self.make_agents()
        self.running = True

    def make_agents(self):
        """ Create N agents, with random positions and starting headings. """
        for i in range(self.N):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = (x, y)
            heading = np.random.random(2) * 2 - np.array((1, 1))
            heading /= np.linalg.norm(heading)
            boid = Boid(i, self, pos, heading, self.vision,
                        self.separation)
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

    def step(self):
        self.schedule.step()


class SimpleCanvas(VisualizationElement):
    local_includes = ["simple_continuous_canvas.js"]
    portrayal_method = None
    canvas_height = 500
    canvas_width = 500

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

boid_canvas = SimpleCanvas(boid_draw, 500, 500)
server = ModularServer(BoidsModel, [boid_canvas], "Boids",
                       100, 100, 100, 10, 2)
server.launch()
