"""
Code for just the visualization element of a Boids model of fish collective
behaviour using code (in shoal_model.py) based on the Flocker example from the
Mesa agent based modelling framework for Python.

This version is built using a customized version of Mesa - allows for chart
titles and at this point actually works.

The visualization uses a JavaScript canvas to create an HTML5 object. It
includes an animation of the agents and a chart that shows a metric for overall
cohesion - also described in the model code.

Can change the model parameters to match the parameters used during
experimentation in the Jupyter notebook version.
"""

from shoal_model import *

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter


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


def fish_draw(agent):
    portrayal = {"Shape": "circle",
                 "Color": "Blue",
                 "Filled": "true",
                 "r": 3}
    return portrayal


# Create slider for interactive parameter
# Todo: make other model parameters interactive
n_slider = UserSettableParameter(param_type='slider', name='Number of Agents',
                                 value=100, min_value=2, max_value=200, step=1)
speed_slider = UserSettableParameter(param_type='slider', name='Speed',
                                     value=2, min_value=0, max_value=10, step=1)
vision_slider = UserSettableParameter(param_type='slider', name='Vision Radius',
                                      value=10, min_value=0, max_value=20, step=1)
sep_slider = UserSettableParameter(param_type='slider', name='Separation Distance',
                                   value=2, min_value=0, max_value=10, step=1)

# Create canvas, 500x500 pixels
shoal_canvas = SimpleCanvas(fish_draw, 500, 500)
model_params = {
    "population": n_slider,
    "width": 50,
    "height": 50,
    "speed": speed_slider,
    "vision": vision_slider,
    "separation": sep_slider
}

# Create charts for the data collectors
# Todo: include chart titles & improve charts - this will require updating Mesa
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
                       [shoal_canvas,
                        polar_chart,
                        neighbor_chart,
                        area_chart],
                       "Boids Model of Shoaling Behavior",
                       model_params)
server.launch()
