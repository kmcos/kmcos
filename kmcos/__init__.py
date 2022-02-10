"""
Feature overview
================
This paragraph is from __init__.py

With kmcos you can:

    * easily create and modify kMC models through GUI
    * store and exchange kMC models through XML
    * generate fast, platform independent, self-contained code [#code]_
    * run kMC models through GUI or python bindings

kmcos has been developed in the context of first-principles based modelling
of surface chemical reactions but might be of help for other types of
kMC models as well.

kmcos' goal is to significantly reduce the time you need
to implement and run a lattice kmc simulation. However it can not help
you plan the model.

Typical users will run kmcos entirely from python code by following the examples.

In technical terms, kmcos is run  an API via the kmcos python module.

Additionally, though now discouraged, kmcos can be invoked directly from the command line in one of the following
ways::

    kmcos [help] (all|benchmark|build|edit|export|help|import|rebuild|run|settings-export|shell|version|view|xml) [options]


.. rubric:: Footnotes

.. [#code] The source code is generated in Fortran90, written in a modular
            fashion. Python bindings are generated using `f2py  <http://cens.ioc.ee/projects/f2py2e/>`_.
"""
from __future__ import print_function

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


#import kmcos.types
#import kmcos.io

__version__ = "0.0.62"
VERSION = __version__

def evaluate_param_expression(param, parameters={}):
    import tokenize
    import io
    import math
    from kmcos import units

    # convert parameters to dict if passed as list of Parameters()
    if type(parameters) is list:
        param_dict = {}
        for parameter in parameters:
            param_dict[parameter.name] = {'value': parameter.value}
        parameters = param_dict

    parameter_str = str(parameters[param]['value'])

    # replace some aliases
    parameter_str = parameter_str.replace('beta', '(1./(kboltzmann*T))')
    # replace units used in parameters
    for unit in units.keys:
        parameter_str = parameter_str.replace(
                        unit, '%s' % eval('units.%s' % unit))
    try:
        return eval(parameter_str)
    except:
        try:
            replaced_tokens=[]
            input = io.StringIO(parameter_str).readline
            tokens = list(tokenize.generate_tokens(input))
        except:
            raise Exception('Could not tokenize expression: %s' % input)
        for i, token, _, _, _ in tokens:
            if token in ['sqrt', 'exp', 'sin', 'cos', 'pi', 'pow', 'log']:
                replaced_tokens.append((i, 'math.' + token))
            elif token.startswith('GibbsGas_'):
                #evaluate gas phase gibbs free energy using ase thermochemistry module,
                #experimental data from NIST CCCBDB, the electronic energy 
                #and current temperature and partial pressure
                from kmcos import species
                species_name = '_'.join(token.split('_')[1:])
                if species_name in dir(species):
                    if not 'T' in parameters:
                        raise Exception('Need "T" in parameters to evaluate gas phase gibbs free energy.')

                    if not ('p_%s' % species_name) in parameters:
                        raise Exception('Need "p_%s" in parameters to evaluate gas phase gibbs free energy.' % species_name)

                    replaced_tokens.append((i, 'species.%s.GibbsGas(%s,%s,%s)' % (
                                species_name,
                                parameters['E_'+species_name]['value'],
                                parameters['T']['value'],
                                parameters['p_%s' % species_name]['value'],
                                )))
                else:
                    print('No NIST data assigned for %s' % species_name)
                    print('Setting chemical potential to zero')
                    replaced_tokens.append((i, '0'))

                #gibbs=eval(replaced_tokens2[-1][-1])
                #print species_name+': %.3f'%gibbs

            elif token.startswith('GibbsAds_'):
                #evaluate gibbs free energy of adsorbate using ase thermochemistry module,
                #calculated frequencies and electronic energy and current temperature
                from kmcos import species
                species_name = '_'.join(token.split('_')[1:])
                if not 'T' in parameters:
                    raise Exception('Need "T" in parameters to evaluate adsorbate gibbs free energy.')
                energy=parameters['E_'+species_name]['value']
                try:
                    eval(energy)
                except:
                    try:
                        replaced_tokens2=[]
                        input = io.StringIO(energy).readline
                        tokens2 = list(tokenize.generate_tokens(input))
                    except:
                        raise Exception('Could not tokenize expression: %s' % input)
                    for j, token2, _, _, _ in tokens2:
                        if token2 in parameters:
                            parameter_str2 = str(parameters[token2]['value'])
                            try:
                                eval(parameter_str2)
                                replaced_tokens2.append((j, parameter_str2))
                            except:
                                try:
                                    input = io.StringIO(parameter_str2).readline
                                    tokens3 = list(tokenize.generate_tokens(input))
                                except:
                                    raise Exception('Could not tokenize expression: %s' % input)
                                for k, token3, _, _, _ in tokens3:
                                    if token3 in parameters:
                                        parameter_str3 = str(parameters[token3]['value'])
                                        replaced_tokens2.append((k, parameter_str3))
                                    else:
                                        replaced_tokens2.append((k, token3))
                        else:
                            replaced_tokens2.append((j, token2))
                    energy = tokenize.untokenize(replaced_tokens2)
                replaced_tokens.append((i, 'species.GibbsAds(%s,%s,%s)' % (
                            energy,
                            parameters['f_'+species_name]['value'],
                            parameters['T']['value'],
                            )))

                #gibbs=eval(replaced_tokens2[-1][-1])
                #print species_name+': %.3f'%gibbs

            elif token in parameters:
                replaced_tokens.append((i, str(parameters[token]['value'])))
            else:
                replaced_tokens.append((i, token))
        parameter_str = tokenize.untokenize(replaced_tokens)
        return eval(parameter_str)
        #print parameter_str
        #print token+': %.7f'%eval(parameter_str)

