#!/usr/bin/env python

from kmcos.types import *
import kmcos

def main():
    model_name = __file__[+0:-3] # This is the python file name, the brackets cut off zero characters from the beginning and three character from the end (".py").  To manually name the model just place a string here.
    model_name = model_name.replace("__build", "")
    kmc_model = kmcos.create_kmc_model(model_name)
# Meta
    kmc_model.meta.author = 'Max J. Hoffmann'
    kmc_model.meta.email = 'mjhoffmann@gmail.com'
    kmc_model.meta.model_name = 'AB_no_diffusion'
    kmc_model.meta.model_dimension = 2
    kmc_model.meta.debug = 0


# add species
    kmc_model.add_species(name='empty')
    kmc_model.add_species(name='A', representation="Atoms('O')")
    kmc_model.add_species(name='B', representation="Atoms('CO', [[0,0,0],[0,0,1.2]])")

# add sites/layer
    layer = Layer(name='default')
    layer.sites.append(Site(name='a'))
    kmc_model.add_layer(layer)
    kmc_model.species_list.default_species = 'empty'


# add parameter
    parameters = {}
    parameters['p_COgas'] = {'value':1., 'adjustable':True,
                                         'min':1.e-13, 'max':1.e2,
                                         'scale':'log'}
    parameters['p_O2gas'] = {'value':1., 'adjustable':True,
                                         'min':1.e-13, 'max':1.e2,
                                         'scale':'log'}
    parameters['T'] = {'value':600}
    parameters['A'] = {'value':1.552e-19}
    parameters['E_bind_O2'] = {'value':-2.138}
    parameters['E_bind_CO'] = {'value':-1.9}
    parameters['E_react'] = {'value': 0.9}


    for key, value in parameters.items():
        kmc_model.add_parameter(name=key, **value)


    coord = kmc_model.lattice.generate_coord('a.(0,0,0).default')
    up = kmc_model.lattice.generate_coord('a.(0,1,0).default')
    right = kmc_model.lattice.generate_coord('a.(1,0,0).default')
    down = kmc_model.lattice.generate_coord('a.(0,-1,0).default')
    left = kmc_model.lattice.generate_coord('a.(-1,0,0).default')

    kmc_model.add_process(name='A_adsorption',
                   rate_constant='p_O2gas*bar*A/sqrt(2*pi*m_O2*umass/beta)',
                   condition_list=[Condition(coord=coord, species='empty')],
                   action_list=[Action(coord=coord, species='A')],)

    kmc_model.add_process(name='A_desorption',
                   rate_constant='p_O2gas*bar*A/sqrt(2*pi*m_O2*umass/beta)*exp(beta*(E_bind_O2-mu_O2gas)*eV)',
                   condition_list=[Condition(coord=coord, species='A')],
                   action_list=[Action(coord=coord, species='empty')],)

    kmc_model.add_process(name='B_adsorption',
                   rate_constant='p_COgas*bar*A/sqrt(2*pi*m_CO*umass/beta)',
                   condition_list=[Condition(coord=coord, species='empty')],
                   action_list=[Action(coord=coord, species='B')],)

    kmc_model.add_process(name='B_desorption',
                   rate_constant='p_COgas*bar*A/sqrt(2*pi*m_CO*umass/beta)*exp(beta*(E_bind_CO-mu_COgas)*eV)',
                   condition_list=[Condition(coord=coord, species='B')],
                   action_list=[Condition(coord=coord, species='empty')],)

    for neighbor, name in [(right, 'right'),
                           (left, 'left'),
                           (up, 'up'),
                           (down, 'down')]:
        kmc_model.add_process(name='AB_react_%s' % name,
                       rate_constant='1/(beta*h)*exp(-beta*E_react*eV)',
                       condition_list=[Condition(coord=coord, species='A'),
                                       Condition(coord=neighbor, species='B')],
                       action_list=[Action(coord=coord, species='empty'),
                                   Action(coord=neighbor, species='empty')],
                       tof_count={'TOF':1})


    return kmc_model

if __name__ == '__main__':
    kmc_model = main()
    kmc_model.save('AB_model.ini')
    # Save the model to an xml file
    ###It's good to simply copy and paste the below lines between model creation files.
    kmc_model.print_statistics()
    kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
    kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
    kmc_model.save_model()
    kmcos.compile(kmc_model)
