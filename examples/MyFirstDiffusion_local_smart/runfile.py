import pickle
from kmcos.run import KMC_Model

model = KMC_Model()
NSTEPS = 1e6
model.do_steps(NSTEPS)
