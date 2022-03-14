#!/usr/bin/env python3
"""
A front-end module to run a compiled kMC model. The actual model is
imported in kmc_model.so and all parameters are stored in kmc_settings.py.

The model can be used directly like so::

    from kmcos.model import KMC_Model
    model = KMC_Model()

    model.parameters.T = 500
    model.do_steps(100000)
    model.view()

which, of course can also be part of a python script.

The model can also be run in a different process using the
multiprocessing module. This mode is designed for use with
a GUI so that the CPU intensive kMC integration can run at
full throttle without impeding the front-end. Interaction with
the model happens through Queues.
"""


#    Copyright 2009-2013 Max J. Hoffmann (mjhoffmann@gmail.com)
#    This file is part of kmcos.
#
#    kmcos is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    kmcos is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with kmcos.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ['base', 'lattice', 'proclist', 'KMC_Model']

from ase.atoms import Atoms
from copy import deepcopy
from fnmatch import fnmatch
from kmcos import evaluate_rate_expression
from kmcos import evaluate_param_expression
from kmcos.utils import OrderedDict
import kmcos.run.acf
import kmcos.utils.progressbar
try:
    import kmcos.run.png
except:
    # quickly create a mock-class
    # keeping this here is important for kmcos.run autodocs to build
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)
    kmcos = Struct()
    kmcos.run = Struct()
    kmcos.run.png = None

from math import log
try:
    import kmcos.run.png
    # keeping this here is important for kmcos.run autodocs to build
except:
   # quickly create a mock-class
   class Struct:
       def __init__(self, **entries):
           self.__dict__.update(entries)
   kmcos = Struct()
   kmcos.run = Struct()
   kmcos.run.png = None
from multiprocessing import Process
import numpy as np
import os
import random
import sys
try:
    from kmc_model import base, lattice, proclist
    import kmc_model
except Exception as e:
    base = lattice = proclist = None
    print("""Error: %s
    Could not find the kmc module. The kmc implements the actual
    kmc model. This can be created from a kmcos xml file using
    kmcos export <xml-file>
    Hint: are you in a directory containing a compiled kMC model?\n\n
    """ % e)

try:
    from kmc_model import proclist_constants
except:
    proclist_constants = None

try:
    from kmc_model import proclist_pars
except:
    proclist_pars = None

try:
    from kmc_model import base_acf, proclist_acf
except:
    base_acf = proclist_acf = None

try:
    import kmc_settings as settings
except Exception as e:
    settings = None
    print("""Error %s
    Could import settings file
    The kmc_settings.py contains all changeable model parameters
    and descriptions for the representation on screen.
    Hint: are you in a directory containing a compiled kMC model?
    """ % e)

try:
    xrange
except NameError:
    xrange = range
    
INTERACTIVE = hasattr(sys, 'ps1') or hasattr(sys, 'ipcompleter')
INTERACTIVE = True  # Turn it off for now because it doesn work reliably

class ProclistProxy(object):

    def __dir__(selftr):
        return list(set(dir(proclist) +
                        dir(proclist_constants) +
                        dir(proclist_pars)))

    def __getattr__(self, attr):
        if attr in dir(proclist):
            return eval('proclist.%s' % attr)
        elif attr in dir(proclist_constants):
            return eval('proclist_constants.%s' % attr)
        elif attr in dir(proclist_pars):
            return eval('proclist_pars.%s' % attr)
        else:
            raise AttributeError('%s not found' % attr)

