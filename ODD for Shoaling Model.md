# ODD for Shoaling Model

## Overview

### Purpose
To accurately represent a mackerel shoal to provide information on overall shape and composition under different conditions in order to improve acoustic stock assessments. The goal is to have this model be _actually_ useful for fisheries managers by providing a better estimate of population levels. Acoustic measurements are always an estimate and are especially difficult for Atlantic mackerel (_Scomber scombrus_) as they do not have a swim bladder.

### Entities, State Variables, and Scales
The model consists of agents/individuals representing individual, identical fish within a shoal. They occupy a two-dimensional, toroidal space, the dimensions of which can be specified in the model. Aside from the behavioural rules, the fish are governed by the following variables: 

* Their speed (min: 0, max: 10)
* The radius in which they perceive other agents (min: 0, max: 20)
* The distance at which they separate (min: 0, max: 10).

These variables can be specified when the model is run, or changed using sliders during the model visualization. 

### Process Overview and Scheduling
When initialized, the fish are given three rules to follow. The influence (relative weight) of these functions is determined in the code. Each returns a vector.

* `cohere` returns a vector towards the centroid of the local neighbours
* `separate` returns a vector away from any neighbours closer than the separation distance
* `match_velocity`: Fish match the velocity of their local neighbours.

These functions are called in `step`. The neighbourhood is defined using the vision radius, and each fish's velocity is determined by combining the vectors created in the proceeding functions and their relative weights. The vector is applied, with the speed, and each fish is given a new position for each step of the model.



## Design Concepts

### Emergence
### Adaptation
### Fitness
### Prediction
### Sensing
### Interaction
### Stochasticity
### Collectives
### Observation

## Details

### Initialisation
### Input
### Submodels