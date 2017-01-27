"""
A visualization of the Mesa tutorial on agent-based models - agent-based
economic model. Visualization uses a server class and a Canvas Grid class,
which uses an HTML canvas to draw a grid. Also includes a chart drawn from the DataCollector.
"""

from MoneyModel import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule


def agent_portrayal(agent):
    """
    Canvas grid loops over every cell and generates a portrayal (dictionary) of
    each agent it finds, then tells the JavaScript side how to draw each
    portrayal. In this case, one way if agents have money and different look if
    agents are broke
    """
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}  # radius of circle

    if agent.wealth > 0:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal

# Create 10x10 grid, drawn in 500x500 pixels
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                    data_collector_name="datacollector")


# Launch server
server = ModularServer(MoneyModel,  # Model class to be visualized
                       [grid, chart],  # List of module objects to include
                       "Money Model",  # Title of the model
                       # Any inputs for the model: 100 agents, height & width 10
                       100, 10, 10)
server.port = 8889
server.launch()
