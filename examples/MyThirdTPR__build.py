#!/usr/bin/env python
#Timing: Python3 MyThirdTPR.py takes about 30 seconds on a regular computer.
#After that, kmcos export or kmcos.compile(kmc_model) takes around 30 minutes to 1 hour time for proclist to finish.
#This file assumes an arrhenius expression from transition state theory for each processes rate constant. This files generates reaction processes automatically.

#compared to the last version, I added a fake process of 120p0 and the reverse -- exciting and de-exciting one of the surface oxygens.  This should prevent lockups during temperature ramp.
#once the temperature gets higher, new processes will appear and lockup will not be an issue.

import kmcos
from kmcos.types import *
from kmcos.io import *
from itertools import product
import numpy as np
#from math import exp
#from math import sqrt

model_name = __file__[+0:-3] # This is the python file name, the brackets cut off zero characters from the beginning and three character from the end (".py").  To manually name the model just place a string here.
model_name = model_name.replace("__build", "")
kmc_model = kmcos.create_kmc_model(model_name)
kmc_model.set_meta(author='Thomas Danielson',
	    email='thomasd1@vt.edu',
	    model_name=model_name,
	    model_dimension=2)
#The species unallowed has been added to keep a parallel data structure and is used in processes where there is a forward, but not a reverse process included (or vice versa).
kmc_model.add_species(name='unallowed', color='white')
kmc_model.add_species(name='empty', color='white')
kmc_model.add_species(name='U1_Ce_4plus', color='blue')
kmc_model.add_species(name='U2_Ce_3plus', color='blue')
kmc_model.add_species(name='U3_Vacancy', color = 'black',
	       representation="Atoms('H',[[0,0,0]])",
	       tags='Vacancy')
kmc_model.add_species(name='U4_H_plus', color='green',
	       representation="Atoms('He',[[0,0,0]])",
	       tags='Proton')
kmc_model.add_species(name='U6_H_star', color='green',
	       representation="Atoms('He',[[0,0,0]])",
	       tags='Hydrogen')
kmc_model.add_species(name='U7_OH_ionic', color='orange',
	       representation="Atoms('OHe',[[0,0,0],[0,0,1.1]])",
	       tags='OH')
kmc_model.add_species(name='U18_Methanol_Ce1_O2_p5_p5_p0', color='red',
	       representation="Atoms('CHeHeHeOHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2],[0,1.0,1.9]])",
	       tags='CH3OH')
kmc_model.add_species(name='U18_Methanol_Ce1_O1_p0_p1_p0', color='red',
	       representation="Atoms('CHeHeHeOHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2],[0,1.0,1.9]])",
	       tags='CH3OH')
kmc_model.add_species(name='U18_Methanol_Ce1_O1_p1_p1_p0', color='red',
	       representation="Atoms('CHeHeHeOHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2],[0,1.0,1.9]])",
	       tags='CH3OH')
kmc_model.add_species(name='U18_Methanol_Ce2_O1_p0_p0_p0', color='red',
	       representation="Atoms('CHeHeHeOHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2],[0,1.0,1.9]])",
	       tags='CH3OH')
kmc_model.add_species(name='U18_Methanol_Ce2_O2_p5_p5_p0', color='red',
	       representation="Atoms('CHeHeHeOHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2],[0,1.0,1.9]])",
	       tags='CH3OH')
kmc_model.add_species(name='U18_Methanol_Ce2_O2_n1_p0_p0', color='red',
	       representation="Atoms('CHeHeHeOHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2],[0,1.0,1.9]])",
	       tags='CH3OH')
kmc_model.add_species(name='U18_Methanol_Ce1', color='red',
	       representation="Atoms('CHeHeHeOHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2],[0,1.0,1.9]])",
	       tags='Ce')
kmc_model.add_species(name='U18_Methanol_Ce2', color='red',
	       representation="Atoms('CHeHeHeOHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2],[0,1.0,1.9]])",
	       tags='Ce')
