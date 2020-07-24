# -*- encoding: utf-8 -*-

'''This Module List(s) out Various Functions for Calculating the Distance b/w Two Points'''

import numpy as np

def EuclideanDistance(startPoint : np.ndarray, targetPoint : np.ndarray) -> float:
	'''Calculates the Eulidean Distance b/w Two Points on an n-Dimensional Plane
	:param startPoint  : Start Point, with [x, y, ... z] Coordinates
	:param targetPoint : Start Point, with [x, y, ... z] Coordinates

	Returns the Distance b/w two Points (unitless Quantity)
	'''
	if (type(startPoint) != np.ndarray) or (type(targetPoint) != np.ndarray):
		startPoint  = np.array(startPoint)
		targetPoint = np.array(targetPoint)

	return np.sqrt(np.sum((startPoint - targetPoint) ** 2))

def ManhattanDistance(startPoint : np.ndarray, targetPoint : np.ndarray) -> float:
	'''Calculates the Manhattan Distance b/w Two Points on an n-Dimensional Plane
	:param startPoint  : Start Point, with [x, y, ... z] Coordinates
	:param targetPoint : Start Point, with [x, y, ... z] Coordinates

	Returns the Distance b/w two Points (unitless Quantity)
	'''
	if (type(startPoint) != np.ndarray) or (type(targetPoint) != np.ndarray):
		startPoint  = np.array(startPoint)
		targetPoint = np.array(targetPoint)

	return sum([abs(i) for i in (startPoint - targetPoint)])

def CircularEuclideanDistance(numElements : int or float, i : int or float, j : int or float) -> float:
	'''Calculates the Circular Euclidean Distance b/w Two-Integers (i, j) in a Circle of n-Elements'''
	manhattanDistance = abs(i - j) # 1-Dimensional Distance
	return min(manhattanDistance, numElements - manhattanDistance)