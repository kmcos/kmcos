#Snapshots Module version 6.6
# The following functions can be utilized to run a kmcos simulation with a user
# defined snapshot size. The associated KMC data (simulation name, parameters
# of interest (user defined), atoms.tof_data, atoms.tof_integ, atoms.occupation)
# will be written to .csv files. In addition, the configuration and a
# simulation log will be written when the simulation is complete.
import time
try:
    import kmcos.snapshots_globals as sg
except:
    import snapshots_globals as sg

# This function creates the output file for the TOF data, occupations data and
# parameters file. The file that is created to hold the data is called
# simulation_name_TOFs_and_Coverages.csv where simulation_name is user defined
# in snapshots_globals.py. The parameters of interest will be printed to the
# same file, if any exist. If desired, parameter initial values will be written
# to a separate file called initial_parameters.txt. By default, the output file
# of the .csv file is created and initial_parameters.txt written, but these
# output files can be turned off by the option of True or False for
# write_output.
def create_headers(print_all_parameters=True):

    # Keeping track of the start time for runtime info
    sg.start = time.time()

    # Check the parameters of interest and write them if requested
    data_file_name = sg.simulation_name + str('_TOFs_and_Coverages.csv')
    with open(data_file_name, 'w') as simulation_data:
        simulation_data.write('Simulation_name,')
        simulation_data.write('Snapshot,')
        simulation_data.write('Step,')
        simulation_data.write('Time_(s),')
        simulation_data.write('sps,')
        simulation_data.write('tps,')
        sg.snapshot_output_headers.append('Simulation_name')
        sg.snapshot_output_headers.append('Step')
        sg.snapshot_output_headers.append('Time_(s)')
        sg.snapshot_output_headers.append('sps')
        sg.snapshot_output_headers.append('tps')
        # None and [] will lead to a 'False' evaluation, but a non-empty list
        # evaluates as 'True'
        if sg.parameters_of_interest:
            for i in range(len(sg.parameters_of_interest)):
                simulation_data.write('%s,' %(sg.parameters_of_interest[i]))
                sg.snapshot_output_headers.append(sg.parameters_of_interest[i])

        # Write the TOF_headers
        for i in range(len(sg.TOF_header_array)):
            simulation_data.write('%s_tof_data,' %(sg.TOF_header_array[i]))
            sg.snapshot_output_headers.append(sg.TOF_header_array[i] + '_tof_data')
        for i in range(len(sg.TOF_header_array)):
            simulation_data.write('%s_tof_integ,' %(sg.TOF_header_array[i]))
            sg.snapshot_output_headers.append(sg.TOF_header_array[i] + '_tof_integ')

        # Write the occupations_headers
        for i in range(len(sg.occ_header_array)):
            simulation_data.write('%s,' %(sg.occ_header_array[i]))
            sg.snapshot_output_headers.append(sg.occ_header_array[i])
        simulation_data.write('\n')

        # Write the initial TOF and coverage values
        simulation_data.write('%s,' %(sg.simulation_name))
        simulation_data.write('%s,' %(sg.snapshots_so_far))
        simulation_data.write('%s,' %(sg.steps_so_far))
        simulation_data.write('%s,' %(sg.atoms.kmc_time))
        simulation_data.write('%s,' %(0))
        simulation_data.write('%s,' %(0))
        # None and [] will lead to a 'False' evaluation, but a non-empty list
        # evaluates as 'True'
        if sg.parameters_of_interest:
            for i in range(len(sg.parameters_of_interest)):
                parameter = getattr(sg.model.parameters,
                    sg.parameters_of_interest[i])['value']
                simulation_data.write('%s,' %(parameter))

        # Write the TOF_headers
        for i in range(len(sg.TOF_header_array)):
            simulation_data.write('%s,' %(sg.atoms.tof_data[i]))
        for i in range(len(sg.TOF_header_array)):
            simulation_data.write('%s,' %(sg.atoms.tof_integ[i]))

        # Write the initial occupation values. These are in a 2-D numpy array.
        for species in range(len(sg.model.settings.species_tags)):
            for site in range(len(sg.model.settings.site_names)):
                simulation_data.write('%s,' %(sg.atoms.occupation[species][site]))
        simulation_data.write('\n')

    # Check to see if the parameters file is wanted
    if print_all_parameters:
        parameters_file_name = sg.simulation_name + '_initial_parameters.txt'
        with open(parameters_file_name, 'w') as simulation_parameters:
            # Use the parameters dictionary in KMC_settings.py to write the
            # initial values and keys
            for index, key in enumerate(sg.model.settings.parameters):
                simulation_parameters.write('%s = %s\n'
                    %(key,sg.model.settings.parameters[key]['value']))

