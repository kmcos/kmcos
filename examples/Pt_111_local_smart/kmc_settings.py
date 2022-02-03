model_name = 'pt111'
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
    "T":{"value":"600", "adjustable":True, "min":"300.0", "max":"800.0","scale":"linear"},
    }

rate_constants = {
    "H_adsorption_hollow1":("100000", True),
    "H_adsorption_hollow2":("100000", True),
    "H_desorption_hollow1":("100000", True),
    "H_desorption_hollow2":("100000", True),
    "H_diff_h1h2":("1000000000", True),
    "H_diff_h2h1":("1000000000", True),
    }

site_names = ['pt111_hollow1', 'pt111_hollow2']
representations = {
    "H":"""Atoms('H')""",
    "empty":"""""",
    }

lattice_representation = """[Atoms(symbols='Pt4',
          pbc=np.array([ True,  True, False]),
          cell=np.array(      ([[2.77185858, 0.0, 0.0], [1.38592929, 2.40049995, 0.0], [0.0, 0.0, 26.78963917]])),
          scaled_positions=np.array(      [[0.0, 0.0, 0.3732786], [0.3333333, 0.3333333, 0.4577595], [0.6666667, 0.6666667, 0.5422405], [0.0, 0.0, 0.6267214]]),
),]"""

species_tags = {
    "H":"""""",
    "empty":"""""",
    }

tof_count = {
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Max J. Hoffmann" debug="0" email="mjhoffmann@gmail.com" model_dimension="2" model_name="pt111"/>
    <species_list default_species="empty">
        <species color="#ffff00" name="H" representation="Atoms('H')" tags=""/>
        <species color="#ffffff" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="True" max="800.0" min="300.0" name="T" scale="linear" value="600"/>
    </parameter_list>
    <lattice cell_size="2.77185858 0.0 0.0 1.38592929 2.40049995 0.0 0.0 0.0 26.78963917" default_layer="pt111" representation="[Atoms(symbols='Pt4',
          pbc=np.array([ True,  True, False]),
          cell=np.array(      ([[2.77185858, 0.0, 0.0], [1.38592929, 2.40049995, 0.0], [0.0, 0.0, 26.78963917]])),
          scaled_positions=np.array(      [[0.0, 0.0, 0.3732786], [0.3333333, 0.3333333, 0.4577595], [0.6666667, 0.6666667, 0.5422405], [0.0, 0.0, 0.6267214]]),
),]" substrate_layer="pt111">
        <layer color="#ffffff" name="pt111">
            <site default_species="default_species" pos="0.333333333333 0.333333333333 0.672" tags="" type="hollow1"/>
            <site default_species="default_species" pos="0.666666666667 0.666666666667 0.672" tags="" type="hollow2"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="H_adsorption_hollow1" rate_constant="100000">
            <condition coord_layer="pt111" coord_name="hollow1" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="pt111" coord_name="hollow1" coord_offset="0 0 0" species="H"/>
        </process>
        <process enabled="True" name="H_adsorption_hollow2" rate_constant="100000">
            <condition coord_layer="pt111" coord_name="hollow2" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="pt111" coord_name="hollow2" coord_offset="0 0 0" species="H"/>
        </process>
        <process enabled="True" name="H_desorption_hollow1" rate_constant="100000">
            <condition coord_layer="pt111" coord_name="hollow1" coord_offset="0 0 0" species="H"/>
            <action coord_layer="pt111" coord_name="hollow1" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="H_desorption_hollow2" rate_constant="100000">
            <condition coord_layer="pt111" coord_name="hollow2" coord_offset="0 0 0" species="H"/>
            <action coord_layer="pt111" coord_name="hollow2" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="H_diff_h1h2" rate_constant="1000000000">
            <condition coord_layer="pt111" coord_name="hollow1" coord_offset="0 0 0" species="H"/>
            <condition coord_layer="pt111" coord_name="hollow2" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="pt111" coord_name="hollow1" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="pt111" coord_name="hollow2" coord_offset="0 0 0" species="H"/>
        </process>
        <process enabled="True" name="H_diff_h2h1" rate_constant="1000000000">
            <condition coord_layer="pt111" coord_name="hollow2" coord_offset="0 0 0" species="H"/>
            <condition coord_layer="pt111" coord_name="hollow1" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="pt111" coord_name="hollow2" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="pt111" coord_name="hollow1" coord_offset="0 0 0" species="H"/>
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
