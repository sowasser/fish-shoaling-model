# fish-shoaling-model
An agent-based modelling using the Mesa framework for Python. This repository includes the following exercises:


1. The Flocking example of collective behaviour from [mesa][mesa]. The code for this example is included as both a Jupyter notebook and Python code. Also includes a JavaScript file that sets up a HTML5 canvas for visualization of a simple, continuous canvas.
2. I've messed with the visualization by updating to the more recent version of Chart.js in order to add chart titles. This is currently not working, but when it does, in order for the script to work without chart titles, just remove the `chart_title="  "` from `ChartModule`.
3.  Preliminary attempts to adapt the boids model for a model of fish shoaling behaviour. So far, this version adds a data collector for spatial statistics with four functions. Others will be added in the future. The outputs are added to pandas dataframes and then exported as .csv files to be used in R. 
4. The Jupyter notebook versions of the data collection file are useful for running the model under various model conditions. 
5. I have also configured the data collector to output agent position (x,y) at every step. This can be used for other visualizations, i.e. [animated plots in matplotlib][matplotlib], or exported to R, etc.
4. Attempts to adapt the Boids model to various other models of collective behaviour from the literature:
	1. Define vision by a certain number of neighbours, rather than a static distance - `shoal_model_neighbours.py`
	2. Include a blind spot behind the agent - `shoal_model_blindspot.py`
	3. Alignment (velocity matching) removed as a behaviour rule & considered an emergent behaviour - `shoal_model_noalign.py`
	4. Bounded, rather than toroidal, topology - `shoal_model_bounded.py`
	5. 3D!


The basic shoal model is broken down into the following scripts:

* `shoal_model.py` contains the agent and model definitions, including the code for collecting the data within the model.
* `data_collectors.py` contains the functions used to collect data on the polarization and spatial extent of the shoal.
* `shoal_model_viz.py` contains the code for the visualization element of the model. Uses a Javascript canvas to create an HTML5 object.
* `data_sensitivity.py` and `data_batch.py` contain code for exporting the data from single runs of the model and batch runs of the model, respectively.



## Installation
These installation instructions assume you are using macOS (because that's all I know how to use).

1. Clone this repository to your computer: `git clone https://github.com/sowassermann/Python_Practice.git`
2. Make sure you have [Homebrew][Homebrew] installed.
3. Make sure you have Python 3.6; currently I am running this project with Python 3.6.3.
4. I am using [my own version of mesa][my_mesa], since I've been playing around. That can be installed with [pip][pip], using the requirements.txt file, along with all dependencies.
6. If you're using PyCharm, you'll need to add Jupyter to the Project Interpreter in order to run the Jupyter notebooks.


[mesa]: https://github.com/projectmesa/mesa
[mesa Issues]: https://github.com/projectmesa/mesa/issues/358
[#378]: https://github.com/projectmesa/mesa/pull/378
[here]: https://github.com/projectmesa/mesa/blob/600c62b35dbac6de9300da471377b0e200b60da8/mesa/space.py
[matplotlib]: https://matplotlib.org/gallery/animation/simple_3danim.html
[Homebrew]: https://brew.sh/
[my_mesa]: https://github.com/sowasser/mesa
[pip]: https://pip.pypa.io/en/stable/