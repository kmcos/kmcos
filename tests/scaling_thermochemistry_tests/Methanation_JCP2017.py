from kmcos.types import *
from kmcos.io import *
import kmcos
import numpy as np
import sys
sys.path.insert(0,'..') #This is for the janaf_data directory.

# This is a KMC model for methanation published in:
# The Journal of Chemical Physics 147, 152705 (2017); doi: 10.1063/1.4989511

kmc_model = kmcos.create_kmc_model()
kmc_model.set_meta(author = 'Mie Andersen',
            email = 'mie.andersen@ch.tum.de',
            model_name = 'Methanation_JCP2017',
            model_dimension = 2)

kmc_model.add_species(name='empty', color='#ffffff')
kmc_model.add_species(name='CO',
               color='#00ff00',
               representation="Atoms('CO',[[0,0,0],[0,0,1.2]])")
kmc_model.add_species(name='OH',
               color='#0065bd',
               representation="Atoms('OH',[[0,0,0],[0,0,0.96]])")
kmc_model.add_species(name='O',
               color='#ff0000',
               representation="Atoms('O')")
kmc_model.add_species(name='C',
               color='#D3D3D3',
               representation="Atoms('C')")
kmc_model.add_species(name='CH',
               color='#ffff00',
               representation="Atoms('CH',[[0,0,0],[0,0,1.09]])")
kmc_model.add_species(name='CH2',
               color='#FFA500',
               representation="Atoms('CH2',[[0,0,0],[0,0.7,0.8],[0,-0.7,0.8]])")
kmc_model.add_species(name='CH3',
               color='#551a8b',
               representation="Atoms('CH3',[[0,0,0],[-0.3,0.5,0.8],[-0.3,-0.5,0.8],[0.7,0,0.8]])")

layer = kmc_model.add_layer(name='Rh211')

kmc_model.lattice.cell = np.array(
      [[  6.582, 0.000,  0.000  ],
       [  0.000, 2.686,  0.000  ],
       [  0.000, 0.000, 20.000  ]])

kmc_model.lattice.representation = """[
Atoms(symbols='Rh3',
          pbc=np.array([False, False, False], dtype=bool),
          cell=np.array(
      [[  6.582, 0.000,  0.000  ],
       [  0.000, 2.686,  0.000  ],
       [  0.000, 0.000, 20.000  ]]),
          positions=np.array(
      [[  0.000, 0.000, 10.776  ],
       [  2.195, 1.344, 10.000  ],
       [  4.389, 0.000,  9.224  ]]))

]"""

layer.sites.append(Site(name='s', pos='0.121 0.5 0.6', #step abs coordinates 0.8 1.344 12
                        default_species='empty'))
layer.sites.append(Site(name='t', pos='0.5 0.0 0.545', #terrace abs coordinates 3.3 0 10.9
                        default_species='empty'))
layer.sites.append(Site(name='f', pos='0.774 0.5 0.53', #fourfold abs coordinates 5.1 1.344 10.6
                        default_species='empty'))

kmc_model.add_parameter(name='T', value=523., adjustable=True, min=400, max=800)
kmc_model.add_parameter(name='p_COgas', value=0.01, adjustable=True, min=1e-10, max=1.e2)
kmc_model.add_parameter(name='p_CH4gas', value=0.01, adjustable=True, min=1e-10, max=1.e2)
kmc_model.add_parameter(name='p_H2Ogas', value=0.01, adjustable=True, min=1e-10, max=1.e2)
kmc_model.add_parameter(name='p_H2gas', value=0.97, adjustable=True, min=1e-10, max=1.e2)

kmc_model.add_parameter(name='A', value='6.582*2.686*angstrom**2') #area of unit cell
kmc_model.add_parameter(name='alpha', value='0.5') #BEP slope for diffusion

#gas phase formation energies
kmc_model.add_parameter(name='E_COgas', value='2.53')
kmc_model.add_parameter(name='E_H2Ogas', value='0')
kmc_model.add_parameter(name='E_CH4gas', value='0')
kmc_model.add_parameter(name='E_H2gas', value='0')

