#!/usr/bin/env python3
"""Holds all the data models used in kmcos.
"""
from __future__ import print_function

# stdlib imports
import os
import re
from fnmatch import fnmatch

# numpy
import numpy as np


# XML handling
try:
    from lxml import etree as ET
except:
    ET = None
# Need to pretty print XML
from xml.dom import minidom

# kmcos own modules
from kmcos.utils import CorrectlyNamed
from kmcos.config import APP_ABS_PATH

kmcproject_v0_1_dtd = '/kmc_project_v0.1.dtd'
kmcproject_v0_2_dtd = '/kmc_project_v0.2.dtd'
kmcproject_v0_3_dtd = '/kmc_project_v0.3.dtd'
xml_api_version = (0, 3)


class FixedObject(object):

    """Handy class that easily allows to define data structures
    that can only hold a well-defined set of fields
    """
    attributes = []

    def __init__(self, **kwargs):
        self.__doc__ = ('\nAllowed keywords: %s' % self.attributes)
        for attribute in self.attributes:
            if attribute in kwargs:
                self.__dict__[attribute] = kwargs[attribute]
        for key in kwargs:
            if key not in self.attributes:
                raise AttributeError(
                    'Tried to initialize illegal attribute %s' % key)

    def __setattr__(self, attrname, value):
        if attrname in self.attributes + ['__doc__']:
            self.__dict__[attrname] = value
        else:
            raise AttributeError('Tried to set illegal attribute %s'
                                 % attrname)

    def __hash__(self):
        """Since python-kiwi update to 1.9.32 it requires all objecst in
           a object tree to be hashable. So, here we give it a hash
           function that is just 'good enough' to do the job.

        """
        return hash(self.__class__.__name__)


