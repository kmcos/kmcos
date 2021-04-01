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
    <meta author="Andreas Garhammer" email="andreas-garhammer@t-online.de" model_name="2d_auto" model_dimension="2" debug="0"/>
    <species_list default_species="empty">
        <species name="empty" representation="Atoms('He')" color="" tags=""/>
        <species name="ion" representation="Atoms('F')" color="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter name="k" value="100" adjustable="True" min="0.0" max="1000000.0" scale="linear"/>
    </parameter_list>
    <lattice cell_size="3.5 0.0 0.0 0.0 3.5 0.0 0.0 0.0 10.0" default_layer="default" substrate_layer="default" representation="">
        <layer name="default" color="#ffffff">
            <site pos="0.25 0.25 0.5" type="a_1" tags="" default_species="ion"/>
            <site pos="0.75 0.25 0.5" type="a_2" tags="" default_species="ion"/>
            <site pos="0.25 0.75 0.5" type="b_1" tags="" default_species="empty"/>
            <site pos="0.75 0.75 0.5" type="b_2" tags="" default_species="empty"/>
        </layer>
    </lattice>
    <process_list>
        <process rate_constant="k" name="a_1_a_2" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="a_1_b_1" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="a_1_b_2" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="a_2_a_1" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="a_2_b_1" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="a_2_b_2" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="b_1_a_1" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="b_1_a_2" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="b_1_b_2" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="b_2_a_1" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="a_1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="b_2_a_2" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="a_2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="k" name="b_2_b_1" enabled="True">
            <condition species="ion" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
            <action species="ion" coord_layer="default" coord_name="b_1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="default" coord_name="b_2" coord_offset="0 0 0"/>
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
