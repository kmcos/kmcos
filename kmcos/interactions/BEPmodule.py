#this class is for BEP  relation objects.
#The reason to have a class is because then we can make functions inside of it and also data structures.
# we can have a person provide a bunch of Ea and DeltaHRxn points,  and then they can apply a class function to fit it.
#they can then also use a function to predict the Ea under other conditions etc.
#one thing to note is that a BEPrelation can be defined by alpha and beta, or by DeltaHRxn and "alpha" (through using E0 in the derivation, which is the activation energy when the DeltaHRxn happens to be 0).
#  this class requires alpha and beta to be provided to create a BEP relation object,  but it should later have a function added that can be used to make an object using DeltaHRxn and alpha.

#TODO: create function to make a BEPrelation object from DeltaHRxn and alpha.  



#To convert from J/molK to eV, you take ValueInJ/101/1000/6.02E23 = ValueInEv    
def J_to_eV(value_in_J): #actually J/molK.
    value_in_eV = value_in_J/96.485/1000
    return value_in_eV

#So to convert from eV to J/molK
def eV_to_J(value_in_eV):
    value_in_J = value_in_eV*1000*96.485
    return value_in_J
    
class BEPRelation:
    def __init__(self, alpha=0.5, beta=0.0):
        self.alpha = alpha
        self.beta = beta
    
    def __call__(self): #if you have a BEP relation called "BEPrelation_123" then typing "BEPrelation_123()" will return a tuple of alpha,beta.
        return (self.alpha, self.beta)
    
    def getReverseRelation(self):
        #From dx.doi.org/10.1021/cs3003269, alpha becomes 1-alpha and beta remains unchanged.
        reverseRelation = BEPRelation(1-self.alpha, self.beta)
        return reverseRelation
    
    def EaFromDeltaH(self, DeltaH):
        Ea = self.alpha * DeltaH + self.beta
        return Ea
        
    def DeltaHfromEa(self, Ea):
        DeltaH  = (Ea - + self.beta)/self.alpha 
        return DeltaH 
     
    def changeInEaFromChangeInDeltaH(self, changeInDeltaH):
        changeInEa = self.alpha*changeInDeltaH
        return changeInEa # The algebra comes out to (Ea_2 - Ea_1) = alpha(DeltaH_2 -DeltaH_1), as shown in 0-BEPfromJustInteractionTermsAndEa.pdf
        
    def newRateConstantFromChangeInEa(self, originalRateConstant, changeInEa, Temperature, EaUnits = "eV"):
        #temperature must be in K. Currently, only supports EaUnits of J / mol K, but that can be changed easily.
        #Basically, the ideal gas constant has to match the EaUnits.
        #see file 0-BEPrateConstantFromChangeInEa.pdf for derivation.
        #EaUnits can also be "eV".        
        originalRateConstant = float(originalRateConstant) #this is mainly because sometimes we receive a string or something.
        if EaUnits == "eV":
            changeInEa = eV_to_J(changeInEa) #actually becomes J/molK.
        R = 8.3145
        import math
        #Note: I am not sure if it's better to do it by using "R" or "k" in the denominator, in order to prevent numerical errors. 
        #Anyway, for me it's easier to convert from eV to J/molK.  1 eV = 96.485 kJ/mol, and 1 kJ/mol = 0.010364 eV
        newRateConstant = originalRateConstant * math.exp(-changeInEa/(R*Temperature))
        return newRateConstant
    
    def newRateConstantFromChangeInEaString(self, originalRateConstant, changeInEa, Temperature, EaUnits = "eV"):
        #this is designed for kmos and returns a string that can be evaluted during runtime. In kmos, the string "eV" represents a constant of ~1.60E-19.
        if EaUnits == "eV":
            newRateConstantAsString = originalRateConstant + "*exp(-beta*("+str(changeInEa)+")*eV)" #we need parenthesis around the changeInEa string because it could be negative, so *(-xxx)* for the syntax.
        return newRateConstantAsString