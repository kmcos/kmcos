from ase.io import write
import pickle

#filehandler opens the pickle file from the runfile_atoms_export.py and unpickles it
filehandler = open('MyFirstDiffusion_atoms_10.pkl', 'rb')
loaded_atoms_object = pickle.load(filehandler)
filehandler.close()

#write creates a .png image of the model's atomic view
write('MyFirstDiffusion_atoms_10.png', loaded_atoms_object)
