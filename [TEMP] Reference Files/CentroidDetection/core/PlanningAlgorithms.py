# -*- encoding: utf-8 -*-

'''Lists all the Available Algorithms/Methodologies for Automatic Self-Planning for LTE'''

import random
import warnings
import functools

from copy import deepcopy

from ..support import (
		ClosestNeuron,
		GroupNeuronLocation,
		selectNeighbourhoodFunctions
	)

from ..commons.DecayFunctions import (
		NoDecay,
		LinearDecay,
		ExponentialDecay,
		MultiplicativeDecay
	)

from ..commons.DistanceFunctions import CircularEuclideanDistance

def KSOFM(
		NeuronObjs    : list or np.ndarray,
		ParticleObjs  : list or np.ndarray,
		LearningRate  : NoDecay or LinearDecay or ExponentialDecay or MultiplicativeDecay,
		numNeuron     : int = None,
		neighbourhood : str = 'gaussian',
		**kwargs
	) -> list:
	'''Kohonen Self-Organizing Feature Map (KSOFM)
	:param ParticleObjs  : Location of all Particle in the Format [[xPos, yPos], ..., [xPos, yPos]]
	:param NeuronObjs	 : List of n-Neurons Created using CentroidDetection.BaseStation.Neuron Class
	:param LearningRate  : Learning Rate of SOM, with Decay Functionality
	:param numNeuron	 : Number of Neurons [can also be Obtained internally using len(NeuronObjs)]
	:param neighbourhood : Neighbourhood Functionality i.e. gaussian or bubble. Default gaussian

	Returns: List of Updated Neurons of type: [CentroidDetection.BaseStation.Neuron, ..., CentroidDetection.BaseStation.Neuron]
	'''
	if numNeuron == None:
		numNeuron = len(NeuronObjs) # this is am Optional Argument, as Passing the No. of Neuron is Advised

	if kwargs.get('copy', True):
		warnings.warn('#TODO: LearningRate is Not-Copied by Default')
		NeuronObjs = deepcopy(NeuronObjs)

	randomUE						= random.choice(ParticleObjs)
	distanceVector				    = functools.partial(CircularEuclideanDistance, numNeuron)
	closestNeuronIDX, closestNeuron = ClosestNeuron(randomUE, GroupNeuronLocation(NeuronObjs))
	
	for IDX, NEURON in enumerate(NeuronObjs): # Update the Weights of the Neuron and its Neighbourhood
		newDistance = distanceVector(IDX, closestNeuronIDX)

		neighbourhoodFunction = selectNeighbourhoodFunctions(neighbourhood)(newDistance, NEURON.curSearchRadius)
		
		# Updating the Current Location of the Neuron
		curLocation     = NEURON.currentLocation
		curLocation[0] += LearningRate.value * neighbourhoodFunction * (randomUE[0] - curLocation[0])
		curLocation[1] += LearningRate.value * neighbourhoodFunction * (randomUE[1] - curLocation[1])
		
		NEURON.updateLocation(newLocation = curLocation)
		
		# Decay the Learning Rate & Neuron Search Space Radius
		for n in NeuronObjs:
			n.decayRadius # Decay the Radius of all Neurons
		LearningRate.decay() # Decay α after a Complete Updatation
	
	return NeuronObjs