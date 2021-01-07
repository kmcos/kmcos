import sys
sys.path.insert(0,'../..') #This is for the janaf_data directory.
import kmcos.snapshots_globals as sg
from kmcos.snapshots import *
import os

#Below sets up some "options" for running the snapshots.
sg.parameters_of_interest = ['T','p_COgas','p_O2gas'] #<-- put the parameters you want exported with each snapshot here. Can also put activation energy etc.
sps = 300000 # <-- this is just an example
n_snapshots = 10 # <-- this is just an example

#Set parameters
sg.model.parameters.p_COgas = 1E-7
sg.model.parameters.p_O2gas = 1E-10
sg.model.parameters.T = 350

#Set temporal acceleration-related parameters
sg.model.set_buffer_parameter(400) #Default value to be trusted equals number of lattice sites (here 20x20 lattice is used)
sg.model.set_sampling_steps(20) #Default value
sg.model.set_threshold_parameter(0.2) #Default value
sg.model.set_execution_steps(200) #Default value

#The kmcos Model is initialized in create_headers
create_headers()

#If it is desired to run snapshots without writing output to a file, set sg.write_output = 'False'.
#If you want to start writing again, set sg.write_output = 'True' before running
#more snapshots.

#If you need to change a parameter after each snapshot, only do 1 snapshot at a time with n_snapshots=1.
do_snapshots(n_snapshots, sps, acc=True) #Set acceleration to True

#do_snapshots(500, 2) <-- here is another example of how to use the syntax.

#If you want to dump a configuration between snapshots, you may want to do something
#like this.
#sg.model.dump_config(sg.simulation_name + str(sg.steps_so_far))#


#below are  some examples of  arrays and lists that may be of interest.
print(sg.occ_header_array)
print(sg.TOF_data_list)
print(sg.occ_data_list)
#print("line 40 of the runfile, sg.last_snapshot_outputs:", sg.last_snapshot_outputs)
#print("line 41 of the runfile, sg.snapshot_output_headers:", sg.snapshot_output_headers)


#The final command below writes the simulation details to the logfile
create_log()
