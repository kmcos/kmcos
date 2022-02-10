model_name = 'MyFirstSnapshots'
simulation_size = 20
random_seed = 1

def setup_model(model):
    """Write initialization steps here.
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

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Aditya (Ashi) Savara" debug="0" email="savaraa@ornl.gov" model_dimension="2" model_name="MyFirstSnapshots"/>
    <species_list default_species="empty">
        <species color="#000000" name="CO" representation="Atoms('CO',[[0,0,0],[0,0,1.2]])" tags="carbon"/>
        <species color="#ffffff" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="False" max="0.0" min="0.0" name="A" scale="linear" value="(3.5*angstrom)**2"/>
        <parameter adjustable="True" max="1500.0" min="300.0" name="T" scale="linear" value="600"/>
        <parameter adjustable="True" max="0.3" min="-1.3" name="deltaG" scale="linear" value="-0.5"/>
        <parameter adjustable="True" max="1000.0" min="1e-13" name="p_COgas" scale="log" value="0.2"/>
    </parameter_list>
    <lattice cell_size="3.5 0.0 0.0 0.0 3.5 0.0 0.0 0.0 10.0" default_layer="simple_cubic" representation="" substrate_layer="simple_cubic">
        <layer color="#ffffff" name="simple_cubic">
            <site default_species="empty" pos="0.5 0.5 0.5" tags="" type="hollow"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="CO_adsorption" rate_constant="0.1*p_COgas*A*bar/sqrt(2*m_CO*umass/beta)" tof_count="{'CO_adsorption': 1}">
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_desorption" rate_constant="p_COgas*bar*A/sqrt(2*pi*umass*m_CO/beta)*exp(-deltaG*eV)" tof_count="{'CO_desorption': 1}">
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="CO"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="empty"/>
        </process>
    </process_list>
    <output_list/>
</kmc>
"""
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        from kmcos import cli
        cli.main("benchmark")
    if len(sys.argv) == 2:
        from kmcos import cli
        cli.main(sys.argv[1])
