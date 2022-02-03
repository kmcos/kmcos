model_name = 'MyFirstModel'
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
    "adsorption_right":{"value":"500", "adjustable":True, "min":"1.0", "max":"1000.0","scale":"linear"},
    "adsorption_up":{"value":"500", "adjustable":True, "min":"1.0", "max":"1000.0","scale":"linear"},
    "desorption_right":{"value":"500", "adjustable":True, "min":"1.0", "max":"1000.0","scale":"linear"},
    "desorption_up":{"value":"500", "adjustable":True, "min":"1.0", "max":"1000.0","scale":"linear"},
    }

rate_constants = {
    "CC_adsorption_right":("adsorption_right", True),
    "CC_adsorption_up":("adsorption_up", True),
    "CC_desorption_right":("desorption_right", True),
    "CC_desorption_up":("desorption_up", True),
    }

site_names = ['simple_cubic_hollow']
representations = {
    "CC_right":"""Atoms('NN', [[0,0,0], [2,0,0]])""",
    "CC_right_1":"""""",
    "CC_up":"""Atoms('CC', [[0,0,0], [0,2,0]])""",
    "CC_up_1":"""""",
    "empty":"""""",
    }

lattice_representation = """"""

species_tags = {
    "CC_right":"""""",
    "CC_right_1":"""""",
    "CC_up":"""""",
    "CC_up_1":"""""",
    "empty":"""""",
    }

tof_count = {
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Your Name" debug="0" email="your.name@server.com" model_dimension="2" model_name="MyFirstModel"/>
    <species_list default_species="empty">
        <species color="" name="CC_right" representation="Atoms('NN', [[0,0,0], [2,0,0]])" tags=""/>
        <species color="" name="CC_right_1" representation="" tags=""/>
        <species color="" name="CC_up" representation="Atoms('CC', [[0,0,0], [0,2,0]])" tags=""/>
        <species color="" name="CC_up_1" representation="" tags=""/>
        <species color="" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="False" max="0.0" min="0.0" name="A" scale="linear" value="(3.5*angstrom)**2"/>
        <parameter adjustable="True" max="1000.0" min="1.0" name="adsorption_right" scale="linear" value="500"/>
        <parameter adjustable="True" max="1000.0" min="1.0" name="adsorption_up" scale="linear" value="500"/>
        <parameter adjustable="True" max="1000.0" min="1.0" name="desorption_right" scale="linear" value="500"/>
        <parameter adjustable="True" max="1000.0" min="1.0" name="desorption_up" scale="linear" value="500"/>
    </parameter_list>
    <lattice cell_size="3.5 0.0 0.0 0.0 3.5 0.0 0.0 0.0 10.0" default_layer="simple_cubic" representation="" substrate_layer="simple_cubic">
        <layer color="#ffffff" name="simple_cubic">
            <site default_species="empty" pos="0.5 0.5 0.5" tags="" type="hollow"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="CC_adsorption_right" rate_constant="adsorption_right">
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="CC_right"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="1 0 0" species="CC_right_1"/>
        </process>
        <process enabled="True" name="CC_adsorption_up" rate_constant="adsorption_up">
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="CC_up"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 1 0" species="CC_up_1"/>
        </process>
        <process enabled="True" name="CC_desorption_right" rate_constant="desorption_right">
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="CC_right"/>
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="1 0 0" species="CC_right_1"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="1 0 0" species="empty"/>
        </process>
        <process enabled="True" name="CC_desorption_up" rate_constant="desorption_up">
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="CC_up"/>
            <condition coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 1 0" species="CC_up_1"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="simple_cubic" coord_name="hollow" coord_offset="0 1 0" species="empty"/>
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
