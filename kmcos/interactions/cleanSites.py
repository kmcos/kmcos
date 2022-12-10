import copy
from kmcos.interactions.cleanCoordinates import *
class dummyclass:
    pass

def initializeProjectForCleanSites(projectObject):
    global pt 
    pt = projectObject
    
pt = dummyclass()
pt.EaDict ={}
pt.ADict ={}
pt.siteDict={}
pt.lattice={}

def addSiteIfNotThere(coordFullName, project = None):
    if project == None:
        project = pt #What I have done here is set pt to be a "default" when no argument is provided. But it only works when pt is defined globally in this module.
    if coordFullName in project.siteDict:
        pass #this means it's already there!
    else:
        addSiteDistinct(coordFullName, project) #else, we add it.

#This function calls the "addSite" function from above, and just takes the arguments in a different way then parses them etc.
def addSiteDistinct(coordFullNameOfSite, project=None):
    coordFullNameOfSiteList = coordFullNameOfSite.split("___")
    #Need to conver the unit cell cartesian cooridnates into a tuple.
    layerName=coordFullNameOfSiteList[0]
    siteType=coordFullNameOfSiteList[1]
    unitCellTupleString = coordFullNameOfSiteList[2]
    #now need to convert unit cell's cartesian coordinates to a tuple.
    unitCellTuple = cartesianCoordinateFromPandNandDtoTuple(unitCellTupleString)
    addSite(layerName, siteType, unitCellTuple, project)
    
#make three arguments for the coordinate generation: siteName, unitCellTuple, layerName.
#In this context, siteName is the site type (such as Pt_atop etc.).
def addSite(layerName, siteName, unitCellTuple=(0,0,0), project=None):
    #Example: addSite("Layer1", "atop_Ce1", (0,0,0)) #I ended up putting the unit cell tuple last so that it can have default of (0,0,0)    
    if project == None:
        project = pt #What I have done here is set pt to be a "default" when no argument is provided. But it only works when pt is defined globally in this module
    #We want unitCellTuple to be a tuple, and we want unitCellTupleString to be a string. The below code does any conversions necessary to fix unitCellTuple, as it was provided.
    if type(unitCellTuple)==tuple:
        unitCellTupleString = str(unitCellTuple)
    if type(unitCellTuple)==str:
        unitCellTupleString = str(unitCellTuple)   
        unitCellTuple = eval(unitCellTupleString)
    #For the coordinate name, we need the underscored version. E.g., (0,0,0) becomes p0_p0_p0
    underScoredCoordinatesString = (unitCellTuple)    
    coordFullNameElements = [layerName, siteName, underScoredCoordinatesString]
    coordFullName = "___".join(coordFullNameElements)    
    
    #CoordInput should be a string like 'atop_Ce1.(0,0,0).Layer1', which is the site_name.unit_cell_coordinate.layer.
    #For example, 'atop_O1.(1,0,0).Ce1' would be a site named atop_01, one unit cell to the right, and in the layer Ce1. 
    coordInput = siteName + "." + unitCellTupleString + "." + layerName #looks like: 'atop_Ce1.(0,0,0).Layer1' #This is kmos syntax.
    newCoord = project.lattice.generate_coord(coordInput) #This generates the kmos coordinate.
    #create the dictionary if it's not already there.    
    if hasattr(project, "siteDict") == False: #This checks if it's in that object's local namespace.
        project.siteDict = {}  #creating an empty dictionary if it's not yet there, so we can add to it with convenient syntax.
    if hasattr(project, "siteTypeDict") == False:
        project.siteTypeDict= {}
    #now create local references for convenience:
    siteDict = project.siteDict
    siteTypeDict = project.siteTypeDict
    #assign the values using coordFullName as keys.
    siteDict[coordFullName]= newCoord
    siteTypeDict[coordFullName]=siteName
    return newCoord

def EaDictToParameters(EaDict = None, project = None, units = "eV"):
    #This adds any non-string as a parameter to kmos.  If the units argument is set to "J", it converts from J/mol to eV.
    #The optional unit conversion occurs if you put in a number. Otherwise the units argument is ignored.
    if project == None:
        project = pt #What I have done here is set pt to be a "default" when no argument is provided. But it only works when pt is defined as a global for this module.
    if EaDict == None:
        EaDict = project.EaDict
    for key in EaDict:
        if isinstance(EaDict[key],str):
            pass #if it's a string, then we don't add it as a kmos parameter.
        else:
            if units == "eV":
                pt.add_parameter(name=key, value=EaDict[key])
            if units == "J":
                from BEPmodule import eV_to_J
                value_in_eV = eV_to_J(EaDict[key])
                pt.add_parameter(name=key, value=value_in_eV)

