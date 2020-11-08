#!/usr/bin/env python

# This is a simple script to extract test results from the output files and
# print the important information (the ATFs and ptEFs and the compression
# ranges) to screen.

cases = range(11,21)

for case in cases:

    # Load the variables
    filename = 'test_throttle_case_' + str(case) + '_params_out.txt'
    print('Case =', case)
    exec(compile(open(filename, "rb").read(), filename, 'exec'))

    # ATF dictionary
    ATF = {}
    for i in [0, 1]:
        num_processes = len(aggregate_throttling_factors[i])
        for j in range(num_processes):
            rxn = aggregate_throttling_factors[i][j][0]
            ATF_element = aggregate_throttling_factors[i][j][1]
            ATF[rxn] = ATF_element

    # ptEFs and corresponding ATFs
    ptEF = []
    num_processes = len(ptEF_list)
    for i in range(num_processes):
        rxn = ptEF_list[i][0]
        ptEF_element = ptEF_list[i][4]
        if rxn in ATF:
            ATF_element = ATF[rxn]
        else:
            ATF_element = 1
        ptEF.append([rxn, ptEF_element, ATF_element])
    ptEF.sort(key=lambda x: x[0])

    # Print the results
    for i in range(num_processes):
        print(ptEF[i])

    print('EF_range_fast_actual =', EF_range_fast_actual)
    print('EF_range_slow_actual =', EF_range_slow_actual)

    print('')
