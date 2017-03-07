# Python_Practice
Practice on agent-based modelling using the Mesa framework for Python. There are three seperate exersizes included.

1. MoneyModelMoney: the completed introductory tutorial from Mesa, a model of a simple agent-based economy. There is a Jupyter notebook with the entire tutorial and a Python file with all of the code documented for future reference.

2. The Flocking example of collective behaviour from Mesa. The code for this example is included as both a Jupyter notebook and Python code. Also includes a JavaScript file that sets up a HTML5 canvas for visualization of a simple, continuous canvas.

3. Preliminary attempts to adapt the boids model for a model of fish shoaling behaviour. There is the start of an adaptation of the Flocker example that is based on a model of satisfaction outlined by Quera et al. 2015, and a preliminary shoaling model that adds data collection and attempts to create a 3-dimensional space.


## Installation
These installation instructions assume you are using macOS (because that's all I know how to use).

1. Clone this repository to your computer: `git clone https://github.com/sowassermann/Python_Practice.git`
2. Make sure you have [Homebrew](Homebrew) installed.
3. Make sure you have Python 3.6; personally I use [pyenv](pyenv) to manage multiple Python versions and install the newest Python version within pyenv.
4. Since I'm using pyenv, I use the [pyenv-virtualenv](virtualenv) plug-in to create a virtual environment, which requires changing the bash-profile (need to see invisible files) to the lines provied in the virtualenv instructions.
5. Within your virtual environment, you can then use [pip](pip) to install the requirements.txt file to install mesa and its dependencies.


[Homebrew]: https://brew.sh/
[pyenv]: https://github.com/pyenv/pyenv
[virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[pip]: https://pip.pypa.io/en/stable/