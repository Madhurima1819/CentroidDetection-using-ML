# -*- encoding: utf-8 -*-

'''Contain the Neuron Class - which is used in SOM for Finding the Centroid of the Moving Object'''

import random
import numpy as np

from string import ascii_uppercase
from ..support import selectDecayMethod

class Neuron:
    '''Defination of a Neuron Class - which is the Core Object in the Algorithm for Finding the Centroid of the Moving Particle
    :param neuronLocation : X-Y Position (i.e. Longitude-Latitude) of the Base-Station
    :param radiusValue    : Radius of the Search Space Area
    :param decayMethod    : Type of Decay to use for Reducing the Search Space Area Default: Exponential Decay (exponential)
    :param decayRate      : Rate of Decay
    
    Properties
    ----------
        1. curSearchRadius : Returns the Current Search-Space Radius of the Neuron
                             # calls the value {property} of the abc.ABCMeta Class
        2. currentLocation : Returns the Current Location of the Neuron in np.ndarray Format
        3. decayRadius     : Decay the radiusValue
                             # calls the decay() of the abc.ABCMeta Class
        4. TODO RETURN's the Shapely/GeoPandas Object of the Neuron with a Radius of self.searchRadius
           This can be Used to Easily Extrapolate the Number of Users in the Vicinity (useful for RB Criteria)
           - this Functionality is Available in jioGIS: to re-use the Functionality!
        5. NeuronInfo      : Returns the Information of the Neuron

    Functionalities
    ---------------
        1. Neuron.updateLocation() : Updates the Location of the Neuron to a New Position!
    '''
    def __init__(
             self,
             radiusValue    : int or float, # Start with a Large Radius, for More Exploration of the Environment
             neuronLocation : list or tuple = None, # if None is Passed, then a Random Neuron Location is Generated
             decayMethod    : str = 'MultiplicativeDecay',
             decayRate      : int or float = 0.1
        ):
        if neuronLocation is not None:
             self.xLoc, self.yLoc = np.random.random(size = 2)
        else:
             self.xLoc, self.yLoc = neuronLocation

        # radiusValue can either be Fixed for all the Neurons, or Variable for Each
        self.searchRadius = selectDecayMethod(decayMethod)(radiusValue, decayRate)

        # Optional self.args for Neuron Identification in Neuron.NeuronInfo()
        self.decayMethod  = decayMethod
        self.NeuronName   = 'N-' + ''.join([random.choice(ascii_uppercase) for _ in range(3)]) + '#' + str(random.randint(10, 99))

    @property
    def curSearchRadius(self) -> float:
        return self.searchRadius.value
    
    @property
    def currentLocation(self) -> np.ndarray:
        return np.array([self.xLoc, self.yLoc])
    
    @property
    def decayRadius(self) -> None:
        # Functionality to Decay the Search-Radius
        self.searchRadius.decay()

    @property
    def NeuronInfo(self) -> str:
        # Returns the Neuron Information
        objID           = f'<property-Neuron {self.NeuronName}:{id(self)}>'
        roundedLocation = [round(i, 3) for i in self.currentLocation]

        return f'{objID} with Current-Radius = {round(self.searchRadius.value, 5)}, having {self.decayMethod} Decay, Loc. at {roundedLocation}'

    def updateLocation(self, newLocation : list or tuple or np.ndarray) -> None:
        # Update the Location of the Neuron to a New Position
        self.xLoc = newLocation[0]
        self.yLoc = newLocation[1]