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
n_snapshots = 10 # <-- this is just an example


#The kmcos Model is initialized in create_headers
create_headers()

#If it is desired to run snapshots without writing output to a file, set sg.write_output = 'False'.
#If you want to start writing again, set sg.write_output = 'True' before running
#more snapshots.

#If you need to change a parameter after each snapshot, only do 1 snapshot at a time with n_snapshots=1.
do_snapshots(sps, n_snapshots)

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

# plot_configuration(self, filename = '', resolution = 150, scale = 20, representation = '', plot_settings = {}):

#The first plot_configuration will use default arguments to construct the plot and export as "plottedConfiguration.png"
#sg.model.plot_configuration()

#The second plot_configuration will use the atomic argument to contruct the plot and export as "atomic_view.png"
#for the filename, you can specify with or without the .png at the end. This function will automatically convert to .png file
sg.model.plot_configuration(filename='MyFirstSnapshots_atomic_view', resolution=100, scale=20, representation='atomic')


plot_settings = {
    "y_label": "y_direction",
    "x_label": "x_direction",
    "legendLabel": "Species",
    "legendExport": False,
    "legend": True,
    "figure_name": "Plot",
    "dpi": 220,
    "speciesName": True,
    "num_x_ticks": 3,
    "num_y_ticks": 3,
    }
#the second plot_configuration here will construct the plot using the above dictionary and export the file as "Plot.png"
# Note that the spatial representation plots by default, but you can always specify in representation
sg.model.plot_configuration(representation='spatial', plot_settings=plot_settings)