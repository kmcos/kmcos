#!/usr/bin/env python
import kmcos
from kmcos.types import *
from itertools import product
import numpy as np

model_name = str( os.path.basename(__file__)[+0:-3]).replace("__build", "")

kmc_model = kmcos.create_kmc_model(model_name)
kmc_model.set_meta(author='Aditya Ashi Savara',
            email='savaraa@ornl.gov',
            model_name=model_name,
            model_dimension=2)

# Species
kmc_model.add_species(name='empty', color='#ffffff')
kmc_model.add_species(name='CO',
               color='#000000',
               representation="Atoms('CO',[[0,0,0],[0,0,1.2]])")
kmc_model.add_species(name='O',
               color='#ff0000',
               representation="Atoms('O')")

# Layer/Sites
layerName = 'ruo2'
layer = Layer(name=layerName)
layer.sites.append(Site(name='bridge', pos='0.0 0.5 0.7'))
layer.sites.append(Site(name='cus', pos='0.5 0.5 0.7'))
layer.sites.append(Site(name='Burrowed', pos='0.0 0.0 0.0')) #This is for the pace-restrictor reaction

kmc_model.possibleParticlesForSiteTypes['bridge']=['empty', 'CO','O']
kmc_model.possibleParticlesForSiteTypes['cus']=['empty', 'CO','O']

kmc_model.add_layer(layer)

kmc_model.lattice.representation = """[Atoms(symbols='O11Ru6',\n          pbc=np.array([False, False, False], dtype=bool),\n          cell=np.array(\n      [[  6.39 ,   0.   ,   0.   ],\n       [  0.   ,   3.116,   0.   ],\n       [  0.   ,   0.   ,  20.   ]]),\n          scaled_positions=np.array(\n      [[-0.        ,  0.50007885,  0.26035664],\n       [ 0.69420673,  0.        ,  0.31692564],\n       [ 0.30581593,  0.        ,  0.31692564],\n       [-0.        ,  0.50007885,  0.3814254 ],\n       [ 0.50001133,  0.50007885,  0.41721538],\n       [ 0.1941954 ,  0.        ,  0.47926097],\n       [ 0.80582726,  0.        ,  0.47926097],\n       [ 0.50001133,  0.50007885,  0.54130656],\n       [-0.        ,  0.50007885,  0.57696872],\n       [ 0.69420673,  0.        ,  0.63901431],\n       [ 0.30581593,  0.        ,  0.63901431],\n       [-0.        ,  0.        ,  0.31502134],\n       [ 0.50001133,  0.50007885,  0.32362425],\n       [-0.        ,  0.50007885,  0.47926097],\n       [ 0.50001133,  0.        ,  0.47926097],\n       [-0.        ,  0.        ,  0.63901431],\n       [ 0.50001133,  0.50007885,  0.63901431]]))]"""
kmc_model.lattice.cell = np.diag([6.43, 3.12, 20])

# Parameters

kmc_model.add_parameter(name='p_COgas', value=1, adjustable=True, min=1e-13, max=1e2,
                 scale='log')
kmc_model.add_parameter(name='p_O2gas', value=1, adjustable=True, min=1e-13, max=1e2,
                 scale='log')
kmc_model.add_parameter(name='T', value=450, adjustable=True, min=300, max=1500)

kmc_model.add_parameter(name='R_constant', value='8.3145', adjustable=False)

kmc_model.add_parameter(name='A', value='%s*angstrom**2' % (kmc_model.lattice.cell[0,0]*
                                                      kmc_model.lattice.cell[1,1]))
kmc_model.add_parameter(name='E_O_bridge', value=-2.3)
kmc_model.add_parameter(name='E_O_cus', value=-1.0)
kmc_model.add_parameter(name='E_CO_bridge', value=-1.6)
kmc_model.add_parameter(name='E_CO_cus', value=-1.3)

