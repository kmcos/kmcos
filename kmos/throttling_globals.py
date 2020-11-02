from kmc_settings import simulation_size

# Be sure to use floats and not integers in general, unless integers make sense
# (e.g., process indices).

################################################################################
#                                                                              #
#                  PART I: USER-ADJUSTABLE/DEFINED PARAMETERS                  #
#                                                                              #
################################################################################

# Number of unit cells in the simulation box
Nsites = simulation_size**2

# Should we print detailed information about the throttling?
print_throttling_info = True

# This is the currently chosen ranking scheme. We have this variable to permit
# flexibly changing the ranking scheme on-the-fly if desired. Currently the only
# type supported is 'paired', but other types may be implemented in the future.
current_ranking_scheme = 'paired'

# A regular expression for extracting only the relevant processes from a list of
# processes created by the snapshots module. Note that the regex r'.*' will
# match everything, thereby allowing one to use the raw TOF lists directly.
#regex = r'.*' # uncomment to turn off regular expression matching
regex = r'^[FR]\d+p\d+$' # comment out if turning off regex matching

# Factor controlling whether reactions are considered to be quasi-equilibrated
# or not. Current default is 0.1.
qe_tolerance = 0.1

# Flag controlling the compression progression employed. The tag 'auto' means to
# use a default progression up to a requested compression range. Otherwise, the
# scheme should be specfied as a list of 2-tuples, with the first (second)
# element of each tuple specifying the fast (slow) compression amount. The
# Python object None can be used to specify no compression is allowed.
# Examples:
#   compression_scheme_flag = 'auto' # default progression
#   compression_scheme_flag = None # No compression, sets compression_schemes = [(0, 0)]
#   compression_scheme_flag = 'manual' # Manual setting of compression schemes
#
# If 'manual' is selected, then set the compression_schemes variable as a list
# of 2-tuples with the fast and slow scaling levels, as in:
#   compression_schemes = [(1, 0)] # Nsites spacing between all fast processes
#   compression_schemes = [(1, 0), (0, 1)] # Nsites spacing between all fast
#     processes followed by Nsites spacing between all slow processes.
# The variable compression_schemes will be overwritten if auto or none is
# selected in the flag.
compression_scheme_flag = 'auto'
compression_schemes = None

# Maximum throttling levels for fast and slow scales. The maximum allowed value
# for this is 3 for each one. If this is set to zero, then no throttling will be
# allowed for that scale.
max_fast_scale = 3
max_slow_scale = 3

# Whether to throttle slow and fast compression ranges separately ('split') or
# together ('full'); 'split' should usually be used.
EF_range_flag = 'split'

# Requested compression ranges (ratio of fastest rate to slowest rate). These
# are adjusted below depending on the value of EF_range_flag. Any ranges not
# associated with the specified EF_range_flag are set to None.
EF_range_fast_requested = 1e2     # For fast processes only ('split')
EF_range_slow_requested = 1e20    # For slow processes only ('split')
EF_range_full_requested = 1e6     # For both fast and slow together ('full')

# Any processes not expected to occur more than Nsites times within this cutoff
# time during the simulations will be excluded from throttling as irrelevant.
max_time = 10. * 3600 #This is the maximum relevant simulation time (MRST in the original SQERTSS paper)

# This is the maximum relevant simulation time that we are concerned with
# simulating. This is a hard limit -- if we reach it, the throttling loop will
# stop.
cutoff_time = 100.0

# The characteristic_EF is the primary benchmark for FFPs. In a system with FFPs, the throttling
# algorithm will step down the slowest FFP until it approaches this value. The value
# is user-adjustable and based on the desired timescale. The floor should be
# approximately the rate of the FRP times Nsites. We leave this in the
# user-adjustable section as this is just a guideline and can be changed as
# desired. If the user wants to change this value, it should be done in the
# runfile.
characteristic_EF = 0.2  # Characteristic transition rate
FFP_floor = characteristic_EF * Nsites
#it is good to use an FFP_roof: the compression will be required to satisfy *both* the roof *and* the EF_range requirementes.
FFP_roof = None 
#By default, the FRP_Buffer between FFP_floor and the FRP is Nsites.
FRP_Buffer = Nsites 

