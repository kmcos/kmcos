from ase.io import write
import pickle

filehandler = open('MyFirstDiffusion_atoms.pkl', 'rb')
loaded_atoms_object = pickle.load(filehandler)
filehandler.close()
write('MyFirstDiffusion_atoms.png', loaded_atoms_object)
