#!/usr/bin/env python

import kmcos
from kmcos.types import *
from kmcos.io import *
from itertools import product
import numpy as np

model_name = str(__file__[+0:-3]).replace("__build", "") # This line automatically names the model based on the python file’s name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the ‘__build’ part of the string. If you want to override this automatic naming, just set the variable ‘model_name’ equal to the string that you would like to use.
kmc_model = kmcos.create_kmc_model(model_name)
kmc_model.set_meta(author='Christa Cody',
            email='codycn@ornl.gov',
            model_name=model_name,
            model_dimension=2)

			
kmc_model.add_species(name='empty', color='#ffffff')
kmc_model.add_species(name='CO', color='#000000',
               representation="Atoms('CO',[[0,0,0],[0,0,1.2]])",
               tags='carbon')
			   
layer = kmc_model.add_layer(name='simple_cubic')
#initially populated
layer.sites.append(Site(name='coord1', pos='.5 .5 .5',
                        default_species='empty'))
					
kmc_model.lattice.cell = np.diag([3.5, 3.5, 10])
kmc_model.add_parameter(name='T', value=600, adjustable=True, min=150, max=500)
kmc_model.add_parameter(name='p_COgas', value=.2, adjustable=True, scale='log', min=1e-13, max=1e3)
kmc_model.add_parameter(name='A', value='(3.5*angstrom)**2')
kmc_model.add_parameter(name='deltaG', value='-0.5', adjustable=True,
                           min=-1.3, max=0.3)
E_act_des_var = 500000
kmc_model.add_parameter(name='A_CO_des', value = 1e13)
kmc_model.add_parameter(name='E_act_des', value = E_act_des_var)
kmc_model.add_parameter(name='R', value = 8.3145)
coord1 = kmc_model.lattice.generate_coord('coord1.(0,0,0).simple_cubic')

# Processes

kmc_model.add_process(name='Do_nothing', #this process does nothing because the rate constant is set to zero. This was done because kmos requires atleast 2 processes to be available. 
               conditions=[Condition(coord=coord1, species='CO')],
               actions=[Action(coord=coord1, species='empty')],
               rate_constant='0',
	       tof_count = {'Do_nothing':1})

kmc_model.add_process(name='CO_desorption',
               conditions=[Condition(coord=coord1, species='CO')],
               actions=[Action(coord=coord1, species='empty')],
               rate_constant='A_CO_des*exp(-E_act_des/(R*T))',
	       tof_count = {'CO_Desorption':1})


# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)
