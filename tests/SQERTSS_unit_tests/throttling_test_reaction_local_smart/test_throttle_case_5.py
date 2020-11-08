# Throttling test case 5: Only slow processes.

try:
    import kmcos.throttling_globals as tg
except:
    import throttling_globals as tg

# Specify some basic model information
tg.Nsites=400
tg.FFP_floor = 1.0E17

# Specify whether to check against hand-calculated results
results_check = True

# Ranges to trigger throttling levels, full range option
EF_range_full = []
EF_range_full_level = []

# Ranges to trigger throttling levels, split range option
EF_range_split = [[1E10, 1E10],
                  [1E10, 1E08],
                  [1E10, 1E06],
                  [1E10, 1E02]]
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
                      1.00E+22,
                      1.00E+20,
                      1.00E+20,
                      1.00E+18,
                      1.00E+18,
                      1.00E+15,
                      1.00E+15
                  ]
