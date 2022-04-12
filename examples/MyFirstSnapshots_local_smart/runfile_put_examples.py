from kmcos.snapshots import *
import kmcos.snapshots_globals as sg
import os

#sg.simulation_name = model_name  #<--- You can change this to whatever you want, but this is the default. All it does is affect the filenames of the exports the format for this type would be MyFirstModel_TOFs_and_Coverages.csv.
#other common options are:
#sg.simulation_name = os.path.basename(__file__)[:-3] #<--- Uses the runfile name as part of the file names i.e. runfile_TOFs_and_Coverages.csv  . The [:-3] is to remove the ".py" from the end of the filename.
#sg.simulation_name = '%s_%s' %(model_name,random_seed) #<--- Includes the model_name and random seed (e.g., 6483) used for the KMC as part of the file names e.g., MyFirstModel_6483_TOFs_and_Coverages.csv


#Below sets up some "options" for running the snapshots.
sg.parameters_of_interest = None #['T','R'] #<-- put the parameters you want exported with each snapshot here. Can also put activation energy etc.
sps = 10 # <-- this is just an example
n_snapshots = 10 # <-- this is just an example


#The kmcos Model is initialized in create_headers
create_headers()

#If it is desired to run snapshots without writing output to a file, set sg.write_output = 'False'.
#If you want to start writing again, set sg.write_output = 'True' before running
#more snapshots.

#If you need to change a parameter after each snapshot, only do 1 snapshot at a time with n_snapshots=1.
do_snapshots(sps, n_snapshots)

#do_snapshots(500, 2) <-- here is another example of how to use the syntax.

#If you want to dump a configuration between snapshots, you may want to do something
#like this.
#sg.model.dump_config(sg.simulation_name + str(sg.steps_so_far))#


#below are  some examples of  arrays and lists that may be of interest.
#print sg.occ_header_array
#print sg.TOF_data_list
#print sg.occ_data_list
#print("line 40 of the runfile, sg.last_snapshot_outputs:", sg.last_snapshot_outputs)
#print("line 41 of the runfile, sg.snapshot_output_headers:", sg.snapshot_output_headers)


#The final command below writes the simulation details to the logfile
create_log()

#Adjusting species at sites and updating the database of available processes automatically
print(sg.model.lattice.simple_cubic)
sg.model.put([1,1,0, sg.model.lattice.simple_cubic_hollow], sg.model.proclist.empty)

"""
Function: put(self, site, new_species, reduce=False)

site: Site where to put the new species, i.e. [x, y, z, bridge]

Puts new_species at site. The site is given by 4-entry sequence like [x, y, z, n], 
where the first 3 entries define the unit cell from 0 to the number of unit cells in the respective direction. 
And n specifies the site within the unit cell.

In this case, '[1,1,0, sg.model.lattice.simple_cubic_hollow]' is the site and
'sg.model.proclist.empty' is the new species.

To know what species name to use, check the Layer name in the build file.
    Ex: layer = kmc_model.add_layer(name='simple_cubic')
        layer.sites.append(Site(name='hollow', pos='0.5 0.5 0.5',
                        default_species='empty'))
    
    set site as 'sg.model.lattice.simple_cubic_hollow'
    
    Ex: layerName = 'ruo2'
        layer = Layer(name=layerName)
        layer.sites.append(Site(name='bridge', pos='0.0 0.5 0.7'))
        layer.sites.append(Site(name='cus', pos='0.5 0.5 0.7'))
        layer.sites.append(Site(name='Burrowed', pos='0.0 0.0 0.0')) #This is for the pace-restrictor reaction

    set site as 'sg.model.lattice.ruo2_bridge' or 'sg.model.lattice.ruo2_cus' or 'sg.model.lattice.ruo2_Burrowed'

The database of available processes will be updated automatically."""


#Adjusting species at sites and updating the database of available processes manually
sg.model._put([1,1,0, sg.model.lattice.simple_cubic_hollow], sg.model.proclist.empty)
sg.model._adjust_database() #This must be called when using ._put() to update the database

"""
Function: put(self, site, new_species, reduce=False)

site: Site where to put the new species, i.e. [x, y, z, bridge]

Puts new_species at site. The site is given by 4-entry sequence like [x, y, z, n], 
where the first 3 entries define the unit cell from 0 to the number of unit cells in the respective direction. 
And n specifies the site within the unit cell.

In this case, '[1,1,0, sg.model.lattice.simple_cubic_hollow]' is the site and
'sg.model.proclist.empty' is the new species.

To know what species name to use, check the Layer name in the build file.
    Ex: layer = kmc_model.add_layer(name='simple_cubic')
        layer.sites.append(Site(name='hollow', pos='0.5 0.5 0.5',
                        default_species='empty'))
    
    set site as 'sg.model.lattice.simple_cubic_hollow'
    
    Ex: layerName = 'ruo2'
        layer = Layer(name=layerName)
        layer.sites.append(Site(name='bridge', pos='0.0 0.5 0.7'))
        layer.sites.append(Site(name='cus', pos='0.5 0.5 0.7'))
        layer.sites.append(Site(name='Burrowed', pos='0.0 0.0 0.0')) #This is for the pace-restrictor reaction

    set site as 'sg.model.lattice.ruo2_bridge' or 'sg.model.lattice.ruo2_cus' or 'sg.model.lattice.ruo2_Burrowed'

The database of available processes will be updated automatically.

Note: This function works the same as the .put(), which is the one above, except that the database
of available processes does not update automatically. You must call sg.model._adjust_database() to do so.

The benefit of this function over the other is that this is much faster when doing multiple updates,
as the database is not updated until the end."""


#Getting the species from the sites
sg.model.lattice.get_species([1,1,0, sg.model.lattice.simple_cubic])