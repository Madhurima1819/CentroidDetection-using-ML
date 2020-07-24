# -*- encoding: utf-8 -*-

'''Contains added Functionalities as Required'''

import numpy as np
from ._selectFuncs import selectDistanceMetric

# Added Functionalities Related to CentroidDetection.BaseNeuron.Neuron
GroupNeuronLocation = lambda NeuronObjs : [neuron.currentLocation for neuron in NeuronObjs] # func. to Find all the Neuron-Locations

def ClosestNeuron(movingObject, neuronObject, distanceMetric : str = 'euclidean', **kwargs) -> [int, np.ndarray]:
    '''Find the Closest Neuron (i.e. Base Statation) to a UE-Location
    :param movingObject   : Pass the Moving-Object of the Format CentroidDetection.movingParticle.Partcle
    :param neuronObject   : Pass the Neuron-Object of the Format CentroidDetection.BaseNeuron.Neuron
    :param distanceMetric : Type of Distance-Metric to be Used [euclidean, manhattan]. Default: euclidean Distance-Metric

    Keyword Arguments
    -----------------
    :param ReturnDistance : (bool) Return the Min. Distance Obtained. Default False
    '''
    DistanceFunction = selectDistanceMetric(distanceMetric)
    distances        = [DistanceFunction(movingObject.RandomPosition, i) for i in neuronObject]
    closestNeuronIDX = distances.index(min(distances))

    ReturnDistance = kwargs.get('ReturnDistance', False)
    
    if ReturnDistance:
        return closestNeuronIDX, neuronObject[closestNeuronIDX], min(distances)
        
    return closestNeuronIDX, neuronObject[closestNeuronIDX]

# Added Functionalities for the CentroidDetection.Particle
_consecutiveDifference_ = lambda li_ : np.array([t - s for s, t in zip(li_, li_[1:])])