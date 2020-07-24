# -*- encoding: utf-8 -*-

from abc import ABCMeta
from ..commons.DecayFunctions import (
		NoDecay,
		LinearDecay,
		ExponentialDecay,
		MultiplicativeDecay
	)

from ..commons.DistanceFunctions import (
		EuclideanDistance,
		ManhattanDistance,
		CircularEuclideanDistance
	)

from ..commons.NeighbourhoodFunctions import (
		BubbleDistribution,
		GaussianDistributon
	)

def selectDecayMethod(var : str) -> ABCMeta:
	'''This Returns the MetaClass Containing the Decay-Function
	:param var : (str) Decay Function Name

	Returns: Any of the Decay Functionalities.
	'''
	if (var == 'noDecay') or (var == None):
		return NoDecay
	elif 'linear' in var.lower():
		return LinearDecay
	elif 'exponential' in var.lower():
		return ExponentialDecay
	elif 'multiplicative' in var.lower():
		return MultiplicativeDecay
	else:
		raise ValueError(f'{var} is an Invalid Argument')

def selectDistanceMetric(var : str) -> EuclideanDistance or ManhattanDistance:
	'''This Returns the Distance Function
	:param var : (str) Distance Metric Name

	Returns: Any of the Distance-Metric Functionalities.
	'''
	if 'euclidean' in var.lower():
		return EuclideanDistance
	elif 'manhattan' in var.lower():
		return ManhattanDistance
	else:
		raise ValueError(f'{var} is Invalid Argument.')

def selectNeighbourhoodFunctions(var : str) -> GaussianDistributon or BubbleDistribution:
	'''This Returns the Neighbourhood Function
	:param var : (str) Neighbourhood Function Name

	Returns: Any of the Neighbourhood Functionalities.
	'''
	if 'gauss' in var.lower():
		return GaussianDistributon
	elif 'bubble' in var.lower():
		return BubbleDistribution
	else:
		raise ValueError(f'{var} is Invalid Argument.')