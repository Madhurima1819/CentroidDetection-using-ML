# -*- encoding: utf-8 -*-

'''Functions for Pre-Processing Datas/Others as Required'''

import numpy as np
import pandas as pd
from copy import deepcopy

def _particle(dataFrame : pd.DataFrame, **kwargs) -> np.ndarray:
	# Given a Data-Frame, process the Data for the AutoPlanning.Particle Class

	dataFrame = deepcopy(dataFrame) # this controls the SettingWithCopyWarning of pd.DataFrame
	# Setting the Keyword-Arguemnts as Below
	keysName  = kwargs.get('keysName', 'DEV_ID')
	timeArray = kwargs.get('timeArray', 'capturedOn')
	locations = kwargs.get('locations', ['xLocs', 'yLocs'])

	# Processing as Mentioned
	dataFrame['LocationPair']      = dataFrame[locations].apply(lambda x: (x[0], x[1]), axis = 1)
	keys, capturedOn, LocationPair = dataFrame.sort_values(keysName)[[keysName, timeArray, 'LocationPair']].values.T

	# Spllitng the Data into the Required Keys-Set
	ukeys, index       = np.unique(keys, True)
	capturedOnArray    = np.split(capturedOn, index[1:])
	LocationPairsArray = np.split(LocationPair, index[1:])

	return ukeys, capturedOnArray, LocationPairsArray