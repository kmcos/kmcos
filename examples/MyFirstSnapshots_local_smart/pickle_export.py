from ase.io import write
import pickle

filehandler = open('atoms_export.pkl', 'rb')
loaded_atoms_object = pickle.load(filehandler)
filehandler.close()
write('atoms_export.png', loaded_atoms_object)