# note that in the below definitions of activation energies we expect things to be in eV.  
# some things have a "(-1)*" in front . that is because the desorption ones are not the elementary step rate constants.
# They have terms that look look like Value1*exp(value2), so for convenience we are using A=Value1 and Ea=-Value2 to achieve Value1*exp((-1)*-Value2) for the same output.
# the adsorption events considered nonactivated in this model.
#you can use an integer or a float, but if you need it to be evaluated in real time or refer to kmos parameters, then you must use a string.
kmc_model.EaDict['EaF1p0'] = 0
kmc_model.EaDict['EaR1p0'] = '(-1)*(E_CO_cus-mu_COgas)' #desorption
kmc_model.EaDict['EaF2p0'] = 0
kmc_model.EaDict['EaR2p0'] = '(-1)*(E_CO_bridge-mu_COgas)' #desorption
kmc_model.EaDict['EaF3p0'] = 0
kmc_model.EaDict['EaR3p0'] = '(-1)*(2*E_O_cus-mu_O2gas)' #desorption
kmc_model.EaDict['EaF4p0'] = 0
kmc_model.EaDict['EaR4p0'] = '(-1)*((E_O_cus+E_O_bridge)-mu_O2gas)' #desorption
kmc_model.EaDict['EaF5p0'] = 0
kmc_model.EaDict['EaR5p0'] = '(-1)*(2*E_O_bridge-mu_O2gas)' #desorption
kmc_model.EaDict['EaF6p0'] = 0
kmc_model.EaDict['EaR6p0'] = '(-1)*((E_O_cus+E_O_bridge)-mu_O2gas)' #desorption
kmc_model.EaDict['EaF7p0'] = 1.7 #'E_COdiff_cus_cus'  #Note that for this reaction and the below reactions, we could have defined the parameter above and then kept the string.
kmc_model.EaDict['EaR7p0'] =1.7 # 'E_COdiff_cus_cus'
kmc_model.EaDict['EaF8p0'] =0.6 # 'E_COdiff_bridge_bridge'
kmc_model.EaDict['EaR8p0'] =0.6 # 'E_COdiff_bridge_bridge'
kmc_model.EaDict['EaF9p0'] = 1.6# 'E_COdiff_bridge_cus'
kmc_model.EaDict['EaR9p0'] = 1.3# 'E_COdiff_cus_bridge'
kmc_model.EaDict['EaF10p0'] = 1.6# 'E_COdiff_bridge_cus'
kmc_model.EaDict['EaR10p0'] = 1.3# 'E_COdiff_cus_bridge'
kmc_model.EaDict['EaF11p0'] = 1.6 #E_Odiff_cus_cus
kmc_model.EaDict['EaR11p0'] = 1.6 #E_Odiff_cus_cus
kmc_model.EaDict['EaF12p0'] = 0.7 #E_Odiff_bridge_bridge
kmc_model.EaDict['EaR12p0'] = 0.7 #E_Odiff_bridge_bridge
kmc_model.EaDict['EaF13p0'] = 2.3 #E_Odiff_bridge_cus
kmc_model.EaDict['EaR13p0'] = 1.0 #E_Odiff_cus_bridge
kmc_model.EaDict['EaF14p0'] = 2.3 #E_Odiff_bridge_cus
kmc_model.EaDict['EaR14p0'] = 1.0 #E_Odiff_cus_bridge
kmc_model.EaDict['EaF15p0'] = 0.9 #E_react_Ocus_COcus
kmc_model.EaDict['EaR15p0'] = 0
kmc_model.EaDict['EaF16p0'] = 0.9 #E_react_Ocus_COcus #reaction
kmc_model.EaDict['EaR16p0'] = 0
kmc_model.EaDict['EaF17p0'] = 0.8 #E_react_Ocus_CObridge #reaction
kmc_model.EaDict['EaR17p0'] = 0
kmc_model.EaDict['EaF18p0'] = 0.8 #E_react_Ocus_CObridge #reaction
kmc_model.EaDict['EaR18p0'] = 0
kmc_model.EaDict['EaF19p0'] = 1.5 #E_react_Obridge_CObridge #reaction
kmc_model.EaDict['EaR19p0'] = 0
kmc_model.EaDict['EaF20p0'] = 1.5 #E_react_Obridge_CObridge #reaction
kmc_model.EaDict['EaR20p0'] = 0
kmc_model.EaDict['EaF21p0'] = 1.2 #E_react_Obridge_COcus #reaction
kmc_model.EaDict['EaR21p0'] = 0
kmc_model.EaDict['EaF22p0'] = 1.2 #E_react_Obridge_COcus #reaction
kmc_model.EaDict['EaR22p0'] = 0
kmc_model.EaDict['EaF150p0'] = 0 #Pace-restrictor reaction.
kmc_model.EaDict['EaR150p0'] = 0 #Reverse of Pace-restrictor reaction.
kmc_model.EaDictToParameters() #Any energy in the EaDict that is not a string gets converted to a kmos object.
#Note: By default, the EaDict expects things in eV. If you want to convert it to J/mol, use the units = "J" argument.
#The optional unit conversion occurs if you put in a number. Otherwise the units argument is ignored.

