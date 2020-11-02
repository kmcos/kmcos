# Throttling test case 4: Only fast processes with some fast processes being
# below the floor.

try:
    import kmos.throttling_globals as tg
except:
    import throttling_globals as tg

# Specify some basic model information
tg.Nsites=400

# Increasing tg.FFP_floor to 1E17 will result in the benchmark FFP bottoming out
# at tg.FFP_floor instead of using the maximum down-step factor.
tg.FFP_floor = 1.0E16

# Specify whether to check against hand-calculated results
results_check = True

# Ranges to trigger throttling levels, full range option
EF_range_full = []
EF_range_full_level = []

# Ranges to trigger throttling levels, split range option
EF_range_split = [[1E06, 1E13],
                  [1E05, 1E13],
                  [1E03, 1E13],
                  [1E00, 1E13]]
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