# Total number of KMC steps to execute per snapshot. This should be at least
#   throttling_sps = EF_range_fast_requested * Nsites * n_characteristic_events_target
# for split range and
#   throttling_sps = EF_range_full_requested
# for full range. If the user wants to change this value, it should be done
# here or in the runfile. The variable n_characteristic_events_target is the
# number of times that the characteristic event (e.g., FRP) should occur during
# the snapshot.
n_characteristic_events_target = 10
if EF_range_flag == 'split':
    throttling_sps = int(EF_range_fast_requested * Nsites *
        n_characteristic_events_target)
else:
    throttling_sps = int(EF_range_full_requested)

# Total KMC time to execute per snapshot. A value of None will cause the
# algorithm to use a fixed number of steps (this should be the typical case).
throttling_tps = None

# Default FFP step down divisor. A smaller divisor will step down less, and any
# value less than one will actually increase the FFP rate (*so don't use a value
# less than 1*). This is used in conjunction with the number of KMC steps and
# the number of sites to automatically choose a reasonable down step divisor. A
# value of 10 is very safe (conservative). The guideline of
# throttling_sps/Nsites is more aggressive but still reasonable, at least in the
# case where fixed step snapshots are employed (time step snapshots are still a
# work in progress, and the default should be used).
default_FFP_step_down = 10.0

# Do we want to use guidelines for setting various quantities?
use_guideline_FFP_step_down = True  # FFP step down
use_guideline_FFP_floor = False  # Floor level #this will override what is set for FFP_floor
use_guideline_sps = False    # SPS size #this will override what is set for throttling_sps

# These are the staggering factors controlling the compression of scales. Each
# factor is used at the corresponding scale (1, 2, or 3). These are all
# reasonable values and are user-adjustable, but any adjustments should be made
# with care! Note that we also have Nsites for the initial entry. This entry is
# only used during FFP step down, and it ensures that the sFFP will not get
# closer than Nsites to an FQP if it exists.
staggering_factors = [Nsites, Nsites, 10., 1.1]

# Total number of steps to take between unthrottling of slow reactions
loop_base = 10 #This is "M" in the original SQERTSS paper.

# If the current snapshot counter is an integer multiple of loop_base, should we
# unthrottle all processes (not just the slow ones) by resetting the local
# snapshot counter to zero?
reset_snapshot_counter = True

# Throttle forward/reverse process pairs together?
throttle_process_pairs = True

# Should we enforce steady state throttling where slow processes are never
# throttled?
steady_state_throttling = False

# General numerical tolerance to allow some slack in determining equality of two
# close floating point numbers. If a calculated quantity is larger than the
# expected amount or requested criterion (e.g., in the EF_range compression
# ratios) by less than this amount, it is treated as still meeting the test. We
# have this to permit some (small) discrepancies to pass that arise from finite
# numerical precision. This tolerance is relative to the requested/expected
# value. It should be fairly small.
floating_point_rel_tol = 1e-4

# Should we regularize rate constants that are too large?
regularization = False

################################################################################
#                                                                              #
#                  PART II: AUTOMATICALLY GENERATED VARIABLES                  #
#                           !! DO NOT EDIT THESE !!                            #
#                                                                              #
################################################################################

# This is a list of all elementary processes in the model. It is a subset of the
# TOF header array in snapshots_globals, but is constructed in the runfile to
# eliminate a dependency.
proc_names = []

# This is a list of the observed event frequencies from the current snapshot
# corresponding to the process names list. It is also created in the runfile.
oEF_TOF_list_next = []

# This is a list of the observed event frequencies from the last snapshot.
oEF_TOF_list = []

# This is a list of paired indices for the forward and reverse processes
# corresponding to each reaction number. This dictionary is populated in
# uEF_back_calculate by a call to a helper function.
EF_indices_dict = {}

# The following list-of-lists is the raw, unsorted process rate data. It can be
# used to generate the sublists for the ranked dictionary variables. Each
# sublist has seven elements: reaction number (e.g., 15p0), forward rate,
# reverse rate, ratio of forward to reverse rate, maximum of forward and reverse
# rate, the direction of the maximum rate ('F' or 'R' for forward/reverse), and
# an index indicating the original order before any ranking is performed.
uEF_list = []

