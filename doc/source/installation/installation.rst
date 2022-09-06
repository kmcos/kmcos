Kmcos has some non-python dependencies so cannot be installed with only pip. It is recommended to install kmcos on Ubuntu within a python virtual environment, and our instructions are written accordingly.
If you plan to use a windows machine, it is recommended to first get `VirtualBox <https://www.virtualbox.org/wiki/Downloads>`_ 
and to `make an Ubuntu virtualmachine <https://www.freecodecamp.org/news/how-to-install-ubuntu-with-oracle-virtualbox/>`_ .

Making a Python Virtual Environment for kmcos within Ubuntu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using a virtual python environment for both installation and for simulations avoids python software conflicts. Here are instructions for installing a python virtual environment.

OPTION 1 (python3-venv)::

    cd ~
    sudo apt-get update
    sudo apt-get install python3
    sudo apt-get install python3-venv
    python3 -m venv ~/VENV/kmcos
    source ~/VENV/kmcos/bin/activate

To use kmcos after this installation, you will need to use that source activation command from the terminal each time.  When finished, you can exit this virtualenv by typing 'deactivate'. 

OPTION 2 (virtualenv)::

    cd ~
    sudo apt-get update
    sudo apt-get install python3
    sudo apt-get install virtualenv
    virtualenv -p /usr/bin/python3 ~/VENV/kmcos  #If this fails, try typing "which python3" and replace the path "/usr/bin/python3" with what your system provides.
    source ~/VENV/kmcos/bin/activate

To use kmcos after this installation, you will need to use that source activation command from the terminal each time.  When finished, you can exit this virtualenv by typing 'deactivate'. Though you should not need it, you can find more information on virtualenv at `this video <https://www.youtube.com/watch?v=N5vscPTWKOk>`_  and `the official website <https://virtualenv.pypa.io/en/latest/>`_   

OPTION 3 (anaconda): 
If you will be installing kmcos in an anaconda environment, you can make a new environment named 'kmcos' from anaconda navigator. See for example `this link <https://medium.com/cluj-school-of-ai/python-environments-management-in-anaconda-navigator-ad2f0741eba7>`_ . 


Virtual environment installations do not require the "--user" tag as the python packages are 'sandboxed' during installation. Accordingly, the "--user" tags are commented out in our further instructions.

Installing kmcos on Ubuntu Linux 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are a typical user, first make sure you are in your virtual environment (after preparation by the above instructions)::

    source ~/VENV/kmcos/bin/activate

The easiest way to install kmcos is to use one of the automatic installers::

    cd ~
    sudo apt-get install git
    git clone https://github.com/kmcos/kmcos-installers
    cd kmcos-installers
    bash install-kmcos-linux-venv.bash #use 'bash install-kmcos-linux-user.bash' if you are not using a venv.  #For the develop branch, use install-kmcos-linux-venv-develop.bash or install-kmcos-linux-user-develop.bash
    
    
For personal computer usage (not on a supercomputer), it is a good idea to also run the following command, which will add the kmcos viewer and movie maker::

    bash install-kmcos-complete-linux-venv-Ubuntu20.bash #this is for Ubuntu20. There is also an Ubuntu18 version.
    
If everything has gone well, you have a minimal installation completed! And now you are done and can leave this installation page!

If the above simple way does not work for you, you will need to go through the commands manually one at a time from `installation on a venv <https://github.com/kmcos/kmcos-installers/blob/main/install-kmcos-linux-venv.bash>`_ or `installation as a user <https://github.com/kmcos/kmcos-installers/blob/main/install-kmcos-linux-user.bash>`_ . A kmcosInstallation directory is created during installation. The files in the kmcosInstallation are no longer needed after installation, but it has exampples in it.  So you can you can navigate into that directory and go through the examples, or you can remove the kmcosInstallation directory using 'rm -r directoryname'.

When doing kmcos upgrades, you will not need to use git again. For kmcos upgrades, you can just use the earlier pip command::

    pip3 install kmcos[MINIMAL] --upgrade #--user

(Optional) If you would like to use the kmcos view capability, you will need to install some non-python dependencies and then kmcos complete::

    sudo apt-get install python-ase
    sudo apt-get install python3-gi
    pip3 install ase #--user
    pip3 install kmcos[COMPLETE] --upgrade #--user

