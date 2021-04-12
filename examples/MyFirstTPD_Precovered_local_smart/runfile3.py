from kmcos.snapshots import *
import kmcos.snapshots_globals as sg
import kmcos.snapshots as snapshots
import kmcos.throttling_globals as tg
import kmcos.throttling as throttling
import os
import export_import_library as eil
import numpy as np
# Random seed
random_seed = -731543673

#sg.simulation_name = model_name  #<--- You can change this to whatever you want, but this is the default. All it does is affect the filenames of the exports the format for this type would be MyFirstModel_TOFs_and_Coverages.csv.
#other common options are:
#sg.simulation_name = os.path.basename(__file__)[:-3] #<--- Uses the runfile name as part of the file names i.e. runfile_TOFs_and_Coverages.csv  . The [:-3] is to remove the ".py" from the end of the filename.
#sg.simulation_name = '%s_%s' %(model_name,random_seed) #<--- Includes the model_name and random seed (e.g., 6483) used for the KMC as part of the file names e.g., MyFirstModel_6483_TOFs_and_Coverages.csv


#Below sets up some "options" for running the snapshots.
sg.parameters_of_interest = ['T'] #['T','R'] #<-- put the parameters you want exported with each snapshot here. Can also put activation energy etc.
sps = 10 # <-- this is just an example
n_snapshots = 1 # <-- this is just an example
#If you need to change a parameter after each snapshot, only do 1 snapshot at a time with n_snapshots=1. 
 
Ti = 300 #initial temperature
Tf = 325 #final temperature
beta = 5 #beta, heating rate in Kelvin per second.
load_simulation_state = True


# File names for loading/saving parameters
tg_load_file = sg.simulation_name + 'throttling_parameters.txt'
tg_save_file = sg.simulation_name + 'throttling_parameters.txt'
sg_load_file = sg.simulation_name + 'snapshots_parameters.txt'
sg_save_file = sg.simulation_name + 'snapshots_parameters.txt'

# Export/import module objects for saving/loading data
tg_module = eil.module_export_import(tg_save_file, tg_load_file, tg)
sg_module = eil.module_export_import(sg_save_file, sg_load_file, sg)


if load_simulation_state:
    # Load modules
    sg_module.load_params()
    #tg_module.load_params()

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

    # Update the cutoff time
    #tg.cutoff_time = cutoff_time

    # The following assignment (and similar assignments elsewhere) is *magical*.
    # It invokes a hidden __setattr__ method of the Model_Parameters class that
    # calls the set_rate_constants() function to update the values of the rate
    # constants in the Fortran base module. Any other kind of assignment will
    # require an explicit call to set_rate_constants(). *Failure to update the
    # rate constants in the Fortran module will result in wrong results!*
    T = Ti + beta * (sg.kmc_time)
    sg.model.parameters.T = T
    print("Restarting from old simulation. Current temperature is " +
        str(T) + " K. Current time is " + str(sg.kmc_time) + " s.\n")
else:
    snapshots.seed_PRNG(restart=False, state=random_seed)
    T = Ti
    sg.model.parameters.T = T
    sg.kmc_time = 0.0
    #The kmcos Model is initialized in create_headers
    create_headers()
    #If it is desired to run snapshots without writing output to a file, set sg.write_output = 'False'.
    #If you want to start writing again, set sg.write_output = 'True' before running
    #more snapshots.
    

#Here is the TPD/TPR loop.
prev_T = T
while T < Tf:
    #Set the 'previous' Temperature and time variables before running any steps.
    prev_T = T
    prev_t = sg.atoms.kmc_time
    #Run some steps as snapshots.
    do_snapshots(sps=sps, n_snapshots=n_snapshots)
    #update the time and temperature for after the snaphsot is over.
    t = sg.atoms.kmc_time
    Tincr = beta*(t-prev_t)	# calculate the value to increment the temperature by
    T = T + Tincr
    sg.model.parameters.T = T
    
    

#do_snapshots(500, 2) <-- here is another example of how to use the syntax.

#If you want to dump a configuration between snapshots, you may want to do something
#like this.
#sg.model.dump_config(sg.simulation_name + str(sg.steps_so_far))#


#below are  some examples of  arrays and lists that may be of interest.
#print sg.occ_header_array
#print sg.TOF_data_list
#print sg.occ_data_list
#print("line 40 of the runfile, sg.last_snapshot_outputs:", sg.last_snapshot_outputs)
#print("line 41 of the runfile, sg.snapshot_output_headers:", sg.snapshot_output_headers)


#The final command below writes the simulation details to the logfile
create_log()
