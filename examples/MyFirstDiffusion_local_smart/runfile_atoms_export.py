import pickle
from kmcos.run import KMC_Model

model = KMC_Model()
NSTEPS = 1e6
model.do_steps(NSTEPS)
model.pickle_export_atoms("MyFirstDiffusion_atoms_" + str(NSTEPS) + ".pkl")