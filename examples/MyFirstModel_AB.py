#!/usr/bin/env python

from kmcos.types import *
import kmcos

def main():
    model_name = str(__file__[+0:-3]).replace("__build", "") # This line automatically names the model based on the python file’s name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the ‘__build’ part of the string. If you want to override this automatic naming, just set the variable ‘model_name’ equal to the string that you would like to use.
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
