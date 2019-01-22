"""
This script is for running Approximate Bayesian Computation (ABC), comparing
output from the shoal model to the data collected from video of the
sticklebacks. ABC allows you to use existing data to estimate parameters and
compare model structure.

ABC requires:
    * Priors for the parameters - what a model knows beyond the data, i.e.
      expert knowledge. The priors are represented by a distribution, like
      Negative Binomial or Beta.
    * Data the model should fit
    * Criteria for when simulated data match the actual data
    * Many runs of the model for comparison

For the shoal model, the priors will be determined with a sensitivity analysis,
through which the extremes of he various parameters (vision, speed, rule
balance, etc.) are tested.

There are many ways to perform ABC in Python. For now, I'm thinking of going
with ABrox: https://github.com/mertensu/ABrox
"""

