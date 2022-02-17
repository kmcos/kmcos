#!/usr/bin/env python3
"""Entry point module for the command-line
   interface. The kmcos executable should be
   on the program path, import this modules
   main function and run it.

   To call kmcos command as you would from the shell,
   use ::

       kmcos.cli.main('...')

   Every command can be shortened as long as it is non-ambiguous, e.g. ::


    kmcos ex <xml-file>

   instead of ::

    kmcos export <xml-file>

   etc.

   You may also use syntax kmcos.export("...") for any cli command.
   
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


from __future__ import with_statement
from __future__ import print_function
import os
import shutil

usage = {}
usage['all'] = """kmcos help all
    Display documentation for all commands.
                """
usage['benchmark'] = """kmcos benchmark
    Run 1 mio. kMC steps on model in current directory
    and report runtime.
                     """

usage['build'] = """kmcos build
    Build kmc_model.%s from *f90 files in the
    current directory.

    Additional Parameters ::
        -d/--debug
            Turn on assertion statements in F90 code

        -n/--no-compiler-optimization
            Do not send optimizing flags to compiler.
                 """ % ('pyd' if os.name == 'nt' else 'so')

usage['help'] = """kmcos help <command>
    Print usage information for the given command.
                """

usage['export'] = """kmcos export <xml-file> [<export-path>]
    Take a kmcos xml-file and export all generated
    source code to the export-path. There try to
    build the kmc_model.%s.

    Additional Parameters ::

        -s/--source-only
            Export source only and don't build binary

        -b/--backend (local_smart|lat_int)
            Choose backend. Default is "local_smart".
            lat_int is EXPERIMENTAL and not made
            for production, yet.

        -t/--temp_acc
            Use temporal acceleration scheme.
            Builds the modules base_acc.f90, lattice_acc.mpy, 
            proclist_constants_acc.mpy and 
            proclist_generic_subroutines_acc.mpy.
            Default is false.

        -d/--debug
            Turn on assertion statements in F90 code.
            (Only active in compile step)

           --acf
            Build the modules base_acf.f90 and proclist_acf.f90. Default is false.
            This both modules contain functions to calculate ACF (autocorrelation function) and MSD (mean squared displacement). 
            
        -n/--no-compiler-optimization
            Do not send optimizing flags to compiler.
                    """ % ('pyd' if os.name == 'nt' else 'so')
          
usage['settings-export'] = """kmcos settings-export <xml-file> [<export-path>]
    Take a kmcos xml-file and export kmc_settings.py
    to the export-path.
                    """

usage['edit'] = """kmcos edit <xml-file>
    Open the kmcos xml-file in a GUI to edit
    the model.
                """

usage['import'] = """kmcos import <xml-file>
    Take a kmcos xml-file and open an ipython shell
    with the project_tree imported as pt.
                  """
usage['rebuild'] = """kmcos rebuild
    Export code and rebuild binary module from XML
    information included in kmc_settings.py in
    current directory.

    Additional Parameters ::
        -d/--debug
            Turn on assertion statements in F90 code
                    """

usage['shell'] = """kmcos shell
    Open an interactive shell and create a KMC_Model in it
               run == shell
               """
usage['run'] = """kmcos run
    Open an interactive shell and create a KMC_Model in it
               run == shell
               """

usage['version'] = """kmcos version
    Print version number and exit.
                   """

usage['view'] = """kmcos view
    Take a kmc_model.%s and kmc_settings.py in the
    same directory and start to simulate the
    model visually.

    Additional Parameters ::
        -v/--steps-per-frame <number>
            Number of steps per frame

                 """ % ('pyd' if os.name == 'nt' else 'so')

usage['xml'] = """kmcos xml
    Print xml representation of model to stdout
               """


def get_options(args=None, get_parser=False):
    import optparse
    import os
    from glob import glob
    import kmcos

    parser = optparse.OptionParser(
        'Usage: %prog [help] ('
        + '|'.join(sorted(usage.keys()))
        + ') [options]',
        version=kmcos.__version__)

    # -s is the shorthamd for --source-only. All following options follow the same syntax
    parser.add_option('-s', '--source-only', 
                      dest='source_only',
                      action='store_true',
                      default=False)

    parser.add_option('-p', '--path-to-f2py',
                      dest='path_to_f2py',
                      default='f2py')

    parser.add_option('-b', '--backend',
                      dest='backend',
                      default='local_smart')
    parser.add_option('-a', '--avoid-default-state',
                      dest='avoid_default_state',
                      action='store_true',
                      default=False,
                      )

    parser.add_option('-v', '--steps-per-frame',
                      dest='steps_per_frame',
                      type='int',
                      default='50000')

    parser.add_option('-d', '--debug',
                      default=False,
                      dest='debug',
                      action='store_true')

    parser.add_option('-n', '--no-compiler-optimization',
                      default=False,
                      dest='no_optimize',
                      action='store_true')

    parser.add_option('-o', '--overwrite',
                      default=False,
                      action='store_true')

    parser.add_option('-l', '--variable-length',
                      dest='variable_length',
                      default=95,
                      type='int')

    parser.add_option('-c', '--catmap',
                      default=False,
                      action='store_true')
   
    parser.add_option('-t', '--temp_acc',
                      default=False,
                      dest='temp_acc',
                      action='store_true')
    
    parser.add_option('--acf',
                      dest='acf',
                      action='store_true',
                      default=False,
                      )
   
    try:
        from numpy.distutils.fcompiler import get_default_fcompiler
        from numpy.distutils import log
        log.set_verbosity(-1, True)
        fcompiler = get_default_fcompiler()
    except:
        fcompiler = 'gfortran'

    parser.add_option('-f', '--fcompiler',
                      dest='fcompiler',
                      default=os.environ.get('F2PY_FCOMPILER', fcompiler))

    if args is not None:
        options, args = parser.parse_args(args.split())
    else:
        options, args = parser.parse_args()
    if len(args) < 1:
        parser.error('Command expected')
    if get_parser:
        return options, args, parser
    else:
        return options, args


def match_keys(arg, usage, parser):
    """Try to match part of a command against
       the set of commands from usage. Throws
       an error if not successful.

    """
    possible_args = [key for key in usage if key.startswith(arg)]
    if len(possible_args) == 0:
        parser.error('Command "%s" not understood.' % arg)
    elif len(possible_args) > 1:
        parser.error(('Command "%s" ambiguous.\n'
                      'Could be one of %s\n\n') % (arg, possible_args))
    else:
        return possible_args[0]


def main(args=None):
    """The CLI main entry point function.

    The optional argument args, can be used to
    directly supply command line argument like

    $ kmcos <args>

    otherwise args will be taken from STDIN.

    """

    from glob import glob

    options, args, parser = get_options(args, get_parser=True)

    global model, pt, np, cm_model

    if not args[0] in list(usage.keys()):
        args[0] = match_keys(args[0], usage, parser)

    if args[0] == 'benchmark':
        from sys import path
        path.append(os.path.abspath(os.curdir))
        nsteps = 1000000
        from time import time
        from kmcos.run import KMC_Model
        model = KMC_Model(print_rates=False, banner=False)
        accelerated = model.can_accelerate
        if not accelerated:
            time0 = time()
            try:
                model.proclist.do_kmc_steps(nsteps)
            except:  # kmos < 0.3 had no model.proclist.do_kmc_steps
                model.do_steps(nsteps)

            needed_time = time() - time0
            print('Using the [%s] backend.' % model.get_backend())
            print('%s steps took %.2f seconds' % (nsteps, needed_time))
            print('Or %.2e steps/s' % (1e6 / needed_time))
            model.deallocate()
        else:
            time0 = time()
            model.do_steps(nsteps)
            needed_time = time() - time0
            print('Using the [%s] backend.' % model.get_backend())
            print('Using the temporal acceleration scheme')
            print('%s normal steps took %.2f seconds' % (nsteps, needed_time))
            print('Or %.2e steps/s' % (1e6 / needed_time))
            print('')
            model.deallocate()
            model = KMC_Model(print_rates=False, banner=False)
            time0 = time()
            model.do_acc_steps(nsteps)
            needed_time = time() - time0
            print('%s accelerated steps took %.2f seconds' % (nsteps, needed_time))
            print('Or %.2e steps/s' % (1e6 / needed_time))
            model.deallocate()

    elif args[0] == 'build':
        from kmcos.utils import build
        build(options)
    elif args[0] == 'edit':
        from kmcos import gui
        gui.main()
    elif args[0] == 'settings-export':
        import kmcos.types
        import kmcos.io
        from kmcos.io import ProcListWriter

        if len(args) < 2:
            parser.error('XML file and export path expected.')
        if len(args) < 3:
            out_dir = '%s_%s' % (os.path.splitext(args[1])[0], options.backend)
            print('No export path provided. Exporting to %s' % out_dir)
            args.append(out_dir)

        xml_file = args[1]
        export_dir = args[2]
        project = kmcos.types.Project()
        project.import_file(xml_file)

        writer = ProcListWriter(project, export_dir)
        writer.write_settings()

    elif args[0] == 'export':
        import kmcos.types
        import kmcos.io
        from kmcos.utils import build
        if len(args) < 2:
            parser.error('XML file and export path expected.')
        if len(args) < 3:
            out_dir = '%s_%s' % (os.path.splitext(args[1])[0], options.backend)

            print('No export path provided. Exporting to %s' % out_dir)
            args.append(out_dir)

        xml_file = args[1]
        export_dir = os.path.join(args[2], 'src')

        project = kmcos.types.Project()
        project.import_file(xml_file)

        project.shorten_names(max_length=options.variable_length)

        kmcos.io.export_source(project,
                               export_dir,
                               options=options,
                               accelerated=options.temp_acc)

        if ((os.name == 'posix'
           and os.uname()[0] in ['Linux', 'Darwin'])
           or os.name == 'nt') \
           and not options.source_only:
            os.chdir(export_dir)
            build(options)
            for out in glob('kmc_*'):
                if os.path.exists('../%s' % out) :
                    if options.overwrite :
                        overwrite = 'y'
                    else:
                        overwrite = input(('Should I overwrite existing %s ?'
                                               '[y/N]  ') % out).lower()
                    if overwrite.startswith('y') :
                        print('Overwriting {out}'.format(**locals()))
                        os.remove('../%s' % out)
                        shutil.move(out, '..')
                    else :
                        print('Skipping {out}'.format(**locals()))
                else:
                    shutil.move(out, '..')

    elif args[0] == 'settings-export':
        import kmcos.io
        pt = kmcos.io.import_file(args[1])
        if len(args) < 3:
            out_dir = os.path.splitext(args[1])[0]
            print('No export path provided. Exporting kmc_settings.py to %s'
                  % out_dir)
            args.append(out_dir)

        if not os.path.exists(args[2]):
            os.mkdir(args[2])
        elif not os.path.isdir(args[2]):
            raise UserWarning("Cannot overwrite %s; Exiting;" % args[2])
        writer = kmcos.io.ProcListWriter(pt, args[2])
        writer.write_settings()

    elif args[0] == 'help':
        if len(args) < 2:
            parser.error('Which help do you  want?')
        if args[1] == 'all':
            for command in sorted(usage):
                print(usage[command])
        elif args[1] in usage:
            print('Usage: %s\n' % usage[args[1]])
        else:
            arg = match_keys(args[1], usage, parser)
            print('Usage: %s\n' % usage[arg])

    elif args[0] == 'import':
        import kmcos.io
        if not len(args) >= 2:
            raise UserWarning('XML file name expected.')
        pt = kmcos.io.import_xml_file(args[1])
        if len(args) == 2:
            sh(banner='Note: pt = kmcos.io.import_xml(\'%s\')' % args[1])
        elif len(args) == 3: # if optional 3rd argument is given, store model there and exit
            pt.save(args[2])

    elif args[0] == 'rebuild':
        from time import sleep
        print('Will rebuild model from kmc_settings.py in current directory')
        print('Please do not interrupt,'
              ' build process, as you will most likely')
        print('loose the current model files.')
        sleep(2.)
        from sys import path
        path.append(os.path.abspath(os.curdir))
        from tempfile import mktemp
        if not os.path.exists('kmc_model.so') \
           and not os.path.exists('kmc_model.pyd'):
            raise Exception('No kmc_model.so found.')
        if not os.path.exists('kmc_settings.py'):
            raise Exception('No kmc_settings.py found.')

        from kmcos.run import KMC_Model

        model = KMC_Model(print_rates=False, banner=False)
        tempfile = mktemp()
        f = file(tempfile, 'w')
        f.write(model.xml())
        f.close()

        for kmc_model in glob('kmc_model.*'):
            os.remove(kmc_model)
        os.remove('kmc_settings.py')
        main('export %s -b %s .' % (tempfile, options.backend))
        os.remove(tempfile)
        model.deallocate()

    elif args[0] in ['run', 'shell']:
        from sys import path
        path.append(os.path.abspath(os.curdir))
        from kmcos.run import KMC_Model

        # useful to have in interactive mode
        import numpy as np
        try:
            from matplotlib import pyplot as plt
        except:
            plt = None

        if options.catmap:
            import catmap
            import catmap.cli.kmc_runner
            seed = catmap.cli.kmc_runner.get_seed_from_path('.')
            cm_model = catmap.ReactionModel(setup_file='{seed}.mkm'.format(**locals()))
            catmap_message = '\nSide-loaded catmap_model {seed}.mkm into cm_model = ReactionModel(setup_file="{seed}.mkm")'.format(**locals())
        else:
            catmap_message = ''

        try:
            model = KMC_Model(print_rates=False)
        except:
            print("Warning: could not import kmc_model!"
                  " Please make sure you are in the right directory")
        sh(banner='Note: model = KMC_Model(print_rates=False){catmap_message}'.format(**locals()))
        try:
            model.deallocate()
        except:
            print("Warning: could not deallocate model. Was is allocated?")

    elif args[0] == 'version':
        from kmcos import VERSION
        print(VERSION)

    elif args[0] == 'view':
        from sys import path
        path.append(os.path.abspath(os.curdir))
        from kmcos import view
        view.main(steps_per_frame=options.steps_per_frame)

    elif args[0] == 'xml':
        from sys import path
        path.append(os.path.abspath(os.curdir))
        from kmcos.run import KMC_Model
        model = KMC_Model(banner=False, print_rates=False)
        print(model.xml())

    else:
        parser.error('Command "%s" not understood.' % args[0])


def sh(banner):
    """Wrapper around interactive ipython shell
    that factors out ipython version depencies.

    """

    from distutils.version import LooseVersion
    import IPython
    if hasattr(IPython, 'release'):
        try:
            from IPython.terminal.embed import InteractiveShellEmbed
            InteractiveShellEmbed(banner1=banner)()

        except ImportError:
            try:
                from IPython.frontend.terminal.embed \
                    import InteractiveShellEmbed
                InteractiveShellEmbed(banner1=banner)()

            except ImportError:
                from IPython.Shell import IPShellEmbed
                IPShellEmbed(banner=banner)()
    else:
        from IPython.Shell import IPShellEmbed
        IPShellEmbed(banner=banner)()