kmc_model.add_species(name='U19_CH3O_ionic', color='#000000',
	       representation="Atoms('CHeHeHeO',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CH3O')
kmc_model.add_species(name='U20_CH3O_neutral', color='#000000',
	       representation="Atoms('CHeHeHeO',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CH3O')
kmc_model.add_species(name='U21_CH3O_neutral_V', color='#000000',
	       representation="Atoms('CHeHeHeO',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CH3O')
kmc_model.add_species(name='U22_CH3O_ionic_V', color='#000000',
	       representation="Atoms('CHeHeHeO',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CH3O')
kmc_model.add_species(name='U23_CHO', color='purple',
	       representation="Atoms('CHeO',[[0,0,0],[0.75,0.75,0.75],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U23_CHO_bridge_V_O', color='purple',
	       representation="Atoms('CHeO',[[0,0,0],[0.75,0.75,0.75],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U23_CHO_bridge_O_V', color='purple',
	       representation="Atoms('CHeO',[[0,0,0],[0.75,0.75,0.75],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U23_CHO_V', color='purple',
	       representation="Atoms('CHeO',[[0,0,0],[0.75,0.75,0.75],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U23_CHO_Ce', color='purple',
	       representation="Atoms('CHeO',[[0,0,0],[0.75,0.75,0.75],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U23_CHO_bridge_V', color='purple',
	       representation="Atoms('CHeO',[[0,0,0],[0.75,0.75,0.75],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U23_CHO_bridge_CH', color='purple',
	       representation="Atoms('CHeO',[[0,0,0],[0.75,0.75,0.75],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U24_CH_bridge_neutral', color='purple',
	       representation="Atoms('CHe',[[0,0,0],[0.75,0.75,0.75]])",
	       tags='CHO')
kmc_model.add_species(name='U24_CH_bridge_neutral_O_V', color='purple',
	       representation="Atoms('CHe',[[0,0,0],[0.75,0.75,0.75]])",
	       tags='CHO')
kmc_model.add_species(name='U24_CH_bridge_neutral_V_O', color='purple',
	       representation="Atoms('CHe',[[0,0,0],[0.75,0.75,0.75]])",
	       tags='CHO')
kmc_model.add_species(name='U25_CH2O_bridge_V', color='blue',
	       representation="Atoms('CHeHeO',[[0,0,0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CH2O')
kmc_model.add_species(name='U25_CH2O_bridge_CH2', color='purple',
	       representation="Atoms('CHeHeO',[[0,0,0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U25_CH2O_bridge_O_V', color='purple',
	       representation="Atoms('CHeHeO',[[0,0,0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U25_CH2O_bridge_V_O', color='purple',
	       representation="Atoms('CHeHeO',[[0,0,0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CHO')
kmc_model.add_species(name='U26_H2O', color='red',
	       representation="Atoms('HeHeO',[[-0.75,0,-1.0],[0.75,0,-1.0],[0,0,1.2]])",
	       tags='H2O')
kmc_model.add_species(name='U27_H2O_V', color='red',
	       representation="Atoms('HeHeO',[[-0.75,0,-1.0],[0.75,0,-1.0],[0,1,1.2]])",
	       tags='H2O')
kmc_model.add_species(name='U28_CH2O_Ce4plus', color='blue',
	       representation="Atoms('CHeHeO',[[0,0,0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CH2O')
kmc_model.add_species(name='U29_CH2O_V', color='blue',
	       representation="Atoms('CHeHeO',[[0,0,0],[-0.75,0.75,-1.0],[0,-0.75,-1.0],[0,1,1.2]])",
	       tags='CH2O')
kmc_model.add_species(name='U30_CH3_star', color='purple',
	       representation="Atoms('CHeHeHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0]])",
	       tags='CHO')
kmc_model.add_species(name='U31_CO_Ce', color='purple',
	       representation="Atoms('CHeHeHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0]])",
	       tags='CHO')
kmc_model.add_species(name='U32_CH2O2_V', color='purple',
	       representation="Atoms('CHeHeHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0]])",
	       tags='CHO')
kmc_model.add_species(name='U32_CH2O2_bridge_V_V', color='purple',
	       representation="Atoms('CHeHeHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0]])",
	       tags='CHO')
kmc_model.add_species(name='U33_CHO2_bridge_V_V', color='purple',
	       representation="Atoms('CHeHeHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0]])",
	       tags='CHO')
kmc_model.add_species(name='U33_CHO2_V', color='purple',
	       representation="Atoms('CHeHeHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0]])",
	       tags='CHO')
kmc_model.add_species(name='U34_CO2_V', color='purple',
	       representation="Atoms('CHeHeHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0]])",
	       tags='CHO')
kmc_model.add_species(name='U34_CO2_bridge_V_V', color='purple',
	       representation="Atoms('CHeHeHe',[[0,0,0],[0.75,0.75,-1.0],[-0.75,0.75,-1.0],[0,-0.75,-1.0]])",
	       tags='CHO')
kmc_model.add_species(name='U50_O', color='green',
	       representation="Atoms('O',[[0,0,0]])",
	       tags='O')
kmc_model.add_species(name='ExcitedOxygen', color='white')


#Middle layer Ce atoms
layer1 = kmc_model.add_layer(name='Ce1')
layer1.sites.append(Site(name='atop_Ce1', pos='0.5 0.8337 0.5',
			 default_species='U1_Ce_4plus'))
layer1.sites.append(Site(name='atop_Ce2', pos='0 0.3333 0.5',
			 default_species='U1_Ce_4plus'))	
#Top layer O atoms
layer1.sites.append(Site(name='atop_O1', pos='0 0 1',
			 default_species='U50_O'))
layer1.sites.append(Site(name='atop_O2', pos='0.5 0.5 1',
			 default_species='U50_O'))
#Bridge sites between neighboring O atoms
layer1.sites.append(Site(name='bridge_O_O_2_p0_p0_p0', pos='0.25 0.25 1',
			 default_species='empty'))
layer1.sites.append(Site(name='bridge_O_O_1_p0_p0_p0', pos='0.5 0 1',
			 default_species='empty'))
layer1.sites.append(Site(name='bridge_O_O_3_p0_p0_p0', pos='0.75 0.25 1',
			 default_species='empty'))
layer1.sites.append(Site(name='bridge_O_O_4_p0_p0_p0', pos='1 0.5 1',
			 default_species='empty'))
layer1.sites.append(Site(name='bridge_O_O_6_p0_p0_p0', pos='0.25 0.75 1',
			 default_species='empty'))
layer1.sites.append(Site(name='bridge_O_O_5_p0_p0_p0', pos='0.75 0.75 1',
			 default_species='empty'))

kmc_model.lattice.cell = np.diag([3.825, 6.626, 2.343])

T_surface_python = 600
T_gas_python = T_surface_python

kmc_model.add_parameter(name='T', value=T_surface_python, adjustable=False)
kmc_model.add_parameter(name='p_CH3OHgas', value=0, adjustable=False)
kmc_model.add_parameter(name='A', value='(3.825*angstrom*6.626*angstrom)')
kmc_model.add_parameter(name='mass_CH3OHkgmol', value='0.03204')
kmc_model.add_parameter(name='R', value=8.3145, adjustable=False)
kmc_model.add_parameter(name='T_gas', value=T_gas_python, adjustable=False)
kmc_model.add_parameter(name='k_B', value=1.381e-23, adjustable=False)
kmc_model.add_parameter(name='alpha', value='1')
kmc_model.add_parameter(name='N_A', value='6.022e+23')
kmc_model.add_parameter(name='p_CH2Ogas', value=0, adjustable=False)
kmc_model.add_parameter(name='mass_CH2Okgmol', value='0.030')
kmc_model.add_parameter(name='p_H2Ogas', value='0')
kmc_model.add_parameter(name='mass_H2Okgmol', value='0.018')
kmc_model.add_parameter(name='Pi', value='3.14159')
kmc_model.add_parameter(name='p_H2gas', value='0')
kmc_model.add_parameter(name='mass_H2kgmol', value='0.002')
kmc_model.add_parameter(name='p_COgas', value='0')
kmc_model.add_parameter(name='mass_COkgmol', value='0.028')
kmc_model.add_parameter(name='p_O2gas', value = 0, adjustable=False)
kmc_model.add_parameter(name='mass_O2kgmol', value = '0.0159')

#The following is a dictionary of the initial state energies i.e. the energies of the reactants.  Each reactant species is specified explicitly in the name string.  For adsorption processes we are setting the reactant energy equal to the transition state energy in cases where they are assumed barrierless.
activation_energies_dict = {
				'EaF8p7': 150000,
				'EaR8p7': 150000,
				'EaF9p0': 70000,
				'EaR9p0': 0,
				'EaF9p8': 140000,
				'EaR9p8': 300000,
				'EaF15p0': 78153.1,
				'EaR15p0': 0,
				'EaR15p1': 8683.68,
				'EaF15p1': 15437.65,
				'EaF16p8': 30000,
				'EaR16p8': 150000,
				'EaR18p0': 0,
				'EaF18p0': 91000,
				'EaF101p1': 10669.91,
				'EaF101p5': 6639.88,
				'EaF101p6': 7847.84,
				'EaF102p6': 88495.35,
				'EaF102p8': 96485.31,
				'EaF103p6': 76223.39,
				'EaF104p7': 17367.36,
				'EaF105p4': 26051.03,
				'EaF106p5': 66969.14,
				'EaF106p6': 68403.26,
				'EaF106p7': 61667.96,
				'EaF108p2': 7855.71,
				'EaF108p4': 0,
				'EaF109p2': 76770.91,
				'EaF109p3': 47351.83,
				'EaF109p4': 50151.78,
				'EaF110p3': 57727.17,
				'EaF110p4': 64645.16,
				'EaF111p2': 84436.39,
				'EaF111p3': 112099.54,
				'EaF112p3': 102300.65,
				'EaF112p7': 114817.52,
				'EaF113p1': 34687.04,
				'EaF113p7': 109099.48,
				'EaF116p1': 126013.38,
				'EaF117p2': 22560.53,
				'EaF117p3': 22560.53,
				'EaR101p1': 4498.71,
				'EaR101p5': 15850.33,
				'EaR101p6': 9783.10,
				'EaR102p6': 123656.84,
				'EaR102p8': 0,	  # 
				'EaR103p6': 71091.45,
				'EaR104p7': 6190.51,
				'EaR105p4': 33424.20,
				'EaR106p5': 0,
				'EaR106p6': 0,
				'EaR106p7': 0,
				'EaR108p2': 14629.91,
				'EaR108p4': 138521.77,
				'EaR109p2': 0,
				'EaR109p3': 0,
				'EaR109p4': 0,
				'EaR110p3': 0,
				'EaR110p4': 0,
				'EaR111p2': 12186.71,
				'EaR111p3': 0,
				'EaR112p3': 109171.72,
				'EaR112p7': 29411.37,
				'EaR113p1': 0,
				'EaR113p7': 0,
				'EaR116p1': 0,
				'EaR117p2': 22560.53,
				'EaR117p3': 22560.53,
				'EaF120p0': 0,
				'EaR120p0': 0
			}

#This loop uses the values from the dictionary of activation energies in order to create a string which will serve to add the values from the dictionary as parameters to KMOS.  An example parameter would look like: kmc_model.add_parameter(name='EaF21p5', value=0, adjustable=False)
for i in range(len(activation_energies_dict)):
	activation_energies_string = str('kmc_model.add_parameter(name=')  \
				+ '\'' + str(list(activation_energies_dict.keys())[i]) + '\'' \
				+ str(', value=') \
				+ str(list(activation_energies_dict.values())[i])  \
				+ str(', adjustable=False)')
	exec("%s" %(activation_energies_string))


#The following is a dictionary of the pre-exponentials for each process.  In the case of adsorption processes the value provided is the steric factor in reactive hard spheres collision theory also known as S_0.
pre_exponentials_dict = {
				'AF8p7'	: 1e+13	,
				'AR8p7'	: 1e+13	,
				'AF9p0'	: 1e+13	,
				'AR9p0'	: 0	,
				'AF9p8'	: 1e+13	,
				'AR9p8'	: 1e+13	,
				'AF15p0': 1e+13	,
				'AR15p0': 0   ,
				'AR15p1': 1e+10	,
				'AF15p1': 1e13	,
				'AF16p8': 1e13	,
				'AR16p8': 1e13	,
				'AR18p0': 0	,
				'AF18p0': 1e+10	,
				'AF101p1': 1e13,
				'AF101p5': 1e13,
				'AF101p6': 1e13,
				'AF102p6': 1e13,
				'AF102p8': 1e13,
				'AF103p6': 1e13,
				'AF104p7': 1e13,
				'AF105p4': 1e13,
				'AF106p5': 1e13,
				'AF106p6': 1e13,
				'AF106p7': 1e13,
				'AF108p2': 1e13,
				'AF108p4': 1e13,
				'AF109p2': 1e13,
				'AF109p3': 1e13,
				'AF109p4': 1e13,
				'AF110p3': 1e13,
				'AF110p4': 1e13,
				'AF111p2': 1e13,
				'AF111p3': 1e13,
				'AF112p3': 1e13,
				'AF112p7': 1e13,
				'AF113p1': 1e13,
				'AF113p7': 1e13,
				'AF116p1': 1e13,
				'AF117p2': 1e13,
				'AF117p3': 1e13,
				'AR101p1': 1e13,
				'AR101p5': 1e13,
				'AR101p6': 1e13,
				'AR102p6': 1e13,
				'AR102p8': 1e13,
				'AR103p6': 1e13,
				'AR104p7': 1e13,
				'AR105p4': 1e13,
				'AR106p5': 0,
				'AR106p6': 0,
				'AR106p7': 0,
				'AR108p2': 1e13,
				'AR108p4': 1e13,
				'AR109p2': 0,
				'AR109p3': 0,
				'AR109p4': 0,
				'AR110p3': 0,
				'AR110p4': 0,
				'AR111p2': 1e13,
				'AR111p3': 0,
				'AR112p3': 1e13,
				'AR112p7': 1e13,
				'AR113p1': 0,
				'AR113p7': 0,
				'AR116p1': 0,
				'AR117p2': 1e13,
				'AR117p3': 1e13,
				'AF120p0': 1,
				'AR120p0': 1e13

			}


#This loop uses the values from the dictionary of pre-exponentials in order to create a string which will serve to add the values from the dictionary as parameters to KMOS.  An example string looks like: kmc_model.add_parameter(name='E_TST_F21p5', value=0, adjustable=False)
for i in range(len(pre_exponentials_dict)):
	preexponentials_string = str('kmc_model.add_parameter(name=')  \
				+ '\'' + str(list(pre_exponentials_dict.keys())[i]) + '\'' \
				+ str(', value=') \
				+ str(list(pre_exponentials_dict.values())[i])  \
				+ str(', adjustable=False)')
	exec("%s" %(preexponentials_string))
	
Ce_1_p0_p0_p0 = kmc_model.lattice.generate_coord('atop_Ce1.(0,0,0).Ce1')
Ce_2_p0_p0_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(0,0,0).Ce1')
O_1_p0_p0_p0 = kmc_model.lattice.generate_coord('atop_O1.(0,0,0).Ce1')
O_2_p0_p0_p0 = kmc_model.lattice.generate_coord('atop_O2.(0,0,0).Ce1')

O_2_p1_p0_p0 = kmc_model.lattice.generate_coord('atop_O2.(1,0,0).Ce1')
O_2_n1_p0_p0 = kmc_model.lattice.generate_coord('atop_O2.(-1,0,0).Ce1')
O_2_p0_n1_p0 = kmc_model.lattice.generate_coord('atop_O2.(0,-1,0).Ce1')
O_2_n1_n1_p0 = kmc_model.lattice.generate_coord('atop_O2.(-1,-1,0).Ce1')
O_2_p1_p1_p0 = kmc_model.lattice.generate_coord('atop_O2.(1,1,0).Ce1')
O_2_p0_p1_p0 = kmc_model.lattice.generate_coord('atop_O2.(0,1,0).Ce1')
O_2_n1_p1_p0 = kmc_model.lattice.generate_coord('atop_O2.(-1,1,0).Ce1')
O_2_n2_p0_p0 = kmc_model.lattice.generate_coord('atop_O2.(-2,0,0).Ce1')

O_1_p0_p1_p0 = kmc_model.lattice.generate_coord('atop_O1.(0,1,0).Ce1')
O_1_p1_p1_p0 = kmc_model.lattice.generate_coord('atop_O1.(1,1,0).Ce1')
O_1_n1_p0_p0 = kmc_model.lattice.generate_coord('atop_O1.(-1,0,0).Ce1')
O_1_p1_p0_p0 = kmc_model.lattice.generate_coord('atop_O1.(1,0,0).Ce1')
O_1_p0_n1_p0 = kmc_model.lattice.generate_coord('atop_O1.(0,-1,0).Ce1')
O_1_p2_p1_p0 = kmc_model.lattice.generate_coord('atop_O1.(2,1,0).Ce1')
O_1_n1_p1_p0 = kmc_model.lattice.generate_coord('atop_O1.(-1,1,0).Ce1')

Ce_1_p0_n1_p0 = kmc_model.lattice.generate_coord('atop_Ce1.(0,-1,0).Ce1')
Ce_1_n1_n1_p0 = kmc_model.lattice.generate_coord('atop_Ce1.(-1,-1,0).Ce1')
Ce_1_n1_p0_p0 = kmc_model.lattice.generate_coord('atop_Ce1.(-1,0,0).Ce1')
Ce_1_p1_p0_p0 = kmc_model.lattice.generate_coord('atop_Ce1.(1,0,0).Ce1')
Ce_1_p1_n1_p0 = kmc_model.lattice.generate_coord('atop_Ce1.(1,-1,0).Ce1')
Ce_1_n2_n1_p0 = kmc_model.lattice.generate_coord('atop_Ce1.(-2,-1,0).Ce1')

Ce_2_p1_p0_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(1,0,0).Ce1')
Ce_2_n1_p0_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(-1,0,0).Ce1')
Ce_2_p2_p0_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(2,0,0).Ce1')
Ce_2_p0_p1_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(0,1,0).Ce1')
Ce_2_p1_p1_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(1,1,0).Ce1')
Ce_2_n1_n1_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(-1,-1,0).Ce1')
Ce_2_p0_n1_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(0,-1,0).Ce1')
Ce_2_p1_n1_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(1,-1,0).Ce1')
Ce_2_n2_n1_p0 = kmc_model.lattice.generate_coord('atop_Ce2.(-2,-1,0).Ce1')

bridge_O_O_1_p0_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_1_p0_p0_p0.(0,0,0).Ce1')
bridge_O_O_2_p0_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_2_p0_p0_p0.(0,0,0).Ce1')
bridge_O_O_3_p0_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_3_p0_p0_p0.(0,0,0).Ce1')
bridge_O_O_4_p0_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_4_p0_p0_p0.(0,0,0).Ce1')
bridge_O_O_5_p0_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_5_p0_p0_p0.(0,0,0).Ce1')
bridge_O_O_6_p0_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_6_p0_p0_p0.(0,0,0).Ce1')

bridge_O_O_1_n1_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_1_p0_p0_p0.(-1,0,0).Ce1')
bridge_O_O_3_n1_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_3_p0_p0_p0.(-1,0,0).Ce1')
bridge_O_O_4_n1_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_4_p0_p0_p0.(-1,0,0).Ce1')
bridge_O_O_5_n1_n1_p0 = kmc_model.lattice.generate_coord('bridge_O_O_5_p0_p0_p0.(-1,-1,0).Ce1')
bridge_O_O_6_p0_n1_p0 = kmc_model.lattice.generate_coord('bridge_O_O_6_p0_p0_p0.(0,-1,0).Ce1')
bridge_O_O_2_p1_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_2_p0_p0_p0.(1,0,0).Ce1')
bridge_O_O_6_p1_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_6_p0_p0_p0.(1,0,0).Ce1')
bridge_O_O_5_n1_p0_p0 = kmc_model.lattice.generate_coord('bridge_O_O_5_p0_p0_p0.(-1,0,0).Ce1')
bridge_O_O_1_p0_p1_p0 = kmc_model.lattice.generate_coord('bridge_O_O_5_p0_p0_p0.(0,1,0).Ce1')

#Lists for automatically generated processes

#list containing Oxygen sites in the cell
O_sites = [0, \
	      [1,'O_1_p0_p0_p0'],[2,'O_2_p0_p0_p0'], \
	      [3,'O_1_p1_p0_p0'],[4,'O_2_p1_p0_p0'], \
	      [5,'O_1_p1_p1_p0'],[6,'O_1_p0_p1_p0']  \
	   ]

O_sites_dictionary = { \
		      'O_1_p0_p0_p0':1,'O_2_p0_p0_p0':2, \
		      'O_1_p1_p0_p0':3,'O_2_p1_p0_p0':4, \
		      'O_1_p1_p1_p0':5,'O_1_p0_p1_p0':6  \
		      }

O_sites_surrounding_O = [0, \
				[1,'O_1_p1_p0_p0','O_2_p0_p0_p0','O_2_n1_p0_p0','O_1_n1_p0_p0','O_2_n1_n1_p0','O_2_p0_n1_p0'],   \
				[2,'O_2_p1_p0_p0','O_1_p1_p1_p0','O_1_p0_p1_p0','O_2_n1_p0_p0','O_1_p0_p0_p0','O_1_p1_p0_p0']    \
			]

#This list gives the nearest neighbor Ce site to the bridge sites.
Ce_sites_surrounding_bridge_sites = [0,[1,'Ce_1_p0_n1_p0'],[2,'Ce_2_p0_p0_p0'],[3,'Ce_2_p1_p0_p0'],[4,'Ce_2_p1_p0_p0'],[5,'Ce_1_p0_p0_p0'],[6,'Ce_1_p0_p0_p0']]

#List containing Ce sites in the cell
Ce_sites = [0,[1,'Ce_1_p0_p0_p0'],[2,'Ce_2_p0_p0_p0']]

#This list gives the nearest neighbor Ce site to the bridge sites.
Ce_surrounding_bridge_sites = [0,[1,'Ce_1_p0_n1_p0'],[2,'Ce_2_p0_p0_p0'],[3,'Ce_2_p1_p0_p0'],[4,'Ce_2_p1_p0_p0'],[5,'Ce_1_p0_p0_p0'],[6,'Ce_1_p0_p0_p0']]

#Bridging sites list, this only includes the 6 unique bridge sites that are located within the cell
bridge_sites = [0,[1,'bridge_O_O_1_p0_p0_p0'],[2,'bridge_O_O_2_p0_p0_p0'],[3,'bridge_O_O_3_p0_p0_p0'],[4,'bridge_O_O_4_p0_p0_p0'],[5,'bridge_O_O_5_p0_p0_p0'],[6,'bridge_O_O_6_p0_p0_p0']]

#List containing Ce sites surrounding Ce sites, the first number in each sublist is the index of the central Ce i.e. Ce_1 or Ce_2.  The sites start at the right (i.e. "3 O'clock") and go counterclockwise
Ce_sites_surrounding_Ce = [0,
			     [1,'Ce_1_p1_p0_p0','Ce_2_p1_p1_p0','Ce_2_p0_p1_p0','Ce_1_n1_p0_p0','Ce_2_p0_p0_p0','Ce_2_p1_p0_p0'],  \
			     [2,'Ce_2_p1_p0_p0','Ce_1_p0_p0_p0','Ce_1_n1_p0_p0','Ce_2_n1_p0_p0','Ce_1_n1_n1_p0','Ce_1_p0_n1_p0']   \
			  ]

#List containing bridge sites surrounding O sites.  Again the sites start at the bottom right and go counterclockwise.
bridge_sites_surrounding_O = [0,[1,'bridge_O_O_6_p0_n1_p0','bridge_O_O_1_p0_p0_p0','bridge_O_O_2_p0_p0_p0','bridge_O_O_3_n1_p0_p0','bridge_O_O_1_n1_p0_p0','bridge_O_O_5_n1_n1_p0'],[2,'bridge_O_O_3_p0_p0_p0','bridge_O_O_4_p0_p0_p0','bridge_O_O_5_p0_p0_p0','bridge_O_O_6_p0_p0_p0','bridge_O_O_4_n1_p0_p0','bridge_O_O_2_p0_p0_p0']]

#List containing Ce sites surrounding O sites.  This list is particularly used for processes concerning bridging processes.  The Ce sites surrounding each oxygen do not start with the 3 o'clock position.
Ce_sites_surrounding_O = [0,\
			    [1,'Ce_1_p0_n1_p0','Ce_2_p0_p0_p0','Ce_1_n1_n1_p0'],[2,'Ce_2_p1_p0_p0','Ce_1_p0_p0_p0','Ce_2_p0_p0_p0'], \
			    [3,'Ce_1_p1_n1_p0','Ce_2_p1_p0_p0','Ce_1_p0_n1_p0'],[4,'Ce_2_p2_p0_p0','Ce_1_p1_p0_p0','Ce_2_p1_p0_p0'], \
			    [5,'Ce_1_p1_p0_p0','Ce_2_p1_p1_p0','Ce_1_p0_p0_p0'],[6,'Ce_1_p0_p0_p0','Ce_2_p0_p1_p0','Ce_1_p1_p0_p0'] \
			  ]

#List containing Ce sites surrounding the neighboring O sites of O1 and O2.  We start with neighboring oxygen atoms to O1.  For both O1 and O2 cases we start at the right and move counterclockwise for neighboring O.  Neighboring Ce atoms start at the right and move counterclockwise as well.  
Ce_sites_surrounding_O_surrounding_O1_and_O2 = [0,  \
						  [1, \
						   [1,'Ce_1_p1_n1_p0','Ce_2_p1_p0_p0','Ce_1_p0_n1_p0'],  \
						   [2,'Ce_2_p1_p0_p0','Ce_1_p0_p0_p0','Ce_2_p0_p0_p0'],  \
						   [3,'Ce_2_p0_p0_p0','Ce_1_n1_p0_p0','Ce_2_n1_p0_p0'],  \
						   [4,'Ce_1_n1_n1_p0','Ce_2_n1_p0_p0','Ce_1_n2_n1_p0'],  \
						   [5,'Ce_2_p0_n1_p0','Ce_1_n1_n1_p0','Ce_2_n1_n1_p0'],  \
						   [6,'Ce_2_p1_n1_p0','Ce_1_p0_n1_p0','Ce_2_p0_n1_p0']   \
						  ],   \
						  [2,  \
						   [1,'Ce_2_p2_p0_p0','Ce_1_p1_p0_p0','Ce_2_p1_p0_p0'],  \
						   [2,'Ce_1_p1_p0_p0','Ce_2_p1_p1_p0','Ce_1_p0_p0_p0'],  \
						   [3,'Ce_1_p0_p0_p0','Ce_2_p0_p1_p0','Ce_1_n1_p0_p0'],  \
						   [4,'Ce_2_p0_p0_p0','Ce_1_n1_p0_p0','Ce_2_n1_p0_p0'],  \
						   [5,'Ce_1_p0_n1_p0','Ce_2_p0_p0_p0','Ce_1_n1_n1_p0'],  \
						   [6,'Ce_1_p1_n1_p0','Ce_2_p1_p0_p0','Ce_1_p0_n1_p0']   \
						  ]   \
						]
#This list will give the 6 neighboring O sites to each of the three O sites that surround each Ce.
O_sites_surrounding_O_surrounding_Ce1_or_Ce2 = [0, \
						[1, \
						[1,'O_2_p1_p0_p0','O_1_p1_p1_p0','O_1_p0_p1_p0','O_2_n1_p0_p0','O_1_p0_p0_p0','O_1_p1_p0_p0'], \
						[2,'O_1_p2_p1_p0','O_2_p1_p1_p0','O_2_p0_p1_p0','O_1_p0_p1_p0','O_2_p0_p0_p0','O_2_p1_p0_p0'], \
						[3,'O_1_p1_p1_p0','O_2_p0_p1_p0','O_2_n1_p1_p0','O_1_n1_p1_p0','O_2_n1_p0_p0','O_2_p0_p0_p0'] \
						  ], \
						[2, \
						[1,'O_1_p1_p0_p0','O_2_p0_p0_p0','O_2_n1_p0_p0','O_1_n1_p0_p0','O_2_n1_n1_p0','O_2_p0_n1_p0'], \
						[2,'O_2_p1_p0_p0','O_1_p1_p1_p0','O_1_p0_p1_p0','O_2_n1_p0_p0','O_1_p0_p0_p0','O_1_p1_p0_p0'], \
						[3,'O_2_p0_p0_p0','O_1_p0_p1_p0','O_1_n1_p1_p0','O_2_n2_p0_p0','O_1_n1_p0_p0','O_1_p0_p0_p0'] \
						  ] \
						]

#List containing O sites surrounding Ce sites in order of O surrounding Ce1 and O surrounding Ce2
O_sites_surrounding_Ce = [0,\
			    [1,'O_2_p0_p0_p0','O_1_p1_p1_p0','O_1_p0_p1_p0'],	[2,'O_1_p0_p0_p0','O_2_p0_p0_p0','O_2_n1_p0_p0'] \
			  ]
#List containing O sites surrounding bridging sites. The first coordinate corresponds to the number of the bridge site, the second coordinate is the neighboring oxygen on the right and the third coordinate is the neighboring oxygen on the left.
O_sites_surrounding_bridge_sites = [0,[1,'O_1_p1_p0_p0','O_1_p0_p0_p0'],[2,'O_2_p0_p0_p0','O_1_p0_p0_p0'],[3,'O_1_p1_p0_p0','O_2_p0_p0_p0'],[4,'O_2_p1_p0_p0','O_2_p0_p0_p0'],[5,'O_1_p1_p1_p0','O_2_p0_p0_p0'],[6,'O_2_p0_p0_p0','O_1_p0_p1_p0']]

#This list tells the two nearest neighboring O atoms to each bridge site.  i.e. if a bridge site is occupied where, this implies that the two oxygen atoms that it is bridging are filled with a bridging species.  There are two additional O atoms that are near neighbors that are not occupied (or so we want to check...).  These two atoms not involved in the bridging are what we are defining.
O_sites_lateral_to_bridge_sites = [0,[1,'O_2_p0_p0_p0','O_2_p0_n1_p0'],[2,'O_1_p1_p0_p0','O_2_n1_p0_p0'],[3,'O_1_p0_p0_p0','O_2_p1_p0_p0'],[4,'O_1_p1_p1_p0','O_1_p1_p0_p0'],[5,'O_1_p0_p1_p0','O_2_p1_p0_p0'],[6,'O_2_n1_p0_p0','O_1_p1_p1_p0']]

#naming of the species goes left right and so O_V means O on the left and V on the right
O_V_order = [0,'O_V','V_O']

#The following list is for all methanol species occupying Ce1 and Ce2 and briding between either Ce1 and Ce2 and one of the three neighboring oxygens.

methanol_species_list = [0,['U18_Methanol_Ce1',[0,'U18_Methanol_Ce1_O2_p5_p5_p0', 'U18_Methanol_Ce1_O1_p1_p1_p0', 'U18_Methanol_Ce1_O1_p0_p1_p0']], ['U18_Methanol_Ce2',[0,'U18_Methanol_Ce2_O1_p0_p0_p0','U18_Methanol_Ce2_O2_p5_p5_p0','U18_Methanol_Ce2_O2_n1_p0_p0']]]

methanol_Ce_species_surrounding_Ce1_or_Ce2 = [0, \
					   [0,'U18_Methanol_Ce1', 'U18_Methanol_Ce2', 'U18_Methanol_Ce2','U18_Methanol_Ce1','U18_Methanol_Ce2','U18_Methanol_Ce2'], \
					   [0,'U18_Methanol_Ce2', 'U18_Methanol_Ce1', 'U18_Methanol_Ce1','U18_Methanol_Ce2','U18_Methanol_Ce1','U18_Methanol_Ce1']] 

#This array contains the process names, pre-exponentials and the energies associated with the initial state and the transition state for each process.  These are all strings that are the names of the parameters and not the parameters themselves.  We do it this way becuase when defining kmos processes, strings are provided to describe the rate constant and kmos parses that recognizing the names of parameters.  The process name will be called in order to select the energies and is given before the process loops as "current_process_name".
process_parameters_array = [
				['pR8p7','AR8p7','EaR8p7'],  \
				['pF8p7','AF8p7','EaF8p7'],  \
				['pR9p0','AR9p0','EaR9p0'],  \
				['pF9p0','AF9p0','EaF9p0'],  \
				['pR9p8','AR9p8','EaR9p8'],  \
				['pF9p8','AF9p8','EaF9p8'],  \
				['pR15p0','AR15p0','EaR15p0'],  \
				['pF15p0','AF15p0','EaF15p0'],  \
				['pR15p1','AR15p1','EaR15p1'],  \
				['pF15p1','AF15p1','EaF15p1'],  \
				['pR16p8','AR16p8','EaR16p8'],  \
				['pF16p8','AF16p8','EaF16p8'],  \
				['pR18p0','AR18p0','EaR18p0'],  \
				['pF18p0','AF18p0','EaF18p0'],  \
				['pF101p1','AF101p1','EaF101p1'],  \
				['pR101p1','AR101p1','EaR101p1'],  \
				['pF101p5','AF101p5','EaF101p5'],  \
				['pR101p5','AR101p5','EaR101p5'],  \
				['pR101p6','AR101p6','EaR101p6'],  \
				['pF101p6','AF101p6','EaF101p6'],  \
				['pR102p6','AR102p6','EaR102p6'],  \
				['pF102p6','AF102p6','EaF102p6'],  \
				['pR102p8','AR102p8','EaR102p8'],  \
				['pF102p8','AF102p8','EaF102p8'],  \
				['pR103p6','AR103p6','EaR103p6'],  \
				['pF103p6','AF103p6','EaF103p6'],  \
				['pR104p7','AR104p7','EaR104p7'],  \
				['pF104p7','AF104p7','EaF104p7'],  \
				['pR105p4','AR105p4','EaR105p4'],  \
				['pF105p4','AF105p4','EaF105p4'],  \
				['pR106p5','AR106p5','EaR106p5'],  \
				['pF106p5','AF106p5','EaF106p5'],  \
				['pR106p6','AR106p6','EaR106p6'],  \
				['pF106p6','AF106p6','EaF106p6'],  \
				['pR106p7','AR106p7','EaR106p7'],  \
				['pF106p7','AF106p7','EaF106p7'],  \
				['pR108p2','AR108p2','EaR108p2'],  \
				['pF108p2','AF108p2','EaF108p2'],  \
				['pR108p4','AR108p4','EaR108p4'],  \
				['pF108p4','AF108p4','EaF108p4'],  \
				['pR109p2','AR109p2','EaR109p2'],  \
				['pF109p2','AF109p2','EaF109p2'],  \
				['pR109p3','AR109p3','EaR109p3'],  \
				['pF109p3','AF109p3','EaF109p3'],  \
				['pR109p4','AR109p4','EaR109p4'],  \
				['pF109p4','AF109p4','EaF109p4'],  \
				['pR110p3','AR110p3','EaR110p3'],  \
				['pF110p3','AF110p3','EaF110p3'],    \
				['pR110p4','AR110p4','EaR110p4'],   \
				['pF110p4','AF110p4','EaF110p4'],   \
				['pR111p2','AR111p2','EaR111p2'],  \
				['pF111p2','AF111p2','EaF111p2'],  \
				['pR111p3','AR111p3','EaR111p3'],  \
				['pF111p3','AF111p3','EaF111p3'],  \
				['pR112p3','AR112p3','EaR112p3'], \
				['pF112p3','AF112p3','EaF112p3'],   \
				['pR112p7','AR112p7','EaR112p7'], \
				['pF112p7','AF112p7','EaF112p7'],   \
				['pF113p1','AF113p1','EaF113p1'],   \
				['pR113p1','AR113p1','EaR113p1'],  \
				['pF113p7','AF113p7','EaF113p7'],  \
				['pR113p7','AR113p7','EaR113p7'], \
				['pF116p1','AF116p1','EaF116p1'],  \
				['pR116p1','AR116p1','EaR116p1'], \
				['pF117p2','AF117p2','EaF117p2'],  \
				['pR117p2','AR117p2','EaR117p2'], \
				['pF117p3','AF117p3','EaF117p3'],  \
				['pR117p3','AR117p3','EaR117p3'],\
				['pF120p0','AF120p0','EaF120p0'], \
				['pR120p0','AR120p0','EaR120p0']]




#These pull specific information given in process_parameters_array to be used later in reaction processes.
unzip_parameters = list(zip(*process_parameters_array))
process_names = unzip_parameters[0]
preexponentials = unzip_parameters[1]
activation_energies_list = unzip_parameters[2]


#Dictionaries for TOF data
R8p7 = {'R8p7':1}
F8p7 = {'F8p7':1}
R9p0 = {'R9p0':1}
F9p0 = {'F9p0':1}
R9p8 = {'R9p8':1}
F9p8 = {'F9p8':1}
R15p0 = {'R15p0':1}
F15p0 = {'F15p0':1}
R15p1 = {'R15p1':1}
F15p1 = {'F15p1':1}
R16p8 = {'R16p8':1}
F16p8 = {'F16p8':1}
R18p0 = {'R18p0':1}
F18p0 = {'F18p0':1}
F101p1 = {'F101p1':1}
R101p1 = {'R101p1':1}
F101p5 = {'F101p5':1}
R101p5 = {'R101p5':1}
R101p6 = {'R101p6':1}
F101p6 = {'F101p6':1}
R102p6 = {'R102p6':1}
F102p6 = {'F102p6':1}
R102p8 = {'R102p8':1}
F102p8 = {'F102p8':1}
R103p6 = {'R103p6':1}
F103p6 = {'F103p6':1}
R104p7 = {'R104p7':1}
F104p7 = {'F104p7':1}
R105p4 = {'R105p4':1}
F105p4 = {'F105p4':1}
R106p5 = {'R106p5':1}
F106p5 = {'F106p5':1}
R106p6 = {'R106p6':1}
F106p6 = {'F106p6':1}
R106p7 = {'R106p7':1}
F106p7 = {'F106p7':1}
R108p2 = {'R108p2':1}
F108p2 = {'F108p2':1}
R108p4 = {'R108p4':1}
F108p4 = {'F108p4':1}
R109p2 = {'R109p2':1}
F109p2 = {'F109p2':1}
R109p3 = {'R109p3':1}
F109p3 = {'F109p3':1}
R109p4 = {'R109p4':1}
F109p4 = {'F109p4':1}
R110p3 = {'R110p3':1}
F110p3 = {'F110p3':1}
R110p4 = {'R110p4':1}
F110p4 = {'F110p4':1}
R111p2 = {'R111p2':1}
F111p2 = {'F111p2':1}
R111p3 = {'R111p3':1}
F111p3 = {'F111p3':1}
R112p3 = {'R112p3':1}
F112p3 = {'F112p3':1}
R112p7 = {'R112p7':1}
F112p7 = {'F112p7':1}
F113p1 = {'F113p1':1}
R113p1 = {'R113p1':1}
F113p7 = {'F113p7':1}
R113p7 = {'R113p7':1}
R116p1 = {'R116p1':1}
F116p1 = {'F116p1':1}
R117p2 = {'R117p2':1}
F117p2 = {'F117p2':1}
R117p3 = {'R117p3':1}
F117p3 = {'F117p3':1}
F120p0 = {'F120p0':1}
R120p0 = {'F120p0':1}

CH3OH_output_flux = {'CH3OH_output_flux':1}
H2_output_flux = {'H2_output_flux':1}
CH2O_output_flux = {'CH2O_output_flux':1}
CO_output_flux = {'CO_output_flux':1}
H2O_output_flux = {'H2O_output_flux':1}
CO2_output_flux = {'CO2_output_flux':1}
Fake_OxygenExcitation_flux = {'Fake_OxygenExcitation_flux':1}
Fake_OxygenExcitationRelaxation_flux = {'Fake_OxygenExcitationRelaxation_flux':1}


#Processes for H+ hopping between oxygens regardless of type of Ce nearby (rxn -8.7)

current_process_name ='pR8p7'
#x loops across O1 and O2
for x in range(1,2+1):
#y loops across oxygen atoms neighboring O1 and O2
	for y in range(1,6+1):
#z loops across Ce atoms surrounding O atoms
		for z in range (1,3+1):
			temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)
			temporary_conditions_list = eval("[Condition(coord=%s, species='U4_H_plus'),  \
							   Condition(coord= %s, species='U50_O')]" %(O_sites[x][1],O_sites_surrounding_O[x][y]))
			temporary_actions_list = eval("[Action(coord=%s, species='U50_O'),   \
							Action(coord=%s, species='U4_H_plus')]" %(O_sites[x][1],O_sites_surrounding_O[x][y]))
	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
			temporary_tst_interaction_energy = 0
			temporary_reactant_interaction_energy = 0
			temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
			temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
			temporary_tof_count_dict = {'R8p7':1}
			temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
			kmc_model.add_process(**temporary_kwargs_dictionary)

#forward process for the hopping event is same as reverse process.	
current_process_name ='pF8p7'
#x loops across O1 and O2
for x in range(1,2+1):
#y loops across oxygen atoms neighboring O1 and O2
	for y in range(1,6+1):
#z loops across Ce atoms surrounding O atoms
		for z in range (1,3+1):
			temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)
			temporary_conditions_list = eval("[Condition(coord=%s, species='U4_H_plus'),  \
							   Condition(coord= %s, species='U50_O')]" %(O_sites[x][1],O_sites_surrounding_O[x][y]))
			temporary_actions_list = eval("[Action(coord=%s, species='U50_O'),   \
							Action(coord=%s, species='U4_H_plus')]" %(O_sites[x][1],O_sites_surrounding_O[x][y]))
	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
			temporary_tst_interaction_energy = 0
			temporary_reactant_interaction_energy = 0
			temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
			temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
			temporary_tof_count_dict = {'F8p7':1}
			temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
			kmc_model.add_process(**temporary_kwargs_dictionary)

#Process for H2O molecular desorption (rxn 9.0)
#Again, only requires two processes for each of the Ce atoms in the cell.

current_process_name ='pF9p0'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
		temporary_name_string = 'pF9p0_a_%s' %(x)

		temporary_conditions_list = eval("[Condition(coord=%s, species='U26_H2O')]" %(Ce_sites[x][1]))

		temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[x][1]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'F9p0':1,'H2O_output_flux':1}

		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)

#Processes for H2O molecular Adsorption(rxn -9.0)
#This process requires two processes as it is an H2O molecule adsorbing on a Ce4+ site.

current_process_name ='pR9p0'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
		temporary_name_string = 'pR9p0_a_%s' %(x)

		temporary_conditions_list = eval("[Condition(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[x][1]))

		temporary_actions_list = eval("[Action(coord=%s, species='U26_H2O')]" %(Ce_sites[x][1]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(p_H2Ogas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2Okgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'R9p0':1}

		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)

		

		
		#116p1
#This process is for 2H@O -> H2O/V , there are two Ce4 that become Ce3+.
current_process_name ='pF9p8'
#Loops through O_1 and O_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central O for H_plus
	for y in range(1,6+1):
#This loops through neighboring Ce sites to O for Ce 3plus
		for i in range(1,3+1):
#This loops through neighboring Ce sites to O for Ce 3plus
			for j in range(1,3+1):
				if i == j or j < i:
					pass
				else:
					temporary_name_string = '%s_a_%s_%s_%s_%s' %(current_process_name,x,y,i,j)
					temporary_conditions_list = eval("[Condition(species='U4_H_plus', coord=%s), \
									Condition(species='U4_H_plus', coord=%s),\
									Condition(species='U1_Ce_4plus', coord=%s), \
									Condition(species='U1_Ce_4plus', coord=%s)]" %(O_sites[x][1],O_sites_surrounding_O[x][y],Ce_sites_surrounding_O[x][i],Ce_sites_surrounding_O[x][j]))

					temporary_actions_list = eval("[Action(species='U27_H2O_V', coord=%s), \
									Action(species='U50_O', coord=%s), \
									Action(species='U2_Ce_3plus', coord=%s), \
									Action(species='U2_Ce_3plus', coord=%s)]" %(O_sites[x][1],O_sites_surrounding_O[x][y],Ce_sites_surrounding_O[x][i],Ce_sites_surrounding_O[x][j]))
	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
					temporary_tst_interaction_energy = 0
					temporary_reactant_interaction_energy = 0
					temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
					temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
					temporary_tof_count_dict = {'F9p8':1}
					temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
					kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.
current_process_name ='pR9p8'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R9p8':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)


#Processes for Methanol Adsorption (rxn -15.0)
#This processes requires an empty Ce and an empty neighboring O (thus 2 Ce* 3 O = 6 processes).  For methanol adsorption, we have used the bridging species to occupy O.  This is for the H on the methanol molecule which is coordinated to the neighboring O.

current_process_name ='pR15p0'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O atoms neighboring Ce1 and Ce2
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)

		temporary_conditions_list = eval("[Condition(species='U1_Ce_4plus', coord=%s),   \
						   Condition(species='U50_O', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

		temporary_actions_list = eval("[Action(species=methanol_species_list[x][0], coord=%s),    \
						Action(species=methanol_species_list[x][1][y], coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))
#methanol_species_list[x][0],
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(p_CH3OHgas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_CH3OHkgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'R15p0':1}
    
		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)

#Processes for Methanol Desorption (rxn 15.0)
#This process requires 6 processes.  And results in an empty Ce and neighboring O.

current_process_name ='pF15p0'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O atoms neighboring Ce1 and Ce2
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)

		temporary_conditions_list = eval("[Condition(coord=%s, species=methanol_species_list[x][0]),   \
						   Condition(coord=%s, species=methanol_species_list[x][1][y])]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

		temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus'),   \
						Action(coord=%s, species='U50_O')]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'F15p0':1,'CH3OH_output_flux':1}
    
		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)

#Processes for Methanol ionic dissociation reactions activation energy is the same as that for desorption (for now)(rxn -15.1)
#This requires that a Ce is occupied by a methanol and a neighboring O is occupied by the bridging methanol species.  The H dissociates leaving Ce occupied by methoxy and O occupied by H+.  This requires 2Ce * 3O = 6 processes.

current_process_name ='pR15p1'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O atoms neighboring Ce1 and Ce2
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)

		temporary_conditions_list = eval("[Condition(coord=%s, species=methanol_species_list[x][0]),    \
						   Condition(coord=%s, species=methanol_species_list[x][1][y])]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

		temporary_actions_list = eval("[Action(coord=%s, species='U19_CH3O_ionic'),   \
						Action(coord=%s, species='U4_H_plus')]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'R15p1':1}
    
		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)

#This is the reverse of 15p1

current_process_name ='pF15p1'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O atoms neighboring Ce1 and Ce2
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)

		temporary_conditions_list = eval("[Condition(coord=%s, species='U19_CH3O_ionic'),    \
						   Condition(coord=%s, species='U4_H_plus')]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

		temporary_actions_list = eval("[Action(coord=%s, species=methanol_species_list[x][0]),   \
						Action(coord=%s, species=methanol_species_list[x][1][y])]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'F15p1':1}
    
		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)

		
		
#Processes for ionic methoxy migration from vacancy to Ce4+ (rxn -16.8)
#This process requires that a vacancy is filled with an ionic methoxy and there is an unoccupied Ce4+ available for Methoxy to occupy.  This will require only 6 processes for the 3 Ce atoms surrounding each O (3 Ce * 2 O = 6 total processes).

current_process_name ='pR16p8'
#x loops across O1 and O2 locations where the vacancies can be
for x in range(1,2+1):
#y loops across Ce atoms neighboring O1 and O2
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)

		temporary_conditions_list = eval("[Condition(coord=%s, species='U22_CH3O_ionic_V'),    \
						   Condition(coord=%s, species='U1_Ce_4plus')]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y]))

		temporary_actions_list = eval("[Action(coord=%s, species='U3_Vacancy'),   \
						Action(coord=%s, species='U19_CH3O_ionic')]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'R16p8':1}
    
		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)

#Processes for ionic methoxy migration to vacancy from Ce4+ (rxn 16.8)
#This is the reverse of -16.8 and requires a vacant O and an adjacent Ce4+ occupied by ionic methoxy.  Again, there should be 6 processes for each of the possible surrounding Ce4+ (2 V * 3 Ce = 6 total processes).

current_process_name ='pF16p8'
#x loops across O1 and O2 locations where the vacancies can be
for x in range(1,2+1):
#y loops across Ce atoms neighboring O1 and O2
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)

		temporary_conditions_list = eval("[Condition(coord=%s, species='U3_Vacancy'),   \
						   Condition(coord=%s, species='U19_CH3O_ionic')]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y]))

		temporary_actions_list = eval("[Action(coord=%s, species='U22_CH3O_ionic_V'),   \
						Action(coord=%s, species='U1_Ce_4plus')]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'F16p8':1}
    
		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)
		
		
#Processes for CH2O molecular desorption (rxn 18.0)
current_process_name ='pF18p0'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
		temporary_name_string = 'pF18p0_a_%s' %(x)
		temporary_conditions_list = eval("[Condition(coord=%s, species='U28_CH2O_Ce4plus')]" %(Ce_sites[x][1]))
		temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[x][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'F18p0':1,'CH2O_output_flux':1}
		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)
#This process does not actually occur, but is included for parallel data structures(rxn 10.0)

current_process_name ='pR18p0'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R18p0':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)


#### Processes 1##.# will implement the TPD mechanism reactions from the DFT team.
#F101p1  
#This reaction is for CH3OH @ Ce + O -> CH3O @ Ce + H @ O.  This reaction has three coadsorbates which are all CH3OH at Ce (this corresponds to 100% local coverage for the KMC).  This will require a CH3OH on a central Ce site which will bridge between the central Ce site and one of three neighboring O sites.  There are 6 additional Ce surrounding the central Ce that will all contain a methanol.
current_process_name ='pF101p1'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O1 and O2
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)
		temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][1],Ce_sites_surrounding_Ce[x][1],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][2],Ce_sites_surrounding_Ce[x][2],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][3],Ce_sites_surrounding_Ce[x][3],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][4],Ce_sites_surrounding_Ce[x][4],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][5],Ce_sites_surrounding_Ce[x][5],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][6],Ce_sites_surrounding_Ce[x][6]))

		temporary_actions_list = eval("[Action(species='U19_CH3O_ionic', coord=%s), \
						Action(species='U4_H_plus', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][1],Ce_sites_surrounding_Ce[x][1],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][2],Ce_sites_surrounding_Ce[x][2],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][3],Ce_sites_surrounding_Ce[x][3],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][4],Ce_sites_surrounding_Ce[x][4],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][5],Ce_sites_surrounding_Ce[x][5],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][6],Ce_sites_surrounding_Ce[x][6]))

		#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
		#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'F101p1':1}

		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

		kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction

current_process_name ='pR101p1'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O1 and O2
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)
		temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic', coord=%s), \
						Condition(species='U4_H_plus', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s), \
						Condition(species='%s', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][1],Ce_sites_surrounding_Ce[x][1],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][2],Ce_sites_surrounding_Ce[x][2],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][3],Ce_sites_surrounding_Ce[x][3],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][4],Ce_sites_surrounding_Ce[x][4],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][5],Ce_sites_surrounding_Ce[x][5],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][6],Ce_sites_surrounding_Ce[x][6]))

		temporary_actions_list = eval("[Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s), \
						Action(species='%s', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][1],Ce_sites_surrounding_Ce[x][1],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][2],Ce_sites_surrounding_Ce[x][2],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][3],Ce_sites_surrounding_Ce[x][3],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][4],Ce_sites_surrounding_Ce[x][4],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][5],Ce_sites_surrounding_Ce[x][5],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][6],Ce_sites_surrounding_Ce[x][6]))


		#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
		#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'R101p1':1}

		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

		kmc_model.add_process(**temporary_kwargs_dictionary)


#101p5
#This reaction is for CH3OH @ Ce + O -> CH3O @ Ce + H @ O.  The coadsorbates from DFT for this reaction are 2CH3OH@Ce.  Since there are 3 neighboring Ce sites in the DFT and 6 in the KMC, we will consider this to be 2/3 (DFT) -> 4/6 (KMC) neighboring Ce sites filled with CH3OH.  
current_process_name ='pF101p5'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
		for z in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
			for i in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
				for j in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
					for k in range(1,6+1):
						if z == i or z == j or z == k or i == j or i == k or j == k or i < z or j < i or k < j:
							pass
						else:
							temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k)

							temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][j],Ce_sites_surrounding_Ce[x][j],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][k],Ce_sites_surrounding_Ce[x][k]))

							temporary_actions_list = eval("[Action(species='U19_CH3O_ionic', coord=%s), \
											Action(species='U4_H_plus', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][j],Ce_sites_surrounding_Ce[x][j],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][k],Ce_sites_surrounding_Ce[x][k]))

	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
							temporary_tst_interaction_energy = 0
							temporary_reactant_interaction_energy = 0
							temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
					#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
							temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

							temporary_tof_count_dict = {'F101p5':1}

							temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

							kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction

current_process_name ='pR101p5'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
		for z in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
			for i in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
				for j in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
					for k in range(1,6+1):
						if z == i or z == j or z == k or i == j or i == k or j == k or i < z or j < i or k < j:
							pass
						else:
							temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k)

							temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic', coord=%s), \
											Condition(species='U4_H_plus', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][j],Ce_sites_surrounding_Ce[x][j],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][k],Ce_sites_surrounding_Ce[x][k]))

							temporary_actions_list = eval("[Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][j],Ce_sites_surrounding_Ce[x][j],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][k],Ce_sites_surrounding_Ce[x][k]))


	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
							temporary_tst_interaction_energy = 0
							temporary_reactant_interaction_energy = 0
							temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
					#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
							temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

							temporary_tof_count_dict = {'R101p5':1}

							temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

							kmc_model.add_process(**temporary_kwargs_dictionary)

#101p6
#This reaction is for CH3OH @ Ce + O -> CH3O @ Ce + H @ O.  The coadsorbates from DFT for this reaction are CH3OH@Ce, CH3O@Ce and H@O.  Since there are 3 neighboring Ce sites in the DFT and 6 in the KMC, we will consider this to be 1/3 (DFT) -> 2/6 (KMC) neighboring Ce sites filled with CH3OH, 1/3 (DFT) -> 2/6 (KMC) neighboring Ce sites filled with CH3O, and 1/3 neighboring O filled with H.  
current_process_name ='pF101p6'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O1 and O2
	for y in range(1,3+1):
#z loops across Ce sites neihboring the central Ce for a CH3OH location
		for z in range(1,6+1):
#i loops across Ce sites neihboring the central Ce for a CH3OH location
			for i in range(1,6+1):
#j loops across Ce sites neihboring the central Ce for a CH3O location
				for j in range(1,6+1):
#j loops across Ce sites neihboring the central Ce for a CH3O location
					for k in range(1,6+1):
#l loops across O sites neighboring the central Ce for an H location
						for l in range(1,3+1):
#We dont want any of the CH3OH or CH3O occupying the same position or the H occupying the same O site as the methanol briding species.
							if z == i or z == j or z == k or i == j or i == k or j == k or l == y or i < z or j < i or k < j:
								pass
							else:
								temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k,l)
								temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
												Condition(species='%s', coord=%s), \
												Condition(species='%s', coord=%s), \
												Condition(species='%s', coord=%s), \
												Condition(species='U19_CH3O_ionic', coord=%s), \
												Condition(species='U19_CH3O_ionic', coord=%s), \
												Condition(species='U4_H_plus', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k], O_sites_surrounding_Ce[x][l]))

								temporary_actions_list = eval("[Action(species='U19_CH3O_ionic', coord=%s), \
												Action(species='U4_H_plus', coord=%s), \
												Action(species='%s', coord=%s), \
												Action(species='%s', coord=%s), \
												Action(species='U19_CH3O_ionic', coord=%s), \
												Action(species='U19_CH3O_ionic', coord=%s), \
												Action(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k], O_sites_surrounding_Ce[x][l]))

								#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
								temporary_tst_interaction_energy = 0
								temporary_reactant_interaction_energy = 0
								temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
								#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
								temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

								temporary_tof_count_dict = {'F101p6':1}

								temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

								kmc_model.add_process(**temporary_kwargs_dictionary)
#The reverse reaction

current_process_name ='pR101p6'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O1 and O2
	for y in range(1,3+1):
#z loops across Ce sites neihboring the central Ce for a CH3OH location
		for z in range(1,6+1):
#i loops across Ce sites neihboring the central Ce for a CH3OH location
			for i in range(1,6+1):
#j loops across Ce sites neihboring the central Ce for a CH3O location
				for j in range(1,6+1):
#j loops across Ce sites neihboring the central Ce for a CH3O location
					for k in range(1,6+1):
#l loops across O sites neighboring the central Ce for an H location
						for l in range(1,3+1):
#We dont want any of the CH3OH or CH3O occupying the same position or the H occupying the same O site as the methanol briding species.
							if z == i or z == j or z == k or i == j or i == k or j == k or l == y or i < z or j < i or k < j:
								pass
							else:
								temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k,l)

								temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic', coord=%s), \
												Condition(species='U4_H_plus', coord=%s), \
												Condition(species='%s', coord=%s), \
												Condition(species='%s', coord=%s), \
												Condition(species='U19_CH3O_ionic', coord=%s), \
												Condition(species='U19_CH3O_ionic', coord=%s), \
												Condition(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k], O_sites_surrounding_Ce[x][l]))

								temporary_actions_list = eval("[Action(species='%s', coord=%s), \
												Action(species='%s', coord=%s), \
												Action(species='%s', coord=%s), \
												Action(species='%s', coord=%s), \
												Action(species='U19_CH3O_ionic', coord=%s), \
												Action(species='U19_CH3O_ionic', coord=%s), \
												Action(species='U4_H_plus', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k], O_sites_surrounding_Ce[x][l]))


								#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
								temporary_tst_interaction_energy = 0
								temporary_reactant_interaction_energy = 0
								temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
								#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
								temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

								temporary_tof_count_dict = {'R101p6':1}

								temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

								kmc_model.add_process(**temporary_kwargs_dictionary)

#102p6
#This reaction is for CH3O @ Ce + O -> CH2O @ Ce + H @ O.  The DFT reports coadsorbate species of 2CH3O@Ce and 3H@O.  This corresponds to 2/3 (DFT) -> 4/6 (KMC) CH3O @ Ce and 100% (2/3 + abstracted H from methoxy) coverage on the surrounding O sites.
current_process_name ='pF102p6'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O1 and O2
	for y in range(1,3+1):
#z loops across Ce sites surrounding Ce 1 or Ce2 for a CH3O location
		for z in range(1,6+1):
#i loops across Ce sites surrounding Ce 1 or Ce2 for a CH3O location
			for i in range(1,6+1):
#j loops across Ce sites surrounding Ce 1 or Ce2 for a CH3O location
				for j in range(1,6+1):
#k loops across Ce sites surrounding Ce 1 or Ce2 for a CH3O location
					for k in range(1,6+1):
#l loops across O sites surrounding Ce 1 or Ce2 for a H location
						for l in range(1,3+1):
#m loops across O sites surrounding Ce 1 or Ce2 for a H location
							for m in range(1,3+1):
								if z == i or z == j or z == k or i == j or i == k or j == k or l == m or l == y or m == y or m < l or i < z or j < i or k < j:
									pass
								else:
									temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k,l,m)
									temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U50_O', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U4_H_plus', coord=%s), \
													Condition(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k],O_sites_surrounding_Ce[x][l],O_sites_surrounding_Ce[x][m]))

									temporary_actions_list = eval("[Action(species='U28_CH2O_Ce4plus', coord=%s), \
													Action(species='U4_H_plus', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U4_H_plus', coord=%s), \
													Action(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k],O_sites_surrounding_Ce[x][l],O_sites_surrounding_Ce[x][m]))

									#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
									temporary_tst_interaction_energy = 0
									temporary_reactant_interaction_energy = 0
									temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
									#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
									temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

									temporary_tof_count_dict = {'F102p6':1}

									temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

									kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction

current_process_name ='pR102p6'
#x loops across Ce1 and Ce2
for x in range(1,2+1):
#y loops across O1 and O2
	for y in range(1,3+1):
#z loops across Ce sites surrounding Ce 1 or Ce2 for a CH3O location
		for z in range(1,6+1):
#i loops across Ce sites surrounding Ce 1 or Ce2 for a CH3O location
			for i in range(1,6+1):
#j loops across Ce sites surrounding Ce 1 or Ce2 for a CH3O location
				for j in range(1,6+1):
#k loops across Ce sites surrounding Ce 1 or Ce2 for a CH3O location
					for k in range(1,6+1):
#l loops across O sites surrounding Ce 1 or Ce2 for a H location
						for l in range(1,3+1):
#m loops across O sites surrounding Ce 1 or Ce2 for a H location
							for m in range(1,3+1):
								if z == i or z == j or z == k or i == j or i == k or j == k or l == m or l == y or m == y or m < l or i < z or j < i or k < j:
									pass
								else:
									temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k,l,m)
									temporary_conditions_list = eval("[Condition(species='U28_CH2O_Ce4plus', coord=%s), \
													Condition(species='U4_H_plus', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U4_H_plus', coord=%s), \
													Condition(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k],O_sites_surrounding_Ce[x][l],O_sites_surrounding_Ce[x][m]))

									temporary_actions_list = eval("[Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U50_O', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U4_H_plus', coord=%s), \
													Action(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k],O_sites_surrounding_Ce[x][l],O_sites_surrounding_Ce[x][m]))


									#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
									temporary_tst_interaction_energy = 0
									temporary_reactant_interaction_energy = 0
									temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
									#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
									temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

									temporary_tof_count_dict = {'R102p6':1}

									temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

									kmc_model.add_process(**temporary_kwargs_dictionary)


#102p8
#This process is for CH bond breaking CH3O@Ce + O -> CH2O@Ce + H@O.  The origianl version of this was R16p1.  However, we will now assume that all of this takes place on a Ce4+ and results in a Hplus and two Ce3plus are created.  No coadsorbate species exist for this reaction.
current_process_name ='pF102p8'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce neighboring Ce for Ce3+
		for z in range(1,6+1):
#This loops through Ce neighboring Ce for Ce3+
			for i in range(1,6+1):
				if i == z or i < z:
					pass
				else:
					temporary_name_string = '%s_a_%s_%s_%s_%s' %(current_process_name,x,y,z,i)

					temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic' ,coord=%s),   \
									   Condition(species='U50_O' ,coord=%s), \
									Condition(species='U1_Ce_4plus' ,coord=%s),   \
									Condition(species='U1_Ce_4plus' ,coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i]))

					temporary_actions_list = eval("[Action(species='U28_CH2O_Ce4plus' ,coord=%s),     \
									Action(species='U4_H_plus' ,coord=%s),     \
									Action(species='U2_Ce_3plus' ,coord=%s),     \
									Action(species='U2_Ce_3plus' ,coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i]))

			#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
					temporary_tst_interaction_energy = 0
					temporary_reactant_interaction_energy = 0
					temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
			#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
					temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

					temporary_tof_count_dict = {'F102p8':1}

					temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

					kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction

current_process_name ='pR102p8'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce neighboring Ce for Ce3+
		for z in range(1,6+1):
#This loops through Ce neighboring Ce for Ce3+
			for i in range(1,6+1):
				if i == z or i < z:
					pass
				else:
					temporary_name_string = '%s_a_%s_%s_%s_%s' %(current_process_name,x,y,z,i)


					temporary_conditions_list = eval("[Condition(species='U28_CH2O_Ce4plus' ,coord=%s),     \
									Condition(species='U4_H_plus' ,coord=%s),     \
									Condition(species='U2_Ce_3plus' ,coord=%s),     \
									Condition(species='U2_Ce_3plus' ,coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i]))

					temporary_actions_list = eval("[Action(species='U19_CH3O_ionic' ,coord=%s),   \
									   Action(species='U50_O' ,coord=%s), \
									Action(species='U1_Ce_4plus' ,coord=%s),   \
									Action(species='U1_Ce_4plus' ,coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i]))

			#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
					temporary_tst_interaction_energy = 0
					temporary_reactant_interaction_energy = 0
					temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
			#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
					temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

					temporary_tof_count_dict = {'R102p8':1}

					temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

					kmc_model.add_process(**temporary_kwargs_dictionary)

#103p6
#This process is for 2CH3O@Ce + O -> CH3OH@Ce + CH2O@Ce . will need an open O site for the CH3OH bridge.
current_process_name ='pF103p6'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central Ce4+ for the CH2O location
	for y in range(1,6+1):
#This loops through the O atoms neighboring Ce for one H+ location
		for z in range(1,3+1):
			temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)

			temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic' ,coord=%s),   \
					   Condition(species='U19_CH3O_ionic' ,coord=%s),   \
					   Condition(species='U50_O' ,coord=%s)]" %(Ce_sites[x][1],Ce_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))

			temporary_actions_list = eval("[Action(species='%s' ,coord=%s),     \
					Action(species='U28_CH2O_Ce4plus' ,coord=%s),     \
					Action(species='%s',coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],Ce_sites_surrounding_Ce[x][y],methanol_species_list[x][1][z],O_sites_surrounding_Ce[x][z]))

	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
			temporary_tst_interaction_energy = 0
			temporary_reactant_interaction_energy = 0
			temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
			temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

			temporary_tof_count_dict = {'F103p6':1}

			temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

			kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction

current_process_name ='pR103p6'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central Ce4+ for the CH2O location
	for y in range(1,6+1):
#This loops through the O atoms neighboring Ce for one H+ location
		for z in range(1,3+1):
			temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)

			temporary_conditions_list = eval("[Condition(species='%s' ,coord=%s),     \
					Condition(species='U28_CH2O_Ce4plus' ,coord=%s),     \
					Condition(species='%s',coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],Ce_sites_surrounding_Ce[x][y],methanol_species_list[x][1][z],O_sites_surrounding_Ce[x][z]))


			temporary_actions_list = eval("[Action(species='U19_CH3O_ionic' ,coord=%s),   \
					   Action(species='U19_CH3O_ionic' ,coord=%s),   \
					   Action(species='U50_O' ,coord=%s)]" %(Ce_sites[x][1],Ce_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))


	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
			temporary_tst_interaction_energy = 0
			temporary_reactant_interaction_energy = 0
			temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
			temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

			temporary_tof_count_dict = {'R103p6':1}

			temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

			kmc_model.add_process(**temporary_kwargs_dictionary)

#104p7
#This process is for CH3OH@Ce + H@O -> CH3O@Ce + H2O@V .  There are no coadsorbate species but there is an H occupying a neighboring O.
#We are modifying this on 7/28/16 to require one empty site to be nearby.
current_process_name ='pF104p7'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through the O atoms neighboring Ce for one for the CH3OH briding location location
	for y in range(1,3+1):
#This loops through the O atoms neighboring O neighboring Ce for one H+ location
		for z in range(1,6+1):
			#this loops across cerium sites neighboring the central one methanol is on, and makes sure one is empty.
			for e in range(1,6+1):
				temporary_name_string = '%s_a_%s_%s_%s_%s' %(current_process_name,x,y,z,e)

				temporary_conditions_list = eval("[Condition(species='%s' ,coord=%s),   \
						   Condition(species='%s' ,coord=%s),   \
						   Condition(species='U4_H_plus' ,coord=%s), \
						   Condition(species='U1_Ce_4plus', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_O_surrounding_Ce1_or_Ce2[x][y][z], Ce_sites_surrounding_Ce[x][e]))

				temporary_actions_list = eval("[Action(species='U19_CH3O_ionic' ,coord=%s),     \
						Action(species='U50_O' ,coord=%s),     \
						Action(species='U27_H2O_V' ,coord=%s), \
						Action(species='U1_Ce_4plus', coord=%s) ]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_O_surrounding_Ce1_or_Ce2[x][y][z], Ce_sites_surrounding_Ce[x][e]))

		#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
				temporary_tst_interaction_energy = 0
				temporary_reactant_interaction_energy = 0
				temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
		#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
				temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

				temporary_tof_count_dict = {'F104p7':1}

				temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

				kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure. But we do not need to require an empty site for water to jump back in.
current_process_name ='pR104p7'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through the O atoms neighboring Ce for one for the CH3OH briding location location
	for y in range(1,3+1):
#This loops through the O atoms neighboring O neighboring Ce for one H+ location
		for z in range(1,6+1):
			temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)

			temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic' ,coord=%s),     \
					Condition(species='U50_O' ,coord=%s),     \
					Condition(species='U27_H2O_V' ,coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_O_surrounding_Ce1_or_Ce2[x][y][z]))


			temporary_actions_list = eval("[Action(species='%s' ,coord=%s),   \
					   Action(species='%s' ,coord=%s),   \
					   Action(species='U4_H_plus' ,coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_O_surrounding_Ce1_or_Ce2[x][y][z]))


	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
			temporary_tst_interaction_energy = 0
			temporary_reactant_interaction_energy = 0
			temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
			temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

			temporary_tof_count_dict = {'R104p7':1}

			temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

			kmc_model.add_process(**temporary_kwargs_dictionary)

#105p4
#This process is for CH3O@Ce + H2O@V -> CH3O@V + H2O@Ce .  There are no coadsorbate species.  The water and methoxy switch places, but it is not an option for the methoxy to push the water to a totally different site (this is different from Jonathan's DFT calculation).
current_process_name ='pF105p4'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through the O atoms neighboring Ce for one for the CH3O location
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)

		temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic' ,coord=%s),   \
				   Condition(species='U27_H2O_V' ,coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

		temporary_actions_list = eval("[Action(species='U26_H2O' ,coord=%s),     \
				Action(species='U22_CH3O_ionic_V' ,coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'F105p4':1}

		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

		kmc_model.add_process(**temporary_kwargs_dictionary)

#the reverse reaction

current_process_name ='pR105p4'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through the O atoms neighboring Ce for one for the CH3O location
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s' %(current_process_name,x,y)

		temporary_conditions_list = eval("[Condition(species='U26_H2O' ,coord=%s),     \
				Condition(species='U22_CH3O_ionic_V' ,coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

		temporary_actions_list = eval("[Action(species='U19_CH3O_ionic' ,coord=%s),   \
				   Action(species='U27_H2O_V' ,coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'R105p4':1}

		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

		kmc_model.add_process(**temporary_kwargs_dictionary)



#106p5
#This process is for CH3OH desorption CH3OH@Ce -> CH3OH(g) + Ce.  There are two coadsorbate CH3OH at neighboring Ce sites from the DFT.  From this, 2/3 (DFT) -> 4/6 (KMC) neighboring sites will be filled with CH3OH. 
current_process_name ='pF106p5'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
		for z in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
			for i in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
				for j in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
					for k in range(1,6+1):
						if z == i or z == j or z == k or i == j or i == k or j == k or i < z or j < i or k < j:
							pass
						else:
							temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k)

							temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][j],Ce_sites_surrounding_Ce[x][j],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][k],Ce_sites_surrounding_Ce[x][k]))

							temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
											Action(species='U50_O', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][j],Ce_sites_surrounding_Ce[x][j],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][k],Ce_sites_surrounding_Ce[x][k]))

	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
							temporary_tst_interaction_energy = 0
							temporary_reactant_interaction_energy = 0
							temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
					#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
							temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

							temporary_tof_count_dict = {'F106p5':1,'CH3OH_output_flux':1}

							temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

							kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.

current_process_name ='pR106p5'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R106p5':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)

#106p6
#This process is for CH3OH desorption CH3OH@Ce -> CH3OH(g) + Ce.  There are three coadsorbate species: CH3OH@Ce, CH3O@Ce and H@O.  This translates to 1/3 (DFT) -> 2/6 (KMC) CH3OH, 1/3 (DFT) -> 2/6 (KMC) CH3O and there will be 1 out of 3 neighboring O filled with H.
current_process_name ='pF106p6'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
		for z in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
			for i in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
				for j in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
					for k in range(1,6+1):
#This loops through O atoms neighboring Ce for Hplus location
						for l in range(1,3+1):
							if z == i or z == j or z == k or i == j or i == k or j == k or l == y or i < z or j < i or k < j:
								pass
							else:
								temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k,l)

								temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
												Condition(species='%s', coord=%s), \
												Condition(species='%s', coord=%s), \
												Condition(species='%s', coord=%s), \
												Condition(species='U19_CH3O_ionic', coord=%s), \
												Condition(species='U19_CH3O_ionic', coord=%s), \
												Condition(species='U4_H_plus', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k],O_sites_surrounding_Ce[x][l]))

								temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
												Action(species='U50_O', coord=%s), \
												Action(species='%s', coord=%s), \
												Action(species='%s', coord=%s), \
												Action(species='U19_CH3O_ionic', coord=%s), \
												Action(species='U19_CH3O_ionic', coord=%s), \
												Action(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][z],Ce_sites_surrounding_Ce[x][z],methanol_Ce_species_surrounding_Ce1_or_Ce2[x][i],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k],O_sites_surrounding_Ce[x][l]))

		#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
								temporary_tst_interaction_energy = 0
								temporary_reactant_interaction_energy = 0
								temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
						#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
								temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

								temporary_tof_count_dict = {'F106p6':1,'CH3OH_output_flux':1}

								temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

								kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.

