#!/usr/bin/env python
"""
    Just a small cursory script how multi-dentate adsorption geometry
    can be implemented. The rules and rates contain no physical input
    and diffusion and rotation is also missing. But it would be
    straightforward to extend.

"""

from kmcos.types import *
import kmcos

model_name = str(__file__[+0:-3]).replace("__build", "") # This line automatically names the model based on the python file’s name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the ‘__build’ part of the string. If you want to override this automatic naming, just set the variable ‘model_name’ equal to the string that you would like to use.
kmc_model = kmcos.create_kmc_model(model_name)

kmc_model.add_species(name='empty')
kmc_model.add_species(name='CC_up', representation="Atoms('CC', [[0,0,0], [0,2,0]])")
kmc_model.add_species(name='CC_up_1', representation="")

kmc_model.add_species(name='CC_right', representation="Atoms('NN', [[0,0,0], [2,0,0]])")
kmc_model.add_species(name='CC_right_1', representation="")
layer = kmc_model.add_layer(name='simple_cubic')
layer.sites.append(Site(name='hollow', pos='0.5 0.5 0.5',
                        default_species='empty'))

kmc_model.lattice.cell = np.diag([3.5, 3.5, 10])

kmc_model.set_meta(author = 'Your Name',
            email = 'your.name@server.com',
            model_name = 'MyFirstModel',
            model_dimension = 2,)
kmc_model.add_parameter(name='A', value='(3.5*angstrom)**2')

kmc_model.add_parameter(name='adsorption_up', adjustable=True, min=1, max=1000, value=500)
kmc_model.add_parameter(name='desorption_up', adjustable=True, min=1, max=1000, value=500)

kmc_model.add_parameter(name='adsorption_right', adjustable=True, min=1, max=1000, value=500)
kmc_model.add_parameter(name='desorption_right', adjustable=True, min=1, max=1000, value=500)

coord = kmc_model.lattice.generate_coord

kmc_model.add_process(name="CC_adsorption_up",
               conditions=[Condition(species='empty', coord=coord('hollow')),
                           Condition(species='empty', coord=coord('hollow.(0,1,0)')),
                          ],
               actions=[Action(species='CC_up', coord=coord('hollow')),
                        Action(species='CC_up_1', coord=coord('hollow.(0,1,0)'))
                       ],
               rate_constant='adsorption_up')

kmc_model.add_process(name="CC_desorption_up",
               conditions=[Condition(species='CC_up', coord=coord('hollow')),
                          Condition(species='CC_up_1', coord=coord('hollow.(0,1,0)')),],
               actions=[Action(species='empty', coord=coord('hollow')),
                        Action(species='empty', coord=coord('hollow.(0,1,0)')),
                       ],
               rate_constant='desorption_up')

kmc_model.add_process(name="CC_adsorption_right",
               conditions=[Condition(species='empty', coord=coord('hollow')),
                           Condition(species='empty', coord=coord('hollow.(1,0,0)')),
                          ],
               actions=[Action(species='CC_right', coord=coord('hollow')),
                       Action(species='CC_right_1', coord=coord('hollow.(1,0,0)')),],
               rate_constant='adsorption_right')

kmc_model.add_process(name="CC_desorption_right",
               conditions=[Condition(species='CC_right', coord=coord('hollow')),
                          Condition(species='CC_right_1', coord=coord('hollow.(1,0,0)')),],

               actions=[Action(species='empty', coord=coord('hollow')), Action(species='empty', coord=coord('hollow.(1,0,0)')) ],
               rate_constant='desorption_right')

# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmcos.compile(kmc_model)