rate_aliases = { 'beta' : '(1/(kboltzmann*T))'}

def evaluate_rate_expression(rate_expr, parameters={}):
    """Evaluates an expression for a typical kMC rate constant.
     External parameters can be passed in as dictionary, like the
     following:
        parameters = {'p_CO':{'value':1},
                      'T':{'value':1}}

     or as a list of parameters:
        parameters = [Parameter(), ... ]
     """
    import tokenize
    import io
    import math
    from kmcos import units

    # convert parameters to dict if passed as list of Parameters()
    if type(parameters) is list:
        param_dict = {}
        for parameter in parameters:
            param_dict[parameter.name] = {'value': parameter.value}
        parameters = param_dict

    if not rate_expr:
        rate_const = 0.0
    else:
        replaced_tokens = []

        # replace some aliases
        for old, new in list(rate_aliases.items()):
            rate_expr = rate_expr.replace(old, new)
        try:
            input = io.StringIO(rate_expr).readline
            tokens = list(tokenize.generate_tokens(input))
        except:
            raise Exception('Could not tokenize expression: %s' % input)
        for i, token, _, _, _ in tokens:
            if token in ['sqrt', 'exp', 'sin', 'cos', 'pi', 'pow', 'log']:
                replaced_tokens.append((i, 'math.' + token))
            elif token in dir(units):
                replaced_tokens.append((i, str(eval('units.' + token))))
            elif token.startswith('m_'):
                from ase.symbols import string2symbols
                from ase.data import atomic_masses
                from ase.data import atomic_numbers
                species_name = '_'.join(token.split('_')[1:])
                symbols = string2symbols(species_name)
                replaced_tokens.append((i,
                            '%s' % sum([atomic_masses[atomic_numbers[symbol]]
                            for symbol in symbols])))
            elif token.startswith('mu_'):
                # evaluate gas phase chemical potential if among
                # available JANAF tables if from current temperature
                # and corresponding partial pressure
                from kmcos import species
                species_name = '_'.join(token.split('_')[1:])
                if species_name in dir(species):
                    if not 'T' in parameters:
                        raise Exception('Need "T" in parameters to evaluate chemical potential.')

                    if not ('p_%s' % species_name) in parameters:
                        raise Exception('Need "p_%s" in parameters to evaluate chemical potential.' % species_name)

                    replaced_tokens.append((i, 'species.%s.mu(%s,%s)' % (
                                   species_name,
                                   parameters['T']['value'],
                                   parameters['p_%s' % species_name]['value'],
                                   )))
                else:
                    print('No JANAF table assigned for %s' % species_name)
                    print('Setting chemical potential to zero')
                    replaced_tokens.append((i, '0'))

            elif token.startswith('GibbsGas_'):
                #evaluate gas phase gibbs free energy using ase thermochemistry module,
                #experimental data from NIST CCCBDB, the electronic energy 
                #and current temperature and partial pressure
                from kmcos import species
                species_name = '_'.join(token.split('_')[1:])
                if species_name in dir(species):
                    if not 'T' in parameters:
                        raise Exception('Need "T" in parameters to evaluate gas phase gibbs free energy.')

                    if not ('p_%s' % species_name) in parameters:
                        raise Exception('Need "p_%s" in parameters to evaluate gas phase gibbs free energy.' % species_name)

                    replaced_tokens.append((i, 'species.%s.GibbsGas(%s,%s,%s)' % (
                                   species_name,
                                   parameters['E_'+species_name]['value'],
                                   parameters['T']['value'],
                                   parameters['p_%s' % species_name]['value'],
                                   )))
                else:
                    print('No NIST data assigned for %s' % species_name)
                    print('Setting chemical potential to zero')
                    replaced_tokens.append((i, '0'))

                #gibbs=eval(replaced_tokens[-1][-1])
                #print species_name+': %.3f'%gibbs

            elif token.startswith('GibbsAds_'):
                #evaluate gibbs free energy of adsorbate using ase thermochemistry module,
                #calculated frequencies and electronic energy and current temperature
                from kmcos import species
                species_name = '_'.join(token.split('_')[1:])
                if not 'T' in parameters:
                    raise Exception('Need "T" in parameters to evaluate adsorbate gibbs free energy.')
                energy=parameters['E_'+species_name]['value']
                try:
                    eval(energy)
                except:
                    try:
                        replaced_tokens2=[]
                        input = io.StringIO(energy).readline
                        tokens2 = list(tokenize.generate_tokens(input))
                    except:
                        raise Exception('Could not tokenize expression: %s' % input)
                    for j, token2, _, _, _ in tokens2:
                        if token2 in parameters:
                            parameter_str = str(parameters[token2]['value'])
                            try:
                                eval(parameter_str)
                                replaced_tokens2.append((j, parameter_str))
                            except:
                                try:
                                    input = io.StringIO(parameter_str).readline
                                    tokens3 = list(tokenize.generate_tokens(input))
                                except:
                                    raise Exception('Could not tokenize expression: %s' % input)
                                for k, token3, _, _, _ in tokens3:
                                    if token3 in parameters:
                                        parameter_str = str(parameters[token3]['value'])
                                        replaced_tokens2.append((k, parameter_str))
                                    else:
                                        replaced_tokens2.append((k, token3))
                        else:
                            replaced_tokens2.append((j, token2))
                    energy = tokenize.untokenize(replaced_tokens2)
                replaced_tokens.append((i, 'species.GibbsAds(%s,%s,%s)' % (
                               energy,
                               parameters['f_'+species_name]['value'],
                               parameters['T']['value'],
                               )))

                #gibbs=eval(replaced_tokens[-1][-1])
                #print species_name+': %.3f'%gibbs

            elif token in parameters:
                parameter_str = str(parameters[token]['value'])
                # replace some aliases
                parameter_str = parameter_str.replace('beta', '(1./(kboltzmann*T))')
                # replace units used in parameters
                for unit in units.keys:
                    parameter_str = parameter_str.replace(
                                    unit, '%s' % eval('units.%s' % unit))
                try:
                    eval(parameter_str)
                    replaced_tokens.append((i, parameter_str))
                except:
                    try:
                        replaced_tokens2=[]
                        input = io.StringIO(parameter_str).readline
                        tokens2 = list(tokenize.generate_tokens(input))
                    except:
                        raise Exception('Could not tokenize expression: %s' % input)
                    for i, token2, _, _, _ in tokens2:
                        if token2 in ['sqrt', 'exp', 'sin', 'cos', 'pi', 'pow', 'log']:
                            replaced_tokens2.append((i, 'math.' + token2))
                        elif token2.startswith('GibbsGas_'):
                            #evaluate gas phase gibbs free energy using ase thermochemistry module,
                            #experimental data from NIST CCCBDB, the electronic energy 
                            #and current temperature and partial pressure
                            from kmcos import species
                            species_name = '_'.join(token2.split('_')[1:])
                            if species_name in dir(species):
                                if not 'T' in parameters:
                                    raise Exception('Need "T" in parameters to evaluate gas phase gibbs free energy.')

                                if not ('p_%s' % species_name) in parameters:
                                    raise Exception('Need "p_%s" in parameters to evaluate gas phase gibbs free energy.' % species_name)

                                replaced_tokens2.append((i, 'species.%s.GibbsGas(%s,%s,%s)' % (
                                            species_name,
                                            parameters['E_'+species_name]['value'],
                                            parameters['T']['value'],
                                            parameters['p_%s' % species_name]['value'],
                                            )))
                            else:
                                print('No NIST data assigned for %s' % species_name)
                                print('Setting chemical potential to zero')
                                replaced_tokens2.append((i, '0'))

                            #gibbs=eval(replaced_tokens2[-1][-1])
                            #print species_name+': %.3f'%gibbs

                        elif token2.startswith('GibbsAds_'):
                            #evaluate gibbs free energy of adsorbate using ase thermochemistry module,
                            #calculated frequencies and electronic energy and current temperature
                            from kmcos import species
                            species_name = '_'.join(token2.split('_')[1:])
                            if not 'T' in parameters:
                                raise Exception('Need "T" in parameters to evaluate adsorbate gibbs free energy.')
                            energy=parameters['E_'+species_name]['value']
                            try:
                                eval(energy)
                            except:
                                try:
                                    replaced_tokens3=[]
                                    input = io.StringIO(energy).readline
                                    tokens3 = list(tokenize.generate_tokens(input))
                                except:
                                    raise Exception('Could not tokenize expression: %s' % input)
                                for j, token3, _, _, _ in tokens3:
                                    if token3 in parameters:
                                        parameter_str = str(parameters[token3]['value'])
                                        try:
                                            eval(parameter_str)
                                            replaced_tokens3.append((j, parameter_str))
                                        except:
                                            try:
                                                input = io.StringIO(parameter_str).readline
                                                tokens4 = list(tokenize.generate_tokens(input))
                                            except:
                                                raise Exception('Could not tokenize expression: %s' % input)
                                            for k, token4, _, _, _ in tokens4:
                                                if token4 in parameters:
                                                    parameter_str = str(parameters[token4]['value'])
                                                    replaced_tokens3.append((k, parameter_str))
                                                else:
                                                    replaced_tokens3.append((k, token4))
                                    else:
                                        replaced_tokens3.append((j, token3))
                                energy = tokenize.untokenize(replaced_tokens3)
                            replaced_tokens2.append((i, 'species.GibbsAds(%s,%s,%s)' % (
                                        energy,
                                        parameters['f_'+species_name]['value'],
                                        parameters['T']['value'],
                                        )))

                            #gibbs=eval(replaced_tokens2[-1][-1])
                            #print species_name+': %.3f'%gibbs

                        elif token2 in parameters:
                            replaced_tokens2.append((i, str(parameters[token2]['value'])))
                        else:
                            replaced_tokens2.append((i, token2))
                    parameter_str = tokenize.untokenize(replaced_tokens2)

                    #print parameter_str
                    #print token+': %.7f'%eval(parameter_str)

                    replaced_tokens.append((i, parameter_str))
            else:
                replaced_tokens.append((i, token))

        rate_expr = tokenize.untokenize(replaced_tokens)
        try:
            rate_const = eval(rate_expr)
        except Exception as e:
            raise UserWarning(
            "Could not evaluate rate expression: %s\nException: %s" \
                % (rate_expr, e))

    return rate_const