current_process_name ='pR106p6'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R106p6':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)


#106p7
#This process is for CH3OH desorption CH3OH@Ce -> CH3OH(g) + Ce.  There are two coadsorbate species: CH3O@Ce and H@O.  This translates to 2/3 (DFT) -> 4/6 (KMC) CH3O, 2/3 (DFT) -> 2/3 (KMC) H@O.
current_process_name ='pF106p7'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
		for z in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
			for i in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
				for j in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
					for k in range(1,6+1):
#This loops through O atoms neighboring Ce for Hplus location
						for l in range(1,3+1):
#This loops through O atoms neighboring Ce for Hplus location
							for m in range(1,3+1):
								if z == i or z == j or z == k or i == j or i == k or j == k or l == y or l == m or m == y or i < z or j < i or k < j or m < l:
									pass
								else:
									temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k,l,m)

									temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
													Condition(species='%s', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U19_CH3O_ionic', coord=%s), \
													Condition(species='U4_H_plus', coord=%s), \
													Condition(species='U4_H_plus', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k],O_sites_surrounding_Ce[x][l],O_sites_surrounding_Ce[x][m]))

									temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
													Action(species='U50_O', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U19_CH3O_ionic', coord=%s), \
													Action(species='U4_H_plus', coord=%s), \
													Action(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j],Ce_sites_surrounding_Ce[x][k],O_sites_surrounding_Ce[x][l],O_sites_surrounding_Ce[x][m]))

			#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
									temporary_tst_interaction_energy = 0
									temporary_reactant_interaction_energy = 0
									temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
							#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
									temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

									temporary_tof_count_dict = {'F106p7':1,'CH3OH_output_flux':1}

									temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

									kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.

current_process_name ='pR106p7'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R106p7':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)


#108p2
#This process is for H abstraction CH3OH@Ce + O -> Ch3O@Ce + H@O.  There are two coadsorbate species: CH3O@Ce and CH3O@V.  This translates to 1/3 (DFT) -> 2/6 (KMC) CH3O, 1/3 (DFT) -> 1/3 (KMC) CH3O@V.
current_process_name ='pF108p2'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
		for z in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
			for i in range(1,6+1):
#This loops through O atoms neighboring Ce for CH3O@V location
				for j in range(1,3+1):
					if z == i or j == y or i < z :
						pass
					else:
						temporary_name_string = '%s_a_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j)

						temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
										Condition(species='%s', coord=%s), \
										Condition(species='U19_CH3O_ionic', coord=%s), \
										Condition(species='U19_CH3O_ionic', coord=%s), \
										Condition(species='U22_CH3O_ionic_V', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))

						temporary_actions_list = eval("[Action(species='U19_CH3O_ionic', coord=%s), \
										Action(species='U4_H_plus', coord=%s), \
										Action(species='U19_CH3O_ionic', coord=%s), \
										Action(species='U19_CH3O_ionic', coord=%s), \
										Action(species='U22_CH3O_ionic_V', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
						temporary_tst_interaction_energy = 0
						temporary_reactant_interaction_energy = 0
						temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
				#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
						temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

						temporary_tof_count_dict = {'F108p2':1}

						temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

						kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction

current_process_name ='pR108p2'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
		for z in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3OH location
			for i in range(1,6+1):
#This loops through O atoms neighboring Ce for CH3O@V location
				for j in range(1,3+1):
					if z == i or j == y or i < z :
						pass
					else:
						temporary_name_string = '%s_a_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j)

						temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic', coord=%s), \
										Condition(species='U4_H_plus', coord=%s), \
										Condition(species='U19_CH3O_ionic', coord=%s), \
										Condition(species='U19_CH3O_ionic', coord=%s), \
										Condition(species='U22_CH3O_ionic_V', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))

						temporary_actions_list = eval("[Action(species='%s', coord=%s), \
										Action(species='%s', coord=%s), \
										Action(species='U19_CH3O_ionic', coord=%s), \
										Action(species='U19_CH3O_ionic', coord=%s), \
										Action(species='U22_CH3O_ionic_V', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
						temporary_tst_interaction_energy = 0
						temporary_reactant_interaction_energy = 0
						temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
				#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
						temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

						temporary_tof_count_dict = {'R108p2':1}

						temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

						kmc_model.add_process(**temporary_kwargs_dictionary)


#108p4
#This process is for H abstraction CH3OH@Ce + O + V -> Ch3O@V + H@O + Ce. There are no coadsorbate species. 
current_process_name ='pF108p4'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through O atoms neighboring Ce for CH3O@V location
		for z in range(1,3+1):
			if z == y:
				pass
			else:
				temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)
				temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
								Condition(species='%s', coord=%s), \
								Condition(species='U3_Vacancy', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))
				temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
								Action(species='U4_H_plus', coord=%s), \
								Action(species='U22_CH3O_ionic_V', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
				temporary_tst_interaction_energy = 0
				temporary_reactant_interaction_energy = 0
				temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
				#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
				temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
				temporary_tof_count_dict = {'F108p4':1}
				temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
				kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction

current_process_name ='pR108p4'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through O atoms neighboring Ce for CH3O@V location
		for z in range(1,3+1):
			if z == y:
				pass
			else:
				temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)

				temporary_conditions_list = eval("[Condition(species='U1_Ce_4plus', coord=%s), \
								Condition(species='U4_H_plus', coord=%s), \
								Condition(species='U22_CH3O_ionic_V', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))


				temporary_actions_list = eval("[Action(species='%s', coord=%s), \
								Action(species='%s', coord=%s), \
								Action(species='U3_Vacancy', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
				temporary_tst_interaction_energy = 0
				temporary_reactant_interaction_energy = 0
				temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
				#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
				temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
				temporary_tof_count_dict = {'R108p4':1}
				temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
				kmc_model.add_process(**temporary_kwargs_dictionary)

#109p2
#This process is for CH3OH desorption CH3OH@Ce + O -> CH3OH(g).  There are two coadsorbate species: CH3O@Ce and CH3O@V.  This translates to 1/3 (DFT) -> 2/6 (KMC) CH3O, 1/3 (DFT) -> 1/3 (KMC) CH3O@V.
current_process_name ='pF109p2'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3O location
		for z in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3O location
			for i in range(1,6+1):
#This loops through O atoms neighboring Ce for CH3O@V location
				for j in range(1,3+1):
					if z == i or j == y or i < z:
						pass
					else:
						temporary_name_string = '%s_a_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j)
						temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
										Condition(species='%s', coord=%s), \
										Condition(species='U19_CH3O_ionic', coord=%s), \
										Condition(species='U19_CH3O_ionic', coord=%s), \
										Condition(species='U22_CH3O_ionic_V', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))
						temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
										Action(species='U50_O', coord=%s), \
										Action(species='U19_CH3O_ionic', coord=%s), \
										Action(species='U19_CH3O_ionic', coord=%s), \
										Action(species='U22_CH3O_ionic_V', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],Ce_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
						temporary_tst_interaction_energy = 0
						temporary_reactant_interaction_energy = 0
						temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
				#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
						temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
						temporary_tof_count_dict = {'F109p2':1, 'CH3OH_output_flux':1}
						temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
						kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.

current_process_name ='pR109p2'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R109p2':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)


#109p3
#This process is for CH3OH desorption CH3OH@Ce + O -> CH3O(g) with spectator CH2O/V.   1/3 (DFT) -> 1/3 (KMC) V.
current_process_name ='pF109p3'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through O atoms neighboring Ce for V location
		for z in range(1,3+1):
			if z == y:
				pass
			else:
				temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)
				temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
								Condition(species='%s', coord=%s), \
								Condition(species='U29_CH2O_V', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))
				temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
								Action(species='U50_O', coord=%s), \
								Action(species='U29_CH2O_V', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
				temporary_tst_interaction_energy = 0
				temporary_reactant_interaction_energy = 0
				temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
				temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
				temporary_tof_count_dict = {'F109p3':1, 'CH3OH_output_flux':1}
				temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
				kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.

current_process_name ='pR109p3'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R109p3':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)



#109p4
#This process is for CH3OH desorption CH3OH@Ce + O -> CH3O(g).   1/3 (DFT) -> 1/3 (KMC) V.
current_process_name ='pF109p4'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+
	for y in range(1,3+1):
#This loops through O atoms neighboring Ce for V location
		for z in range(1,3+1):
			if z == y:
				pass
			else:
				temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)
				temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
								Condition(species='%s', coord=%s), \
								Condition(species='U3_Vacancy', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))
				temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
								Action(species='U50_O', coord=%s), \
								Action(species='U3_Vacancy', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
				temporary_tst_interaction_energy = 0
				temporary_reactant_interaction_energy = 0
				temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
				temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
				temporary_tof_count_dict = {'F109p4':1, 'CH3OH_output_flux':1}
				temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
				kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.

current_process_name ='pR109p4'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R109p4':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)


#110p3
#This process is for H2O desorption H2O@Ce -> H2O (g) + Ce.  There are two coadsorbate species: CH3O@Ce and CH30@V.  There are 1/3 (DFT) -> 2/6 (KMC) CH3O@Ce and 1/3 CH3O@V
current_process_name ='pF110p3'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3O
	for y in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3O
		for z in range(1,6+1):
#Loops through neighboring O atoms for CH3O on V
			for i in range(1,3+1):
				if z == y or z < y:
					pass
				else:
					temporary_name_string = '%s_a_%s_%s_%s_%s' %(current_process_name,x,y,z,i)
					temporary_conditions_list = eval("[Condition(species='U26_H2O', coord=%s), \
									Condition(species='U19_CH3O_ionic', coord=%s), \
									Condition(species='U19_CH3O_ionic', coord=%s), \
									Condition(species='U22_CH3O_ionic_V', coord=%s)]" %(Ce_sites[x][1],Ce_sites_surrounding_Ce[x][y], Ce_sites_surrounding_Ce[x][z],O_sites_surrounding_Ce[x][i]))
					temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
									Action(species='U19_CH3O_ionic', coord=%s), \
									Action(species='U19_CH3O_ionic', coord=%s), \
									Action(species='U22_CH3O_ionic_V', coord=%s)]" %(Ce_sites[x][1],Ce_sites_surrounding_Ce[x][y], Ce_sites_surrounding_Ce[x][z],O_sites_surrounding_Ce[x][i]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
					temporary_tst_interaction_energy = 0
					temporary_reactant_interaction_energy = 0
					temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
					temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
					temporary_tof_count_dict = {'F110p3':1, 'H2O_output_flux':1}
					temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
					kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.

