# fish-shoaling-model
An agent-based modelling using the Mesa framework for Python. There are five seperate exersises included.


1. The Flocking example of collective behaviour from [mesa][mesa]. The code for this example is included as both a Jupyter notebook and Python code. Also includes a JavaScript file that sets up a HTML5 canvas for visualization of a simple, continuous canvas.
2. Attemt to fix an issue in the original Flocker model. All of the boids always headed to the lower-right corner. Various attempts to rectify this followed, and no solution has been reached. However, small improvements have been made, such as having the boids cohere towards the center of mass of local agents. More about this topic can be found in the [mesa Issues][mesa Issues] on Github. This topic has now been addressed in a pull-request ([#378][#378]) by another user and the changes have been adopted. This does require updating the space.py file from the mesa library itself - an iffy proposition, since the libary has not been updated to include these changes. Also should note that I've messed with the visualization by updating to the more recent version of Chart.js in order to add chart titles. In order for the script to work without chart titles, just remove the `chart_title="  "` from `ChartModule`.
3.  Preliminary attempts to adapt the boids model for a model of fish shoaling behaviour. So far, this version adds a data collector for spatial statistics with two functions: mean nearest neighbour distance as a measure of cohesion, and the median absolute deviation of each agent's heading from the mean heading of the group as a measure of polarization. The outputs of the data collector are added to pandas dataframes and then exported as .csv files in a separate Python file. The Jupyter notebook version of this file is useful for running the model under various model conditions.
4. Attempts to adapt the Boids model to various other models of collective behaviour from the literature. Right now, the first attempt is to define vision by a certain number of neighbors, rather than a static distance. Other attempts will include behavioral zones, removing velocity matching, leadership, memory, inclusion of environmental factors, etc. One big future project will be to adapt the model to 3D.


## Installation
These installation instructions assume you are using macOS (because that's all I know how to use).

1. Clone this repository to your computer: `git clone https://github.com/sowassermann/Python_Practice.git`
2. Make sure you have [Homebrew][Homebrew] installed.
3. Make sure you have Python 3.6; personally, I use [pyenv][pyenv] to manage multiple Python versions and install the newest Python version within pyenv.
4. Since I'm using pyenv, I use the [pyenv-virtualenv][virtualenv] plug-in to create a virtual environment, which requires changing the bash-profile (need to see invisible files) to the lines provied in the virtualenv instructions.
5. Within your virtual environment, you can then use [pip][pip] to install the requirements.txt file to install mesa and its dependencies.
6. If you're using PyCharm, you'll need to add Jupyter to the Project Interpreter in order to run the Jupyter notebooks.

In order to use the updated version of the Flocker example, you will need to update your space.py file within the mesa library. In order to do this safely, I made a duplicate the mesa folder to save as a backup before changing the file to match the changes made in the pull request, found [here][here]. The mesa files are located on my computer at: `/Users/user/.pyenv/versions/python-project-virtualenv-3.6.0/lib/python3.6/site-packages/mesa`


[mesa]: https://github.com/projectmesa/mesa
[mesa Issues]: https://github.com/projectmesa/mesa/issues/358
[#378]: https://github.com/projectmesa/mesa/pull/378
[here]: https://github.com/projectmesa/mesa/blob/600c62b35dbac6de9300da471377b0e200b60da8/mesa/space.py
[Homebrew]: https://brew.sh/
[pyenv]: https://github.com/pyenv/pyenv
[virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[pip]: https://pip.pypa.io/en/stable/