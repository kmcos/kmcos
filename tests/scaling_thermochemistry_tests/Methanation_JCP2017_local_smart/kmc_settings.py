model_name = 'Methanation_JCP2017'
simulation_size = 20
buffer_parameter = 1000
threshold_parameter = 0.2
sampling_steps = 20
execution_steps = 200
save_limit = 1000
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
    "A":{"value":"6.582*2.686*angstrom**2", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C":{"value":"1.75", "adjustable":True, "min":"0.0", "max":"3.4","scale":"linear"},
    "E_CH2_H_s":{"value":"(0.5702004*E_C+0.0000000*E_O+(0.2671380))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH2_H_t":{"value":"(0.4478376*E_C+0.0000000*E_O+(0.8536176))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH2_diff":{"value":"0.61", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH2_s":{"value":"(0.5182100*E_C+0.0000000*E_O+(0.0808500))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH2_t":{"value":"(0.3725400*E_C+0.0000000*E_O+(0.7790400))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH3_H_s":{"value":"(0.2833253*E_C+0.0000000*E_O+(0.4130144))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH3_H_t":{"value":"(0.2666275*E_C+0.0000000*E_O+(0.6568485))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH3_diff":{"value":"0.51", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH3_s":{"value":"(0.2512100*E_C+0.0000000*E_O+(-0.0423000))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH3_t":{"value":"(0.2269400*E_C+0.0000000*E_O+(0.3121100))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH4gas":{"value":"0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH_H_f":{"value":"(0.7797550*E_C+0.0000000*E_O+(0.5644764))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH_H_s":{"value":"(0.7924584*E_C+0.0000000*E_O+(0.5548021))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH_H_t":{"value":"(0.7594745*E_C+0.0000000*E_O+(0.7527916))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH__t":{"value":"(0.6374425*E_C+0.0000000*E_O+(0.8626726))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH_diff":{"value":"0.37", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH_f":{"value":"(0.7429400*E_C+0.0000000*E_O+(0.0613900))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH_s":{"value":"(0.7576600*E_C+0.0000000*E_O+(0.0501800))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CH_t":{"value":"(0.7194400*E_C+0.0000000*E_O+(0.2796000))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CO_diff":{"value":"0.11", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CO_s":{"value":"(0.3820000*E_C+0.0000000*E_O+(0.2943200))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_CO_t":{"value":"(0.4036300*E_C+0.0000000*E_O+(0.4840200))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_COgas":{"value":"2.53", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C_H_f":{"value":"(0.9981160*E_C+0.0000000*E_O+(0.7638960))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C_H_s":{"value":"(1.0014700*E_C+0.0000000*E_O+(1.1456844))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C_H_t":{"value":"(0.9333322*E_C+0.0000000*E_O+(1.5325726))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C_OH_f":{"value":"(0.8650000*E_C+0.2819208*E_O+(1.2488243))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C__f":{"value":"(0.2150000*E_C+0.0000000*E_O+(2.4100000))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C_diff":{"value":"0.48", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C_f":{"value":"(1.0000000*E_C+0.0000000*E_O+(0.0000000))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C_s":{"value":"(1.0039000*E_C+0.0000000*E_O+(0.4439400))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_C_t":{"value":"(0.9246700*E_C+0.0000000*E_O+(0.8938100))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_H2O_O__s":{"value":"(0.0000000*E_C+1.0000000*E_O+(0.0000000))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_H2O_O__t":{"value":"(0.0000000*E_C+0.9986800*E_O+(0.4753200))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_H2O_O_s":{"value":"(0.0000000*E_C+1.0000000*E_O+(0.0000000))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_H2O_O_t":{"value":"(0.0000000*E_C+0.9986800*E_O+(0.4753200))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_H2Ogas":{"value":"0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_H2gas":{"value":"0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_H_OH_s":{"value":"(0.0889724*E_C+0.2981794*E_O+(0.5249536))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_H_OH_t":{"value":"(0.0889724*E_C+0.1805597*E_O+(0.9831227))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_H_t":{"value":"(0.1606000*E_C+0.0000000*E_O+(-0.4664000))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_O":{"value":"-1.35", "adjustable":True, "min":"-1.8", "max":"1.4","scale":"linear"},
    "E_OH_diff":{"value":"0.44", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_OH_s":{"value":"(0.0000000*E_C+0.5382300*E_O+(-0.5752000))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_OH_t":{"value":"(0.0000000*E_C+0.3259200*E_O+(0.2518200))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_O_H_s":{"value":"(0.1108140*E_C+0.6900000*E_O+(0.7281840))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_O_H_t":{"value":"(0.1108140*E_C+0.6890892*E_O+(1.0561548))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_O_diff":{"value":"0.82", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_O_s":{"value":"(0.0000000*E_C+1.0000000*E_O+(0.0000000))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_O_t":{"value":"(0.0000000*E_C+0.9986800*E_O+(0.4753200))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "H_cov":{"value":"(1/(1+sqrt(exp(-beta*(GibbsGas_H2gas-2*GibbsAds_H_t)*eV))))", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "T":{"value":"523.0", "adjustable":True, "min":"400.0", "max":"800.0","scale":"linear"},
    "alpha":{"value":"0.5", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH2_H_s":{"value":"[56, 56, 233.3, 506.4, 578.9, 789.0, 904.0, 1326.7, 1822.0, 2925.1, 3029.3]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH2_H_t":{"value":"[56, 56, 233.3, 506.4, 578.9, 789.0, 904.0, 1326.7, 1822.0, 2925.1, 3029.3]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH2_s":{"value":"[56, 289.2, 405.2, 498.9, 597.8, 716.6, 1294.3, 2874.0, 3011.2]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH2_t":{"value":"[89.2, 185.8, 297.1, 456.4, 513.0, 705.4, 1339.5, 2647.4, 2968.4]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH3_H_s":{"value":"[56, 56, 90.9, 157.9, 338.3, 699.0, 812.7, 1248.0, 1370.9, 1418.0, 1609.6, 2916.4, 2997.4, 3076.0]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH3_H_t":{"value":"[56, 56, 90.9, 157.9, 338.3, 699.0, 812.7, 1248.0, 1370.9, 1418.0, 1609.6, 2916.4, 2997.4, 3076.0]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH3_s":{"value":"[56, 56, 56, 252.1, 353.1, 623.3, 1119.6, 1304.3, 1358.3, 2748.0, 2813.4, 3037.3]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH3_t":{"value":"[56, 56, 56, 350.3, 645.4, 679.9, 1117.1, 1381.2, 1400.0, 2903.6, 3002.2, 3016.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH_H_f":{"value":"[56, 332.3, 376.8, 547.7, 640.6, 894.1, 1541.2, 2975.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH_H_s":{"value":"[56, 332.3, 376.8, 547.7, 640.6, 894.1, 1541.2, 2975.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH_H_t":{"value":"[56, 332.3, 376.8, 547.7, 640.6, 894.1, 1541.2, 2975.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH__t":{"value":"[542.7, 605.4, 637.7, 759.4, 3073.2]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH_f":{"value":"[299.9, 347.1, 400.2, 692.2, 739.5, 2896.6]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH_s":{"value":"[356.6, 401.3, 528.4, 610.7, 637.6, 2906.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CH_t":{"value":"[367.9, 388.9, 568.5, 643.9, 696.1, 2958.0]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CO_s":{"value":"[198.2, 269.2, 390.7, 418.4, 489.8, 2002.2]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_CO_t":{"value":"[207.7, 267.2, 413.5, 424.4, 465.6, 1978.8]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_C_H_f":{"value":"[331.4, 512.6, 534.5, 585.5, 1010.5]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_C_H_s":{"value":"[331.4, 512.6, 534.5, 585.5, 1010.5]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_C_H_t":{"value":"[331.4, 512.6, 534.5, 585.5, 1010.5]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_C_OH_f":{"value":"[62.2, 268.2, 369.3, 408.9, 426.5, 748.8, 822.6, 3609.3]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_C__f":{"value":"[296.6, 907.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_C_f":{"value":"[317.9, 510.1, 521.2]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_C_s":{"value":"[468.3, 503.6, 522.4]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_C_t":{"value":"[463.0, 487.6, 513.7]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_H2O_O__s":{"value":"[56, 120.8, 331.4, 439.9, 522.5, 542.4, 637.0, 758.6, 1315.4, 1512.6, 3709.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_H2O_O__t":{"value":"[56, 120.8, 331.4, 439.9, 522.5, 542.4, 637.0, 758.6, 1315.4, 1512.6, 3709.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_H2O_O_s":{"value":"[56, 120.8, 331.4, 439.9, 522.5, 542.4, 637.0, 758.6, 1315.4, 1512.6, 3709.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_H2O_O_t":{"value":"[56, 120.8, 331.4, 439.9, 522.5, 542.4, 637.0, 758.6, 1315.4, 1512.6, 3709.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_H_OH_s":{"value":"[56, 288.1, 331.0, 414.1, 533.0, 626.8, 1008.9, 3544.2]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_H_OH_t":{"value":"[56, 288.1, 331.0, 414.1, 533.0, 626.8, 1008.9, 3544.2]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_H_t":{"value":"[402.8, 572.6, 1013.7]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_OH_s":{"value":"[56, 274.3, 382.8, 657.2, 763.5, 3634.2]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_OH_t":{"value":"[176.7, 305.8, 408.4, 679.3, 712.7, 3602.1]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_O_H_s":{"value":"[412.5, 428.8, 506.7, 550.3, 1069.4]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_O_H_t":{"value":"[412.5, 428.8, 506.7, 550.3, 1069.4]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_O_s":{"value":"[380.0, 444.0, 537.6]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "f_O_t":{"value":"[418.8, 449.2, 517.3]", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "p_CH4gas":{"value":"0.01", "adjustable":True, "min":"1e-10", "max":"100.0","scale":"linear"},
    "p_COgas":{"value":"0.01", "adjustable":True, "min":"1e-10", "max":"100.0","scale":"linear"},
    "p_H2Ogas":{"value":"0.01", "adjustable":True, "min":"1e-10", "max":"100.0","scale":"linear"},
    "p_H2gas":{"value":"0.97", "adjustable":True, "min":"1e-10", "max":"100.0","scale":"linear"},
    }

proc_pair_indices = [1, -1, 2, 3, -3, 4, -2, -4, 5, 6, 7, 8, 9, 10, -10, 11, 12, -12, 13, -11, -13, 14, 15, 16, 17, 18, -18, 19, 20, 21, -19, 22, -22, 23, 24, -21, -24, 25, -20, -23, -25, 26, 27, 28, 29, 30, -29, -30, 31, -31, 32, 33, -33, 34, -32, -34, 35, 36, 37, 38, 39, -39, 40, 41, 42, -40, 43, -43, 44, 45, -42, -45, 46, -41, -44, -46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, -14, -15, -16, -17, -5, -9, -7, -6, -8, -35, -36, -37, -38, -26, -27, -28, -55, -56, 57, 58, -47, -48, -49, -50, -51, -52, -53, -54, 59, -59, 60, 61, -61, 62, -60, -62, -57, -58, 63, -63, 64, 65, -65, 66, -64, -66]

is_diff_proc = [True, True, True, True, True, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, False, False, True, True, True, True, True, True, True, True]

rate_constants = {
    "CH2_diff_s_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_s-GibbsAds_CH2_s)+E_CH2_diff),0)*eV)", True),
    "CH2_diff_s_s_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_s-GibbsAds_CH2_s)+E_CH2_diff),0)*eV)", True),
    "CH2_diff_s_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_t-GibbsAds_CH2_s)+E_CH2_diff),0)*eV)", True),
    "CH2_diff_s_t_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_t-GibbsAds_CH2_s)+E_CH2_diff),0)*eV)", True),
    "CH2_diff_t_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_s-GibbsAds_CH2_t)+E_CH2_diff),0)*eV)", True),
    "CH2_diff_t_S_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_t-GibbsAds_CH2_t)+E_CH2_diff),0)*eV)", True),
    "CH2_diff_t_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_s-GibbsAds_CH2_t)+E_CH2_diff),0)*eV)", True),
    "CH2_diff_t_t_S":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_t-GibbsAds_CH2_t)+E_CH2_diff),0)*eV)", True),
    "CH2_s_E_dis_f":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH_f+GibbsAds_H_t)-GibbsAds_CH2_s,0)*eV)", True),
    "CH2_s_dis":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_s,GibbsAds_CH_s+GibbsAds_H_t)-GibbsAds_CH2_s,0)*eV)", True),
    "CH2_t_N_dis_f":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH_f+GibbsAds_H_t)-GibbsAds_CH2_t,0)*eV)", True),
    "CH2_t_dis":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_t,GibbsAds_CH_t+GibbsAds_H_t)-GibbsAds_CH2_t,0)*eV)", True),
    "CH2_t_dis_f":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH_f+GibbsAds_H_t)-GibbsAds_CH2_t,0)*eV)", True),
    "CH3_diff_s_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_s-GibbsAds_CH3_s)+E_CH3_diff),0)*eV)", True),
    "CH3_diff_s_s_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_s-GibbsAds_CH3_s)+E_CH3_diff),0)*eV)", True),
    "CH3_diff_s_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_t-GibbsAds_CH3_s)+E_CH3_diff),0)*eV)", True),
    "CH3_diff_s_t_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_t-GibbsAds_CH3_s)+E_CH3_diff),0)*eV)", True),
    "CH3_diff_t_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_s-GibbsAds_CH3_t)+E_CH3_diff),0)*eV)", True),
    "CH3_diff_t_S_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_t-GibbsAds_CH3_t)+E_CH3_diff),0)*eV)", True),
    "CH3_diff_t_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_s-GibbsAds_CH3_t)+E_CH3_diff),0)*eV)", True),
    "CH3_diff_t_t_S":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_t-GibbsAds_CH3_t)+E_CH3_diff),0)*eV)", True),
    "CH3_s_dis":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_s,GibbsAds_CH2_s+GibbsAds_H_t)-GibbsAds_CH3_s,0)*eV)", True),
    "CH3_t_dis":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_t,GibbsAds_CH2_t+GibbsAds_H_t)-GibbsAds_CH3_t,0)*eV)", True),
    "CH4_s_ads":("(1-H_cov)/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_s,GibbsAds_CH3_s+GibbsAds_H_t)-GibbsGas_CH4gas,0)*eV)", True),
    "CH4_t_ads":("(1-H_cov)/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_t,GibbsAds_CH3_t+GibbsAds_H_t)-GibbsGas_CH4gas,0)*eV)", True),
    "CH_diff_f_S_f":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_f-GibbsAds_CH_f)+E_CH_diff),0)*eV)", True),
    "CH_diff_f_f_S":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_f-GibbsAds_CH_f)+E_CH_diff),0)*eV)", True),
    "CH_diff_f_s_E":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_f)+E_CH_diff),0)*eV)", True),
    "CH_diff_f_t":("1/(beta*h)*exp(-beta*max(max(GibbsAds_CH__t,GibbsAds_CH_t)-GibbsAds_CH_f,0)*eV)", True),
    "CH_diff_f_t_N":("1/(beta*h)*exp(-beta*max(max(GibbsAds_CH__t,GibbsAds_CH_t)-GibbsAds_CH_f,0)*eV)", True),
    "CH_diff_s_E_f":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_f-GibbsAds_CH_s)+E_CH_diff),0)*eV)", True),
    "CH_diff_s_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_s)+E_CH_diff),0)*eV)", True),
    "CH_diff_s_s_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_s)+E_CH_diff),0)*eV)", True),
    "CH_diff_s_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_t-GibbsAds_CH_s)+E_CH_diff),0)*eV)", True),
    "CH_diff_s_t_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_t-GibbsAds_CH_s)+E_CH_diff),0)*eV)", True),
    "CH_diff_t_N_f":("1/(beta*h)*exp(-beta*max(max(GibbsAds_CH__t,GibbsAds_CH_f)-GibbsAds_CH_t,0)*eV)", True),
    "CH_diff_t_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_t)+E_CH_diff),0)*eV)", True),
    "CH_diff_t_S_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_t-GibbsAds_CH_t)+E_CH_diff),0)*eV)", True),
    "CH_diff_t_f":("1/(beta*h)*exp(-beta*max(max(GibbsAds_CH__t,GibbsAds_CH_f)-GibbsAds_CH_t,0)*eV)", True),
    "CH_diff_t_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_t)+E_CH_diff),0)*eV)", True),
    "CH_diff_t_t_S":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_t-GibbsAds_CH_t)+E_CH_diff),0)*eV)", True),
    "CH_f_dis":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_f,GibbsAds_C_f+GibbsAds_H_t)-GibbsAds_CH_f,0)*eV)", True),
    "CH_s_dis":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_s,GibbsAds_C_s+GibbsAds_H_t)-GibbsAds_CH_s,0)*eV)", True),
    "CH_t_dis":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_t,GibbsAds_C_t+GibbsAds_H_t)-GibbsAds_CH_t,0)*eV)", True),
    "CO_ads_s":("p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_s)-GibbsGas_COgas)*eV)", True),
    "CO_ads_t":("p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_t)-GibbsGas_COgas)*eV)", True),
    "CO_des_s":("p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_s)-GibbsAds_CO_s)*eV)", True),
    "CO_des_t":("p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_t)-GibbsAds_CO_t)*eV)", True),
    "CO_diff_s_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_s-GibbsAds_CO_s)+E_CO_diff),0)*eV)", True),
    "CO_diff_s_s_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_s-GibbsAds_CO_s)+E_CO_diff),0)*eV)", True),
    "CO_diff_s_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_t-GibbsAds_CO_s)+E_CO_diff),0)*eV)", True),
    "CO_diff_s_t_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_t-GibbsAds_CO_s)+E_CO_diff),0)*eV)", True),
    "CO_diff_t_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_s-GibbsAds_CO_t)+E_CO_diff),0)*eV)", True),
    "CO_diff_t_S_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_t-GibbsAds_CO_t)+E_CO_diff),0)*eV)", True),
    "CO_diff_t_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_s-GibbsAds_CO_t)+E_CO_diff),0)*eV)", True),
    "CO_diff_t_t_S":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_t-GibbsAds_CO_t)+E_CO_diff),0)*eV)", True),
    "C_OH_s_react_t_NW":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_s+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)", True),
    "C_OH_s_react_t_W":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_s+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)", True),
    "C_OH_t_react_f":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_t+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)", True),
    "C_OH_t_react_f_S":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_t+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)", True),
    "C_diff_f_S_f":("1/(beta*h)*exp(-beta*max(max(GibbsAds_C__f,GibbsAds_C_f)-GibbsAds_C_f,0)*eV)", True),
    "C_diff_f_f_S":("1/(beta*h)*exp(-beta*max(max(GibbsAds_C__f,GibbsAds_C_f)-GibbsAds_C_f,0)*eV)", True),
    "C_diff_f_s_E":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_f)+E_C_diff),0)*eV)", True),
    "C_diff_f_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_f)+E_C_diff),0)*eV)", True),
    "C_diff_f_t_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_f)+E_C_diff),0)*eV)", True),
    "C_diff_s_E_f":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_f-GibbsAds_C_s)+E_C_diff),0)*eV)", True),
    "C_diff_s_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_s)+E_C_diff),0)*eV)", True),
    "C_diff_s_s_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_s)+E_C_diff),0)*eV)", True),
    "C_diff_s_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_s)+E_C_diff),0)*eV)", True),
    "C_diff_s_t_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_s)+E_C_diff),0)*eV)", True),
    "C_diff_t_N_f":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_f-GibbsAds_C_t)+E_C_diff),0)*eV)", True),
    "C_diff_t_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_t)+E_C_diff),0)*eV)", True),
    "C_diff_t_S_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_t)+E_C_diff),0)*eV)", True),
    "C_diff_t_f":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_f-GibbsAds_C_t)+E_C_diff),0)*eV)", True),
    "C_diff_t_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_t)+E_C_diff),0)*eV)", True),
    "C_diff_t_t_S":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_t)+E_C_diff),0)*eV)", True),
    "H2O_O_s_react_s_N":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_s,2*GibbsAds_OH_s)-(GibbsAds_O_s+GibbsGas_H2Ogas),0)*eV)", True),
    "H2O_O_s_react_s_S":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_s,2*GibbsAds_OH_s)-(GibbsAds_O_s+GibbsGas_H2Ogas),0)*eV)", True),
    "H2O_O_s_react_t":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__s,(GibbsAds_OH_s+GibbsAds_OH_t))-(GibbsAds_O_s+GibbsGas_H2Ogas),0)*eV)", True),
    "H2O_O_s_react_t_N":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__s,(GibbsAds_OH_s+GibbsAds_OH_t))-(GibbsAds_O_s+GibbsGas_H2Ogas),0)*eV)", True),
    "H2O_O_t_N_react_s":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__t,(GibbsAds_OH_t+GibbsAds_OH_s))-(GibbsAds_O_t+GibbsGas_H2Ogas),0)*eV)", True),
    "H2O_O_t_react_s":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__t,(GibbsAds_OH_t+GibbsAds_OH_s))-(GibbsAds_O_t+GibbsGas_H2Ogas),0)*eV)", True),
    "H2O_O_t_react_t_N":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_t,2*GibbsAds_OH_t)-(GibbsAds_O_t+GibbsGas_H2Ogas),0)*eV)", True),
    "H2O_O_t_react_t_S":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_t,2*GibbsAds_OH_t)-(GibbsAds_O_t+GibbsGas_H2Ogas),0)*eV)", True),
    "H2O_s_ads":("(1-H_cov)*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_s,GibbsAds_OH_s+GibbsAds_H_t)-GibbsGas_H2Ogas,0)*eV)", True),
    "H2O_t_ads":("(1-H_cov)*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_t,GibbsAds_OH_t+GibbsAds_H_t)-GibbsGas_H2Ogas,0)*eV)", True),
    "H_CH2_s_react":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_s,GibbsAds_CH3_s)-(GibbsAds_CH2_s+GibbsAds_H_t),0)*eV)", True),
    "H_CH2_t_react":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_t,GibbsAds_CH3_t)-(GibbsAds_CH2_t+GibbsAds_H_t),0)*eV)", True),
    "H_CH3_s_react":("H_cov/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_s,GibbsGas_CH4gas)-(GibbsAds_CH3_s+GibbsAds_H_t),0)*eV)", True),
    "H_CH3_t_react":("H_cov/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_t,GibbsGas_CH4gas)-(GibbsAds_CH3_t+GibbsAds_H_t),0)*eV)", True),
    "H_CH_f_react_s_E":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH2_s)-(GibbsAds_CH_f+GibbsAds_H_t),0)*eV)", True),
    "H_CH_f_react_t":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH2_t)-(GibbsAds_CH_f+GibbsAds_H_t),0)*eV)", True),
    "H_CH_f_react_t_N":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH2_t)-(GibbsAds_CH_f+GibbsAds_H_t),0)*eV)", True),
    "H_CH_s_react":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_s,GibbsAds_CH2_s)-(GibbsAds_CH_s+GibbsAds_H_t),0)*eV)", True),
    "H_CH_t_react":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_t,GibbsAds_CH2_t)-(GibbsAds_CH_t+GibbsAds_H_t),0)*eV)", True),
    "H_CO_s_react_t_NW":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_s+GibbsAds_H_t),0)*eV)", True),
    "H_CO_s_react_t_W":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_s+GibbsAds_H_t),0)*eV)", True),
    "H_CO_t_react_f":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_t+GibbsAds_H_t),0)*eV)", True),
    "H_CO_t_react_f_S":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_t+GibbsAds_H_t),0)*eV)", True),
    "H_C_f_react":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_f,GibbsAds_CH_f)-(GibbsAds_C_f+GibbsAds_H_t),0)*eV)", True),
    "H_C_s_react":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_s,GibbsAds_CH_s)-(GibbsAds_C_s+GibbsAds_H_t),0)*eV)", True),
    "H_C_t_react":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_t,GibbsAds_CH_t)-(GibbsAds_C_t+GibbsAds_H_t),0)*eV)", True),
    "H_OH_s_react":("H_cov*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_s,GibbsGas_H2Ogas)-(GibbsAds_OH_s+GibbsAds_H_t),0)*eV)", True),
    "H_OH_t_react":("H_cov*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_t,GibbsGas_H2Ogas)-(GibbsAds_OH_t+GibbsAds_H_t),0)*eV)", True),
    "H_O_s_react":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_s,GibbsAds_OH_s)-(GibbsAds_O_s+GibbsAds_H_t),0)*eV)", True),
    "H_O_t_react":("H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_t,GibbsAds_OH_t)-(GibbsAds_O_t+GibbsAds_H_t),0)*eV)", True),
    "OH_OH_s_react_s_N":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_s,GibbsAds_O_s+GibbsGas_H2Ogas)-(2*GibbsAds_OH_s),0)*eV)", True),
    "OH_OH_s_react_s_S":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_s,GibbsAds_O_s+GibbsGas_H2Ogas)-(2*GibbsAds_OH_s),0)*eV)", True),
    "OH_OH_s_react_t":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__s,GibbsAds_O_s+GibbsGas_H2Ogas)-(GibbsAds_OH_s+GibbsAds_OH_t),0)*eV)", True),
    "OH_OH_s_react_t_N":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__s,GibbsAds_O_s+GibbsGas_H2Ogas)-(GibbsAds_OH_s+GibbsAds_OH_t),0)*eV)", True),
    "OH_OH_t_N_react_s":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__t,GibbsAds_O_t+GibbsGas_H2Ogas)-(GibbsAds_OH_t+GibbsAds_OH_s),0)*eV)", True),
    "OH_OH_t_react_s":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__t,GibbsAds_O_t+GibbsGas_H2Ogas)-(GibbsAds_OH_t+GibbsAds_OH_s),0)*eV)", True),
    "OH_OH_t_react_t_N":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_t,GibbsAds_O_t+GibbsGas_H2Ogas)-(2*GibbsAds_OH_t),0)*eV)", True),
    "OH_OH_t_react_t_S":("1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_t,GibbsAds_O_t+GibbsGas_H2Ogas)-(2*GibbsAds_OH_t),0)*eV)", True),
    "OH_diff_s_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_s-GibbsAds_OH_s)+E_OH_diff),0)*eV)", True),
    "OH_diff_s_s_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_s-GibbsAds_OH_s)+E_OH_diff),0)*eV)", True),
    "OH_diff_s_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_t-GibbsAds_OH_s)+E_OH_diff),0)*eV)", True),
    "OH_diff_s_t_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_t-GibbsAds_OH_s)+E_OH_diff),0)*eV)", True),
    "OH_diff_t_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_s-GibbsAds_OH_t)+E_OH_diff),0)*eV)", True),
    "OH_diff_t_S_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_t-GibbsAds_OH_t)+E_OH_diff),0)*eV)", True),
    "OH_diff_t_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_s-GibbsAds_OH_t)+E_OH_diff),0)*eV)", True),
    "OH_diff_t_t_S":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_t-GibbsAds_OH_t)+E_OH_diff),0)*eV)", True),
    "OH_s_dis":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_s,GibbsAds_O_s+GibbsAds_H_t)-GibbsAds_OH_s,0)*eV)", True),
    "OH_t_dis":("(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_t,GibbsAds_O_t+GibbsAds_H_t)-GibbsAds_OH_t,0)*eV)", True),
    "O_diff_s_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_s-GibbsAds_O_s)+E_O_diff),0)*eV)", True),
    "O_diff_s_s_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_s-GibbsAds_O_s)+E_O_diff),0)*eV)", True),
    "O_diff_s_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_t-GibbsAds_O_s)+E_O_diff),0)*eV)", True),
    "O_diff_s_t_N":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_t-GibbsAds_O_s)+E_O_diff),0)*eV)", True),
    "O_diff_t_N_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_s-GibbsAds_O_t)+E_O_diff),0)*eV)", True),
    "O_diff_t_S_t":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_t-GibbsAds_O_t)+E_O_diff),0)*eV)", True),
    "O_diff_t_s":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_s-GibbsAds_O_t)+E_O_diff),0)*eV)", True),
    "O_diff_t_t_S":("1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_t-GibbsAds_O_t)+E_O_diff),0)*eV)", True),
    }