current_process_name ='pR110p3'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R110p3':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)

#110p4
#This process is for H2O desorption H2O@Ce -> H2O (g) + Ce.  There are two coadsorbate species: CH3O@Ce.  There are 1/3 (DFT) -> 2/6 (KMC) CH3O@Ce
current_process_name ='pF110p4'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3O
	for y in range(1,6+1):
#This loops through Ce atoms neighboring Ce for CH3O
		for z in range(1,6+1):
#Loops through neighboring O atoms for CH3O on V
			if z == y or z < y:
				pass
			else:
				temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)
				temporary_conditions_list = eval("[Condition(species='U26_H2O', coord=%s), \
								Condition(species='U19_CH3O_ionic', coord=%s), \
								Condition(species='U19_CH3O_ionic', coord=%s)]" %(Ce_sites[x][1],Ce_sites_surrounding_Ce[x][y], Ce_sites_surrounding_Ce[x][z]))
				temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
								Action(species='U19_CH3O_ionic', coord=%s), \
								Action(species='U19_CH3O_ionic', coord=%s)]" %(Ce_sites[x][1],Ce_sites_surrounding_Ce[x][y], Ce_sites_surrounding_Ce[x][z]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
				temporary_tst_interaction_energy = 0
				temporary_reactant_interaction_energy = 0
				temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
				temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
				temporary_tof_count_dict = {'F110p4':1, 'H2O_output_flux':1}
				temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
				kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.

