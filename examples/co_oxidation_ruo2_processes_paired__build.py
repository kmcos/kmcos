#!/usr/bin/env python

#DISCLAIMER: this is hacked down really quickly
#BEWARE OF BUGS

import kmcos
from kmcos.types import *
from kmcos.io import *
import numpy as np

model_name = str(__file__[+0:-3]).replace("__build", "") # This line automatically names the model based on the python file’s name. The brackets cut off zero characters from the beginning and three character from the end (".py"). The replace command removes the ‘__build’ part of the string. If you want to override this automatic naming, just set the variable ‘model_name’ equal to the string that you would like to use.
kmc_model = kmcos.create_kmc_model(model_name)

kmc_model.set_meta(author='Mie Andersen',
            email='mieand@gmail.com',
            model_name='CO_oxidation_Ruo2',
            model_dimension=2)

# Species
kmc_model.add_species(name='empty', color='#ffffff')
kmc_model.add_species(name='CO',
               color='#000000',
               representation="Atoms('CO',[[0,0,0],[0,0,1.2]])")
kmc_model.add_species(name='O',
               color='#ff0000',
               representation="Atoms('O')")

# Layer/Sites
layer = Layer(name='ruo2')
layer.sites.append(Site(name='bridge', pos='0.0 0.5 0.7'))
layer.sites.append(Site(name='cus', pos='0.5 0.5 0.7'))

kmc_model.add_layer(layer)

kmc_model.lattice.representation = """[
Atoms(symbols='O2Ru2',
          pbc=np.array([False, False, False], dtype=bool),
          cell=np.array(
      [[  6.39 ,   0.   ,   0.   ],
       [  0.   ,   3.116,   0.   ],
       [  0.   ,   0.   ,  20.   ]]),
          positions=np.array(
      [[  4.435981  ,   0.        ,  12.7802862 ],
       [  1.95416379,   0.        ,  12.7802862 ],
       [  0.        ,   0.        ,  12.7802862 ],
       [  3.1950724 ,   1.5582457 ,  12.7802862 ]]))

]"""
kmc_model.lattice.cell = np.diag([6.43, 3.12, 20])

# Parameters

kmc_model.add_parameter(name='p_COgas', value=1, adjustable=True, min=1e-13, max=1e2,
                 scale='log')
kmc_model.add_parameter(name='p_O2gas', value=1, adjustable=True, min=1e-15, max=1e2,
                 scale='log')
kmc_model.add_parameter(name='T', value=450, adjustable=True, min=300, max=1500)

kmc_model.add_parameter(name='A', value='%s*angstrom**2' % (kmc_model.lattice.cell[0,0]*
                                                      kmc_model.lattice.cell[1,1]))
kmc_model.add_parameter(name='E_O_bridge', value=-2.3)
kmc_model.add_parameter(name='E_O_cus', value=-1.0)
kmc_model.add_parameter(name='E_CO_bridge', value=-1.6)
kmc_model.add_parameter(name='E_CO_cus', value=-1.3)

kmc_model.add_parameter(name='E_react_Ocus_COcus', value=0.9)
kmc_model.add_parameter(name='E_react_Ocus_CObridge', value=0.8)
kmc_model.add_parameter(name='E_react_Obridge_COcus', value=1.2)
kmc_model.add_parameter(name='E_react_Obridge_CObridge', value=1.5)

kmc_model.add_parameter(name='E_COdiff_cus_cus', value=1.7)
kmc_model.add_parameter(name='E_COdiff_cus_bridge', value=1.3)
kmc_model.add_parameter(name='E_COdiff_bridge_bridge', value=0.6)
kmc_model.add_parameter(name='E_COdiff_bridge_cus', value=1.6)

kmc_model.add_parameter(name='E_Odiff_cus_cus', value=1.6)
kmc_model.add_parameter(name='E_Odiff_bridge_bridge', value=0.7)
kmc_model.add_parameter(name='E_Odiff_bridge_cus', value=2.3)
kmc_model.add_parameter(name='E_Odiff_cus_bridge', value=1.0)


# Coordinates