#scaling parameters
#MF max volcano
kmc_model.add_parameter(name='E_C', value='1.75', adjustable=True, min=0, max=3.4)
kmc_model.add_parameter(name='E_O', value='-1.35', adjustable=True, min=-1.8, max=1.4)

#analytical MF solution to H coverage
kmc_model.add_parameter(name='H_cov', value='(1/(1+sqrt(exp(-beta*(GibbsGas_H2gas-2*GibbsAds_H_t)*eV))))')

#adsorption and TS energies
with open('methanation_kmc_adsorbate_scaling_input.txt') as infile:
    lines = infile.readlines()

for line in lines[1:]:
    if line.strip():
        values = line.strip().split('\t')
        kmc_model.add_parameter(name='E_'+str(values[0]), value='(%.7f*E_C+%.7f*E_O+(%.7f))'%(float(values[1]),float(values[2]),float(values[3])))
        kmc_model.add_parameter(name='f_'+str(values[0]), value=values[4])

#BEP offset for diffusion
kmc_model.add_parameter(name='E_CO_diff', value='0.11')
kmc_model.add_parameter(name='E_O_diff', value='0.82')
kmc_model.add_parameter(name='E_OH_diff', value='0.44')
kmc_model.add_parameter(name='E_C_diff', value='0.48')
kmc_model.add_parameter(name='E_CH_diff', value='0.37')
kmc_model.add_parameter(name='E_CH2_diff', value='0.61')
kmc_model.add_parameter(name='E_CH3_diff', value='0.51')

#Site definitions
s = kmc_model.lattice.generate_coord('s.(0,0,0).Rh211')
t = kmc_model.lattice.generate_coord('t.(0,0,0).Rh211')
f = kmc_model.lattice.generate_coord('f.(0,0,0).Rh211')

s_N = kmc_model.lattice.generate_coord('s.(0,1,0).Rh211')
s_S = kmc_model.lattice.generate_coord('s.(0,-1,0).Rh211')
s_E = kmc_model.lattice.generate_coord('s.(1,0,0).Rh211')
t_N = kmc_model.lattice.generate_coord('t.(0,1,0).Rh211')
t_S = kmc_model.lattice.generate_coord('t.(0,-1,0).Rh211')
t_W = kmc_model.lattice.generate_coord('t.(-1,0,0).Rh211')
t_NW = kmc_model.lattice.generate_coord('t.(-1,1,0).Rh211')
f_N = kmc_model.lattice.generate_coord('f.(0,1,0).Rh211')
f_S = kmc_model.lattice.generate_coord('f.(0,-1,0).Rh211')
f_W = kmc_model.lattice.generate_coord('f.(-1,0,0).Rh211')
f_NW = kmc_model.lattice.generate_coord('f.(-1,1,0).Rh211')

#CO ads/des processes
for site in [s, t]:
    kmc_model.add_process(name='CO_ads_%s' % str(site)[8],
                rate_constant='p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_%s)-GibbsGas_COgas)*eV)' % (str(site)[8]),
                conditions=[Condition(coord=site, species='empty')],
                actions=[Action(coord=site, species='CO')])
for site in [s, t]:
    kmc_model.add_process(name='CO_des_%s' % str(site)[8],
                rate_constant='p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_%s)-GibbsAds_CO_%s)*eV)' % (str(site)[8],str(site)[8]),
                conditions=[Condition(coord=site, species='CO')],
                actions=[Action(coord=site, species='empty')])

#H-CO reactions
for site,name in [(t_W,'t_W'), (t_NW,'t_NW')]:
    kmc_model.add_process(name='H_CO_s_react_%s' % name,
                rate_constant='H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_s+GibbsAds_H_t),0)*eV)',
                condition_list=[Condition(coord=s, species='CO'),
                                Condition(coord=f_W, species='empty'),
                                Condition(coord=site, species='empty')],
                action_list=[Action(coord=s, species='empty'),
                             Action(coord=f_W, species='C'),
                             Action(coord=site, species='OH')])