class KMC_Model(Process):
    """API Front-end to initialize and run a kMC model using python bindings.
    Depending on the constructor call the model can be run either via directory
    calls or in a separate processes access via multiprocessing.Queues.
    Only one model instance can exist simultaneously per process."""

    def __init__(self, image_queue=None,
                       parameter_queue=None,
                       signal_queue=None,
                       size=None, system_name='kmc_model',
                       banner=True,
                       print_rates=False,
                       autosend=True,
                       steps_per_frame=50000,
                       random_seed=None,
                       cache_file=None,
                       buffer_parameter=None,
                       threshold_parameter=None,
                       sampling_steps=None,
                       execution_steps=None,
                       save_limit=None):

        # initialize multiprocessing.Process hooks
        super(KMC_Model, self).__init__()

        # setup queues for viewer
        self.image_queue = image_queue
        self.parameter_queue = parameter_queue
        self.signal_queue = signal_queue
        self.autosend = autosend

        # initalize instance settings
        self.system_name = system_name
        self.banner = banner
        self.print_rates = print_rates
        self.parameters = Model_Parameters(self.print_rates)
        if proclist_pars is None:
            self.rate_constants = Model_Rate_Constants()
        else:
            self.rate_constants = Model_Rate_Constants_OTF()

        # check if the model has been compiled using the temporal acceleration
        #scheme
        try:
            settings.buffer_parameter
        except:
            self.can_accelerate = False
        else:
            self.can_accelerate = True

        # initialize parameters for the temporal acceleration scheme
        if self.can_accelerate:
            if buffer_parameter is not None:
                settings.buffer_parameter = buffer_parameter
                print('buffer_parameter set to: ', settings.buffer_parameter)
            if threshold_parameter is not None:
                settings.threshold_parameter = threshold_parameter
                print('threshold_parameter set to: ', settings.threshold_parameter)
            if sampling_steps is not None:
                settings.sampling_steps = sampling_steps
                print('sampling_steps set to: ', settings.sampling_steps)
            if execution_steps is not None:
                settings.execution_steps = execution_steps
                print('execution_steps set to: ', settings.execution_steps)
            if save_limit is not None:
                settings.save_limit = save_limit
                print('save_limit set to: ', settings.save_limit)

        if random_seed is not None:
            settings.random_seed = random_seed

        if size is None:
            size = settings.simulation_size
        if isinstance(size, int):
            self.size = np.array([size] * int(lattice.model_dimension))
        elif isinstance(size, (tuple, list)):
            if not len(size) == lattice.model_dimension:
                raise UserWarning(('You requested a size %s '
                                   '(i. e. %s dimensions),\n '
                                   'but the compiled model'
                                   'has %s dimensions!')
                                   % (list(size),
                                      len(size),
                                      lattice.model_dimension))
            self.size = np.array(size)

        self.steps_per_frame = steps_per_frame
        self.cache_file = cache_file

        # bind Fortran submodules
        self.base = base
        self.lattice = lattice
        self.proclist = ProclistProxy()
        self.settings = settings
        if base_acf is not None:
            self.base_acf = kmc_model.base_acf
        if proclist_acf is not None:
            self.proclist_acf = kmc_model.proclist_acf

        if hasattr(self.base, 'null_species'):
            self.null_species = self.base.null_species
        elif hasattr(self.base, 'get_null_species'):
            self.null_species = self.base.get_null_species()
        else:
            self.null_species = -1

        self.proclist.seed = np.array(getattr(self.settings, 'random_seed', 1))
        self.reset()

        if hasattr(settings, 'setup_model'):
            try:
                import types #https://stackoverflow.com/questions/37455426/advantages-of-using-methodtype-in-python
                self.setup_model =  types.MethodType(settings.setup_model,
                                         KMC_Model)
            except ModuleNotFoundError:
                import new
                self.setup_model = new.instancemethod(settings.setup_model,
                                                      self,
                                                      KMC_Model)
            self.setup_model()

    def __enter__(self, *args, **kwargs):
        """__enter/exit__ function for with-statement protocol."""
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """__enter/exit__ function for with-statement protocol."""
        self.deallocate()

    def reset(self):
        self.size = np.array(self.size)
        try:
            if self.can_accelerate:
                proclist.init(self.size,
                    self.system_name,
                    lattice.default_layer,
                    self.settings.random_seed,
                    self.settings.buffer_parameter,
                    self.settings.threshold_parameter,
                    self.settings.execution_steps,
                    self.settings.save_limit,
                    not self.banner)
            else:
                proclist.init(self.size,
                    self.system_name,
                    lattice.default_layer,
                    self.settings.random_seed,
                    not self.banner)
        except:
            # fallback if API
            # does not support random seed.
            if self.can_accelerate:
                proclist.init(self.size,
                    self.system_name,
                    lattice.default_layer,
                    self.settings.buffer_parameter,
                    self.settings.threshold_parameter,
                    self.settings.execution_steps,
                    self.settings.save_limit,
                    not self.banner)
            else:
                proclist.init(self.size,
                    self.system_name,
                    lattice.default_layer,
                    not self.banner)
        self.cell_size = np.dot(np.diag(lattice.system_size), lattice.unit_cell_size)

        # prepare structures for TOF evaluation
        self.tofs = tofs = get_tof_names()
        self.tof_matrix = np.zeros((len(tofs), proclist.nr_of_proc))
        for process, tof_count in sorted(settings.tof_count.items()):
            process_nr = getattr(self.proclist, process.lower())
            for tof, tof_factor in list(tof_count.items()):
                self.tof_matrix[tofs.index(tof), process_nr - 1] += tof_factor

        # prepare procstat
        self.procstat = np.zeros((proclist.nr_of_proc), dtype=np.int64)
         # prepare integ_rates (S.Matera 09/25/2012)
        self.integ_rates = np.zeros((proclist.nr_of_proc, ))
        # prepare integ_counter
        self.integ_counter = np.zeros((proclist.nr_of_proc, ))
        self.time = 0.
        self.steps = 0

        self.species_representation = {}
        for species in sorted(settings.representations):
            if settings.representations[species].strip():
                try:
                    self.species_representation[len(self.species_representation)] \
                    = eval(settings.representations[species])
                except Exception as e:
                    print('Trouble with representation %s'
                           % settings.representations[species])
                    print(e)
                    raise
            else:
                self.species_representation[len(self.species_representation)] = Atoms()

        if hasattr(settings, 'species_tags'):
            self.species_tags = settings.species_tags
        else:
            self.species_tags = None

        if len(settings.lattice_representation):
            if hasattr(settings, 'substrate_layer'):
                self.lattice_representation = eval(
                    settings.lattice_representation)[
                        lattice.substrate_layer]
            else:
                lattice_representation = eval(
                    settings.lattice_representation)
                if len(lattice_representation) > 1:
                    self.lattice_representation = \
                         lattice_representation[self.lattice.default_layer]
                else:
                    self.lattice_representation = lattice_representation[0]
        else:
            self.lattice_representation = Atoms()

        set_rate_constants(settings.parameters, self.print_rates, self.can_accelerate)

        self.base.update_accum_rate()
        # S. matera 09/25/2012
        if hasattr(self.base, 'update_integ_rate'):
            self.base.update_integ_rate()
        if hasattr(self.base, 'update_integ_counter'):
            self.base.update_integ_counter()

        if self.can_accelerate:
            #initialize base.proc_pair_indices
            ppi = settings.proc_pair_indices
            for proc in range(proclist.nr_of_proc):
                self.base.initialize_proc_pair_index(proc+1,ppi[proc])
            #initialize base.reverse_indices
            for proc in range(proclist.nr_of_proc):
                f_index = ppi[proc]
                r_index = ppi.index(-f_index)
                self.base.initialize_reverse_index(proc+1,r_index+1)
            #initialize base.is_diff_proc
            diff = settings.is_diff_proc
            for proc in range(proclist.nr_of_proc):
                self.base.initialize_is_diff_proc(proc+1,diff[proc])
            #initialize base.pair_is_eq: If proc pair is a diffusion
            #process it should be set as equilibrated.
            for n,ppi in enumerate(settings.proc_pair_indices):
                if ppi > 0:
                    is_diff = diff[n]
                    self.base.initialize_pair_is_eq(ppi,is_diff)

        # # for otf backend only
        # print('kmcos.run : Updating proclist_pars!')
        # if hasattr(self.proclist,'recalculate_rates_matrix'):
        #     for key,entry in settings.parameters.items():
        #         # print('kmcos.run key.lower() : %s' % key.lower())
        #         # print('kmcos.run entry[value] : %s' % entry.value)
        #         # print('kmcos.run result : %s' %
        #         #       evaluate_rate_expression(entry['value'],settings.parameters))

        #         # setattr(self.proclist,
        #         #         key.lower(),
        #         #         evaluate_rate_expression(entry['value'],settings.parameters)
        #         #         )
        #     self.proclist.recalculate_rates_matrix()

        # load cached configuration if available
        if self.cache_file is not None:
            if os.path.exists(self.cache_file):
                self.load_config(self.cache_file)

    def __repr__(self):
        """Print short summary of current parameters and rate
        constants. It is advisable to include this at the beginning
        of every generated data file for later reconstruction
        """
        return (repr(self.parameters) + repr(self.rate_constants))

    def inverse(self):
        return (repr(self.parameters) + self.rate_constants.inverse())

    def get_param_header(self):
        """Return the names of field return by
        self.get_atoms().params.
        Useful for the header line of an ASCII output.
        """
        return ' '.join(param_name
                       for param_name in sorted(self.settings.parameters)
            if self.settings.parameters[param_name].get('adjustable', False))
    
    def get_param_value(self,param):
        """Return the evaluated value of a parameter"""
        return evaluate_param_expression(param, settings.parameters)

    def get_occupation_header(self):
        """Return the names of the fields returned by
        self.get_atoms().occupation.
        Useful for the header line of an ASCII output.
        """
        return ' '.join(['%s_%s' % (species, site)
                           for species in sorted(settings.representations)
                           for site in settings.site_names])

    def get_tof_header(self):
        """Return the names of the fields returned by
        self.get_atoms().tof_data.
        Useful for the header line of an ASCII output.
        """
        tofs = []
        for _, value in list(settings.tof_count.items()):
            for name in value:
                if name not in tofs:
                    tofs.append(name)
        tofs.sort()
        return ' '.join(tofs)

    def deallocate(self):
        """Deallocate all arrays that are allocated
        by the Fortran module. This needs to be called
        whenever more than one simulation is started
        from one process.

        Note that the currenty state and history of
        the system is lost after calling this method.

        Note: explicit invocation was chosen over the
        __del__ method because there seems to easy
        portable way to control garbage collection.
        """

        if self.cache_file is not None:
            # create directory if necessary
            dirname = os.path.dirname(self.cache_file)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
            self.dump_config(self.cache_file)

        if bool(base.is_allocated()):
            lattice.deallocate_system()
        else:
            print("Model is not allocated.")
        if base_acf is not None :
            base_acf.deallocate_acf()
            
    def set_buffer_parameter(self, value=1000):
        """
        :param value: The value of the buffer parameter
        determines how many times faster equilibrated reaction 
        steps will be than the non-equilibrated steps after
        scaling.
        It could also be called the target timescale disparity.
        (Default: 1000)
        :type value: int > 1
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        self.settings.buffer_parameter = value
        self.base.set_buffer_parameter(value)

    def get_buffer_parameter(self):
        """
        :return value: See set function.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        return self.base.get_buffer_parameter()

    def set_threshold_parameter(self, value=0.2):
        """
        :param value: A pair of processes are flagged as
        equilibrated if within the last `execution_steps` 
        the absolute value of the number of forward minus
        reverse executions divided by `execution_steps` is
        less than the threshold parameter.
        (Default: 0.2)
        :type value: float > 0
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        self.settings.threshold_parameter = value
        self.base.set_threshold_parameter(value)

    def get_threshold_parameter(self):
        """
        :return value: See set function.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        return self.base.get_threshold_parameter()

    def set_sampling_steps(self, value=1000):
        """
        :param value: The number of steps to sample 
        before scaling the rate constants of equilibrated
        processes.
        Note that everytime a non-equilibrated process is
        executed the counter of sampling steps is reset to 0.
        (Default: 1000)
        :type value: int > 1
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        self.settings.sampling_steps = value

    def get_sampling_steps(self):
        """
        :return value: See set function.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        return self.settings.sampling_steps

    def set_execution_steps(self, value=200):
        """
        :param value: The number of steps to sample during
        the full simulation period before assessing the
        equilibrium of a process. See also `threshold_parameter`.
        This is also the number of steps of either the forward
        or the reverse reaction that must have been executed
        within the current superbasin in order for the scaling 
        of the rate constant to be carried out.
        Note that changing this parameter will lead to the model
        being reset.
        (Default: 200)
        :type value: int > 1
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        self.settings.execution_steps = value
        self.deallocate()
        self.reset()

    def get_execution_steps(self):
        """
        :return value: See set function.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        return self.base.get_execution_steps()

    def set_save_limit(self, value=1000):
        """
        :param value: The number of executions following a target
        execution to save.
        Note that changing this parameter will lead to the model
        being reset.
        (Default: 1000)
        :type value: int > 1
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        self.settings.save_limit = value
        self.deallocate()
        self.reset()

    def get_save_limit(self):
        """
        :return value: See set function.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        return self.base.get_save_limit()

    def print_scaling_factors(self):
        """
        Prints the names of the forward and reverse process in each pair
        along with the scaling factor for that pair.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        for m,i in enumerate(settings.proc_pair_indices):
            if i > 0:
                for n,j in enumerate(settings.proc_pair_indices):
                    if i == -j:
                        f = self.base.get_scaling_factor(i)
                        f_name = sorted(self.settings.rate_constants.keys())[m]
                        r_name = sorted(self.settings.rate_constants.keys())[n]
                        print('%s / %s: %.4e' % (f_name, r_name, f))

    def print_scaling_stats(self):
        """Print the average used and last set (=0 if never set) value of the 
        scaling factor for each process pair in the temporal acceleration 
        scheme.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        for m,i in enumerate(settings.proc_pair_indices):
            if i > 0:
                for n,j in enumerate(settings.proc_pair_indices):
                    if i == -j:
                        f_ave = self.base.get_ave_scaling_factor(i)
                        f_last = self.base.get_last_set_scaling_factor(i)
                        f_name = sorted(self.settings.rate_constants.keys())[m]
                        r_name = sorted(self.settings.rate_constants.keys())[n]
                        print('%s / %s: %.4e, %.4e' % (f_name, r_name, f_ave, f_last))

    def get_scaling_stats(self):
        """Returns the names of the process pairs that the scaling factors refer to, the
        average used value of the scaling factor, and the last set (=0 if never set) 
        value of the scaling factor for each process pair in the temporal acceleration 
        scheme.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        pair_names = []
        ave_sf = []
        last_sf = []
        for m,i in enumerate(settings.proc_pair_indices):
            if i > 0:
                for n,j in enumerate(settings.proc_pair_indices):
                    if i == -j:
                        f_ave = self.base.get_ave_scaling_factor(i)
                        ave_sf.append(f_ave)
                        f_last = self.base.get_last_set_scaling_factor(i)
                        last_sf.append(f_last)
                        f_name = sorted(self.settings.rate_constants.keys())[m]
                        r_name = sorted(self.settings.rate_constants.keys())[n]
                        pair_names.append([f_name,r_name])
        return pair_names, ave_sf, last_sf

    def print_proc_pair_eq(self):
        """Prints the names of the forward and reverse process in each pair
        along with a logical for the pair that is True if the process pair 
        is equilibrated and False if the process pair is non-equilibrated.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        for m,i in enumerate(settings.proc_pair_indices):
            if i > 0:
                for n,j in enumerate(settings.proc_pair_indices):
                    if i == -j:
                        is_eq = self.base.check_proc_eq(m+1)
                        f_name = sorted(self.settings.rate_constants.keys())[m]
                        r_name = sorted(self.settings.rate_constants.keys())[n]
                        print('%s / %s: %s' % (f_name, r_name, is_eq))

    def get_saved_executions(self):
        """Returns a list with names and scaling factors of the processes
        executed after the target process in order of execution.
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        execution_list = []
        for i in range(self.settings.save_limit):
            proc = self.base.get_saved_execution(i+1)
            if proc != 0:
                proc_name = sorted(self.settings.rate_constants.keys())[proc-1]
            else:
                proc_name = ''
            sf = self.base.get_saved_scaling_factor(i+1)
            execution_list.append([proc_name,sf])
        return execution_list

    def set_debug_level(self, value=0):
        """
        Set the debug level in the acceleration scheme. If a value larger than 0 is set, 
        certain variables in base.f90 will be printed. For a value of 1 variables will 
        be printed every time reactions are scaled or unscaled. For a value of 2 
        variables will be printed for every accelerated kmc step.
        Possible values: 0, 1, 2
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        assert (value in [0,1,2,3]), 'Only acceptable values are 0, 1, 2, 3'
        self.base.set_debug_level(value)
        proclist.set_debug_level(value)

    def do_steps(self, n=10000, progress=False):
        """Propagate the model `n` steps.

        :param n: Number of steps to run (Default: 10000)
        :type n: int

        """
        if not progress :
            proclist.do_kmc_steps(n)
        else:
            import kmcos.utils.progressbar

            progress_bar = kmcos.utils.progressbar.ProgressBar()
            for i in range(100):
                proclist.do_kmc_steps(n/100)
                progress_bar.render(i+1)
            progress_bar.clear()

    def do_steps_time(self, t=1.0, n=10000):
     """Propagate the model `t` s.

     :param t: Length of time (s) to run (Default: 1)
     :type t: real

     Returns the number of iterations executed.

     """
     num_iter = proclist.do_kmc_steps_time(t,n)
     return num_iter

    def do_acc_steps(self, n=10000, stats=True, save_exe=False, save_proc=0):
        """Propagate the model `n` steps using the temporal
        acceleration scheme.
        :param n: Number of steps to run (Default: 10000)
        :type n: int
        :param stats: Calculate statistics for the scaling factors
        :type stats: logical
        :param save_exe: Track 'save_limit' number of  executions following the execution of the
        :target process 'save_proc'
        :type save_exe: logical
        :param save_proc: Process to be tracked
        :type save_proc: integer
        """
        assert (self.can_accelerate), 'This model has not been compiled using the acceleration flag -t'
        proclist.do_acc_kmc_steps(n, self.settings.sampling_steps, stats, save_exe, save_proc)

    def run(self):
        """Runs the model indefinitely. To control the
        simulations, model must have been initialized
        with proper Queues."""
        if not base.is_allocated():
            self.reset()
        while True:
            for _ in range(self.steps_per_frame):
                proclist.do_kmc_step()
            if self.autosend and not self.image_queue.full():
                atoms = self.get_atoms()
                # attach other quantities need to plot
                # to the atoms object and let it travel
                # piggy-back through the queue
                atoms.size = self.size
                self.image_queue.put(atoms)
            if not self.signal_queue.empty():
                signal = self.signal_queue.get()
                if signal.upper() == 'STOP':
                    self.deallocate()
                    break
                elif signal.upper() == 'PAUSE':
                    print('starting pause')
                elif signal.upper() == 'RESET_TIME':
                    base.set_kmc_time(0.0)
                elif signal.upper() == 'START':
                    pass
                elif signal.upper() == 'ATOMS':
                    self.image_queue.put(self.get_atoms())
                elif signal.upper() == 'DOUBLE':
                    print('Doubling model size')
                    self.double()
                elif signal.upper() == 'HALVE':
                    print('Halving model size')
                    self.halve()
                elif signal.upper() == 'SWITCH_SURFACE_PROCESSES_OFF':
                    self.switch_surface_processes_off()
                elif signal.upper() == 'SWITCH_SURFACE_PROCESSES_ON':
                    self.switch_surface_processes_on()
                elif signal.upper() == 'TERMINATE':
                    self.deallocate()
                    self.terminate()
                elif signal.upper() == 'JOIN':
                    self.join()
                elif signal.upper() == 'WRITEOUT':
                    atoms = self.get_atoms()
                    step = self.base.get_kmc_step()
                    from ase.io import write
                    filename = '%s_%s.traj' % (self.settings.model_name, step)
                    print('Wrote snapshot to %s' % filename)
                    write(filename, atoms)
                elif signal.upper() == 'ACCUM_RATE_SUMMATION':
                    self.print_accum_rate_summation()
                elif signal.upper() == 'COVERAGE':
                    self.print_coverages()

            if not self.parameter_queue.empty():
                while not self.parameter_queue.empty():
                    parameters = self.parameter_queue.get()
                    settings.parameters.update(parameters)
                set_rate_constants(parameters, self.print_rates, self.can_accelerate)

    def export_movie(self, filename = "", resolution = 150, scale = 20, fps=1, frames = 30, steps = 1e6):
        """Exports a series of atomic view snapshots of model instance to a subdirectory, creating png files
        in the folder_with_movie_images directory and then creates a .webm video file of all the images
        of the images into a video
            'filename' sets the filename for the images in the image directory and the video
            'scale' increases the size of each species in the structure (currently not working as desired)
            'resolution' changes the dpi of the images (currently not working as desired)
            'fps' sets how long each image will stay in the video
            'frames' sets the total video length
            'steps' is the amount of steps the model does between each image
        """

        import os
        import moviepy.video.io.ImageSequenceClip

        if filename == '':
            filename = 'atoms_image'
            video_filename = 'atoms_video.webm'
        else:
            video_filename = filename + '.webm'
        if not os.path.exists('folder_with_movie_images'):
            os.mkdir('folder_with_movie_images')
        image_folder = 'folder_with_movie_images'
        os.chdir(image_folder)
        for i in range(frames):
            self.do_steps(steps)
            self.export_picture(filename = filename + str(i), resolution = resolution, scale = scale)
        os.chdir("..")
        image_files = [os.path.join(image_folder,img) for img in os.listdir(image_folder) if img.endswith(".png")]
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
        clip.write_videofile(video_filename)
        clip.close()


    def peek(self, *args, **kwargs):
        """Visualize the current configuration of the model using ASE ag."""
        tag = kwargs.pop('tag', None)

        ase = import_ase()
        ase.visualize.view(self.get_atoms(tag=tag), *args, **kwargs)

    def show(self):
        return self.peek()

    def view(self, scaleA = None):
        """Start current model in live view mode."""
        from kmcos import view
        view.main(self, scaleA = scaleA)

    def get_atoms(self, geometry=True, tag=None, reset_time_overrun=False):
        """Return an ASE Atoms object with additional
        information such as coverage and Turn-over-frequencies
        attached.

        The additional attributes are:
          - `info` (extra tags assigned to species)
          - `kmc_step`
          - `kmc_time`
          - `occupation`
          - `procstat`
          - `integ_rates`
          - `tof_data`

        `tof_data` contains previously defined TOFs in reaction per seconds per
                   cell sampled since the last call to `get_atoms()`
        `info` can be used to better visualize similar looking molecule during
               post-processing
        `procstat` holds the number of times each process was executed since
                   last `get_atoms()` call.

        :param geometry: Return ASE object of current configuration
                         (Default: True).
        :type geometry: bool

        """

        if geometry:
            kmcos_tags = {}
            ase = import_ase()
            atoms = ase.atoms.Atoms()
            for i in range(lattice.system_size[0]):
                for j in range(lattice.system_size[1]):
                    for k in range(lattice.system_size[2]):
                        for n in range(1, 1 + lattice.spuck):
                            species = lattice.get_species([i, j, k, n])
                            if species == self.null_species:
                                continue
                            if self.species_representation.get(species, ''):
                                # create the ad_atoms
                                ad_atoms = deepcopy(
                                    self.species_representation[species])

                                if tag == 'species':
                                    ad_atoms.set_initial_magnetic_moments([species] * len(ad_atoms))
                                elif tag == 'site':
                                    ad_atoms.set_initial_magnetic_moments([n] * len(ad_atoms))
                                elif tag == 'x':
                                    ad_atoms.set_initial_magnetic_moments([i] * len(ad_atoms))
                                elif tag == 'y':
                                    ad_atoms.set_initial_magnetic_moments([j] * len(ad_atoms))
                                elif tag == 'z':
                                    ad_atoms.set_initial_magnetic_moments([k] * len(ad_atoms))

                                # move to the correct location
                                ad_atoms.translate(
                                    np.dot(
                                        np.array([i, j, k]) +
                                        lattice.site_positions[n - 1],
                                            lattice.unit_cell_size))
                                # add to existing slab
                                atoms += ad_atoms
                                if self.species_tags:
                                    for atom in range(len(atoms)
                                                      - len(ad_atoms),
                                                      len(atoms)):
                                        kmcos_tags[atom] = \
                                        list(self.species_tags.values())[species]

                        if self.lattice_representation:
                            lattice_repr = deepcopy(self.lattice_representation)
                            lattice_repr.translate(np.dot(np.array([i, j, k]),
                                                          lattice.unit_cell_size))
                            atoms += lattice_repr
            atoms.set_cell(self.cell_size)

            # workaround for older ASE < 3.6
            if not hasattr(atoms, 'info'):
                atoms.info = {}

            atoms.info['kmcos_tags'] = kmcos_tags
        else:

            class Expando():
                pass
            atoms = Expando()
        atoms.calc = None
        atoms.kmc_time = base.get_kmc_time()
        atoms.kmc_step = base.get_kmc_step()
        atoms.params = [float(self.settings.parameters.get(param_name)['value'])
                   for param_name in sorted(self.settings.parameters)
        if self.settings.parameters[param_name].get('adjustable', False)]

        # calculate TOF since last call
        atoms.procstat = np.zeros((proclist.nr_of_proc,))
        atoms.occupation = proclist.get_occupation()
        for i in range(proclist.nr_of_proc):
            atoms.procstat[i] = base.get_procstat(i + 1)
        # S. Matera 09/25/2012
        if hasattr(self.base, 'get_integ_rate'):
            atoms.integ_rates = np.zeros((proclist.nr_of_proc,))
            for i in range(proclist.nr_of_proc):
                    atoms.integ_rates[i] = base.get_integ_rate(i + 1)
        # S. Matera 09/25/2012
        if hasattr(self.base, 'get_integ_counter'):
            atoms.integ_counter = np.zeros((proclist.nr_of_proc,))
            for i in range(proclist.nr_of_proc):
                atoms.integ_counter[i] = base.get_integ_counter(i + 1)
        delta_t = (atoms.kmc_time - self.time)
        delta_steps = atoms.kmc_step - self.steps
        atoms.delta_t = delta_t
        size = self.size.prod()
        if delta_steps == 0:
            # if we haven't done any steps, return the last TOF again
            atoms.tof_data = self.tof_data if hasattr(self, 'tof_data') else np.zeros_like(self.tof_matrix[:, 0])
            atoms.tof_integ = self.tof_integ  if hasattr(self, 'tof_integ') else np.zeros_like(self.tof_matrix[:, 0])
        elif delta_t == 0. and atoms.kmc_time > 0 and reset_time_overrun :
            print(
                "Warning: numerical precision too low, to resolve time-steps")
            print('         Will reset kMC time to 0s.')
            base.set_kmc_time(0.0)
            atoms.tof_data = np.zeros_like(self.tof_matrix[:, 0])
            atoms.tof_integ = np.zeros_like(self.tof_matrix[:, 0])

        else:
            atoms.tof_data = np.dot(self.tof_matrix,
                            (atoms.procstat - self.procstat) / delta_t / size)
            # S. Matera 09/25/2012
            if hasattr(self.base, 'get_integ_rate'):
                atoms.tof_integ = np.dot(self.tof_matrix,
                                (atoms.integ_rates - self.integ_rates)
                                / delta_t / size)
            # S. Matera 09/25/2012
            if hasattr(self.base, 'get_integ_counter'):
                atoms.norm_counter = ((atoms.integ_counter - self.integ_counter)
                                      / delta_t / size)

        atoms.delta_t = delta_t

        # update trackers for next call
        self.procstat[:] = atoms.procstat
        # S. Matera 09/25/2012
        if hasattr(self.base, 'get_integ_rate'):
            self.integ_rates[:] = atoms.integ_rates
        # S. Matera 09/25/2012
        if hasattr(self.base, 'get_integ_counter'):
            self.integ_counter[:] = atoms.integ_counter

        self.time = atoms.kmc_time
        self.step = atoms.kmc_step
        self.tof_data = atoms.tof_data
        self.tof_integ = atoms.tof_integ

        return atoms

    def get_std_header(self):
        """Return commented line of field names corresponding to
        values returned in get_std_outdata

        """

        std_header = ('#%s %s %s kmc_time simulated_time kmc_steps\n'
                  % (self.get_param_header(),
                     self.get_tof_header(),
                     self.get_occupation_header()))
        return std_header

    def get_std_sampled_data(self, samples, sample_size, tof_method='integ', output='str', show_progress=False):
        """Sample an average model and return TOFs and coverages
        in a standardized format :

        [parameters] [TOFs] [occupations] kmc_time kmc_step

        Parameter tof_method allows to switch between two different methods for
        evaluating turn-over-frequencies. The default method *procstat* evaluates
        the procstat counter, i.e. simply the number of executed events in the
        simulated time interval. *integ* will evaluate the number of times the
        reaction `could` be evaluated in the simulated time interval
        based on the local configurations and the rate constant.

        Credit for this latter method has to be given to Sebastian Matera for
        the idea and implementation.

        In each case check carefully that the observable is sampled good enough!

        :param samples: Number of batches to average coverages over.
        :type sample: int
        :param sample_size: Number of kMC steps in total.
        :type sample_size: int
        :param tof_method: Method of how to sample TOFs.
                           Possible values are procrates or integ.
                           While procrates only counts the processes actually executed,
                           integ evaluates the configuration to estimate the actual
                           rates. The latter can be several orders more efficient
                           for very slow processes.
                           Differences resulting from the two methods can be used
                           as on estimate for the statistical error in samples.
        :type tof_method: str

        """

        # initialize lists for averages
        occs = []
        tofs = []
        delta_ts = []
        step_ts = []
        t0 = self.base.get_kmc_time()
        step0 = self.base.get_kmc_step()

        if show_progress:
            progress_bar = kmcos.utils.progressbar.ProgressBar()

        # reset sampling starting point
        _ = self.get_atoms(geometry = False, reset_time_overrun = False)

        # sample over trajectory
        for sample in range(samples):
            self.do_steps(sample_size/samples)
            atoms = self.get_atoms(geometry=False, reset_time_overrun=False)
            delta_ts.append(atoms.delta_t)
            step_ts.append(self.base.get_kmc_time_step())

            occs.append(list(atoms.occupation.flatten()))
            if tof_method == 'procrates':
                tofs.append(atoms.tof_data.flatten())
            elif tof_method == 'integ':
                tofs.append(atoms.tof_integ.flatten())
            else:
                raise NotImplementedError('tof_method="{tof_method}" not supported. Can be either procrates or integ.'.format(**locals()))

            if show_progress:
                progress_bar.render(1+int(float(sample)/samples*100), 'Sampling')

        # calculate time averages
        occs_mean = np.average(occs, axis=0, weights=step_ts)
        tof_mean = np.average(tofs, axis=0, weights=delta_ts)
        total_time = self.base.get_kmc_time() - t0
        simulated_time = self.base.get_kmc_time()
        total_steps = self.base.get_kmc_step() - step0

        #return tofs, delta_ts

        # write out averages
        outdata = tuple(atoms.params
                        + list(tof_mean.flatten())
                        + list(occs_mean.flatten())
                        + [total_time,
                           simulated_time,
                           total_steps])
        if output == 'str':
            return ((' '.join(['%.5e'] * len(outdata)) + '\n') % outdata)
        elif output == 'dict':
            header = self.get_std_header()[1:].split()
            return dict(list(zip(header, outdata)))
        else:
            raise UserWarning(
                "Output format {output} not defined. I only know 'str' and 'dict'")

    def double(self):
        """
        Double the size of the model in each direction and initialize
        larger model with current configuration in each copy.
        """

        config = self._get_configuration()
        old_system_size = deepcopy(self.lattice.system_size)

        # initialize new version of model w/ twice the size in each direction
        self.deallocate()
        self.size *= 2
        self.reset()

        # initialize new model w/ copies of current state in each of
        # the new copies
        for x in range(self.lattice.system_size[0]):
            for y in range(self.lattice.system_size[1]):
                for z in range(self.lattice.system_size[2]):
                    xi, yi, zi = np.array([x, y, z]) % old_system_size
                    for n in range(self.lattice.spuck):
                        self.lattice.replace_species(
                            [x, y, z, n + 1],
                            self.lattice.get_species([x, y, z, n + 1]),
                            config[xi, yi, zi, n])
        self._adjust_database()

    def switch_surface_processes_off(self):
        """Set rate constant to zero if process
        has 'diff' or 'react' in the name.

        """
        for i, process_name in enumerate(
                               sorted(
                               self.settings.rate_constants)):
            if 'diff' in process_name or 'react' in process_name:
                self.base.set_rate_const(i + 1, .0)

    def switch_surface_processes_on(self):
        set_rate_constants(settings.parameters, self.print_rates, self.can_accelerate)

    def print_adjustable_parameters(self, match=None, to_stdout=True):
        """Print those methods that are adjustable via the GUI.

        :param pattern: fname pattern to limit the parameters.
        :type pattern: str
        """
        res = ''
        w = 80
        res += (w * '-') + '\n'
        for i, attr in enumerate(sorted(self.settings.parameters)):
            if (match is None or fnmatch(attr, match))\
                and settings.parameters[attr]['adjustable']:
                res += '|{0:^78s}|\n'.format((' %40s = %s'
                      % (attr, settings.parameters[attr]['value'])))
        res += (w * '-') + '\n'
        if to_stdout:
            print(res)
        else:
            return res

    def print_coverages(self, to_stdout=True):
        """Show coverages (per unit cell) for each species
        and site type for current configurations.

        """

        res = ''
        # get atoms
        atoms = self.get_atoms(geometry=False)

        # get occupation
        occupation = atoms.occupation

        # get species names
        species_names = sorted(self.settings.representations.keys())

        # get site_names
        site_names = sorted(self.settings.site_names)

        header_line = ('|' +
                      ('%18s|' % 'site \ species') +
                      '|'.join([('%11s' % sn)
                                for sn in species_names] + ['']))
        res += '%s\n' % (len(header_line) * '-')
        res += '%s\n' % header_line
        res += '%s\n' % (len(header_line) * '-')
        for i in range(self.lattice.spuck):
            site_name = self.settings.site_names[i]
            res += '%s\n' % ('|'
                 + '{0:<18s}|'.format(site_name)
                 + '|'.join([('{0:^11.5f}'.format(x) if x else 11 * ' ')
                             for x in list(occupation[:, i])]
                 + ['']))
        res += '%s\n' % (len(header_line) * '-')
        res += '%s\n' % ('Units: "molecules (or atoms) per unit cell"')
        if to_stdout:
            print(res)
        else:
            return res

    def print_procstat(self, to_stdout=True):
        entries = []
        longest_name = 0
        for i, process_name in enumerate(
                               sorted(
                               self.settings.rate_constants)):
            procstat = self.base.get_procstat(i + 1)
            namelength = len(process_name)
            if namelength > longest_name:
                longest_name = namelength
            entries.append((procstat, process_name))

        entries = sorted(entries, key=lambda x: - x[0])
        nsteps = self.base.get_kmc_step()

        width = longest_name + 30

        res = ''
        printed_steps = 0
        res += ('+' + width * '-' + '+' + '\n')
        res += ('| {0:<%ss}|\n' % (width-1)).format('%9s %12s  %s' % ('rel. contrib.', 'procstat', 'process name'))
        res += ('+' + width * '-' + '+' + '\n')
        for entry in entries:
            procstat, name = entry
            printed_steps += procstat
            if procstat:
                res += ('|{0:<%ss}|\n' % width).format('%9.2f %% %12s     %s' % (100 * float(printed_steps) / nsteps, procstat, name))

        res += ('+' + width * '-' + '+' + '\n')
        res += ('   Total steps %s\n' % nsteps)

        if to_stdout:
            print(res)
        else:
            return res

    def print_state_summary(self, order='-rate', to_stdout=True, show=False, print_parameters=False):
        """Show summary of current model state by showing
            - parameters (external, optional)
            - number of times each elementary process has been executed
            - coverage
            - kmc step and kmc time
            - fire up ASE window with current lattice configuration

        """
        res = ''
        if print_parameters:
            res += 'Parameters\n'
            self.print_adjustable_parameters(to_stdout=False)
        res += 'Rate Constants\n'
        res += self.rate_constants(model=self)
        res += 'Procstat\n'
        res += self.print_procstat(to_stdout=False)
        res += 'Accumulated rates\n'
        res += self.print_accum_rate_summation(order=order, to_stdout=False)
        res += 'Coverages\n'
        res += self.print_coverages(to_stdout=False)
        res += 'kMC state\n'
        res += self.print_kmc_state(to_stdout=False)

        if to_stdout:
            print(res)
        else:
            return res

        if show:
            self.show()

    def print_kmc_state(self, to_stdout=True):
        """Shows current kmc step and kmc time.
        """
        kmc_steps = self.base.get_kmc_step()
        kmc_time = self.base.get_kmc_time()
        data_line = '| kmc time {kmc_time:10.5g} | kmc steps {kmc_steps:18d} |\n'.format(**locals())
        res = ('-' * len(data_line)) + '\n'
        res += data_line
        res += ('-' * len(data_line)) + '\n'

        if to_stdout:
            print(res.strip())
        else:
            return res

    def print_accum_rate_summation(self, order='-rate', to_stdout=True):
        """Shows rate individual processes contribute to the total rate

        The optional argument order can be one of: name, rate, rate_constant,
        nrofsites. You precede each keyword with a '-', to show in decreasing
        order.
        Default: '-rate'. Possible values are rate, rate_constant, name, nrofsites .

        """
        accum_rate = 0.
        entries = []
        # collect
        for i, process_name in enumerate(
                               sorted(
                               self.settings.rate_constants)):
            nrofsites = self.base.get_nrofsites(i + 1)
            if nrofsites:
                rate = self.base.get_rate(i + 1)
                prod = nrofsites * rate
                if self.get_backend() in ['otf',]:
                    accum_rate += rate
                else:
                    accum_rate += prod
                entries.append((nrofsites, rate, prod, process_name))

        # reorder
        if order == 'name':
            entries = sorted(entries, key=lambda x: x[3])
        elif order == 'rate':
            entries = sorted(entries, key=lambda x: x[2])
        elif order == 'rate_constant':
            entries = sorted(entries, key=lambda x: x[1])
        elif order == 'nrofsites':
            entries = sorted(entries, key=lambda x: x[0])
        elif order == '-name':
            entries = reversed(sorted(entries, key=lambda x: x[3]))
        elif order == '-rate':
            entries = reversed(sorted(entries, key=lambda x: x[2]))
        elif order == '-rate_constant':
            entries = reversed(sorted(entries, key=lambda x: x[1]))
        elif order == '-nrofsites':
            entries = reversed(sorted(entries, key=lambda x: x[0]))

        # print
        res = ''
        total_contribution = 0
        res += ('+' + 118 * '-' + '+' + '\n')
        if self.get_backend() in ['otf']:
            res += '|{0:<118s}|\n'.format('(cumulative)    nrofsites,  rate         '
                                          '                      [name]')
        else:
            res += '|{0:<118s}|\n'.format('(cumulative)    nrofsites * rate_constant'
                                          '    = rate            [name]')

        res += ('+' + 118 * '-' + '+' + '\n')
        for entry in entries:
            if self.get_backend() in ['otf']:
                total_contribution += float(entry[1])
            else:
                total_contribution += float(entry[2])
            percent = '(%8.4f %%)' % (total_contribution * 100 / accum_rate)
            if self.get_backend() in ['otf']:
                entry = '{0: 12d},  {1: 8.4e} s^-1              [{3:s}]'.format(*entry)
            else:
                entry = '% 12i * % 8.4e s^-1 = %8.4e s^-1 [%s]' % entry
            res += '|{0:<118s}|\n'.format('%s %s' % (percent, entry))

        res += ('+' + 118 * '-' + '+' + '\n')
        res += '|{0:<118s}|\n'.format(('  = total rate = %.8e s^-1'
                                       % accum_rate))
        res += ('+' + 118 * '-' + '+' + '\n')

        if to_stdout:
            print(res)
        else:
            return res
            
    def get_coords(self):
        """
        Config is expected to be a nested array that contains the species's coordinates
            EX: [[[[0]], [[1]], [[1]], [[0]]]]
        Species is exptected to be a dictionary that contains the names of the species
            EX: {"CO" : "carbon"}
        """
        config = self._get_configuration().tolist()
        species = self.species_tags
        coords = []
        for i in range(len(config)):
            for j in range(len(config[0])):
                coords.append([i,j])
        return coords, species
            
    @staticmethod  
    def get_species_coordinates(config, species):
        """
        Gets the species coordinates from a 4d list and appends it into a 2d array that's then returned
        """
        species_coords = []
        for k in range(len(species)):
            species_coords.append([])
            for i in range(len(config)):
                for j in range(len(config[0])):
                    if (config[i][j][0][0] == k):
                        species_coords[k].append([i,j])  
        return species_coords

    @staticmethod 
    def create_configuration_plot(coords, species, plot_settings={}, showFigure=True, directory=''):
        """
        coords is expected to be the results from get_species_coordinates(config, species)
            Ex:
        species is expected to be the results from get_coords(), which is a dictionary that contains the names of the species
            Ex: {"CO" : "carbon"}
        plot_settings is a dictionary that allows for the plot to change given the arguements
            EX:
                "y_label": "test",
                "x_label": "test",
                "legendLabel": "Species",
                "legendExport": False,
                "legend": True,
                "figure_name": "Plot",
                "dpi": 220,
                "speciesName": False
        create_configuration_plot will return the spatial view of the kmc_model and make a graph named 'plottedConfiguration.png,' unless specified by 'figure_name' in plot_settings
        """
        import matplotlib.pyplot as plt
        exportFigure = True #This variable should be moved to an argument or something in plot_settings.
        #First put some defaults in if not already defined.
        if 'x_label' not in plot_settings: plot_settings['x_label'] = ''
        if 'y_label' not in plot_settings: plot_settings['y_label'] = ''
        if 'legendLabels' not in plot_settings: plot_settings['legendLabels'] = ''
        if "legendExport" not in plot_settings: plot_settings['legendExport'] = True
        if "legend" not in plot_settings: plot_settings['legend'] = True
        if 'figure_name' not in plot_settings: plot_settings['figure_name'] = 'plottedConfiguration'
        if 'dpi' not in plot_settings: plot_settings['dpi'] = 220
        if 'speciesName' not in plot_settings: plot_settings['speciesName'] = False
        if 'num_x_ticks' not in plot_settings: plot_settings['num_x_ticks'] = 7
        if 'num_y_ticks' not in plot_settings: plot_settings['num_y_ticks'] = 7
        
        fig0, ax0 = plt.subplots()
        if 'fontdict' in plot_settings: 
            #There are various things that could be added to this fontdict. #https://www.tutorialexample.com/understand-matplotlib-fontdict-a-beginner-guide-matplotlib-tutorial/
            fontdict = plot_settings['fontdict']
            if 'size' in fontdict:
                ax0.tick_params(axis='x', labelsize=fontdict['size'])
                ax0.tick_params(axis='y', labelsize=fontdict['size'])
        else:
            fontdict = None #initializing with the matplotlib default
        ax0.set_xlabel(plot_settings['x_label'], fontdict=fontdict)
        ax0.set_ylabel(plot_settings['y_label'], fontdict=fontdict) #TODO: THis is not yet generalized (will be a function)
        
        for (i, key) in zip(list(range(len(coords))), list(species.keys())): #goes through each species and plots their coordinates
            x, y = list(zip(*coords[i]))
            if plot_settings['legend'] == True:
                    if plot_settings['speciesName'] == False:
                        ax0.scatter(x,y,label="Species "+str(i+1))
                    else:
                        ax0.scatter(x,y,label=key)
            
            if plot_settings['legend'] == True: #creates the configuration's legend
                if 'legendLabel' in plot_settings:
                    ax0.legend(title = plot_settings['legendLabel'], bbox_to_anchor=(1.05,1.0), loc="upper left")
                else:
                    ax0.legend(bbox_to_anchor=(1.05,1.0), loc="upper left")

        if plot_settings['legendExport'] == True: #exports the legend into a separate text file
            with open(plot_settings['figure_name'] + "Legend.txt", 'w') as f:
                for key, value in list(species.items()):
                    f.write('%s\n' % (key))
                    
        if str(plot_settings['num_x_ticks']) != 'auto': #sets the tick locator for the x-axis
            plot_settings['num_x_ticks'] = int(plot_settings['num_x_ticks'])
            from matplotlib.ticker import MaxNLocator
            ax0.xaxis.set_major_locator(MaxNLocator(nbins = plot_settings['num_x_ticks']))
        
        if str(plot_settings['num_y_ticks']) != 'auto': #sets the tick locator for the y-axis
            plot_settings['num_y_ticks'] = int(plot_settings['num_y_ticks'])
            from matplotlib.ticker import MaxNLocator
            ax0.yaxis.set_major_locator(MaxNLocator(nbins = plot_settings['num_y_ticks']))

        if 'x_ticks' in plot_settings: #sets the ticker for the x-axis
            if str(plot_settings['x_ticks']).lower != 'auto':
                ax0.set_xticks(plot_settings['x_ticks'])

        if 'y_ticks' in plot_settings: #sets the ticker for the y-axis
            if str(plot_settings['y_ticks']).lower != 'auto':
                ax0.set_yticks(plot_settings['y_ticks'])

        fig0.tight_layout()
        if exportFigure==True:
            fig0.savefig(directory + plot_settings['figure_name'] + '.png', dpi=plot_settings['dpi'])
        if showFigure==False:
            plt.close(fig0)
        return fig0, ax0

    def export_picture(self, resolution, scale,  filename="", **kwargs):
        """
        Gets the atoms objects of the kmc_model and returns a atomic view of the configuration and make a file named 'atomic_view.png' unless specified by 'filename' in the function's argument
            'filename' sets the filename for the images in the image directory and the video
            'scale' increases the size of each species in the structure (currently not working as desired)
            'resolution' changes the dpi of the images (currently not working as desired)
        """
        atoms = self.get_atoms(reset_time_overrun = False) #here, the self is the KMC_Model object
        kmcos.run.png.MyPNG(atoms, show_unit_cell=False, scale=scale, model=self, **kwargs).write(filename=filename, resolution=resolution)
        return 
        
    def plot_configuration(self, filename = '', resolution = 150, scale = 20, representation = 'spatial', plot_settings = {}):
        """
        representation is an optional argument for spatial and atomic view
        resolution and scale are strictly for the atomic view
            resolution changes the plot's 
        You should specify as 'atomic' to see the atomic view. Leaving representation empty returns spatial view by default.

        plot_settings is a dictionary that allows for the plot to change given the arguements
        EX:
            "y_label": "test",
            "x_label": "test",
            "legendLabel": "Species",
            "legendExport": False,
            "legend": True,
            "figure_name": "Plot",
            "dpi": 220,
            "speciesName": False
        plot_configuration either calls create_configuration_plot to create the spatial representation of the model, or calls export_picture to create the atomic representation of the model
        """        
        if representation == 'atomic':
            if 'show_unit_cell' in plot_settings:
                show_unit_cell = plot_settings['show_unit_cell']
            else:
                show_unit_cell = True
            if 'kwargs' in plot_settings:
                kwargs = plot_settings['kwargs']
            else:
                kwargs = {} #default for kwargs is a blank dictionary
            self.export_picture(resolution = resolution, scale = scale, filename = filename)

        if (representation == 'spatial') or (representation == 'circles'):
            config = self._get_configuration().tolist()
            species = self.species_tags
            species_coordinates = self.get_species_coordinates(config, species)
            self.create_configuration_plot(species_coordinates, species, plot_settings)
            
    def _put(self, site, new_species, reduce=False):
        """
        Works exactly like put, but without updating the database of
        available processes. This is faster for when one does a lot updates
        at once, however one must call _adjust_database afterwards.

        Examples ::

            model._put([0,0,0,model.lattice.lattice_bridge], model.proclist.co])
            # puts a CO molecule at the `bridge` site of the lower left unit cell

            model._put([1,0,0,model.lattice.lattice_bridge], model.proclist.co ])
            # puts a CO molecule at the `bridge` site one to the right

            # ... many more

            model._adjust_database() # Important !

        :param site: Site where to put the new species, i.e. [x, y, z, bridge]
        :type site: list or np.array
        :param new_species: Name of new species.
        :type new_species: str
        :param reduce: Of periodic boundary conditions if site falls out
                       site lattice (Default: False)
        :type reduce: bool

        """
        x, y, z, n = site
        if reduce:
            x, y, z = (x, y, z) % self.lattice.system_size
            site = np.array([x, y, z, n])

        # Error checking
        if not x in range(self.lattice.system_size[0]):
            raise UserWarning('x-coordinate %s seems to fall outside lattice'
                              % x)
        if not y in range(self.lattice.system_size[1]):
            raise UserWarning('y-coordinate %s seems to fall outside lattice'
                              % y)
        if not z in range(self.lattice.system_size[2]):
            raise UserWarning('z-coordinate %s seems to fall outside lattice'
                              % z)
        if not n in range(1, self.lattice.spuck + 1):
            raise UserWarning('n-coordinate %s seems to fall outside lattice'
                              % n)

        old_species = self.lattice.get_species(site)
        self.lattice.replace_species(site, old_species, new_species)

    def put(self, site, new_species, reduce=False):
        """
        Puts new_species at site. The site is given by 4-entry sequence
        like [x, y, z, n], where the first 3 entries define the unit cell
        from 0 to the number of unit cells in the respective direction.
        And `n` specifies the site within the unit cell.

        The database of available processes will be updated automatically.

        Examples ::

            model.put([0,0,0,model.lattice.site], model.proclist.co ])
            # puts a CO molecule at the `bridge` site
            # of the lower left unit cell

        :param site: Site where to put the new species, i.e. [x, y, z, bridge]
        :type site: list or np.array
        :param new_species: Name of new species.
        :type new_species: str
        :param reduce: Of periodic boundary conditions if site falls out site
                       lattice (Default: False)
        :type reduce: bool

        """

        self._put(site, new_species, reduce=reduce)
        self._adjust_database()

    def halve(self):
        """
        Halve the size of the model and initialize each site in the new model
        with a species randomly drawn from the sites that are reduced onto
        one. It is necessary that the simulation size is even.
        """
        if self.settings.simulation_size % 2:
            print("Can only halve system with even size!")
            return

        config = self._get_configuration()

        self.deallocate()
        self.size /= 2
        self.reset()

        X, Y, Z = self.lattice.system_size
        N = self.lattice.spuck
        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    for n in range(N):
                        # collect species
                        # from the 8 sites that are
                        # reduced onto one
                        choices = [config[(x + i * X) % X,
                                         (y + j * Y) % Y,
                                         (z + k * Z) % Z,
                                         n]
                            for i in range(2)
                            for j in range(2)
                            for k in range(2)]

                        # use random.choice
                        # to randomly select one
                        self.lattice.replace_species(
                            [x, y, z, n + 1],
                            self.lattice.get_species([x, y, z, n + 1]),
                            random.choice(choices))
        self._adjust_database()

    def run_proc_nr(self, proc, site):
        if self.base.get_avail_site(proc, site, 2):
            self.proclist.run_proc_nr(proc, site)
            return True
        else:
            print("Process not enabled")
            return False

    def get_next_kmc_step(self):
        proc, site = proclist.get_next_kmc_step()
        return ProcInt(proc), SiteInt(site)

    def get_avail(self, arg):
        """Return available (enabled) processes or sites. If the argument is a sequence it is interpreted as a site (x, y, z, n).
        If it is an integer it is interpreted as a process.
           :param arg: type or process to query
           :type arg: int or [int]

        """

        avail = []
        try:
            arg = list(iter(arg))
            # if is iterable, interpret as site
            site = self.lattice.calculate_lattice2nr([arg[0], arg[1], arg[2], 1])
            for process in range(1, self.proclist.nr_of_proc + 1):
                if self.base.get_avail_site(process, site, 2):
                    avail.append(ProcInt(process, self.settings))

        except Exception as e:
            # if is not iterable, interpret as process
            for x in range(self.lattice.system_size[0]):
                for y in range(self.lattice.system_size[1]):
                    for z in range(self.lattice.system_size[2]):
                        nr = self.lattice.calculate_lattice2nr([x, y, z, 1])
                        if self.base.get_avail_site(arg, nr, 2):
                            avail.append(SiteInt(nr))
        return avail

    def _get_configuration(self):
        """ Return current configuration of model.

           :rtype: np.array
        """
        config = np.zeros(list(self.lattice.system_size) + \
            [int(self.lattice.spuck)], dtype=np.int8)
        for x in range(self.lattice.system_size[0]):
            for y in range(self.lattice.system_size[1]):
                for z in range(self.lattice.system_size[2]):
                    for n in range(self.lattice.spuck):
                        config[x, y, z, n] = \
                            self.lattice.get_species(
                                [x, y, z, n + 1])
        return config

    def _set_configuration(self, config):
        """Set the current lattice configuration.

           Expects a 4-dimensional array, with dimensions [X, Y, Z, N]
           where X, Y, Z are the lattice size and N the number of
           sites in each unit cell.

           :param config: Configuration to set for model. Shape of array
                          has to match with model size.
           :type config: np.array

        """
        X, Y, Z = self.lattice.system_size
        N = self.lattice.spuck
        if not all(config.shape == np.array([X, Y, Z, N])):
            print('Config shape %s does not match' % config.shape)
            print('with model shape %s.' % [X, Y, Z, N])
            return
        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    for n in range(N):
                        species = self.lattice.get_species([x, y, z, n + 1])
                        self.lattice.replace_species([x, y, z, n + 1],
                                                     species,
                                                     config[x, y, z, n])
        self._adjust_database()

    def _adjust_database(self):
        """Set the database of processes currently
        possible according to the current configuration.

        """
        for x in range(self.lattice.system_size[0]):
            for y in range(self.lattice.system_size[1]):
                for z in range(self.lattice.system_size[2]):
                    if self.get_backend() in ['lat_int','otf']:
                        eval('self.proclist.touchup_cell([%i, %i, %i, 0])'
                            % (x, y, z))
                    else:
                        for n in range(self.lattice.spuck):
                            site_name = self.settings.site_names[n].lower()
                            eval('self.proclist.touchup_%s([%i, %i, %i, %i])'
                                % (site_name, x, y, z, n + 1))
        # DEBUGGING, adjust database
        self.base.update_accum_rate()

    def get_backend(self):
        """Return name of backend that model was compiled with.

        :rtype: str

        """
        if hasattr(self.proclist, 'backend'):
            try:
                #NB return ''.join(self.proclist.backend)
                return self.proclist.backend.tostring().decode('utf-8')
            except:
                return '???'
        else:
            return 'local_smart'

    def xml(self):
        """Returns the XML representation that this model was created from.

        :rtype: str
        """
        return settings.xml

    def nr2site(self, n):
        """Accepts a site index and return the site in human readable
        coordinates.

        :param n: Index of site.
        :type n: int
        :rtype: str
        """
        site = list(lattice.calculate_nr2lattice(n))
        site[-1] = settings.site_names[site[-1] - 1]
        return site

    def post_mortem(self, steps=None, propagate=False, err_code=None):
        """Accepts an integer and generates a post-mortem report
        by running that many steps and returning which process
        would be executed next without executing it.

        :param steps: Number of steps to run before exit occurs
                     (Default: None).
        :type steps: int
        :param propagate: Run this one more step, where error occurs
                          (Default: False).
        :type propagate: bool
        :param err_code: Error code generated by backend if
                         project.meta.debug > 0 at compile time.
        :type err_code: str
        """
        if err_code is not None:
            old, new, found, err_site, steps = err_code
            err_site = self.nr2site(err_site)
            if old >= 0:
                old = sorted(settings.representations.keys())[old]
            else:
                old = 'NULL (%s)' % old

            if new >= 0:
                new = sorted(settings.representations.keys())[new]
            else:
                new = 'NULL (%s)' % new

            if found >= 0:
                found = sorted(settings.representations.keys())[found]
            else:
                found = 'NULL (%s)' % found

            self.do_steps(steps)
            nprocess, nsite = proclist.get_next_kmc_step()
            process = list(
                sorted(settings.rate_constants.keys()))[nprocess - 1]
            site = self.nr2site(nsite)
            print('=====================================')
            print('Post-Mortem Error Report')
            print('=====================================')
            print('  kmcos ran %s steps and the next process is "%s"' %
                    (steps, process))
            print('  on site %s,  however this causes oops' % site)
            print('  on site %s because it trys to' % err_site)
            print('  replace "%s" by "%s" but it will find "%s".' %
                  (old, new, found))
            print('  Go fish!')

        else:
            if steps is not None:
                self.do_steps(steps)
            else:
                steps = base.get_kmc_step()
            nprocess, nsite = proclist.get_next_kmc_step()
            process = list(
                sorted(settings.rate_constants.keys()))[nprocess - 1]
            site = self.nr2site(nsite)

            res = "kmcos ran %s steps and next it will execute\n" % steps
            res += "process '%s' on site %s." % (process, site)
            print(res)

            if propagate:
                proclist.run_proc_nr(nprocess, nsite)

    def procstat_pprint(self, match=None):
        """Print an overview view process names along with
        the number of times it has been executed.

        :param match: fname pattern to filter matching parameter name.
        :type match: str

        """

        for i, name in enumerate(sorted(self.settings.rate_constants.keys())):
            if match is None:
                print('%s : %.4e' % (name, self.base.get_procstat(i + 1)))
            else:
                if fnmatch(name, match):
                    print('%s : %.4e' % (name, self.base.get_procstat(i + 1)))

    def procstat_normalized(self, match=None):
        """Print an overview view process names along with
        the number of times it has been executed divided by
        the current rate constant times the kmc time.

        Can help to find those processes which are kinetically
        hindered.

        :param match: fname pattern to filter matching parameter name.
        :type match: str

        """
        kmc_time = self.base.get_kmc_time()

        for i, name in enumerate(sorted(self.settings.rate_constants.keys())):
            if match is None or fnmatch(name, match):
                if kmc_time:
                    print('%s : %.4e' % (name, self.base.get_procstat(i + 1) /
                                             self.lattice.system_size.prod() /
                                             self.base.get_kmc_time() /
                                             self.base.get_rate(i + 1)))
                else:
                    print('%s : %.4e' % (name, 0.))

    def rate_ratios(self, interactive=False):
        ratios = []
        for i, iname in enumerate(
                        sorted(self.settings.rate_constants.keys())):
            for j, jname in enumerate(
                            sorted(self.settings.rate_constants.keys())):
                if i != j:  # i == 1 -> 1., don't need that
                    irate = self.base.get_rate(i + 1)
                    jrate = self.base.get_rate(j + 1)
                    ratios.append(('%s/%s' % (iname, jname), irate / jrate))

        # sort ratios in descending order
        ratios.sort(key=lambda x: - x[1])
        res = ''
        for label, ratio in ratios:
            res += ('%s: %s\n' % (label, ratio))
        if interactive:
            print(res)
        else:
            return res

    def dump_config(self, filename):
        """Use numpy mechanism to store current configuration in a file.

        :param filename: Name of file, to write configuration to.
        :type filename: str

        """
        np.save('%s.npy' % filename, self._get_configuration())

    def load_config(self, filename):
        """Use numpy mechanism to load configuration from a file. User
        must ensure that size of stored configuration is correct.

        :param filename: Name of file, to write configuration to.
        :type filename: str

        """
        x, y, z = self.lattice.system_size
        spuck = self.lattice.spuck
        config = np.load('%s.npy' % filename)

        self._set_configuration(config)
        self._adjust_database()

    def pickle_export_atoms(self, filename = ""):
        # takes atoms object in filename and turns it into a .pkl file
        import pickle
        if filename == "":
            filename = "atoms_export.pkl"
        else:
            if filename[-4:] == '.pkl':
                filename.replace('.pkl', '.pkl')
            else:
                filename = filename + '.pkl'
        filehandler = open(filename, 'wb')
        pickle.dump(self.get_atoms(), filehandler)
        filehandler.close()