site_names = ['Rh211_s', 'Rh211_t', 'Rh211_f']
representations = {
    "C":"""Atoms('C')""",
    "CH":"""Atoms('CH',[[0,0,0],[0,0,1.09]])""",
    "CH2":"""Atoms('CH2',[[0,0,0],[0,0.7,0.8],[0,-0.7,0.8]])""",
    "CH3":"""Atoms('CH3',[[0,0,0],[-0.3,0.5,0.8],[-0.3,-0.5,0.8],[0.7,0,0.8]])""",
    "CO":"""Atoms('CO',[[0,0,0],[0,0,1.2]])""",
    "O":"""Atoms('O')""",
    "OH":"""Atoms('OH',[[0,0,0],[0,0,0.96]])""",
    "empty":"""""",
    }

lattice_representation = """[Atoms(symbols='Rh3',
          pbc=np.array([False, False, False]),
          cell=np.array(      ([6.582, 2.686, 20.0])),
          scaled_positions=np.array(      [[0.0, 0.0, 0.5388], [0.3334853, 0.5003723, 0.5], [0.6668186, 0.0, 0.4612]]),
),]"""

species_tags = {
    "C":"""""",
    "CH":"""""",
    "CH2":"""""",
    "CH3":"""""",
    "CO":"""""",
    "O":"""""",
    "OH":"""""",
    "empty":"""""",
    }

