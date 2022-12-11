import itertools
import copy
import sys
import warnings
from kmcos.interactions.cleanCoordinates import *
try:
    import kmcos.interactions.BEPmodule
    from kmcos.interactions.BEPmodule import *
except:
    pass
from kmcos.types import * #this is necessary in order to make condition objects.

##############################################
#Some things to know about this module:
# 1) This module assumes there is a project object.  By default, the functions expect a variable that is global to this module named pt.  
#    Thus, it's convenient to use initializeProjectForAdsorbateInteractions(projectObject) inside the runfile, after making your project variable.
# 2) This module makes a few dictionaries inside that project variable:
    # siteDict, siteTypeDict, surroundingSitesDict

################################################

###############################################
#For some context about the below functions:
# First and foremost, you need to have a set of sites defined and the possible species for those sites defined in your runfile.
# getAllSurroundingPossibilities calls getCombinedSiteOccupationPossibilities and also getSiteOccupationPossibilities

#############################################

class CIProjectClass:
    pass

def initializeProjectForConfigurationsAndInteractions(projectObject, software ="kmcos"):
    global CIProject
    CIProject = CIProjectClass()
    CIProject.EaDict = {}
    CIProject.ADict = {}
    CIProject.surroundingSitesDict = {}
    CIProject.possibleSpeciesDict = {}
    CIProject.siteDict = {}
    CIProject.siteTypeDict = {}
    CIProject.possibleParticlesForSiteTypes = {}
    CIProject.BEPRelationsDict = {}
    CIProject.aggregateBaseConditionsSitesList = []
    CIProject.interactionTermsDict = {}
    CIProject.software = software
    global pt
    if software == "kmcos": #connect the variables to the kmcos project for convenience
        CIProject.kmcos_project = projectObject
        pt = projectObject
        pt.EaDict = CIProject.EaDict
        pt.ADict = CIProject.ADict
        pt.surroundingSitesDict = CIProject.surroundingSitesDict
        try: #Try to add surroundingSitesDict to the connected variables of the project class object, but this is not required for the module to work.
            pt.connected_variables['surroundingSitesDict'] = pt.surroundingSitesDict 
        except:
            pass
        pt.possibleSpeciesDict =CIProject.possibleSpeciesDict
        pt.siteDict = CIProject.siteDict 
        pt.siteTypeDict = CIProject.siteTypeDict 
        pt.possibleParticlesForSiteTypes= CIProject.possibleParticlesForSiteTypes
        pt.BEPRelationsDict = CIProject.BEPRelationsDict
        pt.aggregateBaseConditionsSitesList = CIProject.aggregateBaseConditionsSitesList
        pt.interactionTermsDict = CIProject.interactionTermsDict
        

def EaDictToParameters(EaDict = None, project = None, units = "eV"):
    #This adds any non-string as a parameter to kmcos.  If the units argument is set to "J", it converts from J/mol to eV.
    #The optional unit conversion occurs if you put in a number. Otherwise the units argument is ignored.
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.
    if EaDict == None:
        EaDict = project.EaDict
    if project.software == "kmcos":
        for key in EaDict:
            if isinstance(EaDict[key],str):
                pass #if it's a string, then we don't add it as a kmcos parameter.
            else:
                if units == "eV":
                    CIProject.kmcos_project.add_parameter(name=key, value=EaDict[key]) #I have hardcoded pt here for the case of kmcos.
                if units == "J":
                    from BEPmodule import eV_to_J
                    value_in_eV = eV_to_J(EaDict[key])
                    CIProject.kmcos_project.add_parameter(name=key, value=value_in_eV) #I have hardcoded pt here for the case of kmcos.


def ADictToParameters(ADict = None, project = None, units = "s-1"):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.
    if ADict == None:
        ADict = project.ADict
    if project.software == "kmcos":
        for key in ADict:
            if isinstance(ADict[key],str):
                pass #if it's a string, then we don't add it as a kmcos parameter.
            else:
                #This is where a unit conversion could be added, if somebody wanted to use such a feature.
                CIProject.kmcos_project.add_parameter(name=key, value=ADict[key]) #I have hardcoded pt here for the case of kmcos.

                
#The below function returns a list of tuples: there is tuple for each possibility of local configuration, with site and occupation.
#Note that the "site" in this case is actually given as a "coordFullName", it's not a site type, and it's just a string.
#Note also that this function must be called for EACH site type separately, since they would have different possible species.
def getSiteOccupationPossibilities (set_of_sites, PossibleSpecies):
    #Use itertools to find all possible products (i.e., permutations) of the possible adsorbates, for the number of equivalent sites.
    #the "repeat" argument is the number of bins, or in this case, sites.    
    if type(set_of_sites) != list:
        raise Exception("set_of_sites must be a list of strings")
    set_of_sites_occupations_possibilities = list((itertools.product(PossibleSpecies,repeat=len(set_of_sites))))
    #Now, we need to make lists and append them into a larger list. If there are 6 sites, we make little lists of 6 for the possible species and append them, but as pairs.
    siteOccupationPossibilities = []
    for possibileSpeciesCombination in set_of_sites_occupations_possibilities:
        #print possibileSpeciesCombination    
#below I create each of the site and species pairs for each possibileSpeciesCombination        
        currentSpeciesCombinationWithSites = []        
        for index, occupation_identity in enumerate(possibileSpeciesCombination):
            currentSpeciesCombinationWithSitePair = (set_of_sites[index],occupation_identity)
            currentSpeciesCombinationWithSites.append(currentSpeciesCombinationWithSitePair)
            #print currentSpeciesCombinationWithSites
            #print set_of_sites[index],occupation_identity
        siteOccupationPossibilities.append(currentSpeciesCombinationWithSites)
    #Below block is for testing purposes.
#    for possibility in siteOccupationPossibilities:
#        print possibility
#        for pair in possibility:
#           print pair
    return siteOccupationPossibilities #This object has the structure possibilities > pairs of site and species [and within each pair, one site one species]

