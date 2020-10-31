#!/usr/bin/env python
"""kMC modeling on steroids"""

import os
from distutils.core import setup
from kmos import __version__ as version

maintainer = 'Aditya Savara'
url = 'https://github.com/kmcos/kmcos'                 
license = 'COPYING'
long_description = open('README.rst').read()
name='kmcos'
maintainer_email = 'AdityaSavara2008@u.northwestern.edu'
author = 'Max J. Hoffmann'
author_email = 'mjhoffmann@gmail.com'
description =  __doc__
classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: Windows',
        'Programming Language :: Fortran',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
              ]
requires = [
                    'ase',
                    'pycairo==1.11.1',
                    'pygobject==3.30',
                    #'goocanvas', #part of pygobject now, I think.
                    'kiwi',
                    'kiwi-gtk',
                    'lxml',
                    'matplotlib',
#                    'pygtk', #This is only for windows so should be under extras.
                   ]
packages = [
           'kmos',
           'kmos.utils',
           'kmos.run',
           'kmos.gui',
           ]
package_dir = {'kmos':'kmos'}
package_data = {'kmos':['fortran_src/*f90',
                        'fortran_src/*.mpy',
                        'kmc_editor.glade',
                        'fortran_src/assert.ppc',
                        'kmc_project_v0.1.dtd',
                        'kmc_project_v0.2.dtd',
                        'kmc_project_v0.3.dtd']}
platforms = ['linux', 'windows']
if os.name == 'nt':
    scripts = [
            'tools/kmos.bat'
            ]
else:
    scripts = [
            'tools/kmos-build-standalone',
            'tools/kmos',
            'tools/kmos-install-dependencies-ubuntu',
            ]

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()
setup(
      author=author,
      author_email=author_email,
      description=description,
      license=license,
      long_description=long_description,
      maintainer=maintainer,
      maintainer_email=maintainer_email,
      name=name,
      package_data=package_data,
      package_dir=package_dir,
      packages=packages,
      platforms=platforms,
      #requires=requires,
      scripts=scripts,
      url=url,
      version=version,
      )