def ADictToParameters(ADict = None, project = None, units = "s-1"):
    if project == None:
        project = pt #What I have done here is set pt to be a "default" when no argument is provided. But it only works when pt is defined as a global for this module.
    if ADict == None:
        ADict = project.ADict
    for key in ADict:
        if isinstance(ADict[key],str):
            pass #if it's a string, then we don't add it as a kmos parameter.
        else:
            #This is where a unit conversion could be added, if somebody wanted to use such a feature.
            pt.add_parameter(name=key, value=ADict[key])

    
def conditionPairToCondition(conditionPair, conditionType = "Condition", project = None):
    if project == None:
        project = pt #What I have done here is set pt to be a "default" when no argument is provided. But it only works when pt is defined globally in this module.    
    #The "type" can be "Condition" or "Action" or "Bystander"
    #print "inside condition pair converter", conditionPair
    if type(conditionPair[0]) == str: #This comparison will return an error if the object is already coordinate.
             conditionCoord = project.siteDict[str(conditionPair[0])]
    else: #else, we assume it's already a coordinate:
        conditionCoord = conditionPair[0]
    # now, we need to make a condition object: 
    if conditionType == "Action" or "Condition":
        thisCondition = eval("{typeFunction}(coord=conditionCoord, species=conditionPair[1])".format(typeFunction=conditionType))
    if conditionType == "Bystander":
        thisCondition = eval("{typeFunction}(coord=conditionCoord, allowed_species=conditionPair[1])".format(typeFunction=conditionType))
    return thisCondition
            
def conditionPairsToConditionsList(conditionPairs, conditionType = "Condition"):
    #The "type" can be "Condition" or "Action" or "Bystander"
    conditionsList = []
    for conditionPair in conditionPairs:
        #print "thisConditionPair", conditionPair
        #We want the coord as a coord object, not a string. So if it's a string, we need to retrieve the coord object from globals.
        thisCondition = conditionPairToCondition(conditionPair, conditionType)
        #print "thisConditionAfterConversion", thisCondition
        conditionsList.append(thisCondition)
    return conditionsList

def checkListAsTuples(ListAsTuples):
    if isinstance(ListAsTuples, tuple) == True:  #If the whole thing is a tuple, they probably entered only one instead of a list, by mistake.
        ListAsTuples = [ListAsTuples]
    if isinstance(ListAsTuples[0], tuple) == False:  #Error for other cases.
        raise Exception("The conditionsListAsTuples and the actionstListAsTuples must be a list of tuples.")    
    return     ListAsTuples

def retrieveTransitionFrequency(processTypeString, project = None, type = "kmos"):  
    #Here, we don't use the processName which is like pF18p0.  We just use the processTypeString, which is like F18p0. 
    #I probably need to think of a better name than "processTypeString"
    if type == "kmos": #As currently written, this function returns a string, designed for kmos.
        Ea = project.EaDict['Ea'+processTypeString]
        if isinstance(Ea, str): #if it's a string, no problem. If it's not a string, that means we need to use the name as  string instead.
            pass
        else:
            Ea = 'Ea' + processTypeString
        
        A = project.ADict['A'+processTypeString]
        if isinstance(A, str): #if it's a string, no problem. If it's not a string, that means we need to use the name as  string instead.
            pass
        else:
            A = 'A' + processTypeString    
        
        #We *do* expect things to be in eV, when using kmos. The "-1" is for "-Ea", and is kept as a separate term to avoid bugs.
        transitionFrequency = A + '*exp(beta*(-1)*('+ Ea + ')*eV)'
        return transitionFrequency
        
def removeCommonElements(list1, list2): #list1 is the list we want common elements removed from. We will cycle through list 2 and try to remove each item from list1.
    truncatedList = copy.copy(list1) #This line is very important so we don't pop the original list!
    for elementToTryAndRemove in list2:
        try:
            indexToPop = truncatedList.index(elementToTryAndRemove)
            truncatedList.pop(indexToPop)
        except:
            pass
            #We don't do anything during the exception.
    return truncatedList