class Project(object):

    """A Project is where (almost) everything comes together.
    A Project holds all other elements needed to describe one
    kMC Project ready to be manipulated, exported, or imported.

    The overall structure is the following as is also displayed
    in the editor GUI.

    Project::

        - Meta
        - Parameters
        - Lattice(s)
        - Species
        - Processes
    """

    def __init__(self, model_name=None):
        self.meta = Meta()
        if type(model_name)==type(None):
            self.model_name = "UntitledModel"
            self.meta.model_name = "UntitledModel"
        else:
            self.model_name = model_name
            self.meta.model_name = model_name
        self.layer_list = LayerList()
        self.lattice = self.layer_list
        self.parameter_list = ParameterList()
        self.species_list = SpeciesList()
        self.process_list = ProcessList()
        self.output_list = OutputList()
        self.filename = self.model_name + ".xml"
        self.backend = "local_smart" #this is just the default.
        self.compile_options = ""
        self.error_list = []

        # Quick'n'dirty define access functions
        # needed in context with GTKProject
        self.get_layers = lambda: sorted(self.layer_list,
                                         key=lambda x: x.name)

        self.add_output = lambda output: self.output_list.append(output)
        self.get_outputs = lambda: sorted(self.output_list,
                                          key=lambda x: x.name)

    def get_speciess(self, pattern=None):
        """Return list of species in Project.

        :param pattern: Pattern to fnmatch name of process against.
        :type pattern: str
        """
        return sorted([item for item in self.species_list
                       if pattern is None or fnmatch(item.name, pattern)
                       ], key=lambda x: x.name)

    def get_parameters(self, pattern=None):
        """Return list of parameters in Project.

        :param pattern: Pattern to fnmatch name of parameter against.
        :type pattern: str
        """
        return sorted([item for item in self.parameter_list
                       if pattern is None or fnmatch(item.name, pattern)
                       ], key=lambda x: x.name)

    def get_processes(self, pattern=None):
        """Return list of processes.

        :param pattern: Pattern to fnmatch name of process against.
        :type pattern: str
        """
        return sorted([item for item in self.process_list
                       if pattern is None or fnmatch(item.name, pattern)
                       ], key=lambda x: x.name)

    def add_parameter(self, *parameters, **kwargs):
        """Add a parameter to the project. A Parameter,
        or keywords that are passed to the Parameter
        constructor are accepted.

        :param name: The name of the parameter.
        :type name: str
        :param value: Default value of parameter.
        :type value: float
        :param adjustable: Create controller in GUI.
        :type adjustable: bool
        :param min: Minimum value for controller.
        :type min: float
        :param max: Maximum value for controller.
        :type max: float
        :param scale: Controller scale: 'log' or 'lin'
        :type scale: str

        """

        for parameter in parameters:
            self.parameter_list.append(parameter)

        if kwargs:
            parameter = Parameter(**kwargs)
            self.parameter_list.append(parameter)
            return parameter

    def add_process(self, *processes, **kwargs):
        """Add a process to the project. A Process,
        or keywords that are passed to the Process
        constructor are accepted.

        :param name: Name of process.
        :type name: str
        :param rate_constant: Expression for rate constant.
        :type rate_constant: str
        :param condition_list: List of conditions (class Condition).
        :type condition_list: list.
        :param action_list: List of conditions (class Action).
        :type action_list: list.
        :param enabled: Switch this process on or of.
        :type enabled: bool.
        :param chemical_expression: Chemical expression (i.e: A@site1 + B@site2 -> empty@site1 + AB@site2) to generate process from.
        :type chemical_expression: str.
        :param tof_count: Stoichiometric factor for observable products {'NH3': 1, 'H2O(gas)': 2}. Hint: avoid space in keys.
        :type tof_count: dict.

        """
        for process in processes:
            self.process_list.append(process)
        if kwargs:
            if 'conditions' in kwargs:
                kwargs['condition_list'] = kwargs['conditions']
                kwargs.pop('conditions')
            if 'actions' in kwargs:
                kwargs['action_list'] = kwargs['actions']
                kwargs.pop('actions')
            process = Process(**kwargs)
            self.process_list.append(process)

            if 'name' in kwargs:
                if len(kwargs['name']) > 30:
                    self.error_list.append(tuple(("Process Name", kwargs['name'], "Process name should not be longer than 30 characters, otherwise the Fortran compiler may raise errors")))
        return process

    def parse_process(self, string):
        """Generate processes using a shorthand notation like, e.g. ::
            process_name; species1A@coord1 + species2A@coord2 + ... -> species1B@coord1 + species2A@coord2 + ...; rate_constant_expression

            .

            :param string: shorthand notation for process
            :type string: str

        """
        process = parse_process(string, self)
        return process

    def parse_and_add_process(self, string):
        """Generate and add processes using a shorthand notation like, e.g. ::
            process_name; species1A@coord1 + species2A@coord2 + ... -> species1B@coord1 + species2A@coord2 + ...; rate_constant_expression

            .

            :param string: shorthand notation for process
            :type string: str

        """
        process = parse_process(string, self)
        self.process_list.append(process)
        return process

    def add_species(self, *speciess, **kwargs):
        """Add a species to the project. A Species,
        or keywords that are passed to the Species
        constructor are accepted.

        :param name: Name of species.
        :type name: str
        :param color: Color of species in editor GUI (#ffffff hex-type specification).
        :type color: str
        :param representation: ase.atoms.Atoms constructor describing species geometry.
        :type representation: str
        :param tags: Tags of species (space separated string).
        :type tags: str

        """
        for species in speciess:
            self.species_list.append(species)
        if kwargs:
            species = Species(**kwargs)
            self.species_list.append(species)

        # if it is the first species and the
        # default species has not been set
        # do it now!
        if len(self.species_list) == 1 and \
           not hasattr(self.species_list, 'default_species'):
            self.species_list.default_species = species.name

        return species

    def add_layer(self, *layers, **kwargs):
        """Add a layer to the project. A Layer,
        or keywords that are passed to the Layer
        constructor are accepted.

        :param layers: List of layers.
        :type layers: list
        :param cell: Size of unit-cell.
        :type cell: np.array (3x3)
        :param default_layer: name of default layer.
        :type default_layer: str.

        """
        for layer in layers:
            self.layer_list.append(layer)
        if kwargs:
            layer = Layer(**kwargs)
            self.layer_list.append(layer)

        # if it is the first layer and default_layer
        # or substrate_layer have not been set
        # do it now!
        if len(self.layer_list) == 1:
            if not hasattr(self.layer_list, 'default_layer'):
                self.layer_list.default_layer = layer.name
            if not hasattr(self.layer_list, 'substrate_layer'):
                self.layer_list.substrate_layer = layer.name
        return layer

    def add_site(self, **kwargs):
        """Add a site to the project. The
        arguments are

        add_site(layer_name, site)

        :param name: Name of layer to add the site to.
        :type name: str
        :param site: Site instance to add.
        :type site: Site

        """

        try:
            layer_name = kwargs.pop('layer')
        except:
            raise UserWarning('Argument layer required.')

        try:
            layer = [layer for layer in self.get_layers()
                     if layer.name == layer_name][0]
        except:
            raise UserWarning('Layer %s not found.' % layer_name)
        layer.add_site(**kwargs)

    def __repr__(self):
        try:
            return self._get_xml_string()
        except (TypeError, AttributeError):
            return self._get_ini_string()

    def _get_xml_string(self):
        """Produces an XML representation of the project data
        """
        return prettify_xml(self._get_etree_xml())

    def _get_ini_string(self):
        """Return representation of model as can be written into a *.ini File.

        """
        from configparser import ConfigParser
        from io import StringIO
        config = ConfigParser()
        config.optionxform = str
        # Meta
        config.add_section('Meta')
        config.set('Meta', 'author', self.meta.author)
        config.set('Meta', 'email', self.meta.email)
        config.set('Meta', 'model_name', self.meta.model_name)
        config.set('Meta', 'model_dimension', str(self.meta.model_dimension))
        config.set('Meta', 'debug', str(self.meta.debug))

        config.add_section('SpeciesList')
        if hasattr(self.species_list, 'default_species'):
            config.set('SpeciesList', 'default_species',
                       self.species_list.default_species)
        else:
            config.set('SpeciesList', 'default_species', '')

        for species in self.get_speciess():
            section_name = 'Species %s' % species.name
            config.add_section(section_name)
            if hasattr(species, 'representation'):
                config.set(section_name,
                           'representation', species.representation)
            if hasattr(species, 'color'):
                config.set(section_name, 'color', species.color)
            config.set(section_name, 'tags', getattr(species, 'tags'))

        for parameter in self.get_parameters():
            section_name = 'Parameter %s' % parameter.name
            config.add_section(section_name)
            config.set(section_name, 'value', str(parameter.value))
            config.set(section_name, 'adjustable', str(parameter.adjustable))
            config.set(section_name, 'min', str(parameter.min))
            config.set(section_name, 'max', str(parameter.max))
            if hasattr(parameter, 'scale'):
                config.set(section_name, 'scale', str(parameter.scale))
            else:
                config.set(section_name, 'scale', 'linear')

        config.add_section('Lattice')
        if hasattr(self.layer_list, 'cell'):
            config.set('Lattice', 'cell_size', ' '.join(
                [str(i) for i in self.layer_list.cell.flatten()]))

            if hasattr(self.layer_list, 'default_layer'):
                config.set(
                    'Lattice', 'default_layer', self.layer_list.default_layer)

            if hasattr(self.layer_list, 'substrate_layer'):
                config.set('Lattice',
                           'substrate_layer',
                           self.layer_list.substrate_layer)

        if hasattr(self.layer_list, 'representation'):
            config.set('Lattice',
                       'representation',
                       self.layer_list.representation)

        for layer in self.get_layers():
            section_name = 'Layer %s' % layer.name
            config.add_section(section_name)
            config.set(section_name, 'color', layer.color)

            for site in layer.sites:
                config.set(section_name, 'site %s' % site.name,
                           '%s; %s; %s' %
                           (tuple(site.pos),
                            site.default_species,
                            site.tags,
                            ))

        for process in self.get_processes():
            section_name = 'Process %s' % process.name
            config.add_section(section_name)
            config.set(section_name, 'rate_constant', process.rate_constant)
            config.set(section_name, 'otf_rate', str(process.otf_rate))
            config.set(section_name, 'enabled', str(process.enabled))
            if process.bystander_list:
                bystanders = [bystander._shorthand()
                              for bystander in process.bystander_list]
                print(process.name)
                print(bystanders)
                config.set(section_name, 'bystanders', ' + '.join(bystanders))
            if process.tof_count:
                config.set(section_name, 'tof_count', str(process.tof_count))
            conditions = [condition._shorthand()
                          for condition in process.condition_list]
            config.set(section_name, 'conditions',
                       ' + '.join(conditions))

            actions = [action._shorthand() for action in process.action_list]
            config.set(section_name, 'actions',
                       ' + '.join(actions))

        f = StringIO()
        config.write(f)

        return f.getvalue()

    def _get_etree_xml(self):
        """Produces an ElemenTree object
        representing the Project"""
        # build XML Tree
        root = ET.Element('kmc')
        root.set('version', str(xml_api_version))
        meta = ET.SubElement(root, 'meta')
        if hasattr(self.meta, 'author'):
            meta.set('author', self.meta.author)
        if hasattr(self.meta, 'email'):
            meta.set('email', self.meta.email)
        if hasattr(self.meta, 'model_name'):
            meta.set('model_name', self.meta.model_name)
        if hasattr(self.meta, 'model_dimension'):
            meta.set('model_dimension', str(self.meta.model_dimension))
        if hasattr(self.meta, 'debug'):
            meta.set('debug', str(self.meta.debug))
        species_list = ET.SubElement(root, 'species_list')
        if hasattr(self.species_list, 'default_species'):
            species_list.set('default_species',
                             self.species_list.default_species)
        else:
            species_list.set('default_species', '')

        for species in self.get_speciess():
            species_elem = ET.SubElement(species_list, 'species')
            species_elem.set('name', species.name)
            if hasattr(species, 'representation'):
                species_elem.set('representation', species.representation)
            if hasattr(species, 'color'):
                species_elem.set('color', species.color)
            species_elem.set('tags', getattr(species, 'tags'))
        parameter_list = ET.SubElement(root, 'parameter_list')
        for parameter in self.get_parameters():
            parameter_elem = ET.SubElement(parameter_list, 'parameter')
            parameter_elem.set('name', parameter.name)
            parameter_elem.set('value', str(parameter.value))
            parameter_elem.set('adjustable', str(parameter.adjustable))
            parameter_elem.set('min', str(parameter.min))
            parameter_elem.set('max', str(parameter.max))
            if hasattr(parameter, 'scale'):
                parameter_elem.set('scale', str(parameter.scale))
            else:
                parameter_elem.set('scale', 'linear')

        lattice_elem = ET.SubElement(root, 'lattice')
        if hasattr(self.layer_list, 'cell'):
            lattice_elem.set('cell_size',
                             ' '.join([str(i)
                                       for i in
                                       self.layer_list.cell.flatten()]))
            if hasattr(self.layer_list, 'default_layer'):
                lattice_elem.set('default_layer',
                                 self.layer_list.default_layer)
            if hasattr(self.layer_list, 'substrate_layer'):
                lattice_elem.set('substrate_layer',
                                 self.layer_list.substrate_layer)
        if hasattr(self.layer_list, 'representation'):
            lattice_elem.set('representation', self.layer_list.representation)
        for layer in self.get_layers():
            layer_elem = ET.SubElement(lattice_elem, 'layer')
            layer_elem.set('name', layer.name)
            layer_elem.set('color', layer.color)

            for site in layer.sites:
                site_elem = ET.SubElement(layer_elem, 'site')
                site_elem.set('pos', '%s %s %s' % tuple(site.pos))
                site_elem.set('type', site.name)
                site_elem.set('tags', site.tags)
                site_elem.set('default_species', site.default_species)

        process_list = ET.SubElement(root, 'process_list')
        for process in self.get_processes():
            process_elem = ET.SubElement(process_list, 'process')
            process_elem.set('rate_constant', process.rate_constant)
            if process.otf_rate:
                process_elem.set('otf_rate', process.otf_rate)
            process_elem.set('name', process.name)
            process_elem.set('enabled', str(process.enabled))
            if process.tof_count:
                process_elem.set('tof_count', str(process.tof_count))
            for condition in process.condition_list:
                condition_elem = ET.SubElement(process_elem, 'condition')
                condition_elem.set('species', condition.species)
                condition_elem.set('coord_layer', condition.coord.layer)
                condition_elem.set('coord_name', condition.coord.name)
                condition_elem.set('coord_offset',
                                   ' '.join([str(i) for i in condition.coord.offset]))
            for action in process.action_list:
                action_elem = ET.SubElement(process_elem, 'action')
                action_elem.set('species', action.species)
                action_elem.set('coord_layer', action.coord.layer)
                action_elem.set('coord_name', action.coord.name)
                action_elem.set('coord_offset',
                                ' '.join([str(i) for i in action.coord.offset]))
            if hasattr(process, 'bystander_list'):
                for bystander in process.bystander_list:
                    bystander_elem = ET.SubElement(process_elem, 'bystander')
                    bystander_elem.set(
                        'allowed_species', ' '.join(bystander.allowed_species))
                    bystander_elem.set('coord_layer', bystander.coord.layer)
                    bystander_elem.set('coord_name', bystander.coord.name)
                    bystander_elem.set('coord_offset',
                                       ' '.join([str(i) for i in bystander.coord.offset]))
                    if bystander.flag:
                        bystander_elem.set('flag', bystander.flag)

        output_list = ET.SubElement(root, 'output_list')
        for output in self.get_outputs():
            if output.output:
                output_elem = ET.SubElement(output_list, 'output')
                output_elem.set('item', output.name)
        return root

    def shorten_names(self, max_length=15):
        if max_length < 5 :
            raise UserWarning("Max variable length has to be at least 5.")
        if max_length < 0 :
            max_length > 9999

        import pprint
        digits = 4
        abbreviation_map = {}
        fullform_map = {}
        stub_map = {}

        for process in self.process_list:
            if len(process.name) > max_length - digits:
                long_name = process.name
                stub = process.name[:max_length - digits]
                short_number = len(stub_map.get(stub, []))
                short_name = '{}{:04d}'.format(stub, short_number)
                stub_map.setdefault(stub, []).append((short_name, long_name))
                abbreviation_map[short_name] = long_name
                fullform_map[long_name] = short_name

                process.name = short_name

        with open('abbreviations_{}.dat'.format(self.meta.model_name), 'w') as outfile:
            outfile.write(pprint.pformat(stub_map))

    def clear_model(self, model_name='', backend=''):
        if backend=='': backend = self.backend
        if model_name=='': model_name = self.model_name
        import kmcos.io
        kmcos.io.clear_model(model_name, backend=backend)
    
    def save_model(self, filename="", validate=True):
        self.model_name = self.meta.model_name
        #If the user provides a filename, save_model will use that. Otherwise, save_model will create a default filename with the model_name
        if len(filename) == 0:
            self.filename = self.model_name + ".xml"
            filename = self.filename
        else:
            self.filename = filename
        #The logic depends on whether the filename type is an xml or ini
        if self.filename.endswith('.xml'):
            self.export_xml_file(self.filename, validate=validate)
        elif filename.endswith('.ini'):
            with open(self.filename, 'w') as outfile:
                outfile.write(self._get_ini_string())
        else:
            raise UserWarning('Cannot export to file suffix %s' %
                              os.path.splitext(self.filename)[-1])

        #If there are errors with the model object, then write the list of errors to a .log file
        if len(self.error_list) > 0:
            np.savetxt(self.model_name+"__build.log", self.error_list, delimiter=", ", fmt="%s", header = "Type, Name, Message")


    def save(self, filename="", validate=True):
        self.save_model(filename, validate)
        

    def export_xml_file(self, filename, validate=True):
        f = open(filename, 'w')
        f.write(str(self))
        f.close()

        if validate:
            self.validate_model()

    def import_file(self, filename):
        if filename.endswith('.ini'):
            self.import_ini_file(filename)
        elif filename.endswith('.xml'):
            self.import_xml_file(filename)

        else:
            raise UserWarning(
                'Don\'t know what to do with this file ending %s' % filename)

        self.filename = filename

    def import_ini_file(self, filename):
        try:
            from ConfigParser import ConfigParser
        except ImportError:
            from configparser import ConfigParser
        from kmcos.utils import evaluate_template
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO 
        config = ConfigParser()
        config.optionxform = str
        if type(filename) is str:
            with open(filename) as infile:
                inputtxt = infile.read()
        else:
            inputtxt = filename.read()

        infile = StringIO()
        infile.write(evaluate_template(inputtxt, escape_python=True, pt=self))
        infile.seek(0)
        config.read_file(infile) #Changed 10/31/20 to replace readfp https://docs.python.org/3/library/configparser.html

        for section in config.sections():
            if section == 'Lattice':
                options = config.options(section)
                for option in options:
                    value = config.get(section, option)
                    if option == 'cell_size':
                        cell = np.array([float(i)
                                         for i in
                                         value.split()])
                        if len(cell) == 3:
                            self.layer_list.cell = np.diag(cell)
                        elif len(cell) == 9:
                            self.layer_list.cell = cell.reshape(3, 3)
                        else:
                            raise UserWarning('%s not understood' % cell)
                    elif option == 'default_layer':
                        self.layer_list.default_layer = value
                if 'default_layer' in options:
                    self.layer_list.default_layer = config.get(
                        section, 'default_layer')

                if 'substrate_layer' in options:
                    self.layer_list.substrate_layer = config.get(
                        section, 'substrate_layer')

                if 'representation' in options:
                    self.layer_list.representation = config.get(
                        section, 'representation')

            elif section.startswith('Layer '):
                options = config.options(section)
                layer_name = section.split()[-1]
                if 'color' in options:
                    layer = self.add_layer(Layer(name=layer_name,
                                                 color=config.get(section, 'color')))
                else:
                    layer = self.add_layer(Layer(name=layer_name))

                if not hasattr(self.layer_list, 'default_layer'):
                    self.layer_list.default_layer = layer_name
                if not hasattr(self.layer_list, 'substrate_layer'):
                    self.layer_list.substrate_layer = layer_name

                for option in options:
                    if option.startswith('site'):
                        name = option.split()[-1]
                        pos_line = config.get(section, option).split(';')
                        if len(pos_line) == 3:
                            pos, default_species, tags = pos_line
                            pos = tuple(eval(pos))
                            site = Site(name=name.strip(),
                                        pos=pos,
                                        default_species=default_species.strip(),
                                        tags=tags.strip())
                        elif len(pos_line) == 2:
                            pos, default_species = pos_line
                            pos = tuple(eval(pos))
                            tags = ''
                            site = Site(name=name.strip(),
                                        pos=pos,
                                        default_species=default_species.strip(),)
                        elif len(pos_line) == 1:
                            pos = tuple(eval(pos_line[0]))

                            if hasattr(self.species_list, 'default_species'):
                                default_species = self.species_list.default_species
                                site = Site(name=name.strip(),
                                            pos=pos,
                                            default_species=default_species.strip(),)
                            else:
                                site = Site(name=name.strip(),
                                            pos=pos,)

                        layer.sites.append(site)
            elif section == 'Meta':
                options = config.options(section)
                for option in options:
                    value = config.get(section, option)
                    self.meta.add({option: value})
            elif section.startswith('Parameter '):
                options = config.options(section)
                name = section.split()[-1]
                min = config.getfloat(section, 'min') if 'min' in options else 0.
                max = config.getfloat(section, 'max') if 'max' in options else 0.
                value = config.get(section, 'value') if 'value' in options else None
                scale = config.get(section, 'scale') if 'scale' in options else 'linear'
                adjustable = config.getboolean(section, 'adjustable') if 'adjustable' in options else None
                self.add_parameter(Parameter(name=name,
                                             value=value,
                                             min=min,
                                             max=max,
                                             scale=scale,
                                             adjustable=adjustable,))

            elif section.startswith('Process '):
                options = config.options(section)
                name = section.split()[-1]
                rate_constant = config.get(section, 'rate_constant')
                if 'otf_rate' in options:
                    otf_rate = config.get(section, 'otf_rate')
                    if otf_rate.strip() == 'None':
                        otf_rate = None
                else:
                    otf_rate = None

                if 'tof_count' in options:
                    tof_count = config.get(section, 'tof_count')
                    if not tof_count: tof_count = {}
                else:
                    tof_count = None

                if 'enabled' in options:
                    enabled = config.getboolean(section, 'enabled')
                else:
                    enabled = True

                process = self.add_process(Process(name=name,
                                                   rate_constant=rate_constant,
                                                   tof_count=tof_count,
                                                   otf_rate=otf_rate,
                                                   enabled=enabled))

                for action in [x.strip() for x in config.get(section, 'actions').split('+')]:
                    try:
                        species, coord = action.split('@')
                    except:
                        print(action)
                        print(action.split('@'))
                        raise
                    coord = coord.split('.')
                    if len(coord) == 3:
                        name, offset, layer = coord
                        offset = eval(offset)
                    elif len(coord) == 2:
                        name, offset = coord
                        offset = eval(offset)
                        layer = [
                            x.split()[-1] for x in config.sections() if x.startswith('Layer')][0]
                    else:
                        name = coord[0]
                        offset = (0, 0, 0)
                        layer = [
                            x.split()[-1] for x in config.sections() if x.startswith('Layer')][0]

                    process.add_action(Action(
                        species=species,
                        coord=Coord(name=name,
                                    offset=offset,
                                    layer=layer)))

                for condition in [x.strip() for x in config.get(section, 'conditions').split('+')]:
                    species, coord = condition.split('@')
                    coord = coord.split('.')
                    if len(coord) == 3:
                        name, offset, layer = coord
                        offset = eval(offset)
                    elif len(coord) == 2:
                        name, offset = coord
                        offset = eval(offset)
                        layer = [
                            x.split()[-1] for x in config.sections() if x.startswith('Layer')][0]
                    else:
                        name = coord[0]
                        offset = (0, 0, 0)
                        layer = [
                            x.split()[-1] for x in config.sections() if x.startswith('Layer')][0]

                    process.add_condition(Condition(
                        species=species,
                        coord=Coord(name=name,
                                    offset=offset,
                                    layer=layer)))

                if 'bystanders' in config.options(section):
                    for bystander in [x.strip() for x in config.get(section, 'bystanders').split('+')]:
                        allowed_species, coord = bystander.split('@')
                        allowed_species = eval(allowed_species)

                        coord, flag = coord.split('|')
                        coord = coord.split('.')
                        if len(coord) == 3:
                            name, offset, layer = coord
                            offset = eval(offset)
                        elif len(coord) == 2:
                            name, offset = coord
                            offset = eval(offset)
                            layer = [
                                x.split()[-1] for x in config.sections() if x.startswith('Layer')][0]
                        else:
                            name = coord[0]
                            offset = (0, 0, 0)
                            layer = [
                                x.split()[-1] for x in config.sections() if x.startswith('Layer')][0]

                        process.add_bystander(Bystander(
                            allowed_species=allowed_species,
                            flag=flag,
                            coord=Coord(name=name,
                                        offset=offset,
                                        layer=layer)))

            elif section == 'SpeciesList':
                self.species_list.default_species = \
                    config.get(section, 'default_species') \
                    if 'default_species' in config.options(section) \
                    else ''

            elif section.startswith('Species '):
                name = section.split()[-1]
                options = config.options(section)
                color = config.get(section, 'color') \
                    if 'color' in options else ''
                representation = config.get(section, 'representation') \
                    if 'representation' in options else ''
                tags = config.get(section, 'tags') \
                    if 'tags' in options else ''
                self.add_species(Species(name=name,
                                         color=color,
                                         representation=representation,
                                         tags=tags))

    def import_xml_file(self, filename):
        """Takes a filename, validates the content against kmc_project.dtd
        and import all fields into the current project tree
        """
        # TODO: catch XML version first and convert if necessary
        self.filename = filename
        #xmlparser = ET.XMLParser(remove_comments=True)
        #  FIXME : automatic removal of comment not supported in
        # stdlib version of ElementTree

        supported_versions = [(0, 2), (0, 3)]

        xmlparser = ET.XMLParser()
        if os.path.exists(filename):
            try:
                root = ET.parse(filename, parser=xmlparser).getroot()
            except:
                raise Exception(('Could not parse file %s. Are you sure this'
                                 ' is a kmcos project file?\n')
                                % os.path.abspath(filename))
        else:
            raise IOError('File not found: %s' % os.path.abspath(filename))

        if 'version' in root.attrib:
            self.version = eval(root.attrib['version'])
        else:
            self.version = (0, 1)

        if not self.version in supported_versions:
            dtd = ET.DTD(APP_ABS_PATH + kmcproject_v0_1_dtd)
            if not dtd.validate(root):
                print(dtd.error_log.filter_from_errors()[0])
                return
            nroot = ET.Element('kmc')
            nroot.set('version', '0.2')
            raise Exception('No legacy support!')
        else:
            if self.version == (0, 2):
                dtd = ET.DTD(APP_ABS_PATH + kmcproject_v0_2_dtd)
            elif self.version == (0, 3):
                dtd = ET.DTD(APP_ABS_PATH + kmcproject_v0_3_dtd)
            else:
                raise Exception(
                    'xml file version not supported. Is your kmcos too old?')
            if not dtd.validate(root):
                print(dtd.error_log.filter_from_errors()[0])
                return
            for child in root:
                if child.tag == 'lattice':
                    print("READING CELL SIZE")
                    print(child.attrib['cell_size'])
                    cell = np.array([float(i)
                                     for i in
                                     child.attrib['cell_size'].split()])
                    print("CELL")
                    print(cell)
                    if len(cell) == 3:
                        self.layer_list.cell = np.diag(np.array(cell))
                    elif len(cell) == 9:
                        self.layer_list.cell = np.array(cell).reshape(3, 3)
                    else:
                        raise UserWarning('%s not understood' % cell)
                    print("LAYER LIST CELL")
                    print(self.layer_list.cell)
                    self.layer_list.default_layer = \
                        child.attrib['default_layer']
                    if 'substrate_layer' in child.attrib:
                        self.layer_list.substrate_layer = \
                            child.attrib['substrate_layer']
                    else:
                        self.layer_list.substrate_layer = \
                            self.layer_list.default_layer
                    if 'representation' in child.attrib:
                        self.layer_list.representation = \
                            child.attrib['representation']
                    else:
                        self.layer_list.representation = ''

                    for elem in child:
                        if elem.tag == 'layer':
                            name = elem.attrib['name']
                            if 'color' in elem.attrib:
                                color = elem.attrib['color']
                            else:
                                color = '#ffffff'
                            layer = Layer(name=name, color=color)
                            self.add_layer(layer)

                            for site in elem:
                                name = site.attrib['type']
                                pos = site.attrib['pos']
                                if 'tags' in site.attrib:
                                    tags = site.attrib['tags']
                                else:
                                    tags = ''
                                if 'default_species' in site.attrib:
                                    default_species = \
                                        site.attrib['default_species']
                                else:
                                    default_species = 'default_species'
                                site_elem = Site(name=name,
                                                 pos=pos,
                                                 tags=tags,
                                                 default_species=default_species)
                                layer.sites.append(site_elem)
                elif child.tag == 'meta':
                    for attrib in ['author',
                                   'debug',
                                   'email',
                                   'model_dimension',
                                   'model_name']:
                        if attrib in child.attrib:
                            self.meta.add({attrib: child.attrib[attrib]})
                elif child.tag == 'parameter_list':
                    for parameter in child:
                        name = parameter.attrib['name']
                        value = parameter.attrib['value']

                        if 'adjustable' in parameter.attrib:
                            adjustable = bool(eval(
                                              parameter.attrib['adjustable']))
                        else:
                            adjustable = False

                        min = float(parameter.attrib['min']) \
                            if 'min' in parameter.attrib else 0.0
                        max = float(parameter.attrib['max']) \
                            if 'max' in parameter.attrib else 0.0
                        scale = parameter.attrib['scale'] \
                            if 'scale' in parameter.attrib else 'linear'

                        parameter_elem = Parameter(name=name,
                                                   value=value,
                                                   adjustable=adjustable,
                                                   min=min,
                                                   max=max,
                                                   scale=scale)
                        self.add_parameter(parameter_elem)
                elif child.tag == 'process_list':
                    for process in child:
                        name = process.attrib['name']
                        rate_constant = process.attrib['rate_constant']
                        if 'tof_count' in process.attrib:
                            tof_count = process.attrib['tof_count']
                        else:
                            tof_count = None
                        if 'otf_rate' in process.attrib:
                            otf_rate = process.attrib['otf_rate']
                        else:
                            otf_rate = None
                        if 'enabled' in process.attrib:
                            try:
                                proc_enabled = bool(
                                    eval(process.attrib['enabled']))
                            except:
                                proc_enabled = True
                        else:
                            proc_enabled = True
                        process_elem = Process(name=name,
                                               rate_constant=rate_constant,
                                               enabled=proc_enabled,
                                               tof_count=tof_count,
                                               otf_rate=otf_rate)
                        for sub in process:
                            # if sub.tag == 'action' or sub.tag == 'condition':
                            if sub.tag in ['action', 'condition', 'bystander']:
                                coord_layer = sub.attrib['coord_layer']
                                coord_name = sub.attrib['coord_name']
                                coord_offset = tuple(
                                    [int(i) for i in
                                     sub.attrib['coord_offset'].split()])
                                coord = Coord(layer=coord_layer,
                                              name=coord_name,
                                              offset=coord_offset,
                                              )
                                if sub.tag == 'bystander':
                                    allowed_species = sub.attrib[
                                        'allowed_species'].split()
                                    if 'flag' in sub.attrib:
                                        flag = sub.attrib['flag']
                                        byst =\
                                            Bystander(allowed_species=allowed_species,
                                                      coord=coord, flag=flag)
                                    else:
                                        byst = Bystander(allowed_species=allowed_species,
                                                         coord=coord)
                                    process_elem.add_bystander(byst)
                                else:
                                    implicit = (
                                        sub.attrib.get('implicit', '') == 'True')
                                    species = sub.attrib['species']
                                    condition_action = \
                                        ConditionAction(species=species,
                                                        coord=coord,
                                                        implicit=implicit)
                                    if sub.tag == 'action':
                                        process_elem.add_action(
                                            condition_action)
                                    elif sub.tag == 'condition':
                                        process_elem.add_condition(
                                            condition_action)
                        self.add_process(process_elem)
                elif child.tag == 'species_list':
                    self.species_list.default_species = \
                        child.attrib['default_species'] \
                        if 'default_species' in child.attrib else ''
                    for species in child:
                        name = species.attrib['name']
                        color = species.attrib['color'] \
                            if 'color' in species.attrib else ''
                        representation = species.attrib['representation'] \
                            if 'representation' in species.attrib else ''
                        tags = species.attrib.get('tags', '')
                        species_elem = Species(name=name,
                                               color=color,
                                               representation=representation,
                                               tags=tags)
                        self.add_species(species_elem)
                if child.tag == 'output_list':
                    for item in child:
                        output_elem = OutputItem(name=item.attrib['item'],
                                                 output=True)
                        self.add_output(output_elem)
