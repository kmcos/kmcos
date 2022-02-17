#!/usr/bin/env python
import kmcos
from kmcos.types import *
from itertools import product
import numpy as np
import kmcos.cli #not needed.

model_name = __file__[+0:-3] # This is the python file name, the brackets cut off zero characters from the beginning and three character from the end (".py").  To manually name the model just place a string here.
model_name = model_name.replace("__build", "")

kmc_model = kmcos.create_kmc_model(model_name)
kmc_model.set_meta(author='Zachary Coin',
            email='coinzc@ornl.gov',
            model_name=model_name,
            model_dimension=2)

			
kmc_model.add_species(name='empty', color='#ffffff')
kmc_model.add_species(name='CO', color='#000000',
               representation="Atoms('CO',[[0,0,0],[0,0,1.2]])",
               tags='carbon')
			   
layer = kmc_model.add_layer(name='simple_cubic')
layer.sites.append(Site(name='hollow1', pos='0.25 0.5 0.5',
                        default_species='empty'))
layer.sites.append(Site(name='hollow2', pos='0.5 0.5 0.5',
                        default_species='empty'))	
layer.sites.append(Site(name='hollow3', pos='0.75 0.5 0.5',
                        default_species='empty'))					
kmc_model.lattice.cell = np.diag([3.5, 3.5, 10])
kmc_model.add_parameter(name='T', value=600, adjustable=True, min=300, max=1500)
kmc_model.add_parameter(name='p_COgas', value=.2, adjustable=True, scale='log', min=1e-13, max=1e3)
kmc_model.add_parameter(name='A', value='(3.5*angstrom)**2')
kmc_model.add_parameter(name='deltaG', value='-0.5', adjustable=True,
                           min=-1.3, max=0.3)
coordhollow1 = kmc_model.lattice.generate_coord('hollow1.(0,0,0).simple_cubic')
coordhollow2 = kmc_model.lattice.generate_coord('hollow2.(0,0,0).simple_cubic')
coordhollow3 = kmc_model.lattice.generate_coord('hollow3.(0,0,0).simple_cubic')



# Processes
kmc_model.add_process(name='CO_adsorption',
               conditions=[Condition(species='empty', coord=coordhollow1)],
               actions=[Action(species='CO', coord=coordhollow1)],
               rate_constant='0.1*p_COgas*A*bar/sqrt(2*pi*m_CO*umass/beta)')

kmc_model.add_process(name='CO_diffusion_hollow1_right', 
				conditions=[Condition(species='CO' ,coord=coordhollow1), 
					Condition(species='empty' ,coord=coordhollow2)], 
				actions=[Action(species='empty' ,coord=coordhollow1), 
					Action(species='CO' ,coord=coordhollow2)], 			
					rate_constant='3*p_COgas*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(beta*deltaG*eV)')
kmc_model.add_process(name='CO_diffusion_hollow2_right', 
				conditions=[Condition(species='CO' ,coord=coordhollow2), 
					Condition(species='empty' ,coord=coordhollow3)], 
				actions=[Action(species='empty' ,coord=coordhollow2), 
					Action(species='CO' ,coord=coordhollow3)], 			
					rate_constant='3*p_COgas*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(beta*deltaG*eV)')

kmc_model.add_process(name='CO_desorption3',
               conditions=[Condition(coord=coordhollow3, species='CO')],
               actions=[Action(coord=coordhollow3, species='empty')],
               rate_constant='p_COgas*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(beta*deltaG*eV)')


# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)