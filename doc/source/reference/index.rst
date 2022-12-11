********************
Reference
********************

Command Line Interface (CLI)
============================

.. include:: cli.rst

Data Types
==========

kmcos.types
^^^^^^^^^^

.. automodule:: kmcos.types
.. autoclass:: kmcos.types.Project
   :members: add_layer, add_parameter, add_process, add_species, add_site,
             get_layers, get_parameters, get_processes, get_speciess,
             import_xml_file, lattice, parse_and_add_process, parse_process,
             print_statistics, save, set_meta, validate_model
.. autoclass:: kmcos.types.Meta
.. autoclass:: kmcos.types.Parameter
.. autoclass:: kmcos.types.LayerList
    :members: generate_coord_set, generate_coord
.. autoclass:: kmcos.types.Layer
.. autoclass:: kmcos.types.Site
.. autoclass:: kmcos.types.Species
.. autoclass:: kmcos.types.Process
.. autoclass:: kmcos.types.ConditionAction
.. autoclass:: kmcos.types.Coord

kmcos.io
^^^^^^^

.. automodule:: kmcos.io
   :members: export_source, import_xml, export_xml

.. autoclass:: kmcos.io.ProcListWriter
   :members: write_lattice, write_proclist, write_settings

Editor frontend
===============

kmcos.gui
^^^^^^^^^^

.. automodule:: kmcos.gui
.. autoclass:: kmcos.gui.Editor
.. autoclass:: kmcos.gui.GTKProject

kmcos.forms
^^^^^^^^^^

.. automodule:: kmcos.forms
   :members: MetaForm, SpeciesListForm, SpeciesForm, ParameterForm,
             LatticeForm, LayerEditor, SiteForm, ProcessForm,
             parse_chemical_expression, BatchProcessForm

Runtime frontend
================

kmcos.run
^^^^^^^^

.. automodule:: kmcos.run

.. autoclass:: kmcos.run.ModelRunner
   :members: run

.. autoclass:: kmcos.run.ModelParameter

.. autoclass:: kmcos.run.PressureParameter

.. autoclass:: kmcos.run.TemperatureParameter

.. autoclass:: kmcos.run.LinearParameter

.. autoclass:: kmcos.run.LogParameter


kmcos.run.KMC_Model (typical usage model.___)
^^^^^^^^

.. autoclass:: kmcos.run.KMC_Model
  :members: _adjust_database,
            _get_configuration,
            _put,
            _set_configuration,
            base,
            cell_size,
            deallocate,
            do_steps,
            double,
            dump_config,
            export_movie,
            get_atoms,
            get_backend,
            get_occupation_header,
            get_param_header,
            get_std_sampled_data,
            get_tof_header,
            halve,
            lattice,
            load_config,
            model.get_std_sampled_data,
            nr2site,
            null_species,
            parameters,
            post_mortem,
            plot_configuration,
            print_accum_rate_summation,
            print_adjustable_parameters,
            print_coverages,
            print_rates,
            procstat,
            procstat_normalized,
            procstat_pprint,
            put,
            rate_constants,
            reset,
            run,
            settings,
            show,
            site2nr,
            start,
            steps_per_frame,
            view,
            xml,

.. autoclass:: kmcos.run.Model_Rate_Constants
   :members: __call__,
             by_name,
             inverse

.. autoclass:: kmcos.run.Model_Parameters
   :members: __call__

kmcos.view
^^^^^^^^^

.. automodule:: kmcos.view
   :members: KMC_Viewer

kmcos.cli
^^^^^^^^

.. automodule:: kmcos.cli
   :members: main

kmcos.utils
^^^^^^^^^^

.. automodule:: kmcos.utils
   :members: T_grid, build, evaluate_kind_values, get_ase_constructor, p_grid \
             product, split_sequence, write_py

kmcos kMC project DTD
====================

A standardized kmc model format has been made in XML. 
XML was chosen over JSON, pickle or alike because near 2010 it was the most flexible
and universal format with good methods to define the overall
structure of the data.