#The below function takes 2 or more lists of tuples, which are the siteOccupationPossibilities lists, and then it returns what is essentially the product.
#For example, if there are 2 different types of sites with 6 possibilities and 4 possibilities respectively, then there are 24 total and this will return all 24 in the same format as the rest of this module: each tuple will be {coordFullName, occupation)
#Note if you try to use a blank list for any of the list-arguments in getCombinedSiteOccupationPossibilities, it returns a blank list.
def getCombinedSiteOccupationPossibilities(siteOccupationPossibilitiesLists):
    #First create the possibilities using an iter product.    
    CombinedSiteOccupationPossibilitiesIter = itertools.product(*siteOccupationPossibilitiesLists)
    #Then initialize list that will be populated and then returned    
    CombinedSiteOccupationPossibilitiesList = []
    #get the data structure we need out of the iter product.    
    for possibility in CombinedSiteOccupationPossibilitiesIter:
        #Because these are nested structures, the iter product is a bunch of lists, and we need a single list. So we chain them.
        chainedPossibility = list(itertools.chain.from_iterable(possibility))    
        #We are going to sort the possibility also, so that when we want to exclude common possibilities later we can detect them easily.
        sortedChainedPossibility = sorted(chainedPossibility)
        CombinedSiteOccupationPossibilitiesList.append(sortedChainedPossibility)
    return CombinedSiteOccupationPossibilitiesList