#I am adding AF2p0 etc. inside so that they can be throttled by the throttling code.
kmc_model.ADict['AF1p0'] = 'AF1p0*p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)'
kmc_model.ADict['AR1p0'] = 'AR1p0*p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)'
kmc_model.ADict['AF2p0'] = 'AF2p0*p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)'
kmc_model.ADict['AR2p0'] = 'AR2p0*p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)'
kmc_model.ADict['AF3p0'] = 'AF3p0*p_O2gas*bar*A/4/sqrt(2*pi*umass*m_O2/beta)'
kmc_model.ADict['AR3p0'] = 'AR3p0*p_O2gas*bar*A/4/sqrt(2*pi*umass*m_O2/beta)'
kmc_model.ADict['AF4p0'] = 'AF4p0*p_O2gas*bar*A/4/sqrt(2*pi*umass*m_O2/beta)'
kmc_model.ADict['AR4p0'] = 'AR4p0*p_O2gas*bar*A/4/sqrt(2*pi*umass*m_O2/beta)'
kmc_model.ADict['AF5p0'] = 'AF5p0*p_O2gas*bar*A/4/sqrt(2*pi*umass*m_O2/beta)'
kmc_model.ADict['AR5p0'] = 'AR5p0*p_O2gas*bar*A/4/sqrt(2*pi*umass*m_O2/beta)'
kmc_model.ADict['AF6p0'] = 'AF6p0*p_O2gas*bar*A/4/sqrt(2*pi*umass*m_O2/beta)'
kmc_model.ADict['AR6p0'] = 'AR6p0*p_O2gas*bar*A/4/sqrt(2*pi*umass*m_O2/beta)'
kmc_model.ADict['AF7p0'] = 'AF7p0*(beta*h)**(-1)'
kmc_model.ADict['AR7p0'] = 'AR7p0*(beta*h)**(-1)'
kmc_model.ADict['AF8p0'] = 'AF8p0*(beta*h)**(-1)'
kmc_model.ADict['AR8p0'] = 'AR8p0*(beta*h)**(-1)'
kmc_model.ADict['AF9p0'] = 'AF9p0*(beta*h)**(-1)'
kmc_model.ADict['AR9p0'] = 'AR9p0*(beta*h)**(-1)'
kmc_model.ADict['AF10p0'] = 'AF10p0*(beta*h)**(-1)'
kmc_model.ADict['AR10p0'] = 'AR10p0*(beta*h)**(-1)'
kmc_model.ADict['AF11p0'] = 'AF11p0*(beta*h)**(-1)'
kmc_model.ADict['AR11p0'] = 'AR11p0*(beta*h)**(-1)'
kmc_model.ADict['AF12p0'] = 'AF12p0*(beta*h)**(-1)'
kmc_model.ADict['AR12p0'] = 'AR12p0*(beta*h)**(-1)'
kmc_model.ADict['AF13p0'] = 'AF13p0*(beta*h)**(-1)'
kmc_model.ADict['AR13p0'] = 'AR13p0*(beta*h)**(-1)'
kmc_model.ADict['AF14p0'] = 'AF14p0*(beta*h)**(-1)'
kmc_model.ADict['AR14p0'] = 'AR14p0*(beta*h)**(-1)'
kmc_model.ADict['AF15p0'] = 'AF15p0*(beta*h)**(-1)/8'
kmc_model.ADict['AR15p0'] = 'AR15p0*None'
kmc_model.ADict['AF16p0'] = 'AF16p0*(beta*h)**(-1)/8'
kmc_model.ADict['AR16p0'] = 'AR16p0*None'
kmc_model.ADict['AF17p0'] = 'AF17p0*(beta*h)**(-1)/8'
kmc_model.ADict['AR17p0'] = 'AR17p0*None'
kmc_model.ADict['AF18p0'] = 'AF18p0*(beta*h)**(-1)/8'
kmc_model.ADict['AR18p0'] = 'AR18p0*None'
kmc_model.ADict['AF19p0'] = 'AF19p0*(beta*h)**(-1)/8'
kmc_model.ADict['AR19p0'] = 'AR19p0*None'
kmc_model.ADict['AF20p0'] = 'AF20p0*(beta*h)**(-1)/8'
kmc_model.ADict['AR20p0'] = 'AR20p0*None'
kmc_model.ADict['AF21p0'] = 'AF21p0*(beta*h)**(-1)/8'
kmc_model.ADict['AR21p0'] = 'AR21p0*None'
kmc_model.ADict['AF22p0'] = 'AF22p0*(beta*h)**(-1)/8'
kmc_model.ADict['AR22p0'] = 'AR22p0*None'
kmc_model.ADict['AF150p0'] = 2.5E2 #This is for the pace-restrictor reaction. I needed to make it NOT A STRING in order to make it a parameter.
kmc_model.ADict['AR150p0'] = 'AF150p0*1E5' #This is for the pace-restrictor reaction's reverse. Tying rate to forward reaction pre-exponential so both would speed up and slow down together based on runfile and throttling code.
kmc_model.add_parameter(name="AR150p0", value=1) #adding the reverse reaction's alleged pre-exponential manually. Needed for throttling code.
kmc_model.ADictToParameters() #These are treated same way as Ea: if it's not a string, it will become a kmos parameter.