class Model_Parameters(object):
    """Holds all user defined parameters of a model in
    concise form. All user defined parameters can be
    accessed and set as attributes, like so ::

        model.parameters.<parameter> = X.Y
    """

    def __init__(self, print_rates=True):
        object.__init__(self)
        self.__dict__.update(settings.parameters)
        self.print_rates = print_rates
        try:
            settings.buffer_parameter
        except:
            self.can_accelerate = False
        else:
            self.can_accelerate = True

    def __setattr__(self, attr, value):
        if not attr in settings.parameters \
           and not attr in ['print_rates','can_accelerate']:
            print("Warning: don't know parameter '%s'." % attr)
        if attr in settings.parameters:
            settings.parameters[attr]['value'] = value
            set_rate_constants(print_rates=self.print_rates, can_accelerate=self.can_accelerate)
        else:
            self.__dict__[attr] = value

    def __repr__(self):
        fixed_parameters = dict((name, param)
                                for name, param
                                in list(settings.parameters.items())
                                if not param['adjustable'])
        res = '# kMC model parameters (%i, fixed %i)\n' \
               % (len(settings.parameters), len(fixed_parameters))
        res += '# --------------------\n'
        for attr in sorted(settings.parameters):
            res += ('# %s = %s' % (attr, settings.parameters[attr]['value']))
            if settings.parameters[attr]['adjustable']:
                res += '  # *\n'
            else:
                res += '\n'
        res += '# --------------------\n'
        if not len(fixed_parameters) == len(settings.parameters):
            res += '# * adjustable parameters\n'
        return res

    def names(self, pattern=None):
        """Return names of parameters that match `pattern'

        :param pattern: fname pattern to filter matching parameter name.
        :type pattern: str

        """
        names = []
        for attr in sorted(settings.parameters):
            if pattern is None or fnmatch(attr, pattern):
                names.append(attr)
        return names

    def __call__(self, match=None, interactive=False):
        """Return parameters that match `pattern'

        :param match: fname pattern to filter matching parameter name.
        :type match: str

        """
        res = ''
        for attr in sorted(settings.parameters):
            if match is None or fnmatch(attr, match):
                res += ('# %s = %s\n'
                      % (attr, settings.parameters[attr]['value']))
        if interactive:
            print(res)
        else:
            return res

