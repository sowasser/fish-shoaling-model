# Python_Practice
Practice on agent-based modelling using the Mesa framework for Python. There are five seperate exersises included.

1. MoneyModelMoney: the completed introductory tutorial from [mesa](mesa), a model of a simple agent-based economy. There is a Jupyter notebook with the entire tutorial and a Python file with all of the code documented for future reference.

2. The Flocking example of collective behaviour from [mesa](mesa). The code for this example is included as both a Jupyter notebook and Python code. Also includes a JavaScript file that sets up a HTML5 canvas for visualization of a simple, continuous canvas.
3. Attemt to fix an issue in the original Flocker model. All of the boids always headed to the lower-right corner. Various attempts to rectify this followed, and no solution has been reached. However, small improvements have been made, such as having the boids cohere towards the center of mass of local agents. More about this topic can be found in the [mesa Issues](mesa Issues) on Github.
4.  Preliminary attempts to adapt the boids model for a model of fish shoaling behaviour. So far, this version adds a data collector for spatial statistics. The Jupyter version of this file is useful for running the model under various conditions (number of agents, vision radius, swimming speed, etc.).


## Installation
These installation instructions assume you are using macOS (because that's all I know how to use).

1. Clone this repository to your computer: `git clone https://github.com/sowassermann/Python_Practice.git`
2. Make sure you have [Homebrew](Homebrew) installed.
3. Make sure you have Python 3.6; personally, I use [pyenv](pyenv) to manage multiple Python versions and install the newest Python version within pyenv.
4. Since I'm using pyenv, I use the [pyenv-virtualenv](virtualenv) plug-in to create a virtual environment, which requires changing the bash-profile (need to see invisible files) to the lines provied in the virtualenv instructions.
5. Within your virtual environment, you can then use [pip](pip) to install the requirements.txt file to install mesa and its dependencies.


[mesa]: https://github.com/projectmesa/mesa
[mesa Issues]: https://github.com/projectmesa/mesa/issues/358
[Homebrew]: https://brew.sh/
[pyenv]: https://github.com/pyenv/pyenv
[virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[pip]: https://pip.pypa.io/en/stable/