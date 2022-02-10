#!/usr/bin/env python

import kmcos
from kmcos.types import *
from kmcos.io import *
import numpy as np


model_name = __file__[+0:-3] # This is the python file name, the brackets cut off zero characters from the beginning and three character from the end (".py").  To manually name the model just place a string here.
model_name = model_name.replace("__build", "")
kmc_model = kmcos.create_kmc_model(model_name)
# Meta information
kmc_model.set_meta(author='Max J. Hoffmann',
            email='mjhoffmann@gmail.com',
            model_name='sand_model',
            model_dimension=2)

# Species
kmc_model.add_species(name='empty',)
kmc_model.add_species(name='source',
               representation="Atoms('Au')")
kmc_model.add_species(name='drain',
               representation="Atoms('Ag')")
kmc_model.add_species(name='blocked',
               representation="Atoms('C')")
kmc_model.add_species(name='grain',
               representation="Atoms('Si')")
kmc_model.species_list.default_species = 'empty'

# Layers
layer = Layer(name='default')
layer.sites.append(Site(name='a', pos='0.5 0.5 0.5',
                        default_species='empty'))
kmc_model.add_layer(layer)
kmc_model.lattice.cell = np.diag([3, 3, 3])

# Parameters
kmc_model.add_parameter(name='k_up', value=1e4, adjustable=True, min=1, max=1.e6, scale='log')
kmc_model.add_parameter(name='k_down', value=1e3, adjustable=True, min=1, max=1.e6, scale='log')
kmc_model.add_parameter(name='k_left', value=1e3, adjustable=True, min=1, max=1.e6, scale='log')
kmc_model.add_parameter(name='k_right', value=1e3, adjustable=True, min=1, max=1.e6, scale='log')
kmc_model.add_parameter(name='k_entry', value=1e3, adjustable=True, min=1, max=1.e6, scale='log')
kmc_model.add_parameter(name='k_exit', value=1e3, adjustable=True, min=1, max=1.e6, scale='log')

# Coords
center = kmc_model.lattice.generate_coord('a.(0,0,0).default')

up = kmc_model.lattice.generate_coord('a.(0,1,0).default')
down = kmc_model.lattice.generate_coord('a.(0,-1,0).default')

left = kmc_model.lattice.generate_coord('a.(-1,0,0).default')
right = kmc_model.lattice.generate_coord('a.(1,0,0).default')

down_left = kmc_model.lattice.generate_coord('a.(-1,-1,0).default')
down_right = kmc_model.lattice.generate_coord('a.(1,-1,0).default')

up_left = kmc_model.lattice.generate_coord('a.(-1,1,0).default')
up_right = kmc_model.lattice.generate_coord('a.(1,1,0).default')

# Processes

kmc_model.add_process(name='diffusion_down',
               conditions=[Condition(species='grain', coord=center),
                           Condition(species='empty', coord=down)],
               actions=[Action(species='grain', coord=down),
                        Action(species='empty', coord=center)],
               rate_constant='k_down')

kmc_model.add_process(name='diffusion_left',
               conditions=[Condition(species='grain', coord=center),
                           Condition(species='grain', coord=down_left),
                           Condition(species='empty', coord=left)],
               actions=[Action(species='grain', coord=left),
                        Action(species='grain', coord=down_left),
                        Action(species='empty', coord=center)],
               rate_constant='k_left')
kmc_model.add_process(name='diffusion_right',
               conditions=[Condition(species='grain', coord=center),
                           Condition(species='grain', coord=down_right),
                           Condition(species='empty', coord=right)],
               actions=[Action(species='grain', coord=right),
                        Action(species='grain', coord=down_right),
                        Action(species='empty', coord=center)],
               rate_constant='k_right')

kmc_model.add_process(name='diffusion_up_left',
               conditions=[Condition(species='grain', coord=center),
                           Condition(species='grain', coord=left),
                           Condition(species='empty', coord=up_left)],
               actions=[Action(species='grain', coord=left),
                        Action(species='grain', coord=up_left),
                        Action(species='empty', coord=center)],
               rate_constant='k_left')


kmc_model.add_process(name='diffusion_up_right',
               conditions=[Condition(species='grain', coord=center),
                           Condition(species='grain', coord=right),
                           Condition(species='empty', coord=up_right)],
               actions=[Action(species='grain', coord=right),
                        Action(species='grain', coord=up_right),
                        Action(species='empty', coord=center)],
               rate_constant='k_right')


kmc_model.add_process(name='diffusion_down_left',
               conditions=[Condition(species='grain', coord=center),
                           Condition(species='empty', coord=down_left),],
               actions=[Action(species='grain', coord=down_left),
                        Action(species='empty', coord=center)],
               rate_constant='k_left')

kmc_model.add_process(name='diffusion_down_right',
               conditions=[Condition(species='grain', coord=center),
                           Condition(species='empty', coord=down_right),],
               actions=[Action(species='grain', coord=down_right),
                        Action(species='empty', coord=center)],
               rate_constant='k_right')

kmc_model.add_process(name='entry',
               conditions=[Condition(species='empty', coord=center),
                           Condition(species='source', coord=up)],
               actions=[Action(species='grain', coord=center),
                        Action(species='source', coord=up)],
               rate_constant='k_entry')

kmc_model.add_process(name='exit',
               conditions=[Condition(species='grain', coord=center),
                           Condition(species='drain', coord=down)],
               actions=[Action(species='empty', coord=center),
                        Action(species='drain', coord=down)],
               rate_constant='k_exit')


# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model(model_name=kmc_model.model_name, backend=kmc_model.backend) #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)