The examples are currently categorized into separate cases to demonstrate various features.
Below is a list of the examples, then explanation of how to use them.

* MyFirstDiffusion shows an example of diffusion.
* MyFirstSnapshots shows an example of how to use snapshots with chemical reactions on surfaces (typical usage).
* MyFirstThrottling shows how to use rate constant rescaling to accelerate fast frivolous processes (to 'solve' the KMC Stiffness problem).
* MyFirstTPD... series shows various ways of running a temperature programmed reaction (TPD/TPR). This feature will become standardized in KMCOS in the future, to make running temperature programmed simulations more user friendly. Such a module has not been made yet, but we would welcome a user helping with this task. It will not take long for someone who knows python and A. Savara can provide guidance, he is just working on other items.

To use one of the examples, follow this type of procedure:

python3 MyFirstSnapshots__build.py
cd MyFirstSnapshots_local_smart
python3 runfile.py

The first command uses a python file to create a chemical model (process definitions) and a KMC modeling executable as well. The “local_smart” is the default backend (default “KMC Engine”, kmcos has several).

After the simulation has run, you will see a csv file named runfile_TOFs_and_Coverages.csv , open this file to see your first KMC output!

Various examples exist. More features and a thorough tutorial are forthcoming. Please join the kmcos-users group https://groups.google.com/g/kmcos-users and email any questions if you get stuck.

