import kmcos
from kmcos.types import *
from kmcos.io import *
import numpy as np
import ase
from ase.io import read, write
from pathlib import Path
from kmcos.utils import get_ase_constructor
import os

model_name = str(os.path.basename(__file__)[+0:-3]).replace("__build", "")  # This line automatically names the model based on the python file’s name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the ‘__build’ part of the string. If you want to override this automatic naming, just set the variable ‘model_name’ equal to the string that you would like to use.
kmc_model = kmcos.create_kmc_model(model_name)
# Meta information
kmc_model.set_meta(author='Max J. Hoffmann',
            email='mjhoffmann@gmail.com',
            model_name='FePtBulk',
            model_dimension=3,
            debug=0)

fept = read("./FePt.cif").repeat([1,1,1])

kmc_model.add_species(name='empty',)
kmc_model.add_species(name='Fe',
               representation="Atoms('Fe')")
kmc_model.add_species(name='Pt',
               representation="Atoms('Pt')")
kmc_model.species_list.default_species = 'empty'

layer = kmc_model.add_layer(name='fept',)
#kmc_model.lattice.representation = f"""[Atoms(symbols='Fe',
#          pbc=np.array([ True,  True, True], dtype=bool),
#          cell=np.array({str((fept.cell / 2).tolist())}),
#          scaled_positions=np.array([[0,0,0]]),
#)]"""

kmc_model.lattice.cell = fept.cell / 2
layer.sites.append(Site(name='origin', pos='0 0 0', default_species='Fe'))

nn = {}
k = 0
nn[f"process_{k}"] = kmc_model.lattice.generate_coord(f'origin.(0,0,0).fept')
k += 1
for i in [-1, 1]:
    for j in [-1, 1]:
        nn[f"process_{k}"] = kmc_model.lattice.generate_coord(f'origin.(0,{i},{j}).fept')
        k += 1
        nn[f"process_{k}"] = kmc_model.lattice.generate_coord(f'origin.({j},0,{i}).fept')
        k += 1
        nn[f"process_{k}"] = kmc_model.lattice.generate_coord(f'origin.({i},{j},0).fept')
        k += 1

for i in nn.keys():
    kmc_model.add_parameter(name=f"fept_test_{i}", value=1e4, adjustable=True, min=1, max=1.e6, scale='log')

for i in nn.keys():
    if i == "process_0":
        pass
    else :
        kmc_model.add_process(name=i,
                    conditions=[Condition(species='Fe', coord=nn["process_0"]),
                                Condition(species='Pt', coord=nn[i])],
                    actions=[Action(species='Fe', coord=nn[i]),
                                Action(species='Pt', coord=nn["process_0"])],
                    rate_constant=f"fept_test_{i}")
                    
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)