aboveNumReactions = 22 #I am below adding all of the AF etc. as parameters up to A22p0, these are needed for throttling.
#Forward Process Pre-exponential creation and setting as 1 Loop
for processCounter in range(1,aboveNumReactions+1):
    current_process_name = 'F'+str(processCounter)+'p0'
    current_preexponential_name = 'A'+ current_process_name
    exec('A'+ current_process_name +'=1') #This only sets it as 1 in this runfile. See below.
    currentCounter = eval('A'+current_process_name)
    print(current_preexponential_name)
    print(current_process_name)
    print(eval('A'+current_process_name))
    kmc_model.add_parameter(name=current_preexponential_name, value=1) #This sets it as 1 in kmos model.
    
#Reverse Process Pre-exponential creation and setting as 1 Loop
for processCounter in range(1,aboveNumReactions+1):
    current_process_name = 'R'+str(processCounter)+'p0'
    current_preexponential_name = 'A'+ current_process_name
    exec('A'+ current_process_name +'=1') #This only sets it as 1 in this runfile. See below.
    currentCounter = eval('A'+current_process_name)
    print(current_preexponential_name)
    print(current_process_name)
    print(eval('A'+current_process_name))
    kmc_model.add_parameter(name=current_preexponential_name, value=1) #This sets it as 1 in kmos model.


#BEPRelations should be defined here. These are needed for interaction models. At the moment, only pairwise BEP is supported.
#we only need to define the BEP relation in the forward direction. The reverse direction gets determined automatically.
#For now, I am going to make diffusion cases have alpha=0.5, and also the reaction cases since that is close to what Over found.
# for adsorption cases, we will use alpha = 0, which means that the desorption gets harder with stronger binding.
from kmcos.interactions.BEPmodule import BEPRelation
kmc_model.BEPRelationsDict['F1p0'] = BEPRelation(0,0) #adsorption
kmc_model.BEPRelationsDict['F2p0'] = BEPRelation(0,0) #adsorption
kmc_model.BEPRelationsDict['F3p0'] = BEPRelation(0,0) #adsorption
kmc_model.BEPRelationsDict['F4p0'] = BEPRelation(0,0) #adsorption
kmc_model.BEPRelationsDict['F5p0'] = BEPRelation(0,0) #adsorption
kmc_model.BEPRelationsDict['F6p0'] = BEPRelation(0,0) #adsorption
kmc_model.BEPRelationsDict['F7p0'] = BEPRelation(0.5,0) #diffusion
kmc_model.BEPRelationsDict['F8p0'] = BEPRelation(0.5,0) #diffusion
kmc_model.BEPRelationsDict['F9p0'] = BEPRelation(0.5,0) #diffusion
kmc_model.BEPRelationsDict['F10p0'] = BEPRelation(0.5,0) #diffusion
kmc_model.BEPRelationsDict['F11p0'] = BEPRelation(0.5,0) #diffusion
kmc_model.BEPRelationsDict['F12p0'] = BEPRelation(0.5,0) #diffusion
kmc_model.BEPRelationsDict['F13p0'] = BEPRelation(0.5,0) #diffusion
kmc_model.BEPRelationsDict['F14p0'] = BEPRelation(0.5,0) #diffusion
kmc_model.BEPRelationsDict['F15p0'] = BEPRelation(0.5,0) #reaction
kmc_model.BEPRelationsDict['F16p0'] = BEPRelation(0.5,0) #reaction
kmc_model.BEPRelationsDict['F17p0'] = BEPRelation(0.5,0) #reaction
kmc_model.BEPRelationsDict['F18p0'] = BEPRelation(0.5,0) #reaction
kmc_model.BEPRelationsDict['F19p0'] = BEPRelation(0.5,0) #reaction
kmc_model.BEPRelationsDict['F20p0'] = BEPRelation(0.5,0) #reaction
kmc_model.BEPRelationsDict['F21p0'] = BEPRelation(0.5,0) #reaction
kmc_model.BEPRelationsDict['F22p0'] = BEPRelation(0.5,0) #reaction



