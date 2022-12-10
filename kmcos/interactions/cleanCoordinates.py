import numpy as np

#This module is intended for sites with names like this: ruo2___bridge___p1_p0_p0 which is layerName___siteType___UnitCellCoordinateInPND, and the p1_p0_p0 means (1,0,0)
# It also supports neighboring sites of different distances.  ruo2___bridge___p1_p0_p0___4 would mean fourth nearest neighbor distance.
# the distance is actually just a classification, so you could include multiple types of neighbors within that classification. For example, you could put 1st to 3rd neareest neighbors in distance 1, and 10th to 12th nearest neighbors in distance 4.
#The PND notation is to convert numbers into strings. When we have things like 1.0 becomes p0d0 , and -5.0 becomes n5d0


def extractDistance(coordFullNamePlusDistance):
    distance = coordFullNamePlusDistance.split("___")[3] #the neighbor distance is the 4th part of the string.
    return distance

def extractSiteLayerName(coordFullName):
    layerName = coordFullName.split("___")[0] #the layer is the 1st part of the coordFullName
    return layerName
    
def extractSiteType(coordFullName):
    siteType = coordFullName.split("___")[1] #the site name is the 2nd part of the coordFullName
    return siteType

def extractSiteUnitCellCoordinateInPND(coordFullName):
    unitCellCoordinateInPND = coordFullName.split("___")[2] #the unit cell coordinate is the 3rd part of the coordFullName
    return unitCellCoordinateInPND #this is in the PandNandD format.

def extractSiteUnitCellCoordinateInTuple(coordFullName):
    unitCellCoordinateInPND = coordFullName.split("___")[2] #the unit cell coordinate is the 3rd part of the coordFullName
    unitCellCoordinateInTuple = convertCoordinateFromPandNandD(unitCellCoordinateInPND)
    return unitCellCoordinateInTuple
    
def applyTranslationVector(originalCoordinate, translationVector): #this applies a translation.
    import numpy as np
    originalCoordinate = np.array(originalCoordinate)
    translationVector = np.array(translationVector)
    translatedCoordinate = originalCoordinate + translationVector
    return translatedCoordinate #this returns a numpy array, regardless of what you give it.
    
def getTranslationVector(referenceCoordinate, targetCoordinate): #this expects a list, tuple, array, etc., for each.
    import numpy as np
    referenceCoordinate = np.array(referenceCoordinate)
    targetCoordinate = np.array(targetCoordinate)
    translationVector = targetCoordinate - referenceCoordinate
    return translationVector #This returns a numpy array, regardless of what you give it.
    

def convertCoordinateToPandNandD(coordTupleOrList): #Expects something like (0,0,1) and creates something like p0_p0_p1
    stringedCoordTupleOrList = []
    for number in coordTupleOrList:
        stringedCoordTupleOrList.append(convertNumberToPandNandD(number)) #The convertNumberToPandNandD function includes converting to a string.
    #The join function is a bit strange, you normally give it the delimiter then a list to join into a string.
    #The reason it probably makes a bit of sense is you want a string, so using the delimeter as the main object
    #makes it a bit more sensible from an object module point of view rather than making it part of list module.
    underScoredCoordinates = "_".join(stringedCoordTupleOrList)
    return underScoredCoordinates

def convertCoordinateFromPandNandD(underscoredPandNandDCoordinate): #Expects something like p0_p0_p1 and creates something like (0,0,1) 
    listPandNandDCoordinate = underscoredPandNandDCoordinate.split("_")
    listCoordinate = [] #make the list, then populate it.    
    for stringValue in listPandNandDCoordinate:
        number = convertNumberFromPandNandD(stringValue)
        listCoordinate.append(number)
    tupleCoordinate = tuple(listCoordinate)
    return tupleCoordinate

def convertNumberToPandNandD(number): #number can be an integer or a float.
    #TODO: write case for when the number has a decimal point.
    #if the number has no decimal point: 
    if number >= 0:
        stringVersion = 'p' + str(number)
    if number < 0:
        stringVersion = 'n' + str(number)[1:] #This is to remove the negative sign.
    return stringVersion

def convertNumberFromPandNandD(string): #string which is "p1" or "n4.5" etc, meaning 1 and -4.5 in these examples.
    #TODO: write case for when the number has a decimal point.
    #if the string has no "d" for decimal point:
    if string[0]== "p":
        number = int(string[1:])
    if string[0]== "n":
        number = 0 - int(string[1:])
    return number

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

def getTranslatedCoordFullname(coordFullName, translationVector):
    siteLayerName = extractSiteLayerName(coordFullName) 
    siteType = extractSiteType(coordFullName)
    siteUnitCellCoordinateInPND = extractSiteUnitCellCoordinateInPND(coordFullName)
    siteUnitCellCoordinateInTuple = extractSiteUnitCellCoordinateInTuple(coordFullName)
    translatedSiteUnitCellCoordinateInTuple = applyTranslationVector(siteUnitCellCoordinateInTuple, translationVector)
    translatedSiteUnitCellCoordinateInPND = convertCoordinateToPandNandD(translatedSiteUnitCellCoordinateInTuple)
    translatedSiteCoordFullName = "___".join([siteLayerName, siteType, translatedSiteUnitCellCoordinateInPND])
    return translatedSiteCoordFullName