# This function will create a nested list with all of the snapshot data. Right
# now it is not currently used for anything, but it could be used as an
# in-memory history of the last snapshot.
def save_snapshot_output_as_list():
    sg.last_snapshot_outputs = []
    sg.last_snapshot_outputs.append(sg.simulation_name)
    sg.last_snapshot_outputs.append(sg.snapshots_so_far)
    sg.last_snapshot_outputs.append(sg.steps_so_far)
    sg.last_snapshot_outputs.append(sg.atoms.kmc_time)
    sg.last_snapshot_outputs.append(sg.sps_actual)
    sg.last_snapshot_outputs.append(sg.tps_actual)
    # None and [] will lead to a 'False' evaluation, but a non-empty list
    # evaluates as 'True'
    if sg.parameters_of_interest:
        for i in range(len(sg.parameters_of_interest)):
            parameter = getattr(sg.model.parameters,
                sg.parameters_of_interest[i])['value']
            sg.last_snapshot_outputs.append(parameter)

    # Add TOF and occupation data to the last_snapshots_outputs data structure.
    # TOF data is in 1-D numpy arrays, and occupation data is in a 2-D numpy
    # array. The occupation header array is a simple 1-D list.
    for i in range(len(sg.TOF_header_array)):
        sg.last_snapshot_outputs.append(sg.atoms.tof_data[i])
    for i in range(len(sg.TOF_header_array)):
        sg.last_snapshot_outputs.append(sg.atoms.tof_integ[i])
    for species in range(len(sg.model.settings.species_tags)):
        for site in range(len(sg.model.settings.site_names)):
            sg.last_snapshot_outputs.append(sg.atoms.occupation[species][site])

# This function will write the snapshot data to disk.
def write_snapshot_data():
    data_file_name = sg.simulation_name + str('_TOFs_and_Coverages.csv')
    with open(data_file_name, 'a') as simulation_data:

        simulation_data.write('%s,' %(sg.simulation_name))
        simulation_data.write('%s,' %(sg.snapshots_so_far))
        simulation_data.write('%s,' %(sg.steps_so_far))
        simulation_data.write('%s,' %(sg.atoms.kmc_time))
        simulation_data.write('%s,' %(sg.sps_actual))
        simulation_data.write('%s,' %(sg.tps_actual))
        # None and [] will lead to a 'False' evaluation, but a non-empty list
        # evaluates as 'True'
        if sg.parameters_of_interest:
            for i in range(len(sg.parameters_of_interest)):
                parameter = getattr(sg.model.parameters,
                    sg.parameters_of_interest[i])['value']
                simulation_data.write('%s,' %(parameter))

        # Write the KMC data associated with each of the TOF_headers
        for i in range(len(sg.TOF_header_array)):
            simulation_data.write('%s,' %(sg.atoms.tof_data[i]))
        for i in range(len(sg.TOF_header_array)):
            simulation_data.write('%s,' %(sg.atoms.tof_integ[i]))

        # Write the KMC data associated with each of the
        # occupations_headers. The occupation array is 2-D, unlike the
        # header array (actually a 1-D list).
        for species in range(len(sg.model.settings.species_tags)):
            for site in range(len(sg.model.settings.site_names)):
                simulation_data.write('%s,' %(sg.atoms.occupation[species][site]))
        simulation_data.write('\n')

# This function will perform a KMC_snapshot and writes the output to the .csv
# file created in the function create_headers.
def do_snapshots(n_snapshots, sps, tps=None):

    # sg.last_snapshot_outputs will be used to write all info (simulation name,
    # parameters of interest (user defined), atoms.tof_data, atoms.tof_integ,
    # atoms.occupation) to a list and can be used for indexing based on column
    # number.

    # This loop will do "snapshot" iterations and will run a snapshot each time.
    for snapshot in range(1, n_snapshots+1):
        if snapshot <= n_snapshots:
            sg.steps_before_snapshot = sg.steps_so_far
            if tps is None:
                sg.model.do_steps(sps)
            else:
                try:
                    # If TPS is specified, try to match it with the appropriate
                    # routine
                    sps_actual = sg.model.do_steps_time(tps, sps)
                except:
                    # Something went wrong, probably because we don't have this
                    # custom add-on to kmcos, so just fall back to the default
                    # routine.
                    print('WARNING: TPS specified but this version of kmcos does not support time-based snapshots. Using fixed-step snapshots instead.')
                    sg.model.do_steps(sps)
            sg.atoms = sg.model.get_atoms(geometry=False)
            sg.steps_so_far = sg.atoms.kmc_step
            sg.sps_actual = sg.steps_so_far - sg.steps_before_snapshot
            sg.snapshots_so_far += 1
            sg.tps_actual = sg.atoms.kmc_time - sg.kmc_time
            sg.kmc_time = sg.atoms.kmc_time

        save_snapshot_output_as_list()

        # Check to see that the output files are requested
        if sg.write_output:
            if sg.snapshots_sampling == None:
                write_snapshot_data()
            elif sg.snapshots_so_far%sg.snapshots_sampling ==0: #This will only write output every sg.snapshots_sampling snapshots (e.g., every 10 snapshots for a value of 10).
                write_snapshot_data()
                

    # update the global lists
    sg.TOF_data_list = sg.atoms.tof_data.tolist()
    sg.TOF_integ_list = sg.atoms.tof_integ.tolist()
    sg.occ_data_list = sg.atoms.occupation.tolist()

    # Save the lattice configuration
    sg.config = sg.model._get_configuration().tolist()

    # Save the PRNG state
    try:
        sg.PRNG_state = sg.model.proclist.get_seed().tolist()
    except:
        sg.PRNG_state = None