#        elif self.version == (0, 3):
#            pass
            # import new XML definition
            # everything tagged and not Output

    def validate_model(self):
        """Run various consistency and completeness
        test of the model to make sure we have a
        minimally complete model.

        """
        # define regular expression
        # for fortran valid fortran
        # variable names
        variable_regex = re.compile('^[a-zA-Z][a-zA-z0-9_]*$')

        #################
        # LATTICE
        #################
        # if at least one layer is defined
        if not len(self.get_layers()) >= 1:
            raise UserWarning('No layer defined.')

        # if a least one site if defined
        if not len([x for layer in self.get_layers()
                    for x in layer.sites]) >= 1:
            raise UserWarning('No site defined.')
        # check if all  lattice sites are unique
        for layer in self.get_layers():
            for x in layer.sites:
                if len([y for y in layer.sites if x.name == y.name]) > 1:
                    raise UserWarning(('Site "%s" in Layer "%s"'
                                       'is not unique.') % (x.name,
                                                            layer.name))

        for x in self.get_layers():
            # check if all lattice names are unique
            if len([y for y in self.get_layers() if x.name == y.name]) > 1:
                raise UserWarning('Layer name "%s" is not unique.' % x.name)

            # check if all lattice have a valid name
            if not variable_regex.match(layer.name):
                raise UserWarning(('Lattice %s is not a valid variable name.\n'
                                   'Only letters, numerals and "_" allowed.\n'
                                   'First character has to be a letter.\n'.format(
                                       layer.name)))

        # check if the default layer is actually defined
        if len(self.get_layers()) > 1 and \
           self.layer_list.default_layer not in [layer.name
                                                 for layer
                                                 in self.get_layers()]:
            raise UserWarning('Default Layer "%s" is not defined.' %
                              self.layer_list.default_layer)

        #################
        # PARAMETERS
        #################
        # check if all parameter names are unique
        for x in self.get_parameters():
            if len([y for y in self.get_parameters()
                    if x.name == y.name]) > 1:
                raise UserWarning(('The parameter "%s" has been defined two'
                                   ' or more times. However each parameter'
                                   ' can be defined only once or the value'
                                   ' cannot be resolved at runtime.') %
                                  x.name)

        #################
        # Species
        #################
        # if at least two species are defined
        if not len(self.get_speciess()) >= 2:
            raise UserWarning('Model has only one species.')

        # if default species is defined
        if self.species_list.default_species not in [x.name
                                                     for x in
                                                     self.get_speciess()]:
            raise UserWarning('Default species "%s" not found.' %
                              self.species_list.default_species)

        for species in self.get_speciess():
            # if species names are valid variable names
            if not variable_regex.match(species.name):
                raise UserWarning(('Species %s is not a valid variable name.\n'
                                   'Only letters, numerals and "_" allowed.\n'
                                   'First character has to be a letter.\n'.format(
                                       species.name)))

        # check if all species have a unique name
        for x in self.get_speciess():
            if [y.name for y in self.get_speciess()].count(x.name) > 1:
                raise UserWarning('Species %s has no unique name!' %
                                  x.name)

        #################
        # PROCESSES
        #################
        # if at least two processes are defined
        if not len(self.get_processes()) >= 2:
            raise UserWarning('Model has less than two processes.')

        # check if all process names are valid
        for x in self.get_processes():
            if not variable_regex.match(x.name):
                raise UserWarning(('Model %s is not a valid variable name.\n'
                                   'Only letters, numerals and "_" allowed.\n'
                                   'First character has to be a letter.\n')
                                  % x.name)

        # check if all process names are unique
        for x in self.get_processes():
            if len([y for y in self.get_processes() if x.name == y.name]) > 1:
                raise UserWarning('Process name "%s" is not unique' % x.name)

        # check if all processes have at least one condition
        for x in self.get_processes():
            if not x.condition_list:
                raise UserWarning('Process "%s" has no conditions!' % x.name)

        # check if all processes have at least one action
        for x in self.get_processes():
            if not x.action_list:
                raise UserWarning('Process %s has no action!' % x.name)

        # check if conditions for each process are unique
        for process in self.get_processes():
            for x in process.condition_list:
                if len([y for y in process.condition_list if x == y]) > 1:
                    raise UserWarning('%s of process %s is not unique!\n\n%s' %
                                      (x, process.name, process))
        # check if actions for each process are unique
        for process in self.get_processes():
            for x in process.action_list:
                if len([y for y in process.action_list if x == y]) > 1:
                    raise UserWarning('%s of process %s is not unique!' %
                                      (x, process.name))

        # check if bystanders for each process are unique and
        # do not coincide with conditions or actions
        for process in self.get_processes():
            for x in process.bystander_list:
                if len([y for y in process.bystander_list
                        if x.coord == y.coord]) > 1:
                    raise UserWarning(('Found more than one bystander for %s\n'
                                       % x.coord) +
                                      ('on process %s' % process.name))
                if len([y for y in process.condition_list if x.coord == y.coord]) > 0:
                    raise UserWarning('Process %s has both a condition and a bystander\n'
                                      'on %s!' % (process.name, x.coord))
                if len([y for y in process.action_list if x.coord == y.coord]) > 0:
                    raise UserWarning('Process %s has an action and a bystander\n on %s!' %
                                      (process.name, x.coord))

        # check if all processes have a rate expression
        for x in self.get_processes():
            if not x.rate_constant:
                raise UserWarning('Process %s has no rate constant defined')

        # check if all rate expressions are valid
        # check if all species used in condition_action are defined
        # after stripping ^ and $ operators
        # check if all species used in bystander are defined
        species_names = [x.name for x in self.get_speciess()]
        for x in self.get_processes():
            for y in x.condition_list + x.action_list:
                stripped_speciess = y.species.replace('$', '').replace('^', '')
                stripped_speciess = [x.strip() for x in stripped_speciess.split(' or ')]

                for stripped_species in stripped_speciess:
                    if not stripped_species in species_names:
                        raise UserWarning(('Species %s used by %s in process %s'
                                           'is not defined') %
                                          (y.species, y, x.name))
            if hasattr(x, 'bystander_list'):
                for y in x.bystander_list:
                    stripped_speciess = [
                        species.replace('$', '').replace('^', '').strip()
                        for species in y.allowed_species]
                    for stripped_species in stripped_speciess:
                        if not stripped_species in species_names:
                            raise UserWarning(
                                ('Species %s used by %s\n'
                                 ' in process %s is not defined') %
                                (stripped_species, y, x.name))

        # check if all sites in processes are defined: actions, conditions
        return True

    def print_statistics(self):
        get_name = lambda x: '_'.join(x.name.split('_')[:-1])
        ml = len(self.get_layers()) > 1
        print('Statistics\n=============')
        print('Parameters: %s' % len(self.get_parameters()))
        print('Species: %s' % len(self.get_speciess()))
        print('Sites: %s' % sum([len(layer.sites)
                                 for layer in self.layer_list]))

        names = [get_name(x) for x in self.get_processes()]
        names = list(set(names))
        nrates = len(set([x.rate_constant for x in self.get_processes()]))
        print('Processes (%s/%s/%s)\n-------------' %
              (len(names), nrates, len(self.get_processes())))

        for process_type in sorted(names):
            nprocs = len([x for x in self.get_processes()
                          if get_name(x) == process_type])
            if ml:
                layer = process_type.split('_')[0]
                pname = '_'.join(process_type.split('_')[1:])
                print('\t- [%s] %s : %s' % (layer, pname, nprocs))

            else:
                print('\t- %s : %s' % (process_type, nprocs))

    def compile_model(self, code_generator='local_smart'):
        from tempfile import mkdtemp
        import os
        import shutil
        from kmcos.utils import build
        from kmcos.cli import get_options
        from kmcos.io import export_source
        cwd = os.path.abspath(os.curdir)
        dir = mkdtemp()
        export_source(self, dir, code_generator=code_generator)
        os.chdir(dir)

        options, args = get_options()
        build(options)
        from kmcos.run import KMC_Model
        model = KMC_Model(print_rates=False, banner=False)
        os.chdir(cwd)
        shutil.rmtree(dir)
        return model

    def set_meta(self,
            author=None,
            email=None,
            model_name=None,
            model_dimension=None,
            debug=None):
        if type(author) != type(None):
            self.meta.author = str(author)
            self.author = str(author)
        if type(email) != type(None):
            self.meta.email = str(email)
            self.email = str(email)
        if type(model_name) != type(None):
            self.meta.model_name = str(model_name)
            self.model_name = str(model_name)
            self.filename = str(model_name) + ".xml"
        if type(model_dimension) != type(None):
            self.meta.model_dimension = int(model_dimension)
            self.model_dimension = int(model_dimension)
        if type(debug) != type(None):
            self.meta.debug = str(debug)
            self.debug = str(debug)


