import sys
sys.path.insert(0,'../..') #This is for the janaf_data directory.
import kmcos.snapshots_globals as sg
from kmcos.snapshots import *
import os

#Below sets up some "options" for running the snapshots.
sg.parameters_of_interest = ['T','p_COgas','p_O2gas'] #<-- put the parameters you want exported with each snapshot here. Can also put activation energy etc.
sps = 3000000 # <-- this is just an example
n_snapshots = 5 # <-- this is just an example

#Set parameters
sg.model.parameters.p_COgas = 1E-7
sg.model.parameters.p_O2gas = 1E-10
sg.model.parameters.T = 350

#The kmcos Model is initialized in create_headers
create_headers()

#If it is desired to run snapshots without writing output to a file, set sg.write_output = 'False'.
#If you want to start writing again, set sg.write_output = 'True' before running
#more snapshots.

#If you need to change a parameter after each snapshot, only do 1 snapshot at a time with n_snapshots=1.
do_snapshots(n_snapshots, sps)

#now will do one larger snapshot.
sps = 3000000*5 
n_snapshots = 1 
do_snapshots(n_snapshots, sps)
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
