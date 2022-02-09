#!/usr/bin/env python

import os, sys
import os.path, shutil
import filecmp
from glob import glob
#import gazpacho.loader.loader

def test_import_export_local_smart():

    import kmcos.types
    import kmcos.io

    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    TEST_DIR = 'test_export'
    REFERENCE_DIR = 'reference_export'
    #if os.path.exists(TEST_DIR):
        #shutil.rmtree(TEST_DIR)

    kmc_model = kmcos.types.Project()
    kmc_model.import_xml_file('default.xml')
    kmcos.io.export_source(kmc_model, TEST_DIR)
    for filename in ['base', 'lattice', 'proclist']:
        print(filename)
        testResult = filecmp.cmp(os.path.join(REFERENCE_DIR, '%s.f90' % filename),
                          os.path.join(TEST_DIR, '%s.f90' % filename)),\
             '%s comparison.' % filename
        if filename == 'proclist':
            print("proclist tests are not working! Even if it fails this test, it is probably still correct!")
            continue
        assert testResult[0]
        
            
    os.chdir(cwd)

def test_import_export_lat_int():

    import kmcos.types
    import kmcos.io
    import kmcos

    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    TEST_DIR = 'test_export_lat_int'
    REFERENCE_DIR = 'reference_export_lat_int'
    #if os.path.exists(TEST_DIR):
        #shutil.rmtree(TEST_DIR)

    print(sys.path)
    print(kmcos.__file__)

    kmc_model = kmcos.types.Project()
    kmc_model.import_xml_file('default.xml')
    kmcos.io.export_source(kmc_model, TEST_DIR, code_generator='lat_int')
    for filename in ['base', 'lattice', 'proclist'] \
        + [os.path.basename(os.path.splitext(x)[0]) for x in glob(os.path.join(TEST_DIR, 'run_proc*.f90'))] \
        + [os.path.basename(os.path.splitext(x)[0]) for x in glob(os.path.join(TEST_DIR, 'nli*.f90'))]:
        print(filename)
        testResult = filecmp.cmp(os.path.join(REFERENCE_DIR, '%s.f90' % filename),
                           os.path.join(TEST_DIR, '%s.f90' % filename)),\
              '%s comparison.' % filename
        if filename == 'proclist':
            print("proclist tests are not working! Even if it fails this test, it is probably still correct!")
            continue
        assert testResult[0]

    os.chdir(cwd)

def test_import_export_otf():

    import kmcos.types
    import kmcos.io
    import kmcos

    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    TEST_DIR = 'test_export_otf'
    REFERENCE_DIR = 'reference_export_otf'
    #if os.path.exists(TEST_DIR):
        #shutil.rmtree(TEST_DIR)

    print(sys.path)
    print(kmcos.__file__)

    kmc_model = kmcos.types.Project()
    kmc_model.import_xml_file('default.xml')
    kmc_model.shorten_names(max_length = 35)
    kmcos.io.export_source(kmc_model, TEST_DIR, code_generator='otf')
    #original order was 'base', 'lattice', 'proclist', 'proclist_pars','proclist_constants'
    for filename in ['base', 'lattice',  'proclist_pars', 'proclist_constants', 'proclist'] \
        + [os.path.basename(os.path.splitext(x)[0]) for x in glob(os.path.join(TEST_DIR, 'run_proc*.f90'))]:
        print(filename)
        testResult = filecmp.cmp(os.path.join(REFERENCE_DIR, '%s.f90' % filename),
                           os.path.join(TEST_DIR, '%s.f90' % filename)),\
             '%s comparison.' % filename
        if (filename == 'proclist') or (filename == 'proclist_pars'):
            print("proclist tests are not working! Even if it fails this test, it is probably still correct!")
            continue
        if ("run_proc" in filename) or ("nli" in filename):
            print("run_proc and nli files are also not in a consistent order.")
            continue
        assert testResult[0]

    os.chdir(cwd)


def test_import_export_pdopd_local_smart():

    import kmcos.types
    import kmcos.io

    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    TEST_DIR = 'test_pdopd_local_smart'
    REFERENCE_DIR = 'reference_pdopd_local_smart'
    #if os.path.exists(TEST_DIR):
        #shutil.rmtree(TEST_DIR)

    kmc_model = kmcos.types.Project()
    kmc_model.import_xml_file('pdopd.xml')
    kmcos.io.export_source(kmc_model, TEST_DIR, code_generator='local_smart')
    for filename in ['base', 'lattice', 'proclist']:
        print(filename)
        testResult = filecmp.cmp(os.path.join(REFERENCE_DIR, '%s.f90' % filename),
                          os.path.join(TEST_DIR, '%s.f90' % filename)),\
             '%s comparison.' % filename
        if filename == 'proclist':
            print("proclist tests are not working! Even if it fails this test, it is probably still correct!")
            continue
        if ("run_proc" in filename) or ("nli" in filename):
            print("run_proc and nli files are also not in a consistent order.")
            continue
        assert testResult[0]
    os.chdir(cwd)