cus = kmc_model.lattice.generate_coord('cus.(0,0,0).ruo2')
cus_right = kmc_model.lattice.generate_coord('bridge.(1,0,0).ruo2')
cus_up = kmc_model.lattice.generate_coord('cus.(0,1,0).ruo2')

bridge = kmc_model.lattice.generate_coord('bridge.(0,0,0).ruo2')
bridge_right = kmc_model.lattice.generate_coord('cus.(0,0,0).ruo2')
bridge_up = kmc_model.lattice.generate_coord('bridge.(0,1,0).ruo2')

# Processes

# CO Adsorption/Desorption
kmc_model.add_process(name='CO_adsorption_cus',
               conditions=[Condition(species='empty', coord=cus)],
               actions=[Action(species='CO', coord=cus)],
               rate_constant='p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)')
kmc_model.add_process(name='CO_desorption_cus',
               conditions=[Condition(species='CO', coord=cus)],
               actions=[Action(species='empty', coord=cus)],
               rate_constant='p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(beta*(E_CO_cus-mu_COgas)*eV)')

kmc_model.add_process(name='CO_adsorption_bridge',
               conditions=[Condition(species='empty', coord=bridge)],
               actions=[Action(species='CO', coord=bridge)],
               rate_constant='p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)')
kmc_model.add_process(name='CO_desorption_bridge',
               conditions=[Condition(species='CO', coord=bridge)],
               actions=[Action(species='empty', coord=bridge)],
               rate_constant='p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(beta*(E_CO_bridge-mu_COgas)*eV)')

# CO diffusion

# cus/cus
kmc_model.add_process(name='COdiff_cus_up',
               conditions=[Condition(species='CO', coord=cus),
                           Condition(species='empty', coord=cus_up)],
               actions=[Condition(species='empty', coord=cus),
                        Condition(species='CO', coord=cus_up)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_COdiff_cus_cus)*eV)')

kmc_model.add_process(name='COdiff_cus_down',
               conditions=[Condition(species='CO', coord=cus_up),
                           Condition(species='empty', coord=cus)],
               actions=[Condition(species='empty', coord=cus_up),
                        Condition(species='CO', coord=cus)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_COdiff_cus_cus)*eV)')

# bridge/bridge
kmc_model.add_process(name='COdiff_bridge_up',
               conditions=[Condition(species='CO', coord=bridge),
                           Condition(species='empty', coord=bridge_up)],
               actions=[Condition(species='empty', coord=bridge),
                        Condition(species='CO', coord=bridge_up)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_COdiff_bridge_bridge)*eV)')
kmc_model.add_process(name='COdiff_bridge_down',
               conditions=[Condition(species='CO', coord=bridge_up),
                           Condition(species='empty', coord=bridge)],
               actions=[Condition(species='empty', coord=bridge_up),
                        Condition(species='CO', coord=bridge)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_COdiff_bridge_bridge)*eV)')

# bridge/cus
kmc_model.add_process(name='COdiff_bridge_right',
               conditions=[Condition(species='CO', coord=bridge),
                           Condition(species='empty', coord=bridge_right)],
               actions=[Condition(species='empty', coord=bridge),
                        Condition(species='CO', coord=bridge_right)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_COdiff_bridge_cus)*eV)')

kmc_model.add_process(name='COdiff_bridge_left',
               conditions=[Condition(species='CO', coord=bridge_right),
                           Condition(species='empty', coord=bridge)],
               actions=[Condition(species='empty', coord=bridge_right),
                        Condition(species='CO', coord=bridge)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_COdiff_cus_bridge)*eV)')

# bridge/cus
kmc_model.add_process(name='COdiff_cus_right',
               conditions=[Condition(species='CO', coord=cus),
                           Condition(species='empty', coord=cus_right)],
               actions=[Condition(species='empty', coord=cus),
                        Condition(species='CO', coord=cus_right)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_COdiff_cus_bridge)*eV)')

kmc_model.add_process(name='COdiff_cus_left',
               conditions=[Condition(species='CO', coord=cus_right),
                           Condition(species='empty', coord=cus)],
               actions=[Condition(species='empty', coord=cus_right),
                        Condition(species='CO', coord=cus)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_COdiff_bridge_cus)*eV)')


