model_name = '2d_auto'
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
    "k":{"value":"100", "adjustable":True, "min":"0.0", "max":"1000000.0","scale":"linear"},
    }

rate_constants = {
    "a_1_a_2":("k", True),
    "a_1_b_1":("k", True),
    "a_1_b_2":("k", True),
    "a_2_a_1":("k", True),
    "a_2_b_1":("k", True),
    "a_2_b_2":("k", True),
    "b_1_a_1":("k", True),
    "b_1_a_2":("k", True),
    "b_1_b_2":("k", True),
    "b_2_a_1":("k", True),
    "b_2_a_2":("k", True),
    "b_2_b_1":("k", True),
    }

site_names = ['default_a_1', 'default_a_2', 'default_b_1', 'default_b_2']
representations = {
    "empty":"""Atoms('He')""",
    "ion":"""Atoms('F')""",
    }

lattice_representation = """"""

species_tags = {
    "empty":"""""",
    "ion":"""""",
    }

tof_count = {
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Andreas Garhammer" debug="0" email="andreas-garhammer@t-online.de" model_dimension="2" model_name="2d_auto"/>
    <species_list default_species="empty">
        <species color="" name="empty" representation="Atoms('He')" tags=""/>
        <species color="" name="ion" representation="Atoms('F')" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="True" max="1000000.0" min="0.0" name="k" scale="linear" value="100"/>
    </parameter_list>
    <lattice cell_size="3.5 0.0 0.0 0.0 3.5 0.0 0.0 0.0 10.0" default_layer="default" representation="" substrate_layer="default">
        <layer color="#ffffff" name="default">
            <site default_species="ion" pos="0.25 0.25 0.5" tags="" type="a_1"/>
            <site default_species="ion" pos="0.75 0.25 0.5" tags="" type="a_2"/>
            <site default_species="empty" pos="0.25 0.75 0.5" tags="" type="b_1"/>
            <site default_species="empty" pos="0.75 0.75 0.5" tags="" type="b_2"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="a_1_a_2" rate_constant="k">
            <condition coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="a_1_b_1" rate_constant="k">
            <condition coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="a_1_b_2" rate_constant="k">
            <condition coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="a_2_a_1" rate_constant="k">
            <condition coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="a_2_b_1" rate_constant="k">
            <condition coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="a_2_b_2" rate_constant="k">
            <condition coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="b_1_a_1" rate_constant="k">
            <condition coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="b_1_a_2" rate_constant="k">
            <condition coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="b_1_b_2" rate_constant="k">
            <condition coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="b_2_a_1" rate_constant="k">
            <condition coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a_1" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="b_2_a_2" rate_constant="k">
            <condition coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a_2" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="b_2_b_1" rate_constant="k">
            <condition coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="ion"/>
            <condition coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="b_1" coord_offset="0 0 0" species="ion"/>
            <action coord_layer="default" coord_name="b_2" coord_offset="0 0 0" species="empty"/>
        </process>
    </process_list>
    <output_list/>
</kmc>
"""
