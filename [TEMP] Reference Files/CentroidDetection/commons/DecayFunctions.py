# -*- encoding: utf-8 -*-

'''This Module List(s) out Various Decay Functions
Available Decay Functions are:
	1. Linear Decay Function,
	2. Exponential Decay Function,
	3. Multiplicative Decay Function

If No-Decay is Required, then for Code-Reusability - use NoDecay()
'''

import warnings
from math import exp as EXP
from abc import ABCMeta, abstractmethod

from ..errors import ValueWarning

class DecayFunction(metaclass = ABCMeta):
	'''Decay Class Base Function, implemented with a Design Pattern
	where, a Design Pattern, in Software Engineering, is a General Resusable Solution to a Commonly Occuring Problem.
	This Function can be inherited in a Child-Class to Define other User-Defined Function, which are not Already Defined.

	:param StartValue    : Initial Value i.e. N(0)
	:param DecayRate (λ) : Constant Ratio at which the Constant Value Decay over Time (τ)
	:param Threshold (τ) : Set the Min. Threshold, beyond which there will be no Decay, all Function has the Structure:
		>> StartValue(τ + 1) = f[StartValue(τ)] if StartValue(τ) <= τ else τ, where f() is the Desired Function

	Function Property
		DecayFunction.value() : Call this Function to Get the Current Value at Time (τ)
	'''
	def __init__(self, initalValue : int or float):
		self._value = initalValue # where Initial-Value is the Start Value with which the Code is Initiated

	@property
	def value(self):
		return self._value

	@abstractmethod
	def decay(self):
		pass # Defined a Decay Function Seperately

class NoDecay(DecayFunction):
	'''No-Decay is Defined for Code-Reusability of SOM, where N(τ + 1) = N(τ)'''
	def __init__(self, StartValue : int or float, DecayRate : int or float = 0, Threshold : int or float = None):
		self.DecayRate = DecayRate
		self.Threshold = Threshold
		super().__init__(StartValue)

		if self.DecayRate != 0.0:
			warnings.warn(f'NoDecay() is Static, got Decay Rate = {self.DecayRate}', ValueWarning)

		if self.Threshold != None:
			warnings.warn(f'NoDecay() is Static, got a Threshold of {self.Threshold}', ValueWarning)

	def decay(self):
		pass

class LinearDecay(DecayFunction):
	'''Linear Decay is Defined as: N(τ + 1) = N(τ) - λ'''
	def __init__(self, StartValue : int or float, DecayRate : int or float, Threshold : int or float = 0):
		self.DecayRate = DecayRate
		self.Threshold = Threshold
		super().__init__(StartValue)

		if (self._value - self.DecayRate) < self.Threshold:
			warnings.warn('Threshold is set too Low. Use NoDecay() if Required.', ValueWarning)

	def decay(self):
		if (self._value - self.DecayRate) >= self.Threshold:
			self._value -= self.DecayRate

class ExponentialDecay(DecayFunction):
	'''Exponential Decay is Defined as: N(τ + 1) = N(τ) * e^(-λ)'''
	def __init__(self, StartValue : int or float, DecayRate : int or float, Threshold : int or float = 0):
		self.DecayRate = DecayRate
		self.Threshold = Threshold
		super().__init__(StartValue)

		if (self._value * EXP(-self.DecayRate)) < self.Threshold:
			warnings.warn('Threshold is set too Low. Use NoDecay() if Required.', ValueWarning)

	def decay(self):
		if (self._value * EXP(-self.DecayRate)) >= self.Threshold:
			self._value *= EXP(-self.DecayRate)

class MultiplicativeDecay(DecayFunction):
	'''Fast-Exponential Decay is Defined as: N(τ + 1) = N(τ) * λ'''
	def __init__(self, StartValue : int or float, DecayRate : int or float, Threshold : int or float = 0):
		self.DecayRate = DecayRate
		self.Threshold = Threshold
		super().__init__(StartValue)

		if (self._value * self.DecayRate) < self.Threshold:
			warnings.warn('Threshold is set too Low. Use NoDecay() if Required.', ValueWarning)

		if self.DecayRate >= 1.0:
			warnings.warn(f'Expects Decay Rate < 1, got {self.DecayRate}', ValueWarning)

	def decay(self):
		if (self._value * self.DecayRate) >= self.Threshold:
			self._value *= self.DecayRate