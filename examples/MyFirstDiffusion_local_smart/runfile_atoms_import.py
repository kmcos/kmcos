from ase.io import write
import pickle

filehandler = open('MyFirstDiffusion_atoms_1000000.0.pkl', 'rb')
loaded_atoms_object = pickle.load(filehandler)
filehandler.close()
write('MyFirstDiffusion_atoms_1000000.0.png', loaded_atoms_object)
