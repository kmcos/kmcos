#!/usr/bin/env python

import kmcos.snapshots_globals as sg
import kmcos.snapshots as snapshots
import kmcos.throttling_globals as tg
import kmcos.throttling as throttling
import export_import_library as eil
import numpy as np
import sys

# Random seed
random_seed = -731543673

# Input/Output options
save_simulation_state = True
load_simulation_state = False
sg.write_output = True
tg.print_throttling_info = True
tg.regularization = False

# Temperature
T_initial = 170 # K
T_ramp    = 2   #Temperature ramp, K/s
T_final   = 800 #Final temperature, K
cutoff_time = float(T_final - T_initial) / T_ramp

# Maximum number of snapshots
total_snapshots = 100000

# Number of snapshots to execute before updating parameters
Nsnapshots = tg.loop_base

# Time per snapshot constraint
tps = None # Use fixed-step algorithm only

# Steps per snapshot
sps = None

# Initial lattice
initial_config_name = 'MeOH-TPD_initial_lattice'

# Some output/restart stuff
lattice_export_dt = 1./T_ramp   #Time between saved lattice configurations
last_dump_T = 170  #Temperature at which last lattice conguration was saved

# File names for loading/saving parameters
tg_load_file = 'MeOH-CeO2_throttling_parameters.txt'
tg_save_file = 'MeOH-CeO2_throttling_parameters.txt'
sg_load_file = 'MeOH-CeO2_snapshots_parameters.txt'
sg_save_file = 'MeOH-CeO2_snapshots_parameters.txt'


#decrease methanol desorption energy for high coverage.
MethanolDesEaDecrease = 6000.0
#//print sg.model.parameters.EaF106p5
#//print sg.model.parameters.EaF106p5['value']
sg.model.settings.parameters['EaF106p5']['value'] = float(sg.model.settings.parameters['EaF106p5']['value']) - MethanolDesEaDecrease
#//print sg.model.parameters.EaF106p5['value']
sg.model.settings.parameters['EaF106p6']['value'] = float(sg.model.settings.parameters['EaF106p6']['value']) - MethanolDesEaDecrease
sg.model.settings.parameters['EaF106p7']['value'] = float(sg.model.settings.parameters['EaF106p7']['value']) - MethanolDesEaDecrease

#Manual throttling to remove some one-way square kinetics identified.
#Using Jonathan's trick to speed it up by only updating all parameters at end.
sg.model.settings.parameters['EaF101p1']['value']= 100000
sg.model.settings.parameters['EaR101p1']['value']= 100000
sg.model.settings.parameters['EaF101p5']['value']= 100000
sg.model.settings.parameters['EaR101p5']['value']= 100000
sg.model.settings.parameters['EaF101p6']['value']= 100000
sg.model.settings.parameters['EaR101p6']['value']= 100000
#sg.model.settings.parameters['EaR104p7']['value']= 100000
sg.model.settings.parameters['EaF108p2']['value']= 100000
sg.model.settings.parameters['EaR108p2']['value']= 100000
sg.model.settings.parameters['EaF108p4']['value']= 200000
sg.model.settings.parameters['EaR108p4']['value']= 200000
sg.model.settings.parameters['EaF117p2']['value']= 200000
sg.model.settings.parameters['EaR117p2']['value']= 200000
sg.model.settings.parameters['EaR16p8']['value']= 300000
#sg.model.settings.parameters['EaF102p8']['value']= sg.model.settings.parameters['EaF112p7']['value']
#sg.model.settings.parameters['EaR102p8']['value']= float(sg.model.settings.parameters['EaF102p8']['value']) + 3000.00
sg.model.settings.parameters['EaF15p1']['value']= 25000
sg.model.settings.parameters['AF112p3']['value']= 0
sg.model.settings.parameters['AR112p3']['value']= 0

#I am using this below line to set all of the parameter attributes instead of using setattr.
sg.model.parameters.AF120p0 = 1000 # O excitation metronome

##//print sg.model.parameters.EaF106p5
##//raise(SystemExit)


################################################################################
#The following inputs are throttling specific inputs
################################################################################