for site,name in [(f,'f'), (f_S,'f_S')]:
    kmc_model.add_process(name='H_CO_t_react_%s' % name,
                rate_constant='H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_t+GibbsAds_H_t),0)*eV)',
                condition_list=[Condition(coord=t, species='CO'),
                                Condition(coord=site, species='empty')],
                action_list=[Action(coord=t, species='OH'),
                             Action(coord=site, species='C')])

for site,name in [(t_W,'t_W'), (t_NW,'t_NW')]:
    kmc_model.add_process(name='C_OH_s_react_%s' % name,
                rate_constant='(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_s+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)',
                condition_list=[Condition(coord=s, species='empty'),
                                Condition(coord=f_W, species='C'),
                                Condition(coord=site, species='OH')],
                action_list=[Action(coord=s, species='CO'),
                             Action(coord=f_W, species='empty'),
                             Action(coord=site, species='empty')])

for site,name in [(f,'f'), (f_S,'f_S')]:
    kmc_model.add_process(name='C_OH_t_react_%s' % name,
                rate_constant='(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_t+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)',
                condition_list=[Condition(coord=site, species='C'),
                                Condition(coord=t, species='OH')],
                action_list=[Action(coord=site, species='empty'),
                             Action(coord=t, species='CO')])

#H-C reactions
for site in [f, s, t]:
    kmc_model.add_process(name='H_C_%s_react' % str(site)[8],
                rate_constant='H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_%s,GibbsAds_CH_%s)-(GibbsAds_C_%s+GibbsAds_H_t),0)*eV)' %(str(site)[8],str(site)[8],str(site)[8]),
                condition_list=[Condition(coord=site, species='C')],
                action_list=[Action(coord=site, species='CH')])

for site in [f, s, t]:
    kmc_model.add_process(name='CH_%s_dis' % str(site)[8],
                rate_constant='(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_%s,GibbsAds_C_%s+GibbsAds_H_t)-GibbsAds_CH_%s,0)*eV)' %(str(site)[8],str(site)[8],str(site)[8]),
                condition_list=[Condition(coord=site, species='CH')],
                action_list=[Action(coord=site, species='C')])

#H-CH reactions
for site,name in [(s_E,'s_E'), (t,'t'), (t_N,'t_N')]:
    kmc_model.add_process(name='H_CH_f_react_%s' % name,
                rate_constant='H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH2_%s)-(GibbsAds_CH_f+GibbsAds_H_t),0)*eV)' % (str(site)[8]),
                condition_list=[Condition(coord=f, species='CH'),
                                Condition(coord=site, species='empty')],
                action_list=[Action(coord=f, species='empty'),
                             Action(coord=site, species='CH2')])

for site in [s, t]:
    kmc_model.add_process(name='H_CH_%s_react' % str(site)[8],
                rate_constant='H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_%s,GibbsAds_CH2_%s)-(GibbsAds_CH_%s+GibbsAds_H_t),0)*eV)' %(str(site)[8],str(site)[8],str(site)[8]),
                condition_list=[Condition(coord=site, species='CH')],
                action_list=[Action(coord=site, species='CH2')])

for site,name in [(s_E,'s_E'), (t,'t'), (t_N,'t_N')]:
    kmc_model.add_process(name='CH2_%s_dis_f' % name,
                rate_constant='(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH_f+GibbsAds_H_t)-GibbsAds_CH2_%s,0)*eV)' % (str(site)[8]),
                condition_list=[Condition(coord=f, species='empty'),
                                Condition(coord=site, species='CH2')],
                action_list=[Action(coord=f, species='CH'),
                             Action(coord=site, species='empty')])

for site in [s, t]:
    kmc_model.add_process(name='CH2_%s_dis' % str(site)[8],
                rate_constant='(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_%s,GibbsAds_CH_%s+GibbsAds_H_t)-GibbsAds_CH2_%s,0)*eV)' %(str(site)[8],str(site)[8],str(site)[8]),
                condition_list=[Condition(coord=site, species='CH2')],
                action_list=[Action(coord=site, species='CH')])

