model_name = 'hopping_model'
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
    }

rate_constants = {
    "ads":("10**6", True),
    "des":("10**6", True),
    "left":("10**8", True),
    "right":("10**8", True),
    }

site_names = ['default_a']
representations = {
    "C":"""Atoms('C',[[0,0,0]])""",
    "empty":"""""",
    }

lattice_representation = """"""

species_tags = {
    "C":"""""",
    "empty":"""""",
    }

tof_count = {
    "ads":{'adsorption': 1},
    "des":{'desorption': 1},
    "left":{'left': 1},
    "right":{'right': 1},
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="StangenMensch" debug="0" email="linie@tum.de" model_dimension="1" model_name="hopping_model"/>
    <species_list default_species="empty">
        <species color="#000000" name="C" representation="Atoms('C',[[0,0,0]])" tags=""/>
        <species color="#ffffff" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list/>
    <lattice cell_size="1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0" default_layer="default" representation="" substrate_layer="default">
        <layer color="#ffffff" name="default">
            <site default_species="default_species" pos="0.0 0.0 0.0" tags="" type="a"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="ads" rate_constant="10**6" tof_count="{'adsorption': 1}">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="des" rate_constant="10**6" tof_count="{'desorption': 1}">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="C"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="left" rate_constant="10**8" tof_count="{'left': 1}">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="default" coord_name="a" coord_offset="-1 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="-1 0 0" species="C"/>
        </process>
        <process enabled="True" name="right" rate_constant="10**8" tof_count="{'right': 1}">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="default" coord_name="a" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="1 0 0" species="C"/>
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
