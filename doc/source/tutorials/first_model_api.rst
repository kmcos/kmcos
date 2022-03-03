.. _api-tutorial:

A first kMC Model--the API way
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In general there are two interfaces to *defining* a new
model: A GUI and an API. While the GUI can be quite
nice especially for beginners, it turns out that the
API is better maintained simply because ... well, maintaing
a GUI is a lot more work.

So we will start by learning how to setup the model using the
API which will turn out not to be hard at all. It is knowing howto
do this will also pay-off especially if you starting tinkering
with your existing models and make little changes here and there.


Build the model
===============

You may also look at MyFirstDiffusion__build.py in the examples directory.

We start by making the necessary import statements (in `*python* <http://python.org>`_ or better `*ipython* <http://ipython.org>`_)::

  import kmcos
  from kmcos.types import *
  from kmcos.io import *
  import numpy as np

which imports all classes that make up a kMC project. The functions
from `kmcos.io` will only be needed at the end to save the project
or to export compilable code.

The example sketched out here leads you to a kMC model for CO adsorption
and desorption on Pd(100). First you should instantiate a new project 
and fill in meta information ::

  kmc_model = kmcos.create_kmc_model()
  kmc_model.set_meta(author = 'Your Name',
              email = 'your.name@server.com',
              model_name = 'MyFirstModel',
              model_dimension = 2,)


Next you add some species or states. Note that whichever
species you add first is the default species with which all sites in the
system will be initialized. Of course this can be changed later

For surface science simulations it is useful to define an
*empty* state, so we add ::

 kmc_model.add_species(name='empty')

and some surface species. Given you want to simulate CO adsorption and
desorption on a single crystal surface you would say ::

  kmc_model.add_species(name='CO',
                 representation="Atoms('CO',[[0,0,0],[0,0,1.2]])")

where the string passed as `representation` is a string representing
a CO molecule which can be evaluated in `ASE namespace <https://gitlab.com/ase/ase/repository/archive.zip?ref=master>`_.

Once you have all species declared is a good time to think about the geometry.
To keep it simple we will stick with a simple-cubic lattice in 2D which
could for example represent the (100) surface of a fcc crystal with only
one adsorption site per unit cell. You start by giving your layer a name ::

  layer = kmc_model.add_layer(name='simple_cubic')

and adding a site ::

  layer.sites.append(Site(name='hollow', pos='0.5 0.5 0.5',
                          default_species='empty'))


Where `pos` is given in fractional coordinates, so this site
will be in the center of the unit cell.

Simple, huh? Now you wonder where all the rest of the geometry went?
For a simple reason: the geometric location of a site is
meaningless from a kMC point of view. In order to solve the master
equation none of the numerical coordinates
of any lattice sites matter since the master equation is only
defined in terms of states and transition between these. However
to allow a graphical representation of the simulation one can add geometry
as you have already done for the site. You set the size of the unit cell
via ::

  kmc_model.lattice.cell = np.diag([3.5, 3.5, 10])

which are prototypical dimensions for a single-crystal surface in
Angstrom.

Ok, let us see what we managed so far: you have a *lattice* with a
*site* that can be either *empty* or occupied with *CO*.


Populate process list and parameter list
========================================

The remaining work is to populate the `process list` and the
`parameter list`. The parameter list defines the parameters
that can be used in the expressions of the rate constants.
In principle one could do without the parameter
list and simply hard code all parameters in the process list,
however one looses some nifty functionality like easily
changing parameters on-the-fly or even interactively.

A second benefit is that you achieve a clear separation
of the kinetic model from the barrier input,
which usually has a different origin.

In practice filling the parameter list and the process
list is often an iterative process, however since
we have a fairly short list, we can try to set all parameters
at once.

First of all you want to define the external parameters to
which our model is coupled. Here we use the temperature
and the CO partial pressure::

  kmc_model.add_parameter(name='T', value=600., adjustable=True, min=400, max=800)
  kmc_model.add_parameter(name='p_CO', value=1., adjustable=True, min=1e-10, max=1.e2)

