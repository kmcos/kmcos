#!/usr/bin/env python

from kmos.types import *
from kmos.io import *
from itertools import product
import numpy as np

model_name = "MyFirstSnapshots"
pt = Project()
pt.set_meta(author='Aditya (Ashi) Savara',
            email='savaraa@ornl.gov',
            model_name=model_name,
            model_dimension=2)

			
pt.add_species(name='empty', color='#ffffff')
pt.add_species(name='CO', color='#000000',
               representation="Atoms('CO',[[0,0,0],[0,0,1.2]])",
               tags='carbon')
			   
layer = pt.add_layer(name='simple_cubic')
layer.sites.append(Site(name='hollow', pos='0.5 0.5 0.5',
                        default_species='empty'))					
pt.lattice.cell = np.diag([3.5, 3.5, 10])
pt.add_parameter(name='T', value=600, adjustable=True, min=300, max=1500)
pt.add_parameter(name='p_COgas', value=.2, adjustable=True, scale='log', min=1e-13, max=1e3)
pt.add_parameter(name='A', value='(3.5*angstrom)**2')
pt.add_parameter(name='deltaG', value='-0.5', adjustable=True,
                           min=-1.3, max=0.3)
coord = pt.lattice.generate_coord('hollow.(0,0,0).simple_cubic')


# Adsorption process
pt.add_process(name='CO_adsorption',
               conditions=[Condition(species='empty', coord=coord)],
               actions=[Action(species='CO', coord=coord)],
               rate_constant='0.1*p_COgas*A*bar/sqrt(2*m_CO*umass/beta)')

pt.add_process(name='CO_desorption',
               conditions=[Condition(coord=coord, species='CO')],
               actions=[Action(coord=coord, species='empty')],
               rate_constant='p_COgas*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(-deltaG*eV)')

pt.filename = model_name + ".xml"
pt.save()
