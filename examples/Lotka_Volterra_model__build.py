#!/usr/bin/env python


import numpy as np
from kmcos.types import Site, Condition, Action
import kmcos

model_name = __file__[+0:-3] # This is the python file name, the brackets cut off zero characters from the beginning and three character from the end (".py").  To manually name the model just place a string here.
model_name = model_name.replace("__build", "")
kmc_model = kmcos.create_kmc_model(model_name)

kmc_model.set_meta(author="LotkaVolterra",
            email='mjhoffmann@gmail.com',
            model_name='lotka_volterra_model',
            model_dimension=2)

kmc_model.add_species(name='empty')
kmc_model.add_species(name='A', representation="Atoms('O')")
kmc_model.add_species(name='B', representation="Atoms('C')")

layer = kmc_model.add_layer(name='sc')

kmc_model.lattice.cell = np.diag([3.5, 3.5, 10])

layer.sites.append(Site(name='site', pos='.5 .5 .5'))


kmc_model.add_parameter(name='k1', value='1000000.', adjustable=True, min=0., max=100.)
kmc_model.add_parameter(name='k2', value=3.65, adjustable=True, min=0., max=100.)
kmc_model.add_parameter(name='k3', value=1.1, adjustable=True, min=0., max=100.)
kmc_model.add_parameter(name='zeta', value='0.06', adjustable=True, min=0., max=1.)



kmc_model.parse_and_add_process('AA_creation1; A@site + empty@site.(1, 0, 0) -> A@site + A@site.(1,0,0); k1')
kmc_model.parse_and_add_process('AA_creation2; A@site + empty@site.(-1, 0, 0) -> A@site + A@site.(-1,0,0); k1')
kmc_model.parse_and_add_process('AA_creation3; A@site + empty@site.(0, 1, 0) -> A@site + A@site.(0,1,0); k1')
kmc_model.parse_and_add_process('AA_creation4; A@site + empty@site.(0, -1, 0) -> A@site + A@site.(0,-1,0); k1')

kmc_model.parse_and_add_process('AB_reaction1; A@site + B@site.(1, 0, 0) -> B@site + B@site.(1,0,0); k2')
kmc_model.parse_and_add_process('AB_reaction2; A@site + B@site.(-1, 0, 0) -> B@site + B@site.(-1,0,0); k2')
kmc_model.parse_and_add_process('AB_reaction3; A@site + B@site.(0, 1, 0) -> B@site + B@site.(0,1,0); k2')
kmc_model.parse_and_add_process('AB_reaction4; A@site + B@site.(0, -1, 0) -> B@site + B@site.(0,-1,0); k2')

# add really slow reverse processes just to keep the model from crashing
kmc_model.parse_and_add_process('B_desorption; B@site -> empty@site; k3')

# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)
