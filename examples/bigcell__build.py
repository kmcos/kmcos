#!/usr/bin/env python
"""Simple model generation script that demonstrate how
   big unit cell could be run periodically and
   non-periodically
"""
import kmcos
from kmcos.types import *

model_name = str(__file__[+0:-3]).replace("__build", "") # This line automatically names the model based on the python file’s name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the ‘__build’ part of the string. If you want to override this automatic naming, just set the variable ‘model_name’ equal to the string that you would like to use.
kmc_model = kmcos.create_kmc_model(model_name)
kmc_model.set_meta(author='Max J. Hoffmann',
            email='mjhoffmann@gmail.com',
            model_dimension=2,
            model_name='big_cell_test')
# add layer
lattice = kmc_model.add_layer(name='default')
# add sites
lattice.add_site(Site(name='bottom',pos=np.array([0.5, 0, 0])))
lattice.add_site(Site(name='left',pos=np.array([0, 0.5, 0])))
lattice.add_site(Site(name='right',pos=np.array([1., 0.5, 0])))
lattice.add_site(Site(name='top',pos=np.array([.5, 1., 0])))

# add parameters
kmc_model.add_parameter(name='k', value=1000.)

# add species
kmc_model.add_species(name='empty')
kmc_model.add_species(name='Li', representation="Atoms('Li')")

# add processes
kmc_model.parse_and_add_process('right_east; Li@right -> Li@left.(1,0,0); k')
kmc_model.parse_and_add_process('left_east; Li@left->Li@right; k')
kmc_model.parse_and_add_process('right_west; Li@right->Li@left; k')
kmc_model.parse_and_add_process('left_west; Li@left->Li@right.(-1,0,0); k')
kmc_model.parse_and_add_process('left_farwest; Li@left->Li@left.(-1,0,0); k')

# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)