# O2 Adsorption/Desorption
# avoiding double-counting ...
kmc_model.add_process(name='O2_adsorption_cus_up',
               conditions=[Condition(species='empty', coord=cus),
                        Condition(species='empty', coord=cus_up),],
               actions=[Condition(species='O', coord=cus),
                        Condition(species='O', coord=cus_up),],
               rate_constant='p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)')

kmc_model.add_process(name='O2_desorption_cus_up',
               conditions=[Condition(species='O', coord=cus),
                        Condition(species='O', coord=cus_up),],
               actions=[Condition(species='empty', coord=cus),
                        Condition(species='empty', coord=cus_up),],
               rate_constant='p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)*exp(beta*(2*E_O_cus-mu_O2gas)*eV)')

kmc_model.add_process(name='O2_adsorption_cus_right',
               conditions=[Condition(species='empty', coord=cus),
                        Condition(species='empty', coord=cus_right),],
               actions=[Condition(species='O', coord=cus),
                        Condition(species='O', coord=cus_right),],
               rate_constant='p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)')

kmc_model.add_process(name='O2_desorption_cus_right',
               conditions=[Condition(species='O', coord=cus),
                        Condition(species='O', coord=cus_right),],
               actions=[Condition(species='empty', coord=cus),
                        Condition(species='empty', coord=cus_right),],
               rate_constant='p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)*exp(beta*((E_O_cus+E_O_bridge)-mu_O2gas)*eV)')

kmc_model.add_process(name='O2_adsorption_bridge_up',
               conditions=[Condition(species='empty', coord=bridge),
                        Condition(species='empty', coord=bridge_up),],
               actions=[Condition(species='O', coord=bridge),
                        Condition(species='O', coord=bridge_up),],
               rate_constant='p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)')

kmc_model.add_process(name='O2_desorption_bridge_up',
               conditions=[Condition(species='O', coord=bridge),
                        Condition(species='O', coord=bridge_up),],
               actions=[Condition(species='empty', coord=bridge),
                        Condition(species='empty', coord=bridge_up),],
               rate_constant='p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)*exp(beta*(2*E_O_bridge-mu_O2gas)*eV)')

kmc_model.add_process(name='O2_adsorption_bridge_right',
               conditions=[Condition(species='empty', coord=bridge),
                        Condition(species='empty', coord=bridge_right),],
               actions=[Condition(species='O', coord=bridge),
                        Condition(species='O', coord=bridge_right),],
               rate_constant='p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)')

kmc_model.add_process(name='O2_desorption_bridge_right',
               conditions=[Condition(species='O', coord=bridge),
                        Condition(species='O', coord=bridge_right),],
               actions=[Condition(species='empty', coord=bridge),
                        Condition(species='empty', coord=bridge_right),],
               rate_constant='p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)*exp(beta*((E_O_bridge+E_O_cus)-mu_O2gas)*eV)')


# O diffusion

# cus/cus
kmc_model.add_process(name='Odiff_cus_up',
               conditions=[Condition(species='O', coord=cus),
                           Condition(species='empty', coord=cus_up)],
               actions=[Condition(species='empty', coord=cus),
                        Condition(species='O', coord=cus_up)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_Odiff_cus_cus)*eV)')

kmc_model.add_process(name='Odiff_cus_down',
               conditions=[Condition(species='O', coord=cus_up),
                           Condition(species='empty', coord=cus)],
               actions=[Condition(species='empty', coord=cus_up),
                        Condition(species='O', coord=cus)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_Odiff_cus_cus)*eV)')


# bridge/bridge
kmc_model.add_process(name='Odiff_bridge_up',
               conditions=[Condition(species='O', coord=bridge),
                           Condition(species='empty', coord=bridge_up)],
               actions=[Condition(species='empty', coord=bridge),
                        Condition(species='O', coord=bridge_up)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_Odiff_bridge_bridge)*eV)')
kmc_model.add_process(name='Odiff_bridge_down',
               conditions=[Condition(species='O', coord=bridge_up),
                           Condition(species='empty', coord=bridge)],
               actions=[Condition(species='empty', coord=bridge_up),
                        Condition(species='O', coord=bridge)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_Odiff_bridge_bridge)*eV)')
