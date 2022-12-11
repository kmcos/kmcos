There are two separate subdirectories here for the CO_O_RuO2_110.py model that was used in this publication:
https://doi.org/10.1021/acscatal.8b00713
The models here are chemically the same as from the zenodo repository,
https://zenodo.org/record/6028197#.Y5VJ_H3MLJ9
but have been updated to the current kmcos syntax (as of Dec 10th 2022)

The interactions module was used here for including pairwise interactions up to 1st nearest neighbor with  a BEP relation.
This requires defining which sites are surrounding any given site,
and requires defining the pairwise interactions term,
and requires defining a BEP relation for each reaction type.

One can choose the distance up to which the neighbors interactions should be considered.
There are examples here for UpToDistanceSetTo0 and UpToDistanceSetTo1

Note that UpToDistanceSetTo1 generates a 27MB xml file in about 5 minutes (30 minutes if including validation is set to True).
Then the compiling of UpToDistanceSetTo1 can take up to 30 hours. 

While UpToDistanceSetTo0 can work with either the lat_int or local_smart backend, UpToDistanceSetTo1 requires the lat_int backend to compile (With the local_smart backend it will cause a computer to run out of memory and freeze up).