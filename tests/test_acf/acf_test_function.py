#!/usr/bin/env python

import os
import filecmp

def test_build_model(indexOfBackendToTest='all'):
    #indexOfBackendToTest is intended to be an integer. However, 'all' will test all.
    import os
    import sys
    import kmos.cli
    import time
    import pprint
    import filecmp

    old_path = os.path.abspath(os.getcwd())

    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    possible_backends_list = ['local_smart','lat_int','otf'] 
    if str(indexOfBackendToTest).lower() == 'all':
        backends_list = possible_backends_list
    else:
        backends_list = [ possible_backends_list[indexOfBackendToTest] ] #Still need to put it in a list of one item since below will iterate over the list.
    for backend in backends_list:
        export_dir = '_tmp_export_' + backend + ''
        kmos.cli.main('export 2d_grid.xml '+export_dir+' -o --acf -b ' + backend + '')
        os.chdir('..')
        sys.path.insert(0, os.path.abspath('.'))
        import kmos.run
        import kmos.run.acf as acf
        
        if kmos.run.settings is None:
            import kmc_settings as settings
            kmos.run.settings = settings

        if kmos.run.lattice is None:
            from kmc_model import base, lattice, proclist, base_acf, proclist_acf
            import kmc_model
            kmos.run.kmc_model = kmc_model
            kmos.run.base = base
            kmos.run.lattice = lattice
            kmos.run.proclist = proclist
            kmos.run.base_acf = base_acf
            kmos.run.proclist_acf = proclist_acf

        with kmos.run.KMC_Model(print_rates=False, banner=False) as model:
            print("Model compilation successfull")
            nr_of_steps = 100
            trace_species = 'ion'

            acf.initialize_msd(model,trace_species)
            acf.allocate_trajectory(model,nr_of_steps)

            acf.do_kmc_steps_displacement(model,nr_of_steps,True)
            traj = acf.get_trajectory(model)

        #check if the sources are equal.
        #The ref_src directories were created by copying a 'successful' src directory and renaming it to ref_src.
        for src_filename in ['base_acf', 'proclist_acf']:
            assert filecmp.cmp('src/'+src_filename+'.f90',
                               'ref_src/'+src_filename+'.f90')


        #This if statement is for the case that someone is using the UnitTesterSG module.
        if type(indexOfBackendToTest) == int: #note that this case (intended for UnitTesterSG) will give a return without doing the loop multiple times.
            # Clean-up action
            os.chdir('..')
            return traj #
        elif str(indexOfBackendToTest).lower() == 'all': #Note that this case will complete a full loop several times.
            ## Regenerate reference trajectory files -- commented out
            ## Uncomment out to make new output result files. 
            # with open('ref_traj_' + backend + '.log', 'w') as outfile:
                # outfile.write(pprint.pformat(list(traj.flatten())))

            with open('test_traj_' + backend + '.log', 'w') as outfile:
                #outfile.write(pprint.pformat(traj))
                outfile.write(pprint.pformat(list(traj.flatten())))

            # check if both trajectories are equal
            print(backend)
            assert filecmp.cmp(
                'test_traj_' + backend + '.log',
                'ref_traj_' + backend + '.log',
            )

            # Clean-up action
            os.chdir('..')

            #kmos.run.lattice = None
            #kmos.run.settings = None

    os.chdir(old_path)

if __name__ == '__main__':
    test_build_model()
