In KMC TPD/TPR, there can be big problems if the temperature is started too low or if the simulation is allowed to run past all of the molecules desorbing.  For runfile 1 and runfile 2, we simply use 300K to 325K as a temperature range that we know will work without any issues for the particular number of sites and activation energy used in those examples. Some of the other TPD/TPR examples have more complex algorithms.

runfile 1 is using the snasphots module
runfile 2 is using the snasphots module and export import to show how to stop a simulation partway and continue it along the exact same trajectory.