tof_count = {
    "CH4_s_ads":{'CH4_formation': -1},
    "CH4_t_ads":{'CH4_formation': -1},
    "H2O_O_s_react_s_N":{'H2O_formation': -1},
    "H2O_O_s_react_s_S":{'H2O_formation': -1},
    "H2O_O_s_react_t":{'H2O_formation': -1},
    "H2O_O_s_react_t_N":{'H2O_formation': -1},
    "H2O_O_t_N_react_s":{'H2O_formation': -1},
    "H2O_O_t_react_s":{'H2O_formation': -1},
    "H2O_O_t_react_t_N":{'H2O_formation': -1},
    "H2O_O_t_react_t_S":{'H2O_formation': -1},
    "H2O_s_ads":{'H2O_formation': -1},
    "H2O_t_ads":{'H2O_formation': -1},
    "H_CH3_s_react":{'CH4_formation': 1},
    "H_CH3_t_react":{'CH4_formation': 1},
    "H_OH_s_react":{'H2O_formation': 1},
    "H_OH_t_react":{'H2O_formation': 1},
    "OH_OH_s_react_s_N":{'H2O_formation': 1},
    "OH_OH_s_react_s_S":{'H2O_formation': 1},
    "OH_OH_s_react_t":{'H2O_formation': 1},
    "OH_OH_s_react_t_N":{'H2O_formation': 1},
    "OH_OH_t_N_react_s":{'H2O_formation': 1},
    "OH_OH_t_react_s":{'H2O_formation': 1},
    "OH_OH_t_react_t_N":{'H2O_formation': 1},
    "OH_OH_t_react_t_S":{'H2O_formation': 1},
    }

