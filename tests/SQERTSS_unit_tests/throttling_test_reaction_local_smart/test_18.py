#!/usr/bin/env python

try:
    import kmcos.snapshots_globals as sg
    import kmcos.snapshots as snapshots
    import kmcos.throttling_globals as tg
    import kmcos.throttling as throttling
    print("line 8 successful import.")
except:
    print("line 9 into the except statement")
    import snapshots_globals as sg
    import snapshots
    import throttling_globals as tg
    import throttling
import export_import_library as eil
from copy import deepcopy



####Expected results populated manually####

#Here is an expectedResultsDict that is being populated manually using the excel sheet 161220_ManualExamples_Deprecated.xlsx (see near column AI).
#The format inside here is reaction number and ptEF, where the ptEF is the higher of the forward and reverse reaction after throttling.
#In the test files above, the aggregate_throttling_factors are not populated. But tg.ptEF_list is, so we'll use ptEF_list.  
expectedResultsDict = {}
expectedResultsDict['11'] = \
[
    [	4	,	0.129855187	]	,
    [	3	,	0.129855187	]	,
    [	1	,	0.259710375	]	,
    [	2	,	0.324637969	]	,
    [	5	,	20.7119024	]	,
    [	6	,	207.119024	]	,
    [	7	,	2071.19024	]	,
]

expectedResultsDict['12'] = \
[
    [	1	,	0.11392763	]	,
    [	2	,	0.11392763	]	,
    [	3	,	0.11392763	]	,
    [	4	,	0.398746706	]	,
    [	5	,	20.05126291	]	,
    [	6	,	200.5126291	]	,
    [	7	,	2005.126291	]	,
]

expectedResultsDict['13'] = \
[
    [	1	,	0	]	,
    [	2	,	0	]	,
    [	3	,	0	]	,
    [	4	,	0	]	,
    [	5	,	0	]	,
    [	6	,	100	]	,
    [	7	,	12102.43902	]	,
]

expectedResultsDict['14'] = \
[
    [	2	,	0.139805995	]	,
    [	3	,	0.170873993	]	,
    [	4	,	0.176051993	]	,
    [	1	,	0.217475991	]	,
    [	5	,	19.49661907	]	,
    [	6	,	70.42079724	]	,
    [	7	,	77.46287696	]	,
]

expectedResultsDict['15'] = \
[
    [	2	,	0.163279537	]	,
    [	3	,	0.173813701	]	,
    [	1	,	0.184347865	]	,
    [	4	,	0.184347865	]	,
    [	5	,	1.843478645	]	,
    [	6	,	18.43478645	]	,
    [	7	,	184.3478645	]	,
]


expectedResultsDict['16'] = \
[
    [	1	,	0	]	,
    [	2	,	0	]	,
    [	3	,	0	]	,
    [	4	,	3.71359657	]	,
    [	5	,	22.28157942	]	,
    [	6	,	1830.803109	]	,
    [	7	,	183841.5982	]	,
]

expectedResultsDict['17'] = \
[
    [	1	,	0	]	,
    [	2	,	0	]	,
    [	3	,	0	]	,
    [	4	,	3.75	]	,
    [	5	,	1500	]	,
    [	6	,	1830.803109	]	,
    [	7	,	183841.5982	]	,
]


expectedResultsDict['18'] = \
[
    [	1	,	0.11392763	]	,
    [	2	,	0.11392763	]	,
    [	3	,	0.11392763	]	,
    [	4	,	0.398746706	]	,
    [	5	,	2	]	,
    [	6	,	122.3582748	]	,
    [	7	,	48943.30993	]	,
]



expectedResultsDict['19'] = \
[
    [	1	,	0.11392763	]	,
    [	2	,	0.11392763	]	,
    [	3	,	0.11392763	]	,
    [	4	,	0.398746706	]	,
    [	5	,	91	]	,
    [	6	,	36400	]	,
    [	7	,	14560000	]	,
]



expectedResultsDict['20'] = \
[
    [	1	,	0.11392763	]	,
    [	2	,	0.11392763	]	,
    [	3	,	0.11392763	]	,
    [	4	,	0.398746706	]	,
    [	5	,	91	]	,
    [	6	,	36400	]	,
    [	7	,	14560000	]	,
]


####Helper functions to conduct the tests####


#Takes one expected_ptEFs_List at a time, like expectedResultsDict['19'], and then returns a sorted version.
def getSortedExpected_ptEF_list(expected_ptEFs_List): 
    sortedExpected_ptEF_list = []
    for reactionNumberDesired in range(1,len(expected_ptEFs_List)+1): #loop once for each reaction to add 
        for listIndex in range(0,len(expected_ptEFs_List)): #loop again for each entry.
            currentReactionNumber = expected_ptEFs_List[listIndex][0]
            if currentReactionNumber == reactionNumberDesired:
                sortedExpected_ptEF_list.append(expected_ptEFs_List[listIndex])
    return sortedExpected_ptEF_list
    
