This is a KMC model for methanation published in:
The Journal of Chemical Physics 147, 152705 (2017); doi: 10.1063/1.4989511

The model uses scaling expressions for the rate constants,
whose parameters are read from the file: 
methanation_kmc_adsorbate_scaling_input.txt

It also uses thermochemistry corrections from ASE, 
where the harmonic approximation is used for the adsorbates
and the ideal gas approximation is used for the gas-phase species.
The frequencies for all species are also read from the file.

The model can also be run using the temporal acceleration algorithm.

All three things are tested simultaneously in the test run. 

The last 5 snapshots are longer in length to ensure steady state, and then the output is tested.

The test takes around 5 minutes to run.

Note: For a quicker test, we could do 2 snapshots at the end rather than 5, which will reduce the test to around 2 minutes.  Then, we would test only index 0 of the TOF_data since the CH4 TOF_data seems to converge sooner than the H2O TOF_data.