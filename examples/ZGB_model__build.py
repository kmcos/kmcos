#!/usr/bin/env python


import numpy as np
import kmcos
from kmcos.types import Project, Site, Condition, Action

model_name = str(__file__[+0:-3]).replace("__build", "") # This line automatically names the model based on the python file’s name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the ‘__build’ part of the string. If you want to override this automatic naming, just set the variable ‘model_name’ equal to the string that you would like to use.
kmc_model = kmcos.create_kmc_model(model_name)

kmc_model.set_meta(author="Ziff,Gulari,Barshad",
            email='mjhoffmann@gmail.com',
            model_name='zgb_model',
            model_dimension=2)

kmc_model.add_species(name='empty', color='#ffffff')
kmc_model.add_species(name='CO', representation="Atoms('C')", color='#000000')
kmc_model.add_species(name='O', representation="Atoms('O')", color='#ff0000')

layer = kmc_model.add_layer(name='sc')

kmc_model.lattice.cell = np.diag([3.5, 3.5, 10])

layer.sites.append(Site(name='site', pos='.5 .5 .5'))

kmc_model.add_parameter(name='yCO', value='0.45', adjustable=True, min=0., max=1.)

kmc_model.parse_and_add_process('CO_adsorption; empty@site -> CO@site; yCO')

kmc_model.parse_and_add_process('O2_adsorption1; empty@site + empty@site.(1, 0, 0) -> O@site + O@site.(1,0,0); (1 - yCO)/2.')
kmc_model.parse_and_add_process('O2_adsorption2; empty@site + empty@site.(0, 1, 0) -> O@site + O@site.(0,1,0); (1 - yCO)/2.')

kmc_model.parse_and_add_process('CO_oxidation1; CO@site + O@site.(1, 0, 0) -> empty@site + empty@site.(1,0,0); 10**10')
kmc_model.parse_and_add_process('CO_oxidation3; CO@site + O@site.(-1, 0, 0) -> empty@site + empty@site.(-1,0,0); 10**10')
kmc_model.parse_and_add_process('CO_oxidation2; CO@site + O@site.(0, 1, 0) -> empty@site + empty@site.(0,1,0); 10**10')
kmc_model.parse_and_add_process('CO_oxidation4; CO@site + O@site.(0, -1, 0) -> empty@site + empty@site.(0,-1,0); 10**10')


# add really slow reverse processes just to keep the model from crashing
kmc_model.parse_and_add_process('CO_desorption; CO@site -> empty@site; 1e-13')
kmc_model.parse_and_add_process('O2_desorption1; O@site + O@site.(1, 0, 0) -> empty@site + empty@site.(1,0,0); 1e-13')
kmc_model.parse_and_add_process('O2_desorption2; O@site + O@site.(0, 1, 0) -> empty@site + empty@site.(0,1,0); 1e-13')

# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)