def compile(kmc_model): #exports the kmc_model.xml file
    import kmcos
    kmcos.export(kmc_model.filename + ' -b' + kmc_model.backend)

def create_kmc_model(model_name = None): #pointer to create_kmc_model in types.py, which creates the kmc_model
    from kmcos.types import create_kmc_model
    return create_kmc_model(model_name)

#kmcos can be invoked directly from the command line in one of the following ways::
#    kmcos [help] (all|benchmark|build|edit|export|help|import|rebuild|run|settings-export|shell|version|view|xml) [options]
#defining small wrapper functions to call cli if person types kmcos.export("MyFirstModel.xml") etc. Probably should have made an "@" decorator, but that's okay.
def build(argumentsString):
    import kmcos.cli as cli
    cli.main('build' +' ' + argumentsString)
def edit(argumentsString):
    import kmcos.cli as cli
    cli.main('edit'+' ' + argumentsString)
def export(argumentsString):
    import kmcos.cli as cli
    cli.main('export'+' ' + argumentsString)
def help(argumentsString):
    import kmcos.cli as cli
    cli.main('help' +' '+ argumentsString)
def rebuild(argumentsString):
    import kmcos.cli as cli
    cli.main('rebuild'+' ' + argumentsString)
def run(argumentsString):
    import kmcos.cli as cli
    cli.main('run'+' ' + argumentsString)
def settings_export(argumentsString):
    import kmcos.cli as cli
    cli.main('settings-export'+' ' + argumentsString)
def shell(argumentsString):
    import kmcos.cli as cli
    cli.main('shell'+' ' + argumentsString)    
def version(argumentsString):
    import kmcos.cli as cli
    cli.main('version'+' ' + argumentsString)    
def viewer(argumentsString): #TODO: should change the view.py file to viewer, and change this to view.
    import kmcos.cli as cli
    cli.main('view'+' ' + argumentsString)    
def xml(argumentsString):
    import kmcos.cli as cli
    cli.main('xml'+' ' + argumentsString)    

from kmcos.io import clear_model