xml = """<?xml version="1.0" ?>
<kmc version="(0, 3)">
    <meta author="Mie Andersen" debug="0" email="mie.andersen@ch.tum.de" model_dimension="2" model_name="Methanation_JCP2017"/>
    <species_list default_species="empty">
        <species color="#D3D3D3" name="C" representation="Atoms('C')" tags=""/>
        <species color="#ffff00" name="CH" representation="Atoms('CH',[[0,0,0],[0,0,1.09]])" tags=""/>
        <species color="#FFA500" name="CH2" representation="Atoms('CH2',[[0,0,0],[0,0.7,0.8],[0,-0.7,0.8]])" tags=""/>
        <species color="#551a8b" name="CH3" representation="Atoms('CH3',[[0,0,0],[-0.3,0.5,0.8],[-0.3,-0.5,0.8],[0.7,0,0.8]])" tags=""/>
        <species color="#00ff00" name="CO" representation="Atoms('CO',[[0,0,0],[0,0,1.2]])" tags=""/>
        <species color="#ff0000" name="O" representation="Atoms('O')" tags=""/>
        <species color="#0065bd" name="OH" representation="Atoms('OH',[[0,0,0],[0,0,0.96]])" tags=""/>
        <species color="#ffffff" name="empty" representation="" tags=""/>
    </species_list>
    <parameter_list>
        <parameter adjustable="False" max="0.0" min="0.0" name="A" scale="linear" value="6.582*2.686*angstrom**2"/>
        <parameter adjustable="True" max="3.4" min="0.0" name="E_C" scale="linear" value="1.75"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH2_H_s" scale="linear" value="(0.5702004*E_C+0.0000000*E_O+(0.2671380))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH2_H_t" scale="linear" value="(0.4478376*E_C+0.0000000*E_O+(0.8536176))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH2_diff" scale="linear" value="0.61"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH2_s" scale="linear" value="(0.5182100*E_C+0.0000000*E_O+(0.0808500))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH2_t" scale="linear" value="(0.3725400*E_C+0.0000000*E_O+(0.7790400))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH3_H_s" scale="linear" value="(0.2833253*E_C+0.0000000*E_O+(0.4130144))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH3_H_t" scale="linear" value="(0.2666275*E_C+0.0000000*E_O+(0.6568485))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH3_diff" scale="linear" value="0.51"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH3_s" scale="linear" value="(0.2512100*E_C+0.0000000*E_O+(-0.0423000))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH3_t" scale="linear" value="(0.2269400*E_C+0.0000000*E_O+(0.3121100))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH4gas" scale="linear" value="0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH_H_f" scale="linear" value="(0.7797550*E_C+0.0000000*E_O+(0.5644764))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH_H_s" scale="linear" value="(0.7924584*E_C+0.0000000*E_O+(0.5548021))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH_H_t" scale="linear" value="(0.7594745*E_C+0.0000000*E_O+(0.7527916))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH__t" scale="linear" value="(0.6374425*E_C+0.0000000*E_O+(0.8626726))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH_diff" scale="linear" value="0.37"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH_f" scale="linear" value="(0.7429400*E_C+0.0000000*E_O+(0.0613900))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH_s" scale="linear" value="(0.7576600*E_C+0.0000000*E_O+(0.0501800))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CH_t" scale="linear" value="(0.7194400*E_C+0.0000000*E_O+(0.2796000))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CO_diff" scale="linear" value="0.11"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CO_s" scale="linear" value="(0.3820000*E_C+0.0000000*E_O+(0.2943200))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_CO_t" scale="linear" value="(0.4036300*E_C+0.0000000*E_O+(0.4840200))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_COgas" scale="linear" value="2.53"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_C_H_f" scale="linear" value="(0.9981160*E_C+0.0000000*E_O+(0.7638960))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_C_H_s" scale="linear" value="(1.0014700*E_C+0.0000000*E_O+(1.1456844))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_C_H_t" scale="linear" value="(0.9333322*E_C+0.0000000*E_O+(1.5325726))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_C_OH_f" scale="linear" value="(0.8650000*E_C+0.2819208*E_O+(1.2488243))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_C__f" scale="linear" value="(0.2150000*E_C+0.0000000*E_O+(2.4100000))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_C_diff" scale="linear" value="0.48"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_C_f" scale="linear" value="(1.0000000*E_C+0.0000000*E_O+(0.0000000))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_C_s" scale="linear" value="(1.0039000*E_C+0.0000000*E_O+(0.4439400))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_C_t" scale="linear" value="(0.9246700*E_C+0.0000000*E_O+(0.8938100))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_H2O_O__s" scale="linear" value="(0.0000000*E_C+1.0000000*E_O+(0.0000000))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_H2O_O__t" scale="linear" value="(0.0000000*E_C+0.9986800*E_O+(0.4753200))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_H2O_O_s" scale="linear" value="(0.0000000*E_C+1.0000000*E_O+(0.0000000))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_H2O_O_t" scale="linear" value="(0.0000000*E_C+0.9986800*E_O+(0.4753200))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_H2Ogas" scale="linear" value="0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_H2gas" scale="linear" value="0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_H_OH_s" scale="linear" value="(0.0889724*E_C+0.2981794*E_O+(0.5249536))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_H_OH_t" scale="linear" value="(0.0889724*E_C+0.1805597*E_O+(0.9831227))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_H_t" scale="linear" value="(0.1606000*E_C+0.0000000*E_O+(-0.4664000))"/>
        <parameter adjustable="True" max="1.4" min="-1.8" name="E_O" scale="linear" value="-1.35"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_OH_diff" scale="linear" value="0.44"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_OH_s" scale="linear" value="(0.0000000*E_C+0.5382300*E_O+(-0.5752000))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_OH_t" scale="linear" value="(0.0000000*E_C+0.3259200*E_O+(0.2518200))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_O_H_s" scale="linear" value="(0.1108140*E_C+0.6900000*E_O+(0.7281840))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_O_H_t" scale="linear" value="(0.1108140*E_C+0.6890892*E_O+(1.0561548))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_O_diff" scale="linear" value="0.82"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_O_s" scale="linear" value="(0.0000000*E_C+1.0000000*E_O+(0.0000000))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="E_O_t" scale="linear" value="(0.0000000*E_C+0.9986800*E_O+(0.4753200))"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="H_cov" scale="linear" value="(1/(1+sqrt(exp(-beta*(GibbsGas_H2gas-2*GibbsAds_H_t)*eV))))"/>
        <parameter adjustable="True" max="800.0" min="400.0" name="T" scale="linear" value="523.0"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="alpha" scale="linear" value="0.5"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH2_H_s" scale="linear" value="[56, 56, 233.3, 506.4, 578.9, 789.0, 904.0, 1326.7, 1822.0, 2925.1, 3029.3]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH2_H_t" scale="linear" value="[56, 56, 233.3, 506.4, 578.9, 789.0, 904.0, 1326.7, 1822.0, 2925.1, 3029.3]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH2_s" scale="linear" value="[56, 289.2, 405.2, 498.9, 597.8, 716.6, 1294.3, 2874.0, 3011.2]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH2_t" scale="linear" value="[89.2, 185.8, 297.1, 456.4, 513.0, 705.4, 1339.5, 2647.4, 2968.4]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH3_H_s" scale="linear" value="[56, 56, 90.9, 157.9, 338.3, 699.0, 812.7, 1248.0, 1370.9, 1418.0, 1609.6, 2916.4, 2997.4, 3076.0]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH3_H_t" scale="linear" value="[56, 56, 90.9, 157.9, 338.3, 699.0, 812.7, 1248.0, 1370.9, 1418.0, 1609.6, 2916.4, 2997.4, 3076.0]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH3_s" scale="linear" value="[56, 56, 56, 252.1, 353.1, 623.3, 1119.6, 1304.3, 1358.3, 2748.0, 2813.4, 3037.3]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH3_t" scale="linear" value="[56, 56, 56, 350.3, 645.4, 679.9, 1117.1, 1381.2, 1400.0, 2903.6, 3002.2, 3016.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH_H_f" scale="linear" value="[56, 332.3, 376.8, 547.7, 640.6, 894.1, 1541.2, 2975.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH_H_s" scale="linear" value="[56, 332.3, 376.8, 547.7, 640.6, 894.1, 1541.2, 2975.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH_H_t" scale="linear" value="[56, 332.3, 376.8, 547.7, 640.6, 894.1, 1541.2, 2975.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH__t" scale="linear" value="[542.7, 605.4, 637.7, 759.4, 3073.2]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH_f" scale="linear" value="[299.9, 347.1, 400.2, 692.2, 739.5, 2896.6]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH_s" scale="linear" value="[356.6, 401.3, 528.4, 610.7, 637.6, 2906.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CH_t" scale="linear" value="[367.9, 388.9, 568.5, 643.9, 696.1, 2958.0]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CO_s" scale="linear" value="[198.2, 269.2, 390.7, 418.4, 489.8, 2002.2]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_CO_t" scale="linear" value="[207.7, 267.2, 413.5, 424.4, 465.6, 1978.8]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_C_H_f" scale="linear" value="[331.4, 512.6, 534.5, 585.5, 1010.5]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_C_H_s" scale="linear" value="[331.4, 512.6, 534.5, 585.5, 1010.5]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_C_H_t" scale="linear" value="[331.4, 512.6, 534.5, 585.5, 1010.5]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_C_OH_f" scale="linear" value="[62.2, 268.2, 369.3, 408.9, 426.5, 748.8, 822.6, 3609.3]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_C__f" scale="linear" value="[296.6, 907.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_C_f" scale="linear" value="[317.9, 510.1, 521.2]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_C_s" scale="linear" value="[468.3, 503.6, 522.4]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_C_t" scale="linear" value="[463.0, 487.6, 513.7]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_H2O_O__s" scale="linear" value="[56, 120.8, 331.4, 439.9, 522.5, 542.4, 637.0, 758.6, 1315.4, 1512.6, 3709.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_H2O_O__t" scale="linear" value="[56, 120.8, 331.4, 439.9, 522.5, 542.4, 637.0, 758.6, 1315.4, 1512.6, 3709.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_H2O_O_s" scale="linear" value="[56, 120.8, 331.4, 439.9, 522.5, 542.4, 637.0, 758.6, 1315.4, 1512.6, 3709.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_H2O_O_t" scale="linear" value="[56, 120.8, 331.4, 439.9, 522.5, 542.4, 637.0, 758.6, 1315.4, 1512.6, 3709.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_H_OH_s" scale="linear" value="[56, 288.1, 331.0, 414.1, 533.0, 626.8, 1008.9, 3544.2]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_H_OH_t" scale="linear" value="[56, 288.1, 331.0, 414.1, 533.0, 626.8, 1008.9, 3544.2]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_H_t" scale="linear" value="[402.8, 572.6, 1013.7]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_OH_s" scale="linear" value="[56, 274.3, 382.8, 657.2, 763.5, 3634.2]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_OH_t" scale="linear" value="[176.7, 305.8, 408.4, 679.3, 712.7, 3602.1]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_O_H_s" scale="linear" value="[412.5, 428.8, 506.7, 550.3, 1069.4]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_O_H_t" scale="linear" value="[412.5, 428.8, 506.7, 550.3, 1069.4]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_O_s" scale="linear" value="[380.0, 444.0, 537.6]"/>
        <parameter adjustable="False" max="0.0" min="0.0" name="f_O_t" scale="linear" value="[418.8, 449.2, 517.3]"/>
        <parameter adjustable="True" max="100.0" min="1e-10" name="p_CH4gas" scale="linear" value="0.01"/>
        <parameter adjustable="True" max="100.0" min="1e-10" name="p_COgas" scale="linear" value="0.01"/>
        <parameter adjustable="True" max="100.0" min="1e-10" name="p_H2Ogas" scale="linear" value="0.01"/>
        <parameter adjustable="True" max="100.0" min="1e-10" name="p_H2gas" scale="linear" value="0.97"/>
    </parameter_list>
    <lattice cell_size="6.582 0.0 0.0 0.0 2.686 0.0 0.0 0.0 20.0" default_layer="Rh211" representation="[Atoms(symbols='Rh3',
          pbc=np.array([False, False, False]),
          cell=np.array(      ([6.582, 2.686, 20.0])),
          scaled_positions=np.array(      [[0.0, 0.0, 0.5388], [0.3334853, 0.5003723, 0.5], [0.6668186, 0.0, 0.4612]]),
),]" substrate_layer="Rh211">
        <layer color="#ffffff" name="Rh211">
            <site default_species="empty" pos="0.121 0.5 0.6" tags="" type="s"/>
            <site default_species="empty" pos="0.5 0.0 0.545" tags="" type="t"/>
            <site default_species="empty" pos="0.774 0.5 0.53" tags="" type="f"/>
        </layer>
    </lattice>
    <process_list>
        <process enabled="True" name="CH2_diff_s_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_s-GibbsAds_CH2_s)+E_CH2_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="CH2"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH2_diff_s_s_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_s-GibbsAds_CH2_s)+E_CH2_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH2_diff_s_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_t-GibbsAds_CH2_s)+E_CH2_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH2_diff_s_t_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_t-GibbsAds_CH2_s)+E_CH2_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH2_diff_t_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_s-GibbsAds_CH2_t)+E_CH2_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH2"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH2_diff_t_S_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_t-GibbsAds_CH2_t)+E_CH2_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="CH2"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH2_diff_t_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_s-GibbsAds_CH2_t)+E_CH2_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH2_diff_t_t_S" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH2_t-GibbsAds_CH2_t)+E_CH2_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH2_s_E_dis_f" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH_f+GibbsAds_H_t)-GibbsAds_CH2_s,0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="CH2"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="empty"/>
        </process>
        <process enabled="True" name="CH2_s_dis" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_s,GibbsAds_CH_s+GibbsAds_H_t)-GibbsAds_CH2_s,0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH2_t_N_dis_f" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH_f+GibbsAds_H_t)-GibbsAds_CH2_t,0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH2"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
        </process>
        <process enabled="True" name="CH2_t_dis" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_t,GibbsAds_CH_t+GibbsAds_H_t)-GibbsAds_CH2_t,0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH2_t_dis_f" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH_f+GibbsAds_H_t)-GibbsAds_CH2_t,0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="CH3_diff_s_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_s-GibbsAds_CH3_s)+E_CH3_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="CH3"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH3_diff_s_s_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_s-GibbsAds_CH3_s)+E_CH3_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH3_diff_s_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_t-GibbsAds_CH3_s)+E_CH3_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH3_diff_s_t_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_t-GibbsAds_CH3_s)+E_CH3_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH3_diff_t_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_s-GibbsAds_CH3_t)+E_CH3_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH3"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH3_diff_t_S_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_t-GibbsAds_CH3_t)+E_CH3_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="CH3"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH3_diff_t_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_s-GibbsAds_CH3_t)+E_CH3_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH3"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH3_diff_t_t_S" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH3_t-GibbsAds_CH3_t)+E_CH3_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH3"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH3_s_dis" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_s,GibbsAds_CH2_s+GibbsAds_H_t)-GibbsAds_CH3_s,0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH3_t_dis" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_t,GibbsAds_CH2_t+GibbsAds_H_t)-GibbsAds_CH3_t,0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH3"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="CH4_s_ads" rate_constant="(1-H_cov)/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_s,GibbsAds_CH3_s+GibbsAds_H_t)-GibbsGas_CH4gas,0)*eV)" tof_count="{'CH4_formation': -1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH4_t_ads" rate_constant="(1-H_cov)/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_t,GibbsAds_CH3_t+GibbsAds_H_t)-GibbsGas_CH4gas,0)*eV)" tof_count="{'CH4_formation': -1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH3"/>
        </process>
        <process enabled="True" name="CH_diff_f_S_f" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_f-GibbsAds_CH_f)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_f_f_S" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_f-GibbsAds_CH_f)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_f_s_E" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_f)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_f_t" rate_constant="1/(beta*h)*exp(-beta*max(max(GibbsAds_CH__t,GibbsAds_CH_t)-GibbsAds_CH_f,0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_f_t_N" rate_constant="1/(beta*h)*exp(-beta*max(max(GibbsAds_CH__t,GibbsAds_CH_t)-GibbsAds_CH_f,0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_s_E_f" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_f-GibbsAds_CH_s)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_s_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_s)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_s_s_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_s)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_s_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_t-GibbsAds_CH_s)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_s_t_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_t-GibbsAds_CH_s)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_t_N_f" rate_constant="1/(beta*h)*exp(-beta*max(max(GibbsAds_CH__t,GibbsAds_CH_f)-GibbsAds_CH_t,0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_t_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_t)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_t_S_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_t-GibbsAds_CH_t)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_t_f" rate_constant="1/(beta*h)*exp(-beta*max(max(GibbsAds_CH__t,GibbsAds_CH_f)-GibbsAds_CH_t,0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_t_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_s-GibbsAds_CH_t)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_diff_t_t_S" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CH_t-GibbsAds_CH_t)+E_CH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="CH"/>
        </process>
        <process enabled="True" name="CH_f_dis" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_f,GibbsAds_C_f+GibbsAds_H_t)-GibbsAds_CH_f,0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="CH_s_dis" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_s,GibbsAds_C_s+GibbsAds_H_t)-GibbsAds_CH_s,0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="CH_t_dis" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_t,GibbsAds_C_t+GibbsAds_H_t)-GibbsAds_CH_t,0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="CO_ads_s" rate_constant="p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_s)-GibbsGas_COgas)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_ads_t" rate_constant="p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_t)-GibbsGas_COgas)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_des_s" rate_constant="p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_s)-GibbsAds_CO_s)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="CO_des_t" rate_constant="p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(-beta*(max(GibbsGas_COgas,GibbsAds_CO_t)-GibbsAds_CO_t)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="CO_diff_s_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_s-GibbsAds_CO_s)+E_CO_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_diff_s_s_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_s-GibbsAds_CO_s)+E_CO_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_diff_s_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_t-GibbsAds_CO_s)+E_CO_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_diff_s_t_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_t-GibbsAds_CO_s)+E_CO_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_diff_t_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_s-GibbsAds_CO_t)+E_CO_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_diff_t_S_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_t-GibbsAds_CO_t)+E_CO_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_diff_t_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_s-GibbsAds_CO_t)+E_CO_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="CO_diff_t_t_S" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_CO_t-GibbsAds_CO_t)+E_CO_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="CO"/>
        </process>
        <process enabled="True" name="C_OH_s_react_t_NW" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_s+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="-1 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="-1 1 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="-1 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="-1 1 0" species="empty"/>
        </process>
        <process enabled="True" name="C_OH_s_react_t_W" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_s+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="-1 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="-1 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="-1 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="-1 0 0" species="empty"/>
        </process>
        <process enabled="True" name="C_OH_t_react_f" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_t+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="C_OH_t_react_f_S" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_CO_t+GibbsAds_H_t)-(GibbsAds_C_f+GibbsAds_OH_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
        </process>
        <process enabled="True" name="C_diff_f_S_f" rate_constant="1/(beta*h)*exp(-beta*max(max(GibbsAds_C__f,GibbsAds_C_f)-GibbsAds_C_f,0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_f_f_S" rate_constant="1/(beta*h)*exp(-beta*max(max(GibbsAds_C__f,GibbsAds_C_f)-GibbsAds_C_f,0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_f_s_E" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_f)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_f_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_f)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_f_t_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_f)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_s_E_f" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_f-GibbsAds_C_s)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_s_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_s)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_s_s_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_s)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_s_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_s)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_s_t_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_s)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_t_N_f" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_f-GibbsAds_C_t)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_t_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_t)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_t_S_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_t)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_t_f" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_f-GibbsAds_C_t)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_t_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_s-GibbsAds_C_t)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="C_diff_t_t_S" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_C_t-GibbsAds_C_t)+E_C_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="C"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="C"/>
        </process>
        <process enabled="True" name="H2O_O_s_react_s_N" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_s,2*GibbsAds_OH_s)-(GibbsAds_O_s+GibbsGas_H2Ogas),0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="OH"/>
        </process>
        <process enabled="True" name="H2O_O_s_react_s_S" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_s,2*GibbsAds_OH_s)-(GibbsAds_O_s+GibbsGas_H2Ogas),0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 -1 0" species="OH"/>
        </process>
        <process enabled="True" name="H2O_O_s_react_t" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__s,(GibbsAds_OH_s+GibbsAds_OH_t))-(GibbsAds_O_s+GibbsGas_H2Ogas),0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="H2O_O_s_react_t_N" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__s,(GibbsAds_OH_s+GibbsAds_OH_t))-(GibbsAds_O_s+GibbsGas_H2Ogas),0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="OH"/>
        </process>
        <process enabled="True" name="H2O_O_t_N_react_s" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__t,(GibbsAds_OH_t+GibbsAds_OH_s))-(GibbsAds_O_t+GibbsGas_H2Ogas),0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="H2O_O_t_react_s" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__t,(GibbsAds_OH_t+GibbsAds_OH_s))-(GibbsAds_O_t+GibbsGas_H2Ogas),0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="H2O_O_t_react_t_N" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_t,2*GibbsAds_OH_t)-(GibbsAds_O_t+GibbsGas_H2Ogas),0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="OH"/>
        </process>
        <process enabled="True" name="H2O_O_t_react_t_S" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_t,2*GibbsAds_OH_t)-(GibbsAds_O_t+GibbsGas_H2Ogas),0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="OH"/>
        </process>
        <process enabled="True" name="H2O_s_ads" rate_constant="(1-H_cov)*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_s,GibbsAds_OH_s+GibbsAds_H_t)-GibbsGas_H2Ogas,0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="H2O_t_ads" rate_constant="(1-H_cov)*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_t,GibbsAds_OH_t+GibbsAds_H_t)-GibbsGas_H2Ogas,0)*eV)" tof_count="{'H2O_formation': -1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="H_CH2_s_react" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_s,GibbsAds_CH3_s)-(GibbsAds_CH2_s+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
        </process>
        <process enabled="True" name="H_CH2_t_react" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH2_H_t,GibbsAds_CH3_t)-(GibbsAds_CH2_t+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH3"/>
        </process>
        <process enabled="True" name="H_CH3_s_react" rate_constant="H_cov/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_s,GibbsGas_CH4gas)-(GibbsAds_CH3_s+GibbsAds_H_t),0)*eV)" tof_count="{'CH4_formation': 1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH3"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="H_CH3_t_react" rate_constant="H_cov/(2*beta*h)*exp(-beta*max(max(GibbsAds_CH3_H_t,GibbsGas_CH4gas)-(GibbsAds_CH3_t+GibbsAds_H_t),0)*eV)" tof_count="{'CH4_formation': 1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH3"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="H_CH_f_react_s_E" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH2_s)-(GibbsAds_CH_f+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="1 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="H_CH_f_react_t" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH2_t)-(GibbsAds_CH_f+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="H_CH_f_react_t_N" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_f,GibbsAds_CH2_t)-(GibbsAds_CH_f+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="CH2"/>
        </process>
        <process enabled="True" name="H_CH_s_react" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_s,GibbsAds_CH2_s)-(GibbsAds_CH_s+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="H_CH_t_react" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_CH_H_t,GibbsAds_CH2_t)-(GibbsAds_CH_t+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH2"/>
        </process>
        <process enabled="True" name="H_CO_s_react_t_NW" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_s+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="-1 0 0" species="empty"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="-1 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="-1 0 0" species="C"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="-1 1 0" species="OH"/>
        </process>
        <process enabled="True" name="H_CO_s_react_t_W" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_s+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="-1 0 0" species="empty"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="-1 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="-1 0 0" species="C"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="-1 0 0" species="OH"/>
        </process>
        <process enabled="True" name="H_CO_t_react_f" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_t+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
        </process>
        <process enabled="True" name="H_CO_t_react_f_S" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_OH_f,GibbsAds_C_f+GibbsAds_OH_t)-(GibbsAds_CO_t+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CO"/>
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 -1 0" species="C"/>
        </process>
        <process enabled="True" name="H_C_f_react" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_f,GibbsAds_CH_f)-(GibbsAds_C_f+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="C"/>
            <action coord_layer="Rh211" coord_name="f" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="H_C_s_react" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_s,GibbsAds_CH_s)-(GibbsAds_C_s+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="C"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="H_C_t_react" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_C_H_t,GibbsAds_CH_t)-(GibbsAds_C_t+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="C"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="CH"/>
        </process>
        <process enabled="True" name="H_OH_s_react" rate_constant="H_cov*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_s,GibbsGas_H2Ogas)-(GibbsAds_OH_s+GibbsAds_H_t),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="H_OH_t_react" rate_constant="H_cov*4/(16*beta*h)*exp(-beta*max(max(GibbsAds_H_OH_t,GibbsGas_H2Ogas)-(GibbsAds_OH_t+GibbsAds_H_t),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="H_O_s_react" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_s,GibbsAds_OH_s)-(GibbsAds_O_s+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="H_O_t_react" rate_constant="H_cov/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_t,GibbsAds_OH_t)-(GibbsAds_O_t+GibbsAds_H_t),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="OH_OH_s_react_s_N" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_s,GibbsAds_O_s+GibbsGas_H2Ogas)-(2*GibbsAds_OH_s),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
        </process>
        <process enabled="True" name="OH_OH_s_react_s_S" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_s,GibbsAds_O_s+GibbsGas_H2Ogas)-(2*GibbsAds_OH_s),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 -1 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 -1 0" species="empty"/>
        </process>
        <process enabled="True" name="OH_OH_s_react_t" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__s,GibbsAds_O_s+GibbsGas_H2Ogas)-(GibbsAds_OH_s+GibbsAds_OH_t),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="OH_OH_s_react_t_N" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__s,GibbsAds_O_s+GibbsGas_H2Ogas)-(GibbsAds_OH_s+GibbsAds_OH_t),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
        </process>
        <process enabled="True" name="OH_OH_t_N_react_s" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__t,GibbsAds_O_t+GibbsGas_H2Ogas)-(GibbsAds_OH_t+GibbsAds_OH_s),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="O"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="OH_OH_t_react_s" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O__t,GibbsAds_O_t+GibbsGas_H2Ogas)-(GibbsAds_OH_t+GibbsAds_OH_s),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
        </process>
        <process enabled="True" name="OH_OH_t_react_t_N" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_t,GibbsAds_O_t+GibbsGas_H2Ogas)-(2*GibbsAds_OH_t),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
        </process>
        <process enabled="True" name="OH_OH_t_react_t_S" rate_constant="1/(16*beta*h)*exp(-beta*max(max(GibbsAds_H2O_O_t,GibbsAds_O_t+GibbsGas_H2Ogas)-(2*GibbsAds_OH_t),0)*eV)" tof_count="{'H2O_formation': 1}">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
        </process>
        <process enabled="True" name="OH_diff_s_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_s-GibbsAds_OH_s)+E_OH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="OH_diff_s_s_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_s-GibbsAds_OH_s)+E_OH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="OH"/>
        </process>
        <process enabled="True" name="OH_diff_s_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_t-GibbsAds_OH_s)+E_OH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="OH_diff_s_t_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_t-GibbsAds_OH_s)+E_OH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="OH"/>
        </process>
        <process enabled="True" name="OH_diff_t_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_s-GibbsAds_OH_t)+E_OH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="OH_diff_t_S_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_t-GibbsAds_OH_t)+E_OH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="OH_diff_t_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_s-GibbsAds_OH_t)+E_OH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
        </process>
        <process enabled="True" name="OH_diff_t_t_S" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_OH_t-GibbsAds_OH_t)+E_OH_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="OH"/>
        </process>
        <process enabled="True" name="OH_s_dis" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_s,GibbsAds_O_s+GibbsAds_H_t)-GibbsAds_OH_s,0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
        </process>
        <process enabled="True" name="OH_t_dis" rate_constant="(1-H_cov)/(beta*h)*exp(-beta*max(max(GibbsAds_O_H_t,GibbsAds_O_t+GibbsAds_H_t)-GibbsAds_OH_t,0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="OH"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
        </process>
        <process enabled="True" name="O_diff_s_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_s-GibbsAds_O_s)+E_O_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
        </process>
        <process enabled="True" name="O_diff_s_s_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_s-GibbsAds_O_s)+E_O_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 1 0" species="O"/>
        </process>
        <process enabled="True" name="O_diff_s_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_t-GibbsAds_O_s)+E_O_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
        </process>
        <process enabled="True" name="O_diff_s_t_N" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_t-GibbsAds_O_s)+E_O_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="O"/>
        </process>
        <process enabled="True" name="O_diff_t_N_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_s-GibbsAds_O_t)+E_O_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
        </process>
        <process enabled="True" name="O_diff_t_S_t" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_t-GibbsAds_O_t)+E_O_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
        </process>
        <process enabled="True" name="O_diff_t_s" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_s-GibbsAds_O_t)+E_O_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="s" coord_offset="0 0 0" species="O"/>
        </process>
        <process enabled="True" name="O_diff_t_t_S" rate_constant="1/(beta*h)*exp(-beta*max((alpha*(GibbsAds_O_t-GibbsAds_O_t)+E_O_diff),0)*eV)">
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="O"/>
            <condition coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 0 0" species="empty"/>
            <action coord_layer="Rh211" coord_name="t" coord_offset="0 -1 0" species="O"/>
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
