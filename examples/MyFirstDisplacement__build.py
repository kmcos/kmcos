"""
Simple adatom diffusion model
"""
import kmcos
from kmcos.types import *
from itertools import product
import numpy as np


model_name = str( os.path.basename(__file__)[+0:-3]).replace("__build", "") # This line automatically names the model based on the python fileâs name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the â__buildâ part of the string. If you want to override this automatic naming, just set the variable âmodel_nameâ equal to the string that you would like to use.

pt = kmcos.create_kmc_model(model_name)

#pt = Project()
# Meta information
pt.set_meta(author='Mie Andersen',
            email='mie.andersen@ch.tum.de',
            model_name=model_name, #Used to be'Au100_diffusion_model',
            model_dimension=2)

# Species
pt.add_species(name='empty', color='#d3d3d3')
pt.add_species(name='Au', color = '#00ff00',
               representation="Atoms('Au')")
pt.species_list.default_species = 'empty'

# Layers
layer = Layer(name='default')
layer.sites.append(Site(name='a', pos='0.5 0.5 0.5',
                        default_species='empty'))
pt.add_layer(layer)
pt.lattice.cell = np.diag([2.885, 2.885, 10])

# Parameters
pt.add_parameter(name= 'E_hop', value = 0.83)
pt.add_parameter(name= 'E_exc', value = 0.65)
pt.add_parameter(name= 'eps_int', value = 0.1, adjustable=True, min=0.0, max=0.2)
pt.add_parameter(name='T', value = 300)

# Coords
center = pt.lattice.generate_coord('a.(0,0,0).default')

#Coordinates for hopping diffusion
up = pt.lattice.generate_coord('a.(0,1,0).default')
down = pt.lattice.generate_coord('a.(0,-1,0).default')
left = pt.lattice.generate_coord('a.(-1,0,0).default')
right = pt.lattice.generate_coord('a.(1,0,0).default')

#Coordinates for exchange diffusion
right_up = pt.lattice.generate_coord('a.(1,1,0).default')
right_down = pt.lattice.generate_coord('a.(1,-1,0).default')
left_up = pt.lattice.generate_coord('a.(-1,1,0).default')
left_down = pt.lattice.generate_coord('a.(-1,-1,0).default')

# Processes
pt.add_process(name='hop_up',
               conditions=[Condition(species='Au', coord=center),
                           Condition(species='empty', coord=up)],
               actions=[Action(species='Au', coord=up),
                        Action(species='empty', coord=center)],
               rate_constant='1/(beta*h)*exp(-beta*E_hop*eV)')

pt.add_process(name='hop_down',
               conditions=[Condition(species='Au', coord=center),
                           Condition(species='empty', coord=down)],
               actions=[Action(species='Au', coord=down),
                        Action(species='empty', coord=center)],
               rate_constant='1/(beta*h)*exp(-beta*E_hop*eV)')

pt.add_process(name='hop_left',
               conditions=[Condition(species='Au', coord=center),
                           Condition(species='empty', coord=left)],
               actions=[Action(species='Au', coord=left),
                        Action(species='empty', coord=center)],
               rate_constant='1/(beta*h)*exp(-beta*E_hop*eV)')

pt.add_process(name='hop_right',
               conditions=[Condition(species='Au', coord=center),
                           Condition(species='empty', coord=right)],
               actions=[Action(species='Au', coord=right),
                        Action(species='empty', coord=center)],
               rate_constant='1/(beta*h)*exp(-beta*E_hop*eV)')

pt.add_process(name='exc_right_up',
               conditions=[Condition(species='Au', coord=center),
                           Condition(species='empty', coord=right_up)],
               actions=[Action(species='Au', coord=right_up),
                        Action(species='empty', coord=center)],
               rate_constant='1/(beta*h)*exp(-beta*E_exc*eV)')

pt.add_process(name='exc_right_down',
               conditions=[Condition(species='Au', coord=center),
                           Condition(species='empty', coord=right_down)],
               actions=[Action(species='Au', coord=right_down),
                        Action(species='empty', coord=center)],
               rate_constant='1/(beta*h)*exp(-beta*E_exc*eV)')

pt.add_process(name='exc_left_up',
               conditions=[Condition(species='Au', coord=center),
                           Condition(species='empty', coord=left_up)],
               actions=[Action(species='Au', coord=left_up),
                        Action(species='empty', coord=center)],
               rate_constant='1/(beta*h)*exp(-beta*E_exc*eV)')

pt.add_process(name='exc_left_down',
               conditions=[Condition(species='Au', coord=center),
                           Condition(species='empty', coord=left_down)],
               actions=[Action(species='Au', coord=left_down),
                        Action(species='empty', coord=center)],
               rate_constant='1/(beta*h)*exp(-beta*E_exc*eV)')

# Export
#pt.export_xml_file('Au100_diffusion_model.xml')

pt.print_statistics()
pt.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
pt.compile_options = "--acf"
pt.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
pt.save_model()
kmcos.compile(pt)
