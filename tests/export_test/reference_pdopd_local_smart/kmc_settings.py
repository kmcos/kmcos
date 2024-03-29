model_name = 'sqrt5PdO'
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
    "E_adsorption_o2_bridge_bridge":{"value":"1.9", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_co_bridge":{"value":"", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_co_hollow":{"value":"", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_diff_co_bridge_bridge":{"value":"", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_diff_co_hollow_hollow":{"value":"", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_diff_o_bridge_bridge":{"value":"", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_diff_o_bridge_hollow":{"value":"", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_diff_o_hollow_hollow":{"value":"", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_o_bridge":{"value":"", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_o_hollow":{"value":"", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "lattice_size":{"value":"10 10 1", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "T":{"value":"600", "adjustable":True, "min":"500.0", "max":"600.0","scale":"linear"},
    "p_co":{"value":"1.", "adjustable":True, "min":"0.0", "max":"0.0","scale":"linear"},
    "p_o2":{"value":"1.", "adjustable":True, "min":"0.0", "max":"0.0","scale":"linear"},
    }

rate_constants = {
    "destruct1":("10E15", False),
    "destruct10":("10E15", False),
    "destruct11":("10E15", False),
    "destruct2":("10E15", False),
    "destruct3":("10E15", False),
    "destruct4":("10E15", False),
    "destruct5":("10E15", False),
    "destruct6":("10E15", False),
    "destruct7":("10E15", False),
    "destruct8":("10E15", False),
    "destruct9":("10E15", False),
    "m_COads_b1":("10E8*p_co", True),
    "m_COads_b10":("10E8*p_co", True),
    "m_COads_b2":("10E8*p_co", True),
    "m_COads_b3":("10E8*p_co", True),
    "m_COads_b4":("10E8*p_co", True),
    "m_COads_b5":("10E8*p_co", True),
    "m_COads_b6":("10E8*p_co", True),
    "m_COads_b7":("10E8*p_co", True),
    "m_COads_b8":("10E8*p_co", True),
    "m_COads_b9":("10E8*p_co", True),
    "m_COdes_b1":("10E8", True),
    "m_COdes_b10":("10E8", True),
    "m_COdes_b2":("10E8", True),
    "m_COdes_b3":("10E8", True),
    "m_COdes_b4":("10E8", True),
    "m_COdes_b5":("10E8", True),
    "m_COdes_b6":("10E8", True),
    "m_COdes_b7":("10E8", True),
    "m_COdes_b8":("10E8", True),
    "m_COdes_b9":("10E8", True),
    "o_COads_bridge1":("10E8", True),
    "o_COads_bridge2":("10E8", True),
    "o_COads_hollow1":("10E8", True),
    "o_COads_hollow2":("10E8", True),
    "o_COdes_bridge1":("10E8", True),
    "o_COdes_bridge2":("10E8", True),
    "o_COdes_hollow1":("10E8", True),
    "o_COdes_hollow2":("10E8", True),
    "o_COdif_h1h2down":("10E8", True),
    "o_COdif_h1h2up":("10E8", True),
    "o_O2ads_h1h2":("10E12*p_o2", False),
    "o_O2ads_h2h1":("10E12*p_o2", False),
    "o_O2des_h1h2":("10E8", True),
    "o_O2des_h2h1":("10E8", True),
    "oxidize1":("10E15", True),
    }

site_names = ['Pd100_h1', 'Pd100_h2', 'Pd100_h4', 'Pd100_h5', 'Pd100_b1', 'Pd100_b2', 'Pd100_b3', 'Pd100_b4', 'Pd100_b5', 'Pd100_b6', 'Pd100_b7', 'Pd100_b8', 'Pd100_b9', 'Pd100_b10', 'Pd100_h3', 'PdO_bridge2', 'PdO_hollow1', 'PdO_hollow2', 'PdO_bridge1', 'PdO_Pd2', 'PdO_Pd3', 'PdO_Pd4', 'PdO_hollow3', 'PdO_hollow4', 'PdO_Pd1']
representations = {
    "CO":"""Atoms('CO',[[0,0,0],[0,0,1.2]])""",
    "Pd":"""Atoms('Pd',[[0,0,0]])""",
    "empty":"""""",
    "oxygen":"""Atoms('O',[[0,0,0]])""",
    }

lattice_representation = """[Atoms(symbols='Pd15',
          pbc=np.array([False, False, False]),
          cell=np.array(      ([1.0, 1.0, 1.0])),
          scaled_positions=np.array(      [[4.7453659, 0.3423996, -6.2962764], [5.92199, 2.865787, -6.2962764], [0.87534, 5.2190976, -6.2962764], [2.2219785, 1.5190861, -6.2962764], [3.398665, 4.0424111, -6.2962764], [2.820011, 5.9091707, -4.2497057], [0.340976, 0.918238, -4.2436278], [1.5767403, 3.4067118, -4.2507073], [5.2625035, 4.7117339, -4.2996003], [4.0675213, 2.194329, -4.2897029], [4.7417245, 0.3299249, -2.2558073], [5.9969157, 2.8580194, -2.2268554], [0.9748391, 5.2373292, -2.2376649], [2.198544, 1.5397536, -2.2315154], [3.4408186, 4.0677313, -2.3337728]]),
),]"""

species_tags = {
    "CO":"""""",
    "Pd":"""""",
    "empty":"""""",
    "oxygen":"""""",
    }

tof_count = {
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Max J. Hoffmann" email="max.hoffmann@ch.tum.de" model_name="sqrt5PdO" model_dimension="2" debug="0"/>
    <species_list default_species="empty">
        <species name="CO" representation="Atoms('CO',[[0,0,0],[0,0,1.2]])" color="#000000" tags=""/>
        <species name="Pd" representation="Atoms('Pd',[[0,0,0]])" color="#0034be" tags=""/>
        <species name="empty" representation="" color="#fff" tags=""/>
        <species name="oxygen" representation="Atoms('O',[[0,0,0]])" color="#ff1717" tags=""/>
    </species_list>
    <parameter_list>
        <parameter name="E_adsorption_o2_bridge_bridge" value="1.9" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_co_bridge" value="" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_co_hollow" value="" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_diff_co_bridge_bridge" value="" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_diff_co_hollow_hollow" value="" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_diff_o_bridge_bridge" value="" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_diff_o_bridge_hollow" value="" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_diff_o_hollow_hollow" value="" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_o_bridge" value="" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_o_hollow" value="" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="T" value="600" adjustable="True" min="500.0" max="600.0" scale="linear"/>
        <parameter name="lattice_size" value="10 10 1" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="p_co" value="1." adjustable="True" min="0.0" max="0.0" scale="linear"/>
        <parameter name="p_o2" value="1." adjustable="True" min="0.0" max="0.0" scale="linear"/>
    </parameter_list>
    <lattice cell_size="1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0" default_layer="PdO" substrate_layer="PdO" representation="[Atoms(symbols='Pd15',
          pbc=np.array([False, False, False]),
          cell=np.array(      ([1.0, 1.0, 1.0])),
          scaled_positions=np.array(      [[4.7453659, 0.3423996, -6.2962764], [5.92199, 2.865787, -6.2962764], [0.87534, 5.2190976, -6.2962764], [2.2219785, 1.5190861, -6.2962764], [3.398665, 4.0424111, -6.2962764], [2.820011, 5.9091707, -4.2497057], [0.340976, 0.918238, -4.2436278], [1.5767403, 3.4067118, -4.2507073], [5.2625035, 4.7117339, -4.2996003], [4.0675213, 2.194329, -4.2897029], [4.7417245, 0.3299249, -2.2558073], [5.9969157, 2.8580194, -2.2268554], [0.9748391, 5.2373292, -2.2376649], [2.198544, 1.5397536, -2.2315154], [3.4408186, 4.0677313, -2.3337728]]),
),]">
        <layer name="Pd100" color="#6dbf6e">
            <site pos="0.1 0.1 0.0" type="h1" tags="" default_species="default_species"/>
            <site pos="0.3 0.5 0.0" type="h2" tags="" default_species="default_species"/>
            <site pos="0.9 0.7 0.0" type="h4" tags="" default_species="default_species"/>
            <site pos="0.7 0.3 0.0" type="h5" tags="" default_species="default_species"/>
            <site pos="0.2 0.3 0.0" type="b1" tags="" default_species="default_species"/>
            <site pos="0.4 0.7 0.0" type="b2" tags="" default_species="default_species"/>
            <site pos="0.5 0.4 0.0" type="b3" tags="" default_species="default_species"/>
            <site pos="0.9 0.2 0.0" type="b4" tags="" default_species="default_species"/>
            <site pos="0.8 0.5 0.0" type="b5" tags="" default_species="default_species"/>
            <site pos="0.7 0.8 0.0" type="b6" tags="" default_species="default_species"/>
            <site pos="0.1 0.6 0.0" type="b7" tags="" default_species="default_species"/>
            <site pos="0.6 0.1 0.0" type="b8" tags="" default_species="default_species"/>
            <site pos="0.3 0.0 0.0" type="b9" tags="" default_species="default_species"/>
            <site pos="0.0 0.9 0.0" type="b10" tags="" default_species="default_species"/>
            <site pos="0.5 0.9 0.0" type="h3" tags="" default_species="default_species"/>
        </layer>
        <layer name="PdO" color="#a14b49">
            <site pos="0.5 0.5 0.1" type="bridge2" tags="" default_species="empty"/>
            <site pos="0.25 0.25 0.2" type="hollow1" tags="" default_species="empty"/>
            <site pos="0.25 0.75 0.2" type="hollow2" tags="" default_species="empty"/>
            <site pos="0.5 0.0 0.1" type="bridge1" tags="" default_species="empty"/>
            <site pos="0.0 0.5 0.1" type="Pd2" tags="" default_species="Pd"/>
            <site pos="0.5 0.25 0.05" type="Pd3" tags="" default_species="Pd"/>
            <site pos="0.5 0.75 0.05" type="Pd4" tags="" default_species="Pd"/>
            <site pos="0.75 0.25 0.0" type="hollow3" tags="" default_species="oxygen"/>
            <site pos="0.75 0.75 0.0" type="hollow4" tags="" default_species="oxygen"/>
            <site pos="0.0 0.0 0.1" type="Pd1" tags="" default_species="Pd"/>
        </layer>
    </lattice>
    <process_list>
        <process rate_constant="10E15" name="destruct1" enabled="False">
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct10" enabled="False">
            <condition species="CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct11" enabled="False">
            <condition species="CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct2" enabled="False">
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct3" enabled="False">
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct4" enabled="False">
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct5" enabled="False">
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct6" enabled="False">
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct7" enabled="False">
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct8" enabled="False">
            <condition species="CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E15" name="destruct9" enabled="False">
            <condition species="CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <condition species="CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="$CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="^CO" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b1" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b10" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b10" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b2" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b2" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b3" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b3" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b3" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b4" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b4" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b4" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b5" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b5" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b5" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b6" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b6" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b6" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b7" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b7" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b8" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b8" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b8" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8*p_co" name="m_COads_b9" enabled="True">
            <condition species="empty" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b1" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b10" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b10" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b2" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b3" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b3" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b3" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b4" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b4" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b4" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b5" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b5" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b5" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b6" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b6" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b6" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b7" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b7" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b8" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b8" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b8" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="m_COdes_b9" enabled="True">
            <condition species="CO" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COads_bridge1" enabled="True">
            <condition species="empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COads_bridge2" enabled="True">
            <condition species="empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COads_hollow1" enabled="True">
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COads_hollow2" enabled="True">
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COdes_bridge1" enabled="True">
            <condition species="CO" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COdes_bridge2" enabled="True">
            <condition species="CO" coord_layer="PdO" coord_name="bridge2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COdes_hollow1" enabled="True">
            <condition species="CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COdes_hollow2" enabled="True">
            <condition species="CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COdif_h1h2down" enabled="True">
            <condition species="CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_COdif_h1h2up" enabled="True">
            <condition species="CO" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
            <action species="CO" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E12*p_o2" name="o_O2ads_h1h2" enabled="False">
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
            <action species="oxygen" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="oxygen" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E12*p_o2" name="o_O2ads_h2h1" enabled="False">
            <condition species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 1 0"/>
            <action species="oxygen" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
            <action species="oxygen" coord_layer="PdO" coord_name="hollow1" coord_offset="0 1 0"/>
        </process>
        <process rate_constant="10E8" name="o_O2des_h1h2" enabled="True">
            <condition species="oxygen" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <condition species="oxygen" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E8" name="o_O2des_h2h1" enabled="True">
            <condition species="oxygen" coord_layer="PdO" coord_name="hollow1" coord_offset="0 1 0"/>
            <condition species="oxygen" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
            <action species="empty" coord_layer="PdO" coord_name="hollow1" coord_offset="0 1 0"/>
            <action species="empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="10E15" name="oxidize1" enabled="True">
            <condition species="oxygen" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <condition species="empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
            <action species="$oxygen" coord_layer="Pd100" coord_name="h1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="Pd100" coord_name="b1" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="Pd100" coord_name="b9" coord_offset="0 0 0"/>
            <action species="$empty" coord_layer="Pd100" coord_name="b10" coord_offset="0 -1 0"/>
            <action species="$empty" coord_layer="Pd100" coord_name="b7" coord_offset="0 -1 0"/>
            <action species="^oxygen" coord_layer="PdO" coord_name="hollow1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="PdO" coord_name="hollow2" coord_offset="0 -1 0"/>
            <action species="^empty" coord_layer="PdO" coord_name="bridge1" coord_offset="0 0 0"/>
            <action species="^empty" coord_layer="PdO" coord_name="bridge2" coord_offset="0 -1 0"/>
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