# This list is similar to uEF_list, but it has the projected throttled rates.
ptEF_list = []

# These variables contain the current index values for the benchmark and
# slowest rate limiting processes. These indices can be used to extract various
# quantities from the ranked_EF lists.
BP_index = 0
sSP_index = 0

# Dictionaries with the names and types of the current benchmark process
BP_name = None
BP_type = None

# This is a list collecting the processes sorted according to various
# schemes. The format for each scheme is identical. Each scheme has a single
# list with an arbitrary number of related three element sublists. Each sublist
# collects the process number (e.g., F15p0), the event frequency, and a 2-tuple
# with (1) the index to the reaction in uEF_list and (2) the index to the
# forward/reverse process in the process list in uEF_list. The first three
# element sublist is always the process that is deemed most important for the
# grouping. For example, for the paired rank scheme, it is the process with the
# maximum rate.
ranked_uEF_list = []

# These lists contain the ascending FFP and descending SP lists for the current
# ranking scheme. Each of the sublists has the reaction number, associated rate,
# direction of maximum rate, and a 2-tuple with indices to its location in the
# master uEF_list structure and its location in the ranked_uEF_list. The rates
# in these lists are unthrottled.
ascend_FFP_list = []
descend_SP_list = []

# The following variables are all used in the throttling functions.

# These are the aggregate and incremental throttling factors lists. They are
# used to store the total throttling over all snapshots (aggregate factors) and
# new throttling due to this snapshot (incremental factors). The aggregate
# factors are used to back-calculate unthrottled rates that are used to rank
# processes for determining the new incremental throttling factors. These lists
# have an exact correspondence to the ascend_FFP and descend_SP lists.
#
# The structure of these lists is as follows:
#   First index: [0] - list of FFPs (ascending order), [1] - list of SPs
#       (descending order)
#   Second index (for each FFP/SP): Selects sublist for individual processes
#   Third index: [0] - reaction number, [1] - throttling factor,
#       [2] - reaction direction, [3] - process name (F/R + reaction number),
#       [4] - 2-tuple with (1) index to reaction in uEF_list and (2) index to
#       corresponding entry in ranked_uEF_list.
aggregate_throttling_factors = [[], []]
incremental_throttling_factors = [[], []]

# These lists contain the names of the never throttled and previously throttled
# negligible processes.
unthrottled_negligible_process_names = [] # never throttled
throttled_negligible_process_names = [] # previously throttled

# This list contains the names of the fast and slow processes that have been
# throttled. It is used to undo the throttling for only the throttled processes
# during the unthrottling step. This list is also not sorted in any particular
# order.
#
# The structure of this list is as follows:
#   First index: [0] - list of FFPs, [1] - list of SPs
#   Second index: list of process names
throttled_process_names = [[],[]]

# Amount by which to throttle the slowest quasi-equilibrated step in a system
# with only quasi-equilibrated steps (i.e., only FFPs). A value of 10 is very
# safe (conservative); a value of throttling_sps/Nsites is more agressive but
# still reasonable. This approximation is only valid for fixed-step snapshot
# execution and needs to be revisited for time-step snapshot execution. Here we
# choose 10 as the minimum amount allowed, but this is user adjustable. A value
# closer to 1 means less down throttling, and a value less than 1 will actually
# speed up the slowest FFP. (*So don't go below 1!*)
if use_guideline_FFP_step_down:
    FFP_step_down = max(float(throttling_sps)/Nsites, default_FFP_step_down)
else:
    FFP_step_down = default_FFP_step_down

# Variable containing the kind of FFP step down behavior
FFP_step_down_type = None

# List containing the back-calculated unthrottled event frequencies (i.e., the
# rates at which each reaction would have occurred had throttling not been
# applied). This is important for periodically recalibrating the throttling.
# The structure is a simple list with the same order as sg.atoms.tof_data.
uEF_TOF_list = []

# Current aggregate throttling factors for all processes ever throttled. The
# format is a simple dictionary where keys are process names (e.g., F15p0) and
# the values are the current aggregate throttling factors.
aggregate_throttling_factors_dict = {}