#Processes with characteristic times scales (seconds) lower than this remain unthrottled.
#This should be equal to desired TPD resolution, Ashi says 1-50 K
#3s equals 9K
tg.max_time = 3000

#cutoff time is the simulation time (seconds) after which the simulation gets cut off
# Ashi recommends 1000s, with a heating rate of 3K/s experimental time is 133.4 s
tg.cutoff_time = cutoff_time

# Use guidelines for calculating FFP_floor, sps, and FFP_step_down
tg.use_guideline_FFP_step_down = True  # FFP step down
tg.use_guideline_FFP_floor = True  # Floor level
tg.use_guideline_sps = True    # SPS size


# Characteristic event frequency (rate) controlling the slow processes
tg.characteristic_EF = sg.model.parameters.AF120p0['value']/400./100.

# Number of characteristic events that should happen in each snapshot
tg.n_characteristic_events_target = 0.01

#Change the EF_range settings
#EF_range_flag controls whether we use one EF_range for all processes (full) or a separate
#value for the fast process' EF_range and the slow process' EF range (split)
#this separation is necessary for TPD
tg.EF_range_flag = 'split'

#Ashi says this could be set as low as 1e3
tg.EF_range_fast = 1e3  #Originally 1e6

#This large value should prevent the slow processes from being throttled
tg.EF_range_slow = 1e20

# Number of unit cells in each x, y direction
sim_size  = 20  # this is the size of the initial lattice provided by Jonathan

# End of initialization parameters

# Start TPD
sys.stdout.write("Starting TPD ramp\n")

# Export/import module objects for saving/loading data
tg_module = eil.module_export_import(tg_save_file, tg_load_file, tg)
sg_module = eil.module_export_import(sg_save_file, sg_load_file, sg)

# Load parameters
kmc_time_tpdinit = 0.0
if load_simulation_state:

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

    # Update the cutoff time
    tg.cutoff_time = cutoff_time

    # The following assignment (and similar assignments elsewhere) is *magical*.
    # It invokes a hidden __setattr__ method of the Model_Parameters class that
    # calls the set_rate_constants() function to update the values of the rate
    # constants in the Fortran base module. Any other syntax of assignment will
    # require an explicit call to set_rate_constants(). *Failure to update the
    # rate constants in the Fortran module will result in wrong results!*
    T = T_initial + T_ramp * (kmc_time - kmc_time_tpdinit)
    sg.model.parameters.T = T
    dt = (T - last_dump_T) / T_ramp

    sys.stdout.write("Restarting from old simulation. Current temperature is " +
        str(T) + " K. Current time is " + str(kmc_time) + " s.\n")

else:

    #Load lattice
    sg.model.load_config(initial_config_name)

    # Initialize output files
    snapshots.seed_PRNG(restart=False, state=random_seed)

    #Initialize temperature and time
    sg.model.parameters.T = T_initial
    T = T_initial
    kmc_time = 0.0
    dt = 0.0
    if sg.write_output:
        snapshots.create_headers()

# Execute snapshots
# Algorithm step 4
first_snapshot = tg.current_snapshot * 1
if first_snapshot >= total_snapshots:
    print('No more snapshots to run. Please increase total_snapshots.')
for i in range(first_snapshot, total_snapshots, Nsnapshots):
    throttling.do_throttled_snapshots(Nsnapshots, sps, tps, eic_module_objects=[tg_module, sg_module])

    # Update parameters
    kmc_time_old = kmc_time
    kmc_time = sg.model.base.get_kmc_time()
    T = T_initial + T_ramp * (kmc_time - kmc_time_tpdinit)
    sys.stdout.write("Updated parameters\n")
    sys.stdout.write("T = " + str(T) + " K, time = " + str(kmc_time) + " s.\n")

    #   Update the temperature and rate constants
    sg.model.parameters.T = T

    #   Export the lattice state if enough time has elapsed
    dt += (kmc_time - kmc_time_old)
    if (dt > lattice_export_dt):
        dt = 0.0
        sg.model.dump_config(sg.simulation_name + '_lattice_config_' + str(T))

    if tg.cutoff_time_exceeded:
        break

# Write summary/diagnostic data
if sg.write_output:
    snapshots.create_log()

sg.model.deallocate()
sys.stdout.write("Simulation complete.\n")
