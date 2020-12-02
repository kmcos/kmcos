

Kmcos has some non-python dependencies (including gfortran) so cannot be installed with only pip. It is recommended to install kmcos on a Linux operating system (such as Ubuntu). Additionally, based on current best practices for Python programs, it is recommended to create a virtual environment, so our instructions begin with how to create a virtual environment.
If you plan to use a windows os, it is recommended to first get `VirtualBox <https://www.virtualbox.org/wiki/Downloads>`_ .
Then get Ubuntu. Here are some `Example Instructions to install Ubuntu <https://www.freecodecamp.org/news/how-to-install-ubuntu-with-oracle-virtualbox/>`_ .

In the future, instructions for other system configurations may be provided.


Making a Virtual Python Environment for kmcos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is recommended to use a virtual python environment for both installation and for simulations. This avoids python software conflicts.

OPTION 1 (python3-venv)::

    cd ~
    sudo apt-get update
    sudo apt-get install python3
    sudo apt-get install python3-venv
    python3 -m venv ~/VENV/kmcos
    source ~/VENV/kmcos/bin/activate

If installing kmcos in a virtualenv, to use kmcos after installation, you will need to activate from the terminal each time, since kmcos will only be installed in the virtualenv. To exit this virtualenv you will type 'deactivate'. 

OPTION 2 (virtualenv)::

    cd ~
    sudo apt-get update
    sudo apt-get install python3-pip
    sudo apt-get install virtualenv
    virtualenv -p /usr/bin/python3 kmcos3venv  #If the virtualenv command gives you an error, then try typing "which python3" and replace the path "/usr/bin/python3" with what your system provides.
    source ~/kmcos3venv/bin/activate

If you install kmcos in a virtualenv, to use kmcos after installation, you will need to activate from the terminal each time, since kmcos will only be installed in the virtualenv. To exit this virtualenv you will type 'deactivate'. You can find more information on virtualenv at https://www.youtube.com/watch?v=N5vscPTWKOk and https://virtualenv.pypa.io/en/latest/

OPTION 3 (anaconda)::
    
    If you will be installing kmcos in an anaconda environment, you can make a new environment named 'kmcos' from anaconda navigator. See for example 
    `this link <https://medium.com/cluj-school-of-ai/python-environments-management-in-anaconda-navigator-ad2f0741eba7>`_ . 


Virtual environment installations do not require the "--user" tag as the python packages are 'sandboxed' during installation.

Installing kmcos on Ubuntu Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The easiest way to install kmcos is to use the automatic installers ::

    cd ~
    git clone https://github.com/kmcos/kmcos-installers
    cd kmcos-installers
    bash install-kmcos-linux-venv.bash #use 'bash install-kmcos-linux-user.bash' if you are not using a virtual environment.
    
If the above simple way does not work for you, you will need to go through the commands one at a time for `installation on a venv <https://github.com/kmcos/kmcos-installers/blob/main/install-kmcos-linux-venv.bash>`_ or `installation as a user <https://github.com/kmcos/kmcos-installers/blob/main/install-kmcos-linux-user.bash>`_ . A kmcosInstallation directory is created during installation. The files in the kmcosInstallation are no longer needed, so you can remove the kmcosInstallation directory. Alternatively, you can navigate into that directory and go through the examples. 

For upgrades, you will not need to use git again. For upgrades, you can just use the earlier pip command ::

    pip install kmcos[MINIMAL] --upgrade --user

(Optional) If you would like to use the kmcos view capability, you will need to install some non-python dependencies and then kmcos complete ::

    sudo apt-get install python-ase
    sudo apt-get install python3-gi
    pip install ase --user
    pip install kmcos[COMPLETE] --upgrade --user

If the last command of 'pip install kmcos[COMPLETE] --upgrade --user' gives an error, try to run it again.


<bold>THE ABOVE INSTRUCTIONS SHOULD ALSO WORK ON MOST LINUX PLATFORMS. BELOW IS ADDITOINAL INFO FOR UBUNTU INSTALLATION THAT IS CONSIDERED DEPRECATED, FOLLOWED BY OTHER DEPRECATED INSTRUCTIONS.  UPDATED INSTRUCTIONS WILL BE PLACED ON THIS SITE IF PROVIDED.</bold>

