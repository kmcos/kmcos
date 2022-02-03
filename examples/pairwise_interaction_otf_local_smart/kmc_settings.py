model_name = 'dummy_pairwise_interaction_otf'
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
    "A":{"value":"(3*angstrom)**2", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CO":{"value":"-1", "adjustable":True, "min":"-2.0", "max":"0.0","scale":"linear"},
    "E_CO_nn":{"value":"0.2", "adjustable":True, "min":"-1.0", "max":"1.0","scale":"linear"},
    "T":{"value":"600", "adjustable":True, "min":"300.0", "max":"1500.0","scale":"linear"},
    "p_COgas":{"value":"0.2", "adjustable":True, "min":"1e-13", "max":"1000.0","scale":"log"},
    }

rate_constants = {
    "CO_adsorption":("p_COgas*A*bar/sqrt(2*m_CO*umass/beta)", True),
    "CO_desorption":("p_COgas*A*bar/sqrt(2*m_CO*umass/beta)*exp(beta*(E_CO-mu_COgas)*eV)", True),
    "O_adsorption":("p_COgas*A*bar/sqrt(2*m_O*umass/beta)", True),
    "O_desorption":("p_COgas*A*bar/sqrt(2*m_O*umass/beta)", True),
    }

site_names = ['simplecubic_2d_a']
representations = {
    "CO":"""Atoms('CO',[[0,0,0],[0,0,1.2]])""",
    "O":"""Atoms('O')""",
    "empty":"""""",
    }

lattice_representation = """"""

species_tags = {
    "CO":"""carbon""",
    "O":"""""",
    "empty":"""""",
    }

tof_count = {
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Juan M. Lorenzi" debug="0" email="jmlorenzi@gmail.com" model_dimension="2" model_name="dummy_pairwise_interaction_otf"/>
    <species_list default_species="empty">
        <species color="#000000" name="CO" representation="Atoms('CO',[[0,0,0],[0,0,1.2]])" tags="carbon"/>
        <species color="#ff0000" name="O" representation="Atoms('O')" tags=""/>
        <species color="#ffffff" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="False" max="0.0" min="0.0" name="A" scale="linear" value="(3*angstrom)**2"/>
        <parameter adjustable="True" max="0.0" min="-2.0" name="E_CO" scale="linear" value="-1"/>
        <parameter adjustable="True" max="1.0" min="-1.0" name="E_CO_nn" scale="linear" value="0.2"/>
        <parameter adjustable="True" max="1500.0" min="300.0" name="T" scale="linear" value="600"/>
        <parameter adjustable="True" max="1000.0" min="1e-13" name="p_COgas" scale="log" value="0.2"/>
    </parameter_list>
    <lattice cell_size="1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 10.0" default_layer="simplecubic_2d" representation="" substrate_layer="simplecubic_2d">
        <layer color="#ffffff" name="simplecubic_2d">
            <site default_species="default_species" pos="0.0 0.0 0.0" tags="" type="a"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="CO_adsorption" rate_constant="p_COgas*A*bar/sqrt(2*m_CO*umass/beta)">
            <condition coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_desorption" otf_rate="base_rate*exp(beta*nr_CO_1nn*E_CO_nn*eV)" rate_constant="p_COgas*A*bar/sqrt(2*m_CO*umass/beta)*exp(beta*(E_CO-mu_COgas)*eV)">
            <condition coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 0 0" species="CO"/>
            <action coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 0 0" species="empty"/>
            <bystander allowed_species="CO" coord_layer="simplecubic_2d" coord_name="a" coord_offset="-1 0 0" flag="1nn"/>
            <bystander allowed_species="CO" coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 -1 0" flag="1nn"/>
            <bystander allowed_species="CO" coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 1 0" flag="1nn"/>
            <bystander allowed_species="CO" coord_layer="simplecubic_2d" coord_name="a" coord_offset="1 0 0" flag="1nn"/>
        </process>
        <process enabled="True" name="O_adsorption" rate_constant="p_COgas*A*bar/sqrt(2*m_O*umass/beta)">
            <condition coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 0 0" species="O"/>
        </process>
        <process enabled="True" name="O_desorption" rate_constant="p_COgas*A*bar/sqrt(2*m_O*umass/beta)">
            <condition coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 0 0" species="O"/>
            <action coord_layer="simplecubic_2d" coord_name="a" coord_offset="0 0 0" species="empty"/>
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
