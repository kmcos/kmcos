model_name = 'MyFirstSnapshots'
simulation_size = 20 #TODO: A. Savara found on 12/04/22 that this is hardcoded in io.py, and it should not be hardcoded. 
random_seed = 1 #TODO: A. Savara found on 12/04/22 that this is hardcoded in io.py, and it should not be hardcoded.

def setup_model(model):
    """ Aug 15th 2022: setup_model is legacy code. Please ignore the rest of this comment and this function. 
    Write initialization steps here.
       e.g. ::
    model.put([0,0,0,model.lattice.default_a], model.proclist.species_a)
    """
    #from setup_model import setup_model
    #setup_model(model)
    pass

# Default history length in graph
hist_length = 30

parameters = {
    "A":{"value":"(3.5*angstrom)**2", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "T":{"value":"600", "adjustable":True, "min":"300.0", "max":"1500.0","scale":"linear"},
    "deltaG":{"value":"-0.5", "adjustable":True, "min":"-1.3", "max":"0.3","scale":"linear"},
    "p_COgas":{"value":"0.2", "adjustable":True, "min":"1e-13", "max":"1000.0","scale":"log"},
    }

rate_constants = {
    "CO_adsorption":("0.1*p_COgas*A*bar/sqrt(2*m_CO*umass/beta)", True),
    "CO_desorption":("p_COgas*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(-deltaG*eV)", True),
    }

site_names = ['simple_cubic_hollow']
representations = {
    "CO":"""Atoms('CO',[[0,0,0],[0,0,1.2]])""",
    "empty":"""""",
    }

lattice_representation = """"""

species_tags = {
    "CO":"""carbon""",
    "empty":"""""",
    }

tof_count = {
    "CO_adsorption":{'CO_adsorption': 1},
    "CO_desorption":{'CO_desorption': 1},
    }

connected_variables={'surroundingSitesDict': {}}
xml = """<?xml version="1.0" ?>
<kmc version="(0, 4)">
    <meta author="Aditya (Ashi) Savara" email="savaraa@ornl.gov" model_name="MyFirstSnapshots" model_dimension="2" debug="0"/>
    <species_list default_species="empty">
        <species name="CO" representation="Atoms('CO',[[0,0,0],[0,0,1.2]])" color="#000000" tags="carbon"/>
        <species name="empty" representation="" color="#ffffff" tags=""/>
    </species_list>
    <parameter_list>
        <parameter name="A" value="(3.5*angstrom)**2" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="T" value="600" adjustable="True" min="300.0" max="1500.0" scale="linear"/>
        <parameter name="deltaG" value="-0.5" adjustable="True" min="-1.3" max="0.3" scale="linear"/>
        <parameter name="p_COgas" value="0.2" adjustable="True" min="1e-13" max="1000.0" scale="log"/>
    </parameter_list>
    <lattice cell_size="3.5 0.0 0.0 0.0 3.5 0.0 0.0 0.0 10.0" default_layer="simple_cubic" substrate_layer="simple_cubic" representation="">
        <layer name="simple_cubic" color="#ffffff">
            <site pos="0.5 0.5 0.5" type="hollow" tags="" default_species="empty"/>
        </layer>
    </lattice>
    <process_list>
        <process rate_constant="0.1*p_COgas*A*bar/sqrt(2*m_CO*umass/beta)" name="CO_adsorption" enabled="True" tof_count="{'CO_adsorption': 1}">
            <condition species="empty" coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="p_COgas*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(-deltaG*eV)" name="CO_desorption" enabled="True" tof_count="{'CO_desorption': 1}">
            <condition species="CO" coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0"/>
        </process>
    </process_list>
    <output_list/>
    <connected_variables connected_variables_string="{'surroundingSitesDict': {}}"/>
</kmc>
"""
if __name__ == "__main__":
    #benchmark if kmc_settings.py is run without additional arguments, else call cli with additional argument provided.
    import sys
    if len(sys.argv) == 1:
        from kmcos import cli
        cli.main("benchmark")
    if len(sys.argv) == 2:
        from kmcos import cli
        cli.main(sys.argv[1])
