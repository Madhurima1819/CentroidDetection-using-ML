# -*- encoding: utf-8 -*-

# init-Time Option Registration for _support Module
from ._preProcess import _particle
from ._addedFuncs import (
		GroupNeuronLocation, # this Function Returns a List of Tuples, containing ONLY the Current Neuron Location
		ClosestNeuron, # Finds the Closes Neuron b/w all the Neurons and the Moving Particles at any Point of Time
		_consecutiveDifference_ # Finds the Difference b/w all the Consecutive Numbers in an Array
	)

from ._selectFuncs import (
		selectDecayMethod,
		selectDistanceMetric,
		selectNeighbourhoodFunctions
	)