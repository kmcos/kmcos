#!/usr/bin/env python

import kmcos
from kmcos.types import Condition, Action
import numpy as np

model_name = str(__file__[+0:-3]).replace("__build", "") # This line automatically names the model based on the python file’s name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the ‘__build’ part of the string. If you want to override this automatic naming, just set the variable ‘model_name’ equal to the string that you would like to use.
kmc_model = kmcos.create_kmc_model(model_name)



kmc_model.set_meta(author='StangenMensch',
            email='linie@tum.de',
            model_dimension=1,
            model_name='hopping_model')
kmc_model.add_species(name='empty',
               color='#ffffff',
               )
kmc_model.add_species(name='C',
               representation="Atoms('C',[[0,0,0]])",
               color='#000000')

kmc_model.layer_list.cell = np.diag([1., 1., 1.])
kmc_model.add_layer(name='default',
                     color='#ffffff')
kmc_model.add_site(layer='default',
            pos='0 0 0',
            name='a')

coord = kmc_model.layer_list.generate_coord

kmc_model.add_process(name='ads',
               rate_constant='10**6',
               conditions=[Condition(species='empty', coord=coord('a'))],
               actions=[Action(species='C', coord=coord('a'))],
               tof_count={'adsorption': 1})

kmc_model.add_process(name='des',
               rate_constant='10**6',
               conditions=[Condition(species='C', coord=coord('a'))],
               actions=[Action(species='empty', coord=coord('a'))],
               tof_count={'desorption': 1})

kmc_model.add_process(name='left',
               rate_constant='10**8',
               conditions=[Condition(species='C', coord=coord('a')),
                           Condition(species='empty', coord=coord('a.(-1, 0, 0)'))],
               actions=[Action(species='empty', coord=coord('a')),
                           Condition(species='C', coord=coord('a.(-1, 0, 0)'))],
               tof_count={'left': 1})

kmc_model.add_process(name='right',
               rate_constant='10**8',
               conditions=[Condition(species='C', coord=coord('a')),
                           Condition(species='empty', coord=coord('a.(1, 0, 0)'))],
               actions=[Action(species='empty', coord=coord('a')),
                           Condition(species='C', coord=coord('a.(1, 0, 0)'))],
               tof_count={'right': 1})

# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)