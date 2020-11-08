The following descriptions are to aid in the use of the snapshots module.

The global variables used in each of the functions are found in the file
snapshots_globals.py

The file snapshots.py contains 4 functions:

1) create_headers()
	- creates the .csv file and writes the headers of species and TOF process
	names
	- optional arguments for the function are print_all_parameters and
	write_output.
		- if print_all_parameters = 'True', all of the parameters for the
		simulation will be printed.  Otherwise, only specified parameters
		in the global variable 'parameters_of_interest' will be printed.
		'True' is the default.
		- if write_output = 'True', then the files will be created and
		written, otherwise they will not.  'True' is the defualt


2) do_snapshots_time(tps, n_snapshots)
	- executes the model.do_steps_time() kmcos command and extracts the tof and 
	concentration data from the sequence of steps to the file created in 
	create_headers().  Each sequence of steps here will correspond to a given
	increment of time.  
		- the argument tps stands for 'time per snapshot' and each execution
		of model.do_steps_time will be for this specified increment.
		- n_snapshots is the total number of snapshots that user wants to run

3) do_snapshots(sps, n_snapshots)
	- executes the model.do_steps() kmcos command and extracts the tof and 
	concentration data from the snapshot to the file created in create_headers().
		- the argument sps stands for 'steps per snapshot'.  So, an sps
		of 1000 would equate to model.do_steps(1000) in kmcos.
		- n_snapshots is the total number of snapshots the user wants to run

4) create_log()
	- this function executes when called if the global variable write_output
	is set to 'True' and creates a log file for the kmcos simulation
	-optionally prints all parameters at the current kmcos step when called
		- if print_all_parameters = 'True' (this is the default)
	-optionally dumps the configuration
		- if dump_configuration = 'True', the configuration will be dumped
		('True' is the default)


================================================================================
================================================================================
=============================  GLOBAL VARIABLES ================================
================================================================================
================================================================================

The following global variables need to be modified by the user.  All other 
globals should remain the default value that they are set in snapshots_globals.py.

The globals can be modified within a runfile by the following procedure:
import snapshots_globals as sg
sg.write_output = 'True' or 'False'
This example would decide whether or not to write the output files.

parameters_of_interest: this is a list of strings corresponding to the kmcos parameter
names e.g. ['T'] would print the temperature parameter

simulation_name: This is a string that specifies the simulation name and this
name will be used to name each of the output files


