# bridge/cus
kmc_model.add_process(name='Odiff_bridge_right',
               conditions=[Condition(species='O', coord=bridge),
                           Condition(species='empty', coord=bridge_right)],
               actions=[Condition(species='empty', coord=bridge),
                        Condition(species='O', coord=bridge_right)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_Odiff_bridge_cus)*eV)')

kmc_model.add_process(name='Odiff_bridge_left',
               conditions=[Condition(species='O', coord=bridge_right),
                           Condition(species='empty', coord=bridge)],
               actions=[Condition(species='empty', coord=bridge_right),
                        Condition(species='O', coord=bridge)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_Odiff_cus_bridge)*eV)')

# bridge/cus
kmc_model.add_process(name='Odiff_cus_right',
               conditions=[Condition(species='O', coord=cus),
                           Condition(species='empty', coord=cus_right)],
               actions=[Condition(species='empty', coord=cus),
                        Condition(species='O', coord=cus_right)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_Odiff_cus_bridge)*eV)')

kmc_model.add_process(name='Odiff_cus_left',
               conditions=[Condition(species='O', coord=cus_right),
                           Condition(species='empty', coord=cus)],
               actions=[Condition(species='empty', coord=cus_right),
                        Condition(species='O', coord=cus)],
                rate_constant='(beta*h)**(-1)*exp(-beta*(E_Odiff_bridge_cus)*eV)')


# Reaction
kmc_model.add_process(name='React_cus_up',
               conditions=[Condition(species='O', coord=cus),
                           Condition(species='CO', coord=cus_up)],
               actions=[Action(species='empty', coord=cus),
                        Action(species='empty', coord=cus_up)],
                rate_constant='(beta*h)**(-1)*exp(-beta*E_react_Ocus_COcus*eV)',
                tof_count={'CO_oxidation':1})

kmc_model.add_process(name='Ads_cus_up',
               conditions=[Condition(species='empty', coord=cus),
                           Condition(species='empty', coord=cus_up)],
               actions=[Action(species='O', coord=cus),
                        Action(species='CO', coord=cus_up)],
                rate_constant='0',
                tof_count={'CO_oxidation':-1})


kmc_model.add_process(name='React_cus_down',
               conditions=[Condition(species='O', coord=cus_up),
                           Condition(species='CO', coord=cus)],
               actions=[Action(species='empty', coord=cus_up),
                        Action(species='empty', coord=cus)],
                rate_constant='(beta*h)**(-1)*exp(-beta*E_react_Ocus_COcus*eV)',
                tof_count={'CO_oxidation':1})

kmc_model.add_process(name='Ads_cus_down',
               conditions=[Condition(species='empty', coord=cus_up),
                           Condition(species='empty', coord=cus)],
               actions=[Action(species='O', coord=cus_up),
                        Action(species='CO', coord=cus)],
                rate_constant='0',
                tof_count={'CO_oxidation':-1})


kmc_model.add_process(name='React_cus_right',
               conditions=[Condition(species='O', coord=cus),
                           Condition(species='CO', coord=cus_right)],
               actions=[Action(species='empty', coord=cus),
                        Action(species='empty', coord=cus_right)],
                rate_constant='(beta*h)**(-1)*exp(-beta*E_react_Ocus_CObridge*eV)',
                tof_count={'CO_oxidation':1})

kmc_model.add_process(name='Ads_cus_right',
               conditions=[Condition(species='empty', coord=cus),
                           Condition(species='empty', coord=cus_right)],
               actions=[Action(species='O', coord=cus),
                        Action(species='CO', coord=cus_right)],
                rate_constant='0',
                tof_count={'CO_oxidation':-1})


kmc_model.add_process(name='React_cus_left',
               conditions=[Condition(species='O', coord=cus_right),
                           Condition(species='CO', coord=cus)],
               actions=[Action(species='empty', coord=cus_right),
                        Action(species='empty', coord=cus)],
                rate_constant='(beta*h)**(-1)*exp(-beta*E_react_Obridge_COcus*eV)',
                tof_count={'CO_oxidation':1})

