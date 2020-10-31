#The following functions can be utilized to run a KMOS simulation with a user
#defined snapshot size.  The associated KMC data (simulation name, 
#parameters of interest (user defined), atoms.tof_data, atoms.tof_integ, 
#atoms.occupation) will be written to .csv files.  In addition, the 
#configuration and a simulation log will be written when the simulation is complete.
import timeit
import numpy
from kmc_settings import *
import kmos.snapshots_globals as sg

#This function creates the output file for the TOF data, occupations data and 
#parameters file. The file that is created to hold the data is called 
#simulation_name_TOFs_and_Coverages.csv where simulation_name is user defined in
#snapshots_globals.py.  The parameters of interest will be printed to the same 
#file, if any exist.  If desired, parameter initial values will be written to a 
#separate file called initial_parameters.txt.  By default, the output file of
# the  .csv file is created and  initial_parameters.txt  written, but these 
# output files can be turned off by the option of 'True' or 
#'False' for write_output.

def create_headers(print_all_parameters='True',write_output='True'):
#Keeping track of the start time for runtime info
	sg.start = timeit.default_timer()
#modify parameters of interest in snapshot_globals.py
	parameters_of_interest_sp=sg.parameters_of_interest
	sg.write_output = write_output
#Create the .csv file and write the column headers
	if sg.write_output == 'True':
	#Check the parameters of interest and write them if requested
		data_file_name = sg.simulation_name + str('_TOFs_and_Coverages.csv')
		simulation_data = open(data_file_name, 'w')
		if parameters_of_interest_sp != 'None':
			simulation_data.write('Simulation_name,')
			simulation_data.write('Step,')
			simulation_data.write('Time_(s),')
			simulation_data.write('sps/tps,')
			sg.snapshot_output_headers.append('Simulation_name')
			sg.snapshot_output_headers.append('Step')
			sg.snapshot_output_headers.append('Time_(s)')
			sg.snapshot_output_headers.append('sps/tps')
			for i in range(len(parameters_of_interest_sp)):
				simulation_data.write('%s,' %(parameters_of_interest_sp[i]))
				sg.snapshot_output_headers.append(parameters_of_interest_sp[i])
		else:
			simulation_data.write('Simulation_name,')
			simulation_data.write('Step,')
			simulation_data.write('Time_(s),')
			simulation_data.write('sps/tps,')
			sg.snapshot_output_headers.append('Simulation_name')
			sg.snapshot_output_headers.append('Step')
			sg.snapshot_output_headers.append('Time_(s)')
			sg.snapshot_output_headers.append('sps/tps')
	#Write the TOF_headers
		for i in range(len(sg.TOF_header_array)):
			simulation_data.write('%s_tof_data,' %(sg.TOF_header_array[i]))
			sg.snapshot_output_headers.append(sg.TOF_header_array[i] + 'tof_data')
		for i in range(len(sg.TOF_header_array)):
			simulation_data.write('%s_tof_integ,' %(sg.TOF_header_array[i]))
			sg.snapshot_output_headers.append(sg.TOF_header_array[i] + 'tof_integ')
	#Write the occupations_headers
		for i in range(len(sg.occ_header_array)):
			if i == len(sg.occ_header_array) - 1:
				simulation_data.write('%s\n' %(sg.occ_header_array[i]))
				sg.snapshot_output_headers.append(sg.occ_header_array[i])
			else:
				simulation_data.write('%s,' %(sg.occ_header_array[i]))
				sg.snapshot_output_headers.append(sg.occ_header_array[i])
		if parameters_of_interest_sp != 'None':
			simulation_data.write('%s,' %(sg.simulation_name))
			simulation_data.write('%s,' %(sg.steps_so_far))
			simulation_data.write('%s,' %(sg.atoms.kmc_time))
			simulation_data.write('%s,' %(0))
			for i in range(len(parameters_of_interest_sp)):
				parameter = eval('sg.model.parameters.' + parameters_of_interest_sp[i] + '[' + str("'value'") + ']')
				simulation_data.write('%s,' %(parameter))
		else:
	#If there are no parameters of interest requested
			simulation_data.write('%s,' %(sg.simulation_name))
			simulation_data.write('%s,' %(sg.steps_so_far))
			simulation_data.write('%s,' %(sg.atoms.kmc_time))
			simulation_data.write('%s,' %(0))
	#Write the TOF_headers
		for i in range(len(sg.TOF_header_array)):
			simulation_data.write('%s,' %(sg.atoms.tof_data[i]))
		for i in range(len(sg.TOF_header_array)):
			simulation_data.write('%s,' %(sg.atoms.tof_integ[i]))
	#Write the occupations_headers
		for species in range(len(species_tags)): #array indexing. The occupations array does not have the same structure as occ_header_array.
			for site in range(len(site_names)): #array indexing.
				if species == len(species_tags) - 1 and site == len(site_names) - 1:
					simulation_data.write('%s\n' %(sg.atoms.occupation[species][site]))
				else:
					simulation_data.write('%s,' %(sg.atoms.occupation[species][site]))
	#Check to see if the parameters file is wanted
		if print_all_parameters == 'True':
			parameters_file_name = sg.simulation_name + '_initial_parameters.txt' 
			simulation_parameters = open(parameters_file_name, 'w')
	#Use the parameters dictionary in KMC_settings.py to write the initial values and keys
			for index, key in enumerate(parameters):
				simulation_parameters.write('%s = %s\n' %(key,parameters[key]['value']))
		else:
			pass
	else:
#If write_output =='False'
		pass
	return

#This function will perform a KMC_snapshot and writes the output to the .csv 
#file created in the function create_headers.
def do_snapshots_time(tps, n_snapshots):
	parameters_of_interest_sp=sg.parameters_of_interest
#sg.last_snapshot_outputs will be used to write all info (simulation name, parameters of
#interest (user defined), atoms.tof_data, atoms.tof_integ, atoms.occupation) to
# a list and can be used for indexing based on column number.
	sg.last_snapshot_outputs = []
	data_file_name = sg.simulation_name + str('_TOFs_and_Coverages.csv')	
	simulation_data = open(data_file_name, 'a')		
	#This loop will do "steps" iterations and will run a snapshot at each step.
	for step in range(1,n_snapshots+1):
		if step <= n_snapshots:
			sg.sp_steps_initial = sg.steps_so_far
			sg.model.do_steps_time(tps)
			sg.steps_so_far = sg.atoms.kmc_step
			sg.sp_steps = sg.steps_so_far - sg.sp_steps_initial
			sg.snapshots_so_far += 1
			sg.atoms = sg.model.get_atoms(geometry=False)
#Check to see that the output files are requested
		if sg.write_output == 'True':
#Check which parameters to write to the .csv file
			if parameters_of_interest_sp != 'None':
				simulation_data.write('%s,' %(sg.simulation_name))
				simulation_data.write('%s,' %(sg.steps_so_far))
				simulation_data.write('%s,' %(sg.atoms.kmc_time))
				simulation_data.write('%s,' %(tps))
				for i in range(len(parameters_of_interest_sp)):
					parameter = eval('sg.model.parameters.' + parameters_of_interest_sp[i] + '[' + str("'value'") + ']')
					simulation_data.write('%s,' %(parameter))
			else:
#If no parameters of interest are requested
				simulation_data.write('%s,' %(sg.simulation_name))
				simulation_data.write('%s,' %(sg.steps_so_far))
				simulation_data.write('%s,' %(sg.atoms.kmc_time))
				simulation_data.write('%s,' %(tps))
		#Write the KMC data associated with each of the TOF_headers
			for i in range(len(sg.TOF_header_array)):
				simulation_data.write('%s,' %(sg.atoms.tof_data[i]))
			for i in range(len(sg.TOF_header_array)):
				simulation_data.write('%s,' %(sg.atoms.tof_integ[i]))
		#Write the KMC data associated with each of the occupations_headers
			for species in range(len(species_tags)): #array indexing. The occupations array does not have the same structure as occ_header_array.
				for site in range(len(site_names)): #array indexing.
					if species == len(species_tags) - 1 and site == len(site_names) - 1:
						simulation_data.write('%s\n' %(sg.atoms.occupation[species][site]))
					else:
						simulation_data.write('%s,' %(sg.atoms.occupation[species][site]))
#write to sg.last_snapshot_outputs which will be used to hold all info (simulation name,
#parameters of interest (user defined), atoms.tof_data, atoms.tof_integ, 
#atoms.occupation) to a list and can be used for indexing based on column 