# Coordinates
#The project name, "pt" is optional, provided that the initializeProjectForAdsorbateInteractions function has been called.
#In the below naming sytem, the string is called a coordFullname , with syntax layerName___siteType____unitCellOffset  where p1 means positive 1, and n2 means negative 2.
#the below command does put the coordFullName into siteDict.
kmc_model.addSiteDistinct("ruo2___cus___p0_p0_p0") 
kmc_model.addSiteDistinct("ruo2___bridge___p0_p0_p0") 
kmc_model.addSiteDistinct("ruo2___bridge___p0_p0_p0") 
kmc_model.addSiteDistinct("ruo2___Burrowed___p0_p0_p0") 
#we can also use the below syntax, but I am discouraging it because it is less consistent with the rest of the module.
#addSite(layerName, siteName, unitCellTuple=(0,0,0), project=None):
#addSite("ruo2", "bridge", "(0,0,0)", pt) #this line is equivalent to addSiteDistinct("ruo2___bridge___p0_p0_p0", pt) 

#Add surrounding sites requires using the convention of the output of the addSites function.  This means we need to have layer___siteType___unitCellOffset
#If you want to include the distance, then the first argument gets a suffix: ruo2___cus___p0_p0_p0___2 means second nearest neighbor distance. Then you give a list of sites at that distance.
# The sites at further than nearest distance feature has been  programmed, but not fully tested.
#If the first argument has no distance provided, then a default distance of "1" is used. Putting sites with further than nearest neighbor distance in the same list as that with no distance specified will end up including them in distance "1".
kmc_model.addSurroundingSites("ruo2___cus___p0_p0_p0", ["ruo2___cus___p0_p1_p0","ruo2___cus___p0_n1_p0", "ruo2___bridge___p0_p0_p0", "ruo2___bridge___p1_p0_p0" ] )
kmc_model.addSurroundingSites("ruo2___bridge___p0_p0_p0", ["ruo2___bridge___p0_p1_p0","ruo2___bridge___p0_n1_p0", "ruo2___cus___p0_p0_p0", "ruo2___cus___n1_p0_p0" ] )
kmc_model.addSurroundingSites("ruo2___Burrowed___p0_p0_p0", ["ruo2___Burrowed___p0_p0_p0"] )

#It is convenenient to make a list of ALL of the sites that you will need in your baseConditions, for ALL processes (this is NOT counting bystanders, just direct actions and conditions for reactions that occur in or across the boundary of your native unit cell).
#Be careful to use extend here, because we are connecting to a blank list in the CIProjectClass.
kmc_model.aggregateBaseConditionsSitesList.extend(["ruo2___cus___p0_p0_p0",
                                    "ruo2___bridge___p0_p0_p0",
                                    "ruo2___bridge___p1_p0_p0",
                                    "ruo2___cus___p0_n1_p0",
                                    "ruo2___bridge___p0_n1_p0",
                                    "ruo2___cus___n1_p0_p0",
                                    "ruo2___bridge___p0_p1_p0",
                                    "ruo2___cus___p0_p1_p0"])

#although you MUST add the Surrounding Sites for every site type at p0_p0_p0... but after that by translational symmetry we can auto-add the surrounding sites for anything else you need in the conditions.
kmc_model.autoAddSurroundingSites(kmc_model.aggregateBaseConditionsSitesList, upToDistance = 1)

