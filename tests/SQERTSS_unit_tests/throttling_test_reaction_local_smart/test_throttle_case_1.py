# Throttling test case 1: Both fast and slow processes for reactions where some
# processes have time scale separations that prevent throttling at the C1 level
# but are throttled at the C2 and C3 level. We provide a progression of
# throttling ranges for both the full and split range options. The intent is to
# loop over each series of throttling criteria printing the achieved throttling
# level and the aggregate throttling factors in order to verify the output.
# The progressions in this test case assume paired ranking. This test case
# assumes that there is no prior throttling.

try:
    import kmcos.throttling_globals as tg
except:
    import throttling_globals as tg

# Specify some basic model information
tg.Nsites=400

# Specify whether to check against hand-calculated results
results_check = True

# Ranges to trigger throttling levels, full range option
EF_range_full = [1E22, 1E20, 1E17, 1E15, 1E13, 5E12, 1E11]

# Hand-calculated expected progression of throttling levels
EF_range_full_level = [[0, 0],
                       [1, 0],
                       [2, 0],
                       [3, 0],
                       [3, 1],
                       [2, 2],
                       [3, 2]]

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

# Hand-calculated expected progression of throttling levels
EF_range_split_level = [[0, 0],
                        [1, 0],
                        [2, 0],
                        [3, 0],
                        [1, 1],
                        [2, 1],
                        [3, 1],
                        [1, 2],
                        [2, 2],
                        [3, 2]]

# Hand calculated aggregate throttling factors, corresponding to each of the
# throttling levels in the split range progression. Columns are for reactions,
# rows are for cases in the requested compression scales.
split_level_aggregate_factors = [[1.0000E+00, 1.0000E+00, 1.0000E+00, 1.0000E+00, 1.0000E+00, 1.0000E+00, 1.0000E+00],
                                 [1.6000E-02, 4.0000E-01, 4.0000E-01, 1.0000E+00, 1.0000E+00, 1.0000E+00, 1.0000E+00],
                                 [4.0000E-05, 4.0000E-02, 4.0000E-01, 1.0000E+00, 1.0000E+00, 1.0000E+00, 1.0000E+00],
                                 [4.8400E-07, 4.4000E-03, 4.0000E-01, 1.0000E+00, 1.0000E+00, 1.0000E+00, 1.0000E+00],
                                 [1.6000E-02, 4.0000E-01, 4.0000E-01, 1.0000E+00, 2.5000E+00, 2.5000E+00, 6.2500E+01],
                                 [4.0000E-05, 4.0000E-02, 4.0000E-01, 1.0000E+00, 2.5000E+00, 2.5000E+00, 6.2500E+01],
                                 [4.8400E-07, 4.4000E-03, 4.0000E-01, 1.0000E+00, 2.5000E+00, 2.5000E+00, 6.2500E+01],
                                 [1.6000E-02, 4.0000E-01, 4.0000E-01, 1.0000E+00, 2.5000E+00, 2.5000E+01, 2.5000E+04],
                                 [4.0000E-05, 4.0000E-02, 4.0000E-01, 1.0000E+00, 2.5000E+00, 2.5000E+01, 2.5000E+04],
                                 [4.8400E-07, 4.4000E-03, 4.0000E-01, 1.0000E+00, 2.5000E+00, 2.5000E+01, 2.5000E+04]]

# Allowed residual on aggregate throttling factors
atf_residual_tolerance = 1E-6

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
