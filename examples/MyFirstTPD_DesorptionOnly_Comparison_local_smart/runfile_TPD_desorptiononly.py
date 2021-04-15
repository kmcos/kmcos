#!/usr/bin/env python

#Summary: This program creates a TPD simulation using a previously created model. It #updates the #temperature using how much time has passed and beta. The time is determined #by kmc_time. #Also, the program exports information after each set of steps is executed, #such as site #coverage, temperature, time, etc. 

from kmcos.run import KMC_Model
from ase import Atoms
from ase.io import write
from ase.visualize import view
import os
import sys
from kmc_model import base, lattice, proclist
import kmc_settings
import random
import multiprocessing
from math import log
import kmc_settings
from time import time as clock
from itertools import product
import pdb

# This function initializes starting and final temperatures(Ti and Tf), the species, Tupdate, and coverage. The random seed is generated using the random class. Then, simulate_tpd() is passed the starting and intial temperatures, beta, the coverage, the species, and the random seed.
def main():
	global ncalc
	global tstart 
	global Tupdate

	status = open('status.txt','w')
	counter = 0
	tstart = 0.0
	
	############################################# User Set Parameters 1 0f 2 #############################################################

	Ti = int(eval(input("Enter the initial starting temperature: "))) #starting temperature
	Tf = int(eval(input("Enter the final temperature: ")))	    #final temperature used in stopping the simulation
	maxsteps = int(eval(input("Enter the max number of steps: ")))    #max number of steps
	minsteps = int(eval(input("Enter the min number of steps: ")))    #min number of steps
	B = 5		     #beta
	spec = 'CO'	     #species
	Tupdate = 0.005      #used in updating the temperature
	ncovs = 1	     #number of coverages to be simulated
	nelems = 1	     #number of random seeds to be simulated with
	ncalc = ncovs*nelems #determine the number of simulations 

	covs = []	     #an array for the different coverages to be used
	ensemble = []	     #an array for the different random seeds to be used
	covs = [1]	     #the array containing the coverages to be used
	

	######################################################################################################################################

	for i in range(nelems): #populates the random seed array 
		r = random.randint(10,10000)
		ensemble.append(r)
	
	print("Starting calculations... ({0} in total)".format(ncalc))
	tstart = clock()
	po = multiprocessing.Pool()
	for cov in covs: #simulates the model using the different coverages and random 
		for element in ensemble: #seeds in the arrays
			po.apply_async(simulate_tpd, (Ti, Tf, B, cov, spec, element, maxsteps,minsteps), callback = cb)
	po.close()
	po.join()
	print("All done.")

def cb(i):

	global status
	global ncalc
	global counter
	global tstart

	tcur = clock()
	counter += 1
	status.seek(0)
	status.write('Done {0} out of {1} after {2} seconds.\t'.format(counter, ncalc, tcur-tstart))
	sys.stdout.flush()
	return

	