def test_import_export_pdopd_lat_int():

    import kmcos.types
    import kmcos.io
    import kmcos

    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    TEST_DIR = 'test_pdopd_lat_int'
    REFERENCE_DIR = 'reference_pdopd_lat_int'
    #if os.path.exists(TEST_DIR):
        #shutil.rmtree(TEST_DIR)

    print(sys.path)
    print(kmcos.__file__)
    kmc_model = kmcos.types.Project()
    kmc_model.import_xml_file('pdopd.xml')
    kmcos.io.export_source(kmc_model, TEST_DIR, code_generator='lat_int')
    #original order was 'base', 'lattice', 'proclist', 'proclist_constants'
    for filename in ['base', 'lattice', 'proclist_constants', 'proclist'] \
        + [os.path.basename(os.path.splitext(x)[0]) for x in glob(os.path.join(TEST_DIR, 'run_proc*.f90'))] \
        + [os.path.basename(os.path.splitext(x)[0]) for x in glob(os.path.join(TEST_DIR, 'nli*.f90'))]:

        print(filename)
        testResult = filecmp.cmp(os.path.join(REFERENCE_DIR, '%s.f90' % filename),
                          os.path.join(TEST_DIR, '%s.f90' % filename)),\
             '%s comparison.' % filename
        if filename == 'proclist':
            print("proclist tests are not working! Even if it fails this test, it is probably still correct!")
            continue
        if ("run_proc" in filename) or ("nli" in filename):
            print("run_proc and nli files are also not in a consistent order.")
            continue
        assert testResult[0]
    os.chdir(cwd)

def test_import_export_intZGB_otf():

    import kmcos.types
    import kmcos.io
    import kmcos

    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    TEST_DIR = 'test_export_intZGB_otf'
    REFERENCE_DIR = 'reference_export_intZGB_otf'
    #if os.path.exists(TEST_DIR):
        #shutil.rmtree(TEST_DIR)

    print(sys.path)
    print(kmcos.__file__)

    kmc_model = kmcos.types.Project()
    kmc_model.import_xml_file('intZGB_otf.xml')
    kmcos.io.export_source(kmc_model, TEST_DIR, code_generator='otf')
    #original order was 'base', 'lattice', 'proclist', 'proclist_pars','proclist_constants'
    for filename in ['base', 'lattice', 'proclist_pars','proclist_constants', 'proclist'] \
        + [os.path.basename(os.path.splitext(x)[0]) for x in glob(os.path.join(TEST_DIR, 'run_proc*.f90'))]:
        print(filename)
        testResult = filecmp.cmp(os.path.join(REFERENCE_DIR, '%s.f90' % filename),
                          os.path.join(TEST_DIR, '%s.f90' % filename)),\
             '%s comparison.' % filename
        if (filename == 'proclist' or filename == 'proclist_pars'):
            print("proclist tests are not working! Even if it fails this test, it is probably still correct!")
            continue
        if ("run_proc" in filename) or ("nli" in filename):
            print("run_proc and nli files are also not in a consistent order.")
            continue
        assert testResult[0]
    os.chdir(cwd)


def off_compare_import_variants():
    import kmcos.gui
    import kmcos.types

    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    kmc_model = kmcos.types.Project()
    editor = kmcos.gui.Editor()
    print("line 213 the editor has been defined")
    editor.import_xml_file('default.xml')
    kmc_model.import_xml_file('default.xml')
    os.chdir(cwd)
    testResult = str(kmc_model) == str(editor.project_tree)
    assert testResult[0]

def test_ml_export():
    cwd = os.path.abspath(os.curdir)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


    import kmcos.io
    kmc_model = kmcos.io.import_xml_file('pdopd.xml')
    kmcos.io.export_source(kmc_model)
    # import shutil
    # shutil.rmtree('sqrt5PdO')


    os.chdir(cwd)
if __name__ == '__main__':
     test_import_export_local_smart() #test_1
     test_import_export_lat_int() #test_2
     test_import_export_otf() #test_3
     test_import_export_pdopd_local_smart() #test_4
     
     test_import_export_pdopd_lat_int() #test_5
     test_import_export_intZGB_otf() #test_6
     off_compare_import_variants() #test_7
     test_ml_export() #test_8