def create_kmc_model(model_name=None): #Creates a project, which is the kmc model, object with an optional argument for model name.
    if type(model_name) == type(None):
        pt = Project()
    else:
        pt = Project(model_name)
    return pt


class Meta(object):

    """Class holding the meta-information about the kMC project
    """
    name = 'Meta'

    def __init__(self, *args, **kwargs):
        self.add(kwargs)
        self.debug = kwargs.get('debug', 0)

    def add(self, attrib):
        for key in attrib:
            if key in ['debug', 'model_dimension']:
                self.__setattr__(key, int(attrib[key]))
            else:
                self.__setattr__(key, attrib[key])

    def setattribute(self, attr, value):
        if attr in ['author', 'email', 'debug',
                    'model_name', 'model_dimension']:
            self.add({attr: value})

        else:
            print('%s is not a known meta information')

    def get_extra(self):
        return "%s(%s)" % (self.model_name, self.model_dimension)


class ParameterList(FixedObject, list):

    """A list of parameters
    """
    attributes = ['name']

    def __call__(self, match):
        return [x for x in self if fnmatch(x.name, match)]

    def __init__(self, **kwargs):
        self.name = 'Parameters'


class Parameter(FixedObject, CorrectlyNamed):

    """A parameter that can be used in a rate constant expression
    and defined via some init file.

    :param name: The name of the parameter.
    :type name: str
    :param adjustable: Create controller in GUI.
    :type adjustable: bool
    :param min: Minimum value for controller.
    :type min: float
    :param max: Maximum value for controller.
    :type max: float
    :param scale: Controller scale: 'log' or 'lin'
    :type scale: str

    """
    attributes = ['name', 'value', 'adjustable', 'min', 'max', 'scale']

    def __init__(self, **kwargs):
        FixedObject.__init__(self, **kwargs)
        self.name = kwargs.get('name', '')
        self.adjustable = kwargs.get('adjustable', False)
        self.value = kwargs.get('value', 0.)
        self.min = kwargs.get('min', 0.)
        self.max = kwargs.get('max', 0.)
        self.scale = kwargs.get('scale', 'linear')

    def __repr__(self):
        return '[PARAMETER] Name: %s Value: %s\n' % (self.name, self.value)

    def on_adjustable__do_toggled(self, value):
        print(value)

    def on_name__content_changed(self, _):
        self.project_tree.update(self.process)

    def get_info(self):
        return self.value


