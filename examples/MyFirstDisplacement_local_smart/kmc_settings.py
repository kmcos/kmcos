model_name = 'MyFirstDisplacement'
simulation_size = 20 #TODO: A. Savara found on 12/04/22 that this is hardcoded in io.py, and it should not be hardcoded. 
random_seed = 1 #TODO: A. Savara found on 12/04/22 that this is hardcoded in io.py, and it should not be hardcoded.

def setup_model(model):
    """ Aug 15th 2022: setup_model is legacy code. Please ignore the rest of this comment and this function. 
    Write initialization steps here.
       e.g. ::
    model.put([0,0,0,model.lattice.default_a], model.proclist.species_a)
    """
    #from setup_model import setup_model
    #setup_model(model)
    pass

# Default history length in graph
hist_length = 30

parameters = {
    "E_exc":{"value":"0.65", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_hop":{"value":"0.83", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "T":{"value":"300", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "eps_int":{"value":"0.1", "adjustable":True, "min":"0.0", "max":"0.2","scale":"linear"},
    }

rate_constants = {
    "exc_left_down":("1/(beta*h)*exp(-beta*E_exc*eV)", True),
    "exc_left_up":("1/(beta*h)*exp(-beta*E_exc*eV)", True),
    "exc_right_down":("1/(beta*h)*exp(-beta*E_exc*eV)", True),
    "exc_right_up":("1/(beta*h)*exp(-beta*E_exc*eV)", True),
    "hop_down":("1/(beta*h)*exp(-beta*E_hop*eV)", True),
    "hop_left":("1/(beta*h)*exp(-beta*E_hop*eV)", True),
    "hop_right":("1/(beta*h)*exp(-beta*E_hop*eV)", True),
    "hop_up":("1/(beta*h)*exp(-beta*E_hop*eV)", True),
    }

site_names = ['default_a']
representations = {
    "Au":"""Atoms('Au')""",
    "empty":"""""",
    }

lattice_representation = """"""

species_tags = {
    "Au":"""""",
    "empty":"""""",
    }

tof_count = {
    }

connected_variables={'surroundingSitesDict': {}}
xml = """<?xml version="1.0" ?>
<kmc version="(0, 4)">
    <meta author="Mie Andersen" debug="0" email="mie.andersen@ch.tum.de" model_dimension="2" model_name="MyFirstDisplacement"/>
    <species_list default_species="empty">
        <species color="#00ff00" name="Au" representation="Atoms('Au')" tags=""/>
        <species color="#d3d3d3" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_exc" scale="linear" value="0.65"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_hop" scale="linear" value="0.83"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="T" scale="linear" value="300"/>
        <parameter adjustable="True" max="0.2" min="0.0" name="eps_int" scale="linear" value="0.1"/>
    </parameter_list>
    <lattice cell_size="2.885 0.0 0.0 0.0 2.885 0.0 0.0 0.0 10.0" default_layer="default" representation="" substrate_layer="default">
        <layer color="#ffffff" name="default">
            <site default_species="empty" pos="0.5 0.5 0.5" tags="" type="a"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="exc_left_down" rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="Au"/>
            <condition coord_layer="default" coord_name="a" coord_offset="-1 -1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="-1 -1 0" species="Au"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="exc_left_up" rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="Au"/>
            <condition coord_layer="default" coord_name="a" coord_offset="-1 1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="-1 1 0" species="Au"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="exc_right_down" rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="Au"/>
            <condition coord_layer="default" coord_name="a" coord_offset="1 -1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="1 -1 0" species="Au"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="exc_right_up" rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="Au"/>
            <condition coord_layer="default" coord_name="a" coord_offset="1 1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="1 1 0" species="Au"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="hop_down" rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="Au"/>
            <condition coord_layer="default" coord_name="a" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 -1 0" species="Au"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="hop_left" rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="Au"/>
            <condition coord_layer="default" coord_name="a" coord_offset="-1 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="-1 0 0" species="Au"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="hop_right" rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="Au"/>
            <condition coord_layer="default" coord_name="a" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="1 0 0" species="Au"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="hop_up" rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)">
            <condition coord_layer="default" coord_name="a" coord_offset="0 0 0" species="Au"/>
            <condition coord_layer="default" coord_name="a" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 1 0" species="Au"/>
            <action coord_layer="default" coord_name="a" coord_offset="0 0 0" species="empty"/>
        </process>
    </process_list>
    <output_list/>
    <connected_variables connected_variables_string="{'surroundingSitesDict': {}}"/>
</kmc>
"""
if __name__ == "__main__":
    #benchmark if kmc_settings.py is run without additional arguments, else call cli with additional argument provided.
    import sys
    if len(sys.argv) == 1:
        from kmcos import cli
        cli.main("benchmark")
    if len(sys.argv) == 2:
        from kmcos import cli
        cli.main(sys.argv[1])
