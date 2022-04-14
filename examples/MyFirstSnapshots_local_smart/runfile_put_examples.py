from kmcos.snapshots import *
import kmcos.snapshots_globals as sg
import os


"""
This runfile is intended for a user to learn how to use the put function.
"""

sps = 10 # <-- this is just an example
n_snapshots = 10 # <-- this is just an example

#The kmcos Model is initialized in create_headers
create_headers()

#First we will do some snapshots so that the system has done some steps.
do_snapshots(sps, n_snapshots)

#After doing some steps, we can add a species to the surface.
#Frist we will print one of the lattice sub objects.
print(sg.model.lattice.simple_cubic)

#We can see what is the particular species on one of the sites.
sg.model.lattice.get_species([1,1,0, sg.model.lattice.simple_cubic])
print(sg.model.lattice.get_species([1,1,0, sg.model.lattice.simple_cubic]))

#For adjusting species at sites and updating the database of available processes automatically, we will use the "put" function. 
#The put function's documentation and source code are included below

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


#Rather than using the "put" function, we can use the "_put" function. This separates the adjusting species at sites and updating the database of available processes manually
#This is useuful if a person needs to do many (e.g., thousands) of put functions in the middle of a simulation.
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


#We can do some more steps.
do_snapshots(sps=10, n_snapshots=2)

#After finishing a simulation with snapshots, the final command below writes the simulation details to the logfile.  This command only exports information from steps. It is unrelated to the "put" examples we have used and will ignore them.
create_log()
