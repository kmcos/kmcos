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
#The put function's documentation and source code are included below this function call, and also explain how to know what species and sites options are available.
sg.model.put(site = [1,1,0, sg.model.lattice.simple_cubic_hollow], new_species = sg.model.proclist.empty)
"""
Function: put(self, site, new_species, reduce=False)

Puts new_species at site. The site is given by 4-entry sequence like [x, y, z, n], 
where the first 3 entries define the unit cell from 0 to the number of unit cells in the respective direction. 
And n specifies the site within the unit cell.

The database of available processes will be updated automatically.

    Example ::

        model.put([0,0,0,model.lattice.site], model.proclist.co ])
        # puts a CO molecule at the `bridge` site
        # of the lower left unit cell

:param site: Site where to put the new species, i.e. [x, y, z, bridge]
:type site: list or np.array
:param new_species: Name of new species.
:type new_species: str
:param reduce: Of periodic boundary conditions if site falls out site
                lattice (Default: False)
:type reduce: bool

In this case, '[1,1,0, sg.model.lattice.simple_cubic_hollow]' is the site and
'sg.model.proclist.empty' is the new species. 'sg.model.lattice.simple_cubic_hollow' is the site name.

To see all the available site names, check the site_name in kmc_settings.py.
    Ex: site_names = ['simple_cubic_hollow']
    set site name as 'sg.model.lattice.simple_cubic_hollow'
    
    Ex: site_names = ['ruo2_bridge', 'ruo2_cus', 'ruo2_Burrowed']
    set site name as 'sg.model.lattice.ruo2_bridge' or 'sg.model.lattice.ruo2_cus' or 'sg.model.lattice.ruo2_Burrowed'

To see all the available species names, check the species_tags in kmc_settings.py.
    Ex: species_tags = {
            "CO":"""""",
            "O":"""""",
            "empty":"""""",
            }
"""


#Rather than using the "put" function, we can use the "_put" function. This separates the adjusting species at sites and updating the database of available processes manually
#This is useuful if a person needs to do many (e.g., thousands) of put functions in the middle of a simulation.
sg.model._put(site = [1,1,0, sg.model.lattice.simple_cubic_hollow], new_species = sg.model.proclist.empty)
sg.model._adjust_database() #This must be called when using ._put() to update the database

"""
Function: _put(self, site, new_species, reduce=False)

Works exactly like put, but without updating the database of
        available processes. This is faster for when one does a lot updates
        at once, however one must call _adjust_database afterwards.

        Examples ::

            model._put([0,0,0,model.lattice.lattice_bridge], model.proclist.co])
            # puts a CO molecule at the `bridge` site of the lower left unit cell

            model._put([1,0,0,model.lattice.lattice_bridge], model.proclist.co])
            # puts a CO molecule at the `bridge` site one to the right

            # ... many more

            model._adjust_database() # Important! This updates the database.

:param site: Site where to put the new species, i.e. [x, y, z, bridge]
        :type site: list or np.array
        :param new_species: Name of new species.
        :type new_species: str
        :param reduce: Of periodic boundary conditions if site falls out
                       site lattice (Default: False)
        :type reduce: bool

In this case, '[1,1,0, sg.model.lattice.simple_cubic_hollow]' is the site and
'sg.model.proclist.empty' is the new species. 'sg.model.lattice.simple_cubic_hollow' is the site name.

To see all the available site names, check the site_name in kmc_settings.py.
    Ex: site_names = ['simple_cubic_hollow']
    set site name as 'sg.model.lattice.simple_cubic_hollow'
    
    Ex: site_names = ['ruo2_bridge', 'ruo2_cus', 'ruo2_Burrowed']
    set site name as 'sg.model.lattice.ruo2_bridge' or 'sg.model.lattice.ruo2_cus' or 'sg.model.lattice.ruo2_Burrowed'

To see all the available species names, check the species_tags in kmc_settings.py.
    Ex: species_tags = {
            "CO":"""""",
            "O":"""""",
            "empty":"""""",
            }
"""


#We can do some more steps.
do_snapshots(sps=10, n_snapshots=2)

#After finishing a simulation with snapshots, the final command below writes the simulation details to the logfile.  This command only exports information from steps. It is unrelated to the "put" examples we have used and will ignore them.
create_log()
