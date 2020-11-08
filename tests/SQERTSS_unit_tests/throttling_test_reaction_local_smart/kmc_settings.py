model_name = 'throttling_test_reaction'
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
    "AF1p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AF2p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AF3p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AF4p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AF5p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AF6p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AF7p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AR1p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AR2p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AR3p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AR4p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AR5p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AR6p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "AR7p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_F1p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_F2p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_F3p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_F4p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_F5p0":{"value":"100.0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_F6p0":{"value":"10000.0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_F7p0":{"value":"1000000.0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_R1p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_R2p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_R3p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_R4p0":{"value":"1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_R5p0":{"value":"1000.0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_R6p0":{"value":"100000.0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "BRC_R7p0":{"value":"10000000.0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "T":{"value":"600", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    }

rate_constants = {
    "pF1p0":("AF1p0*BRC_F1p0", True),
    "pF2p0":("AF2p0*BRC_F2p0", True),
    "pF3p0":("AF3p0*BRC_F3p0", True),
    "pF4p0":("AF4p0*BRC_F4p0", True),
    "pF5p0":("AF5p0*BRC_F5p0", True),
    "pF6p0":("AF6p0*BRC_F6p0", True),
    "pF7p0":("AF7p0*BRC_F7p0", True),
    "pR1p0":("AR1p0*BRC_R1p0", True),
    "pR2p0":("AR2p0*BRC_R2p0", True),
    "pR3p0":("AR3p0*BRC_R3p0", True),
    "pR4p0":("AR4p0*BRC_R4p0", True),
    "pR5p0":("AR5p0*BRC_R5p0", True),
    "pR6p0":("AR6p0*BRC_R6p0", True),
    "pR7p0":("AR7p0*BRC_R7p0", True),
    }

site_names = ['Site_coord']
representations = {
    "A1":"""""",
    "B1":"""""",
    "B2":"""""",
    "C1":"""""",
    "C2":"""""",
    "D1":"""""",
    "D2":"""""",
    "E1":"""""",
    }

lattice_representation = """"""

species_tags = {
    "A1":"""""",
    "B1":"""""",
    "B2":"""""",
    "C1":"""""",
    "C2":"""""",
    "D1":"""""",
    "D2":"""""",
    "E1":"""""",
    }

tof_count = {
    "pF1p0":{'F1p0': 1},
    "pF2p0":{'F2p0': 1},
    "pF3p0":{'F3p0': 1},
    "pF4p0":{'F4p0': 1},
    "pF5p0":{'F5p0': 1},
    "pF6p0":{'F6p0': 1},
    "pF7p0":{'F7p0': 1},
    "pR1p0":{'R1p0': 1},
    "pR2p0":{'R2p0': 1},
    "pR3p0":{'R3p0': 1},
    "pR4p0":{'R4p0': 1},
    "pR5p0":{'R5p0': 1},
    "pR6p0":{'R6p0': 1},
    "pR7p0":{'R7p0': 1},
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Thomas Danielson" debug="0" email="thomasd1@vt.edu" model_dimension="2" model_name="throttling_test_reaction"/>
    <species_list default_species="A1">
        <species color="white" name="A1" representation="" tags=""/>
        <species color="green" name="B1" representation="" tags=""/>
        <species color="blue" name="B2" representation="" tags=""/>
        <species color="red" name="C1" representation="" tags=""/>
        <species color="orange" name="C2" representation="" tags=""/>
        <species color="black" name="D1" representation="" tags=""/>
        <species color="grey" name="D2" representation="" tags=""/>
        <species color="purple" name="E1" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="False" max="0.0" min="0.0" name="AF1p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AF2p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AF3p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AF4p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AF5p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AF6p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AF7p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AR1p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AR2p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AR3p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AR4p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AR5p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AR6p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="AR7p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_F1p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_F2p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_F3p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_F4p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_F5p0" scale="linear" value="100.0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_F6p0" scale="linear" value="10000.0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_F7p0" scale="linear" value="1000000.0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_R1p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_R2p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_R3p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_R4p0" scale="linear" value="1"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_R5p0" scale="linear" value="1000.0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_R6p0" scale="linear" value="100000.0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="BRC_R7p0" scale="linear" value="10000000.0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="T" scale="linear" value="600"/>
    </parameter_list>
    <lattice cell_size="3.825 0.0 0.0 0.0 3.825 0.0 0.0 0.0 2.343" default_layer="Site" representation="" substrate_layer="Site">
        <layer color="#ffffff" name="Site">
            <site default_species="A1" pos="0.5 0.5 1.0" tags="" type="coord"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="pF1p0" rate_constant="AF1p0*BRC_F1p0" tof_count="{'F1p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="A1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="B1"/>
        </process>
        <process enabled="True" name="pF2p0" rate_constant="AF2p0*BRC_F2p0" tof_count="{'F2p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="B1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="C1"/>
        </process>
        <process enabled="True" name="pF3p0" rate_constant="AF3p0*BRC_F3p0" tof_count="{'F3p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="C1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="D1"/>
        </process>
        <process enabled="True" name="pF4p0" rate_constant="AF4p0*BRC_F4p0" tof_count="{'F4p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="D1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="E1"/>
        </process>
        <process enabled="True" name="pF5p0" rate_constant="AF5p0*BRC_F5p0" tof_count="{'F5p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="B1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="B2"/>
        </process>
        <process enabled="True" name="pF6p0" rate_constant="AF6p0*BRC_F6p0" tof_count="{'F6p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="C1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="C2"/>
        </process>
        <process enabled="True" name="pF7p0" rate_constant="AF7p0*BRC_F7p0" tof_count="{'F7p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="D1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="D2"/>
        </process>
        <process enabled="True" name="pR1p0" rate_constant="AR1p0*BRC_R1p0" tof_count="{'R1p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="B1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="A1"/>
        </process>
        <process enabled="True" name="pR2p0" rate_constant="AR2p0*BRC_R2p0" tof_count="{'R2p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="C1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="B1"/>
        </process>
        <process enabled="True" name="pR3p0" rate_constant="AR3p0*BRC_R3p0" tof_count="{'R3p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="D1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="C1"/>
        </process>
        <process enabled="True" name="pR4p0" rate_constant="AR4p0*BRC_R4p0" tof_count="{'R4p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="E1"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="D1"/>
        </process>
        <process enabled="True" name="pR5p0" rate_constant="AR5p0*BRC_R5p0" tof_count="{'R5p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="B2"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="B1"/>
        </process>
        <process enabled="True" name="pR6p0" rate_constant="AR6p0*BRC_R6p0" tof_count="{'R6p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="C2"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="C1"/>
        </process>
        <process enabled="True" name="pR7p0" rate_constant="AR7p0*BRC_R7p0" tof_count="{'R7p0': 1}">
            <condition coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="D2"/>
            <action coord_layer="Site" coord_name="coord" coord_offset="0 0 0" species="D1"/>
        </process>
    </process_list>
    <output_list/>
</kmc>
"""
