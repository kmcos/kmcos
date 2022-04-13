from kmcos.snapshots import *
import kmcos.snapshots_globals as sg
import os

#Below sets up some "options" for running the snapshots.
sg.parameters_of_interest = None #['T','R'] #<-- put the parameters you want exported with each snapshot here. Can also put activation energy etc.
sps = 10 # <-- this is just an example
n_snapshots = 10 # <-- this is just an example


create_headers()

do_snapshots(sps, n_snapshots)

# sg.model.get_species_coords(filename_csv = "meshgrid", directory = "./mesh", matrix_format = "meshgrid")

# import numpy as np
# config = sg.model._get_configuration()
# #print(config)
# matrix_array = config * 1.0

# #print(matrix_array)
# matrix_array = matrix_array[:5]
# #print(matrix_array)

# im = np.reshape(matrix_array, (10,10))
# print(im)
# counter = 1

# # Alters the current meshgrid to 0 through 100
# # for row in range(len(im)):
# #     for column in range (len(im[0])):
# #         im[row][column] = counter
# #         counter+=1

# np.savetxt("./mesh" + "/meshgrid.csv", np.array(im, dtype = "object"), delimiter=", ", fmt="%s") 

# # path = r'C:\Users\Meelo\kmcos18\kmcos\examples\MyFirstSnapshots_local_smart\mesh\meshgrid.txt'
# # from PIL import Image
# # im = Image.open(path)

# # M = im.shape[0]//2
# # N = im.shape[1]//2
# M = 5
# N = 5
# # tiles = [im[x:x+M,y:y+N] for x in range(0,im.shape[0],M) for y in range(0,im.shape[1],N)]

# #print(tiles) #current does not print anything
# # print(im)
# # # center_values = np.vstack(tiles[2:8, 2:8])
# # print(center_values)

# # Getting all the possible local configurations (Note: only supports squares)

# # Functionaize this get_local_configurations()
# # return a bunch of tiles, returns subsquarelist, optional argument to save to .npy
# nRows = len(im)
# nCols = len(im[0])
# radius = 2 #basically UpToDistance
# sidel = 1+(2*radius)
# cornersRow = np.arange(nRows - sidel + 1)[:, np.newaxis, np.newaxis, np.newaxis]
# cornersCol = np.arange(nCols - sidel + 1)[np.newaxis, :, np.newaxis, np.newaxis]
# corners = im[cornersRow, cornersCol]
# subsquareRow = cornersRow + np.arange(sidel)[:, np.newaxis]
# subsquareCol = cornersCol + np.arange(sidel)
# subsquares = im[subsquareRow, subsquareCol]
# subsquareList = subsquares.reshape(-1, sidel, sidel)

# # TODO Now taking the set to get only the unique values
# # for row in range(len(subsquareList)): (loop to make each array into a list)

# # subsquareListAsStrings = list(np.array(subsquareList, dtype = "str"))
# # print(subsquareListAsStrings)

# # subsquaresSet = set(subsquareListAsStrings)
# # uniqueSubsquaresList = list(subsquareList)

# np.save(file="local_configurations.npy", arr=subsquareList)
# data = np.load("local_configurations.npy") 

# #print(data)

# # print(im)
# # print(data)
# # print(len(data))
# #print(subsquareRow)
# # print("break")
# # print(cornersRow)
# #print(subsquares)
# # print(len(subsquaresSet))
# # print(len(uniqueSubsquaresList))

sg.model.get_local_configuration(directory = "./test", meshgrid=sg.model.get_species_coords(export_csv=False, matrix_format='meshgrid'))
