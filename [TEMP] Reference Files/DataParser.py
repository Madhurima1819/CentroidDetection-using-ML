# -*- encoding: utf-8 -*-

'''Parser for BerlinMOD (Secondo) Data'''

__author__       = 'Debmalya Pramanik'
__author_email__ = 'DebmalyaPramanik.005@gmail.com'

__status__       = 'Development'
__version__		 = 0.1
__docformat__    = 'camelCasing'

__copyright__	 = 'Copyright (c) 2020 Debmalya Pramanik | Indian Institute of Technology (IIT), Dhanbad'

import warnings
import numpy as np
import pandas as pd

from tqdm import tqdm as TQ
from datetime import datetime
from datetime import timedelta

from optimizationFunctions import profilingFunction
from CentroidDetection.commons.DistanceFunctions import EuclideanDistance

def AppendTrailingValues(timeLength : int) -> str:
    return {
        5 : lambda : ':00.000', # for time like 10:00
        8 : lambda : '.000',    # for time like 10:00:02
    }.get(timeLength, lambda : '')()
    
def DateTimeParser(val : str, refVal : str):
    if len(val) <= 10:
        if len(refVal.split()[1]) != 12:
            refVal = f'{refVal}{AppendTrailingValues(len(refVal.split()[1]))}'
            
        refVal = datetime.strptime(refVal, '%Y-%m-%d %H:%M:%S.%f')
        newVal = refVal - timedelta(seconds = 2)
        
    elif len(refVal) <= 10:
        if len(val.split()[1]) != 12:
            val = f'{val}{AppendTrailingValues(len(val.split()[1]))}'
            
        newVal = datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')
        refVal = newVal + timedelta(seconds = 2)
        
    else:
        if (len(val.split()[1]) != 12) or (len(refVal.split()[1]) != 12):
            val    = f'{val}{AppendTrailingValues(len(val.split()[1]))}'
            refVal = f'{refVal}{AppendTrailingValues(len(refVal.split()[1]))}'
            
        newVal = datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')
        refVal = datetime.strptime(refVal, '%Y-%m-%d %H:%M:%S.%f')
    
    return newVal, refVal
    
def CalculateVelocity(tStart, tEnd, startPoint, endPoint) -> [float, float, float]:
    time     = abs(tStart.timestamp() - tEnd.timestamp())
    distance = EuclideanDistance(np.array(startPoint), np.array(endPoint))
    
    return distance, time, distance / time

if __name__ == '__main__':
    print(f'Welcome to BerlinMOD Data-Parser v{__version__}\n')
    warnings.simplefilter('ignore') # Ignoring FutureWarning: The Panel class is removed from pandas.
    
    timer = profilingFunction('Reading BerlinMOD Data')
    BerlinMOD = pd.read_csv('./data/trips.csv', names = ['MOID', 'TRIPID', 'tStart', 'tEnd', 'xStart', 'yStart', 'xEnd', 'yEnd'], skiprows = 1)
    timer.checkPoint()
    
    TQ.pandas(desc = 'Parsing Time-Objects')
    BerlinMOD['tStart'], BerlinMOD['tEnd'] = zip(*BerlinMOD[['tStart', 'tEnd']].progress_apply(lambda x: DateTimeParser(x[0], x[1]), axis = 1))
    
    TQ.pandas(desc = 'Calculating Velocity')
    BerlinMOD['EuclideanDistance'], BerlinMOD['TimeTaken'], BerlinMOD['Velocity'] = zip(*BerlinMOD[['tStart', 'tEnd', 'xStart', 'yStart', 'xEnd', 'yEnd']]\
        .progress_apply(lambda x :CalculateVelocity(x[0], x[1], startPoint = [x[2], x[4]], endPoint = [x[3], x[5]]), axis = 1))
        
    timer = profilingFunction('Saving BerlinMOD Parsed-Data')
    BerlinMOD.to_csv('./output/BerlinMOD.csv', index = False)
    timer.checkPoint()