class LayerList(FixedObject, list):

    """A list of layers

    :param cell: Size of unit-cell.
    :type cell: np.array (3x3)
    :param default_layer: name of default layer.
    :type default_layer: str.

    """
    attributes = ['cell',
                  'default_layer',
                  'name',
                  'representation',
                  'substrate_layer']

    def __init__(self, **kwargs):
        FixedObject.__init__(self, **kwargs)
        self.name = 'Lattice(s)'
        if 'cell' in kwargs:
            if type(kwargs['cell']) is str:
                kwargs['cell'] = np.array([float(i)
                                           for i in kwargs['cell'].split()])
            if type(kwargs['cell']) is np.ndarray:
                if len(kwargs['cell']) == 9:
                    self.cell = kwargs['cell'].resize(3, 3)
                elif len(kwargs['cell']) == 3:
                    self.cell = np.diag(kwargs['cell'])
            else:
                raise UserWarning('%s not understood' % kwargs['cell'])
        else:
            self.cell = np.identity(3)
        self.representation = kwargs.get('representation', '')

    def set_representation(self, images):
        """FIXME: If there is more than one representation they should be
        sorted by their name!!!"""
        import ase.atoms
        from kmcos.utils import get_ase_constructor

        if type(images) is list:
            repr = '['
            for atoms in images:
                repr += '%s, ' % get_ase_constructor(atoms)
            repr += ']'
            self.representation = repr
        elif type(images) is str:
            self.representation = images
        elif type(images) is ase.atoms.Atoms:
            self.representation = '[%s]' % get_ase_constructor(images)
        else:
            raise UserWarning("Data type %s of %s not understood." %
                              (type(images), images))

    def __setattr__(self, key, value):
        if key == 'representation':
            if value:
                from kmcos.utils import get_ase_constructor
                from ase.atoms import Atoms
                value = eval(value)
                if (not hasattr(self, 'representation') or
                        not self.representation):
                    try:# if it's a list or a tuple, then take first value.
                        self.cell = value[0].get_cell()
                    except:
                        self.cell = value.get_cell()
                value = '[%s]' % get_ase_constructor(value)
            self.__dict__[key] = '%s' % value
        else:
            self.__dict__[key] = value

    def generate_coord_set(self, size=[1, 1, 1], layer_name='default', site_name=None):
        """Generates a set of coordinates around unit cell of any
        desired size. By default it includes exactly all sites in
        the unit cell. By setting size=[2,1,1] one gets an additional
        set in the positive and negative x-direction.
        """

        def drange(n):
            return list(range(1 - n, n))

        layers = [layer for layer in self if layer.name == layer_name]
        if layers:
            layer = layers[0]
        else:
            raise UserWarning('No Layer named %s found.' % layer_name)

        if site_name is not None and not any([re.search(site_name, x) for x in ['_'.join(x.name.split('_')) for x in layer.sites]]):
            raise UserWarning('Layer {layer_name} has no site matching {site_name}. Please check spelling and try again.')

        if site_name is None:
            return [
                self.generate_coord('%s.(%s, %s, %s).%s' % (site.name, i, j, k,
                                                            layer_name))
                for i in drange(size[0])
                for j in drange(size[1])
                for k in drange(size[2])
                for site in layer.sites]
        else:
            selected_site_names = [site.name for site in layer.sites if re.search(site_name, '_'.join(site.name.split('_')[:]))]
            return [
                self.generate_coord('%s.(%s, %s, %s).%s' % (site, i, j, k,
                                                            layer_name))
                for i in drange(size[0])
                for j in drange(size[1])
                for k in drange(size[2])
                for site in selected_site_names
            ]

    def generate_coord(self, terms):
        """Expecting something of the form site_name.offset.layer
        and return a Coord object"""

        term = terms.split('.')
        if len(term) == 3:
            coord = Coord(name=term[0],
                          offset=eval(term[1]),
                          layer=term[2])
        elif len(term) == 2:
            coord = Coord(name=term[0],
                          offset=eval(term[1]),
                          layer=self.default_layer)
        elif len(term) == 1:
            coord = Coord(name=term[0],
                          offset=(0, 0, 0),
                          layer=self.default_layer)
        else:
            raise UserWarning("Cannot parse coord description")

        offset = np.array(coord.offset)
        cell = self.cell
        layer = list(filter(lambda x: x.name == coord.layer, list(self)))[0] #like layer = [x for x in list(self) if x.name == coord.layer][0]
        sites = [x for x in layer.sites if x.name == coord.name]
        if not sites:
            raise UserWarning('No site names %s in %s found!' %
                              (coord.name, layer.name))
        else:
            site = sites[0]
        pos = site.pos
        coord.pos = np.dot(offset + pos, cell)
        coord.tags = site.tags

        return coord