To use the core functionality
(programmatic model setup, code generation, model execution)
kmcos has a fairly modest depedency foot-print. You will need ::

  python-numpy, a Fortran compiler, python-lxml

In order to watch the model run on screen you will additionally
need ::

  python-matplotlib, python-ase

Finally in order to use all features, in particular the GUI
model editor of kmcos you have to install
a number of dependencies. This should not be very difficult
on a recent Linux distribution with package management. So
on Ubuntu it suffices to call::

  sudo apt-get install gazpacho gfortran python-dev \
                       python-glade2 python-kiwi python-lxml \
                       python-matplotlib python-numpy \
                       python-pygoocanvas


and if you haven't already installed it, one way to fetch the
atomic simulation environment (ASE) is currently to ::

  sudo add-apt-repository ppa:campos-dev/campos
  sudo apt-get update
  sudo apt-get install python-ase

Or go to their `website <https://gitlab.com/ase/ase/repository/archive.zip?ref=master>`_
to fetch the latest version.

Unfortunately Debian/Ubuntu have discontinued maintaining the gazpacho package which I find very unfortunate since it eased gtk GUI building a lot and I haven't found a simple transition path (simple as in one reliable conversion script and two changed import lines) towards gtkbuilder. Therefore for the moment I can only suggest to fetch the latest old package from e.g. `here <https://gist.github.com/mhoffman/d2a9466c22f33a9e046b/raw/4c73c5029f3c01e656f161c7459f720aff331705/gazpacho_0.7.2-3_all.deb>`_ and install it manually with ::

    sudo dpkg -i gazpacho_*.deb



If you think this dependency list hurts. Yes, it does!
And I am happy about any suggestions how to
minimize it. However one should note these dependencies are only
required for the model development. Running a model has virtually
no dependencies except for a Fortran compiler.

To ease the installation further on Ubuntu one can simply run::

 kmcos-install-dependencies-ubuntu


