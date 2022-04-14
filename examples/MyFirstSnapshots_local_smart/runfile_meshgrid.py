from kmcos.snapshots import *
import kmcos.snapshots_globals as sg
import numpy as np
import os

#Below sets up some "options" for running the snapshots.
sg.parameters_of_interest = None #['T','R'] #<-- put the parameters you want exported with each snapshot here. Can also put activation energy etc.
sps = 10 # <-- this is just an example
n_snapshots = 10 # <-- this is just an example


create_headers()

do_snapshots(sps, n_snapshots)

meshgrid=sg.model.get_species_coords(export_csv=False, matrix_format='meshgrid')
sg.model.get_local_configuration(meshgrid = meshgrid, radius = 2, filename = "unique_local_configurations", directory = "./local_configurations")