class Model_Rate_Constants(object):
    """Holds all rate constants currently associated with the model.
    To inspect the expression and current settings of it you can just
    call it as a function with a (glob) pattern that matches
    the desired processes, e.g. ::

      model.rate_constant('*ads*')

    could print all rate constants for adsorption. Given of course that
    'ads' is part of the process name. The just get the rate constant
    for one specific process you can use ::

      model.rate_constant.by_name("<process name>")

    To set rate constants manually use ::

      model.rate_constants.set("<pattern>", <rate-constant (expr.)>)

    """

    def __repr__(self):
        """Compact representation of all current rate_constants."""
        res = '# kMC rate constants (%i)\n' % len(settings.rate_constants)
        res += '# ------------------\n'
        for i, proc in enumerate(sorted(settings.rate_constants)):
            rate_expr = settings.rate_constants[proc][0]
            rate_const = base.get_rate(i + 1)
            res += '# %s: %s = %.2e s^{-1}\n' % (proc, rate_expr, rate_const)
        res += '# ------------------\n'

        return res

    def __call__(self, pattern=None, interactive=False, model=None):
        """Return rate constants.

        :param pattern: fname pattern to filter matching parameter name.
        :type pattern: str
        :param model: runtime instance of kMC to extract rate constants from (optional)
        :type model: kmcos Model

        """
        res = ''
        for i, proc in enumerate(sorted(settings.rate_constants.keys())):
            if pattern is None or fnmatch(proc, pattern):
                rate_expr = settings.rate_constants[proc][0]
                if model is None:
                    rate_const = evaluate_rate_expression(rate_expr,
                                                          settings.parameters)
                else:
                    rate_const = model.base.get_rate(i+1)
                res += ('# %s: %s = %.2e s^{-1}\n' % (proc, rate_expr,
                                                      rate_const))
        if interactive:
            print(res)
        else:
            return res

    def names(self, pattern=None):
        """Return names of processes that match `pattern`.

        :param pattern: fname pattern to filter matching parameter name.
        :type pattern: str

        """
        names = []
        for i, proc in enumerate(sorted(settings.rate_constants.keys())):
            if pattern is None or fnmatch(proc, pattern):
                names.append(proc)
        return names

    def by_name(self, proc):
        """Return rate constant currently set for `proc`

        :param proc: Name of process.
        :type proc: str
        """
        rate_expr = settings.rate_constants[proc][0]
        return evaluate_rate_expression(rate_expr, settings.parameters)

    def inverse(self, interactive=False):
        """Return inverse list of rate constants.

        """
        res = '# kMC rate constants (%i)\n' % len(settings.rate_constants)
        res += '# ------------------\n'
        for proc in sorted(settings.rate_constants):
            rate_expr = settings.rate_constants[proc][0]
            rate_const = evaluate_rate_expression(rate_expr,
                                                  settings.parameters)
            res += '# %s: %.2e s^{-1} = %s\n' % (proc, rate_const, rate_expr)
        res += '# ------------------\n'
        if interactive:
            print(res)
        else:
            return res

    def set(self, pattern, rate_constant, parameters=None):
        """Set rate constants. Pattern can be a glob pattern,
        and the rate constant will be applied to all processes,
        where the pattern matches. The rate constant can be either
        a number or a rate expression.

        :param pattern: fname pattern that selects the process affected.
        :type pattern: str
        :param rate_constant: Rate constant to be set.
        :type rate_constant: str or float
        :param parameters: List of parameters to be used when
                           evaluating expression.
        :type parameters: list

        """

        if parameters is None:
            parameters = settings.parameters
        if type(rate_constant) is str:
            rate_constant = evaluate_rate_expression(rate_constant,
                                                     parameters)
        try:
            rate_constant = float(rate_constant)
        except:
            raise UserWarning("Could not convert rate constant to float")
        for i, proc in enumerate(sorted(settings.rate_constants.keys())):
            if pattern is None or fnmatch(proc, pattern):
                base.set_rate_const(i + 1, rate_constant)

        #For acceleration scheme
        try:
            settings.buffer_parameter
        except:
            can_accelerate = False
        else:
            can_accelerate = True

        if can_accelerate:
            for i, proc in enumerate(sorted(settings.rate_constants.keys())):
                if pattern is None or fnmatch(proc, pattern):
                    try:
                        base.set_original_rate_const(i + 1, rate_constant)

                    except Exception as e:
                        raise UserWarning(
                            "Could not set original rate %s for process %s!\nException: %s" \
                                % (rate_constant, proc, e))

