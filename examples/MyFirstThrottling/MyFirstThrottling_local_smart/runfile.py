#THIS IS A FAIRLY BARE-BONES EXAMPLE RUNFILE FOR THE THROTTLING MODULE, INCLUDING HOW TO LOAD A PREVIOUS SIMULATION'S DATA.

try:
    import kmos.snapshots_globals as sg
    import kmos.snapshots as snapshots
    import kmos.throttling_globals as tg
    import kmos.throttling as throttling
    import kmos.runfile_init as runfile_init
except:
    import snapshots_globals as sg
    import snapshots
    import throttling_globals as tg
    import throttling
    import runfile_init #This is optional.
import export_import_library as eil #optional, but useful.

# Initialize variables
# File names for loading/saving parameters (optional, but useful).
tg_load_file = 'test_reaction_throttling_parameters.txt'
tg_save_file = 'test_reaction_throttling_parameters.txt'
sg_load_file = 'test_reaction_snapshots_parameters.txt'
sg_save_file = 'test_reaction_snapshots_parameters.txt'
tg_eil_object = eil.module_export_import(tg_save_file, tg_load_file, tg)
sg_eil_object = eil.module_export_import(sg_save_file, sg_load_file, sg)
eic_module_objects = [tg_eil_object, sg_eil_object]

sg.model.parameters.T = 600

#If you want to set the random seed:
random_seed = -731543675
runfile_init.set_PRNG_state(load_saved_parameters_on=True, random_seed=random_seed)

# The number of snapshots
Nsnapshots = 100 # Number of snapshots to run

# The total steps per snapshot (sps) and time per snapshot (tps). Values of None
# mean to use tg.throttling_sps and tg.throttling_tps instead.
sps = None
tps = None
tg.FFP_roof = 1000

###BELOW WOULD BE A TYPICAL SINGLE USAGE OF THE FUNCTION AND OUTPUT OF DATA####

# Write output file headers if output on and we have not loaded saved data (this is before running simulation)
snapshots.create_headers()

# Execute throttled snapshots
throttling.do_throttled_snapshots(Nsnapshots, sps=sps, tps=tps, eic_module_objects=eic_module_objects) #by default, settings will be exported with the eic_module after each set/batch of throttled snapshots, as long as eic_module_objects is provided.
#one can then do other analysis and call do_throttled_snapshots again.

# Write summary/diagnostic data (this is after running simulation)
snapshots.create_log()
