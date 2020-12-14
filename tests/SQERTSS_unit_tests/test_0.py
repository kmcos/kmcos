"""
There are two ways to use UnitTesterSG: either with a known expected response, or simply comparing to a stored response.
This file is an example and template for a case with a known (e.g., analytical or otherwise calculated) expected response.
Just name your file test_N where N is an integer.

#NOTE: FOR THE TEMPLATE AS DISTRIBUTED: WHEN YOU RUN THIS FILE, IT WILL SAY THE **EXPECTED RESULT** MATCHES BUT THAT THE **EXPECTED RESULT STRING** DOES NOT MATCH. IT IS PERFECTLY FINE THAT THE RESULT STRING DOES NOT MATCH. THAT IS A TYPICAL SITUATION AND A FEATURE. IT DOES NOT MEAN THE TEST FAILED.
"""
#import the functions from UnitTesterSG
import UnitTesterSG as ut
#The below lines are typical code. There is no need to modify them.
#get the suffix argument for check_results
suffix = ut.returnDigitFromFilename(__file__)
#prefix. Make this '' if you do not want any prefix.
prefix = ''


####in this file, we are going to delete the xml and freshly export a model and change directories before doing anything####
import os
ModelName = "throttling_test_reaction"
backend = 'local_smart'
import kmcos.io
kmcos.io.clear_model(ModelName, backend=backend)
exec('import ' +ModelName) #This will create the xml. Like import MyFirstThrottling.py
import kmcos.cli
kmcos.cli.main('export '+ModelName+ '.xml '+ ' -o -b '+ backend)  #this will export the model with the standard backend.
os.chdir('..') #need to go back since export moves into src directory
os.chdir('..') #go back one further since what we are going to do is compare the xml.

"""
#This file is an example/template for when we ***know*** what result to expect.
#In the original template example, when we put in the number 4, we expect to get two arrays: One with values  [3,4,5]  and another with [32,64] Note that they are of different lengths. This is not a problem for UnitTesterSG.
#We must make a single results object: we will put lists with those values inside. Recognize that we are expecting array objects, but we can define our analytical result as a list. This is part of why UnitTesterSG was developed, since it compares what is inside, not just the objects.
"""

#This file is really just to export the xml before the other unit tests are run.
#We will keep and use the expected xml in order to make this a unit test.
expectedXMLfile = open("throttling_test_reaction_expected_xml.xml", "r") 
expectedResult = expectedXMLfile.read()
expectedXMLfile.close() #don't forget to close a file when not using "with open" !

ut.set_expected_result(expectedResult,expected_result_str=str(expectedResult), prefix=prefix,suffix=suffix) #This is the typical syntax if you want to force an analytical result for your test.


"""
#Calculate our function outputs (actual results). We can functions from another module in this section.
"""
actualXMLfile = open(ModelName+".xml", "r") 
actualResult = actualXMLfile.read()
actualXMLfile.close() #don't forget to close a file when not using "with open" !

"""We put our actual result into the resultObj variable."""
#put this in the resultObject
resultObj = actualResult

#String must be provided provided. Make it '' if you do not want to use a result string.
resultStr = str(resultObj)


"""We set our tolerances. There can be some rounding when the tolerances get checked, so they are not exact."""
relativeTolerance = 0.20 #The relative tolerances have to be quite large this time due to statistical fluctuations. It would probably pass most of the time with 0.10, but 0.20 is more safe and is still very distinct for what comes out with this algorithm.
absoluteTolerance = 1E-5


#this is so that pytest can do UnitTesterSG tests.
def test_pytest(): #note that it cannot have any required arguments for pytest to use it, and that it is using variables that are defined above in the module.
    ut.doTest(resultObj, resultStr, prefix=prefix,suffix=suffix, allowOverwrite = False, relativeTolerance=relativeTolerance, absoluteTolerance=absoluteTolerance)

"""#For any individual test, after finishing getting it working, set allowOverwrite to False in the line below calling doTest if you want to skip UnitTesterSG from stopping to notify user when results match but result strings don't. """        
if __name__ == "__main__":
   #This is the normal way of using the UnitTesterSG module, and will be run by UnitTesterSG or by running this test file by itself.
   ut.doTest(resultObj, resultStr, prefix=prefix,suffix=suffix, allowOverwrite = True, relativeTolerance=relativeTolerance, absoluteTolerance=absoluteTolerance)
   
os.system("cd ..")