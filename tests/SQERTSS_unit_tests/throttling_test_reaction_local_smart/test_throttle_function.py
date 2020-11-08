#!/usr/bin/env python

# This is a script to test the throttling functions for the various
# test cases. The goal is to verify that the throttling code is properly
# calculating the aggregate throttling factors for the specified compression
# ranges.

from test_throttle_case_7 import *
try:
    import kmcos.throttling as throttling
except:
    import throttling

# Function to extract the aggregate throttling factors from the returned
# structure for easy comparison to our flat list of aggregate throttling
# factors.
def extract_aggregate_throttling_factors():

    local_aggregate_throttling_factors = []
    for i in [0, 1]:    #Fwd/Rev
        atf_sublist = tg.aggregate_throttling_factors[i]
        for j in range(len(atf_sublist)):
            local_aggregate_throttling_factors.append(atf_sublist[j][0:2])
    local_aggregate_throttling_factors.sort(key=lambda x: x[0])

    atf = []
    for i in range(len(local_aggregate_throttling_factors)):
        atf.append(local_aggregate_throttling_factors[i][1])
    return atf

# Sort and rank the unthrottled rate data
tg.current_ranking_scheme = 'paired'
throttling.rank_EFs_driver()

# Print the process rankings
print('Process rankings: ', tg.ranked_uEF_list)

# Full range test
for i in range(len(EF_range_full)):

    # Set the EF range
    tg.EF_range_flag = 'full'
    tg.EF_range_full = EF_range_full[i]

    # Call the throttling function
    throttling.throttle_rate_constants_driver()

    # Print the results
    if results_check and len(EF_range_full) == len(EF_range_full_level):
        if [tg.fast_throttling_scale, tg.slow_throttling_scale] == EF_range_full_level[i]:
            print('Full range OK:', EF_range_full_level[i])
        else:
            print('Full range not OK: ')
            print('  Expected: ', EF_range_full_level[i])
            print('  Actual: ', [tg.fast_throttling_scale, tg.slow_throttling_scale])
    else:
        print('Full range compression: ', [tg.fast_throttling_scale, tg.slow_throttling_scale])

# Split range test
calculated_atf = []
# FIXME: Add test for throttled ef list
for i in range(len(EF_range_split)):

    # Set the EF range
    tg.EF_range_flag = 'split'
    tg.EF_range_fast = EF_range_split[i][0]
    tg.EF_range_slow = EF_range_split[i][1]

    # Call the throttling function
    throttling.throttle_rate_constants_driver()

    # Also save the aggregate throttling factors for testing after the range
    # compression tests are complete.
    atf = extract_aggregate_throttling_factors()
    calculated_atf.append(atf)

    # Extract the aggregate throttling factors for this run and sort them by
    # reaction number

    # Print the results
    if results_check and len(EF_range_split) == len(EF_range_split_level):
        if [tg.fast_throttling_scale, tg.slow_throttling_scale] == EF_range_split_level[i]:
            print('Split range OK:', EF_range_split_level[i])
        else:
            print('Split range not OK: ')
            print('  Expected: ', EF_range_split_level[i])
            print('  Actual: ', [tg.fast_throttling_scale, tg.slow_throttling_scale])
    else:
        print('Split range compression: ', [tg.fast_throttling_scale, tg.slow_throttling_scale])

# Aggregate throttling factors test
for i in range(len(EF_range_split)):

    # Calculate relative residuals for checking
    if (results_check
        and len(calculated_atf) == len(split_level_aggregate_factors)
        and len(split_level_aggregate_factors[i]) == len(calculated_atf[i])):
        atf_residual = [(k - j)/k for k, j in
            zip(split_level_aggregate_factors[i], calculated_atf[i])]

    if (results_check and len(EF_range_split) == len(EF_range_split_level)
        and len(split_level_aggregate_factors) == len(calculated_atf)):
        if (abs(max(atf_residual)) > atf_residual_tolerance or
            abs(min(atf_residual)) > atf_residual_tolerance):
            print('Aggregate throttling factors not OK:', EF_range_split_level[i])
            print('  Expected aggregate throttling factors: ', split_level_aggregate_factors[i])
            print('  Actual aggregate throttling factors: ', calculated_atf[i])
        else:
            print('Aggregate throttling factors OK:', EF_range_split_level[i])
    else:
        print('Actual aggregate throttling factors: ', calculated_atf[i])