# This function will optionally dump the configuration and create the log file
# for a simulation run. The simulation run time is calculated in this function
# based on the start time from create_headers, the log file is written to a file
# called simulation_name_log.txt and if requested, all final parameters will be
# written to a file called 'final_parameters.txt'
def create_log(dump_configuration=True, print_all_parameters=True):
    if dump_configuration:
        sg.model.dump_config(sg.simulation_name + '_final_config')
    if print_all_parameters:
        parameters_file_name = sg.simulation_name + '_final_parameters.txt'
        with open(parameters_file_name, 'w') as simulation_parameters:
            # Use the parameters dictionary in KMC_settings.py to write the
            # initial values and keys
            for index, key in enumerate(sg.model.settings.parameters):
                simulation_parameters.write('%s = %s\n'
                    %(key,sg.model.settings.parameters[key]['value']))
    stop = time.time() # stop the timer right before last exports.
    run_time = stop - sg.start
    simulation_log_name = '%s_log.txt' %(sg.simulation_name)
    with open(simulation_log_name, 'w') as simulation_log:
        simulation_log.write('total number of snapshots = %s\n'%(sg.snapshots_so_far))
        simulation_log.write('total number of steps = %s\n'%(sg.steps_so_far))
        simulation_log.write('total simulation time = %s\n' %(sg.atoms.kmc_time))
        simulation_log.write('simulation run time (wall clock time) = %s\n' %(run_time))
        # None and [] will lead to a 'False' evaluation, but a non-empty list
        # evaluates as 'True'
        if sg.parameters_of_interest:
            for i in range(len(sg.parameters_of_interest)):
                parameter = getattr(sg.model.parameters,
                    sg.parameters_of_interest[i])['value']
                simulation_log.write('%s = %s\n' %(sg.parameters_of_interest[i], parameter))

# This is a function to seed the random number generator with the requested
# state. It takes two arguments: whether the simulation is a restart or not
# and the actual PRNG state to use. In the event of a new simulation, the
# state is initialized with a single 64 bit integer; otherwise it is an array
# of 64 bit integers. For a restart, the number of integers needed is
# compiler-dependent, and there is no good way to check this a priori. It is
# incumbent upon the user to make sure that the same compiler is used for all
# segments of a multi-segment simulation.
def seed_PRNG(restart=False, state=None):

    if not restart:
        if state is None:
            print('New simulation with no random seed supplied -- using kmcos default.')
            return
        else:
            try:
                prng_state = sg.model.proclist.seed_gen(state)
                sg.model.proclist.put_seed(prng_state)
            except:
                print('PRNG seeding routines not available -- using kmcos default.')
                return

    else:
        if state is None:
            print('Restarted simulation but no PRNG state supplied -- using new default state.')
            return
        else:
            try:
                sg.model.proclist.put_seed(state)
            except:
                print('PRNG seeding routines not available -- using kmcos default.')
                return

#For snapshots module. Requires the module_state_export_import  module
def reload(sg_module_state):
    # Load module state
    sg_module_state.load_params()
    
    # Reset number of steps and time
    try:
        sg.model.base.set_kmc_step(sg.steps_so_far)
    except:
        print("Warning: sg.model.base.set_kmc_step(sg.steps_so_far) function does not exist. Proceeding without it. Sutton once wrote it. Savara may have it somewhere.")
        pass
    else:
        pass
    sg.model.base.set_kmc_time(sg.kmc_time)
    sg.atoms.kmc_step = sg.steps_so_far

    # Load the lattice
    import numpy as np
    sg.model._set_configuration(np.array(sg.config))
    sg.model._adjust_database()

    # Read the PRNG state, if available, and set it in the model if possible.
    seed_PRNG(restart=True, state=sg.PRNG_state)

    #Update the rate constants based on the temperature etc. 
    #This is necessary, or rate constants will be those of kmc_settings parameter settings.
    try:
        sg.kmcos.run.set_rate_constants() # <-- was getting a math domain error for some reason...
    except:
        print("Warning: kmcos.run.set_rate_constants() did not work correctly in the restart. \n \
               This is a known bug, but the reason is not yet looked into. \n \
               You may need to throw away your first restarted datapoint,  \n \
               and if it affects your system dynamics then this bug needs to be fixed.")