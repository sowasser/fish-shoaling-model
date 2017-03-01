"""
Code for just the visualization element of a Boids model of fish collective
behaviour using code (in shoal_model_prelim.py) based on the Flocker example
from the Mesa agent based modelling framework for Python.

The visualization uses a JavaScript canvas to create an HTML5 object. It
includes an animation of the agents and a chart that shows a metric for overall
cohesion - also described in the model code.

Can change the inputs for the model (line 75) to match the parameters used
during experimentation in the Jupyter notebook version.
"""

from shoal_model_prelim import *
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule


# Create canvas for visualization
class SimpleCanvas(VisualizationElement):
    """ Uses JavaScript file for a simple, continuous canvas. """
    local_includes = ["simple_continuous_canvas.js"]
    portrayal_method = None
    canvas_height = 500
    canvas_width = 500

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        """ Instantiate a new SimpleCanvas """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Simple_Continuous_Module({}, {})".
                       format(self.canvas_width, self.canvas_height))
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
    """
    Right now, the only option for shape is circle or rectangle (rect).
    Working on creating a triangle or arrow option so the agents' heading
    is explicit in the visualization. Future improvements will hopefully also
    include changes in color with degrees of cohesion and a dot for the
    centroid/center of mass.
    """
    return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "Blue"}


# Create canvas, 500x500 pixels
shoal_canvas = SimpleCanvas(fish_draw, 500, 500)

# Create chart of polarization
polarization_chart = ChartModule([{"Label": "Polarization", "Color": "Black"}],
                                 data_collector_name="datacollector")

# Launch server
server = ModularServer(ShoalModel,  # Model class to be visualized
                       [shoal_canvas, polarization_chart],  # List of module objects to include
                       "Boid Model of Shoaling Behavior",  # Title of the model
                       100, 100, 100, 5, 5, 2)  # Inputs for the model
server.launch()