#number. This is rewritten for each snapshot.
	if parameters_of_interest_sp != 'None':
		sg.last_snapshot_outputs.append(sg.simulation_name)
		sg.last_snapshot_outputs.append(sg.steps_so_far)
		sg.last_snapshot_outputs.append(sg.atoms.kmc_time)
		sg.last_snapshot_outputs.append(tps)				
		for i in range(len(parameters_of_interest_sp)):
			parameter = eval('sg.model.parameters.' + parameters_of_interest_sp[i] + '[' + str("'value'") + ']')
			sg.last_snapshot_outputs.append(parameter)
	else:
		sg.last_snapshot_outputs.append(sg.simulation_name)
		sg.last_snapshot_outputs.append(sg.steps_so_far)
		sg.last_snapshot_outputs.append(sg.atoms.kmc_time)
		sg.last_snapshot_outputs.append(tps)
#Create the arrays for the atoms.tof_data/integ and atoms.occupation and update
#sg global variables associated with each of the data lists.  temp_tof_data_list
#and temp_OCC_data_list are lists written to the global variables TOF_data_list 
#and OCC_data_list.  If you want to access an array form of these, simply access 
#the atoms objects for tof_data or occupations
	temp_TOF_data_list = []
	temp_TOF_integ_list = []
	for i in range(len(sg.TOF_header_array)):
		temp_TOF_data_list.append(sg.atoms.tof_data[i])
		temp_TOF_integ_list.append(sg.atoms.tof_integ[i])
		sg.last_snapshot_outputs.append(sg.atoms.tof_data[i])
	for i in range(len(sg.TOF_header_array)):
		sg.last_snapshot_outputs.append(sg.atoms.tof_integ[i])
	temp_OCC_data_list = []
	for species in range(len(species_tags)): #array indexing. The occupations array does not have the same structure as occ_header_array.
		for site in range(len(site_names)): #array indexing.
			temp_OCC_data_list.append(sg.atoms.occupation[species][site])
			sg.last_snapshot_outputs.append(sg.atoms.occupation[species][site])
#update the global lists
	sg.TOF_data_list = temp_TOF_data_list
	sg.TOF_integ_list = temp_TOF_integ_list
	sg.occ_data_list = temp_OCC_data_list
	return

#This function will perform a KMC_snapshot and writes the output to the .csv 
#file created in the function create_headers.
def do_snapshots(sps, n_snapshots):
	parameters_of_interest_sp=sg.parameters_of_interest
#sg.last_snapshot_outputs will be used to write all info (simulation name, parameters of
#interest (user defined), atoms.tof_data, atoms.tof_integ, atoms.occupation) to
# a list and can be used for indexing based on column number.
	sg.last_snapshot_outputs = []
	data_file_name = sg.simulation_name + str('_TOFs_and_Coverages.csv')	
	simulation_data = open(data_file_name, 'a')		
	#This loop will do "steps" iterations and will run a snapshot at each step.
	for step in range(1,n_snapshots+1):
		if step <= n_snapshots:
			sg.sp_steps_initial = sg.steps_so_far
			sg.model.do_steps(sps)
			sg.steps_so_far += sps
			sg.sp_steps = sg.steps_so_far - sg.sp_steps_initial 
			sg.snapshots_so_far += 1
			sg.atoms = sg.model.get_atoms(geometry=False)
#Check to see that the output files are requested
		if sg.write_output == 'True':
#Check which parameters to write to the .csv file
			if parameters_of_interest_sp != 'None':
				simulation_data.write('%s,' %(sg.simulation_name))
				simulation_data.write('%s,' %(sg.steps_so_far))
				simulation_data.write('%s,' %(sg.atoms.kmc_time))
				simulation_data.write('%s,' %(sps))
				for i in range(len(parameters_of_interest_sp)):
					parameter = eval('sg.model.parameters.' + parameters_of_interest_sp[i] + '[' + str("'value'") + ']')
					simulation_data.write('%s,' %(parameter))
			else:
#If no parameters of interest are requested
				simulation_data.write('%s,' %(sg.simulation_name))
				simulation_data.write('%s,' %(sg.steps_so_far))
				simulation_data.write('%s,' %(sg.atoms.kmc_time))
				simulation_data.write('%s,' %(sps))
		#Write the KMC data associated with each of the TOF_headers
			for i in range(len(sg.TOF_header_array)):
				simulation_data.write('%s,' %(sg.atoms.tof_data[i]))
			for i in range(len(sg.TOF_header_array)):
				simulation_data.write('%s,' %(sg.atoms.tof_integ[i]))
		#Write the KMC data associated with each of the occupations_headers
			for species in range(len(species_tags)): #array indexing. The occupations array does not have the same structure as occ_header_array.
				for site in range(len(site_names)): #array indexing.
					if species == len(species_tags) - 1 and site == len(site_names) - 1:
						simulation_data.write('%s\n' %(sg.atoms.occupation[species][site]))
					else:
						simulation_data.write('%s,' %(sg.atoms.occupation[species][site]))