#In the test files, the aggregate_throttling_factors are not populated. But tg.ptEF_list is, so we'll use ptEF_list.  One difference in the test files relative to the excel sheet is that ptEF_list has None objects instead of zeros. #So we can't use an == check without first converting any "None" into zero.  We actually don't need to check whether the reaction is forward or reverse because one of the items in the ptEF_list is the greater of the two EF's.
#The individual elements in the ptEF_List are like this:
#['1p0', 0.11, 0.11, 1.0, 0.11, 'F', 0]
#[RxnString, F_EF, R_EF, ITF??, faster_EF, directionOf_faster_EF, RxnIndex]
#So we just need to pull out (in arrayIndexing) index 4 and 6. We do this with a helper function called get_ptEF_for_rxn.
def get_Actual_ptEF_for_rxn(full_ptEF_List, desiredRxnNumber): #feed tg.ptEF_List as full_ptEF_List
    for rxn_ptEF_list in full_ptEF_List: #The tg.ptEF_List is actually a list of lists. rxn_ptEF_list is an individual reaction's ptEF_list.
        if rxn_ptEF_list[6] + 1  == desiredRxnNumber: #This checks if it's the right reaction number.
            ptEF_for_rxn = rxn_ptEF_list[4] #this gets the ptEF for that reaction.
            if type(ptEF_for_rxn) == type(None): #set to 0 if it's a None type.
                ptEF_for_rxn = 0
            return ptEF_for_rxn
       #else pass #is implied.
       
def getSortedActual_ptEF_list(full_ptEF_List):
    sortedActual_ptEF_list = []
    for reactionNumberDesired in range(1,len(full_ptEF_List)+1): #loop once for each reaction to add 
        Actual_ptEF_for_rxn = get_Actual_ptEF_for_rxn(full_ptEF_List, reactionNumberDesired)
        sortedActual_ptEF_list.append([reactionNumberDesired, Actual_ptEF_for_rxn])
    return sortedActual_ptEF_list

      


####Actual Testing section####
#import the functions from UnitTesterSG
#We are actually the same code repeatedly but changing the file name.
#This is so that pytest and UnitTesterSG can discriminate these as separate tests.
#It is a little bit slower this way, but better for unit testing and these are anyway fast tests.
import UnitTesterSG as ut

all_ExpectedResults = []
all_ActualResults = []
for case_number in [ut.returnDigitFromFilename(__file__)]: 
    print(case_number)
    tg.FFP_roof = None
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

    tg.aggregate_throttling_factors

    # Calculate throttling factors
    throttling.calculate_throttling_factors(unthrottle_slow_processes=False)

    # Save the module
    tg_module.save_params()
    
    tg.aggregate_throttling_factors_dict
    
    #Now to compare the expected and actual.
    expectedResult = getSortedExpected_ptEF_list(expectedResultsDict[str(case_number)])
    actualResult = getSortedActual_ptEF_list(tg.ptEF_list)
    all_ExpectedResults.append(expectedResult)
    all_ActualResults.append(actualResult)



    ####Below is so that UnitTesterSG tests can bedone####

    #The below lines are typical code. There is no need to modify them.
    #get the suffix argument for check_results
    suffix = ut.returnDigitFromFilename(__file__)
    suffix = case_number
    #prefix. Make this '' if you do not want any prefix.
    prefix = ''



    """We set our tolerances. There can be some rounding when the tolerances get checked, so they are not exact."""
    relativeTolerance = 1.0E-5
    absoluteTolerance = 1.0E-8

    ut.set_expected_result(expectedResult,expected_result_str=str(expectedResult), prefix=prefix,suffix=suffix) #This is the typical syntax if you want to force an analytical result for your test.
    
    
    resultObj = actualResult
    resultStr = str(resultObj)
    
    #this is so that pytest can do UnitTesterSG tests.
    def test_pytest(): #note that it cannot have any required arguments for pytest to use it, and that it is using variables that are defined above in the module.
        ut.doTest(resultObj, resultStr, prefix=prefix,suffix=suffix, allowOverwrite = False, relativeTolerance=relativeTolerance, absoluteTolerance=absoluteTolerance)
        
    """#For any individual test, after finishing getting it working, set allowOverwrite to False in the line below calling doTest if you want to skip UnitTesterSG from stopping to notify user when results match but result strings don't. """        
    if __name__ == "__main__":
       #pass #*****TURNING OFF FOR DEBUGGING PURPOSES**************
       #This is the normal way of using the UnitTesterSG module, and will be run by UnitTesterSG or by running this test file by itself.
       ut.doTest(resultObj, resultStr, prefix=prefix,suffix=suffix, allowOverwrite = True, relativeTolerance=relativeTolerance, absoluteTolerance=absoluteTolerance)