model_name = 'MyFirstTPD_Precovered'
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
    "A_CO_des":{"value":"14500000000000.0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_act_des":{"value":"84000", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "R":{"value":"8.314", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "T":{"value":"600", "adjustable":True, "min":"150.0", "max":"500.0","scale":"linear"},
    "deltaG":{"value":"-0.5", "adjustable":True, "min":"-1.3", "max":"0.3","scale":"linear"},
    "p_COgas":{"value":"0.2", "adjustable":True, "min":"1e-13", "max":"1000.0","scale":"log"},
    }

rate_constants = {
    "CO_desorption":("A_CO_des*exp(-E_act_des/(R*T))", True),
    "Do_nothing":("0", True),
    }

site_names = ['simple_cubic_coord1']
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
    "CO_desorption":{'CO_Desorption': 1},
    "Do_nothing":{'Do_nothing': 1},
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Christa Cody" email="codycn@ornl.gov" model_name="MyFirstTPD_Precovered" model_dimension="2" debug="0"/>
    <species_list default_species="empty">
        <species name="CO" representation="Atoms('CO',[[0,0,0],[0,0,1.2]])" color="#000000" tags="carbon"/>
        <species name="empty" representation="" color="#ffffff" tags=""/>
    </species_list>
    <parameter_list>
        <parameter name="A" value="(3.5*angstrom)**2" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="A_CO_des" value="14500000000000.0" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_act_des" value="84000" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="R" value="8.314" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="T" value="600" adjustable="True" min="150.0" max="500.0" scale="linear"/>
        <parameter name="deltaG" value="-0.5" adjustable="True" min="-1.3" max="0.3" scale="linear"/>
        <parameter name="p_COgas" value="0.2" adjustable="True" min="1e-13" max="1000.0" scale="log"/>
    </parameter_list>
    <lattice cell_size="3.5 0.0 0.0 0.0 3.5 0.0 0.0 0.0 10.0" default_layer="simple_cubic" substrate_layer="simple_cubic" representation="">
        <layer name="simple_cubic" color="#ffffff">
            <site pos="0.5 0.5 0.5" type="coord1" tags="" default_species="CO"/>
        </layer>
    </lattice>
    <process_list>
        <process rate_constant="A_CO_des*exp(-E_act_des/(R*T))" name="CO_desorption" enabled="True" tof_count="{'CO_Desorption': 1}">
            <condition species="CO" coord_layer="simple_cubic" coord_name="coord1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="simple_cubic" coord_name="coord1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="0" name="Do_nothing" enabled="True" tof_count="{'Do_nothing': 1}">
            <condition species="CO" coord_layer="simple_cubic" coord_name="coord1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="simple_cubic" coord_name="coord1" coord_offset="0 0 0"/>
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