#H-CH2 reactions
for site in [s, t]:
    kmc_model.add_process(name='H_CH2_%s_react' % str(site)[8],
                rate_constant='H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_%s,GibbsAds_CH3_%s)-(GibbsAds_CH2_%s+GibbsAds_H_t),0)*eV)' %(str(site)[8],str(site)[8],str(site)[8]),
                condition_list=[Condition(coord=site, species='CH2')],
                action_list=[Action(coord=site, species='CH3')])

for site in [s, t]:
    kmc_model.add_process(name='CH3_%s_dis' % str(site)[8],
                rate_constant='(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_%s,GibbsAds_CH2_%s+GibbsAds_H_t)-GibbsAds_CH3_%s,0)*eV)' %(str(site)[8],str(site)[8],str(site)[8]),
                condition_list=[Condition(coord=site, species='CH3')],
                action_list=[Action(coord=site, species='CH2')])

#H-CH3 reactions
for site in [s, t]:
    kmc_model.add_process(name='H_CH3_%s_react' % str(site)[8],
                rate_constant='H_cov/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_%s,GibbsGas_CH4gas)-(GibbsAds_CH3_%s+GibbsAds_H_t),0)*eV)' %(str(site)[8],str(site)[8]),
                tof_count={'CH4_formation':1},
                condition_list=[Condition(coord=site, species='CH3')],
                action_list=[Action(coord=site, species='empty')])

for site in [s, t]:
    kmc_model.add_process(name='CH4_%s_ads' % str(site)[8],
                rate_constant='(1-H_cov)/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_%s,GibbsAds_CH3_%s+GibbsAds_H_t)-GibbsGas_CH4gas,0)*eV)' %(str(site)[8],str(site)[8]),
                tof_count={'CH4_formation':-1},
                condition_list=[Condition(coord=site, species='empty')],
                action_list=[Action(coord=site, species='CH3')])

#H-OH reaction
for site in [s, t]:
    kmc_model.add_process(name='H_OH_%s_react' % str(site)[8],
                rate_constant='H_cov*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_%s,GibbsGas_H2Ogas)-(GibbsAds_OH_%s+GibbsAds_H_t),0)*eV)' %(str(site)[8],str(site)[8]),
                tof_count={'H2O_formation':1},
                condition_list=[Condition(coord=site, species='OH')],
                action_list=[Action(coord=site, species='empty')])

for site in [s, t]:
    kmc_model.add_process(name='H2O_%s_ads' % str(site)[8],
                rate_constant='(1-H_cov)*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_%s,GibbsAds_OH_%s+GibbsAds_H_t)-GibbsGas_H2Ogas,0)*eV)' %(str(site)[8],str(site)[8]),
                tof_count={'H2O_formation':-1},
                condition_list=[Condition(coord=site, species='empty')],
                action_list=[Action(coord=site, species='OH')])

#OH-OH reaction
for (site1,name1), (site2,name2) in [((s,'s'), (s_S,'s_S')), ((s,'s'), (s_N,'s_N')), ((t,'t'), (t_S,'t_S')), ((t,'t'), (t_N,'t_N'))]:
    kmc_model.add_process(name='OH_OH_%s_react_%s' % (name1,name2),
                rate_constant='1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_%s,GibbsAds_O_%s+GibbsGas_H2Ogas)-(2*GibbsAds_OH_%s),0)*eV)' %(str(site1)[8],str(site1)[8],str(site1)[8]),
                tof_count={'H2O_formation':1},
                condition_list=[Condition(coord=site1, species='OH'),
                                Condition(coord=site2, species='OH')],
                action_list=[Action(coord=site1, species='O'),
                             Action(coord=site2, species='empty')])

