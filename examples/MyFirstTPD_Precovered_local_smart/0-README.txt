This is an example of a TPD, but this is also a set of examples for the the load and restart feature as well as the tps feature.

In KMC TPD/TPR, there can be big problems if the temperature is started too low or if the simulation is allowed to run past all of the molecules desorbing.  For runfile 1 and runfile 2, we simply use 300K to 325K as a temperature range that we know will work without any issues for the particular number of sites and activation energy used in those examples. Some of the other TPD/TPR examples have more complex algorithms.

****
Runfile 7 was made to show how to do this with a good flow. Let's look in that file.
There are some loading features. Let's ignore that for now.

We see that we set the "steps per snapshot" and the "time per snapshot" between lines 50 and 60. The tps is set at 1.0, which means that anytime a snapshot reaches beyond 1 second of simulation time, the snapshot will end without doing further steps (so the actual steps per snapshot will not be constant). For example, if the sps is set at 100 steps but tps is set at , if 1 second is reached after 43 steps, then the snapshot will end at 43 steps instead of finishing all 100 steps.

In this runfile, for the temperature programmed reaction, we also set the initial temperature, final temperature, and heating rate for the temperature programmed reaction. Near the bottom of the file is a loop that goes across temperatures.

Now, try running this runfile.
After the file is run, open the TOFs file produced by the snapshots module. Make a scatter plot with the x axis as temperature and the Y axis as the TOF_data , and make another for TOF_integ.
Save this plotting file.

Now, open the runfile, change the TPS to 0.1, run again, and make the same plots.

****

runfile 1 is using the snasphots module.
runfile 2 and runfile 3 are using the snapshots module and export import to show how to stop a simulation partway and continue it along the exact same trajectory as runfile 1.  Runfile 2 exports and stops once the temperature is above 310K and then continues.  It is important to recognize that "T" after "T_incr" is the temperature at the end of a snapshot, and serves as the temperature for the beginning of the next snapshot.
Runfile 4 uses save, load, restart in a single runfile, and was used as a check when making runfile 2+3.
Runfile 5 uses the tps feature. It has an sps of 1000, which serves as a maximum sps, and a tps of 1.0 s.  For this example, each snapshot is around 1.0 second since (for these conditions) 1000 steps is not required to reach 1.0 s.
Runfile 6 uses the tps feature, It has an sps of 20, which is such that the first two snapshots are time limited, and then the later snapshots are limited by the sps.

