#!/usr/bin/env python

from ase.lattice.surface import fcc111
import ase
import kmcos
import kmcos
from kmcos.utils import get_ase_constructor
from kmcos.types import *
import numpy as np


slab = fcc111('Pt', [1,1,4], vacuum=10)

positions = slab.get_scaled_positions()
model_name = str(__file__[+0:-3]).replace("__build", "") # This line automatically names the model based on the python file’s name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the ‘__build’ part of the string. If you want to override this automatic naming, just set the variable ‘model_name’ equal to the string that you would like to use.
kmc_model = kmcos.create_kmc_model(model_name)
kmc_model.set_meta(model_name='pt111',
            model_dimension='2',
            author='Max J. Hoffmann',
            email='mjhoffmann@gmail.com',
            debug=0)

layer = Layer(name='pt111')
pos1 = np.array([positions[1, 0],
        positions[1, 1], 0.672])

layer.add_site(Site(name='hollow1',
                    pos=pos1))

pos2 = np.array([positions[2, 0],
                positions[2, 1], 0.672])

#slab += ase.atoms.Atoms('H', cell=slab.cell, scaled_positions=[pos1])
#slab += ase.atoms.Atoms('H', cell=slab.cell, scaled_positions=[pos2])
#ase.visualize.view(slab, repeat=(1,1,1))
rpos = np.linalg.solve(slab.cell, np.array(pos2))
layer.add_site(Site(name='hollow2',
                    pos=pos2))

kmc_model.add_layer(layer)
kmc_model.lattice.representation = '[%s]' % get_ase_constructor(slab)

# Add species
kmc_model.add_species(name='empty', color='#ffffff')
kmc_model.add_species(name='H', representation="Atoms('H')", color='#ffff00')

#Add Processes
kmc_model.parse_and_add_process('H_adsorption_hollow1; ->H@hollow1; 100000')
kmc_model.parse_and_add_process('H_adsorption_hollow2; ->H@hollow2; 100000')

kmc_model.parse_and_add_process('H_desorption_hollow1; H@hollow1->; 100000')
kmc_model.parse_and_add_process('H_desorption_hollow2; H@hollow2->; 100000')


kmc_model.parse_and_add_process('H_diff_h1h2; H@hollow1 -> H@hollow2; 1000000000')
kmc_model.parse_and_add_process('H_diff_h2h1; H@hollow2 -> H@hollow1; 1000000000')


# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)