class Layer(FixedObject, CorrectlyNamed):

    """Represents one layer in a possibly multi-layer geometry.

    :param name: Name of layer.
    :type name: str
    :param sites: Sites associated with this layer (Default: [])
    :type sites: list

    """
    attributes = ['name', 'sites', 'active', 'color']

    def __init__(self, **kwargs):
        FixedObject.__init__(self, **kwargs)
        self.name = kwargs.get('name', '')
        self.active = kwargs.get('active', True)
        self.color = kwargs.get('color', '#ffffff')
        self.sites = kwargs.get('sites', [])

    def __repr__(self):
        return "[LAYER] %s\n[\n%s\n]" % (self.name, self.sites)

    def add_site(self, *sites, **kwargs):
        """Adds a new site to a layer.
        """
        for site in sites:
            self.sites.append(site)

        if kwargs:
            site = Site(**kwargs)
            self.sites.append(site)

    def get_site(self, site_name):
        sites = [site for site in self.sites if site.name == site_name]
        if not sites:
            raise Exception('Site not found')
        return sites[0]

    def get_info(self):
        if self.active:
            return 'visible'
        else:
            return 'invisible'


class Site(FixedObject):

    """Represents one lattice site.

    :param name: Name of site.
    :type name: str
    :param pos: Position within unit cell.
    :type pos: np.array or str
    :param tags: Tags for this site (space separated).
    :type tags: str
    :param default_species: Initial population for this site.
    :type default_species: str

    """
    attributes = ['name', 'pos', 'tags', 'default_species']
    # pos is now a list of floats for the graphical representation

    def __init__(self, **kwargs):
        FixedObject.__init__(self, **kwargs)
        self.tags = kwargs.get('tags', '')
        self.name = kwargs.get('name', '')
        self.default_species = kwargs.get('default_species', 'default_species')
        if 'pos' in kwargs:
            if type(kwargs['pos']) is str:
                self.pos = np.array([float(i) for i in kwargs['pos'].split()])
            elif type(kwargs['pos']) in [np.ndarray, tuple, list]:
                self.pos = np.array(kwargs['pos'])
            else:
                raise Exception('Input %s not understood!' % kwargs['pos'])
        else:
            self.pos = np.array([0., 0., 0.])

    def __repr__(self):
        return '[SITE] {0:12s} ({1:5s}) {2:s} {3:s}'.format(self.name,
                                                            self.default_species,
                                                            self.pos,
                                                            self.tags)


class ProcessFormSite(Site):

    """This is just a little varient of the site object,
    with the sole difference that it has a layer attribute
    and is meant to be used in the process form. This separation was chosen,
    since the Site object as in the Project should not have a layer
    attribute to avoid data duplication but in the ProcessForm we need this
    to define processes
    """
    attributes = Site.attributes
    attributes.append('layer')
    attributes.append('color')

    def __init__(self, **kwargs):
        Site.__init__(self, **kwargs)
        self.layer = kwargs.get('layer', '')