kmc_model.add_process(name='Ads_cus_left',
               conditions=[Condition(species='empty', coord=cus_right),
                           Condition(species='empty', coord=cus)],
               actions=[Action(species='O', coord=cus_right),
                        Action(species='CO', coord=cus)],
                rate_constant='0',
                tof_count={'CO_oxidation':-1})


kmc_model.add_process(name='React_bridge_up',
               conditions=[Condition(species='O', coord=bridge),
                           Condition(species='CO', coord=bridge_up)],
               actions=[Action(species='empty', coord=bridge),
                        Action(species='empty', coord=bridge_up)],
                rate_constant='(beta*h)**(-1)*exp(-beta*E_react_Obridge_CObridge*eV)',
                tof_count={'CO_oxidation':1})

kmc_model.add_process(name='Ads_bridge_up',
               conditions=[Condition(species='empty', coord=bridge),
                           Condition(species='empty', coord=bridge_up)],
               actions=[Action(species='O', coord=bridge),
                        Action(species='CO', coord=bridge_up)],
                rate_constant='0',
                tof_count={'CO_oxidation':-1})


kmc_model.add_process(name='React_bridge_down',
               conditions=[Condition(species='O', coord=bridge_up),
                           Condition(species='CO', coord=bridge)],
               actions=[Action(species='empty', coord=bridge_up),
                        Action(species='empty', coord=bridge)],
                rate_constant='(beta*h)**(-1)*exp(-beta*E_react_Obridge_CObridge*eV)',
                tof_count={'CO_oxidation':1})

kmc_model.add_process(name='Ads_bridge_down',
               conditions=[Condition(species='empty', coord=bridge_up),
                           Condition(species='empty', coord=bridge)],
               actions=[Action(species='O', coord=bridge_up),
                        Action(species='CO', coord=bridge)],
                rate_constant='0',
                tof_count={'CO_oxidation':-1})


kmc_model.add_process(name='React_bridge_right',
               conditions=[Condition(species='O', coord=bridge),
                           Condition(species='CO', coord=bridge_right)],
               actions=[Action(species='empty', coord=bridge),
                        Action(species='empty', coord=bridge_right)],
                rate_constant='(beta*h)**(-1)*exp(-beta*E_react_Obridge_COcus*eV)',
                tof_count={'CO_oxidation':1})

kmc_model.add_process(name='Ads_bridge_right',
               conditions=[Condition(species='empty', coord=bridge),
                           Condition(species='empty', coord=bridge_right)],
               actions=[Action(species='O', coord=bridge),
                        Action(species='CO', coord=bridge_right)],
                rate_constant='0',
                tof_count={'CO_oxidation':-1})


kmc_model.add_process(name='React_bridge_left',
               conditions=[Condition(species='O', coord=bridge_right),
                           Condition(species='CO', coord=bridge)],
               actions=[Action(species='empty', coord=bridge_right),
                        Action(species='empty', coord=bridge)],
                rate_constant='(beta*h)**(-1)*exp(-beta*E_react_Ocus_CObridge*eV)',
                tof_count={'CO_oxidation':1})

kmc_model.add_process(name='Ads_bridge_left',
               conditions=[Condition(species='empty', coord=bridge_right),
                           Condition(species='empty', coord=bridge)],
               actions=[Action(species='O', coord=bridge_right),
                        Action(species='CO', coord=bridge)],
                rate_constant='0',
                tof_count={'CO_oxidation':-1})


# Save the model to an xml file
###It's good to simply copy and paste the below lines between model creation files.
kmc_model.print_statistics()
kmc_model.backend = 'local_smart' #specifying is optional. 'local_smart' is the default. Currently, the other options are 'lat_int' and 'otf'
kmc_model.clear_model() #This line is optional: if you are updating a model, this line will remove the old model files (including compiled files) before exporting the new one. It is convenient to always include this line because then you don't need to 'confirm' removing/overwriting the old model during the compile step.
kmc_model.save_model()
kmc_model.compile_options = ' -t '
kmcos.compile(kmc_model)