for (site1,name1), (site2,name2) in [((s,'s'), (t,'t')), ((s,'s'), (t_N,'t_N')), ((t,'t'), (s,'s')), ((t_N,'t_N'), (s,'s'))]:
    kmc_model.add_process(name='OH_OH_%s_react_%s' % (name1,name2),
                rate_constant='1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__%s,GibbsAds_O_%s+GibbsGas_H2Ogas)-(GibbsAds_OH_%s+GibbsAds_OH_%s),0)*eV)' %(str(site1)[8],str(site1)[8],str(site1)[8],str(site2)[8]),
                tof_count={'H2O_formation':1},
                condition_list=[Condition(coord=site1, species='OH'),
                                Condition(coord=site2, species='OH')],
                action_list=[Action(coord=site1, species='O'),
                             Action(coord=site2, species='empty')])

for (site1,name1), (site2,name2) in [((s,'s'), (s_S,'s_S')), ((s,'s'), (s_N,'s_N')), ((t,'t'), (t_S,'t_S')), ((t,'t'), (t_N,'t_N'))]:
    kmc_model.add_process(name='H2O_O_%s_react_%s' % (name1,name2),
                rate_constant='1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_%s,2*GibbsAds_OH_%s)-(GibbsAds_O_%s+GibbsGas_H2Ogas),0)*eV)' %(str(site1)[8],str(site1)[8],str(site1)[8]),
                tof_count={'H2O_formation':-1},
                condition_list=[Condition(coord=site1, species='O'),
                                Condition(coord=site2, species='empty')],
                action_list=[Action(coord=site1, species='OH'),
                             Action(coord=site2, species='OH')])

for (site1,name1), (site2,name2) in [((s,'s'), (t,'t')), ((s,'s'), (t_N,'t_N')), ((t,'t'), (s,'s')), ((t_N,'t_N'), (s,'s'))]:
    kmc_model.add_process(name='H2O_O_%s_react_%s' % (name1,name2),
                rate_constant='1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__%s,(GibbsAds_OH_%s+GibbsAds_OH_%s))-(GibbsAds_O_%s+GibbsGas_H2Ogas),0)*eV)' %(str(site1)[8],str(site1)[8],str(site2)[8],str(site1)[8]),
                tof_count={'H2O_formation':-1},
                condition_list=[Condition(coord=site1, species='O'),
                                Condition(coord=site2, species='empty')],
                action_list=[Action(coord=site1, species='OH'),
                             Action(coord=site2, species='OH')])

#O-H reaction
for site in [s, t]:
    kmc_model.add_process(name='H_O_%s_react' % str(site)[8],
                rate_constant='H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_%s,GibbsAds_OH_%s)-(GibbsAds_O_%s+GibbsAds_H_t),0)*eV)' %(str(site)[8],str(site)[8],str(site)[8]),
                condition_list=[Condition(coord=site, species='O')],
                action_list=[Action(coord=site, species='OH')])

for site in [s, t]:
    kmc_model.add_process(name='OH_%s_dis' % str(site)[8],
                rate_constant='(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_%s,GibbsAds_O_%s+GibbsAds_H_t)-GibbsAds_OH_%s,0)*eV)' %(str(site)[8],str(site)[8],str(site)[8]),
                condition_list=[Condition(coord=site, species='OH')],
                action_list=[Action(coord=site, species='O')])

#CO, O, OH, CH2, CH3 diffusion
for ads in ['CO', 'O', 'OH', 'CH2', 'CH3']:
    for (site1,name1), (site2,name2) in [((s,'s'), (s_N,'s_N')), ((s_N,'s_N'), (s,'s')), ((t,'t'), (t_S,'t_S')), ((t_S,'t_S'), (t,'t')), ((s,'s'), (t, 't')), ((s,'s'), (t_N, 't_N')), 
                                         ((t, 't'), (s,'s')), ((t_N, 't_N'), (s,'s'))]:
        kmc_model.add_process(name='%s_diff_%s_%s' % (ads,name1,name2),
                    rate_constant='1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_%s_%s-GibbsAds_%s_%s)+E_%s_diff),0)*eV)' % (ads,str(site2)[8],ads,str(site1)[8],ads),
                    condition_list=[Condition(coord=site1, species=ads),
                                    Condition(coord=site2, species='empty')],
                    action_list=[Action(coord=site1, species='empty'),
                                 Action(coord=site2, species=ads)])

