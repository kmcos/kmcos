#!/usr/bin/env python

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
import export_import_library as eil
from copy import deepcopy

# Easy way to loop over all test cases
case_numbers = range(11, 21)
#case_numbers = [18]

for case_number in case_numbers:

    print(case_number)

    # File names for loading/saving parameters
    tg_load_file = 'test_throttle_case_' + str(case_number) + '_params.txt'
    tg_save_file = 'test_throttle_case_' + str(case_number) + '_params_out.txt'

    # Module object for saving/loading
    tg_module = eil.module_export_import(tg_save_file, tg_load_file, tg)

    # Load the module
    tg_module.load_params()

    # Make sure to update the new ATF dictionary so we don't accidentally get
    # one with the wrong size or process entries. (The ITF one is automatically
    # created.)
    tg.aggregate_throttling_factors_dict = deepcopy(
        tg.aggregate_throttling_factors_dict_old)

    # Calculate throttling factors
    throttling.calculate_throttling_factors(unthrottle_slow_processes=False)

    # Save the module
    tg_module.save_params()