class Model_Rate_Constants_OTF(Model_Rate_Constants):
    """
    A subclass of Model_Rate_Constants to be used with the
    otf backend
    """
    def __call__(self, pattern=None, interactive=False, **kwargs):
        """ Return rate constants

        Can be called with keyword arguments of the form
        nr_<species>_<flag>, to calculate the rate for
        the appropiate value of the chemical environment
        """
        res = ''
        for i, proc in enumerate(sorted(settings.rate_constants.keys())):
            if pattern is None or fnmatch(proc,pattern):
                res += ('# %s: %.2e s^{-1}\n' % (proc,
                                                 self._rate(proc,**kwargs)))

        if interactive:
            print(res)
        else:
            return res

    def _rate(self,procname,**kwargs):
        nr_vars = ''.join(getattr(proclist_pars,
                                  'byst_{}'.format(procname.lower()))
                          ).split()
        if nr_vars:
            input_array = np.zeros([len(nr_vars)],int)
            for nr_var, value in list(kwargs.items()):
                if nr_var in nr_vars:
                    input_array[nr_vars.index(nr_var)] = int(value)

            return getattr(proclist_pars,
                           'rate_{}'.format(procname.lower()))(input_array)
        else:
            return getattr(proclist_pars,
                           'rate_{}'.format(procname.lower()))()

    def bystanders(self, pattern=None, interactive=True):
        """ Print the bystanders defined for processes"""

        res = ''
        for i, proc in enumerate(sorted(settings.rate_constants.keys())):
            if pattern is None or fnmatch(proc,pattern):
                bysts = ''.join(getattr(proclist_pars,
                                        'byst_{}'.format(proc.lower())))
                res += ('# %s: %s\n' % (proc,
                                        bysts))
        if interactive:
            print(res)
        else:
            return res