#C diffusion f<->f
for ads in ['C']:
    for (site1,name1), (site2,name2) in [((f,'f'), (f_S,'f_S')), ((f_S,'f_S'), (f,'f'))]:
        kmc_model.add_process(name='%s_diff_%s_%s' % (ads,name1,name2),
                    rate_constant='1/(beta*h)*exp(-beta*max(max(GibbsAds_C__f,GibbsAds_C_f)-GibbsAds_C_f,0)*eV)',
                    condition_list=[Condition(coord=site1, species=ads),
                                    Condition(coord=site2, species='empty')],
                    action_list=[Action(coord=site1, species='empty'),
                                 Action(coord=site2, species=ads)])

#C diffusion others
for ads in ['C']:
    for (site1,name1), (site2,name2) in [((s,'s'), (s_N,'s_N')), ((s_N,'s_N'), (s,'s')), ((t,'t'), (t_S,'t_S')), ((t_S,'t_S'), (t,'t')),
                                         ((f,'f'), (s_E,'s_E')), ((f,'f'), (t,'t')), ((f,'f'), (t_N,'t_N')), ((s_E,'s_E'), (f,'f')), ((s,'s'), (t, 't')), ((s,'s'), (t_N, 't_N')),
                                         ((t, 't'), (s,'s')), ((t_N, 't_N'), (s,'s')), ((t,'t'), (f,'f')), ((t_N,'t_N'), (f,'f'))]:
        kmc_model.add_process(name='%s_diff_%s_%s' % (ads,name1,name2),
                    rate_constant='1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_%s_%s-GibbsAds_%s_%s)+E_%s_diff),0)*eV)' % (ads,str(site2)[8],ads,str(site1)[8],ads),
                    condition_list=[Condition(coord=site1, species=ads),
                                    Condition(coord=site2, species='empty')],
                    action_list=[Action(coord=site1, species='empty'),
                                 Action(coord=site2, species=ads)])

#CH diffusion f<->t
for ads in ['CH']:
    for (site1,name1), (site2,name2) in [((f,'f'), (t,'t')), ((f,'f'), (t_N,'t_N')), ((t,'t'), (f,'f')), ((t_N,'t_N'), (f,'f'))]:
        kmc_model.add_process(name='%s_diff_%s_%s' % (ads,name1,name2),
                    rate_constant='1/(beta*h)*exp(-beta*max(max(GibbsAds_CH__t,GibbsAds_%s_%s)-GibbsAds_%s_%s,0)*eV)' % (ads,str(site2)[8],ads,str(site1)[8]),
                    condition_list=[Condition(coord=site1, species=ads),
                                    Condition(coord=site2, species='empty')],
                    action_list=[Action(coord=site1, species='empty'),
                                 Action(coord=site2, species=ads)])

#CH diffusion others
for ads in ['CH']:
    for (site1,name1), (site2,name2) in [((f,'f'), (f_S,'f_S')), ((f_S,'f_S'), (f,'f')), ((s,'s'), (s_N,'s_N')), ((s_N,'s_N'), (s,'s')), ((t,'t'), (t_S,'t_S')), ((t_S,'t_S'), (t,'t')),
                                         ((f,'f'), (s_E,'s_E')), ((s_E,'s_E'), (f,'f')), ((s,'s'), (t, 't')), ((s,'s'), (t_N, 't_N')),
                                         ((t, 't'), (s,'s')), ((t_N, 't_N'), (s,'s'))]:
        kmc_model.add_process(name='%s_diff_%s_%s' % (ads,name1,name2),
                    rate_constant='1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_%s_%s-GibbsAds_%s_%s)+E_%s_diff),0)*eV)' % (ads,str(site2)[8],ads,str(site1)[8],ads),
                    condition_list=[Condition(coord=site1, species=ads),
                                    Condition(coord=site2, species='empty')],
                    action_list=[Action(coord=site1, species='empty'),
                                 Action(coord=site2, species=ads)])

kmc_model.filename = 'Methanation_JCP2017.xml'
kmc_model.save_model()





