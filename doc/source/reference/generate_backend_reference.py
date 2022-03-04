#!/usr/bin/env python

import tempfile
import sys
import glob
import os
import shutil

from kmcos.types import *
from kmcos.io import *

# Copy DTD
import kmcos
shutil.copy(os.path.join(os.path.dirname(kmcos.__file__),
                                'kmc_project_v0.2.dtd'),
            '.')

# Fetch doc from dummy project

for backend in ['local_smart', 'lat_int', 'otf']:
    print("Backend {backend}".format(**locals()))

    kmc_model = kmcos.create_kmc_model()
    outdir = tempfile.mkdtemp()
    outdir = 'outdir'
    outdir
    kmc_model.meta.model_dimension = 2
    kmc_model.species_list.default_species = 'default'

    kmc_model.meta.model_name = 'example'
    kmc_model.meta.model_name = 'some_model'
    kmc_model.meta.author = 'some guy'
    kmc_model.meta.email = 'some.guy@server.org'

    kmc_model.add_layer(name='default')
    kmc_model.get_layers()[0].add_site(Site(name='default'))
    kmc_model.add_species(name='a', representation='')
    kmc_model.add_species(name='b', representation='')

    kmc_model.species_list.default_species = 'a'
    coord = kmc_model.layer_list.generate_coord('default.(0,0,0).default')

    kmc_model.add_process(name='ab',
                   condition_list=[Condition(coord=coord, species='a')],
                   action_list=[Condition(coord=coord, species='b')],
                   )
    kmc_model.add_process(name='ba',
                   condition_list=[Condition(coord=coord, species='b')],
                   action_list=[Condition(coord=coord, species='a')],
                   )
    export_source(pt, outdir, code_generator=backend)

    print(glob.glob('{outdir}/*.f90'.format(**locals())))
    for f90_file in glob.glob('{outdir}/*.f90'.format(**locals())):
        prefix = os.path.splitext(os.path.basename(f90_file))[0]
    #for prefix in ['base', 'lattice', 'proclist']:
        f90_path = os.path.join(outdir, prefix)
        os.system('robodoc --src {f90_path}.f90 --doc {prefix}_{backend} --singlefile --ascii'.format(**locals()))

        asci = file('{prefix}_{backend}.txt'.format(**locals()), 'r').readlines()

        new_asci = []
        jump = 0
        for i, line in enumerate(asci):
            if jump:
                jump += -1
                continue
            if not i:
            # make first line header
                new_asci.append(line)
                new_asci.append('-' * 40 + '\n')
            elif i >= len(asci) - 2:
            # ignore last line
                continue
            elif 'FUNCTION' in line:
            # ignore the function string
                continue
            elif 'ARGUMENTS' in line:
            # ignore the arguments string
                new_asci.append('\n')
            elif '------' in line:
                new_asci.append(asci[i + 1])
                new_asci.append('"' * 50)
                jump = 1
            else:
                new_asci.append(line)
        if new_asci :
            rst = file('robodoc/{backend}_{prefix}.rst'.format(**locals()), 'w')
            for line in new_asci:
                rst.write(line)
            rst.close()

        os.system('rm {prefix}_{backend}.txt'.format(**locals()))
        #os.system('rst2html base.rst > base.html')

    shutil.rmtree(outdir)

with file('cli.rst', 'w') as outfile:
    from kmcos.cli import usage
    from kmcos import cli
    outfile.write(cli.__doc__)
    outfile.write('List of commands\n^^^^^^^^^^^^^^^^\n\n')
    for i, doc in enumerate(sorted(usage.values())):
        outfile.write('\n\n')
        doc = doc.replace('*', '\*')
        doc = doc.split('\n')
        doc[0] = '``%s``' % doc[0]
        for i, line in enumerate(doc):
            doc[i] = line.rstrip()
        doc = '\n'.join(doc)
        outfile.write('%s' % doc)
