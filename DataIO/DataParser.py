# -*- encoding: utf-8 -*-

import numpy as np
import pandas as pd
from copy import deepcopy
from tqdm import tqdm as TQ

### --- Functions Copied from CentroidDetection.commons.DistanceFunctions --- ###
def _EuclideanDistance_(startPoint : np.ndarray, targetPoint : np.ndarray) -> float:
	'''Calculates the Eulidean Distance b/w Two Points on an n-Dimensional Plane
	:param startPoint  : Start Point, with [x, y, ... z] Coordinates
	:param targetPoint : Start Point, with [x, y, ... z] Coordinates

	Returns the Distance b/w two Points (unitless Quantity)
	'''
	if (type(startPoint) != np.ndarray) or (type(targetPoint) != np.ndarray):
		startPoint  = np.array(startPoint)
		targetPoint = np.array(targetPoint)

	return np.sqrt(np.sum((startPoint - targetPoint) ** 2))

def _ManhattanDistance_(startPoint : np.ndarray, targetPoint : np.ndarray) -> float:
	'''Calculates the Manhattan Distance b/w Two Points on an n-Dimensional Plane
	:param startPoint  : Start Point, with [x, y, ... z] Coordinates
	:param targetPoint : Start Point, with [x, y, ... z] Coordinates

	Returns the Distance b/w two Points (unitless Quantity)
	'''
	if (type(startPoint) != np.ndarray) or (type(targetPoint) != np.ndarray):
		startPoint  = np.array(startPoint)
		targetPoint = np.array(targetPoint)

	return sum([abs(i) for i in (startPoint - targetPoint)])

def _ChooseDistanceMetric_(param : str):
	return {
		'euclidean' : _EuclideanDistance_,
		'manhattan' : _ManhattanDistance_,
	}.get(param) # if any ValueError is Passed, it is taken cared in the Main Function: dist_date_parser()

def _CalculateVelocity_(tStart, tEnd, startPoint, endPoint, dist_metric) -> [float, float]:
	'''Given the Reqd. Values, calculates Distance & Velocity'''
	time     = abs(tStart - tEnd)
	distance = dist_metric(np.array(startPoint), np.array(endPoint))

	return distance, distance / time

### --- Main Functionalities --- ###
def dist_date_parser(data : dict or pd.DataFrame, distance_type : str = 'euclidean', **kwargs) -> pd.DataFrame:
	'''Given a Data as per GenerateData.RandMOD01() Format
	This Function Calculates Distance (Euclidean/Manhattan) and Velocity
	The Data Expects Column Names as per the Required Format - if there is any Name-Change,
	Then use the kwargs to List out the Names.
	
	Parameters
	----------
	distance_type : either euclidean or manhattan, Default euclidean

	Keyword Arguments
	-----------------
	keep_trip_sub_num : (bool) Keep the Column Named TripSubNum. Default False
	keep_data_indexed : (bool) Keep the Data Indexed [ParticleID, TripID]. Default False
	'''
	if type(data) == dict:
		data = deepcopy(pd.DataFrame(data))
	elif type(data) == pd.DataFrame:
		data = deepcopy(data)
	else:
		raise TypeError(f'Expects dtype dict or pd.DataFrame, got {type(data)}')

	# Selection of Ditance-Metric
	if distance_type not in ['euclidean', 'manhattan']:
		raise ValueError(f'Expects euclidean/manhattan, got {distance_type}') # Need to Append for both
	else:
		dist_metric = _ChooseDistanceMetric_(distance_type)

	# Setting the Keyword Arguments for the Column Names
	ParticleID = kwargs.get('ParticleID', 'ParticleID')
	TripID     = kwargs.get('TripID', 'TripID')
	TimeStamp  = kwargs.get('TimeStamp', 'TimeStamp')
	xStart     = kwargs.get('xStart', 'xStart')
	yStart     = kwargs.get('yStart', 'yStart')
	TripSubNum = kwargs.get('TripSubNum', 'TripSubNum')

	# Other Optional Keyword Arguments as Described
	keep_trip_sub_num = kwargs.get('keep_trip_sub_num', False)
	keep_data_indexed = kwargs.get('keep_data_indexed', False)

	# Parsed Values
	velocity = []
	distances = []

	for idx, row in TQ(data.iterrows(), desc = f'Appending Required Values to a DF of Shape {data.shape}'):
		if row[TripSubNum] == 0: # Determines Starting of the Trip
			velocity.append(0)
			distances.append(0)
		else:
			_prev_time   = data.iloc[idx - 1][TimeStamp]
			_prev_xStart = data.iloc[idx - 1][xStart]
			_prev_yStart = data.iloc[idx - 1][yStart]

			d, v = _CalculateVelocity_(_prev_time, row[TimeStamp], [_prev_xStart, _prev_yStart], [row[xStart], row[yStart]], dist_metric)
			velocity.append(v)
			distances.append(d)

	data['Velocity'] = velocity
	data[f'{distance_type.capitalize()}Distance'] = distances

	if keep_data_indexed:
		data.set_index([ParticleID, TripID], inplace = True)

	return data