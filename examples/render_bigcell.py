#!/usr/bin/env python
"""Simple model generation script that demonstrate how
   big unit cell could be run periodically and
   non-periodically
"""

from kmcos.types import *

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

kmc_model.filename = 'big_cell.xml'
kmc_model.save()
