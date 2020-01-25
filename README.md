# fish-shoaling-model
An agent-based modelling using the Mesa framework for Python. This repository includes the following exercises:


1. The Flocking example of collective behaviour from [mesa][mesa]. The code for this example is included as both a Jupyter notebook and Python code. Also includes a JavaScript file that sets up a HTML5 canvas for visualization of a simple, continuous canvas.
2. I've messed with the visualization by updating to the more recent version of Chart.js in order to add chart titles. This is currently not working, but when it does, in order for the script to work without chart titles, just remove the `chart_title="  "` from `ChartModule`.
3.  Preliminary attempts to adapt the boids model for a model of fish shoaling behaviour. So far, this version adds a data collector for spatial statistics with four functions. Others will be added in the future. The outputs are added to pandas dataframes and then exported as .csv files to be used in R. 
4. The Jupyter notebook versions of the data collection file are useful for running the model under various model conditions. 
5. I have also configured the data collector to output agent position (x,y) at every step. This can be used for other visualizations, i.e. [animated plots in matplotlib][matplotlib], or exported to R, etc.
6. Attempts to adapt the Boids model to various other models of collective behaviour from the literature, housed in the `alternative models` folder:
	1. Define vision by a certain number of neighbours, rather than a static distance - [`shoal_model_neighbours.py`][shoalneigh]
	2. Include a blind spot behind the agent - [`shoal_model_blindspot.py`][shoalblind]
	3. Alignment (velocity matching) removed as a behaviour rule & considered an emergent behaviour - [`shoal_model_noalign.py`][shoalnoalign]
	4. 3D!
7. Collection, analysis, graphing, and export of model data, all in the `data_handling` folder. These collect data from, among others,:
	1. a single run in [`single_run.py`][single]
	2. multiple runs of the model under set conditions in [`data_batch.py`][databatch], with graphing of those runs in [`batch_graphs.py`][batchgraphs]
	3. multiple runs of the model with varying conditions in [`data_senstivity.py`][sensitivity]
8. Import of position data from videos of sticklebacks and zebrafish, collected using [LoggerPro][lp]. Once imported and cleaned, these data can be used in various statistics.

<br>

The basic shoal model is broken down into the following scripts:

* [`shoal_model.py`][shoal] contains the agent and model definitions, including the code for collecting the data within the model.
* [`data_collectors.py`][datacollect] contains the functions used to collect data on the polarization and spatial extent of the shoal.
* [`shoal_model_viz.py`][shoalviz] contains the code for the visualization element of the model. Uses a Javascript canvas to create an HTML5 object.
* [`single_run.py`][single] runs the model once without the visualization.



## Installation
These installation instructions assume you are using macOS or Linux with [Python 3.6](python) or newer installed.

1. Clone this repository to your computer:
   
   ```
   git clone https://github.com/sowasser/fish-shoaling-model.git
   ```
   
2. Create a virtual environment so Python dependencies will not conflict with other Python projects you may have on your machine:
   
   ```
	cd fish-shoaling-model
   python3 -m venv env
   ```
   
3. Activate the virtual environment:
   
   ```
   source env/bin/activate 
   ```
   
4. Make sure you have the latest version of pip (Python package installer):
   
   ```
   pip install --upgrade pip 
   ```
   
5. Install the third party dependencies the project require:
	
	```
	pip install -r requirements.txt
	```
	
6. You should now be able to run the Python code in the project:
	
	```
	python3 test_run.py
	```
	
7. If you're using PyCharm, you'll need to add Jupyter to the Project Interpreter in order to run the Jupyter notebooks.


[mesa]: https://github.com/projectmesa/mesa
[mesa Issues]: https://github.com/projectmesa/mesa/issues/358
[#378]: https://github.com/projectmesa/mesa/pull/378
[here]: https://github.com/projectmesa/mesa/blob/600c62b35dbac6de9300da471377b0e200b60da8/mesa/space.py
[matplotlib]: https://matplotlib.org/gallery/animation/simple_3danim.html
[shoalneigh]: https://github.com/sowasser/fish-shoaling-model/blob/master/alternative_models/shoal_model_neighbours.py
[shoalblind]: https://github.com/sowasser/fish-shoaling-model/blob/master/alternative_models/shoal_model_blindspot.py
[shoalnoalign]: https://github.com/sowasser/fish-shoaling-model/blob/master/alternative_models/shoal_model_noalign.py
[single]: https://github.com/sowasser/fish-shoaling-model/blob/master/data_handling/single_run.py
[databatch]: https://github.com/sowasser/fish-shoaling-model/blob/master/data_handling/data_batch.py
[batchgraphs]: https://github.com/sowasser/fish-shoaling-model/blob/master/data_handling/batch_graphs.py
[sensitivity]: https://github.com/sowasser/fish-shoaling-model/blob/master/data_handling/data_sensitivity.py
[lp]: https://www.vernier.com/products/software/lp/
[shoal]: https://github.com/sowasser/fish-shoaling-model/blob/master/shoal_model.py
[datacollect]: https://github.com/sowasser/fish-shoaling-model/blob/master/data_collectors.py
[shoalviz]: https://github.com/sowasser/fish-shoaling-model/blob/master/shoal_model_viz.py
[Homebrew]: https://brew.sh/
[my_mesa]: https://github.com/sowasser/mesa
[pip]: https://pip.pypa.io/en/stable/