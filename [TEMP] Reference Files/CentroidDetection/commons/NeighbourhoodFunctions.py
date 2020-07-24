# -*- encoding: utf-8 -*-

'''Neighbourhood Functions for Self-Organizing Maps. These distribution functions are:
	1. Bubble Distribution Function
	2. Gaussian Distribution Function
'''

import math

BubbleDistribution  = lambda dist, sigma : 1 if (dist <= sigma) else 0
GaussianDistributon = lambda dist, sigma : 0 if (math.pow(sigma, 2) == 0) else math.exp(- math.pow(dist, 2) / (2 * math.pow(sigma, 2)))