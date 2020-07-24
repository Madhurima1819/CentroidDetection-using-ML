# -*- encoding: utf-8 -*-

'''Automatic Self-Planning for LTE'''

__author__       = ['Debmalya Pramanik']
__author_email__ = ['Debmalya.Pramanik@ril.com']

__credits__      = {
	'Diego Vicente' : {
		'Work Title'  : 'Using Self-Organizing Maps to solve the Traveling Salesman Problem',
		'URL'         : 'https://diego.codes/post/som-tsp/',
		'Source Code' : 'https://github.com/DiegoVicen/som-tsp'
	}
}

__status__       = 'Development'
__version__		 = 0.10
__docformat__    = 'camelCasing'

__copyright__	 = 'Copyright (c) 2020 Debmalya Pramanik | Indian Institute of Technology (IIT), Dhanbad'

# init-Time Option Registrations
from .core.BaseNeuron import Neuron
from .core.MovingParticle import Particle
from .core.PlanningAlgorithms import KSOFM
from .commons.DecayFunctions import ( # this is Necessary and Reqd. for Creating Objects like LearningRate
		NoDecay,
		LinearDecay,
		ExponentialDecay,
		MultiplicativeDecay
	)