class ModelParameter(object):
    """A model parameter to be scanned. If instantiated with only
    one value this parameter will be fixed at this value.

    Use a subclass for specific type of grid.

    :param min: Minimum value for this parameter.
    :type min: float
    :param max: Maximum value for this parameter (Default: min)
    :type max: float
    :param steps: Number of steps between minimum and maximum.
    :type steps: int

    """

    def __init__(self, min, max=None, steps=1, type=None, unit=''):
        self.min = min
        self.max = max if max is not None else min
        self.steps = steps
        self.type = type
        self.unit = unit

    def __repr__(self):
        return ('[%s] min: %s, max: %s, steps: %s'
              % (self.type, self.min, self.max, self.steps))

    def get_grid(self):
        pass

class PressureParameter(ModelParameter):
    """Create a grid of p \in [p_min, p_max] such
    that ln({p}) is a regular grid.

    """

    def __init__(self, *args, **kwargs):
        kwargs['type'] = 'pressure'
        kwargs['unit'] = 'bar'
        super(PressureParameter, self).__init__(*args, **kwargs)

    def get_grid(self):
        from kmcos.utils import p_grid
        return p_grid(self.min, self.max, self.steps)

class TemperatureParameter(ModelParameter):
    """Create a grid of p \in [T_min, T_max] such
    that ({T})**(-1) is a regular grid.

    """

    def __init__(self, *args, **kwargs):
        kwargs['type'] = 'temperature'
        kwargs['unit'] = 'K'
        super(TemperatureParameter, self).__init__(*args, **kwargs)

    def get_grid(self):
        from kmcos.utils import T_grid
        return T_grid(self.min, self.max, self.steps)