#getAllSurroundingPossibilities which will iterate through the surroundingSitesDict for a particular site, and will call repeatedly use possibleAdsorbatesForSiteTypes as an argument inside getSiteOccupationPossibilities, which will in turn return an argument for getCombinedSiteOccupationPossibilities repeatedly. 
#Made this ready for nearest neighbors syntax.  For example if somebody provides ruo2___bridge___p1_p0_p0 and upToDistance = 2 that will mean the 2nd nearest neighbors.
#Inside the surroundingSitesDict, the keys for further neighbor Distances will be like this: ruo2___bridge___p1_p0_p0____2 etc.
def getAllSurroundingPossibilities(coordFullName, definedSurroundingSites = None, upToDistance = 1, project = None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.
    possibleSpeciesDict = project.possibleParticlesForSiteTypes
    surroundingSitesDict = project.surroundingSitesDict
    if definedSurroundingSites == None:
        sitesAroundThisSite =[] #make an empty list, then extend it for each distance.
        for distance in range(1,upToDistance+1):
            try:
                sitesAroundThisSite.extend(surroundingSitesDict[coordFullName+"___"+str(distance)])
            except:
                print(("Warning: you requested a surrounding site distance of upToDistance " + str(upToDistance) + " for " + coordFullName + " but there is no surrounding site definition at distance " + distance))
                sitesAroundThisSite.extend([]) #extend with an empty list if there are no sites at the distance attempted.
    else: 
        sitesAroundThisSite = definedSurroundingSites
    AllSurroundingPossibilities = []#initialize as empty, and then fill.
    
    #TODO: Below code should actually be split into its own function for getting all possibilities. Then it could be called with just a list of sites. So we can get the surrounding sites, then call that function.
    for site in sitesAroundThisSite: #note that "site" here is actually the coordFullName of a site.
        siteType = extractSiteType(site)
        possibleSpeciesForThisSite = possibleSpeciesDict[siteType]
        occupationPossibilities = getSiteOccupationPossibilities([site],possibleSpeciesForThisSite) #Notes that the function on right requires a list of strings for first argument, so we feed it a list of length 1.
        if len(AllSurroundingPossibilities) == 0:
            AllSurroundingPossibilities = occupationPossibilities #First case has to be added, because when you try to use a blank list for any of the list-arguments in getCombinedSiteOccupationPossibilities, it returns a blank list.
        elif len(AllSurroundingPossibilities) > 0:
            AllSurroundingPossibilities = getCombinedSiteOccupationPossibilities([AllSurroundingPossibilities,occupationPossibilities])
    return AllSurroundingPossibilities
        
    
#The below function returns a list of lists: there is one list of conditions for each possibility of local configuration.
#Because the siteOccupationPossibilites are pairs with coordFullName and occupation type, the conditions are actually coordinates.
#Actions and Conditions are generated the same way except for one word, so I am providing an argument to let person generate Actions instead of Conditions, if they want to. That is needed for the real application, anyway.
#This function does not seem to be used anymore.
def getConditionsListsFromSitePossibilities(siteOccupationPossibilities, conditionType = "Condition", project = None):
    #The conditionType optional argument takes values of either "Condition" or "Action" or "Bystander"
    conditionsLists = [] #There will be a separate list within each list of possibilties
    for possibility in siteOccupationPossibilities:
        conditionsListForThisPossibility = []        
        for pair in possibility:
            coordString = pair[0]
            speciesString = pair[1]
            conditionStringToEval = conditionType + "(coord={coordString}, species='{speciesString}')".format(coordString=coordString, speciesString=speciesString)         
            #The below line *does* Depend on kmcos, as written now, since it creates a condition object.            
            currentCondition = eval(conditionStringToEval)            
            conditionsListForThisPossibility.append(currentCondition)
        conditionsLists.append(conditionsListForThisPossibility)
    return conditionsLists #one list of Conditions (or Actions) for each possibility of local configuration.

#make three arguments for the coordinate generation: siteName, unitCellTuple, layerName.
#In this context, siteName is the site type (such as Pt_atop etc.).
#This is specifically for kmcos, as currently written.
def addSite(layerName, siteName, unitCellTuple=(0,0,0), project=None):
    #Example: addSite("Layer1", "atop_Ce1", (0,0,0)) #I ended up putting the unit cell tuple last so that it can have default of (0,0,0)
    if project == None:
        project = CIProject #What I have done here is set pt to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module
    
    #We want unitCellTuple to be a tuple, and we want unitCellTupleString to be a string. The below code does any conversions necessary to fix unitCellTuple, as it was provided.
    if type(unitCellTuple)==tuple:
        unitCellTupleString = str(unitCellTuple)
    if type(unitCellTuple)==str:
        unitCellTupleString = str(unitCellTuple)   
        unitCellTuple = eval(unitCellTupleString)
    #For the coordinate name, we need the underscored version. E.g., (0,0,0) becomes p0_p0_p0
    underScoredCoordinatesString = convertCoordinateToPandNandD(unitCellTuple)    
    coordFullNameElements = [layerName, siteName, underScoredCoordinatesString]
    coordFullName = "___".join(coordFullNameElements)    
    
    if project.software == "kmcos":
        #CoordInput should be a string like 'atop_Ce1.(0,0,0).Layer1', which is the site_name.unit_cell_coordinate.layer.
        #For example, 'atop_O1.(1,0,0).Ce1' would be a site named atop_01, one unit cell to the right, and in the layer Ce1. 
        coordInput = siteName + "." + unitCellTupleString + "." + layerName #looks like: 'atop_Ce1.(0,0,0).Layer1' #This is kmcos syntax.
        newCoord = CIProject.kmcos_project.lattice.generate_coord(coordInput) #This generates the kmcos coordinate.
    #assign the values using coordFullName as keys.
    project.siteDict[coordFullName]= newCoord
    project.siteTypeDict[coordFullName]=siteName
    return newCoord


#This function converts from p0_p0_n5 to (0,0,-5) for example.
def cartesianCoordinateFromPandNandDtoTuple(cartesianAsPandNandDstring):
    cartesianListOfStrings = cartesianAsPandNandDstring.split("_")
    #temporarily make a list since we can append to that and then convert to tuple after.
    cartesianList = []
    for cartesianValueString in cartesianListOfStrings:
        cartesianValue = convertNumberFromPandNandD(cartesianValueString)
        cartesianList.append(cartesianValue)
    cartesianTuple = tuple(cartesianList)
    return cartesianTuple
    
#This function calls the "addSite" function from above, and just takes the arguments in a different way then parses them etc.
def addSiteDistinct(coordFullNameOfSite, project=None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.
    coordFullNameOfSiteList = coordFullNameOfSite.split("___")
    #Need to conver the unit cell cartesian cooridnates into a tuple.
    layerName=coordFullNameOfSiteList[0]
    siteType=coordFullNameOfSiteList[1]
    unitCellTupleString = coordFullNameOfSiteList[2]
    #now need to convert unit cell's cartesian coordinates to a tuple.
    unitCellTuple = cartesianCoordinateFromPandNandDtoTuple(unitCellTupleString)
    if project.software == "kmcos":
        addSite(layerName, siteType, unitCellTuple, project = None) # I am intentionally putting "None" so that kmcos project gets called.

def addSiteIfNotThere(coordFullName, project = None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.
    if coordFullName in project.siteDict:
        pass #this means it's already there!
    else: #else, we add it.
        addSiteDistinct(coordFullName, project) 
    
#This function adds a list of surrounding sites to a particular site. If no site distance is provided, it assumes nearest neighbors (distance =1).
#Add surrounding sites requires using the convention of the output of the addSites function.  This means we need to have layer___siteType___unitCellTuple and optional ____distance
#For example: addSurroundingSites("ruo2___cus___p0_p0_p0", ["ruo2___cus___p0_p1_p0","ruo2___cus___p0_n1_p0"] )
# which is the same as addSurroundingSites("ruo2___cus___p0_p0_p0___1", ["ruo2___cus___p0_p1_p0","ruo2___cus___p0_n1_p0"] )
def addSurroundingSites(coordFullNameOfSiteWithDistance, coordFullNamesOfSurroundingSitesAtDistance, project=None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.
    
    try:
        distance = coordFullNameOfSiteWithDistance.split("___")[3] #the distance is the 4th part of the coordFullName
        splitUpCoordFullNameOfSite = coordFullNameOfSiteWithDistance.split("___")[0:3]  #this is to get rid of the distance from the name.
        coordFullNameOfSite = "___".join(splitUpCoordFullNameOfSite)

    except: #if that doesn't work due to the name not being long enough, then we use the default of nearest neighbors by making it 1.
        distance = 1
        coordFullNameOfSite = coordFullNameOfSiteWithDistance #we assume that the string has no distance at end if it didn't get past the try statement.
        #then we add the distance at the end.
        coordFullNameOfSiteWithDistance = coordFullNameOfSiteWithDistance + "___" + str(distance)
    
    #Some warnings in case a person tries to give the wrong argument type:
    if type(coordFullNameOfSiteWithDistance) !=str:
        raise Exception("WARNING: addSurroundingSites is supposed to receive coordFullNameOfSite as a string, and coordFullNamesOfSurroundingSitesAtDistance as a list of strings.")
    if type(coordFullNamesOfSurroundingSitesAtDistance[0]) !=str:
        raise Exception("WARNING: addSurroundingSites is supposed to receive coordFullNameOfSite as a string, and coordFullNamesOfSurroundingSitesAtDistance as a list of strings.")
        
    #coordFullNamesOfSurroundingSitesAtDistance should be a list of strings. But in case it's not a list, we'll assume it's a signle coordFullName and can put it into the first position of one.
    if type(coordFullNamesOfSurroundingSitesAtDistance)==str:
        coordFullNamesOfSurroundingSitesString = coordFullNamesOfSurroundingSitesAtDistance
        coordFullNamesOfSurroundingSitesAtDistance= [coordFullNamesOfSurroundingSitesString]
    
    #Make local variable for convenience.
    surroundingSitesDict = project.surroundingSitesDict
    #Append to it the list within the approprite key. Note: one could use sets or some other trick to make sure that duplicates don't appear during this appending. For now, I'm not going to worry about that.
    surroundingSitesDict[coordFullNameOfSiteWithDistance] = coordFullNamesOfSurroundingSitesAtDistance
    #now, at the end, we will check that both the central site and other sites exist, and add them if they don't.
    addSiteIfNotThere(coordFullNameOfSite, project)
    for surroundingSiteCoordFullName in coordFullNamesOfSurroundingSitesAtDistance:
        addSiteIfNotThere(surroundingSiteCoordFullName)

def autoAddSurroundingSites(coordFullNameOfSite, upToDistance,  project = None):
    #The "upToDistance" *must* be specified, but you can specify it larger than you need without causing a bug, so "3" is a reasonable choice for many applications.
    #The function was originally designed to take a single central site, but I realized that I could use it recursively if it receives a list. So now it does that also.
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.    
    if isinstance(coordFullNameOfSite, list):
        coordFullNameOfSitesList = coordFullNameOfSite #if the first argument is actually a list, we'll iterate across that list.
        for coordFullName in  coordFullNameOfSitesList:
            autoAddSurroundingSites(coordFullName, upToDistance)
    else: #else we got a single item, and undergo our normal behaviour.
        siteLayerName = extractSiteLayerName(coordFullNameOfSite) 
        siteType = extractSiteType(coordFullNameOfSite)
        siteUnitCellCoordinateInPND = extractSiteUnitCellCoordinateInPND(coordFullNameOfSite)
        siteUnitCellCoordinateInTuple = extractSiteUnitCellCoordinateInTuple(coordFullNameOfSite)
        translationVector = getTranslationVector((0,0,0),siteUnitCellCoordinateInTuple) #in this case, we only care about distance relative to native unit cell.
        nativeUnitCellCoordFullName = "___".join([siteLayerName, siteType, "p0_p0_p0"])
        #now, we get the unit cell equivalent coordFullName and look up the surrounding Sites for it.
        #We need to do this for each distance until we run out of distances. I'm capping this with an upToDistance rather than having a while loop.
        #I'm forcing the user to specify the upToDistance.
        for distance in range(1,upToDistance+1):
            coordFullNameOfSiteWithDistance = coordFullNameOfSite+"___"+str(distance)
            nativeUnitCellCoordFullNameWithDistance = nativeUnitCellCoordFullName+"___"+str(distance)
            try:
                nativeUnitCellSurroundingSites = project.surroundingSitesDict[nativeUnitCellCoordFullNameWithDistance]
                translatedSurroundingSites = []
                for surroundingSiteCoordFullName in nativeUnitCellSurroundingSites:
                    translatedSurroundingSiteCoordFullName = getTranslatedCoordFullname(surroundingSiteCoordFullName, translationVector)
                    translatedSurroundingSites.append(translatedSurroundingSiteCoordFullName)
                addSurroundingSites(coordFullNameOfSiteWithDistance, translatedSurroundingSites, project)
            except:
                print(("Warning: autoAddSurroundingSites could not create a surroundingSitesDict entry for " + coordFullNameOfSite + " at distance of " + str(distance) + " because there is no entry for surrounding sites of " + nativeUnitCellCoordFullName + " at that distance."))
                translatedSurroundingSites = []

def getTranslatedCoordFullname(coordFullName, translationVector):
    siteLayerName = extractSiteLayerName(coordFullName) 
    siteType = extractSiteType(coordFullName)
    siteUnitCellCoordinateInPND = extractSiteUnitCellCoordinateInPND(coordFullName)
    siteUnitCellCoordinateInTuple = extractSiteUnitCellCoordinateInTuple(coordFullName)
    translatedSiteUnitCellCoordinateInTuple = applyTranslationVector(siteUnitCellCoordinateInTuple, translationVector)
    translatedSiteUnitCellCoordinateInPND = convertCoordinateToPandNandD(translatedSiteUnitCellCoordinateInTuple)
    translatedSiteCoordFullName = "___".join([siteLayerName, siteType, translatedSiteUnitCellCoordinateInPND])
    return translatedSiteCoordFullName
    
def conditionPairToCondition(conditionPair, conditionType = "Condition", project = None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.    
    #The "type" can be "Condition" or "Action" or "Bystander"
    #print "inside condition pair converter", conditionPair
    if type(conditionPair[0]) == str: #This comparison will return an error if the object is already coordinate.
             conditionCoord = project.siteDict[str(conditionPair[0])]
    else: #else, we assume it's already a coordinate:
        conditionCoord = conditionPair[0]
    # now, we need to make a condition object: 
    if project.software == "kmcos":
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

def retrieveTransitionFrequency(processTypeString, project = None, type = "kmcos"):  
    #Here, we don't use the processName which is like pF18p0.  We just use the processTypeString, which is like F18p0. 
    #I probably need to think of a better name than "processTypeString"
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.    
    if project.software == "kmcos": #As currently written, this function returns a string, designed for kmcos.
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
        
        #We *do* expect things to be in eV, when using kmcos. The "-1" is for "-Ea", and is kept as a separate term to avoid bugs.
        transitionFrequency = A + '*exp(beta*(-1)*('+ Ea + ')*eV)'
        return transitionFrequency
    
    
def addAProcess(processName, conditionsListAsTuples, actionsListAsTuples, bystandersListAsTuples = None, individualTOFDict = True, rxnNumberTOFDict = True, additionalTOFDict=None, baseTransitionFrequency = 'retrieve',  otfTransitionFrequency= '0', project = None):    
#Note: a suffix like "_01" and "_03" etc. is expected at the end of the processName. That will not cause bugs here, but that's the kmcos package convention as of 9/11/17.
#NOTE: By default, the process name expects something like 'pF8p7' which would mean the forward direction of reaction 8.7.
#The baseTransitionFrequency and otfTransitionFrequency must be strings. That string can be '4.0' for example, or something like '5.0*(P_CO)**2'
#The otfTransitionFrequency can be either a different value from the baseTransitionFrequency, or a string that can be evaluated based on kmcos parameters.
#It *does* require having a table of BEP relations parameters *and* a table of interaction energies, in the forms of dictionaries.
#Unlike Juan's code, we will use 'eval' the way myself and Tom did. That way, the words "coord=" and "species=" etc. do not need to be included as the arguments for this function.
#NOTE: The bystandersListAsTuples is currently being fed as a bystandersList since this is allowed by my code below and is easier.    
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.

    tofDict = None #initialize tofDict as none, only add to it it needs to be added.
    
    processTypeString = processName.split("_")[0][1:] #For this syntax, it gets split and then we take the 0 index of the split thing: so that pF18p0_5 becomes pF18p0. After that, the [1:0] drops the first character to make it F18p0.
    rxnName = processTypeString[1:]
    if baseTransitionFrequency == 'retrieve':
        baseTransitionFrequency = retrieveTransitionFrequency(processTypeString, project)
    
    if individualTOFDict == True: #by default, will add a tofDict for that process name. But people can also remove that if they put "None". They can also provide a more complex tofDict.        
        if tofDict == None:
            tofDict = {}
        tofDict.update({processName[2:]:1})

    if rxnNumberTOFDict == True:
        if additionalTOFDict == None:
            additionalTOFDict = {} #need to make it a dictionary if it is "None".
        additionalTOFDict.update({processTypeString : 1})
        
    if additionalTOFDict != None:
        if tofDict == None:
            tofDict = {}
        tofDict.update(additionalTOFDict)
    
    #First check if somebody tried to feed a conditionsList or actionsList directly. If so, we'll take it and skip the conversion:
    if isinstance(conditionsListAsTuples[0], Condition):
        conditionsList = conditionsListAsTuples
    else: #With the expected arguments, it will go in here and create the conditions list.
        conditionsListAsTuples = checkListAsTuples(conditionsListAsTuples)
        #now create the correctly formatted conditions list, and same thing for actionsList and bystandersList
        conditionsList = conditionPairsToConditionsList(conditionsListAsTuples, "Condition")
    
    #First check if somebody tried to feed a conditionsList or actionsList directly. If so, we'll take it and skip the conversion:
    if isinstance(actionsListAsTuples[0], Action):
        actionsList = actionsListAsTuples
    else:
        actionsListAsTuples = checkListAsTuples(actionsListAsTuples)
        #now create the correctly formatted conditions list, and same thing for actionsList and bystandersList
        actionsList = conditionPairsToConditionsList(actionsListAsTuples, "Action")
    
    #bysttandersList might not work, because there may not be a "Bystander" type in kmcos, if it's old kmcos. Also, the list might just be "None".
    if bystandersListAsTuples == None:
        bystandersList = None
    else:
        try:
            if isinstance(bystandersListAsTuples[0], Bystander):
                bystandersList = bystandersListAsTuples
            else:
                bystandersListAsTuples = checkListAsTuples(bystandersListAsTuples)
                #now create the correctly formatted conditions list, and same thing for actionsList and bystandersList
                bystandersList = conditionPairsToConditionsList(bystandersListAsTuples, "Bystander")
        except:
            bystandersList = None
    
    #now to add processes. First case, don't need otf if there are no bystanders:
    if bystandersList == None:
        temporary_kwargs_dictionary = {"name": processName, "conditions" : conditionsList, "actions" : actionsList, "rate_constant" : baseTransitionFrequency,  "tof_count" : tofDict}
    else:        
        temporary_kwargs_dictionary = {"name": processName, "conditions" : conditionsList, "actions" : actionsList, "bystander_list": bystandersList, "rate_constant" : baseTransitionFrequency,  'otf_rate': otfTransitionFrequency , "tof_count" : tofDict}

    #in any of the cases, we ultimately need to add the process:
    if project.software == "kmcos":
        CIProject.kmcos_project.add_process(**temporary_kwargs_dictionary)
    return

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

#as of 9/13/17 some additional arguments still need  to be added regarding how base energies are calculated and how activation energies are calculated (BEP versus other methods),  to be passed on to the  functions inside.    
def addAProcessIncludingNeighbors(baseProcessName, baseconditionsListAsTuples, baseactionsListAsTuples, individualTOFDict=False, rxnNumberTOFDict = True, additionalTOFDict=None, baseTransitionFrequency = 'retrieve',  otfTransitionFrequency= '0', useOtf=False, includeNeighboringInteractions = True, project = None, interactionModel="pairwise", Ea_prediction_type="BEP", upToDistance=1):
    #individualTOFDict = True means that you would have a TOF for *each* and every process. 
    #rxnNumberTOFDict requires expecting a regular expression with Savara's nomenclature. That means that "pF8p7" would mean forward reaction 8.7.  The p is for process. But this way you would get R8p7 as an entry in the tofDict.
    #It is also useful to make the base process name have a suffix like _5 etc. to be useful with some other kmcos statistics parsing. So pF8p7_1 and then increment the 1 if you have variations of the same reaction (like for different configurations).
    #includeNeighboringInteractions will consider *all* of the surroundingSitesDict for each of the base conditions and each of the actions, along with a BEP relation or other way of determining activation energies.
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.

    #First make the "standard" entries in TOF dict, since that is easy enough.
    processTypeString = baseProcessName[1:] #This is like pF18p0, and includes the direction. (F is for forward)
    rxnName = baseProcessName[2:] #This is like 18p0 and does not include the direction.
    if baseTransitionFrequency == 'retrieve':
        baseTransitionFrequency = retrieveTransitionFrequency(processTypeString, project)
    
    #We will need this site list to remove common elements. This is true regardless of whether we're using otf or not.
    baseConditionsSiteList =[]
    for baseConditionTuple in baseconditionsListAsTuples:
        baseConditionsSiteList.append(baseConditionTuple[0]) #index 0 is the site name, which we need here.
    
    if useOtf==True:    #We don't need all of the possibilities in this case, just the species that can exist in any particular surrounding site.
        #for the baseProcessName, we only need to gather the Bystander objects of each surrounding site, which consists of coordinates and their allowed_species. That's it! And eliminate double counting....
        bystandersList = []
        for baseConditionTuple in baseconditionsListAsTuples: #in baseConditionTuple, index 0 is the coordFullName and index 1 is the species occupying it.
            sitesSurroundingThisSite = project.surroundingSitesDict[baseConditionTuple[0]+"___1"] #Note: This line of code is deprecated.
            truncatedSitesSurroundingThisSite = removeCommonElements(sitesSurroundingThisSite, baseConditionsSiteList)
            #now need to create the Bystander object for each surrounding site.
            for surroundingSiteCoordFullName in truncatedSitesSurroundingThisSite:
                siteType = extractSiteType(surroundingSiteCoordFullName)
                allowed_species_list = project.possibleParticlesForSiteTypes[siteType]
                coordObject = project.siteDict[surroundingSiteCoordFullName]
                bystanderObject = Bystander(allowed_species=allowed_species_list, coord=coordObject)
                if bystanderObject not in bystandersList: #This line is to make sure that the bystander doesn't exist, since surrounding sites can overlap and in this code we didn't account for that (for useOtf=False we did need to account for that earlier in the process...)
                    bystandersList.append(bystanderObject)        
    
        #TODO: finish function for getOtfBystanderAffectedTransitionFrequency(baseTransitionFrequency, processTypeString, interactionModel="pairwise", Ea_prediction_type="BEP", project = None)
        otfTransitionFrequency = getOtfBystanderAffectedTransitionFrequency(baseTransitionFrequency, processTypeString, interactionModel, Ea_prediction_type, project)
        #only need to call "addAProcess" one time when using otf. Sending the bystandersList as a list,and not as tuples.
        addAProcess(baseProcessName +"_0", baseconditionsListAsTuples, baseactionsListAsTuples, bystandersList, individualTOFDict = individualTOFDict, additionalTOFDict =additionalTOFDict, baseTransitionFrequency = baseTransitionFrequency,  otfTransitionFrequency= otfTransitionFrequency, project = project)
    
    if useOtf==False:
    #Now we already have the baseconditionsListAsTuples, and the baseactionsListAsTuples, but need to create a configuration *for each* possibility, and add a process for each possibility.
    #We already have a function for getting all the surrounding possibilities.
        aggregateSurroundingSitesList = getAggregateSurroundingSitesList(baseConditionsSiteList, upToDistance, project)
        #we are going to pass an optional argument into the getAllSurroundingPossibilities function that allows us to give it definedSurroundingSites argument.
        #Note, Sep 14 2017: getAllSurroundingPossibilities can take anything as first argument when definedSurroundingSites is provided. We have a "Todo" to change that to a separate function which gets called by getAllSurroundingPossibilities, but it's not done yet.
        bystandersPossibilitiesList = getAllSurroundingPossibilities(None, definedSurroundingSites = aggregateSurroundingSitesList, project = project)
        #now, for each of these bystanderPossibilities, we need to make a new condition, and add it to the conditionsList along with the new rate_constant.
        if len(bystandersPossibilitiesList) ==0:
            #If there are no bystandersPossibilitiesList (for example, when distance is set to 0) then we just call addAProcess without changing any of our arguments, and there is only one possibility.
            possibilityNumber = 1
            conditionsListAsTuples = baseconditionsListAsTuples
            bystanderAffectedTransitionFrequency = baseTransitionFrequency
            addAProcess(baseProcessName +"_" + str(possibilityNumber), conditionsListAsTuples, baseactionsListAsTuples, individualTOFDict = individualTOFDict, rxnNumberTOFDict = rxnNumberTOFDict, additionalTOFDict =additionalTOFDict, baseTransitionFrequency = bystanderAffectedTransitionFrequency, project = project)
        for index, possibility in enumerate(bystandersPossibilitiesList):
            conditionsListAsTuples = [] #This is going to be all conditions, both base conditions and bystander possibility.
            conditionsListAsTuples.extend(baseconditionsListAsTuples)
            conditionsListAsTuples.extend(possibility)
            surroundingPossibilityAsTuples = possibility
            #add in a call to "calculate rate constant" function which takes baseconditionsListAsTuples, baseactionsListAsTuples, surroundingPossibilityAsTuples
            bystanderAffectedTransitionFrequency = getBystanderAffectedTransitionFrequency(baseTransitionFrequency, baseconditionsListAsTuples, baseactionsListAsTuples, surroundingPossibilityAsTuples, processTypeString, interactionModel=interactionModel, Ea_prediction_type=Ea_prediction_type, project = project)
            #note that we are effectively changing the baseTransitionFrequency to be the bystanderAffectedTransitionFrequency when we are not using otf.
            possibilityNumber = index+1 #we don't start at 0 for this suffix.
            #I am putting "None" in the below function call so that it uses the kmcos object.
            addAProcess(baseProcessName +"_" + str(possibilityNumber), conditionsListAsTuples, baseactionsListAsTuples, individualTOFDict = individualTOFDict, rxnNumberTOFDict = rxnNumberTOFDict, additionalTOFDict =additionalTOFDict, baseTransitionFrequency = bystanderAffectedTransitionFrequency, project = None) 
            

#Below Should Be a Function to Return the Aggregate Surrounding Sites List for a Given Set of Base Conditions, OR Potentially Base Sites.
def getAggregateSurroundingSitesList(baseConditionsSiteListProvided, upToDistance = 1, project = None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.
    #If it's bunch of tuples, we will assume it's a bunch of coordinate tuples and can use zip(*listLikeItemsList)[0] to extract index 0 of each item in the list.
    if isinstance(baseConditionsSiteListProvided[0],tuple): 
        baseConditionsSiteList = list(zip(*baseConditionsSiteListProvided))[0]
    else:
        baseConditionsSiteList = baseConditionsSiteListProvided
    aggregateSurroundingSitesList = []
    for baseConditionSite in baseConditionsSiteList: 
        #need to pull out the sites for *each* distance.
        sitesSurroundingThisSite =[] #need to make a blank list first, and then extend it for each distance.
        for distance in range(1,upToDistance+1):
            try:
                sitesSurroundingThisSite.extend(project.surroundingSitesDict[baseConditionSite + "___" + str(distance)]) 
            except:
                sitesSurroundingThisSite.extend([]) #if there are no sites at that distance, just extend by a blank list, which does nothing.
                print(("Warning: you requested a surrounding site distance of upToDistance " + str(upToDistance) + " for a process with " + baseConditionSite + " but there is no surrounding site definition at distance " + str(distance)))
        truncatedSitesSurroundingThisSite = removeCommonElements(sitesSurroundingThisSite, baseConditionsSiteList)            
        #We don't want to add sites to the list that already exist. If there are 2 or more conditions, they could have some surrounding sites that overlap. So we remove common elements prior to extending. Based on how that function works, we want to send the first argument as the list that we want to have popping occur from.
        truncatedSitesSurroundingThisSite = removeCommonElements(truncatedSitesSurroundingThisSite, aggregateSurroundingSitesList)            
        aggregateSurroundingSitesList.extend(truncatedSitesSurroundingThisSite)
    return aggregateSurroundingSitesList

def calculateTotalInteractionTerm(baseconditionsListAsTuples, surroundingPossibilityAsTuples, interactionModel="pairwise", project = None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.
    #we use project.interactionTermsDict, but in principle somebody could do things differently.
    totalInteractionTerm = 0.0
    if interactionModel == "pairwise":
        #go over each base condition, and for eachSiteOccupationTuple we'll get that pairwise interaction term, then add it to the total one.
        for baseConditionTuple in baseconditionsListAsTuples:
            for eachSiteOccupationTuple in surroundingPossibilityAsTuples:
                thisClusterList = [baseConditionTuple, eachSiteOccupationTuple] #we are doing only pairs for our cluster in pairwise, but the same "strategy" of making a list here would work for larger clusters.
                #note that we use the "getInteractionTerm" function rather than trying to call the dictionary directly, this is because there is a sorting that occurs inside that function.
                totalInteractionTerm = totalInteractionTerm + float(getInteractionTerm(thisClusterList, project))
    return totalInteractionTerm
        

def getBystanderAffectedTransitionFrequency(baseTransitionFrequency, baseconditionsListAsTuples, baseactionsListAsTuples, surroundingPossibilityAsTuples, processTypeString, interactionModel="pairwise", Ea_prediction_type="BEP", project = None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.    
    if interactionModel=="pairwise":
        reactantInteractionTerm = calculateTotalInteractionTerm(baseconditionsListAsTuples, surroundingPossibilityAsTuples, interactionModel="pairwise") 
        productInteractionTerm = calculateTotalInteractionTerm(baseactionsListAsTuples, surroundingPossibilityAsTuples, interactionModel="pairwise")         
    if Ea_prediction_type=="BEP": #We only need the new enthalpy for rxn, and the original rate constant.
        changeInDeltaH = productInteractionTerm - reactantInteractionTerm
        thisBEPRelation = getBEPRelation(processTypeString) #processTypeString is like F18p0, you need the direction for BEP.
        changeInEa  = thisBEPRelation.changeInEaFromChangeInDeltaH(changeInDeltaH)
        newTransitionFrequency = thisBEPRelation.newRateConstantFromChangeInEaString(baseTransitionFrequency, changeInEa, 'T', EaUnits = "eV")
    return newTransitionFrequency 
    # desiredEa = BEPrelation #with name of the particular relation.... perhaps reaction naming system needed... too...like CO_O_empty... interactionEa

def getBEPRelation(processTypeString, project = None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.
    #below lines are not interesting, you should skip ahead.
    if processTypeString[0] == "F":  #expect something like F18p0
        reverseProcessTypeString = "R" + processTypeString[1:] #reverseProcessTypeString would be R18p0 in that case.
    if processTypeString[0] == "R":
        reverseProcessTypeString = "F" + processTypeString[1:]    
    #Here we try to get the BEP relation. But frequently, on the forward direction exists. In that case, we create the reverse relation (and store it).
    if processTypeString in project.BEPRelationsDict:
        thisProcessBEPrelation = project.BEPRelationsDict[processTypeString] #
        return thisProcessBEPrelation 
    elif reverseProcessTypeString in project.BEPRelationsDict: #here, we are checking if the reverse direction BEP exists.
        #if it exists, we grab it.
        reverseProcessBEPrelation = project.BEPRelationsDict[reverseProcessTypeString] #
        #then, we "reverse it" to get the BEP relation for this process.
        thisProcessBEPrelation = reverseProcessBEPrelation.getReverseRelation()
        #then, we return it.
        return thisProcessBEPrelation 
    else:
        raise Exception("There was no BEP relation found for" +processTypeString + "nor for the reverse process.")
    
def getOtfBystanderAffectedTransitionFrequency(baseTransitionFrequency, processTypeString, interactionModel="pairwise", Ea_prediction_type="BEP", project = None):
    #note that the conditions and the actions and the possibilities are not needed: that is what the on the fly part will do.
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.    
    raise Exception("We cannot do otf BEP, at present. Because we need both reactant state and product state configuration. Currently, the otf does not provide the product state configuration.")
    # if interactionModel=="pairwise":
        # reactantInteractionTerm = calculateTotalInteractionTerm(baseconditionsListAsTuples, surroundingPossibilityAsTuples, interactionModel="pairwise") 
        # productInteractionTerm = calculateTotalInteractionTerm(baseactionsListAsTuples, surroundingPossibilityAsTuples, interactionModel="pairwise")         
    # if Ea_prediction_type=="BEP": #We only need the new enthalpy for rxn, and the original rate constant.
        # changeInDeltaH = productInteractionTerm - reactantInteractionTerm
        # import BEPmodule
        # try:
            # BEPrelation = getBEPrelation(rxnName)
        # except:
            # BEPrelation = BEPmodule.BEPrelation() #THIS LINE IS PRIMARILY FOR TESTING PURPOSES
        # changeInEa  = BEPrelation.changeInEaFromChangeInDeltaH(changeInDeltaH)
        # newTransitionFrequency = BEPrelation.newRateConstantFromChangeInEaString(baseTransitionFrequency, changeInEa, 200, EaUnits = "eV")
    # return newTransitionFrequency 
    # desiredEa = BEPrelation #with name of the particular relation.... perhaps reaction naming system needed... too...like CO_O_empty... interactionEa


def autoAddInteractionTerms(configurationPossibility, InteractionTermValue, aggregateBaseConditionsSitesList = None, project = None):
    #To use this feature, the first condition pair MUST be in the native unit cell (0,0,0), but the later conditon pairs do not have to be.
    #Your base aggregateBaseConditionsSitesList also can contain sites outside of the native unit cell.
    #this function will search inside of aggregateBaseConditionsSitesList  for any other sites  that are of the same site type,
    #and then it will use translational symmetry  to make the corresponding interaction terms for those sites.
    #this means that you only need to define left, right, up etc. for the native unit cell (0,0,0) and not the surrounding cases.
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.    
    if aggregateBaseConditionsSitesList == None:
        aggregateBaseConditionsSitesList = project.aggregateBaseConditionsSitesList
    referenceSiteFromConfigurationPossibility = configurationPossibility[0][0] #first term in first conditionPair
    siteTypeOfReferenceSiteFromConfigurationPossibility = extractSiteType(referenceSiteFromConfigurationPossibility)
    for baseConditionSiteCoordFullName in aggregateBaseConditionsSitesList: #iterate across each aggregateBaseConditionsSite to see compare site types (which will occur below)
        siteTypeOfBaseConditionSite = extractSiteType(baseConditionSiteCoordFullName)
        if siteTypeOfBaseConditionSite == siteTypeOfReferenceSiteFromConfigurationPossibility: #check if they are the same site type, then we do the translation to create the analagous interaction terms.
            foundSiteCoordFullName = baseConditionSiteCoordFullName
            foundSiteUnitCellCoordinateInTuple = extractSiteUnitCellCoordinateInTuple(foundSiteCoordFullName)
            translationVector = getTranslationVector((0,0,0),foundSiteUnitCellCoordinateInTuple) #in this case, we only care about distance relative to native unit cell.
            #now that we have the translation vector, we can get the translated configuration possibility by applying it to each item in the original configurationPossibility.
            translatedConfigurationPossibility = []
            for conditionPair in configurationPossibility:
                #conditionPair[0] is the coordFullName, and we will translate it based on the translationVector.
                translatedConditionPairCoordFullName = getTranslatedCoordFullname(conditionPair[0], translationVector)
                translatedConditionPairOccupation = conditionPair[1] #the occupation (i.e., species) does not change.
                translatedConditionPair = (translatedConditionPairCoordFullName, translatedConditionPairOccupation)
                translatedConfigurationPossibility.append(translatedConditionPair)
            addInteractionTerm(translatedConfigurationPossibility, InteractionTermValue, project)
         #once we've found any of the conditionPairs, we've found a unique configuration and translated it so we don't need to check further.


def addInteractionTerm(configurationPossibility, InteractionTermValue, project = None):
    #The configurationPossibility should include the central species. Not just the surrounding sites. It's a list of tuples, like this:
    # configurationPossibility = [("ruo2___cus___p0_p0_p0", "CO"), ("ruo2___cus___p0_p1_p0", "empty")]
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.    
    #Because we want all combinations of that possibility to have the same key value, we're going to *first* sort the configurationPossibility, even though that means the central species will not be central anymore.
    #First we convert configurationPossibility into a list, just in case it was provided as a tuple.
    SortedConfigurationPossibility = sorted(list(configurationPossibility))
    #now we add it to the dictionary, which requires using a tuple as the key instead of a list:
    project.interactionTermsDict[tuple(SortedConfigurationPossibility)]= InteractionTermValue

def getInteractionTerm(configurationPossibility, project = None):
    if project == None:
        project = CIProject #What I have done here is set CIProject to be a "default" when no argument is provided. But it only works when that variable is defined globally in this module.    
    
    #We first need to sort the configurationPossibility since the keys of the interactionTermsDict are always sorted:
    #First we convert configurationPossibility into a list, just in case it was provided as a tuple.
    SortedConfigurationPossibility = sorted(list(configurationPossibility))
    #now we can retrieve the value:
    try:    
        InteractionTermValue = project.interactionTermsDict[tuple(SortedConfigurationPossibility)]
    except: #if that value does not exist, then we will return 0.0.
        InteractionTermValue = 0.0
        #TODO: FIXME: Get this warning below to work better.
        #warnings.warn("Warning: No interaction term exists for the following configurationPossibility, so a value of 0.0 is being used:" + str(configurationPossibility) + "\n If there was a value in the interactionTermsDict for the above configuration, it would be under this key:" + str( tuple(SortedConfigurationPossibility)))
    return InteractionTermValue
    
if __name__ == '__main__':
 
        #Below are some unit tests. But they require kmcos for some of them. 
    print(convertNumberToPandNandD(-5))
    print(convertCoordinateToPandNandD((0,0,0)))
    
    Ce_1_p0_p0_p0 = addSite("Ce1", "atop_Ce1", "(0,0,0)")
    Ce_1_p0_p0_p0 = addSite("Ce1", "atop_Ce2", "(0,0,0)")
    print(siteDict)
    print(siteTypeDict)
    
    O_sites_surrounding_O = [0, \
                    [1,'O_1_p1_p0_p0','O_2_p0_p0_p0','O_2_n1_p0_p0','O_1_n1_p0_p0','O_2_n1_n1_p0','O_2_p0_n1_p0'],   \
                    [2,'O_2_p1_p0_p0','O_1_p1_p1_p0','O_1_p0_p1_p0','O_2_n1_p0_p0','O_1_p0_p0_p0','O_1_p1_p0_p0']    \
                ]
    set_of_sites = O_sites_surrounding_O[x][1:7]
    PossibleAdsorbatesForSiteTypes = {}
    PossibleAdsorbatesForSiteTypes['atop_O2']=["empty", "filled_CO"]
    PossibleAdsorbates = PossibleAdsorbatesForSiteTypes['atop_O2']
    siteOccupationPossibilities = getSiteOccupationPossibilities(set_of_sites, PossibleAdsorbates)
    conditionsLists = getConditionsListsFromSitePossibilities(siteOccupationPossibilities, "Condition")
    actionsLists = getConditionsListsFromSitePossibilities(siteOccupationPossibilities, "Action")
    print(conditionsLists[63], siteOccupationPossibilities[63])
    print(len(conditionsLists))
    if actionsLists[0]==conditionsLists[0]:
        print("interesting")