current_process_name ='pR110p4'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R110p4':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)

#111p2
#This process is for CH3O@Ce + CH3O@V -> CH3OH@Ce CH2O@V.  There are two coadsorbate species: CH3O@Ce and H@O.  There are 1/3 (DFT) -> 2/6 (KMC) CH3O@Ce and 1/3 H@O
current_process_name ='pF111p2'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3OH bridge
	for y in range(1,3+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3OH bridge
		for k in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3O
			for z in range(1,6+1):
	#This loops through Ce atoms neighboring Ce for CH3O
				for i in range(1,6+1):
	#This loops through O atoms neighboring Ce for H
					for j in range(1,3+1):
	#Loops through neighboring O atoms for CH3O on V
						if z == i or j == y or i < z or y == k or k == j:
							pass
						else:
							temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,k,z,i,j)
							temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic', coord=%s), \
											Condition(species='U50_O', coord=%s), \
											Condition(species='U22_CH3O_ionic_V', coord=%s), \
											Condition(species='U19_CH3O_ionic', coord=%s), \
											Condition(species='U19_CH3O_ionic', coord=%s), \
											Condition(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][k],Ce_sites_surrounding_Ce[x][z], Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))
							temporary_actions_list = eval("[Action(species='%s', coord=%s), \
											Action(species='%s', coord=%s), \
											Action(species='U29_CH2O_V', coord=%s), \
											Action(species='U19_CH3O_ionic', coord=%s), \
											Action(species='U19_CH3O_ionic', coord=%s), \
											Action(species='U4_H_plus', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][k],Ce_sites_surrounding_Ce[x][z], Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
							temporary_tst_interaction_energy = 0
							temporary_reactant_interaction_energy = 0
							temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
				#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
							temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
							temporary_tof_count_dict = {'F111p2':1}
							temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
							kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction

current_process_name ='pR111p2'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3OH bridge
	for y in range(1,3+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3OH bridge
		for k in range(1,3+1):
#This loops through Ce atoms neighboring Ce for CH3O
			for z in range(1,6+1):
	#This loops through Ce atoms neighboring Ce for CH3O
				for i in range(1,6+1):
	#This loops through O atoms neighboring Ce for H
					for j in range(1,3+1):
	#Loops through neighboring O atoms for CH3O on V
						if z == i or j == y or i < z or y == k or k == j:
							pass
						else:
							temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,k,z,i,j)

							temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
											Condition(species='%s', coord=%s), \
											Condition(species='U29_CH2O_V', coord=%s), \
											Condition(species='U19_CH3O_ionic', coord=%s), \
											Condition(species='U19_CH3O_ionic', coord=%s), \
											Condition(species='U4_H_plus', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][k],Ce_sites_surrounding_Ce[x][z], Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))

							temporary_actions_list = eval("[Action(species='U19_CH3O_ionic', coord=%s), \
											Action(species='U50_O', coord=%s), \
											Action(species='U22_CH3O_ionic_V', coord=%s), \
											Action(species='U19_CH3O_ionic', coord=%s), \
											Action(species='U19_CH3O_ionic', coord=%s), \
											Action(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][k],Ce_sites_surrounding_Ce[x][z], Ce_sites_surrounding_Ce[x][i],O_sites_surrounding_Ce[x][j]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
							temporary_tst_interaction_energy = 0
							temporary_reactant_interaction_energy = 0
							temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
				#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
							temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
							temporary_tof_count_dict = {'R111p2':1}
							temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
							kmc_model.add_process(**temporary_kwargs_dictionary)

#111p3
#This process is for CH3O@Ce + CH3O@V -> CH3OH@Ce + CH2O@V.  There are no coadsorbate species.
current_process_name ='pF111p3'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3OH bridge
	for y in range(1,3+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3OH bridge
		for k in range(1,3+1):
			if y == k:
				pass
			else:
				temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,k)
				temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic', coord=%s), \
								Condition(species='U50_O', coord=%s), \
								Condition(species='U22_CH3O_ionic_V', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][k]))
				temporary_actions_list = eval("[Action(species='%s', coord=%s), \
								Action(species='%s', coord=%s), \
								Action(species='U29_CH2O_V', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][k]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
				temporary_tst_interaction_energy = 0
				temporary_reactant_interaction_energy = 0
				temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
				temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
				temporary_tof_count_dict = {'F111p3':1}
				temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
				kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction

current_process_name ='pR111p3'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3OH bridge
	for y in range(1,3+1):
#This loops through all possible Ce neighbors of the central Ce4+ for CH3OH bridge
		for k in range(1,3+1):
			if y == k:
				pass
			else:
				temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,k)

				temporary_conditions_list = eval("[Condition(species='%s', coord=%s), \
								Condition(species='%s', coord=%s), \
								Condition(species='U29_CH2O_V', coord=%s)]" %(methanol_species_list[x][0],Ce_sites[x][1],methanol_species_list[x][1][y],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][k]))


				temporary_actions_list = eval("[Action(species='U19_CH3O_ionic', coord=%s), \
								Action(species='U50_O', coord=%s), \
								Action(species='U22_CH3O_ionic_V', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][k]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
				temporary_tst_interaction_energy = 0
				temporary_reactant_interaction_energy = 0
				temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
				temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
				temporary_tof_count_dict = {'R111p3':1}
				temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
				kmc_model.add_process(**temporary_kwargs_dictionary)


#112p3
#This process is for CH3O@Ce + O -> CH2O@Ce + H@O.  There is one coadsorbate species: CH3O@V.  This corresponds to 1/3 CH3O on O sites.
current_process_name ='pF112p3'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+ for CH3O@V
	for y in range(1,3+1):
#This loops through neighboring O sites for H plus
		for z in range(1,3+1):
#This loops through neighboring Ce sites for Ce3 plus
			for i in range(1,6+1):
#This loops through neighboring Ce sites for Ce3 plus
				for j in range(1,6+1):
					if y == z or i == j or j < i:
						pass
					else:
						temporary_name_string = '%s_a_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j)
						temporary_conditions_list = eval("[Condition(species='U19_CH3O_ionic', coord=%s), \
										Condition(species='U22_CH3O_ionic_V', coord=%s), \
										Condition(species='U50_O', coord=%s), \
										Condition(species='U1_Ce_4plus', coord=%s), \
										Condition(species='U1_Ce_4plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j]))
						temporary_actions_list = eval("[Action(species='U28_CH2O_Ce4plus', coord=%s), \
										Action(species='U22_CH3O_ionic_V', coord=%s), \
										Action(species='U4_H_plus', coord=%s), \
										Action(species='U2_Ce_3plus', coord=%s), \
										Action(species='U2_Ce_3plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j]))
		#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
						temporary_tst_interaction_energy = 0
						temporary_reactant_interaction_energy = 0
						temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
		#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
						temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
						temporary_tof_count_dict = {'F112p3':1}
						temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
						kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction
current_process_name ='pR112p3'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+ for CH3O@V
	for y in range(1,3+1):
#This loops through neighboring O sites for H plus
		for z in range(1,3+1):
#This loops through neighboring Ce sites for Ce3 plus
			for i in range(1,6+1):
#This loops through neighboring Ce sites for Ce3 plus
				for j in range(1,6+1):
					if y == z or i == j or j < i:
						pass
					else:
						temporary_name_string = '%s_a_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j)

						temporary_conditions_list = eval("[Condition(species='U28_CH2O_Ce4plus', coord=%s), \
										Condition(species='U22_CH3O_ionic_V', coord=%s), \
										Condition(species='U4_H_plus', coord=%s), \
										Condition(species='U2_Ce_3plus', coord=%s), \
										Condition(species='U2_Ce_3plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j]))


						temporary_actions_list = eval("[Action(species='U19_CH3O_ionic', coord=%s), \
										Action(species='U22_CH3O_ionic_V', coord=%s), \
										Action(species='U50_O', coord=%s), \
										Action(species='U1_Ce_4plus', coord=%s), \
										Action(species='U1_Ce_4plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z],Ce_sites_surrounding_Ce[x][i],Ce_sites_surrounding_Ce[x][j]))
		#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
						temporary_tst_interaction_energy = 0
						temporary_reactant_interaction_energy = 0
						temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
		#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
						temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
						temporary_tof_count_dict = {'R112p3':1}
						temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
						kmc_model.add_process(**temporary_kwargs_dictionary)

#112p7
#This process is for CH3O@V + O -> CH2O/v + H@O.  There are no coadsorbate species, but two Ce4plus will become Ce3+ for charge balance.
current_process_name ='pF112p7'
#Loops through O_1 and O_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central O for CH2O@V
	for y in range(1,6+1):
#This loops through neighboring Ce sites for Ce3+
		for z in range(1,3+1):
#This loops through neighboring Ce sites for Ce3+
			for i in range(1,3+1):
				if z == i or i < z:
					pass
				else:
					temporary_name_string = '%s_a_%s_%s_%s_%s' %(current_process_name,x,y,z,i)
					temporary_conditions_list = eval("[Condition(species='U22_CH3O_ionic_V', coord=%s), \
									Condition(species='U50_O', coord=%s), \
									Condition(species='U1_Ce_4plus', coord=%s), \
									Condition(species='U1_Ce_4plus', coord=%s)]" %(O_sites[x][1],O_sites_surrounding_O[x][y],Ce_sites_surrounding_O[x][z],Ce_sites_surrounding_O[x][i]))

					temporary_actions_list = eval("[Action(species='U29_CH2O_V', coord=%s), \
									Action(species='U4_H_plus', coord=%s), \
									Action(species='U2_Ce_3plus', coord=%s), \
									Action(species='U2_Ce_3plus', coord=%s)]" %(O_sites[x][1],O_sites_surrounding_O[x][y],Ce_sites_surrounding_O[x][z],Ce_sites_surrounding_O[x][i]))
	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
					temporary_tst_interaction_energy = 0
					temporary_reactant_interaction_energy = 0
					temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
					temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
					temporary_tof_count_dict = {'F112p7':1}
					temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
					kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction
current_process_name ='pR112p7'
#Loops through O_1 and O_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central O for CH2O@V
	for y in range(1,6+1):
#This loops through neighboring Ce sites for Ce3+
		for z in range(1,3+1):
#This loops through neighboring Ce sites for Ce3+
			for i in range(1,3+1):
				if z == i or i < z:
					pass
				else:
					temporary_name_string = '%s_a_%s_%s_%s_%s' %(current_process_name,x,y,z,i)

					temporary_conditions_list = eval("[Condition(species='U29_CH2O_V', coord=%s), \
									Condition(species='U4_H_plus', coord=%s), \
									Condition(species='U2_Ce_3plus', coord=%s), \
									Condition(species='U2_Ce_3plus', coord=%s)]" %(O_sites[x][1],O_sites_surrounding_O[x][y],Ce_sites_surrounding_O[x][z],Ce_sites_surrounding_O[x][i]))

					temporary_actions_list = eval("[Action(species='U22_CH3O_ionic_V', coord=%s), \
									Action(species='U50_O', coord=%s), \
									Action(species='U1_Ce_4plus', coord=%s), \
									Action(species='U1_Ce_4plus', coord=%s)]" %(O_sites[x][1],O_sites_surrounding_O[x][y],Ce_sites_surrounding_O[x][z],Ce_sites_surrounding_O[x][i]))

	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
					temporary_tst_interaction_energy = 0
					temporary_reactant_interaction_energy = 0
					temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
					temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
					temporary_tof_count_dict = {'R112p7':1}
					temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
					kmc_model.add_process(**temporary_kwargs_dictionary)


#113p1
#This process is for CH2O@Ce -> CH2O(g) + Ce.  There are 2 coadsorbate species: CH3O@V and H@O.  This corresponds to 1/3 O sites filled with CH3O on V and 1/3 O sites filled with H.
current_process_name ='pF113p1'
#Loops through Ce_1 and Ce_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central Ce4+ for CH3O@V
	for y in range(1,3+1):
#This loops through neighboring O sites for H plus
		for z in range(1,3+1):
			if y == z:
				pass
			else:
				temporary_name_string = '%s_a_%s_%s_%s' %(current_process_name,x,y,z)
				temporary_conditions_list = eval("[Condition(species='U28_CH2O_Ce4plus', coord=%s), \
								Condition(species='U22_CH3O_ionic_V', coord=%s), \
								Condition(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))
				temporary_actions_list = eval("[Action(species='U1_Ce_4plus', coord=%s), \
								Action(species='U22_CH3O_ionic_V', coord=%s), \
								Action(species='U4_H_plus', coord=%s)]" %(Ce_sites[x][1],O_sites_surrounding_Ce[x][y],O_sites_surrounding_Ce[x][z]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
				temporary_tst_interaction_energy = 0
				temporary_reactant_interaction_energy = 0
				temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
				temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
				temporary_tof_count_dict = {'F113p1':1, 'CH2O_output_flux':1}
				temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
				kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.
current_process_name ='pR113p1'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R113p1':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)

#113p7
#This process is for CH2O@V -> CH2O(g) + V.  There are no coadsorbate species
current_process_name ='pF113p7'
#Loops through O_1 and O_2
for x in range (1,2+1):
	temporary_name_string = '%s_a_%s' %(current_process_name,x)
	temporary_conditions_list = eval("[Condition(species='U29_CH2O_V', coord=%s)]" %(O_sites[x][1]))
	temporary_actions_list = eval("[Action(species='U3_Vacancy', coord=%s)]" %(O_sites[x][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
	temporary_tst_interaction_energy = 0
	temporary_reactant_interaction_energy = 0
	temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
	temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
	temporary_tof_count_dict = {'F113p7':1, 'CH2O_output_flux':1}
	temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
	kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.
current_process_name ='pR113p7'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R113p7':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)

#116p1
#This process is for 2H@O -> H2(g) + 2O.  There are no coadsorbate species, but there are 2 Ce3+ that become Ce4+
current_process_name ='pF116p1'
#Loops through O_1 and O_2
for x in range (1,2+1):
#This loops through all possible O neighbors of the central O for H_plus
	for y in range(1,6+1):
#This loops through neighboring Ce sites to O for Ce 3plus
		for i in range(1,3+1):
#This loops through neighboring Ce sites to O for Ce 3plus
			for j in range(1,3+1):
				if i == j or j < i:
					pass
				else:
					temporary_name_string = '%s_a_%s_%s_%s_%s' %(current_process_name,x,y,i,j)
					temporary_conditions_list = eval("[Condition(species='U4_H_plus', coord=%s), \
									Condition(species='U4_H_plus', coord=%s),\
									Condition(species='U2_Ce_3plus', coord=%s), \
									Condition(species='U2_Ce_3plus', coord=%s)]" %(O_sites[x][1],O_sites_surrounding_O[x][y],Ce_sites_surrounding_O[x][i],Ce_sites_surrounding_O[x][j]))

					temporary_actions_list = eval("[Action(species='U50_O', coord=%s), \
									Action(species='U50_O', coord=%s), \
									Action(species='U1_Ce_4plus', coord=%s), \
									Action(species='U1_Ce_4plus', coord=%s)]" %(O_sites[x][1],O_sites_surrounding_O[x][y],Ce_sites_surrounding_O[x][i],Ce_sites_surrounding_O[x][j]))
	#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
					temporary_tst_interaction_energy = 0
					temporary_reactant_interaction_energy = 0
					temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
	#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
					temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
					temporary_tof_count_dict = {'F116p1':1, 'H2_output_flux':1}
					temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
					kmc_model.add_process(**temporary_kwargs_dictionary)

#This process is for parallel data structure and will not happen.
current_process_name ='pR116p1'
temporary_name_string = '%s_a' %(current_process_name)		
temporary_conditions_list = eval("[Condition(coord=%s, species='unallowed')]" %(Ce_sites[1][1]))
temporary_actions_list = eval("[Action(coord=%s, species='U1_Ce_4plus')]" %(Ce_sites[1][1]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
temporary_tst_interaction_energy = 0
temporary_reactant_interaction_energy = 0
temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential.  
temporary_rate_constant_string = '(p_H2gas*bar*A/sqrt(2*Pi*1.38e-23*T*(mass_H2kgmol/N_A)))*(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
temporary_tof_count_dict = {'R116p1':1}
temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
kmc_model.add_process(**temporary_kwargs_dictionary)

#117p2
#This process is for CH2O@V + Ce + O -> V + CH2O@O + O.  There are 2 coadsorbate H.  This corresponds to 2/3 (DFT) -> 4/6 (KMC) H@O.
current_process_name ='pF117p2'
#Loops through O_1 and O_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central O for CH2O@Ce
	for y in range(1,3+1):
#This loops through neighboring O sites for H
		for z in range(1,6+1):
#This loops through neighboring O sites for H
			for i in range(1,6+1):
#This loops through neighboring O sites for H
				for j in range(1,6+1):
#This loops through neighboring O sites for H
					for k in range(1,6+1):
						if z == i or z == j or z == k or i == j or i == k or j == k or k < j or j < i or i < z:
							pass
						else:
							temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k)
							temporary_conditions_list = eval("[Condition(species='U29_CH2O_V', coord=%s), \
											Condition(species='U1_Ce_4plus', coord=%s), \
											Condition(species='U4_H_plus', coord=%s), \
											Condition(species='U4_H_plus', coord=%s), \
											Condition(species='U4_H_plus', coord=%s), \
											Condition(species='U4_H_plus', coord=%s)]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y],O_sites_surrounding_O[x][z],O_sites_surrounding_O[x][i],O_sites_surrounding_O[x][j],O_sites_surrounding_O[x][k]))

							temporary_actions_list = eval("[Action(species='U3_Vacancy', coord=%s), \
											Action(species='U28_CH2O_Ce4plus', coord=%s), \
											Action(species='U4_H_plus', coord=%s), \
											Action(species='U4_H_plus', coord=%s), \
											Action(species='U4_H_plus', coord=%s), \
											Action(species='U4_H_plus', coord=%s)]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y],O_sites_surrounding_O[x][z],O_sites_surrounding_O[x][i],O_sites_surrounding_O[x][j],O_sites_surrounding_O[x][k]))
			#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
							temporary_tst_interaction_energy = 0
							temporary_reactant_interaction_energy = 0
							temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
			#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
							temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
							temporary_tof_count_dict = {'F117p2':1}
							temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
							kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction
current_process_name ='pR117p2'
#Loops through O_1 and O_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central O for CH2O@Ce
	for y in range(1,3+1):
#This loops through neighboring O sites for H
		for z in range(1,6+1):
#This loops through neighboring O sites for H
			for i in range(1,6+1):
#This loops through neighboring O sites for H
				for j in range(1,6+1):
#This loops through neighboring O sites for H
					for k in range(1,6+1):
						if z == i or z == j or z == k or i == j or i == k or j == k or k < j or j < i or i < z:
							pass
						else:
							temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k)

							temporary_conditions_list = eval("[Condition(species='U3_Vacancy', coord=%s), \
											Condition(species='U28_CH2O_Ce4plus', coord=%s), \
											Condition(species='U4_H_plus', coord=%s), \
											Condition(species='U4_H_plus', coord=%s), \
											Condition(species='U4_H_plus', coord=%s), \
											Condition(species='U4_H_plus', coord=%s)]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y],O_sites_surrounding_O[x][z],O_sites_surrounding_O[x][i],O_sites_surrounding_O[x][j],O_sites_surrounding_O[x][k]))


							temporary_actions_list = eval("[Action(species='U29_CH2O_V', coord=%s), \
											Action(species='U1_Ce_4plus', coord=%s), \
											Action(species='U4_H_plus', coord=%s), \
											Action(species='U4_H_plus', coord=%s), \
											Action(species='U4_H_plus', coord=%s), \
											Action(species='U4_H_plus', coord=%s)]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y],O_sites_surrounding_O[x][z],O_sites_surrounding_O[x][i],O_sites_surrounding_O[x][j],O_sites_surrounding_O[x][k]))

			#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
							temporary_tst_interaction_energy = 0
							temporary_reactant_interaction_energy = 0
							temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
			#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
							temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
							temporary_tof_count_dict = {'R117p2':1}
							temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
							kmc_model.add_process(**temporary_kwargs_dictionary)

#117p3
#This process is for CH2O@V + Ce + O -> V + CH2O@O + O.  There are no coadsorbates.
current_process_name ='pF117p3'
#Loops through O_1 and O_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central O for CH2O@Ce
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k)
		temporary_conditions_list = eval("[Condition(species='U29_CH2O_V', coord=%s), \
						Condition(species='U1_Ce_4plus', coord=%s)]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y]))

		temporary_actions_list = eval("[Action(species='U3_Vacancy', coord=%s), \
						Action(species='U28_CH2O_Ce4plus', coord=%s)]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y]))
#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
		temporary_tof_count_dict = {'F117p3':1}
		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		kmc_model.add_process(**temporary_kwargs_dictionary)

#The reverse reaction.
current_process_name ='pR117p3'
#Loops through O_1 and O_2
for x in range (1,2+1):
#This loops through all possible Ce neighbors of the central O for CH2O@Ce
	for y in range(1,3+1):
		temporary_name_string = '%s_a_%s_%s_%s_%s_%s_%s' %(current_process_name,x,y,z,i,j,k)

		temporary_conditions_list = eval("[Condition(species='U3_Vacancy', coord=%s), \
						Condition(species='U28_CH2O_Ce4plus', coord=%s)]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y]))

		temporary_actions_list = eval("[Action(species='U29_CH2O_V', coord=%s), \
						Action(species='U1_Ce_4plus', coord=%s)]" %(O_sites[x][1],Ce_sites_surrounding_O[x][y]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)
		temporary_tof_count_dict = {'R117p3':1}
		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		kmc_model.add_process(**temporary_kwargs_dictionary)


#This changes an empty O site ('U50_O') into a fake species called "ExcitedOxygen". The reverse reaction goes the other way.		
#This is to prevent the system from ever having "no reactions" on a 1 second time scale. So the excitation happens about 1 time per second
#and then the de-excitation is very rapid.
current_process_name ='pF120p0'
#x loops across O1 and O2
for x in range(1,2+1):
		temporary_name_string = 'pF120p0_a_%s' %(x)
		
		temporary_conditions_list = eval("[Condition(coord=%s, species='U50_O')]" %(O_sites[x][1]))
		
		temporary_actions_list = eval("[Action(coord=%s, species='ExcitedOxygen')]" %(O_sites[x][1]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'F120p0':1,'Fake_OxygenExcitation_flux':1}

		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)

		
#This is the reverse process of F120p0.
current_process_name ='pR120p0'
#Loops through O_1 and O_2
for x in range(1,2+1):
		temporary_name_string = 'pR120p0_a_%s' %(x)
		
		temporary_conditions_list = eval("[Condition(coord=%s, species='ExcitedOxygen')]" %(O_sites[x][1]))
		
		temporary_actions_list = eval("[Action(coord=%s, species='U50_O')]" %(O_sites[x][1]))

#total_reactants_energy and total_tst_energy are located using the index of current process name and located from the unzip parameters lists
		temporary_tst_interaction_energy = 0
		temporary_reactant_interaction_energy = 0
		temporary_total_interaction_energy = temporary_tst_interaction_energy - temporary_reactant_interaction_energy
#the rate constant string will only contain the difference between total_reactants_energy and total_tst_energy and the pre-exponential
		temporary_rate_constant_string = '(%s*exp(-((%s)+(%s))/(R*T)))' %(process_parameters_array[process_names.index(current_process_name)][1], process_parameters_array[process_names.index(current_process_name)][2], temporary_total_interaction_energy)

		temporary_tof_count_dict = {'R120p0':1,'Fake_OxygenExcitationRelaxation_flux':1}

		temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}
		
		kmc_model.add_process(**temporary_kwargs_dictionary)

		

# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
print("For this example, we are not using the compile step because it takes more than 30 minutes. To do the compile step, the user should uncomment the kmcos.compile(kmc_model) line or should type in 'kmcos export MyThirdTPR.xml' in the terminal")
# For this example, we are not using the compile step because it takes more than 30 minutes. To do the compile step, the user should uncomment the below kmcos.compile(kmc_model) line or should type in 'kmcos export MyThirdTPR.xml' in the terminal
#kmcos.compile(kmc_model)