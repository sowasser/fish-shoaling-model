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
    def __init__(self, unique_id, model, pos, speed=5, heading=None,
                 vision=5, separation=1):
        """
        Create a new Boid flocker agent. Args:
            unique_id: Unique agent identifyer.
            pos: Starting position
            speed: Distance to move per step.
            heading: numpy vector for the Boid's direction of movement.
            vision: Radius to look around for nearby Boids.
            separation: Minimum distance to maintain from other Boids.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.speed = speed
        if heading is not None:
            self.heading = heading
        else:
            self.heading = np.random.random(2)
            self.heading /= np.linalg.norm(self.heading)
        self.vision = vision
        self.separation = separation

    def cohere(self, neighbors):
        """
        Add the vector toward the center of mass of the local neighbors to the
        position of each agent.
        """
        my_pos = np.array(self.pos)
        coh_vector = np.array([0.0, 0.0])
        for neighbor in neighbors:
            center = np.array(neighbor.pos) / len(neighbors)
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
            opposite = -their_pos
            dist = np.linalg.norm(my_pos - their_pos)
            if dist < self.separation:
                sep_vector += [my_pos[0] - opposite[0],
                               my_pos[1] - opposite[1]]
        return sep_vector

    def match_heading(self, neighbors):
        """ Return a vector of the neighbors' average heading. """
        mean_heading = np.array([0.0, 0.0])
        for neighbor in neighbors:
            mean_heading += np.int64(neighbor.heading)
        return mean_heading / len(neighbors)

    def step(self):
        """ Get the Boid's neighbors, compute the new vector, and move accordingly."""
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        if len(neighbors) > 0:
            cohere_vector = self.cohere(neighbors)
            separate_vector = self.separate(neighbors)
            match_heading_vector = self.match_heading(neighbors)
            self.heading = [(cohere_vector[0] +
                             separate_vector[0] +
                             match_heading_vector[0]),
                            (cohere_vector[1] +
                             separate_vector[1] +
                             match_heading_vector[1])]
            self.heading /= np.linalg.norm(self.heading)
        new_pos = np.array(self.pos) + self.heading * self.speed
        new_x, new_y = new_pos
        self.model.space.move_agent(self, (new_x, new_y))


class BoidsModel(Model):
    """ Flocker model class. Handles agent creation, placement and scheduling. """

    def __init__(self, N, width, height, speed, vision, separation):
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
        self.speed = speed
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
            boid = Boid(i, self, pos, self.speed, heading, self.vision,
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
                       100, 100, 100, 5, 10, 2)
server.launch()
