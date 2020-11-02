#this file is normally used by "import snapshots_globals as sg"
import kmos.run
import kmc_settings

simulation_name = kmc_settings.model_name
start = 0.0
model = kmos.run.KMC_Model()
atoms = model.get_atoms(geometry=False)
occ_header_string = model.get_occupation_header()
occ_header_array = occ_header_string.split()
TOF_header_string = model.get_tof_header()
TOF_header_array = TOF_header_string.split()
data_file_name = simulation_name + str('_TOFs_and_Coverages.csv')
parameters_of_interest = ['T']
steps_so_far = 0
snapshots_so_far = 0
write_output = True
TOF_data_list = []
TOF_integ_list = []
occ_data_list = []
last_snapshot_outputs = []
snapshot_output_headers = []
kmc_time = atoms.kmc_time * 1
config = model._get_configuration().tolist()
PRNG_state = None
steps_before_snapshot = 0.0
sps_actual = 0
tps_actual = 0
snapshots_sampling = None

# List of variables to save. *DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOU ARE
# DOING!*
__var_list__ = ['simulation_name', 'start', 'occ_header_string',
    'occ_header_array', 'TOF_header_string', 'TOF_header_array',
    'data_file_name', 'parameters_of_interest', 'steps_so_far',
    'snapshots_so_far', 'write_output', 'TOF_data_list', 'TOF_integ_list',
    'occ_data_list', 'last_snapshot_outputs', 'snapshot_output_headers',
    'kmc_time', 'config', 'PRNG_state', 'steps_before_snapshot',
    'sps_actual', 'tps_actual', 'snapshots_sampling']