class LogParameter(ModelParameter):
    """Create a log grid  between 10^min and 10^max
    (like np.logspace)

    """

    def __init__(self, *args, **kwargs):
        kwargs['type'] = 'log'
        super(LogParameter, self).__init__(*args, **kwargs)

    def get_grid(self):
        return np.logspace(self.min, self.max, self.steps)

class LinearParameter(ModelParameter):
    """Create a regular grid between min and max.

    """

    def __init__(self, *args, **kwargs):
        kwargs['type'] = 'linear'
        super(LinearParameter, self).__init__(*args, **kwargs)

    def get_grid(self):
        return np.linspace(self.min, self.max, self.steps)

class _ModelRunner(type):

    def __new__(cls, name, bases, dct):
        obj = super(_ModelRunner, cls).__new__(cls, name, bases, dct)
        obj.runner_name = name
        obj.parameters = OrderedDict()
        for key, item in list(dct.items()):
            if key == '__module__':
                pass
            elif isinstance(item, ModelParameter):
                obj.parameters[key] = item

        return obj

class ModelRunner(object, metaclass=_ModelRunner):
    """
Setup and initiate many runs in parallel over a regular grid
of parameters. A standard type of script is given below.

To allow execution from multiple hosts connected
to the same filesystem calculated points are blocked
via <classname>.lock. To redo a calculation <classname>.dat
and <classname>.lock should be moved out of the way ::

    from kmcos.run import ModelRunner, PressureParameter, TemperatureParameter

    class ScanKinetics(ModelRunner):
        p_O2gas = PressureParameter(1)
        T = TemperatureParameter(600)
        p_COgas = PressureParameter(min=1, max=10, steps=40)
        # ... other parameters to scan

    ScanKinetics().run(init_steps=1e7, sample_steps=1e7, cores=4)

    """

    def __product(self, *args, **kwds):
        """Manual implementation of itertools.product for
          python <= 2.5 """

        # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
        pools = list(map(tuple, args)) * kwds.get('repeat', 1)
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)

    def __split_seq(self, seq, size):
        """Split a list into n chunks of roughly equal size."""
        newseq = []
        splitsize = 1.0 / size * len(seq)
        for i in range(size):
                newseq.append(seq[int(round(i * splitsize)):
                                  int(round((i + 1) * splitsize))])
        return newseq

    def __touch(self, fname, times=None):
        """Pythonic version of Unix touch.

        :param fname: filename.
        :type fname: str
        :param times: timestamp (Default: None meaning now).
        :type times: datetime timestamp

        """
        fhandle = open(fname, 'a')
        try:
            os.utime(fname, times)
        finally:
            fhandle.close()

    def __run_sublist(self, sublist, init_steps, sample_steps, samples, random_seed=None):
        """
        Run sampling run for a list of parameter-tuples.

        :param init_steps: Steps to run model before sampling (.ie. to reach steady-state).
        :type init_steps: int
        :param sample_steps: Number of steps to sample over.
        :type sample_steps: int
        :param cores: Number of parallel processes to launch.
        :type cores: int
        :param samples: Number of samples. Use more samples if precise coverages are needed.
        :type samples: int

        """
        for i, datapoint in enumerate(sublist):
            #============================
            # DEFINE labels
            #===========================
            lockfile = '%s.lock' % (self.runner_name)
            format_string = '_'.join(['%s'] * (len(self.parameters) + 1))
            arguments = tuple([self.runner_name] + list(datapoint))

            input_line = format_string % arguments

            outfile = os.path.abspath('%s.dat' % (self.runner_name))

            #============================
            # lockfile mechanism
            #===========================
            self.__touch(lockfile)
            fdata = open(lockfile, 'r')
            readlines = [x.strip() for x in fdata.readlines()]
            fdata.close()
            if input_line in readlines:
                continue
            fdata = open(lockfile, 'a')
            fdata.write('%s\n' % input_line)
            fdata.close()

            #============================
            # SETUP Model
            #===========================
            model = KMC_Model(print_rates=False,
                              banner=False,
                              random_seed=random_seed,
                              cache_file='%s_configs/config_%s.pckl'
                                          % (self.runner_name, input_line))
            for name, value in zip(list(self.parameters.keys()), datapoint):
                setattr(model.parameters, name, value)

            #============================
            # EVALUATE model
            #===========================
            model.do_steps(int(init_steps))
            model.get_atoms(geometry=False)
            data = model.get_std_sampled_data(samples=samples,
                                              sample_size=int(sample_steps),
                                              tof_method='integ')

            if not os.path.exists(outfile):
                out = open(outfile, 'a')
                out.write(model.get_std_header())
                out.write(str(model.parameters))
                out.write("""# If one or more parameters change between data lines\n# the set above corresponds to the first line.\n""")
                out.close()
            out = open(outfile, 'a')
            out.write(data)
            out.close()
            model.deallocate()

    def plot(self,
             rcParams=None,
             touchup=None,
             filename=None,
             backend='Agg',
             suffixes=['png', 'pdf', 'eps'],
             variable_parameters=None,
             fig_width_pt=246.0,
             plot_tofs=None,
             plot_occs=None,
             occ_xlabel=None,
             occ_ylabel=None,
             tof_xlabel=None,
             tof_ylabel=None,
             label=None,
             sublabel=None,
             arrhenius=False,
             ):
        """
        Plot the generated data using matplotlib. By default we will try
        to generate publication quality output of the specified TOFs and
        coverages.
        """
        import matplotlib
        matplotlib.use(backend)
        # Suppress backend warning, because we cannot
        # control how often the current method is called from
        # a script and superfluous warning tends to confuse users
        from matplotlib import pyplot as plt

        inches_per_pt = 1.0 / 72.27               # Convert pt to inches
        golden_mean = (np.sqrt(5)-1.0) / 2.0         # Aesthetic ratio
        fig_width = fig_width_pt * inches_per_pt  # width in inches
        fig_height = fig_width * golden_mean       # height in inches
        figsize = [fig_width, fig_height]
        font_size = 10
        tick_font_size = 8
        xlabel_pad = 6
        ylabel_pad = 16

        default_rcParams = {
            'font.family': 'serif',
            'font.serif': 'Computer Modern Roman',
            'font.sans-serif': 'Computer Modern Sans serif',
            'font.size': 10,
            'axes.labelsize': font_size,
            'legend.fontsize': font_size,
            'xtick.labelsize': tick_font_size,
            'ytick.labelsize': tick_font_size,
            'text.usetex': 'false',
            'lines.linewidth': 1.,
        }

        data = np.recfromtxt('%s.dat' % self.runner_name, names=True, deletechars=None)

        model = KMC_Model(print_rates=False,
                          banner=False,)

        # override with user-provided parameters
        if rcParams is not None:
            default_rcParams.update(rcParams)
        matplotlib.rcParams.update(default_rcParams)

        # plot all TOFs defined in model if not specified
        if plot_tofs is None:
            plot_tofs = model.tofs

        if plot_occs is None:
            plot_occs = list(data.dtype.names)
            plot_occs.remove('kmc_time')
            plot_occs.remove('kmc_steps')
            for header_param in model.get_param_header().split():
                plot_occs.remove(header_param)

            for tof in model.tofs:
                tof = tof.replace(')', '').replace('(', '')
                try:
                    plot_occs.remove(tof)
                except ValueError:
                    print('%s not in %s' % (tof, plot_occs))

        # check how many variable parameters we have
        # if not specified

        if variable_parameters is None:
            variable_parameters = {}
            for param_name, param in list(self.parameters.items()):
                if param.steps > 1:
                    variable_parameters[param_name] = param
        else:
            vparams = {}
            for vparam in variable_parameters:
                if vparam in self.parameters:
                    vparams[vparam] = self.parameters[vparam]
                else:
                    raise UserWarning("Request variable not in ModelRunner.")

            variable_parameters = vparams

        ######################
        # plot coverages     #
        ######################
        fig = plt.figure(figsize=figsize)
        if len(variable_parameters) == 0:
            print("No variable parameter. Nothing to plot.")
        elif len(variable_parameters) == 1:
            xvar = list(variable_parameters.keys())[0]
            data.sort(order=xvar)
            for occ in plot_occs:
                occs = [data[name] for name in data.dtype.names if name.startswith(occ)]
                N_occs = len(occs)
                occ_data = np.array(occs).sum(axis=0) / N_occs
                plt.plot(data[xvar], occ_data, label=occ.replace('_', '\_'))
            legend = plt.legend(loc='best', fancybox=True)
            legend.get_frame().set_alpha(0.5)
            plt.ylim([0, 1])

        elif len(variable_parameters) == 2:
            print("Two variable parameters. Doing a surface plot.")
        else:
            print("Too many variable parameters. No automatic plotting possible.")

        for suffix in suffixes:
            if label is None:
                if sublabel is None:
                    plt.savefig('%s_coverages.%s' % (self.runner_name, suffix), bbox_inces='tight')
                else:
                    plt.savefig('%s_%s_coverages.%s' % (self.runner_name, sublabel, suffix), bbox_inces='tight')
            else:
                if sublabel is None:
                    plt.savefig('%s_coverages.%s' % (label, suffix), bbox_inces='tight')
                else:
                    plt.savefig('%s_%s_coverages.%s' % (label, sublabel, suffix), bbox_inces='tight')

        ######################
        # plot TOFs          #
        ######################
        fig = plt.figure(figsize=figsize)
        if len(variable_parameters) == 0:
            print("No variable parameter. Nothing to plot.")
        elif len(variable_parameters) == 1:
            xvar = list(variable_parameters.keys())[0]
            param = list(variable_parameters.values())[0]
            data.sort(order=xvar)
            for tof in plot_tofs:
                tof = tof.replace(')', '').replace('(', '')
                if arrhenius :
                    plt.plot(1000./data[xvar], np.log(data[tof]), label=tof.replace('_', '\_'))
                else:
                    plt.plot(data[xvar], data[tof], label=tof.replace('_', '\_'))
            legend = plt.legend(loc='best', fancybox=True)
            legend.get_frame().set_alpha(0.5)
            if arrhenius:
                plt.xlabel(r'$1000\,/%s$ [%s$^{-1}$]' % (xvar, param.unit))
                plt.ylabel(r'log(TOF)')
            else:
                plt.xlabel(r'\emph{%s} [%s]' % (xvar, param.unit))
                plt.ylabel(r'TOF [s$^{-1}$ cell$^{-1}$]')
        elif len(variable_parameters) == 2:
            print("Two variable parameters. Doing a surface plot.")
        else:
            print("Too many variable parameters. No automatic plotting possible.")

        for suffix in suffixes:
            if label is None:
                plt.savefig('%s_TOFs.%s' % (self.runner_name, suffix), bbox_inches='tight')
            else:
                plt.savefig('%s_TOFs.%s' % (label, suffix), bbox_inches='tight')

        model.deallocate()

    def run(self, init_steps=1e8,
                  sample_steps=1e8,
                  cores=4,
                  samples=1,
                  random_seed=None):
        """Launch the ModelRunner instance. Creates a regular grid over
        all ModelParameters defined in the ModelRunner class.

        :param init_steps: Steps to run model before sampling (.ie. to reach steady-state).
        (Default: 1e8)
        :type init_steps: int
        :param sample_steps: Number of steps to sample over (Default: 1e8)
        :type sample_steps: int
        :param cores: Number of parallel processes to launch.
        :type cores: int
        :param samples: Number of samples. Use more samples if precise coverages are needed (Default: 1).
        :type samples: int

        """

        parameters = []
        for parameter in list(self.parameters.values()):
            parameters.append(parameter.get_grid())
        points = list(self.__product(*tuple(parameters)))

        random.shuffle(points)

        for sub_list in self.__split_seq(points, cores):
            p = Process(target=self.__run_sublist, args=(sub_list,
                                                         init_steps,
                                                         sample_steps,
                                                         samples,
                                                         random_seed,
                                                         ))
            p.start()

