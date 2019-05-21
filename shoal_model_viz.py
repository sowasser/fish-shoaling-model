"""
Code for just the visualization element of the shoal model of fish collective
behaviour using code (in shoal_model.py) based on the Flocker example from the
Mesa agent based modelling framework for Python.

The visualization uses a JavaScript canvas to create an HTML5 object. It
includes an animation of the agents, charts that showing a metrics of overall
cohesion. The current options for charts are:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest Neighbour Distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal Area: convex hull
    4. Mean Distance from Centroid
More information is available in the shoal_model.py and data_collectors.py
scripts.

The visualization also includes sliders for model variables, such as:
    - number of agents
    - agent speed
    - vision/perception radius
    - distance at which agents separate
"""

from shoal_model import *

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule


# Create canvas for visualization
class SimpleCanvas(VisualizationElement):
    """ Uses JavaScript file for a simple, continuous canvas. """
    local_includes = ["simple_continuous_canvas.js"]

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        """ Instantiate a new SimpleCanvas """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Simple_Continuous_Module({}, {})"
                       .format(self.canvas_width, self.canvas_height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        """ Creates the space in which the agents exist. """
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


def agent_draw(agent):
    """
    Defines how the agents (the fish & the obstructions/borders) are drawn in
    the model visualization.
    """
    portrayal = None

    if isinstance(agent, Fish):
        # Todo: change portrayal to include heading & make the viz clearer.
        portrayal = {
            "Shape": "rect",
            "Filled": "True",
            "Color": "Blue",
            "heading_x": agent.velocity[0],
            "heading_y": agent.velocity[1],
            "w": 0.01,
            "h": 0.01
        }

    elif isinstance(agent, Obstruct):
        portrayal = {
            "Shape": "rect",
            "Filled": "True",
            "Color": "Red",
            "w": 0.02,
            "h": 0.02
        }

    return portrayal


# Create canvas, 500x500 pixels
shoal_canvas = SimpleCanvas(agent_draw)
model_params = {
    "speed": speed_slider,
    "vision": vision_slider,
    "separation": sep_slider
}

# Create charts for the data collectors
# Todo: include chart titles & improve charts
polar_chart = ChartModule([{"Label": "Polarization", "Color": "Black"}],
                          data_collector_name="datacollector")
#                         chart_title="Polarization")

neighbor_chart = ChartModule([{"Label": "Nearest Neighbour Distance", "Color": "Black"}],
                             data_collector_name="datacollector")
#                            chart_title="Nearest Neighbour Distance")

area_chart = ChartModule([{"Label": "Shoal Area", "Color": "Black"}],
                         data_collector_name="datacollector")
#                        chart_title="Shoal Area")


# Launch server
server = ModularServer(ShoalModel,
                       [shoal_canvas, polar_chart, neighbor_chart, area_chart],
                       "Boids Model of Shoaling Behavior",
                       model_params)
server.launch()
