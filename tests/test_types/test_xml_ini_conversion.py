#!/usr/bin/env python

import os
import filecmp

def test_xml_ini_conversion():
    import kmcos.types
    import kmcos.io

    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    TEST_DIR = 'test'
    REFERENCE_DIR = 'reference'


    kmc_model = kmcos.create_kmc_model()
    kmc_model.import_file('reference/AB_model.xml')
    kmc_model.save('test/AB_model.ini')

    assert filecmp.cmp('test/AB_model.ini', 'reference/AB_model.ini')

def test_ini_xml_conversion():
    import kmcos.types
    import kmcos.io

    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    TEST_DIR = 'test'
    REFERENCE_DIR = 'reference'


    kmc_model = kmcos.create_kmc_model()
    kmc_model.import_file('reference/AB_model.ini')
    kmc_model.save('test/AB_model.xml')

    assert filecmp.cmp('test/AB_model.xml', 'reference/AB_model.xml')
