#!/usr/bin/env python
#This file assumes an arrhenius expression from transition state theory for each processes rate constant. This files generates reaction processes automatically.
from kmcos.types import *
from kmcos.io import *
from itertools import product
import numpy as np
#from math import exp
#from math import sqrt

model_name = str(__file__[+0:-3]) # This is the python file name, the brackets cut off zero characters from the beginning and three character from the end (".py").  To manually name the model just place a string here.
kmc_model = kmcos.create_kmc_model(model_name)
kmc_model.set_meta(author='Thomas Danielson',
            email='thomasd1@vt.edu',
            model_name=model_name,
            model_dimension=2)
#Add pecies
kmc_model.add_species(name='A1', color='white')
kmc_model.add_species(name='B1', color='green')
kmc_model.add_species(name='C1', color='red')
kmc_model.add_species(name='D1', color='black')
kmc_model.add_species(name='E1', color='purple')
kmc_model.add_species(name='B2', color='blue')
kmc_model.add_species(name='C2', color='orange')
kmc_model.add_species(name='D2', color='grey')

#One layer and one site at the center
layer1 = kmc_model.add_layer(name='Site')
layer1.sites.append(Site(name='coord', pos='0.5 0.5 1',
                         default_species='A1'))

#Square cell with a single site at the center
kmc_model.lattice.cell = np.diag([3.825, 3.825, 2.343])

#Add parameters
kmc_model.add_parameter(name='T', value=600, adjustable=False)

#We will give the rate constant as a parameter and this way we can modify it on the fly if we desire.
rate_constants_dict = {
				'BRC_F1p0': 1	, #A1 -> B1
				'BRC_R1p0': 1	, #B1 -> A1
				'BRC_F2p0': 1	, #B1 -> C1
				'BRC_R2p0': 1	, #C1 -> B1
				'BRC_F3p0': 1	, #C1 -> D1
				'BRC_R3p0': 1	, #D1 -> C1
				'BRC_F4p0': 1	, #D1 -> E1
				'BRC_R4p0': 1	, #E1 -> D1
				'BRC_F5p0': 1e+2 , #B1 -> B2
				'BRC_R5p0': 1e+3 , #B2 -> B1
				'BRC_F6p0': 1e+4 , #C1 -> C2
				'BRC_R6p0': 1e+5 , #C2 -> C1
				'BRC_F7p0': 1e+6 , #D1 -> D2
				'BRC_R7p0': 1e+7   #D2 -> D1
			}

pre_exponentials_dict = {
				'AF1p0': 1 , #A1 -> B1
				'AR1p0': 1 , #B1 -> A1
				'AF2p0': 1 , #B1 -> C1
				'AR2p0': 1 , #C1 -> B1
				'AF3p0': 1 , #C1 -> D1
				'AR3p0': 1 , #D1 -> C1
				'AF4p0': 1 , #D1 -> E1
				'AR4p0': 1 , #E1 -> D1
				'AF5p0': 1 , #B1 -> B2
				'AR5p0': 1 , #B2 -> B1
				'AF6p0': 1 , #C1 -> C2
				'AR6p0': 1 , #C2 -> C1
				'AF7p0': 1 , #D1 -> D2
				'AR7p0': 1   #D2 -> D1
			}

#This generates and executes the string to add the rate_constants in the 
#rate_constants_dict as parameters
for i in range(len(rate_constants_dict)):
	rate_constants_string = str('kmc_model.add_parameter(name=')  \
				+ '\'' + str(list(rate_constants_dict.keys())[i]) + '\'' \
				+ str(', value=') \
			        + str(list(rate_constants_dict.values())[i])  \
				+ str(', adjustable=False)')
	exec("%s" %(rate_constants_string))

#This generates and executes the string to add the pre_exponentials in the 
#pre_exponentials_dict as parameters
for i in range(len(pre_exponentials_dict)):
	pre_exponentials_string = str('kmc_model.add_parameter(name=')  \
				+ '\'' + str(list(pre_exponentials_dict.keys())[i]) + '\'' \
				+ str(', value=') \
			        + str(list(pre_exponentials_dict.values())[i])  \
				+ str(', adjustable=False)')
	exec("%s" %(pre_exponentials_string))

