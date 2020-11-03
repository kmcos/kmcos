#!/usr/bin/env python

import os
import filecmp
import numpy as np

def test_build_model(indexOfBackendToTest='all'):
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
        export_dir = '_tmp_export_'+backend+''
        kmos.cli.main('export AB_model.ini '+export_dir+' -o -b'+backend+'')
        #print("line 26"); sys.exit()

        os.chdir('..')
        sys.path.insert(0, os.path.abspath('.'))
        
        import kmos.run
    
        if kmos.run.settings is None:
            import kmc_settings as settings
            kmos.run.settings = settings

        if kmos.run.lattice is None:
            from kmc_model import base, lattice, proclist
            kmos.run.base = base
            kmos.run.lattice = lattice
            kmos.run.proclist = proclist

        procs_sites = []
        with kmos.run.KMC_Model(print_rates=False, banner=False) as model:
            print("Model compilation successfull")
            for i in range(10000):
                proc, site = model.get_next_kmc_step()
                procs_sites.append((proc.real, site.real))
                model.run_proc_nr(proc, site)
        
        import time;  time.sleep(0.5) #Need to add a small delay, because otherwise pytest can have problems with the next test.

        if type(indexOfBackendToTest) == type(1):#check if it's an integer. If it is, return what UnitTesterSG would be looking for.
            # Clean-up action
            os.chdir('..')
            return np.mean(np.array(procs_sites), axis=0)
        elif str(indexOfBackendToTest).lower() == 'all': #else do the 'old' way of testing.
            ## Regenerate reference trajectory files -- comment out
            ## Uncomment to make new reference trajectories.
            # with open('ref_procs_sites_'+backend+'.log', 'w') as outfile:
                # outfile.write(pprint.pformat(procs_sites))

            with open('test_procs_sites_'+backend+'.log', 'w') as outfile:
                outfile.write(pprint.pformat(procs_sites))

            # check if the trajectory is the same as before
            assert filecmp.cmp(
                'test_procs_sites_'+backend+'.log',
                'ref_procs_sites_'+backend+'.log',
            ), 'Trajectories differ for backend '+backend+''

            # Clean-up action
            os.chdir('..')

            kmos.run.lattice = None
            kmos.run.settings = None

    os.chdir(old_path)

if __name__ == '__main__':
    test_build_model()
