model_name = 'sand_model'
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
    "k_down":{"value":"1000.0", "adjustable":True, "min":"1.0", "max":"1000000.0","scale":"log"},
    "k_entry":{"value":"1000.0", "adjustable":True, "min":"1.0", "max":"1000000.0","scale":"log"},
    "k_exit":{"value":"1000.0", "adjustable":True, "min":"1.0", "max":"1000000.0","scale":"log"},
    "k_left":{"value":"1000.0", "adjustable":True, "min":"1.0", "max":"1000000.0","scale":"log"},
    "k_right":{"value":"1000.0", "adjustable":True, "min":"1.0", "max":"1000000.0","scale":"log"},
    "k_up":{"value":"10000.0", "adjustable":True, "min":"1.0", "max":"1000000.0","scale":"log"},
    }

rate_constants = {
    "diffusion_down":("k_down", True),
    "diffusion_down_left":("k_left", True),
    "diffusion_down_right":("k_right", True),
    "diffusion_left":("k_left", True),
    "diffusion_right":("k_right", True),
    "diffusion_up_left":("k_left", True),
    "diffusion_up_right":("k_right", True),
    "entry":("k_entry", True),
    "exit":("k_exit", True),
    }

site_names = ['default_a']
representations = {
    "blocked":"""Atoms('C')""",
    "drain":"""Atoms('Ag')""",
    "empty":"""""",
    "grain":"""Atoms('Si')""",
    "source":"""Atoms('Au')""",
    }

lattice_representation = """"""

species_tags = {
    "blocked":"""""",
    "drain":"""""",
    "empty":"""""",
    "grain":"""""",
    "source":"""""",
    }

tof_count = {
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Max J. Hoffmann" debug="0" email="mjhoffmann@gmail.com" model_dimension="2" model_name="sand_model"/>
    <species_list default_species="empty">
        <species color="" name="blocked" representation="Atoms('C')" tags=""/>
        <species color="" name="drain" representation="Atoms('Ag')" tags=""/>
        <species color="" name="empty" representation="" tags=""/>
        <species color="" name="grain" representation="Atoms('Si')" tags=""/>
        <species color="" name="source" representation="Atoms('Au')" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="True" max="1000000.0" min="1.0" name="k_down" scale="log" value="1000.0"/>
        <parameter adjustable="True" max="1000000.0" min="1.0" name="k_entry" scale="log" value="1000.0"/>
        <parameter adjustable="True" max="1000000.0" min="1.0" name="k_exit" scale="log" value="1000.0"/>
        <parameter adjustable="True" max="1000000.0" min="1.0" name="k_left" scale="log" value="1000.0"/>
        <parameter adjustable="True" max="1000000.0" min="1.0" name="k_right" scale="log" value="1000.0"/>
        <parameter adjustable="True" max="1000000.0" min="1.0" name="k_up" scale="log" value="10000.0"/>
    </parameter_list>
    <lattice cell_size="3.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 3.0" default_layer="default" representation="" substrate_layer="default">
        <layer color="#ffffff" name="default">
            <site default_species="empty" pos="0.5 0.5 0.5" tags="" type="a"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="diffusion_down" rate_constant="k_down">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 -1 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="diffusion_down_left" rate_constant="k_left">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="-1 -1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="-1 -1 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="diffusion_down_right" rate_constant="k_right">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="1 -1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="1 -1 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="diffusion_left" rate_constant="k_left">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="-1 -1 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="-1 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="-1 0 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="-1 -1 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="diffusion_right" rate_constant="k_right">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="1 -1 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="1 0 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="1 -1 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="diffusion_up_left" rate_constant="k_left">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="-1 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="-1 1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="-1 0 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="-1 1 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="diffusion_up_right" rate_constant="k_right">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="1 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="1 1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="1 0 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="1 1 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="entry" rate_constant="k_entry">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="default" coord_name="a" coord_offset="0 1 0" species="source"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="grain"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 1 0" species="source"/>
        </process>
        <process enabled="True" name="exit" rate_constant="k_exit">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="grain"/>
            <condition coord_layer="default" coord_name="a" coord_offset="0 -1 0" species="drain"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 -1 0" species="drain"/>
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
