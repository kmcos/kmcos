# Throttling test case 7: Same as case 4, but with aggregate throttling factors.

try:
    import kmcos.throttling_globals as tg
except:
    import throttling_globals as tg

# Specify some basic model information
tg.Nsites=400

tg.FFP_floor = 1.0E16

# Specify whether to check against hand-calculated results
results_check = True

# Ranges to trigger throttling levels, full range option
EF_range_full = []
EF_range_full_level = []

# Ranges to trigger throttling levels, split range option
EF_range_split = [[1E07, 1E13],
                  [1E06, 1E13],
                  [1E03, 1E13],
                  [1E01, 1E13]]
EF_range_split_level = []
split_level_aggregate_factors = []

# Process names
tg.proc_names = [
                        "F1p0",
                        "R1p0",
                        "F2p0",
                        "R2p0",
                        "F3p0",
                        "R3p0",
                        "F4p0",
                        "R4p0"
                ]

# Reaction rates
tg.oEF_TOF_list = [
                      1.00E+24,
                      1.00E+24,
                      1.00E+20,
                      1.00E+20,
                      1.00E+18,
                      1.00E+18,
                      1.00E+15,
                      1.00E+15
                  ]

# The unthrottled rate is the throttled rate divided by the aggregate throttling
# factor. Therefore, aggregate throttling factors less than (greater than) 1
# result in unthrottled rates that are faster (slower) than the corresponding
# throttled rates. Any aggregate throttling factor not specified is assumed to
# be 1 (no change). These aggregate throttling factors are chosen to throttle
# down two of the reactions, resulting in a system of 3 FFPs and 1 FQP.
tg.aggregate_throttling_factors_dict_old = {'F3p0': 4E0,
                                            'R3p0': 4E0,
                                            'F4p0': 2E0,
                                            'R4p0': 2E0}
