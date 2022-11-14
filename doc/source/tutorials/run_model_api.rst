Running the Model From Runfiles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Running the Model--the API way
==============================

Normally, one uses python runfiles.
However, it is convenient to initially run commands interactively for learning purposes.
The simplest thing to do is to start the model
from within a compiled model directory
using "python3 kmc_settings.py run"

That will start a python shell, allowing one to skip the below commands ::

  #!/usr/bin/env python
  from kmcos.run import KMC_Model
  model = KMC_Model()

and just interact directly with `model`. It is often a good idea to use ::

    %logstart some_scriptname.py

as your first command in the IPython command to save what you have typed for later use.

When using a runfile, the starting banner can be turned off by using::

  model = KMC_Model(print_rates=False, banner=False)

Now that you have got a model, you try to do some KMC steps ::

  model.do_steps(100000)

which would run 100,000 kMC steps.

Let's say you want to change the temperature and a partial pressure of
the model you could type ::

  model.parameters.T = 550
  model.parameters.p_COgas = 0.5

and all rate constants are instantly updated. In order get a quick
overview of the current settings you can issue e.g. ::

  print(model.parameters)
  print(model.rate_constants)

or just ::

  print(model)

Now an instantiated und configured model has mainly two functions: run
kMC steps and report its current configuration.

To analyze the current state you may use ::

  atoms = model.get_atoms()

.. note::

  If you want to fetch data from the current state without
  actually visualizing the geometry can speed up the get_atoms()
  call using ::

    atoms = model.get_atoms(geometry=False)

This will return an ASE atoms object of the current system, but
it also contains some additional data piggy-backed such as ::

  model.get_occupation_header()
  atoms.occupation

  model.get_tof_header()
  atoms.tof_data


  atoms.kmc_time
  atoms.kmc_step

These quantities are often sufficient when running and simulating
a catalyst surface, but of course the model could be expanded
to more observables. The Fortran modules `base`, `lattice`,
and `proclist` are atttributes of the model instance so,
please feel free to explore the model instance e.g. using
ipython and ::

  model.base.<TAB>
  model.lattice.<TAB>
  model.proclist.<TAB>

etc..

The `occupation` is a 2-dimensional array which contains
the `occupation` for each surface `site` divided by
the number of unit cell. The first slot
denotes the species and the second slot denotes the
surface site, i.e. ::

  occupation = model.get_atoms().occupation
  occupation[species, site-1]

So given there is a `hydrogen` species
in the model, the occupation of `hydrogen` across all site
type can be accessed like ::

  hydrogen_occupation = occupation[model.proclist.hydrogen]

To access the coverage of one surface site, we have to
remember to subtract 1, when using the the builtin constants,
like so ::

  hollow_occupation = occupation[:, model.lattice.hollow-1]

Lastly it is important to call ::

  model.deallocate()

once the simulation if finished as this frees the memory
allocated by the Fortan modules. This is particularly
necessary if you want to run more than one simulation
in one script.

Generate Grids of Sampled Data
==============================

For some kMC applications you simply require a large number of data points
across a set of external parameters (phase diagrams, microkinetic models).
For this case there is a convenient class `ModelRunner` to work with ::

    from kmcos.run import ModelRunner, PressureParameter, TemperatureParameter

    class ScanKinetics(ModelRunner):
        p_O2gas = PressureParameter(1)
        T = TemperatureParameter(600)
        p_COgas = PressureParameter(min=1, max=10, steps=40)


    ScanKinetics().run(init_steps=1e8, sample_steps=1e8, cores=4)


This script generates data points over the specified range(s). The
temperature parameters is uniform grids over 1/T and the
pressure parameters is uniform over log(p). The
script can be run synchronously over many cores as long
as the cores can access the same file system. You have to test whether
the steps before sampling (`init_steps`) as well as the batch size
(`sample_steps`) is sufficient.


.. _manipulate_model_runtime:

Manipulating the Model Species at Runtime
=================================

To change species on the lattice at the start of simulation
or at any other time in the simulation, one can change
either the whole configuration, or only species on a specific site.

To change species on a specific site, one uses the put command.
There are several syntaxes to use the put command ::

  model.put(site=[x,y,z,n], model.proclist.<species>)
  Where 'n' and <species> are the site type and species, respectively. For example:
  model.put([0,0,0,model.lattice.ruo2_bridge], model.proclist.co)
  model.put([0,0,0,"ruo2_bridge"], "model.proclist.co")
  model.put([0,0,0,2], 1) #The 'n' is has indexing starting from 1 (there is no 0 for n), whereas the <species> indexing starts at 0.
  

If changing many sites at once, the abovev command is quite inefficient,
since each `put` call, adjusts the book-keeping database. To circumvent
the database update you can use the `_put` method, like so ::

  model._put(...)
  model._put(...)
  ...
  model._adjust_database()

note that after using '_put', one must remember to call `_adjust_database()`
before executing any next step or the database of available processes
will not match the species, the kmc simulation will become incorrect and likely crash after some steps.

If one wants to set the whole configuration of the lattice
once can retreive it, save it, and load it with the following commands ::

  model.dump_config("YourConfigurationName") 
  model.load_config("YourConfigurationName")

Those commands use the following internal commands as part of how they function :: 

  #saving the configuration uses:
  config = model._get_configuration()
  #loading configuration uses:
  model._set_configuration(config)
  model._adjust_database()
  



Running models in parallel
==========================

Due to the global clock in kMC there seems to be no
simple and efficient way to parallelize a kMC program.
kmcos certainly cannot parallelize a single system over
processors. However one can run several kmcos instances
in parallel which might accelerate sampling or efficiently
check for steady state conditions.

However in many applications it is still useful to
run several models seperately at once, for example to scan
some set of parameters one a multicore computer. This
kind of problem can be considered `embarrasingly parallel`
since it requires no communication between the runs.

This is made very simple through the `multiprocessing` module,
which is in the Python standard library since version 2.6.
For older versions this needs to be `downloaded <http://pypi.python.org/pypi/multiprocessing/>`
and installed manually. The latter is pretty straightforward.


Then besides `kmcos` we need to import `multiprocessing` ::

  from multiprocessing import Process
  from numpy import linspace
  from kmcos.run import KMC_Model

and let's say you wanted to scan a range of temperature,
while keeping all other parameteres constant. You first
define a function, that takes a set of temperatures
and runs the simulation for each ::


  def run_temperatures(temperatures):
      for T in temperatures:
          model = KMC_Model()
          model.parameters.T = T
          model.do_steps(100000)

          # do some evaluation

          model.deallocate()


In order to split our full range of input parameters, we
can use a utility function ::

  from kmcos.utils import split_sequence


All that is left to do, is to define the input parameters,
split the list and start subprocesses for each sublist ::

  if __name__ == '__main__':
      temperatures = linspace(300, 600, 50)
      nproc = 8
      for temperatures in split_sequence(temperatures, nproc):
          p = Process(target=run_temperatures, args=(temperatures, ))
          p.start()