#below I am making a dictionary for interaction terms, but I'm using my custom function which *must* be used. The way of using it is a tuple of pairs of coordFullNames and occupations (as keys), followed by the interaction term. The 1st coord full name is the species that we are concerned with.
#Note that you may need to get creative if you wanted to do something that was occupying more than 1 site with the same molecule.
#By using the "autoAdd" feature, we only need to define things for the p0_p0_p0 case, and the rest are propagated using 2D translations.
#To consider: The tuples can be formed in an automated way if we make an ordered dictionary with the sites prior to doing this. We could even read a table of values from a CSV if we do that.

#O on bridge sites for nearest neighbor bridge sites:
kmc_model.autoAddInteractionTerms([("ruo2___bridge___p0_p0_p0", "O"), ("ruo2___bridge___p0_p1_p0", "O")], InteractionTermValue = -.045)
kmc_model.autoAddInteractionTerms([("ruo2___bridge___p0_p0_p0", "O"), ("ruo2___bridge___p0_n1_p0", "O")], InteractionTermValue = -.045)


#CO on bridge sites, for nearest neighor bridge sites:
kmc_model.autoAddInteractionTerms([("ruo2___bridge___p0_p0_p0", "CO"), ("ruo2___bridge___p0_p1_p0", "CO")], InteractionTermValue = .01)
kmc_model.autoAddInteractionTerms([("ruo2___bridge___p0_p0_p0", "CO"), ("ruo2___bridge___p0_n1_p0", "CO")], InteractionTermValue = .01)

#O on cus sites for nearest neighbor cus sites.
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "O"), ("ruo2___cus___p0_p1_p0", "O")], InteractionTermValue = .02)
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "O"), ("ruo2___cus___p0_n1_p0", "O")], InteractionTermValue = .02)

#CO on cus sites for nearest neighbor cus sites.
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "CO"), ("ruo2___cus___p0_p1_p0", "CO")], InteractionTermValue = .035)
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "CO"), ("ruo2___cus___p0_n1_p0", "CO")], InteractionTermValue = .035)

#Cross terms for Ocus and neighboring Obr
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "O"), ("ruo2___bridge___p0_p0_p0", "O")], InteractionTermValue = .09)
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "O"), ("ruo2___bridge___p1_p0_p0", "O")], InteractionTermValue = .09)

#Cross terms for Ocus and neighboring CObr
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "O"), ("ruo2___bridge___p0_p0_p0", "CO")], InteractionTermValue = .07)
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "O"), ("ruo2___bridge___p1_p0_p0", "CO")], InteractionTermValue = .07)

#Cross terms for COcus and neighboring Obr
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "CO"), ("ruo2___bridge___p0_p0_p0", "O")], InteractionTermValue = .05)
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "CO"), ("ruo2___bridge___p1_p0_p0", "O")], InteractionTermValue = .05)

#Cross terms for COcus and neighboring CObr
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "CO"), ("ruo2___bridge___p0_p0_p0", "CO")], InteractionTermValue = .05)
kmc_model.autoAddInteractionTerms([("ruo2___cus___p0_p0_p0", "CO"), ("ruo2___bridge___p1_p0_p0", "CO")], InteractionTermValue = .05)


# Processes
# CO Adsorption/Desorption
kmc_model.addAProcessIncludingNeighbors("pF1p0",  #base process name. CO_adsorption_cus
            [("ruo2___cus___p0_p0_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0","CO")], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)
kmc_model.addAProcessIncludingNeighbors("pR1p0",  #base process name. CO_desorption_cus
            [("ruo2___cus___p0_p0_p0", 'CO')],  #conditions
            [("ruo2___cus___p0_p0_p0","empty")], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)

kmc_model.addAProcessIncludingNeighbors("pF2p0",  #base process name. #CO_adsorption_bridge
            [("ruo2___bridge___p0_p0_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0","CO")], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)
kmc_model.addAProcessIncludingNeighbors("pR2p0",  #base process name. #CO_desorption_bridge
            [("ruo2___bridge___p0_p0_p0", 'CO')],  #conditions
            [("ruo2___bridge___p0_p0_p0","empty")], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            

# O2 Adsorption/Desorption
# avoiding double-counting ...
kmc_model.addAProcessIncludingNeighbors("pF3p0",  #base process name. #O2_adsorption_ruo2___cus___p0_p1_p0
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_p1_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___cus___p0_p1_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR3p0",  #base process name. #O2_desorption_ruo2___cus___p0_p1_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___cus___p0_p1_p0", 'O')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_p1_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            


kmc_model.addAProcessIncludingNeighbors("pF4p0",  #base process name. #O2_adsorption_ruo2___bridge___p1_p0_p0
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p1_p0_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___bridge___p1_p0_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR4p0",  #base process name. #O2_desorption_ruo2___bridge___p1_p0_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___bridge___p1_p0_p0", 'O')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p1_p0_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)         


