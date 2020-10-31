#this file is normally used by "import snapshots_globals as sg"
from kmos.run import KMC_Model
from kmc_settings import *
simulation_name = model_name
start = 0.0
model = KMC_Model()
atoms = model.get_atoms(geometry=False)
occ_header_string = model.get_occupation_header()
occ_header_array = occ_header_string.split()
TOF_header_string = model.get_tof_header()
TOF_header_array= TOF_header_string.split()
data_file_name = simulation_name + str('TOFs_and_Coverages.csv')
parameters_of_interest = ['T']
steps_so_far = 0
snapshots_so_far = 0
write_output = 'True'
TOF_data_list = []
TOF_integ_list = []
occ_data_list = []
last_snapshot_outputs = []
snapshot_output_headers = []
sp_steps = 0.0
sp_steps_initial = 0.0
kmc_time = sg.atoms.kmc_time
#to get atoms.kmc_time access it by from sg.atoms.kmc_time
