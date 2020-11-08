# -*- coding: utf-8 -*-
"""
There are two ways to use UnitTesterSG: either with a known expected response, or simply comparing to a stored response.
This file is an example and template for a case where we can't simply 'provide' a solution so must compare to an **existing from before** output.

TO USE THIS TEMPLATE/EXAMPLE, YOU MUST RUN THIS FILE ONE TIME TO INITIATE. THE FIRST TIME THIS FILE IS RUN, IT WILL SAY THAT THE CALCULATED RESULT AND EXPECTED RESULT DO NOT MATCH -- THAT IS BECAUSE THE EXPECTED RESULT DOES NOT YET EXIST. DURING RUNTIME, THE SECOND QUESTION THE PROGRAM ASKS WILL BE IF YOU WANT TO OVERRWRITE OR CREATE EXPECTED RESULTS FILES: CHOOSE "Y"  AFTER DOING SO, THE EXPECTED RESULT HAS BEEN SET.  RUN THIS FILE AGAIN. SINCE YOU ARE RUNNING ON THE SAME COMPUTER, THE RESULT WILL BE THE SAME AND THE TEST WILL PASS. THE RESULT HAS BEEN STORED, SO THE TEST DIRECTORY CAN NOW BE INCLUDED IN A REPOSITORY OR COPIED TO ANOTHER COMPUTER FOR TESTING.

IF YOU WISH TO RESET THE STORED EXPECTED RESULTS TO NOT BEING SET YET, DELETE THE FILES THAT BEGIN WITH THE WORD EXPECTED.

You may copy this file and modify it to make your own test. Just name your file test_N where N is an integer.
"""

#These "sys" lines are mainly because this are standard lines in our examples. Normally, you would not include these three lines.
import sys
sys.path.insert(1, ".\\lib")
sys.path.insert(1, "..")



#import the functions from UnitTesterSG
import UnitTesterSG as ut

#The below lines are typical code. There is no need to modify them.
#get the suffix argument for check_results
suffix = ut.returnDigitFromFilename(__file__)
#prefix. Make this '' if you do not want any prefix.
prefix = ''


"""
#This file is an example/template for when we ***don't have an analytical result*** but we know our function is working.
#We know the function is working during template distribution because we are just using the test 12 example.
In this template, we ***will not*** use the "set_expected_result" command. So we are commenting out the below lines, and will go directly to using the function to create an actual output.
"""
# # # #input for the unit that will be tested
# # # inputValue = 4
# # # expectedFirstPart = [3,4,5]
# # # expectedSecondPart = [32,64]
# # # expectedResult = (expectedFirstPart,expectedSecondPart) #We are using a tuple, but it this could have been a list.

# # # ut.set_expected_result(expectedResult,expected_result_str=str(expectedResult), prefix=prefix,suffix=suffix) #This is the typical syntax if you want to force an analytical result for your test.


"""
#Calculate our function outputs (actual results). We can functions from another module in this section.
"""
indexOfBackendToTest = int(suffix) - 1 #test_1 will be index 0, test_2 will be index 1, and test_3 will be index 2.
import acf_test_function
actualResult = acf_test_function.test_build_model(indexOfBackendToTest=indexOfBackendToTest)

"""We put our actual result into the resultObj variable."""
#put this in the resultObject
resultObj = actualResult

#String must be provided provided. Make it '' if you do not want to use a result string.
resultStr = str(resultObj)


"""We set our tolerances. There can be some rounding when the tolerances get checked, so they are not exact."""
relativeTolerance = 0.10
absoluteTolerance = 2.0


#this is so that pytest can do UnitTesterSG tests.
def test_pytest(): #note that it cannot have any required arguments for pytest to use it, and that it is using variables that are defined above in the module.
    ut.doTest(resultObj, resultStr, prefix=prefix,suffix=suffix, allowOverwrite = False, relativeTolerance=relativeTolerance, absoluteTolerance=absoluteTolerance)
    
"""#For any individual test, after finishing getting it working, set allowOverwrite to False in the line below calling doTest if you want to skip UnitTesterSG from stopping to notify user when results match but result strings don't. """        
if __name__ == "__main__":
   #This is the normal way of using the UnitTesterSG module, and will be run by UnitTesterSG or by running this test file by itself.
   ut.doTest(resultObj, resultStr, prefix=prefix,suffix=suffix, allowOverwrite = True, relativeTolerance=relativeTolerance, absoluteTolerance=absoluteTolerance)