kmc_model.addAProcessIncludingNeighbors("pF5p0",  #base process name. #O2_adsorption_ruo2___bridge___p0_p1_p0
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p1_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_p1_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR5p0",  #base process name. #O2_desorption_ruo2___bridge___p0_p1_p0
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_p1_p0", 'O')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p1_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            


kmc_model.addAProcessIncludingNeighbors("pF6p0",  #base process name. #O2_adsorption_ruo2___cus___p0_p0_p0
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p0_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_p0_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR6p0",  #base process name. #O2_desorption_ruo2___cus___p0_p0_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_p0_p0", 'O')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p0_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)         

# CO diffusion
# cus/cus

kmc_model.addAProcessIncludingNeighbors("pF7p0",  #base process name. #COdiff_ruo2___cus___p0_p1_p0
            [("ruo2___cus___p0_p0_p0", 'CO'),
             ("ruo2___cus___p0_p1_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_p1_p0", 'CO')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR7p0",  #base process name. #COdiff_ruo2___cus___p0_n1_p0
            [("ruo2___cus___p0_p0_p0", 'CO'),
             ("ruo2___cus___p0_n1_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_n1_p0", 'CO')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)         


# bridge/bridge
kmc_model.addAProcessIncludingNeighbors("pF8p0",  #base process name. #COdiff_ruo2___bridge___p0_p1_p0
            [("ruo2___bridge___p0_p0_p0", 'CO'),
             ("ruo2___bridge___p0_p1_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p1_p0", 'CO')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR8p0",  #base process name. #COdiff_ruo2___bridge___p0_n1_p0
            [("ruo2___bridge___p0_p0_p0", 'CO'),
             ("ruo2___bridge___p0_n1_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_n1_p0", 'CO')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            

# bridge/cus (config 1)
kmc_model.addAProcessIncludingNeighbors("pF9p0",  #base process name. #COdiff_ruo2___cus___p0_p0_p0
            [("ruo2___bridge___p0_p0_p0", 'CO'),
             ("ruo2___cus___p0_p0_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_p0_p0", 'CO')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR9p0",  #base process name. #COdiff_ruo2___bridge___p0_p0_p0
            [("ruo2___cus___p0_p0_p0", 'CO'),
             ("ruo2___bridge___p0_p0_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p0_p0", 'CO')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)      


# bridge/cus (config 2)
kmc_model.addAProcessIncludingNeighbors("pF10p0",  #base process name. #COdiff_ruo2___cus___n1_p0_p0
            [("ruo2___bridge___p0_p0_p0", 'CO'),
             ("ruo2___cus___n1_p0_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___cus___n1_p0_p0", 'CO')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR10p0",  #base process name. #COdiff_ruo2___bridge___p1_p0_p0
            [("ruo2___cus___p0_p0_p0", 'CO'),
             ("ruo2___bridge___p1_p0_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p1_p0_p0", 'CO')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)      

# O diffusion
# cus/cus
kmc_model.addAProcessIncludingNeighbors("pF11p0",  #base process name. #Odiff_ruo2___cus___p0_p1_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___cus___p0_p1_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_p1_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR11p0",  #base process name. #Odiff_ruo2___cus___p0_n1_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___cus___p0_n1_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_n1_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)         

# bridge/bridge
kmc_model.addAProcessIncludingNeighbors("pF12p0",  #base process name. #Odiff_ruo2___bridge___p0_p1_p0
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_p1_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p1_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR12p0",  #base process name. #Odiff_ruo2___bridge___p0_n1_p0
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_n1_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_n1_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            

# bridge/cus (config 1)
kmc_model.addAProcessIncludingNeighbors("pF13p0",  #base process name. #Odiff_ruo2___cus___p0_p0_p0
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___cus___p0_p0_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_p0_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR13p0",  #base process name. #Odiff_ruo2___bridge___p0_p0_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_p0_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p0_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)      

# bridge/cus (config 2)
kmc_model.addAProcessIncludingNeighbors("pF14p0",  #base process name. #Odiff_ruo2___cus___n1_p0_p0
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___cus___n1_p0_p0", 'empty')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___cus___n1_p0_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)            
kmc_model.addAProcessIncludingNeighbors("pR14p0",  #base process name. #Odiff_ruo2___bridge___p1_p0_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___bridge___p1_p0_p0", 'empty')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p1_p0_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)      

# Reaction. Note: there are no reverse reactions for these.
kmc_model.addAProcessIncludingNeighbors("pF15p0",  #base process name. #React_ruo2___cus___p0_p1_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___cus___p0_p1_p0", 'CO')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_p1_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True, 
            additionalTOFDict ={'CO_oxidation':1})      

kmc_model.addAProcessIncludingNeighbors("pF16p0",  #base process name. #React_ruo2___cus___p0_n1_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___cus___p0_n1_p0", 'CO')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_n1_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True, 
            additionalTOFDict ={'CO_oxidation':1})      

kmc_model.addAProcessIncludingNeighbors("pF17p0",  #base process name. #React_ruo2___bridge___p1_p0_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___bridge___p1_p0_p0", 'CO')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p1_p0_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True, 
            additionalTOFDict ={'CO_oxidation':1})      

kmc_model.addAProcessIncludingNeighbors("pF18p0",  #base process name. #React_ruo2___bridge___p0_p0_p0
            [("ruo2___cus___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_p0_p0", 'CO')],  #conditions
            [("ruo2___cus___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p0_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True, 
            additionalTOFDict ={'CO_oxidation':1})      


kmc_model.addAProcessIncludingNeighbors("pF19p0",  #base process name. #React_ruo2___bridge___p0_p1_p0
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_p1_p0", 'CO')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_p1_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True, 
            additionalTOFDict ={'CO_oxidation':1})      

kmc_model.addAProcessIncludingNeighbors("pF20p0",  #base process name. #React_ruo2___bridge___p0_n1_p0
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___bridge___p0_n1_p0", 'CO')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___bridge___p0_n1_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True, 
            additionalTOFDict ={'CO_oxidation':1})                    

kmc_model.addAProcessIncludingNeighbors("pF21p0",  #base process name. #React_ruo2___cus___p0_p0_p0
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___cus___p0_p0_p0", 'CO')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___cus___p0_p0_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True, 
            additionalTOFDict ={'CO_oxidation':1})                                    

kmc_model.addAProcessIncludingNeighbors("pF22p0",  #base process name. #React_ruo2___cus___p0_p0_p0
            [("ruo2___bridge___p0_p0_p0", 'O'),
             ("ruo2___cus___n1_p0_p0", 'CO')],  #conditions
            [("ruo2___bridge___p0_p0_p0", 'empty'),
             ("ruo2___cus___n1_p0_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True, 
            additionalTOFDict ={'CO_oxidation':1})                                    

kmc_model.addAProcessIncludingNeighbors("pF150p0",  #base process name. #Pace restrictor reaction.
            [("ruo2___Burrowed___p0_p0_p0", 'empty')],  #conditions
            [("ruo2___Burrowed___p0_p0_p0", 'O')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)                                    
            
kmc_model.addAProcessIncludingNeighbors("pR150p0",  #base process name. #Reverse of Pace restrictor reaction.
            [("ruo2___Burrowed___p0_p0_p0", 'O')],  #conditions
            [("ruo2___Burrowed___p0_p0_p0", 'empty')], #actions
            upToDistance=1, individualTOFDict=False, rxnNumberTOFDict=True)             
#TODO: There should be a function that checks all processes to make sure that there are no conditions or actions that have orbits outside of the aggregateBaseConditionsSitesList. [orbits seems to be a typo... maybe it means sites/conditions?]

# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'lat_int' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model(validate=True) #The save model to XML takes around 5 minutes with this model when upToDistance is set with a value of 1, creating a 27 MB file. But there is also a validation step that occurs, and that adds 30 minutes or so if one waits for it.  One can turn off the validation by setting it to false.
#kmcos.compile(kmc_model) #The compiling step may take up to 30 hours for this model when upToDistance is set with a value of 1, so is commented out. To compile the model, one can uncomment this step. (and one can comment out the save_model step if one already has the xml)