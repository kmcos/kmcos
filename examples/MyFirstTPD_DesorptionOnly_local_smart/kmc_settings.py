model_name = 'MyFirstTPD_DesorptionOnly'
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

parameters = {
    "A":{"value":"(3.5*angstrom)**2", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "A_CO_des":{"value":"1.45e+13", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
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
<kmc version="(0, 2)">
    <meta author="Christa Cody" debug="0" email="coinzc@ornl.gov" model_dimension="2" model_name="MyFirstTPD_DesorptionOnly"/>
    <species_list default_species="empty">
        <species color="#000000" name="CO" representation="Atoms('CO',[[0,0,0],[0,0,1.2]])" tags="carbon"/>
        <species color="#ffffff" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="False" max="0.0" min="0.0" name="A" scale="linear" value="(3.5*angstrom)**2"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="A_CO_des" scale="linear" value="1.45e+13"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_act_des" scale="linear" value="84000"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="R" scale="linear" value="8.314"/>
        <parameter adjustable="True" max="500.0" min="150.0" name="T" scale="linear" value="600"/>
        <parameter adjustable="True" max="0.3" min="-1.3" name="deltaG" scale="linear" value="-0.5"/>
        <parameter adjustable="True" max="1000.0" min="1e-13" name="p_COgas" scale="log" value="0.2"/>
    </parameter_list>
    <lattice cell_size="3.5 0.0 0.0 0.0 3.5 0.0 0.0 0.0 10.0" default_layer="simple_cubic" representation="" substrate_layer="simple_cubic">
        <layer color="#ffffff" name="simple_cubic">
            <site default_species="empty" pos="0.5 0.5 0.5" tags="" type="coord1"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="CO_desorption" rate_constant="A_CO_des*exp(-E_act_des/(R*T))" tof_count="{'CO_Desorption': 1}">
            <condition coord_layer="simple_cubic" coord_name="coord1" coord_offset="0 0 0" species="CO"/>
            <action coord_layer="simple_cubic" coord_name="coord1" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="Do_nothing" rate_constant="0" tof_count="{'Do_nothing': 1}">
            <condition coord_layer="simple_cubic" coord_name="coord1" coord_offset="0 0 0" species="CO"/>
            <action coord_layer="simple_cubic" coord_name="coord1" coord_offset="0 0 0" species="empty"/>
        </process>
    </process_list>
    <output_list/>
</kmc>
"""