#We need to generate a single coordinate	
coord = kmc_model.lattice.generate_coord('coord.(0,0,0).Site')



#Processes
#A1 -> B1
current_process_name ='pF1p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='A1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='B1')]")

temporary_rate_constant_string = 'AF1p0*BRC_F1p0'

temporary_tof_count_dict = {'F1p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#B1 -> A1
current_process_name ='pR1p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='B1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='A1')]")

temporary_rate_constant_string = 'AR1p0*BRC_R1p0'

temporary_tof_count_dict = {'R1p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#B1 -> C1
current_process_name ='pF2p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='B1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='C1')]")

temporary_rate_constant_string = 'AF2p0*BRC_F2p0'

temporary_tof_count_dict = {'F2p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#C1 -> B1
current_process_name ='pR2p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='C1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='B1')]")

temporary_rate_constant_string = 'AR2p0*BRC_R2p0'

temporary_tof_count_dict = {'R2p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#C1 -> D1
current_process_name ='pF3p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='C1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='D1')]")

temporary_rate_constant_string = 'AF3p0*BRC_F3p0'

temporary_tof_count_dict = {'F3p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#D1 -> C1
current_process_name ='pR3p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='D1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='C1')]")

temporary_rate_constant_string = 'AR3p0*BRC_R3p0'

temporary_tof_count_dict = {'R3p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#D1 -> E1
current_process_name ='pF4p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='D1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='E1')]")

temporary_rate_constant_string = 'AF4p0*BRC_F4p0'

temporary_tof_count_dict = {'F4p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#E1 -> D1
current_process_name ='pR4p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='E1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='D1')]")

temporary_rate_constant_string = 'AR4p0*BRC_R4p0'

temporary_tof_count_dict = {'R4p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#B1 -> B2
current_process_name ='pF5p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='B1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='B2')]")

temporary_rate_constant_string = 'AF5p0*BRC_F5p0'

temporary_tof_count_dict = {'F5p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#B2 -> B1
current_process_name ='pR5p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='B2')]") 

temporary_actions_list = eval("[Action(coord=coord, species='B1')]")

temporary_rate_constant_string = 'AR5p0*BRC_R5p0'

temporary_tof_count_dict = {'R5p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#C1 -> C2
current_process_name ='pF6p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='C1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='C2')]")

temporary_rate_constant_string = 'AF6p0*BRC_F6p0'

temporary_tof_count_dict = {'F6p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#C2 -> C1
current_process_name ='pR6p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='C2')]") 

temporary_actions_list = eval("[Action(coord=coord, species='C1')]")

temporary_rate_constant_string = 'AR6p0*BRC_R6p0'

temporary_tof_count_dict = {'R6p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#D1 -> D2
current_process_name ='pF7p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='D1')]") 

temporary_actions_list = eval("[Action(coord=coord, species='D2')]")

temporary_rate_constant_string = 'AF7p0*BRC_F7p0'

temporary_tof_count_dict = {'F7p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)

#D2 -> D1
current_process_name ='pR7p0'
temporary_name_string = '%s' %(current_process_name)		

temporary_conditions_list = eval("[Condition(coord=coord, species='D2')]") 

temporary_actions_list = eval("[Action(coord=coord, species='D1')]")

temporary_rate_constant_string = 'AR7p0*BRC_R7p0'

temporary_tof_count_dict = {'R7p0':1}

temporary_kwargs_dictionary = {"name": temporary_name_string, "conditions" : temporary_conditions_list, "actions" : temporary_actions_list, "rate_constant" : temporary_rate_constant_string, "tof_count" : temporary_tof_count_dict}

kmc_model.add_process(**temporary_kwargs_dictionary)


kmc_model.filename = model_name + ".xml"
kmc_model.save_model()