def set_rate_constants(parameters=None, print_rates=None, can_accelerate=False):
    """Tries to evaluate the supplied expression for a rate constant
    to a simple real number and sets it for the corresponding process.
    For the evaluation it draws on predefined natural constants, user defined
    parameters and mathematical functions.

    :param parameters: List of parameters to be used when evaluating expression.
                      (Default: None)
    :type parameters: list
    :param print_rates: Print the rates while setting them
                        (Default: True)
    :type print_rates: bool

    """
    proclist = ProclistProxy()
    if print_rates is None:
        print_rates = True

    if parameters is None:
        parameters = settings.parameters

    if print_rates:
        print('-------------------')
    for proc in sorted(settings.rate_constants):
        rate_expr = settings.rate_constants[proc][0]
        rate_const = evaluate_rate_expression(rate_expr, parameters)

        if rate_const < 0.:
            raise UserWarning('%s = %s: Negative rate-constants do no make sense'
                              % (rate_expr, rate_const))
        try:
            base.set_rate_const(getattr(proclist, proc.lower()),
                                rate_const)
            if print_rates:
                n = int(4 * log(rate_const))
                print('%30s: %.3e s^{-1}: %s' % (proc, rate_const, '#' * n))
        except Exception as e:
            raise UserWarning(
                "Could not set %s for process %s!\nException: %s" \
                    % (rate_expr, proc, e))
        
        if can_accelerate:
            try:
                base.set_original_rate_const(getattr(proclist, proc.lower()),
                                                                   rate_const)
            except Exception as e:
                raise UserWarning(
                    "Could not set %s for process %s!\nException: %s" \
                        % (rate_expr, proc, e))
        
    if print_rates:
        print('-------------------')

    # FIXME
    # update chemical potentials (works for otf backend only)
    if hasattr(proclist,'update_user_parameter'):
         for name,entry in list(settings.parameters.items()):
             proclist.update_user_parameter(
                 getattr(proclist,name.lower()),
                 evaluate_rate_expression(
                 # FIXME Take first item of lists
                 # to support for deprecated 'lattice_size' parameter
                     str(entry['value']).split(' ')[0],
                                          parameters))

    if hasattr(proclist,'update_chempot'):
         for chempot in settings.chemical_potentials:
             proclist.update_chempot(
                 getattr(proclist,chempot.lower()),
                 evaluate_rate_expression(chempot,parameters))

    if hasattr(proclist,'recalculate_rates_matrix'):
         proclist.recalculate_rates_matrix()

def import_ase():
    """Wrapper for import ASE."""
    try:
        import ase
        import ase.visualize
    except:
        print('Please download the ASE from')
        print('https://wiki.fysik.dtu.dk/ase/')
    return ase

def get_tof_names():
    """Return names turn-over-frequencies (TOF) previously defined in model."""
    tofs = []
    for process, tof_count in list(settings.tof_count.items()):
        for tof in tof_count:
            if tof not in tofs:
                tofs.append(tof)
    return sorted(tofs)

class ProcInt(int):

    def __new__(cls, value, *args, **kwargs):
        return int.__new__(cls, value)

    def __init__(self, value):
        self.procnames = sorted(settings.rate_constants.keys())

    def __repr__(self):
        name = self.procnames[self.__int__() - 1]
        return 'Process model.proclist.%s (%s)' % (name.lower(), self.__int__())

class SiteInt(int):

    def __new__(cls, value, *args, **kwargs):
        return int.__new__(cls, value)

    def __repr__(self):
        x, y, z, n = lattice.calculate_nr2lattice(self.__int__())
        return 'Site (%s, %s, %s, %s) [#%s]' % (x, y, z, n, self.__int__())

    def __getitem__(self, item):
        site = lattice.calculate_nr2lattice(self.__int__())
        return site[item]
