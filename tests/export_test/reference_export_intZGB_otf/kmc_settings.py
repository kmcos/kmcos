model_name = 'IntZGB'
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
    "J_CO_CO":{"value":"1.0", "adjustable":True, "min":"0.5", "max":"1.5","scale":"linear"},
    "J_O_CO":{"value":"1.0", "adjustable":True, "min":"0.5", "max":"1.5","scale":"linear"},
    "J_O_O":{"value":"1.0", "adjustable":True, "min":"0.5", "max":"1.5","scale":"linear"},
    "kDes":{"value":"1e-10", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "yCO":{"value":"0.5", "adjustable":True, "min":"0.0", "max":"1.0","scale":"linear"},
    }

rate_constants = {
    "CO_ads":("yCO", True),
    "CO_des":("kDes", True),
    "CO_oxidation_00":("0.25*yCO", True),
    "CO_oxidation_01":("0.25*yCO", True),
    "CO_oxidation_02":("0.25*yCO", True),
    "CO_oxidation_03":("0.25*yCO", True),
    "O2_des_right":("kDes", True),
    "O2_des_up":("kDes", True),
    "O_ads_00":("0.5*(1-yCO)", True),
    "O_ads_01":("0.5*(1-yCO)", True),
    }

site_names = ['square_default']
representations = {
    "CO":"""Atoms('N',[[0.,0.,0.]])""",
    "O":"""Atoms('O',[[0.,0.,0.]])""",
    "empty":"""""",
    }

lattice_representation = """"""

species_tags = {
    "CO":"""""",
    "O":"""""",
    "empty":"""""",
    }

tof_count = {
    "CO_oxidation_00":{'CO_oxidation': 1},
    "CO_oxidation_01":{'CO_oxidation': 1},
    "CO_oxidation_02":{'CO_oxidation': 1},
    "CO_oxidation_03":{'CO_oxidation': 1},
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Juan M. Lorenzi" email="jmlorenzi@gmail.com" model_name="IntZGB" model_dimension="2" debug="1"/>
    <species_list default_species="empty">
        <species name="CO" representation="Atoms('N',[[0.,0.,0.]])" color="#000000" tags=""/>
        <species name="O" representation="Atoms('O',[[0.,0.,0.]])" color="#ff0000" tags=""/>
        <species name="empty" representation="" color="#ffffff" tags=""/>
    </species_list>
    <parameter_list>
        <parameter name="J_CO_CO" value="1.0" adjustable="True" min="0.5" max="1.5" scale="linear"/>
        <parameter name="J_O_CO" value="1.0" adjustable="True" min="0.5" max="1.5" scale="linear"/>
        <parameter name="J_O_O" value="1.0" adjustable="True" min="0.5" max="1.5" scale="linear"/>
        <parameter name="kDes" value="1e-10" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="yCO" value="0.5" adjustable="True" min="0.0" max="1.0" scale="linear"/>
    </parameter_list>
    <lattice cell_size="3.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 3.0" default_layer="square" substrate_layer="square" representation="">
        <layer name="square" color="#ffffff">
            <site pos="0.5 0.5 0.5" type="default" tags="" default_species="default_species"/>
        </layer>
    </lattice>
    <process_list>
        <process rate_constant="yCO" otf_rate="base_rate*(J_O_CO**nr_O_1nn)*(J_CO_CO**nr_CO_1nn)" name="CO_ads" enabled="True">
            <condition species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 0 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 1 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 0 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 -1 0" flag="1nn"/>
        </process>
        <process rate_constant="kDes" name="CO_des" enabled="True">
            <condition species="CO" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="0.25*yCO" otf_rate="base_rate*(J_O_O**(-nr_O_Onn))*(J_CO_CO**(-nr_CO_COnn))*(J_O_CO**(-nr_O_COnn-nr_CO_Onn))" name="CO_oxidation_00" enabled="True" tof_count="{'CO_oxidation': 1}">
            <condition species="CO" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <condition species="O" coord_layer="square" coord_name="default" coord_offset="1 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="1 0 0"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 1 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 0 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 -1 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="2 0 0" flag="Onn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 1 0" flag="Onn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 -1 0" flag="Onn"/>
        </process>
        <process rate_constant="0.25*yCO" otf_rate="base_rate*(J_O_O**(-nr_O_Onn))*(J_CO_CO**(-nr_CO_COnn))*(J_O_CO**(-nr_O_COnn-nr_CO_Onn))" name="CO_oxidation_01" enabled="True" tof_count="{'CO_oxidation': 1}">
            <condition species="CO" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <condition species="O" coord_layer="square" coord_name="default" coord_offset="0 1 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 1 0"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 0 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 0 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 -1 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 1 0" flag="Onn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 2 0" flag="Onn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 1 0" flag="Onn"/>
        </process>
        <process rate_constant="0.25*yCO" otf_rate="base_rate*(J_O_O**(-nr_O_Onn))*(J_CO_CO**(-nr_CO_COnn))*(J_O_CO**(-nr_O_COnn-nr_CO_Onn))" name="CO_oxidation_02" enabled="True" tof_count="{'CO_oxidation': 1}">
            <condition species="CO" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <condition species="O" coord_layer="square" coord_name="default" coord_offset="-1 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="-1 0 0"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 0 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 1 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 -1 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 1 0" flag="Onn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-2 0 0" flag="Onn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 -1 0" flag="Onn"/>
        </process>
        <process rate_constant="0.25*yCO" otf_rate="base_rate*(J_O_O**(-nr_O_Onn))*(J_CO_CO**(-nr_CO_COnn))*(J_O_CO**(-nr_O_COnn-nr_CO_Onn))" name="CO_oxidation_03" enabled="True" tof_count="{'CO_oxidation': 1}">
            <condition species="CO" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <condition species="O" coord_layer="square" coord_name="default" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 -1 0"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 0 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 1 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 0 0" flag="COnn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 -1 0" flag="Onn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 -1 0" flag="Onn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 -2 0" flag="Onn"/>
        </process>
        <process rate_constant="kDes" name="O2_des_right" enabled="True">
            <condition species="O" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <condition species="O" coord_layer="square" coord_name="default" coord_offset="1 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="1 0 0"/>
        </process>
        <process rate_constant="kDes" name="O2_des_up" enabled="True">
            <condition species="O" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <condition species="O" coord_layer="square" coord_name="default" coord_offset="0 1 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="square" coord_name="default" coord_offset="0 1 0"/>
        </process>
        <process rate_constant="0.5*(1-yCO)" otf_rate="base_rate*(J_O_O**nr_O_1nn)*(J_O_CO**nr_CO_1nn)" name="O_ads_00" enabled="True">
            <condition species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="square" coord_name="default" coord_offset="1 0 0"/>
            <action species="O" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="O" coord_layer="square" coord_name="default" coord_offset="1 0 0"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="2 0 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 1 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 1 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 0 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 -1 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 -1 0" flag="1nn"/>
        </process>
        <process rate_constant="0.5*(1-yCO)" otf_rate="base_rate*(J_O_O**nr_O_1nn)*(J_O_CO**nr_CO_1nn)" name="O_ads_01" enabled="True">
            <condition species="empty" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="square" coord_name="default" coord_offset="0 1 0"/>
            <action species="O" coord_layer="square" coord_name="default" coord_offset="0 0 0"/>
            <action species="O" coord_layer="square" coord_name="default" coord_offset="0 1 0"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 0 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="1 1 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 2 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 1 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="-1 0 0" flag="1nn"/>
            <bystander allowed_species="O CO" coord_layer="square" coord_name="default" coord_offset="0 -1 0" flag="1nn"/>
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
