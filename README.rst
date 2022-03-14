.. image:: https://img.shields.io/badge/license-GPLv3-brightgreen.svg?style=flat-square)
    :target COPYING
.. image:: https://readthedocs.org/projects/kmcos/badge/?version=latest
    :target: http://kmcos.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

kmcos: Kinetic Monte Carlo of Systems
=====================================
*kmcos is designed for lattice based Kinetic Monte Carlo simulations to understand chemical kinetics and mechanisms. It has been used to produce more than 10 scientific publications. Links to tutorials and other documentation are below.*


DOCUMENTATION
##############

Please refer to

* Documentation (including installation): http://kmcos.readthedocs.org/
* Examples https://github.com/kmcos/kmcos/tree/master/examples
* Workshop files: https://github.com/kmcos/intro2kmcos [the later part of the document are for advanced users and may require an instructor]


HELP, BUGS, ISSUES, TROUBLE
###########################

This code is research code for scientists by scientists. If you
believe you have hit a bug, have a feature request get in touch
with us either via the `mailing list <https://groups.google.com/forum/#!forum/kmcos-users>`_, or open an `issue <https://github.com/kmcos/kmcos/issues/new>`_ .


CONTRIBUTORS
############
Current Project Leaders:

* Karsten Reuter
* Aditya (Ashi) Savara

Creator:

* Max J. Hoffmann

Developers:

* Sebastian Matera
* Juan M. Lorenzi
* Mie Andersen
* Michal Bajdich
* Andreas Garhammer

Other:
* Martin Deimel
* Thomas Danielson
* Jonathan Sutton
* Joseba Alberdi
* Steve Erwin & NB
* Meelod Waheed

THANKS
######

This project draws on several other great Python modules, which are in turn
each free software and we would like to thank each of these projects for
making their code freely avalaible, namely:

* `Python <http://www.python.org>`_
* `ASE <https://wiki.fysik.dtu.dk/ase/>`_
* Numpy
* `f2py <http://cens.ioc.ee/projects/f2py2e/>`_
* `kiwi <http://www.async.com.br/projects/kiwi/>`_, gazpacho
* lxml and in particular `ElementTree <http://www.effbot.org/>`_

FILES
#####
| ├── COPYING                                      # Copy of GPLv3
| ├── INSTALL.rst                                  # installation instructions
| ├── README.rst                                   # This document
| ├── TODO.rst                                     # Ideas for improvement and new features
| ├── requirements.txt                             # Dependencies which can be installed via pip
| ├── setup.py                                     # setuptools using setup script
| ├── index.html                                   # landing website
| ├── kmcos/                                        # the core kmcos python modules
| │   ├── cli.py                                   # the command line interface
| │   ├── config.py                                # configuration of some project wide paths
| │   ├── fortran_src/                             # static Fortran 90 source files
| │   │   ├── assert.ppc                           # assertion macro
| │   │   ├── base.f90                             # the default kMC solver
| │   │   ├── base_lat_int.f90                     # slightly modified kMC solver for lat_int backend
| │   │   ├── kind_values.f90                      # definition of project wide kind values
| │   │   └── main.f90                             # source template for standalone Fortran 90 clients
| │   ├── gui/                                     # kmcos.gui module
| │   │   ├── forms.py                             # view definitions (MVC) of editor GUI
| │   │   └── __init__.py                          # controller definitions (MVC) of editor GUI
| │   ├── __init__.py                              # root import module
| │   ├── io.py                                    # conversion between format: contains main Code Generator
| │   ├── kmc_editor.glade                         # Glade XML definiton for form interfaces
| │   ├── kmc_project_v0.1.dtd                     # Document Type Definition file of kMC project v0.1
| │   ├── kmc_project_v0.2.dtd                     # Document Type Definition file of kMC project v0.2
| │   ├── run.py                                   # High-level API for compiled models
| │   ├── species.py                               # Convenient interface for some reaction intermediates
| │   ├── types.py                                 # The basic classes for building kMC models
| │   ├── units.py                                 # Definition of conversion factor (CODATA 2010)
| │   ├── utils/                                   # Utility function that didn't fit elsewhere
| │   │   ├── __init__.py
| │   │   ├── ordered_dict.py
| │   │   ├── progressbar.py
| │   │   └── terminal.py
| │   └── view.py                                  # The runtime GUI for compiled models
| ├── doc/                                         # user guide, documentation, and reference
| │   └── source/                                  # documentation source file for compilation with Sphinx
| ├── examples/                                    # demoing non-standard features and useful idioms
| │   ├── AB_model.py                              # small demo file
| │   ├── benchmark_compilers_and_backends.sh      # demo file
| │   ├── crowded.xml                              # demo file
| │   ├── dreiD.xml                                # demo file for 3d model
| │   ├── dummy.xml                                # mininal model
| │   ├── model_Pt111_surface.py                   # demo file for non-rectangular lattice
| │   ├── multidentate.py                          # basic example for multidentate adsorption
| │   ├── render_bigcell.py                        # demo containing many sites
| │   ├── render_co_oxidation_ruo2.py              # demoing th CO Oxidation at RuO2(110) model
| │   ├── render_diffusion_model.py                # idioms for describing lateral interaction
| │   ├── render_einsD.py                          # simple 1-dimensional model
| │   ├── render_multispecies.py                   # render many species
| │   ├── render_pairwise_interaction.py           # idioms for describing lateral interaction
| │   ├── render_Pt_111.py                         # another non-rectangular lattice
| │   ├── render_sand_model.py                     # a neat diffusion model for non-trivial boundary conditions
| │   ├── run_in_multi_process.py                  # an example for parallelization over processes
| │   ├── run.py                                   # a high-level run script using the ModelRunner metaclass
| │   ├── ruptured_Pd.xml                          # a fcc(100) like surface with some sites missing
| │   └── small.xml                                # demo file
| ├── tests/                                       # Unit tests and test data
| ├── tools                                        # Entry points for command line interface
| │   ├── kmcos
| │   ├── kmcos.bat
| │   ├── kmcos-build-standalone
| │   └── kmcos-install-dependencies-ubuntu


COPYRIGHT AND LICENSE
#####################

Copyright (C) 2009-13 Max J. Hoffmann

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, see `http://www.gnu.org/licenses/ <http://www.gnu.org/licenses/>`_.
