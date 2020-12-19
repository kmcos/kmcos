#!/usr/bin/env python

from kmcos.types import *
from kmcos.io import *
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
               rate_constant='0.1*p_COgas*A*bar/sqrt(2*m_CO*umass/beta)',
               tof_count={'CO_adsorption':1}) 

pt.add_process(name='CO_desorption',
               conditions=[Condition(coord=coord, species='CO')],
               actions=[Action(coord=coord, species='empty')],
               rate_constant='p_COgas*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(-deltaG*eV)',
               tof_count={'CO_desorption':1}) 

###It's good to simply copy and paste the below lines between model creation files.
pt.filename = model_name + ".xml"
pt.backend = 'local_smart' #specifying is optional. local_smart is the dfault. Currently, the other options are 'lat_int' and 'otf'
pt.clear_model(model_name, backend=pt.backend) #This line is optional: if you are updating a model, this line will remove the old model before exporting the new one. It is convenent to always include this line because then you don't need to 'confirm' removing the old model.
pt.save()
kmcos.export(pt.filename + ' -b ' + pt.backend) #alternatively, one can use: kmcos.cli.main('export '+  pt.filename + ' -b' + pt.backend)