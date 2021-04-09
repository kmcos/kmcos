#   Specify various input parameters (initial temperature, run time, etc.)
T_initial = 200 #K
T_final   = 700 #K
T_ramp    = 3   #K/s
sim_size  = 50  #Number of times to repeat the unit cell in x, y directions
max_time_step = 1e-18  #Maximum time step allowed, in s
#   Random seed for simulation -- can generate with 'cat /dev/urandom | od -N 4 -t d4'
random_seed = 242797216
