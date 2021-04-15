#!/usr/bin/env python
"""This is a program to carry out a temperature programmed desorption simulation
using the KMOS KMC package as a backend.

Author:         Jonathan E. Sutton
Affiliation:    Surface Chemistry & Catalysis Group
                Chemical Sciences Division
                Oak Ridge National Laboratory
First Version:  2015/08/10
Last Updated:   2021/04/09 by A. Savara

#When applied to the example MySecondTPR_local_smart, as 
#of April 9th 2021 the model simply takes some steps and then jumps in temperature.
#This is currently just an example of syntax etc. and not a useful TPR example

"""

from kmcos.run import KMC_Model, set_rate_constants
import sys
import numpy as np
import kmc_settings
import tpd_settings

#   Specify various input parameters (initial temperature, run time, etc.).
#   This 'includes' the following python file's contents. This file contains
#   various parameters related to actually running the simulation.
exec(compile(open('tpd_settings.py', "rb").read(), 'tpd_settings.py', 'exec'))

#   Function to import mechanism from KMCOS run file
def import_model(sim_size, random_seed):
    model = KMC_Model(print_rates=False, banner=False, size=sim_size,
        random_seed=random_seed)
    return model

#   Lattice initialization function that takes the KMCOS model and loads the
#   corresponding previously generated initial lattice configuration.
def init_lattice(model, lattice):

    try:
        model.load_config(lattice)
    except:
        sys.stdout.write('Lattice configuration file ' + lattice + '.npy does' +
            ' not exist or is not consistent with the current model.' +
            ' Aborting.\n')
        raise SystemExit

#   Function to write parameters
def write_model_parameters():
    with open(kmc_settings.model_name + '_tpd_settings_save.py', 'w') as params:
        params.write('T_initial = ' + str(T_initial) + '\n')
        params.write('T_final = ' + str(T_final) + '\n')
        params.write('T_ramp = ' + str(T_ramp) + '\n')
        params.write('sim_size = ' + str(sim_size) + '\n')
        params.write('max_time_step = ' + str(max_time_step) + '\n')
        params.write('random_seed = ' + str(random_seed) + '\n')

#   Function to extract the array of current rates
def get_rates(model):

    nproc = len(kmc_settings.rate_constants)
    rates = np.zeros(nproc)

    for i in range(nproc):
        rates[i] = model.base.get_rate(i+1)
    return rates

#   Function to get process names
def get_proc_names():
    return sorted(kmc_settings.rate_constants.keys())

#   Function to get process statistics
def get_procstat(model):

    nproc = len(kmc_settings.rate_constants)
    procstat = np.zeros(nproc, dtype=np.int64)

    for i in range(nproc):
        procstat[i] = model.base.get_procstat(i+1)
    return procstat

#   Function to create a pretty-printed string for writing output to a file
def str_pretty_print(data):

    d = np.array(data).flatten()
    str_out = ''
    str_out = '  '.join(['{: 12.8G}'.format(d[i]) for i in
        range(len(d))]) + '\n'
    return str_out

#   Function to switch desorption processes off to assist in equilibrating the
#   surface before starting the temperature ramp.
def switch_des_off(processes):

    for process in processes:
        kmc_settings.parameters['A' + process]['value'] = 0.0
    set_rate_constants(print_rates=False)

#   Function to switch desorption processes on to assist in equilibrating the
#   surface before starting the temperature ramp.
def switch_des_on(processes):

    for process in processes:
        kmc_settings.parameters['A' + process]['value'] = 1.E13
    set_rate_constants(print_rates=False)

def post_mortem(err_code, model):
#   Commented out code lifted from the KMCOS KMC_Model class
#    old, new, found, err_site, steps = err_code
#    err_site = model.nr2site(err_site)
#    if old >= 0:
#        old = sorted(kmc_settings.representations.keys())[old]
#    else:
#        old = 'NULL (%s)' % old
#
#    if new >= 0:
#        new = sorted(kmc_settings.representations.keys())[new]
#    else:
#        new = 'NULL (%s)' % new
#
#    if found >= 0:
#        found = sorted(kmc_settings.representations.keys())[found]
#    else:
#        found = 'NULL (%s)' % found

    nprocess, nsite = model.proclist.get_next_kmc_step()
    process = list(
        sorted(kmc_settings.rate_constants.keys()))[nprocess - 1]
    site = model.nr2site(nsite)
    print('Process = ', process)
    print('Site = ', site)
    print('Species = ', model.base.get_species(nsite))
