In KMC TPD/TPR, there can be big problems if the temperature is started too low or if the simulation is allowed to run past all of the molecules desorbing. Runfile 3 has an advanced algorithm that solves this problem. For runfile 1 and runfile 2, we simply use 300K to 325K as a temperature range that we know will work without any issues for the particular number of sites and activation energy used in those examples.

runfile 1 is using the snasphots module
runfile 2 is using the snasphots module and export import to show how to stop a simulation partway and continue it along the exact same trajectory.
Runfile 3 has an advanced algorithm that solves this problem.
runfile 3 is showing a more complex TPR API that will be incorporated 'directly' into kmcos but has not been yet. (Though when it is incorporated, the resets will require PRNG resets also).


For the runfile3 TPD example, the activation energy is typical for an adsorbate desorbing. 

You should use these settings:
Starting temperature = 200 
Final temperature = 700
Max steps: 30
Min steps: 10