#write to sg.last_snapshot_outputs which will be used to hold all info (simulation name,
#parameters of interest (user defined), atoms.tof_data, atoms.tof_integ, 
#atoms.occupation) to a list and can be used for indexing based on column 
#number. This is rewritten for each snapshot.
	if parameters_of_interest_sp != 'None':
		sg.last_snapshot_outputs.append(sg.simulation_name)
		sg.last_snapshot_outputs.append(sg.steps_so_far)
		sg.last_snapshot_outputs.append(sg.atoms.kmc_time)
		sg.last_snapshot_outputs.append(sps)				
		for i in range(len(parameters_of_interest_sp)):
			parameter = eval('sg.model.parameters.' + parameters_of_interest_sp[i] + '[' + str("'value'") + ']')
			sg.last_snapshot_outputs.append(parameter)
	else:
		sg.last_snapshot_outputs.append(sg.simulation_name)
		sg.last_snapshot_outputs.append(sg.steps_so_far)
		sg.last_snapshot_outputs.append(sg.atoms.kmc_time)
		sg.last_snapshot_outputs.append(sps)
#Create the arrays for the atoms.tof_data/integ and atoms.occupation and update
#sg global variables associated with each of the data lists.  temp_tof_data_list
#and temp_OCC_data_list are lists written to the global variables TOF_data_list 
#and OCC_data_list.  If you want to access an array form of these, simply access 
#the atoms objects for tof_data or occupations
	temp_TOF_data_list = []
	temp_TOF_integ_list = []
	for i in range(len(sg.TOF_header_array)):
		temp_TOF_data_list.append(sg.atoms.tof_data[i])
		temp_TOF_integ_list.append(sg.atoms.tof_integ[i])
		sg.last_snapshot_outputs.append(sg.atoms.tof_data[i])
	for i in range(len(sg.TOF_header_array)):
		sg.last_snapshot_outputs.append(sg.atoms.tof_integ[i])
	temp_OCC_data_list = []
	for species in range(len(species_tags)): #array indexing. The occupations array does not have the same structure as occ_header_array.
		for site in range(len(site_names)): #array indexing.
			temp_OCC_data_list.append(sg.atoms.occupation[species][site])
			sg.last_snapshot_outputs.append(sg.atoms.occupation[species][site])
#update the global lists
	sg.TOF_data_list = temp_TOF_data_list
	sg.TOF_integ_list = temp_TOF_integ_list
	sg.occ_data_list = temp_OCC_data_list
	return

#This function will optionally dump the configuration and create the log file 
#for a simulation run.  The simulation run time is calculated in this function based on the start time from create_headers, the log file is written to a file called simulation_name_log.txt
#and if requested, all final parameters will be written to a file called 'final_parameters.txt'
def create_log(dump_configuration='True', print_all_parameters='True'):
	parameters_of_interest_sp=sg.parameters_of_interest
	if sg.write_output == 'True':
		if dump_configuration == 'True':
			sg.model.dump_config(sg.simulation_name + '_final_config')
		if print_all_parameters == 'True':
			parameters_file_name = '%s_final_parameters.txt' %(sg.simulation_name)
			simulation_parameters = open(parameters_file_name, 'w')
			for index, key in enumerate(parameters):
				simulation_parameters.write('%s = %s\n' %(key,parameters[key]['value']))
		stop = timeit.default_timer() #stop the timer right before last exports.
		run_time = stop - sg.start
		simulation_log_name = '%s_log.txt' %(sg.simulation_name)
		simulation_log = open(simulation_log_name, 'w')
		simulation_log.write('total number of steps = %s\n'%(sg.steps_so_far))
		simulation_log.write('total number of snapshots = %s\n'%(sg.snapshots_so_far))
		simulation_log.write('total simulation time = %s\n' %(sg.atoms.kmc_time))
		simulation_log.write('simulation run time (wall clock time)= %s\n' %(run_time))
		if parameters_of_interest_sp != 'None':
			for i in range(len(parameters_of_interest_sp)):
				parameter = eval('sg.model.parameters.' + parameters_of_interest_sp[i] + '[' + str("'value'") + ']')
				simulation_log.write('%s = %s\n' %(parameters_of_interest_sp[i], parameter))		
	else:
		pass	
			