If the last command of 'pip3 install kmcos[COMPLETE] --upgrade #--user' gives an error before finishing, try the command a second time.



Installing kmcos on Fedora Linux (typically inside a virtual environment)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install developement tools gcc and fortran.

For fedora 32+ ::

    sudo dnf groupinstall "Development Tools" "Development Libraries"
    sudo dnf install gcc-gfortran

For fedora below 32 ::

    sudo dnf groupinstall @development-tools @development-libraries
    sudo dnf install gcc-gfortran

Make a virtual environment for the kmcos and activate it::

    python3 -m venv ~/VENV/kmcos
    source ~/VENV/kmcos/bin/activate

Clone the kmcos github repository in a folder you want and change to the kmcos directory::

    git clone https://github.com/kmcos/kmcos.git
    cd kmcos

Install the python package requirements and finally the kmcos package::

    pip3 install numpy lxml ase matplotlib UnitTesterSG CiteSoft IPython
    python3 setup.py install

Installation on openSUSE 12.1 Linux (Deprecated Instructions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On a recent openSUSE some dependencies are distributed a little
different but nevertheless doable. We start by install some
package from the repositories::

  sudo zypper install libgfortran46, python-lxml, python-matplotlib, \
                      python-numpy, python-numpy-devel, python-goocanvas,
                      python-imaging

And two more packages SUSE packages have to be fetched from the
openSUSE `build service <https://build.opensuse.org/>`_

- `gazpacho <https://build.opensuse.org/package/files?package=gazpacho&project=home%3Ajoshkress>`_
- `python-kiwi <https://build.opensuse.org/package/files?package=python-kiwi&project=home%3Ajoshkress>`_


For each one just download the \*.tar.bz2 files. Unpack them and inside
run::

  python setup.py install

In the same vein you can install ASE. Download a recent version
from the `GitLab website <https://gitlab.com/ase/ase/repository/archive.zip?ref=master>`_
unzip it and install it with::

  python setup.py install



Installation on openSUSE 13.1 Linux (Deprecated Instructions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to use the editor GUI you will want to install python-kiwi (not KIWI)
and right now you can find a recent build `here <https://build.opensuse.org/package/show/home:leopinheiro/python-kiwi>`_ .

Installation on Mac OS X 10.10 or above (Deprecated Instructions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is more than one way to get required dependencies. MacPorts was previously tested and worked.

#. Get MacPorts
    Search for MacPorts online, you'll need to install Xcode in the process

#. Install Python, lxml, numpy, ipython, ASE, gcc48. I assume you are using Python 2.7.
   kmcos has not been thoroughly tested with Python 3.X, yet, but should not be too hard.
    Having MacPorts this can be as simple as::

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

Direct installation on windows is currently not supported, but it is possible to use either "WSL" or to use Ubuntu on a virtualbox. It is recommended to download virtualbox, to install Ubuntu, and then follow the Ubuntu installation instructions in the intro2kmcos pdf file here: https://github.com/kmcos/intro2kmcos. You may need to adjust the resolution to work effectively.

If you prefer to use WSL rather than Virtualbox, you will need to install WSL Ubuntu. Press the "start menu" button.  Type "Windows Powershell" but don't press enter:  Use run as administrator. Then enter::
    
    wsl --install -d Ubuntu

Now, you can close the Powershell window. Within ubuntu, use::

    sudo apt update
    sudo apt install x11-apps

From the terminal, type::

    xeyes &

With windows 11 and higher, you may see a GUI pop up. If you do not, then you probably will not be able to use a GUI with WSL, and the kmcos export_movie feature also will not work.

For future reference: "cd ~" will take you to the home (default) place for working in WSL Ubuntu, while "cd /" will take you to the root directory of WSL Ubuntu. 

For sharing files, "cd /mnt/c" will let you access files on to go to the windows C drive.
By going to mnt/c, you can move files back and forth between Ubuntu directories and the Windows directories.

Now that you have WSL working with Ubuntu, follow the regular instructions from the top of this Installation page. Going forward, you can start WSL Ubuntu by finding Ubuntu in the windows start menu.

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
path run::

    python -c"import sys; print(sys.path)"

Inside the `janaf_data` directory has to be a file
named `__init__.py`, so that python recognizes it as a module::

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
.. todo:: test installation on other platforms
