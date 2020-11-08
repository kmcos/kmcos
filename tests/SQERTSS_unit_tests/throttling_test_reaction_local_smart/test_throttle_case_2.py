# Throttling test case 2: Same as case 1, but we also have a value of
# tg.FFP_floor set to prevent some fast processes from being throttled.

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
EF_range_split = [[1E10, 1E13],
                  [1E08, 1E13],
                  [1E05, 1E13],
                  [1E03, 1E13],
                  [1E08, 1E11],
                  [1E05, 1E11],
                  [1E03, 1E11],
                  [1E08, 1E08],
                  [1E05, 1E08],
                  [1E03, 1E08]]
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

# Reaction rates
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
