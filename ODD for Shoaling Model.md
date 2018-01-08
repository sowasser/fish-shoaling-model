# ODD for Shoaling Model

## Overview

### Purpose
To accurately represent a mackerel shoal to provide information on overall shape and composition under different conditions in order to improve acoustic stock assessments. The goal is to have this model be _actually_ useful for fisheries managers by providing a better estimate of population levels. Acoustic measurements are always an estimate and are especially difficult for Atlantic mackerel (_Scomber scombrus_) as they do not have a swim bladder.

<br>

### Entities, State Variables, and Scales
The model consists of agents/individuals representing individual, identical fish within a shoal. They occupy a two-dimensional, toroidal space, the dimensions of which can be specified in the model. Aside from the behavioural rules, the fish are governed by the following variables: 

* Their speed (min: 0, max: 10)
* The radius in which they perceive other agents (min: 0, max: 20)
* The distance at which they separate (min: 0, max: 10).

These variables can be specified when the model is run, or changed using sliders during the model visualization. 

<br>

### Process Overview and Scheduling
When initialized, the fish are given three rules to follow. The influence (relative weight) of these functions is determined in the code. Each returns a vector.

* `cohere` returns a vector towards the centroid of the local neighbours
* `separate` returns a vector away from any neighbours closer than the separation distance
* `match_velocity`: Fish match the velocity of their local neighbours.

These functions are called in `step`. The neighbourhood is defined using the vision radius, and each fish's velocity is determined by combining the vectors created in the proceeding functions and their relative weights. The vector is applied, with the speed, and each fish is given a new position for each step of the model.


<br>

## Design Concepts

### Emergence
Coordinated movement between individuals, collective behaviour, emerges from these simple movement rules, with no direct communication between the agents. In real systems, behaviour is mediated by more factors, including non-visual sensory input, differences between individuals' goals and personality, and environmental conditions. This model, however, does replicate behaviour similar to that seen in systems such as fish shoals and bird flocks.

<br>

### Adaptation

<br>

### Fitness
Fitness-seeking is not currently included in the model. Possible expansions to the model include factoring in the goal directedness of the individuals, if some are seeking food and are more interested in exploration, versus safety-seeking individuals. 

<br>

### Prediction
Individuals do no predict future conditions, nor are their behaviours mediated by past conditions; they have no memory.

<br>

### Sensing
Individuals are aware of their neighbours within a vision radius, determined in the model. 

In later versions of the model, environmental variables, e.g. representing temperature gradients, can be added and will be sensed within the same radius as the individual. Therefore, these factors will be 'sensed' differently by the entire shoal, than by the individual, contributing to the greater intelligence of the collective group.

<br>

### Interaction
At the moment, individuals do not interact directly with each other, i.e., their behaviour is mediated by others' positions, but they do not influence those positions directly.

<br>

### Stochasticity
The activation of each individual is randomised. The function `RandomActivation` activates each agent once per step, in a random order. Therefore, no individual is repeatedly activated before other agents, affecting the order of operations within the model. 

The starting position and initial velocity of each individual are also random. As there is no pre-determined shape of the group included in the model, random positions and velocities allow the shoal to emerge from random positions and directions, rather than being determined by the starting point.

<br>

### Collectives
The goal of the model is the formation of a collective.

<br>

### Observation
Through the built-in visualization, the user can observe the positioning of the agents as the model progresses and see the emergence of collective behaviour. From this interface, the user can control the frames per second, the number of individuals, their speed, their vision radius, and the distance at which they separate with sliders. The visualization also includes three real-time graphs showing the mediate absolute deviation of individual heading as a measure of polarisation, the mean nearest neighbour distance, and the total area of the shoal (area of the convex hull). The visualization therefore provides both visual and empirical measures of cohesion.

The sliders for model parameters also allow the user to test the model response and sensitivity to various inputs and the effect on the model outputs.

<br>

## Details

### Initialisation
Individuals are initialized at a random position and are given a random velocity. They then move to a new position at the speed determined in the model parameters and begin to implement the rules provided. The initial position and velocity and the speed of the individuals moving forward does not currently come from any data, but can be later adapted to fit data collected in the lab.

<br>

### Input
There are currently no data inputs into the model. This will change as lab data are collected.

<br>

### Submodels
Currently, the following submodels are being developed:

* __Bounded space__ - in this model, the space is bounded, not toroidal. This is to better represent the lab conditions, where individuals cannot wrap around to the other edge of the space.
* __No alignment__ - in this model, alignment is itself considered an emergent behaviour and is therefore not included as one of the rules the individuals have to follow, leaving only coherence and separation. Alignment as an emergent behaviour is supported in the literature ([Quera _et al._, 2016][quera]; [Mann _et al._, 2011][mann]).
* __Fixed number of neighbours__ - instead of the individuals reacting to neighbours within a vision radius, they react to a set number of neighbours. This submodel is inspired by different ways of determining the local neighbourhood in the literature.
* __Three-dimensions__ - model in three-dimensional space. All other variables are the same.


[quera]: https://www.sciencedirect.com/science/article/pii/S0025556415002394
[mann]: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0022827
