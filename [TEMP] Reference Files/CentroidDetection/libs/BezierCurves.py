# -*- encoding: utf-8 -*-

'''Given a Set of n-Points Draws the Bezier Curve'''

__author__       = 'Debmalya Pramanik'
__author_email__ = 'Debmalya.Pramanik@ril.com'

__credits__      = {
	'Combination-Function from SciPy' : 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.comb.html',
	'Stack-Over Flow Users'           : {
		'thomi'      : 'https://stackoverflow.com/users/1304/thomi',
		'reptilicus' : 'https://stackoverflow.com/users/1443118/reptilicus'
	},
	'Bézier Curve Fitting Problem'    : 'https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy',
	'Bézier Information'              : [
		'https://javascript.info/bezier-curve',
		'http://processingjs.nihongoresources.com/bezierinfo/'
	]
}

__status__       = 'Production'
__version__		 = 0.1
__docformat__    = 'camelCasing'

__copyright__	 = 'Copyright (c) 2020 Debmalya Pramanik'

import warnings
import numpy as np

try:
	from scipy.misc import comb as nOk
	# SciPy >=0.19 uses from scipy.special import comb instead of from scipy.misc import comb
	warnings.warn('Old Version of SciPy Detected')
except ImportError:
	from scipy.special import comb as nOk

# Bernstein Polynomial of (n, i) as a Function of t
bernsteinPolynomial         = lambda i, n, t       : nOk(n, i) * ( t**i ) * (1 - t)**(n - i)
weightedBernsteinPolynomial = lambda i, n, t, r : nOk(n, i) * ( t**i ) * (1 - t)**(n - i) * r

def BezierCurve(points, nTimes = 1000, ratios = None):
	'''Given a Set of Control Points - Returns a Bezier Curve'''
	nPoints = len(points)
	xPoints = np.array([p[0] for p in points])
	yPoints = np.array([p[1] for p in points])

	# Defining a Time-Step of 't'
	t = np.linspace(0.0, 1.0, nTimes)

	# Finding the Polynomial Array
	if ratios is not None:
		if len(points) != len(ratios):
			raise ValueError(f'len(points) (= {points.shape[0]}) is not Equal to len(ratios) (= {ratios.shape[0]})')
		polynomial_array = np.array([weightedBernsteinPolynomial(i, nPoints - 1, t, r) for i, r in zip(range(0, nPoints), ratios)])
	else:
		polynomial_array = np.array([bernsteinPolynomial(i, nPoints - 1, t) for i in range(0, nPoints)])

	xVals = np.dot(xPoints, polynomial_array)
	yVals = np.dot(yPoints, polynomial_array)

	return xVals, yVals