You can also set a default value and a minimum and maximum value
set defines how the scrollbars a behave later in the runtime GUI.

To describe the adsorption rate constant you will need the area
of the unit cell::

  kmc_model.add_parameter(name='A', value='(3.5*angstrom)**2')

Last but not least you need a binding energy of the particle on
the surface. Since without further ado we have no value for the
gas phase chemical potential, we'll just call it deltaG and keep
it adjustable ::

  kmc_model.add_parameter(name='deltaG', value='-0.5', adjustable=True,
                             min=-1.3, max=0.3)

To define processes we first need a coordinate [#coord_minilanguage]_  ::

  coord = kmc_model.lattice.generate_coord('hollow.(0,0,0).simple_cubic')


Then you need to have at least two processes. A process or elementary step in kMC
means that a certain local configuration must be given so that something
can happen at a certain rate constant. In the framework here this is
phrased in terms of 'conditions' and 'actions'. [#proc_minilanguage]_
So for example an adsorption requires at least one site to be empty
(condition). Then this site can be occupied by CO (action) with a
rate constant. Written down in code this looks as follows ::

  kmc_model.add_process(name='CO_adsorption',
                 conditions=[Condition(coord=coord, species='empty')],
                 actions=[Action(coord=coord, species='CO')],
                 rate_constant='p_CO*bar*A/sqrt(2*pi*umass*m_CO/beta)')



.. note:: In order to ensure correct functioning of the kmcos kMC solver every action should have a corresponding condition for the same coordinate.

Now you might wonder, how come we can simply use m_CO and beta and such.
Well, that is because the evaluator will to some trickery to resolve such
terms. So beta will be first be translated into 1/(kboltzmann*T) and as
long as you have set a parameter `T` before, this will go through. Same
is true for m_CO, here the atomic masses are looked up and added. Note
that we need conversion factors of `bar` and `umass`.

Then the desorption process is almost the same, except the reverse::

  kmc_model.add_process(name='CO_desorption',
                 conditions=[Condition(coord=coord, species='CO')],
                 actions=[Action(coord=coord, species='empty')],
                 rate_constant='p_CO*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(beta*deltaG*eV)')


To reduce typing, kmcos also knows a shorthand notation for processes.
In order to produce the same process you could also type ::

  kmc_model.parse_process('CO_desorption; CO@hollow->empty@hollow ; p_CO*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(beta*deltaG*eV)')

and since any non-existing on either the left or the right side
of the `->` symbol is replaced by a corresponding term with
the `default_species` (in this case `empty`) you could as
well type ::

  kmc_model.parse_process('CO_desorption; CO@hollow->; p_CO*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(beta*deltaG*eV)')


and to make it even shorter you can parse and add the process on one line ::

  kmc_model.parse_and_add_process('CO_desorption; CO@hollow->; p_CO*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(beta*deltaG*eV)')


In order to add processes on more than one site possible spanning across unit
cells, there is a shorthand as well. The full-fledged syntax for each
coordinate is ::

  "<site-name>.<offset>.<lattice>"

check :ref:`manual_coord_generation` for details.

Export, save, compile
=====================

Before we compile the model, we should specify and understand the various backends that are involved.

local_smart backend (default) for models with <100 processes.
lat_int backend for models with >100 processes. (build the model same ways local_smart but different backend for compile step)
otf backend requires custom model (build requires different process definitions compared to local_smart) and can work for models which require >10000 processes, since each process rate is calculated on the fly instead of being held in memory.

Here is how we specify the model's backend ::

  kmc_model.backend = 'local_smart'
  kmc_model.backend = 'lat_int'
  kmc_model.backend = 'otf'

Next, it's a good idea to save and compile your work ::

  kmc_model.save_model()
  kmcos.compile(kmc_model)

This creates an XML file with the full definition of your model and exports the model to compiled code.

Now is the time to leave the python shell. In the current
directory you should see a `myfirst_kmc.xml`.
You will also see a directory ending with _local_smart,
this directory includes your compiled model.

You can also skip the model exporting and do it later by removing kmcos.compile(kmc_model):
you can use a separate python file later, or from the command line 
can run `kmcos export myfirst_kmc.xml` in the same directory as the XML.

During troubleshooting, exporting separately can be useful to make sure 
the compiling occurs gracefully without any line
containining an error.

Running and viewing the model
-----------------------------

If you now `cd` to that folder `myfirst_kmc_local_smart` and run ::

  python3 kmc_settings.py benchmark 

You should see that the model was able to run!
Next, let's try seeing how it looks visually with ::
  
  python3 kmc_settings.py view

... and dada! Your first running kMC model right there!
For some installations, one can type `kmcos benchmark` and `kmcos view.`

For running the model, you should use a runfile.

If you wonder why the CO molecules are basically just dangling
there in mid-air that is because you have no background setup, yet.
Choose a transition metal of your choice and add it to the
lattice setup for extra credit :-).

Wondering where to go from here? If the work-flow makes
complete sense, you have a specific model in mind,
and just need some more idioms to implement it
I suggest you take a look at the `examples folder <https://github.com/mhoffman/kmcos/tree/master/examples>`_.
for some hints. To learn more about the kmcos approach
and methods you should into :ref:`topic guides <topic-guides>`.

In technical terms, kmcos is run  an API via the kmcos python module.

Additionally, though now discouraged, kmcos can be invoked directly from the command line in one of the following
ways::

    kmcos [help] (all|benchmark|build|edit|export|help|import|rebuild|run|settings-export|shell|version|view|xml) [options]

Taking it home
==============

Despite its simplicity you have now seen all elements needed
to implement a kMC model and hopefully gotten a first feeling for
the workflow.



.. [#proc_minilanguage]  You will have to describe all processes
                         in terms of  `conditions` and
                         `actions` and you find a more complete
                         description in the
                         :ref:`topic guide <proc_mini_language>`
                         to the process description syntax.

.. [#coord_minilanguage] The description of coordinates follows
                         the simple syntax of the coordinate
                         syntax and the
                         :ref:`topic guide <coord_mini_language>`
                         explains how that works.


An alternative way using .ini files
===================================

Presently, a full description of the .ini capability is not being provided because this way is not the standard way of using kmcos. However, it is available.  This method is an alternative to making an xml file, and can be used instead of kmcos export.

Prepare a minimal input file with the following content and save it as ``mini_101.ini`` ::

    [Meta]
    author = Your Name
    email = you@server.com
    model_dimension = 2
    model_name = fcc_100

    [Species empty]
    color = #FFFFFF

    [Species CO]
    representation = Atoms("CO", [[0, 0, 0], [0, 0, 1.17]])
    color = #FF0000

    [Lattice]
    cell_size = 3.5 3.5 10.0

    [Layer simple_cubic]
    site hollow = (0.5, 0.5, 0.5)
    color = #FFFFFF

    [Parameter k_CO_ads]
    value = 100
    adjustable = True
    min = 1
    max = 1e13
    scale = log

    [Parameter k_CO_des]
    value = 100
    adjustable = True
    min = 1
    max = 1e13
    scale = log

    [Process CO_ads]
    rate_constant = k_CO_ads
    conditions = empty@hollow
    actions = CO@hollow
    tof_count = {'adsorption':1}

    [Process CO_des]
    rate_constant = k_CO_des
    conditions = CO@hollow
    actions = empty@hollow
    tof_count = {'desorption':1}

In the same directory run ``kmcos export mini_101.ini``. You should now have a folder ``mini_101_local_smart``
in the same directory. ``cd`` into it and run ``kmcos benchmark``. If everything went well you should see something
like ::

    Using the [local_smart] backend.
    1000000 steps took 1.51 seconds
    Or 6.62e+05 steps/s

In the same directory try running ``kmcos view`` to watch the model run or fire up ``kmcos shell``
to interact with the model interactively. Explore more commands with ``kmcos help`` and please
refer to the documentation how to build complex model and evaluate them systematically. To test all bells and whistles try ``kmcos edit mini_101.ini`` and inspect the model visually.