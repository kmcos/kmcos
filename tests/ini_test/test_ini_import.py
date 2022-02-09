#!/usr/bin/env python

from glob import glob
import kmcos

def test_ini_import():
    for ini_filename in glob('*.ini'):
        from kmcos.types import Project
        kmc_model = kmcos.create_kmc_model()
        kmc_model.import_ini_file(open(ini_filename))
        kmc_model.save('foo.ini')
        kmc_model.save('foo.xml')

if __name__ == '__main__':
    test_ini_import()
