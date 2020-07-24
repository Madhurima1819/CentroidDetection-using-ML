# -*- encoding: utf-8 -*-

import time
import random
import pandas as pd
from tqdm import tqdm as TQ

### --- Internal Functions --- ###
_HEXCodeGenerate_ = lambda CodeLength : ''.join([random.choice('0123456789ABCDEF') for _ in range(CodeLength)])

### --- Main Function(s) --- ###
def RandMOD01(MaxParticles : int = 255, MaxPoint : int = 100, **kwargs) -> dict:
	'''RandMOD01 : Random Data based on BerlinMOD Format
	Except, the Data and all the Particles is Generated Randomly
	The Coordinates associated is also Randomly Generated'''
	ParticleIDs = []; NumTrips = [] # List of Unique Particle IDs and Number (Random) of Trips for Each
	for _ in TQ(range(MaxParticles), desc = f'Gen. {MaxParticles} Unique Particles'):
		numUniqueTrips = random.randint(1, 15)

		BIT7_HEX = _HEXCodeGenerate_(CodeLength = 7)
		BIT2_LEN = hex(numUniqueTrips)[2:].upper()
		BIT7_DEC = str(random.randint(0, int(1e7 - 1))).zfill(7)

		NumTrips.append(numUniqueTrips)
		ParticleIDs.append(f"{BIT7_HEX}:{BIT2_LEN}:{BIT7_DEC}")

	if len(set(ParticleIDs)) != MaxParticles:
		raise ValueError(f"{MaxParticles} Unique Particles is Not-Generated. A Simple re-run might Fix the Problem.")

	# Settings xLims, yLims from kwargs
	xlim = kwargs.get('xlim', (-10, 10))
	ylim = kwargs.get('ylim', (-10, 10))
	tnum = kwargs.get('set_trip_sub_numbering', True) # Generate a Seperate Number for Each Trip-ID

	# Generating Final Data
	GenData = {
		'ParticleID' : [], # Particle ID
		'TripID'     : [], # Trip ID associated with each Particle
		'TimeStamp'  : [], # in epoch-Format
		'xStart'     : [],
		'yStart'     : []
	}

	if tnum:
		GenData['TripSubNum'] = []

	for idx, ParticleID in TQ(enumerate(ParticleIDs), desc = 'Generating Final dict() Data'):
		for TripID in range(NumTrips[idx]):
			subNumber = 0
			StartTime = random.randint(int(1e8), int(1e9 - 1))

			for i in range(random.randint(1, MaxPoint)): # each Trip can have Max. of MaxPoint-Travel Points
				GenData['ParticleID'].append(ParticleID)
				GenData['TripID'].append(f'TRIP-#{str(TripID).zfill(2)}')

				GenData['TimeStamp'].append(StartTime)
				GenData['xStart'].append(random.randint(xlim[0], xlim[1]))
				GenData['yStart'].append(random.randint(ylim[0], ylim[1]))

				if tnum:
					GenData['TripSubNum'].append(subNumber)

				subNumber += 1
				StartTime += random.randint(3, 17)

	return GenData

if __name__ == '__main__':
	mParts = int(input('Max. no. of Particles (int) : '))
	mPoint = int(input('Max. no. of Points for Each Particles (int) : '))

	data = RandMOD01(MaxParticles = mParts, MaxPoint = mPoint)
	data = pd.DataFrame(data)

	# Generating File
	fName = f'../data/RandMOD_{int(time.time())}.csv' # STATIC FOLDER NAME
	print(f'Saved at : {fName}')
	data.to_csv(fName, index = False)