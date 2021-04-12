from kmcos.snapshots import *
import kmcos.snapshots_globals as sg
import os

#sg.simulation_name = model_name  #<--- You can change this to whatever you want, but this is the default. All it does is affect the filenames of the exports the format for this type would be MyFirstModel_TOFs_and_Coverages.csv.
#other common options are:
#sg.simulation_name = os.path.basename(__file__)[:-3] #<--- Uses the runfile name as part of the file names i.e. runfile_TOFs_and_Coverages.csv  . The [:-3] is to remove the ".py" from the end of the filename.
#sg.simulation_name = '%s_%s' %(model_name,random_seed) #<--- Includes the model_name and random seed (e.g., 6483) used for the KMC as part of the file names e.g., MyFirstModel_6483_TOFs_and_Coverages.csv


#Below sets up some "options" for running the snapshots.
sg.parameters_of_interest = None #['T','R'] #<-- put the parameters you want exported with each snapshot here. Can also put activation energy etc.
sps = 10 # <-- this is just an example
n_snapshots = 1 # <-- this is just an example
 
Ti = 300 #initial temperature
Tf = 325 #final temperature
B = 5 #beta, heating rate in Kelvin per second.



#The kmcos Model is initialized in create_headers
create_headers()

#If it is desired to run snapshots without writing output to a file, set sg.write_output = 'False'.
#If you want to start writing again, set sg.write_output = 'True' before running
#more snapshots.

#If you need to change a parameter after each snapshot, only do 1 snapshot at a time with n_snapshots=1.
T = Ti
prev_T = T
while T < Tf:
    #Set the 'previous' Temperature and time variables before running any steps.
    prev_T = T
    prev_t = sg.atoms.kmc_time
    #Run some steps as snapshots.
    do_snapshots(sps, n_snapshots)
    #update the time and temperature for after the snaphsot is over.
    t = sg.atoms.kmc_time
    Tincr = beta*(t-prev_t)	# calculate the value to increment the temperature by
    T_incremented = T + Tincr
    
    

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