# Aggregate throttling factors for the last snapshot
aggregate_throttling_factors_dict_old = {}

# The format (a simple dictionary) is the same as for
# aggregate_throttling_factors_dict, but it contains the incremental throttling
# factors for this snapshot only. It is currently only used for debugging
# purposes.
incremental_throttling_factors_dict = {}

# Variables containing the current kind of compression applied at each level
fast_throttling_scale = 0
slow_throttling_scale = 0

# Adjustments to the requested EF range values
if EF_range_flag == 'full':
    EF_range_fast_requested = None
    EF_range_slow_requested = None
elif EF_range_flag == 'split':
    EF_range_full_requested = None
else:
    print('WARNING: Invalid EF_range_flag detected')
    EF_range_fast_requested = None
    EF_range_slow_requested = None
    EF_range_full_requested = None

# Variables containing the actual compression ratios
EF_range_fast_actual = None
EF_range_slow_actual = None
EF_range_full_actual = None

# Round-off error of the machine; this value is true for CPython on standard x86
# hardware for IEEE double precision floating point values (the standard float
# in Python on all or nearly all platforms is IEEE double precision). This is
# the smallest quantity that when added to 1 results in a sum that is
# distinguishible from 1.
machine_epsilon = 2**-52

# Number of resolvable decimal digits at the cutoff time
resolvable_digits = 2

# Maximum rate constant allowed. Any processes with larger rate constants will
# be capped at this value. This quantity should be chosen with care. If any rate
# constant is too large, the amount of time resolvable by the KMC simulation
# will drop below numerical machine precision and calculated TOF values will
# become undefined. The default value here is sufficient to permit ~3 decimal
# digits of resolution in the KMC time increment at the end of the simulation.
max_rate_constant = 1./(max_time / Nsites * machine_epsilon * 10**resolvable_digits)

# Current snapshot number
current_snapshot = 0

# Original values of pre-exponentials
preexp_dict_original = None # Current snapshot
preexp_dict_original_reg_old = None # Regularized pre-exponentials from the last snapshot
modified_preexp_set = set() # Set of all processes with pre-exponentials that have been modified

# NSP threshold -- below this processes will be NSPs
NSP_EF_threshold = float(Nsites)/max_time

# Flag whether we have exceeded the cutoff time
cutoff_time_exceeded = False

# List of variables to save. *DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOU ARE
# DOING!*
__var_list__ = ['print_throttling_info', 'aggregate_throttling_factors',
    'aggregate_throttling_factors_dict',
    'aggregate_throttling_factors_dict_old', 'ascend_FFP_list', 'BP_index',
    'BP_name', 'BP_type', 'staggering_factors', 'compression_schemes',
    'compression_scheme_flag', 'current_ranking_scheme', 'current_snapshot',
    'cutoff_time', 'default_FFP_step_down', 'descend_SP_list', 'proc_names',
    'EF_indices_dict', 'oEF_TOF_list_next', 'oEF_TOF_list', 'uEF_list',
    'ptEF_list', 'EF_range_fast_requested', 'EF_range_fast_actual', 'EF_range_flag',
    'EF_range_full_requested', 'EF_range_full_actual', 'EF_range_slow_requested',
    'EF_range_slow_actual', 'fast_throttling_scale', 'FFP_floor',
    'FFP_step_down', 'FFP_step_down_type', 'incremental_throttling_factors',
    'incremental_throttling_factors_dict', 'loop_base', 'machine_epsilon',
    'max_rate_constant', 'max_time', 'Nsites', 'preexp_dict_original',
    'preexp_dict_original_reg_old', 'qe_tolerance', 'ranked_uEF_list',
    'resolvable_digits', 'slow_throttling_scale', 'sSP_index',
    'steady_state_throttling', 'reset_snapshot_counter',
    'throttled_negligible_process_names', 'throttled_process_names',
    'throttle_process_pairs', 'throttling_sps', 'uEF_TOF_list',
    'unthrottled_negligible_process_names', 'use_guideline_FFP_step_down',
    'floating_point_rel_tol', 'modified_preexp_set', 'regularization']