def simulate_tpd(Tinitial,Tfinal,beta,cov,species,element,maxstp, minstp):
	
	#******************************Initiating & opening*******************************
	# In this section, the files to be exported to are created and opened. Then, some of the initial conditions and headers are exported to files. The size and number of sites of the model are calculated. Then, the initial 		coverage is produced using the random seed and coverage that was set in the main() function. 
	
	path = 'tpd_info_{0}_{1}'.format(cov,element)
	prefix = "*****"+str(path)+"***** "
	print(prefix,"Starting run of",cov,species,"coverage at",Tinitial,"Kelvin...")
	
	os.mkdir(path)
	cov1 = open(path+'/site_coverages.txt','w')
	des = open(path+'/desorptions.txt','w')
	representation = open(path+'/representation.txt','w')
	cov2 = open(path+'/total_coverages.txt','w')
       
	info = open(path+'/info.txt','w')
	info.write("Starting temperature = {0} \nFinal temperature = {1} \nHeating rate = {2}\n".format(Tinitial, Tfinal, beta))
	info.write("Initial coverage = {0} of {1}\n".format(cov, species))
	info.write("Pseudo-random generator seed = {0}\n".format(element))
       
	cov1.write("Temperature[K]\tTime[s]\tDesorption_events\tSite_coverage_filled\tSite_coverage_empty\tDesorption_TOF\n")
	cov2.write("Temperature[K]\tTime[s]\tDesorption_events\tTotal_sitecoverage_filled\tTotal_sitecoverage_empty\n")

	model = KMC_Model(print_rates=False, banner=False)
	kmc_settings.random_seed = element #set the random seed to the seed that was generated
	model.parameters.T = Tinitial	   #the temperature parameter is set so that the processes' rate contstants reflect the temperature changes
	representation.write(str(model.__repr__)+'\n')
	representation.close()
	
	des.write("Temperature[K]\tTime[s]\tDesorption_events"+'\n')
	
	nsites = model.lattice.spuck   #sets the number of sites per cell
	vol = model.base.get_volume()  #sets the volume of the model(num of sites * num of cells)

	# dictionary of {species_name : corresponding int}
	reps = {}
	for i,spec in enumerate(sorted(kmc_settings.representations)):
		reps[spec] = i

	# initial coverage:	
	print(prefix,"Producing initial coverage...")
	nadsorbed = 0
	nads = int(round(cov*vol))#changed this temporarily(cov)
	
	X,Y,Z = model.lattice.system_size
	sites = [ [x,y,z, n+1] for (x,y,z,n) in product(list(range(X)), list(range(Y)), list(range(Z)), list(range(nsites))) ] # for loop to populate an array with every possible cell/site combination in the model; the range function excludes the last 														#number; for x,y,z the indices work out but for n, 1 has to be added for it to be correct
	random.seed(element) #sets the random seed to the random seed passed in
	for i in range(nads): #for loop for producing the coverage that was set previously
		while True:
			site = random.choice(sites)
			if model.lattice.get_species(site)==reps['empty']:
				model._put(site, model.proclist.co)
				nadsorbed += 1
				break
	
	model._adjust_database()
	info.write('Initial number of CO atoms = {0} (total of {1} sites)'.format(nadsorbed,vol))
	info.close()
	config = model._get_configuration()

	#*******************************Start*******************************
	#The initial temperature, min and max steps are set. The initial temperature is set according the the number passed into the simulate_tpd function. The min and max steps are set according to user input information. Then the 	model does a set number of steps to 'warm' the model up. Then, a for loop is entered until the final temperature is reached or the number desorbed is equal to the number adsorbed. In this loop, the model does steps and 		increments the temperature between snapshots. Then, it exports information if a molecule has been desorbed
	
	print(prefix,"Starting TPD...\n")
	
	
	atoms = model.get_atoms(geometry=True)
	write(path+'/initial.traj', atoms)
	
	################################################################## User Set Parameters 2 of 2 ####################################################################
	
	ndesorbed = 0
	maxsteps = maxstp	# max number of steps that should be in a snapshot
	minsteps = minstp	# min number of steps that should be in a snap shot
	steps = minsteps

	max_covChange = 0.5	# max percent of coverage change that should occur
	min_covChange = 0.0001	# min percent of coverage change that should occur
	covForDecSteps = .03	# percent coverage left, used for slowing the model down towards the end of the sim
	cov_final = .01		# the lowest amount of coverage before the simulation needs to stop
	curr_cov = (atoms.occupation[0])[0]	 # the current amount of coverage
	prev_cov = curr_cov			 # the previous coverage, used for determining coverage change
	
	T = Tinitial			# the starting temperature
	prev_T = T			# the previous temperature, used in exporting data 
	maxDeltaTpersnapshot = 5	# max number the temperature can increase by between snapshots
	
	prev_config = model._get_configuration()	# previous configuration, used for reseting the model
	prev_t = atoms.kmc_time				# previous kmc_time, used for reseting the model
	

	##################################################################################################################################################################

	while T < Tfinal and ndesorbed < nadsorbed and curr_cov > cov_final: #while the temperature hasn't reached the final temp, and all the molecules haven't desorbed

		desorbed = False
		model.parameters.T = T
		model.do_steps(steps)
		
		atoms = model.get_atoms(geometry=False)
		t = atoms.kmc_time
		curr_cov = (atoms.occupation[0])[0]
		prev_T = T

		Tincr = beta*(t-prev_t)			# calculate the value to increment the temperature by(if it passes all the checks)
		T_incremented = T + Tincr
		cov_change = (prev_cov- curr_cov)	# coverage change, used to see if any molecules have desorbed

		if Tincr > maxDeltaTpersnapshot:	# if the value to increment the temperature is too large, reset the model and decrease the steps by half
			model._set_configuration(prev_config)
			model.base.set_kmc_time(prev_t)
			model._adjust_database()
			steps = steps/2
			successfulresolution = False
			
			if ndesorbed == 0:
				T = T + maxDeltaTpersnapshot

			atoms = model.get_atoms(geometry=False)

		elif cov_change > max_covChange:	# if the coverage change is too large, reset the model and decrease the steps by half
			model._set_configuration(prev_config)
			model.base.set_kmc_time(prev_t)
			model._adjust_database()
			steps = steps/2
			successfulresolution = False
			atoms = model.get_atoms(geometry=False)

		elif cov_change < min_covChange:	# if the coverage change is too small, double the steps
			successfulresolution = True
			T = T_incremented
			steps = steps*2
			prev_cov = curr_cov
			prev_t = atoms.kmc_time
		else:					# if the checks have been passed, increment the temperature using the calculated T_incremented value
			successfulresolution = True
			T = T_incremented
			prev_cov = curr_cov
			prev_t = atoms.kmc_time
		
		if curr_cov < covForDecSteps:	# if the current coverage is lower than the set amount, decrease the steps by half and set minsteps to 1. This prevents the simulation crashing from too many steps
			minsteps = 1
			steps = steps/2

		if successfulresolution: 	# if the snapshot passed all of the tests
			desorbed = False 
			avg_T = (T + prev_T)/2

			print(prefix,"Avg Temp:",avg_T,"Time:", t, "\nSteps per update:", steps,"Coverage change:" , cov_change,"Tincr:", Tincr,'\n') 
		
			if cov_change != 0:	# if the coverage change was zero, no molecules desorbed, don't export the data
				desorbed = True
				recentdesorbed = cov_change*vol
				ndesorbed += recentdesorbed #counter for total number desorbed
	
			
	
			if desorbed: 		# if a molecule did desorb, export the data
				entry = str(avg_T)+'\t'+str(t)+'\t'+str(recentdesorbed)+'\t'#temp could be exported by linear fitting the tof calculations and picking whether to export curr or prev temp based on those calcs
				print(prefix,"DESORBED",ndesorbed, 'out of',nadsorbed, "Total sites:", model.base.get_volume(),'\n')
				des.write(entry+'\n')
				cov1.write(entry)
				cov2.write(entry)
				
				for spec in atoms.occupation:
					tot = 0.0
					for site in range(nsites):
						cov1.write(str(spec[site])+'\t')
						tot += spec[site]
					cov2.write(str(tot/nsites)+'\t')
				cov1.write(str(atoms.tof_integ[0]) + '\t')				
				cov1.write('\n')
				cov2.write('\n')
				
			
		if steps < minsteps: steps = minsteps	# if the steps are lower than the min amount of steps, set equal to the minsteps
		elif steps > maxsteps: steps = maxsteps # if the steps are higher than the max amount of steps, set equal to the maxsteps
		
		prev_config = model._get_configuration()
		
		sys.stdout.flush()

	cov1.close()
	cov2.close()
	des.close()	
	
	
	#*************************Finalize*******************************
	model.deallocate()
	print(prefix,"Finished!")
	status.close()	
	return

if __name__ == "__main__":
	main()
