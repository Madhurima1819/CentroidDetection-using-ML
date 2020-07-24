# -*- encoding: utf-8 -*-

'''Contains the Defination of an UE (User Equipment)'''

import random
import warnings
import numpy as np

try:
	import BezierCurves
except ImportError:
	from ..libs import BezierCurves

from ..errors import ValueWarning
from ..support import _consecutiveDifference_
from sklearn.preprocessing import MinMaxScaler

class Particle:
	'''Particle is defined as an Object in Space, that has an (x, y)-coordinates.
	For our case, this Particle moves in the defined n-Dimensional Space (considering n = 2) with time.
	:param UIN           : Unique Identification Number (UIN) of the Particle, which can be any ID associated with it.
	:param samplingRatio : Sampling Ratio is the Number of Epoch for CentroidDetection.core.PlanningAlgorithms.KSOFM Implementations

	Keyword Arguments
	-----------------
	:param properties      : Other Properties associated with the Particle, for example Velocity, Weight etc. [Default None]
	:param BezierCurveMode : Should use Weighted Bezier Curve or not : ['weighted', 'none']. Default: Weighted Bezier Curve ('weighted')

	Instructions on Passing Data to Make a Particle-Class
	-----------------------------------------------------
	STEP 1 : First Generate Location Pair on the Total Data Frame on Column Name LocationPair using:
	>> data['LocationPair'] = data[['xLocs', 'yLocs']].apply(lambda x: (x[0], x[1]), axis = 1)

	STEP 2 : Sort the DataFrame and Create Three-Iterables as Follows, following NumPy Commands:
	>> keys, capturedOn, LocationPair = data.sort_values('DEV_ID')[['DEV_ID', 'capturedOn', 'LocationPair']].values.T
	>> ukeys, index = np.unique(keys, True)

	# Generation of ND-Array Objects
	>> capturedOnArray    = np.split(capturedOn, index[1:])   # which is the TimeArray for all the UE
	>> LocationPairsArray = np.split(LocationPair, index[1:]) # which is the LocationPairs for all the UE

	STEP 3 : Next you can Generate Particle-Class for all the Unique Moving-Object using for-Loop as Follows:
	>> for idx in range(n): # where n-Number of Unique Particles is Present in the Dataset
	...		CentroidDetection.Particle(
				UIN           = ukeys[idx],             # this is the DEV_ID (in-case of NVPM Data)
				TimeArray     = capturedOnArray[idx],
				LocationPairs = LocationPairsArray[idx]
			)

	NOTE: You can use the CentroidDetection.support._particle as Follows to Generate ukeys, capturedOnArray, and LocationPairsArray
	>> ukeys, capturedOnArray, LocationPairsArray = CentroidDetection.support._particle(data[['DEV_ID', 'xLocs', 'yLocs']])

	Example (pandas) DataFrame Object
	---------------------------------
	RowKey     DEV_ID     capturedOn     xLocs       yLocs       LocationPair
	123451     DEV_IDA01  1578068722500  12.123456   10.123456   (12.123456, 10.123456)
	123452     DEV_IDA01  1578068722505  12.123456   10.123456   (12.123456, 10.123456)
	123453     DEV_IDA01  1578068722513  12.123456   10.123456   (12.123456, 10.123456)
	123454     DEV_IDA02  1578068722608  12.123456   10.123456   (12.123456, 10.123456)
	123455     DEV_IDA02  1578068722617  12.123456   10.123456   (12.123456, 10.123456)
	'''
	def __init__(
			self,
			UIN           : int or str, # float applicable, but Not-Preffered
			TimeArray     : list,
			LocationPairs : np.ndarray,
			samplingRatio : int = 2500,
			**kwargs
		):

		self.UIN             = UIN
		self.TimeArray       = TimeArray
		self.LocationPairs   = LocationPairs
		self.samplingRatio   = samplingRatio

		# Keyword Arguments
		properties = kwargs.get('properties', None) # else pass in Dictionary Format

		# Understanding Inserted Data Type, and Type Conversion when Required
		if type(self.LocationPairs) != np.ndarray:
			warnings.warn('type(self.LocationPairs) != np.ndarray', ValueWarning)
			self.LocationPairs = np.array(self.LocationPairs)
		
		# Generation of Bezier Curve
		if self.LocationPairs.shape[0] == 1:
			self.xVals, self.yVals = self.LocationPairs[0] # since LocationPairs is a list of tuples
		else:
			self.BezierCurveMode   = kwargs.get('BezierCurveMode', 'weighted')
			self.xVals, self.yVals = self.BezierCurve

		# Dynamically Send the Current User Location
		self._CurrentUserLocation_ = iter(CurrentUserLocation(self.xVals, self.yVals, self.samplingRatio))

	@property
	def BezierCurve(self):
		if self.BezierCurveMode == 'weighted':
			xVals, yVals = BezierCurves.BezierCurve(self.LocationPairs, nTimes = self.samplingRatio, ratios = self._WeightRatio_)
		else:
			xVals, yVals = BezierCurves.BezierCurve(self.LocationPairs, nTimes = self.samplingRatio) # Considering No-Ratio's Associated
		return xVals, yVals
	

	@property
	def _WeightRatio_(self):
		# this Calculates the Weights that is to be Assigned to Each Control-Point
		_consecutiveDifference = _consecutiveDifference_(self.TimeArray)

		TimeScalar = MinMaxScaler(feature_range = (0.001, 0.002))
		_consecutiveDifference = TimeScalar.fit_transform(_consecutiveDifference.reshape(-1, 1)).reshape(1, -1)

		Weights     = np.ones(shape = len(self.TimeArray) - 1) - _consecutiveDifference
		Weights     = np.insert(Weights, 0, 1) # the First Weight is Always 1
		Weights[-1] = 1 # Assigining Equal Weitage at Initial and Ending Position, why (?)

		return Weights

	@property
	def ParticleInfo(self):
		# Returns the UE Information - useful for Logging Purpose - with UIN Masking Feature
		return f"<property-Particle {self.UIN}:{id(self)}>"

	@property
	def StartPosition(self):
		# Returns the Initial Position of the UE
		if self.LocationPairs.shape[0] == 1:
			return (self.xVals, self.yVals)
		return (self.xVals[0], self.yVals[0])

	@property
	def TargetPosition(self):
		# Returns the Final Position of the UE
		if self.LocationPairs.shape[0] == 1:
			return (self.xVals, self.yVals)
		return (self.xVals[-1], self.yVals[-1])

	def CurrentPosition(self):
		# This Returns and Updates the Location of the UE based on the Bézier Curve Specifications
		if self.LocationPairs.shape[0] == 1:
			return (self.xVals, self.yVals)

		# Removing the First Element from List, so that the Start-Position is Updated!
		self.xVals, self.yVals = np.delete(self.xVals, 0), np.delete(self.yVals, 0) # this method is Permanent!

		# This also keeps in Check that No Value Error is Raised - if self.samplingRatio > KSOFM.EpochCount
		return next(self._CurrentUserLocation_)

	@property
	def RandomPosition(self):
		# Returns a Random Location from the Set of Bezier Curve
		if self.LocationPairs.shape[0] == 1:
			return (self.xVals, self.yVals)

		_randomPoint = random.randint(0, len(self.xVals) - 1)
		return (self.xVals[_randomPoint], self.yVals[_randomPoint])

class CurrentUserLocation:
	'''Iterator-Class of Python to Get the Current Location of the UE'''
	def __init__(self, xLocs, yLocs, samplingRatio):
		self.xLocs       = xLocs
		self.yLocs       = yLocs
		self.samplingRatio = samplingRatio

	def __iter__(self):
		self._StartIndex_  = 0 # Indexing in Python Starts from Zero, fetches the First Location of the UE
		return self

	def __next__(self):
		if self._StartIndex_ < self.samplingRatio:
			_curPos_ = (self.yLocs[self._StartIndex_], self.xLocs[self._StartIndex_])
			self._StartIndex_ += 1

			return _curPos_
		else:
			raise StopIteration(f'Got Sampling Ratio {self.samplingRatio + 1}, which is not Equal to KSOFM Epochs.')