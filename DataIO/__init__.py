# -*- encoding: utf-8 -*-

"""DataIO - Parsers, Data Generator for RNN-Centroid Detection Project"""

__author__       = 'Debmalya Pramanik'
__author_email__ = 'DebmalyaPramanik.005@gmail.com'

__status__       = 'Development'
__version__		 = 0.1 # initial commit
__docformat__    = 'camelCasing'

__copyright__	 = 'Copyright (c) 2020 Debmalya Pramanik | Indian Institute of Technology (IIT), Dhanbad'

# init-Time Option Registrations
from .GenerateData import RandMOD01 # Specifies a Format of Random Data Generated as per BerlinMOD Format
from .DataParser import dist_date_parser