Installation on openSUSE 12.1 Linux (Deprecated Instructions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On a recent openSUSE some dependencies are distributed a little
different but nevertheless doable. We start by install some
package from the repositories ::

  sudo zypper install libgfortran46, python-lxml, python-matplotlib, \
                      python-numpy, python-numpy-devel, python-goocanvas,
                      python-imaging

And two more packages SUSE packages have to be fetched from the
openSUSE `build service <https://build.opensuse.org/>`_

- `gazpacho <https://build.opensuse.org/package/files?package=gazpacho&project=home%3Ajoshkress>`_
- `python-kiwi <https://build.opensuse.org/package/files?package=python-kiwi&project=home%3Ajoshkress>`_


For each one just download the \*.tar.bz2 files. Unpack them and inside
run ::

  python setup.py install

In the same vein you can install ASE. Download a recent version
from the `GitLab website <https://gitlab.com/ase/ase/repository/archive.zip?ref=master>`_
unzip it and install it with ::

  python setup.py install



Installation on openSUSE 13.1 Linux (Deprecated Instructions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to use the editor GUI you will want to install python-kiwi (not KIWI)
and right now you can find a recent build `here <https://build.opensuse.org/package/show/home:leopinheiro/python-kiwi>`_ .

Installation on Mac OS X 10.10 or above (Deprecated Instructions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is more than one way to get required dependencies. I have tested MacPorts and worked quite well.

#. Get MacPorts
    Search for MacPorts online, you'll need to install Xcode in the process

#. Install Python, lxml, numpy, ipython, ASE, gcc48. I assume you are using Python 2.7.
   kmcos has not been thoroughly tested with Python 3.X, yet, but should not be too hard.
    Having MacPorts this can be as simple as ::

        sudo port install -v py27-ipython
        sudo port select --set ipython py27-ipython

        sudo port install gcc48
        sudo port select --set gcc mp-gcc48 # need to that f2py finds a compiler

        sudo port install py27-readline
        sudo port install py27-goocanvas
        sudo port install py27-lxml
        sudo port install kiwi
        # possibly more ...

        # if you install these package manually, skip pip :-)
        sudo port install py27-pip
        sudo port select --set pip pip27

        pip install python-ase --user
        pip install python-kmcos --user


Installation on windows
^^^^^^^^^^^^^^^^^^^^^^^^^

Direct installation on windows is currently not supported. It is recommended to download virtualbox, to install Ubuntu, and then follow the Ubuntu installation instructions. You may need to adjust the resolution to work effectively.
For direct installin on windows, partial instructions have been written below. In the future, an "Ubuntu on Windows 10 via Windows Subsystem" set of instructions will be provided (and would be welcomed as a contribution).

***

In order for kmcos to work in a recent windows it is best to get Anaconda.

Download anaconda and open an anaconda terminal.

The first time you install kmcos, you will need to fetch the full package from github ::

    git clone http://www.github.com/kmcos/kmcos

Next, go into the package directory and install using the setup.py file ::

    cd kmcos
    python setup.py install
    
Note that on windows it is recommended to not use the --user command, otherwise the command line interface (typing 'kmcos' from the command line) will not work. Next, install the MINIMAL dependencies.

    pip install kmcos[MINIMAL] --upgrade --user
    
Note: pip install kmcos[COMPLETE] won't work. to install pycairo and use the visual aspects, Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": https://visualstudio.microsoft.com/downloads/

BELOW ARE DEPRECATED INSTRUCTIONS

#. **Python**
   If you have no python previously installed you should get `Anaconda`
   with python 3.
   or `Enthought Python Distribution`_ (EPD) in its free version since it
   already comes with a number of useful libraries such a numpy, scipy,
   ipython and matplotlib.

#. **numpy**
   Fetch it for `your version` of python from
   `sourceforge's Numpy site <http://sourceforge.net/project/numpy>`_
   and install it. [Not needed with EPD ]

#.  **MinGW**
    provides free Fortran and C compilers and can be obtained from the
    `sourceforge's MinGW site <https://sourceforge.net/projects/mingw/>`_ .
    Make sure you make a tick for the Fortran and the C compiler.

#. **pyGTK**
   is needed for the GUI frontend so fetch the
   `all-in-one <http://www.pygtk.org/downloads.html>`_ bundle installer and
   install most of it.

#. **lxml**
   is an awesome library to process xml files, which has unfortunately
   not fully found its way into the standard library. As of this writing
   the latest version with prebuilt binaries is `lxml 2.2.8`_ and installation
   works without troubles.

#. **ASE**
   is needed for the representation of atoms in the frontend. So
   download the latest from the
   `GitLab website <https://gitlab.com/ase/ase/repository/archive.zip?ref=master>`_
   and install it. This has to be installed using e.g. the powershell.
   So after unpacking it, fire up the powershell, cd to the directory
   and run ::

    python setup.py install

   in there. Note that there is currently a slight glitch in the
   `setup.py` script on windows, so open `setup.py` in a text
   editor and find the line saying ::

     version = ...

   comment out the lines above it and hard-code the current version
   number.

#. **kmcos**
   is finally what we are after, so download the latest version
   from `github <http://mhoffman.github.com/kmcos/>`_ and install
   it in the same way as you installed **ASE**.


There are probably a number of small changes you have to make
which are not described in this document. Please post questions
and comments in the
`issues area <https://github.com/mhoffman/kmcos/issues>`_ .



Installing JANAF Thermochemical Tables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can conveniently use gas phase chemical potentials
inserted in rate constant expressions using
JANAF Thermochemical Tables. A couple of molecules
are automatically supported. If you need support
for more gas-phase species, drop me a line.

The tabulated values are not distributed since
the terms of distribution do not permit this.
Fortunately manual installation is easy.
Just create a directory called `janaf_data`
anywhere on your python path. To see the directories on your python
path run ::

    python -c"import sys; print(sys.path)"

Inside the `janaf_data` directory has to be a file
named `__init__.py`, so that python recognizes it as a module ::

    touch __init__.py

Then copy all needed data files from the
`NIST website <http://kinetics.nist.gov/janaf/>`_
in the tab-delimited text format
to the `janaf_data` directory. To download the ASCII file,
search for your molecule. In the results page click on 'view'
under 'JANAF Table' and click on 'Download table in tab-delimited text format.'
at the bottom of that page.



.. _Enthought Python Distribution: http://www.enthought.com/products/epd_free.php
.. _python.org: http://www.python.org/download
.. _lxml 2.2.8: http://pypi.python.org/pypi/lxml/2.2.8
.. todo :: test installation on other platforms
