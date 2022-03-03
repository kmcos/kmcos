Introduction
^^^^^^^^^^^^

kmcos is designed for lattice based Kinetic Monte Carlo simulations to understand chemical kinetics and mechanisms. It has been used to produce more than 10 scientific publications. The best way to learn how to use kmcos is by following the examples.

If you have already followed the kmcos installation instructions and still have the kmcosInstallation directory, then navigate to /kmcosInstallation/kmcos/examples 

If you do not have that directory, but have kmcos installed, go to https://github.com/kmcos/kmcos Click on the green button and download zip, to get the examples.

Inside /examples/, run the following commands ::

    python3 MyFirstSnapshots__build.py
    cd MyFirstSnapshots_local_smart
    python3 runfile.py

The first command uses a python file to create a chemical model (process definitions) and a KMC modeling executable as well.
The "local_smart" is the default backend (default "KMC Engine", kmcos has several).

After the simulation has run, you will see a csv file named runfile_TOFs_and_Coverages.csv, open this file to see your first KMC output!

Various examples exist. More features and a thorough tutorial are forthcoming. Please join the kmcos-users group https://groups.google.com/g/kmcos-users and email any questions if you get stuck.

.. automodule:: kmcos