class Coord(FixedObject):

    """Class that holds exactly one coordinate as used in the description
    of a process. The distinction between a Coord and a Site may seem
    superfluous but it is made to avoid data duplication.

    :param name: Name of coordinate.
    :type name: str
    :param offset: Offset in term of unit-cells.
    :type offset: np.array or list
    :param layer: Name of layer.
    :type layer: str
    :param tags: List of tags (space separated string).
    :type tags: str

    .. attribute:: pos

       pos is np.array((3, 1)) and is calculated from offset and position. Not to be set manually.

    """
    attributes = ['offset', 'name', 'layer', 'pos', 'tags']

    def __init__(self, **kwargs):
        FixedObject.__init__(self, **kwargs)
        self.offset = kwargs.get('offset', np.array([0, 0, 0]))
        if len(self.offset) == 1:
            self.offset = np.array([self.offset[0], 0, 0])
        elif len(self.offset) == 2:
            self.offset = np.array([self.offset[0], self.offset[1], 0])
        elif len(self.offset) == 3:
            self.offset = np.array([self.offset[0],
                                    self.offset[1],
                                    self.offset[2]])

        self.pos = np.array([float(i) for i in kwargs['pos'].split()]) \
            if 'pos' in kwargs else np.array([0., 0., 0.])

        self.tags = kwargs.get('tags', '')

    def __repr__(self):
        return '[COORD] %s.%s.%s' % (self.name,
                                     tuple(self.offset),
                                     self.layer)

    def _get_genstring(self):
        return '%s.%s.%s' % (self.name,
                             tuple(self.offset),
                             self.layer)

    def eq_mod_offset(self, other):
        """Compares wether to coordinates are the same up to (modulo)
        a cell offset.
        """
        return (self.layer, self.name) == (other.layer, other.name)

    def __eq__(self, other):
        return ((self.layer, self.name) ==
                (other.layer, other.name)) and (self.offset == other.offset).all()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return ((self.layer,
                 self.name,
                 self.offset[0],
                 self.offset[1],
                 self.offset[2]) <
                (other.layer,
                 other.name,
                 other.offset[0],
                 other.offset[1],
                 other.offset[2]))

    def __le__(self, other):
        return any(self == other, self < other)

    def __gt__(self, other):
        return ((self.layer,
                 self.name,
                 self.offset[0],
                 self.offset[1],
                 self.offset[2]) >
                (other.layer,
                 other.name,
                 other.offset[0],
                 other.offset[1],
                 other.offset[2]))

    def __ge__(self, other):
        return any(self == other, self < other)


    def __hash__(self):
        return hash(self.__repr__())

    def __sub__(a, b):
        """When subtracting two lattice coordinates from each other,
        i.e. a-b, we want to keep the name and layer from a, and just
        take the difference in supercells
        """
        offset = [(x - y) for (x, y) in zip(a.offset, b.offset)]
        if a.layer:
            a_name = '%s_%s' % (a.layer, a.name)
        else:
            a_name = a.name

        if b.layer:
            b_name = '%s_%s' % (b.layer, b.name)
        else:
            b_name = b.name

        if a_name == b_name:
            name = '0'
        else:
            name = '%s - %s' % (a_name, b_name)
        layer = ''
        return Coord(name=name, layer=layer, offset=offset)

    def rsub_ff(self):
        """Build term as if subtracting on the right, omit '-' if 0 anyway
        (in Fortran Form :-)
        """
        ff = self.ff()
        if ff == '(/0, 0, 0, 0/)':
            return ''
        else:
            return ' - %s' % ff

    def site_offset_unpacked(self):
        ff = self.ff()
        if ff == '(/0, 0, 0, 0/)':
            return 'site(1), site(2), site(3), site(4)'
        else:
            return 'site(1) + (%s), site(2) + (%s), site(3) + (%s), site(4) + (%s)' % \
                (self.offset[0], self.offset[1], self.offset[2], self.name)

    def radd_ff(self):
        """Build term as if adding on the right, omit '+' if 0 anyway
        (in Fortran Form :-)
        """
        ff = self.ff()
        if ff == '(/0, 0, 0, 0/)':
            return ''
        else:
            return ' + %s' % ff

    def sort_key(self):
        return "%s_%s_%s_%s_%s" % (self.layer,
                                   self.name,
                                   self.offset[0],
                                   self.offset[1],
                                   self.offset[2])

    def ff(self):
        """ff like 'Fortran Form'"""
        if self.layer:
            return "(/%s, %s, %s, %s_%s/)" % (self.offset[0], self.offset[1],
                                              self.offset[2], self.layer,
                                              self.name,)
        else:
            return "(/%s, %s, %s, %s/)" % (self.offset[0], self.offset[1],
                                           self.offset[2], self.name, )


def cmp_coords(self, other):
    #NB maybe there's a cleaner/faster way of replicating old cmp behavior
    if self.layer != other.layer:
        return (-1 if self.layer < other.layer else 1)
    elif (self.offset != other.offset).any():
        for i in range(3):
            if self.offset[i] != other.offset[i]:
                return (-1 if self.offset[i] < other.offset[i] else 1)
    else:
        return 0


class Species(FixedObject):

    """Class that represent a species such as oxygen, empty, ... .
    Note: `empty` is treated just like a species.

    :param name: Name of species.
    :type name: str
    :param color: Color of species in editor GUI (#ffffff hex-type specification).
    :type color: str
    :param representation: ase.atoms.Atoms constructor describing species geometry.
    :type representation: str
    :param tags: Tags of species (space separated string).
    :type tags: str

    """
    attributes = ['name', 'color', 'representation', 'tags']

    def __init__(self, **kwargs):
        FixedObject.__init__(self, **kwargs)
        self.name = kwargs.get('name', '')
        self.representation = kwargs.get('representation', '')
        self.tags = kwargs.get('tags', '')

    def __repr__(self):
        if hasattr(self, 'color'):
            return '[SPECIES] Name: %s Color: %s\n' % (self.name, self.color)
        else:
            return '[SPECIES] Name: %s Color: no color set.\n' % (self.name)


class SpeciesList(FixedObject, list):

    """A list of species
    """
    attributes = ['default_species', 'name']

    def __call__(self, match):
        return [x for x in self if fnmatch(x.name, match)]

    def __init__(self, **kwargs):
        kwargs['name'] = 'Species'
        FixedObject.__init__(self, **kwargs)


class ProcessList(FixedObject, list):

    """A list of processes
    """
    attributes = ['name']

    def __call__(self, match):
        return [x for x in self if fnmatch(x.name, match)]

    def __init__(self, **kwargs):
        self.name = 'Processes'

    def __lt__(self, other):
        return self.name < other.name


class Process(FixedObject):

    """One process in a kMC process list

    :param name: Name of process.
    :type name: str
    :param rate_constant: Expression for rate constant.
    :type rate_constant: str
    :param otf_rate: Expression used to calculate rate on the fly using bystander's configuration, otf backend only!.
    :type otf_rate: str
    :param condition_list: List of conditions (class Condition).
    :type condition_list: list.
    :param action_list: List of conditions (class Action).
    :type action_list: list.
    :param bystander_list: List of bystanders (class Bystander), otf backend only!.
    :type bystander_list: list.
    :param enabled: Switch this process on or of.
    :type enabled: bool.
    :param chemical_expression: Chemical expression (i.e: A@site1 + B@site2 -> empty@site1 + AB@site2) to generate process from.
    :type chemical_expression: str.
    :param tof_count: Stoichiometric factor for observable products {'NH3': 1, 'H2Ogas': 2}. Hint: avoid space in keys.
    :type tof_count: dict.

    """
    attributes = ['name',
                  'rate_constant',
                  'otf_rate',
                  'condition_list',
                  'action_list',
                  'bystander_list',
                  'enabled',
                  'chemical_expression',
                  'tof_count']

    def __init__(self, **kwargs):
        FixedObject.__init__(self, **kwargs)
        self.name = kwargs.get('name', '')
        self.rate_constant = kwargs.get('rate_constant', '0.')
        self.otf_rate = kwargs.get('otf_rate', None)
        self.condition_list = kwargs.get('condition_list', [])
        self.action_list = kwargs.get('action_list', [])
        self.bystander_list = kwargs.get('bystander_list', [])
        self.tof_count = kwargs.get('tof_count', None)
        self.enabled = kwargs.get('enabled', True)
    
    #TODO: Change "Rate" below to Transition_Frequency if doing so does not break anything.
    def __repr__(self):
        repr_str = ('[PROCESS] Name:%s\n'
                    '     Rate: %s\n'
                    'Conditions: %s\n'
                    'Actions: %s') \
            % (self.name, self.rate_constant,
               self.condition_list, self.action_list,)
        if self.bystander_list:
            repr_str += '\nBystanders: %s' % self.bystander_list
        return repr_str

    def add_condition(self, condition):
        """Adds a conditions to a process"""
        self.condition_list.append(condition)

    def add_action(self, action):
        """Adds an action to a process"""
        self.action_list.append(action)

    def add_bystander(self, bystander):
        """Adds a bystander to a process"""
        self.bystander_list.append(bystander)

    def executing_coord(self):
        return sorted(self.action_list,
                      key=lambda action: action.coord.sort_key())[0].coord

    def get_info(self):
        return self.rate_constant

    def _get_max_d(self):
        max_d = 0
        for condition in self.condition_list + self.action_list + self.bystander_list :
            d = max(np.abs(condition.coord.offset))
            if d > max_d:
                max_d = d
        return max_d

    def evaluate_rate_expression(self, parameters={}):
        import kmcos.evaluate_rate_expression
        return kmcos.evaluate_rate_expression(self.rate_constant, parameters)


class SingleLatIntProcess(Process):

    """A process that corresponds to a single lateral interaction
    configuration. This is conceptually the same as the old
    condition/action model, just some conditions are now called
    bystanders."""
    attributes = ['name',
                  'rate_constant',
                  'condition_list',
                  'action_list',
                  'bystanders',
                  'enabled',
                  'chemical_expression',
                  'tof_count']

    def __init__(self, **kwargs):
        FixedObject.__init__(self, **kwargs)
        self.name = kwargs.get('name', '')
        self.rate_constant = kwargs.get('rate_constant', '0.')
        self.condition_list = kwargs.get('condition_list', [])
        self.action_list = kwargs.get('action_list', [])
        self.tof_count = kwargs.get('tof_count', None)
        self.enabled = kwargs.get('enabled', True)

    def __repr__(self):
        return ('[PROCESS] Name:%s Rate: %s\n'
                'Conditions: %s\n'
                'Actions: %s\n'
                'Bystanders: %s') \
            % (self.name,
               self.rate_constant,
               self.condition_list,
               self.action_list,
               self.bystanders)


class LatIntProcess(Process):

    """A process which directly includes lateral interactions.
    In this model a bystander just defines a set of allowed
    species so, it allows for additional degrees of freedom
    here. Different lateral model can be accounted for through
    counters and placeholder in rate expression.

    """
    attributes = ['name',
                  'rate_constant',
                  'condition_list',
                  'action_list',
                  'bystanders',
                  'enabled',
                  'chemical_expression',
                  'tof_count']


