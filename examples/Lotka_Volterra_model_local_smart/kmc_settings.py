model_name = 'lotka_volterra_model'
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
    "k1":{"value":"1000000.", "adjustable":True, "min":"0.0", "max":"100.0","scale":"linear"},
    "k2":{"value":"3.65", "adjustable":True, "min":"0.0", "max":"100.0","scale":"linear"},
    "k3":{"value":"1.1", "adjustable":True, "min":"0.0", "max":"100.0","scale":"linear"},
    "zeta":{"value":"0.06", "adjustable":True, "min":"0.0", "max":"1.0","scale":"linear"},
    }

rate_constants = {
    "AA_creation1":("k1", True),
    "AA_creation2":("k1", True),
    "AA_creation3":("k1", True),
    "AA_creation4":("k1", True),
    "AB_reaction1":("k2", True),
    "AB_reaction2":("k2", True),
    "AB_reaction3":("k2", True),
    "AB_reaction4":("k2", True),
    "B_desorption":("k3", True),
    }

site_names = ['sc_site']
representations = {
    "A":"""Atoms('O')""",
    "B":"""Atoms('C')""",
    "empty":"""""",
    }

lattice_representation = """"""

species_tags = {
    "A":"""""",
    "B":"""""",
    "empty":"""""",
    }

tof_count = {
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="LotkaVolterra" debug="0" email="mjhoffmann@gmail.com" model_dimension="2" model_name="lotka_volterra_model"/>
    <species_list default_species="empty">
        <species color="" name="A" representation="Atoms('O')" tags=""/>
        <species color="" name="B" representation="Atoms('C')" tags=""/>
        <species color="" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="True" max="100.0" min="0.0" name="k1" scale="linear" value="1000000."/>
        <parameter adjustable="True" max="100.0" min="0.0" name="k2" scale="linear" value="3.65"/>
        <parameter adjustable="True" max="100.0" min="0.0" name="k3" scale="linear" value="1.1"/>
        <parameter adjustable="True" max="1.0" min="0.0" name="zeta" scale="linear" value="0.06"/>
    </parameter_list>
    <lattice cell_size="3.5 0.0 0.0 0.0 3.5 0.0 0.0 0.0 10.0" default_layer="sc" representation="" substrate_layer="sc">
        <layer color="#ffffff" name="sc">
            <site default_species="default_species" pos="0.5 0.5 0.5" tags="" type="site"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="AA_creation1" rate_constant="k1">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <action coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="A"/>
        </process>
        <process enabled="True" name="AA_creation2" rate_constant="k1">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="-1 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <action coord_layer="sc" coord_name="site" coord_offset="-1 0 0" species="A"/>
        </process>
        <process enabled="True" name="AA_creation3" rate_constant="k1">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="A"/>
        </process>
        <process enabled="True" name="AA_creation4" rate_constant="k1">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 -1 0" species="A"/>
        </process>
        <process enabled="True" name="AB_reaction1" rate_constant="k2">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="B"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="B"/>
            <action coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="B"/>
        </process>
        <process enabled="True" name="AB_reaction2" rate_constant="k2">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="-1 0 0" species="B"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="B"/>
            <action coord_layer="sc" coord_name="site" coord_offset="-1 0 0" species="B"/>
        </process>
        <process enabled="True" name="AB_reaction3" rate_constant="k2">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="B"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="B"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="B"/>
        </process>
        <process enabled="True" name="AB_reaction4" rate_constant="k2">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="A"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="0 -1 0" species="B"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="B"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 -1 0" species="B"/>
        </process>
        <process enabled="True" name="B_desorption" rate_constant="k3">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="B"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
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
