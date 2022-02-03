model_name = 'zgb_model'
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
    "yCO":{"value":"0.45", "adjustable":True, "min":"0.0", "max":"1.0","scale":"linear"},
    }

rate_constants = {
    "CO_adsorption":("yCO", True),
    "CO_desorption":("1e-13", True),
    "CO_oxidation1":("10**10", True),
    "CO_oxidation2":("10**10", True),
    "CO_oxidation3":("10**10", True),
    "CO_oxidation4":("10**10", True),
    "O2_adsorption1":("(1 - yCO)/2.", True),
    "O2_adsorption2":("(1 - yCO)/2.", True),
    "O2_desorption1":("1e-13", True),
    "O2_desorption2":("1e-13", True),
    }

site_names = ['sc_site']
representations = {
    "CO":"""Atoms('C')""",
    "O":"""Atoms('O')""",
    "empty":"""""",
    }

lattice_representation = """"""

species_tags = {
    "CO":"""""",
    "O":"""""",
    "empty":"""""",
    }

tof_count = {
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Ziff,Gulari,Barshad" debug="0" email="mjhoffmann@gmail.com" model_dimension="2" model_name="zgb_model"/>
    <species_list default_species="empty">
        <species color="#000000" name="CO" representation="Atoms('C')" tags=""/>
        <species color="#ff0000" name="O" representation="Atoms('O')" tags=""/>
        <species color="#ffffff" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="True" max="1.0" min="0.0" name="yCO" scale="linear" value="0.45"/>
    </parameter_list>
    <lattice cell_size="3.5 0.0 0.0 0.0 3.5 0.0 0.0 0.0 10.0" default_layer="sc" representation="" substrate_layer="sc">
        <layer color="#ffffff" name="sc">
            <site default_species="default_species" pos="0.5 0.5 0.5" tags="" type="site"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="CO_adsorption" rate_constant="yCO">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_desorption" rate_constant="1e-13">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="CO"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="CO_oxidation1" rate_constant="10**10">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="O"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="empty"/>
        </process>
        <process enabled="True" name="CO_oxidation2" rate_constant="10**10">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="O"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="empty"/>
        </process>
        <process enabled="True" name="CO_oxidation3" rate_constant="10**10">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="-1 0 0" species="O"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="-1 0 0" species="empty"/>
        </process>
        <process enabled="True" name="CO_oxidation4" rate_constant="10**10">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="0 -1 0" species="O"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 -1 0" species="empty"/>
        </process>
        <process enabled="True" name="O2_adsorption1" rate_constant="(1 - yCO)/2.">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="O"/>
            <action coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="O"/>
        </process>
        <process enabled="True" name="O2_adsorption2" rate_constant="(1 - yCO)/2.">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="O"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="O"/>
        </process>
        <process enabled="True" name="O2_desorption1" rate_constant="1e-13">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="O"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="1 0 0" species="empty"/>
        </process>
        <process enabled="True" name="O2_desorption2" rate_constant="1e-13">
            <condition coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="O"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="sc" coord_name="site" coord_offset="0 1 0" species="empty"/>
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
