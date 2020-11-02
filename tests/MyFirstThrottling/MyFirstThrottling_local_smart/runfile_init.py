import export_import_library as eil
try:
    import kmos.snapshots_globals as sg
    import kmos.snapshots as snapshots
    import kmos.throttling_globals as tg
    import kmos.throttling as throttling
except:
    import snapshots_globals as sg
    import snapshots
    import throttling_globals as tg
    import throttling
# This function will reset any values that will be clobbered by loading from
# disk. It should manipulate the global variables directly. If nothing should
# be done, the body of this function should be replaced with 'pass'.
def set_runfile_params(load_saved_parameters_on):

    # The ending simulation time
    tg.cutoff_time = 100.0 # New cutoff time for simulation

    # Temperature
    sg.model.parameters.T = 600

    # PRNG state
    random_seed = -731543675
    set_PRNG_state(load_saved_parameters_on, random_seed)

# This is a function to load all of the saved module data.
def load_saved_data():

    # File names for loading/saving parameters
    tg_load_file = 'test_reaction_throttling_parameters.txt'
    tg_save_file = 'test_reaction_throttling_parameters.txt'
    sg_load_file = 'test_reaction_snapshots_parameters.txt'
    sg_save_file = 'test_reaction_snapshots_parameters.txt'

    # Export/import module objects for saving/loading data
    tg_eil_object = eil.module_export_import(tg_save_file, tg_load_file, tg)
    sg_eil_object = eil.module_export_import(sg_save_file, sg_load_file, sg)

    # Load modules
    sg_eil_object.load_params()
    tg_eil_object.load_params()

    # Reset number of steps and time
    sg.model.base.set_kmc_time(sg.kmc_time)
    sg.model.base.set_kmc_step(sg.steps_so_far)
    sg.atoms.kmc_step = sg.steps_so_far

    # Load the lattice
    sg.model._set_configuration(np.array(sg.config))
    sg.model._adjust_database()

    # Update the snapshot number
    tg.current_snapshot += 1

# This function initializes all the global variables for the runfile other than
# those required for the basic usage of do_throttled_snapshots.
def init(load_saved_parameters_on=False):

    # Load any saved data
    if load_saved_parameters_on:
        load_saved_data()

    # Reset any global variables that got clobbered
    set_runfile_params(load_saved_data_on)

def set_PRNG_state(load_saved_parameters_on, random_seed=None):

    if load_saved_parameters_on:
        snapshots.seed_PRNG(restart=True, state=sg.PRNG_state)
    else:
        snapshots.seed_PRNG(restart=False, state=random_seed)
