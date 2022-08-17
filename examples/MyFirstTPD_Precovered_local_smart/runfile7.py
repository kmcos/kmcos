from kmcos.snapshots import *
import kmcos.snapshots_globals as sg
import kmcos.snapshots as snapshots
import kmcos.throttling_globals as tg
import kmcos.throttling as throttling
import os; import sys
import export_import_library as eil


##### SOME LINES THAT SHOULD NOT NORMALLY BE CHANGED####

# File names for loading/saving parameters (related to the export import module and throttling module)
# These will not really be used for this example, but are good lines to have.
# In the future, this may be done automatically within kmcos.
tg_load_file = sg.simulation_name + 'throttling_parameters.txt'
tg_save_file = sg.simulation_name + 'throttling_parameters.txt'
sg_load_file = sg.simulation_name + 'snapshots_parameters.txt'
sg_save_file = sg.simulation_name + 'snapshots_parameters.txt'

# Export/import module objects for saving/loading data
tg_module = eil.module_export_import(tg_save_file, tg_load_file, tg)
sg_module = eil.module_export_import(sg_save_file, sg_load_file, sg)


#### LOADING AND INITIALIZING #####
# Random seed
random_seed = -731543673 #can be any integer. only used if not loading a simulation. The PRNG_state that will be generated is a list, unlike the seed, which is an integer.

load_simulation_state = False #This is a user setting that will affect what happens below. It is for continuing a simulation from where one left off.

if load_simulation_state == False: #initialize the seed.
    snapshots.seed_PRNG(restart=False, state=random_seed)
elif load_simulation_state == True: #load everything and set the SEED to be what it was before.
    # Load modules
    sg_module.load_params()
    tg_module.load_params()

    # Reset number of steps and time
    sg.model.base.set_kmc_time(sg.kmc_time)
    sg.model.base.set_kmc_step(sg.steps_so_far)
    sg.atoms.kmc_step = sg.steps_so_far

    # Load the lattice
    sg.model._set_configuration(np.array(sg.config))
    sg.model._adjust_database()

    # Read the PRNG state, if available, and set it in the model
    snapshots.seed_PRNG(restart=True, state=sg.PRNG_state)
    # Update the snapshot number
    tg.current_snapshot += 1


##### GETTING SETTINGS READY FOR THE SIMULATION ####

#Snapshots module options.
sg.parameters_of_interest = ['T'] #['T','R'] #<-- put the parameters you want exported with each snapshot here. Can also put activation energy etc.
sps = 1000 # <-- the kmc steps per snapshot. Defining this variable now is optional, and also the value can be changed later.
n_snapshots = 1 # <-- The total number of snapshots to do. Defining this variable now is optional, and also the value can be changed later.
tps = 1.0 #this sets the maximum amount of time per snapshot.

#Generally, if a user needs to change a parameter after each snapshot, only do 1 snapshot at a time with n_snapshots=1. 
#This example is a temperature programmed reaction example, so n_snapshots=1 makes sense, since we need to change the temperature after each snapshot.
 
#Some simulation settings.
Ti = 300 #initial temperature
Tf = 345 #final temperature
beta = 5 #beta, heating rate in Kelvin per second.



# Update the cutoff time
tg.cutoff_time = 1E6 #the throttling module's cutoff time is in seconds. We are not using that feature in this simulation, but it could be set here, for example.


if load_simulation_state == False:
    sg.model.parameters.T = 300 #set the initial temperature.
    T = Ti
    sys.stdout.write("Starting a fresh simulation. Current temperature is " +
        str(T) + " K. Current time is " + str(sg.kmc_time) + " s.\n")
    #The kmcos Model is initialized in create_headers
    create_headers()
    #If it is desired to run snapshots without writing output to a file, set sg.write_output = 'False'.
    #If you want to start writing again, set sg.write_output = 'True' before running
    #more snapshots.
elif load_simulation_state == True:
    #The temperatures will have been loaded already, but we need to set our runfile's variable.
    T =  sg.model.parameters.T
    sys.stdout.write("Restarting from old simulation. Current temperature is " +
        str(T) + " K. Current time is " + str(sg.kmc_time) + " s.\n")
  
    
# The following assignment (and similar assignments elsewhere) is *magical*.
# It invokes a hidden __setattr__ method of the Model_Parameters class that
# calls the set_rate_constants() function to update the values of the rate
# constants in the Fortran base module. Any other kind of assignment will
# require an explicit call to set_rate_constants(). *Failure to update the
# rate constants in the Fortran module will result in wrong results!*
sg.model.parameters.T = T

#### SIMULATING AFTER ALL INITIALIZING IS DONE ####
 
#Here is the TPD/TPR loop.
while T < Tf:
    #Set the 'previous' Temperature and time variables before running any steps.
    last_T = T
    last_t = sg.atoms.kmc_time
    #Run some steps as snapshots.
    # Note that the below command will try to run n_snapshots with a certain 'steps per snapshot'
    # but for any given snapshot, if thte time per snapshot (tps) is reached, the snapshot will be stopped.
    # in this way, no snapshot will be greater than 1 second.

    do_snapshots(sps=sps, n_snapshots=n_snapshots, tps=tps)
    #update the time and temperature for after the snaphsot is over.
    t = sg.atoms.kmc_time
    Tincr = beta*(t-last_t)	# calculate the value to increment the temperature by
    T = T + Tincr
    sg.model.parameters.T = T
    print("Snapshot taken. New temperature:", T)
    	
      
#The final command below writes the simulation details to the logfile
create_log()
