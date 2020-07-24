# -*- encoding: utf-8 -*-

import warnings

class ValueWarning(Warning):
	def __init__(self, message : str):
		self.message = message

	def __str__(self):
		return f'{self.message}\nThis Warning is Raised if the Input/Output Value does not meet the Expected Criteria'