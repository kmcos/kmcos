#!/usr/bin/env python

from kmcos.types import *
from kmcos.io import *
from itertools import product
import numpy as np

model_name = __file__[+0:-3] # This is the python file name, the brackets cut off zero characters from the beginning and three character from the end (".py").  To manually name the model just place a string here.
pt = Project()
pt.set_meta(author='Christa Cody',
            email='codycn@ornl.gov',
            model_name=model_name,
            model_dimension=2)

			
pt.add_species(name='empty', color='#ffffff')
pt.add_species(name='CO', color='#000000',
               representation="Atoms('CO',[[0,0,0],[0,0,1.2]])",
               tags='carbon')
			   
layer = pt.add_layer(name='simple_cubic')
#initially populated
layer.sites.append(Site(name='coord1', pos='.5 .5 .5',
                        default_species='empty'))
					
pt.lattice.cell = np.diag([3.5, 3.5, 10])
pt.add_parameter(name='T', value=600, adjustable=True, min=150, max=500)
pt.add_parameter(name='p_COgas', value=.2, adjustable=True, scale='log', min=1e-13, max=1e3)
pt.add_parameter(name='A', value='(3.5*angstrom)**2')
pt.add_parameter(name='deltaG', value='-0.5', adjustable=True,
                           min=-1.3, max=0.3)
E_act_des_var = 84000
pt.add_parameter(name='A_CO_des', value = 1.45e13)
pt.add_parameter(name='E_act_des', value = E_act_des_var)
pt.add_parameter(name='R', value = 8.314)
coord1 = pt.lattice.generate_coord('coord1.(0,0,0).simple_cubic')

# Processes

pt.add_process(name='Do_nothing', #this process does nothing because the rate constant is set to zero. This was done because kmos requires atleast 2 processes to be available. 
               conditions=[Condition(coord=coord1, species='CO')],
               actions=[Action(coord=coord1, species='empty')],
               rate_constant='0',
	       tof_count = {'Do_nothing':1})

pt.add_process(name='CO_desorption',
               conditions=[Condition(coord=coord1, species='CO')],
               actions=[Action(coord=coord1, species='empty')],
               rate_constant='A_CO_des*exp(-E_act_des/(R*T))',
	       tof_count = {'CO_Desorption':1})



pt.filename = model_name + ".xml"
pt.save()