New infrastrcture for JSON formats now exists, and it is on the to-do list to 
switch to using JSON to make a standard kmc model format.

One way to define an XML format is by using a document type description
(DTD) and in fact at every import a kmcos file is validated against
the DTD below.

.. literalinclude:: kmc_project_v0.2.dtd



Connected Variables
====================

The connected_variables dictionary allows a person to pass string-writable objects
created during the model building into the runtime environment. This can be useful if
a person needs access to some data structures (like lists of surrounding sites) during runtime.
Dictionaries, strings, and lists can be passed. For more complex variables,
one could pass the name of a pickle file.
This feature is used for the surroundingSitesDict.


The basic syntax in a build_file would be as follows::

    kmc_model = kmcos.create_kmc_model(model_name)
    kmc_model.connected_variables['frog_list'] = [1,2,3,4]

Then, during runtime, one could do the following::

    print(model.connected_variables['frog_list'])
    
Additional Information for developers. Currently (Dec 2022), the way kmcos processes things from the build file to the Runtime environment is as follows:

    A person's build file makes a Project class object (typically "kmc_model"), for example in https://github.com/kmcos/kmcos/blob/master/examples/MyFirstDiffusion__build.py
    That build file makes an xml file (or ini file), which occurs in types.py _get_etree_xml or _get_etree_ini where a string is made that then gets written to file.
    That xml/ini is then read back in and validated , which occurs against a DTD. A new Project class object is made from what is read back in.
    It is important to recognize that the new Project class object has many attributes that are the same as the one in the build file, but it is not the same object. It has fewer of the original attributes due to hardcoded mapping during xml writing and xml reading.
    When the source code compilation occurs, kmc_settings. is made. What is in kmc_settings roughly mirrors the original Project class object, but it is actually from the new Project class object that has been created from the xml. 


Backends
========

In general the backend includes all functions that are implemented in Fortran90,
which therefore should not have to be changed by hand often. The backend is
divided into three modules, which import each other in the following way ::

  base <- lattice <- proclist

The key for this division is reusability of the code. The `base` module
implement all aspects of the kMC code, which do not depend on the described
model. Thus it "never" has to change. The `latttice` module basically
repeats all methods of the `base` model in terms of lattice coordinates.
Thus the `lattice` module only changes, when the geometry of the model
changes, *e.g.* when you add or delete sites.
The `proclist` module implements the process list, that is the species
or states each site can have and the elementary steps. Typically that
changes most often while developing a model.

The rate constants and physical parameters of the system are not implemented
in the backend at all, since in the physical sense they are too high-level
to justify encoding and compilation at the Fortran level and so they
are typical read and parsed from a python script.

The `kmcos.run.KMC_Model` class implements a convenient interface for most of
these functions, however all public methods (in Fortran called subroutines)
and variables can also be accessed directly like so ::

  from kmcos.run import KMC_Model
  model = KMC_Model(print_rates=False, banner=False)
  model.base.<TAB>
  model.lattice.<TAB>
  model.proclist.<TAB>

which works best in conjunction with `ipython <ipython.org>`_.

local_smart
^^^^^^^^^^^^
.. include:: robodoc/local_smart_base.rst
.. include:: robodoc/local_smart_lattice.rst
.. include:: robodoc/local_smart_proclist.rst
.. include:: robodoc/local_smart_kind_values.rst

lat_int
^^^^^^^

.. include:: robodoc/lat_int_base.rst
.. include:: robodoc/lat_int_lattice.rst
.. include:: robodoc/lat_int_proclist_constants.rst
.. include:: robodoc/lat_int_proclist.rst
.. include:: robodoc/lat_int_kind_values.rst

otf
^^^

.. include:: robodoc/otf_base.rst
.. include:: robodoc/otf_lattice.rst
.. include:: robodoc/otf_proclist_constants.rst
.. include:: robodoc/otf_proclist.rst
.. include:: robodoc/otf_kind_values.rst