class Bystander(FixedObject):
    attributes = ['coord', 'allowed_species', 'flag']

    def __init__(self, **kwargs):
        kwargs['flag'] = kwargs.get('flag', '')
        FixedObject.__init__(self, **kwargs)

    def __repr__(self):
        return ("[BYSTANDER] Coord:%s Allowed species: (%s)" %
                (self.coord, ','.join([spec for spec in self.allowed_species])))

    def _shorthand(self):
        if self.coord.offset.any():
            return '%s@%s.%s|%s' % (self.allowed_species,
                                    self.coord.name,
                                    tuple(self.coord.offset),
                                    self.flag)
        else:
            return '%s@%s|%s' % (self.allowed_species,
                                 self.coord.name,
                                 self.flag)


class ConditionAction(FixedObject):

    """Represents either a condition or an action. Since both
    have the same attributes we use the same class here, and just
    store them in different lists, depending on its role. For better
    readability one can also use `Condition` or `Action` which are
    just aliases.

    :param coord: Relative Coord (generated by :meth:`LayerList.generate_coord`
                                  or :meth:`Lattice.generate_coord_set`).
    :type coord: Coord
    :param species: Name of species.
    :type species: str

    """
    attributes = ['species', 'coord', 'implicit']

    def __init__(self, **kwargs):
        kwargs['implicit'] = kwargs.get('implicit', False)
        FixedObject.__init__(self, **kwargs)

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return ("[COND_ACT] Species: %s Coord:%s%s\n" %
                (self.species,
                 self.coord,
                 ' (implicit)' if self.implicit else ''))

    def _shorthand(self):
        if self.coord.offset.any():
            return '%s@%s.%s' % (self.species,
                                 self.coord.name,
                                 tuple(self.coord.offset))
        else:
            return '%s@%s' % (self.species,
                              self.coord.name)

    def __hash__(self):
        return hash(self.__repr__())


# Add aliases for ConditionAction
# to make API using code more readable
Condition = ConditionAction
Action = ConditionAction


class OutputList(FixedObject, list):

    """A dummy class, that will hold the values which are to be
    printed to logfile.
    """
    attributes = ['name']

    def __init__(self):
        self.name = 'Output'


class OutputItem(FixedObject):

    """Not implemented yet
    """
    attributes = ['name', 'output']

    def __init__(self, *args, **kwargs):
        FixedObject.__init__(self, **kwargs)


def prettify_xml(elem):
    """This function takes an XML document, which can have one or many lines
    and turns it into a well-breaked, nicely-indented string
    """
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='    ')


def parse_chemical_expression(eq, process, project_tree):
    """Evaluates a chemical expression 'eq' and adds
    conditions and actions accordingly. Rules are:
        - each chemical expression has the form ::

            conditions -> actions

        - each condition or action term has the form (regex) ::

            [$^]*SPECIES@SITE\.OFFSET\.LAYER

        - each SPECIES must have been defined before.
        - each SITE must have been defined before via the
          layer form.
        - an offset in units of units cell can be given as
          tuple such as `'(0, 0)'`
        - a condition or action term containing the default species,
          i.e. by default 'empty' may be omitted. However a term containing
          the omitted site and a species other then the default must exist
          on the opposite side of the expression
        - ^ and $ are special prefixes for the 'creation' and
          'annihilation' of a site, respectively. In case of `$`
           the species can be always omitted. In case of `^` the default
           species may be omitted. Creation and annihilation is only
           needed for lattice reconstructions/multi-lattice models and
           they only stand on the right-hand (i.e. action) side of
           the expression
        - white spaces may be used for readability but have no effect

    Examples ::
        - oxygen@cus -> oxygen@bridge #diffusion
        - co@bridge -> co@cus.(-1,0) # diffusion
        - -> oxygen@cus + oxygen@bridge # adsorption
        - oxygen@cus + co@bridge -> # reaction
    """
    # remove spaces
    eq = re.sub(' ', '', eq)

    # remove comments
    if '#' in eq:
        eq = eq[:eq.find('#')]

    # split at ->
    if eq.count('->') != 1:
        raise Exception('Chemical expression must contain ' +
                            'exactly one "->"\n%s' % eq)
    eq = re.split('->', eq)
    left, right = eq

    # split terms
    left = left.split('+')
    right = right.split('+')

    # Delete term, which contain nothing
    while '' in left:
        left.remove('')
    while '' in right:
        right.remove('')

    # small validity checking
    for term in left + right:
        if term.count('@') != 1:
            raise Exception('Each term needs to contain ' +
                                'exactly one @:\n%s' % term)

    # split each term again at @
    for i, term in enumerate(left):
        left[i] = term.split('@')
    for i, term in enumerate(right):
        right[i] = term.split('@')

    # check if species is defined
    for term in left + right:
        if term[0][0] in ['$', '^'] and term[0][1:]:
            if not [x for x in project_tree.get_speciess() if x.name == term[0][1:]]:
                raise UserWarning('Species %s unknown ' % term[0:])
        elif not [x for x in project_tree.get_speciess() if x.name == term[0]]:
            raise UserWarning('Species %s unknown ' % term[0])

    condition_list = []
    action_list = []

    for i, term in enumerate(left + right):
        # parse coordinate
        coord_term = term[1].split('.')
        if len(coord_term) == 1:
            coord_term.append('(0,0)')

        if len(coord_term) == 2:
            name = coord_term[0]
            active_layers = list(filter(lambda x: x.active,
                                   project_tree.get_layers())) #like [x for x in project_tree.get_layers() if x.active]
            if len(active_layers) == 1:
                layer = active_layers[0].name
            else:  # if more than one active try to guess layer from name
                possible_sites = []
                # if no layer visible choose among all of them
                # else choose among visible
                if not len(active_layers):
                    layers = project_tree.get_layers()
                else:
                    layers = active_layers
                for ilayer in layers:
                    for jsite in ilayer.sites:
                        if jsite.name == name:
                            possible_sites.append((jsite.name, ilayer.name))
                if not possible_sites:
                    raise UserWarning("Site %s not known" % name)
                elif len(possible_sites) == 1:
                    layer = possible_sites[0][1]
                else:
                    raise UserWarning("Site %s is ambiguous because it" +
                                      "exists on the following lattices: %" %
                                      (name, [x[1] for x in possible_sites]))
            coord_term.append(layer)

        if len(coord_term) == 3:
            name = coord_term[0]
            offset = eval(coord_term[1])
            layer = coord_term[2]
            layer_names = [x.name for x in project_tree.get_layers()]
            if layer not in layer_names:
                raise UserWarning("Layer %s not known, must be one of %s"
                                  % (layer, layer_names))
            else:
                layer_instance = list(filter(lambda x: x.name == layer,
                                        project_tree.get_layers()))[0]
                site_names = [x.name for x in layer_instance.sites]
                if name not in site_names:
                    raise UserWarning("Site %s not known, must be one of %s"
                                      % (name, site_names))

        species = term[0]
        coord = Coord(name=name, offset=offset, layer=layer)
        if i < len(left):
            condition_list.append(ConditionAction(species=species,
                                                  coord=coord))
        else:
            action_list.append(ConditionAction(species=species, coord=coord))

    default_species = project_tree.species_list.default_species
    # every condition that does not have a corresponding action on the
    # same coordinate gets complemented with a 'default_species' action
    for condition in condition_list:
        if not [x for x in action_list if x.coord == condition.coord]:
            action_list.append(ConditionAction(species=default_species,
                                               coord=condition.coord))

    # every action that does not have a corresponding condition on
    # the same coordinate gets complemented with a 'default_species'
    # condition
    for action in action_list:
        if not [x for x in condition_list if x.coord == action.coord] \
                and not action.species[0] in ['^', '$']:
            condition_list.append(ConditionAction(species=default_species,
                                                  coord=action.coord))

    # species completion and consistency check for site creation/annihilation
    for action in action_list:
        # for a annihilation the following rules apply:
        #   -  if no species is gives, it will be complemented with the
        #      corresponding species as on the left side.
        #   -  if a species is given, it must be equal to the corresponding
        #      one on the left side. if no corresponding condition is given on
        #      the left side, the condition will be added with the same
        #      species as the annihilated one.
        if action.species[0] == '$':
            corresponding_condition = [x for x in condition_list if x.coord == action.coord]
            if action.species[1:]:
                if not corresponding_condition:
                    condition_list.append(
                        ConditionAction(
                            species=action.species[1:],
                            coord=action.coord))
                else:
                    if corresponding_condition[0].species \
                       != action.species[1:]:
                        raise UserWarning(
                            'When annihilating a site,'
                            ' species must be the same'
                            'for condition\n  and action.\n')
            else:
                if corresponding_condition:
                    action.species = '$%s' % corresponding_condition[0].species
                else:
                    raise UserWarning(
                        'When omitting the species in the site '
                        + 'annihilation, a species must\n'
                        + 'must be given in a corresponding condition.')
        elif action.species == '^':
            raise UserWarning(
                'When creating a site, the species on the new site '
                + 'must be stated.')

    process.condition_list += condition_list
    process.action_list += action_list


def parse_process(string, project_tree):

    name, chem_exp, rate_constant = [x.strip() for x in string.split(';')]
    process = Process(name=name,
                      rate_constant=rate_constant,)
    parse_chemical_expression(chem_exp, process, project_tree)
    return process
