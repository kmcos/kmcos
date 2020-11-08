# Throttling test case 6: Same as case 2, but we have some aggregate throttling
# factors specified to test the unthrottling code.

try:
    import kmcos.throttling_globals as tg
except:
    import throttling_globals as tg

# Specify some basic model information
tg.Nsites=400
tg.FFP_floor = 1.0E19

# Specify whether to check against hand-calculated results
results_check = True

# Ranges to trigger throttling levels, full range option
EF_range_full = []
EF_range_full_level = []

# Ranges to trigger throttling levels, split range option
EF_range_split = [[1E14, 1E13],
                  [1E06, 1E13],
                  [1E04, 1E13],
                  [1E01, 1E13],
                  [1E14, 1E12],
                  [1E04, 1E12],
                  [1E01, 1E12],
                  [1E14, 1E10],
                  [1E02, 1E10],
                  [1E00, 1E10],
                  [1E14, 1E07]]
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
                        "R4p0",
                        "F5p0",
                        "R5p0",
                        "F6p0",
                        "R6p0",
                        "F7p0",
                        "R7p0"
                ]

# Throttled reaction rates
tg.oEF_TOF_list = [
                      1.00E+24,
                      1.00E+24,
                      1.00E+20,
                      1.00E+20,
                      1.00E+18,
                      1.00E+18,
                      1.00E+15,
                      1.00E+10,
                      1.00E+12,
                      1.00E+07,
                      1.00E+10,
                      1.00E+10,
                      1.00E+06,
                      1.00E+03
                  ]

# The unthrottled rate is the throttled rate divided by the aggregate throttling
# factor. Therefore, aggregate throttling factors less than (greater than) 1
# result in unthrottled rates that are faster (slower) than the corresponding
# throttled rates. Any aggregate throttling factor not specified is assumed to
# be 1 (no change). These aggregate throttling factors are chosen to throttle
# down one of the FFPs and throttle up a slow process that becomes the FRP.
tg.aggregate_throttling_factors_dict_old = {'F3p0': 4E0,
                                            'R3p0': 4E0,
                                            'F4p0': 1E-1,
                                            'R4p0': 1E-1}