#    print('=====================================')
#    print('Post-Mortem Error Report')
#    print('=====================================')
#    print('  KMCOS ran %s steps and the next process is "%s"' %
#            (steps, process))
#    print('  on site %s,  however this causes oops' % site)
#    print('  on site %s because it trys to' % err_site)
#    print('  replace "%s" by "%s" but it will find "%s".' %
#          (old, new, found))
#    print('  Go fish!')

def main():

    #   TODO: need to collect output for coverage, reaction rates, etc. as a
    #   function of temperature/time. Then we need to output it and/or plot it
    #   with matplotlib.

    #   Import KMCOS model
    sys.stdout.write("Importing model\n")
    model = import_model(sim_size, random_seed)

    #   Initialize lattice with all methanol and equilibrate it
    sys.stdout.write("Equilibrating initial lattice\n")
    #TODO: Make below "optional" since it loads in a lattice.
    #init_lattice(model, kmc_settings.model_name + '_initial_lattice')
    kmc_settings.parameters['T']['value'] = T_initial
#    switch_des_off(des_processes)   #Turn desorption off
#    model.do_steps(n=equil_steps)   #Run equilibration
#    switch_des_on(des_processes)    #Turn desorption on
#    model.base.set_kmc_time(0.0)    #Reset clock to 0

    #   Specify output files
    integ_rate_filename = kmc_settings.model_name + '_integ_rates.txt'
    rate_filename = kmc_settings.model_name + '_rates.txt'
    procstat_filename = kmc_settings.model_name + '_procstat.txt'
    cov_filename = kmc_settings.model_name + '_cov.txt'

    #   Save input parameters
    write_model_parameters()

    #   Get initial occupations, rates, etc.
    atoms = model.get_atoms()

    #   Open output files
    integ_rate_file = open(integ_rate_filename, 'w')
    rate_file = open(rate_filename, 'w')
    procstat_file = open(procstat_filename, 'w')
    cov_file = open(cov_filename, 'w')

    #   Write file headers
    tof_header = 'Time [s]   Temperature [K]  ' + model.get_tof_header() + '\n'
    integ_rate_file.write(tof_header)
    rate_file.write(tof_header)
    proc_names_str = '  '.join(get_proc_names()) + '\n'
    procstat_header = 'Time [s]   Temperature [K]  ' + proc_names_str
    procstat_file.write(procstat_header)
    cov_header = 'Time [s]   Temperature [K]  ' + model.get_occupation_header() + '\n'
    cov_file.write(cov_header)

    #   TPD loop
    sys.stdout.write('Starting TPD ramp\n')
    kmc_time = model.base.get_kmc_time()
    T = T_initial
    kmc_settings.parameters['T']['value'] = T
    set_rate_constants(print_rates=False)
    while T < T_final:    #FIXME: add other checks for zero coverage, etc.
        print("line 193, T is ", T)
        #   Execute steps
        sys.stdout.write('T = ' + str(T) + ' K, time = ' + str(kmc_time) + ' s\n')
        model.do_steps(n=100)
        err_code = (42, 46,  0,       2221,     168321) #Taken from crashed simulation
        post_mortem(err_code, model)
        #raise SystemExit    #Bail out so we don't keep simulating -- comment out to keep going

        #   Update global KMC time, temperature, and rates
        kmc_time_new = model.base.get_kmc_time()
        T = T_initial + T_ramp * kmc_time_new
        kmc_time = kmc_time_new
        kmc_settings.parameters['T']['value'] = T
        set_rate_constants(print_rates=False)
        print("line 207, T is ", T)
        #   For all steps, write output to disk
        atoms = model.get_atoms()
        integ_rate_file.write(' {: 12.8G}  {: 12.8G}  '.format(kmc_time, T))
        integ_rate_file.write(str_pretty_print(atoms.tof_integ))
        rate_file.write(' {: 12.8G}  {: 12.8G}  '.format(kmc_time, T))
        rate_file.write(str_pretty_print(atoms.tof_data))
        procstat_file.write(' {: 12.8G}  {: 12.8G}  '.format(kmc_time, T))
        procstat_file.write(str_pretty_print(get_procstat(model)))
        cov_file.write(' {: 12.8G}  {: 12.8G}  '.format(kmc_time, T))
        cov_file.write(str_pretty_print(atoms.occupation))
        model.base.set_kmc_time(kmc_time)   #Make sure we don't reset the clock

    #   Close output files
    integ_rate_file.close()
    rate_file.close()
    procstat_file.close()
    cov_file.close()

    #   Deallocate model
    model.deallocate()
    sys.stdout.write("Model deallocated\n")

if __name__ == "__main__":
    main()
