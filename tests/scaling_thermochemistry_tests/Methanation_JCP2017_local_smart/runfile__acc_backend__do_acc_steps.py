from kmcos.snapshots import *
import kmcos.snapshots_globals as sg
import os

#Below sets up some "options" for running the snapshots.
sg.parameters_of_interest = ['T','p_COgas','p_H2gas','p_CH4gas','p_H2Ogas'] #<-- put the parameters you want exported with each snapshot here. Can also put activation energy etc.
sps = 1000000 # <-- this is just an example
n_snapshots = 10 # <-- this is just an example

#Set parameters
sg.model.parameters.E_C=1.65 #Point A in JCP 2017
sg.model.parameters.E_O=-0.6 #Point A in JCP 2017

#Set temporal acceleration-related parameters
sg.model.set_buffer_parameter(1) #Use very aggressive scaling for test simulation
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

#now do more snapshots that are longer.
sps = 10000000 # <-- this is just an example
n_snapshots = 5 # <-- this is just an example
do_snapshots(n_snapshots, sps, acc=True)

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
