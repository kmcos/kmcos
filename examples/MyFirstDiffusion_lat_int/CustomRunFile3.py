'''This file is made to run with MyFirstDiffusion. This file does steps 1 by 1 and records the site occupations for each step at each site. '''
import os
import math 
import pdb
from kmos.run import KMC_Model
from kmc_settings import *
model = KMC_Model()
atoms = model.get_atoms(geometry=False)

# represents the full directory path name that the kmos directory is in with directory name last, have to add the _ or we cannot retrieve the last character
dirpath_name = os.getcwd() + '_'


simulation_size = model.size[0] # model.size gives you the size of the arrays which would be [3,3] for a model
totalsites = simulation_size*simulation_size#with a sim_size of 3. 

spt = 20 # total number of steps
sps = 1 # total number of steps per "snapshot"
SNI = int(spt/sps) # number of s iterations  
Step = 0

SimulationName = 'MyFirstDiffusion' # Change to current simulation name for each run
filename1 = '%s_OccupationPopulations.csv' %(SimulationName) 
with open(filename1, 'a') as f1:
	# headers for file1
	f1.write('Step;')
	f1.write('Time;')
	f1.write('SiteA_SiteOccupation;')
	f1.write('SiteB_SiteOccupation;')
	f1.write('SiteC_SiteOccupation\n')
	for s in range(0,SNI+1): # snapshot iterations plus 1 because range always excludes the last number
		
		
		f1.write('%s;'%(Step))
		f1.write('%s;'%(atoms.kmc_time))
		f1.write('%s;'%(atoms.occupation[0])[0])
		f1.write('%s;'%(atoms.occupation[0])[1])	
		f1.write('%s\n'%(atoms.occupation[0])[2])

		model.do_steps(sps)
		Step += sps
		atoms = model.get_atoms(geometry=False) # Have to recall it everytime or it will not refresh atoms
