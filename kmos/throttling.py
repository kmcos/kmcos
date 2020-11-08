#Version 8.2
# This module has functions related to ranking, sorting, and calculating the
# throttling factors required to achieve a desired scale compression. It relies
# on data stored in throttling_globals.

try:
    import kmcos.snapshots_globals as sg
    from kmcos.snapshots import do_snapshots
except:
    import snapshots_globals as sg
    from snapshots import do_snapshots
try:
    import kmcos.throttling_globals as tg
except:
    import throttling_globals as tg
import re   # Regular Expressions module
from copy import deepcopy
from timeit import default_timer as timer

#These veriables have been renamed so are being reassigned for backwards compatibility.
if hasattr(tg, 'EF_range_fast'):
    tg.EF_range_fast_requested = tg.EF_range_fast
if hasattr(tg, 'EF_range_slow'):
    tg.EF_range_slow_requested = tg.EF_range_slow
if hasattr(tg, 'EF_range_full'):
    tg.EF_range_full_requested = tg.EF_range_full

# TODO: Because rare configuration slow processes do not increase when the rate
# constants for them are increased, this could potentially inhibit compression
# in certain cases. Ashi does not yet have ideas on how to achieve increased
# compression in these cases. However, the good news is that because we redo the
# rankings with predicted unthrottled event frequencies every snapshot, the
# system dynamics are probably not distorted by this issue.

################################################################################
#                                                                              #
#        PART I: FUNCTIONS RELATED TO SORTING AND RANKING THE PROCESSES        #
#                                                                              #
#   This part has the following functions:                                     #
#                                                                              #
#       1.  back_calculate_uEF                                                 #
#               Estimates the unthrottled rates based on the throttled rates   #
#               and the aggregate throttling factors                           #
#       2.  find_process_pairs                                                 #
#               Finds indices for forward/reverse process pairs in the TOF     #
#               header array and rate data                                     #
#       3.  get_process_info                                                   #
#               Constructs an unranked master list with the forward/reverse    #
#               rate data                                                      #
#       4.  create_ranked_EF_list                                              #
#               Creates groups of processes and then ranks each process group  #
#               by the key rate in that group                                  #
#       5.  create_FFP_SP_lists                                                #
#               Identifies which process groups are fast and slow and records  #
#               the breakpoints for these groups in the ranked list            #
#       6.  rank_EFs_driver                                                    #
#               Driver routine for the sorting/ranking step                    #
#                                                                              #
################################################################################

# This function back calculates the unthrottled event frequency from a throttled
# snapshot.
# Algorithm step 1.a.
def back_calculate_uEF():

    # Initialize the list and make sure they are all floating point values to
    # avoid integer division later.
    tg.uEF_TOF_list = deepcopy(tg.oEF_TOF_list)
    for i in range(len(tg.uEF_TOF_list)):
        tg.uEF_TOF_list[i] = float(tg.uEF_TOF_list[i])

    # Get the old throttling factors
    unthrottling_factors_dict = tg.aggregate_throttling_factors_dict_old

    # Create a dictionary with the reaction names and the indices with the
    # EF_header_array. The resulting dictionary is stored in tg.EF_indices_dict.
    find_process_pairs()

    # Iterate across the reactions in the dictionary and calculate uEF values
    # for each associated process
    for rxn_number in tg.EF_indices_dict:
        indices = tg.EF_indices_dict[rxn_number]
        for i in range(len(indices)):
            proc_index = indices[i]
            if proc_index is not None:
                if i == 0: # Forward
                    proc_name = 'F' + rxn_number
                elif i == 1: # Reverse
                    proc_name = 'R' + rxn_number
                else:
                    pass # Should not happen
                if proc_name in unthrottling_factors_dict:
                    unthrottling_factor = unthrottling_factors_dict[proc_name]
                    tg.uEF_TOF_list[proc_index] /= unthrottling_factor

    # return tg.uEF_TOF_list is implied because python is accessing it as
    # a global variable and changing it.

# This function creates a list of reaction names from the TOF header array
# matched to their forward and reverse process indices. It specifically looks
# for matches to the regular expression specified in throttling_globals.
def find_process_pairs():

    # Make a local copy of the header array augmented with list indices. We know
    # that the source array does not have any entries not corresponding to
    # actual processes, as these have already been filtered out.
    header_array_local = [[tg.proc_names[i], i] for i in
        range(len(tg.proc_names))]

    # Loop over the augmented header array and construct a dictionary with the
    # corresponding forward and reverse processes.
    tg.EF_indices_dict = {}
    for process in header_array_local:
        process_number = process[0]
        process_direction = process_number[0]
        reaction_number = process_number[1:]
        header_index = process[1]
        if reaction_number not in tg.EF_indices_dict:
            # This is a new reaction; we need to add it to the list of
            # processes.
            if process_direction == 'F':
                tg.EF_indices_dict[reaction_number] = [header_index, None]
            elif process_direction == 'R':
                tg.EF_indices_dict[reaction_number] = [None, header_index]
            else:
                pass # Should not happen
        else:
            # This is an existing reaction, so we just need to update the entry.
            if process_direction == 'F':
                tg.EF_indices_dict[reaction_number][0] = header_index
            elif process_direction == 'R':
                tg.EF_indices_dict[reaction_number][1] = header_index
            else:
                pass # Should not happen

# This function takes the constructed list of paired reaction indices and
# creates a list with all of the process statistics (reaction name, forward and
# reverse rates, the ratio of the rates, the maximum of the forward/reverse
# rates, and its order in the list before any ranking occurs). It also
# identifies which processes have negligible rates and classifies them as either
# unthrottled (never throttled) or previously throttled.
# Algorithm step 1.b
def get_process_info():

    # Temporary list of [rxn_number, EF_F, EF_R, EF_ratio, EF_max, max_dir] for
    # constructing the complete list one sublist at a time.
    tg.uEF_list = []
    tg.throttled_negligible_process_names = []
    tg.unthrottled_negligible_process_names = []

    i = 0
    for rxn_number in tg.EF_indices_dict: # note that there is one element for each process here.

        EF_sublist = []

        # Get the event frequencies, if the corresponding process exists (note
        # that we should always have a pair of processes!)
        if tg.EF_indices_dict[rxn_number][0] is not None:
            EF_F = tg.uEF_TOF_list[tg.EF_indices_dict[rxn_number][0]] # forward
        else:
            EF_F = None
        if tg.EF_indices_dict[rxn_number][1] is not None:
            EF_R = tg.uEF_TOF_list[tg.EF_indices_dict[rxn_number][1]] # reverse
        else:
            EF_R = None

        # Check the forward and reverse EFs against the minimum non-negligible
        # EF. If we are using paired throttling, we set the EFs to None only
        # if both are negligible. If we are using unpaired throttling, then the
        # processes EFs are set to None individually.
        # Algorithm step 1.b.i
        if tg.throttle_process_pairs:
            if EF_F < tg.NSP_EF_threshold and EF_R < tg.NSP_EF_threshold:
                EF_F = None
                EF_R = None
                for rxn_dir in ['F', 'R']:
                    proc_name = rxn_dir + rxn_number
                    if proc_name in tg.aggregate_throttling_factors_dict:
                        tg.throttled_negligible_process_names.append(proc_name)
                    else:
                        tg.unthrottled_negligible_process_names.append(proc_name)
        else:
            if EF_F < tg.NSP_EF_threshold:
                EF_F = None
                proc_name = 'F' + rxn_number
                if proc_name in tg.aggregate_throttling_factors_dict:
                    tg.throttled_negligible_process_names.append(proc_name)
                else:
                    tg.unthrottled_negligible_process_names.append(proc_name)
            if EF_R < tg.NSP_EF_threshold:
                EF_R = None
                proc_name = 'R' + rxn_number
                if proc_name in tg.aggregate_throttling_factors_dict:
                    tg.throttled_negligible_process_names.append(proc_name)
                else:
                    tg.unthrottled_negligible_process_names.append(proc_name)

        # This may not be mathematically correct, but it will prevent problems
        # later on to simply consider this ratio as zero if we divide by zero.
        # Think of it as 0 ratio. We also include cases where one direction or
        # the other is not defined. We should never have a case where neither
        # direction is defined, as this is filtered out when we constructed
        # tg.EF_indices_dict.
        if EF_R == 0 or EF_F is None or EF_R is None:
            EF_ratio = 0
        else:
            EF_ratio = EF_F/EF_R

        # Now we determine which direction has the maximum EF
        if EF_F is not None and EF_R is not None:
            if EF_F < EF_R:
                EF_max = EF_R
                max_dir = 'R'
            else:
                EF_max = EF_F
                max_dir = 'F'
        elif EF_F is None:
            EF_max = EF_R
            max_dir = 'R'
        elif EF_R is None:
            EF_max = EF_F
            max_dir = 'F'
        else: # Both are negligible
            EF_max = 0
            max_dir = None # Flag that this is a negligible reaction in both directions

        # Add all of this to the list
        tg.uEF_list.append([rxn_number, EF_F, EF_R, EF_ratio, EF_max, max_dir, i])
        i += 1

# This function creates a ranked_uEF_list variable that is ranked according to
# the specified ranking scheme. It reads the global uEF_list variable but should
# not alter it.
def create_ranked_EF_list():

    # Extract the information from EF_sorted_list and assign it to local lists.
    tg.ranked_uEF_list = []
    for i in range(len(tg.uEF_list)):

        # Reaction number
        rxn_number = tg.uEF_list[i][0]

        # Forward EF data
        fwd_EF = tg.uEF_list[i][1]

        # Reverse EF data
        rev_EF = tg.uEF_list[i][2]

        # Unsorted index
        idx = tg.uEF_list[i][6]

        # Add to temporary master list
        if tg.current_ranking_scheme == 'paired':
            if fwd_EF is not None and rev_EF is not None:
                if fwd_EF >= rev_EF:
                    tg.ranked_uEF_list.append([
                        ['F' + rxn_number, fwd_EF, (idx, 1)],
                        ['R' + rxn_number, rev_EF, (idx, 2)]])
                else:
                    tg.ranked_uEF_list.append([
                        ['R' + rxn_number, rev_EF, (idx, 2)],
                        ['F' + rxn_number, fwd_EF, (idx, 1)]])
            elif fwd_EF is not None:
                tg.ranked_uEF_list.append([['F' + rxn_number, fwd_EF, (idx, 1)]])
            elif rev_EF is not None:
                tg.ranked_uEF_list.append([['R' + rxn_number, rev_EF, (idx, 2)]])
            else:
                pass # Completely negligible reaction. Do not add it to the list.
        elif tg.current_ranking_scheme == 'unpaired':
            if fwd_EF is not None:
                tg.ranked_uEF_list.append([['F' + rxn_number, fwd_EF, (idx, 1)]])
            else:
                pass # Completely negligible reaction. Do not add it to the list.
            if rev_EF is not None:
                tg.ranked_uEF_list.append([['R' + rxn_number, rev_EF, (idx, 2)]])
            else:
                pass # Completely negligible reaction. Do not add it to the list.
        else:
            pass # Should not happen, but can add logic for additional schemes here

    # Sort the ranked_uEF_list list according to the EF and the process name in
    # the first three element sublist
    tg.ranked_uEF_list.sort(key=lambda x: (x[0][1], x[0][0]), reverse=True)

# This function will divide the ranked processes into FFPs and SPs. By
# definition, the BP is the fastest non-quasi-equilibrated reaction for systems
# with either both fast and slow reactions or slow reactions only and the
# slowest fast equilibrated reaction with a rate above the floor for systems
# with fast processes only. This function will handle both paired and unpaired
# ranking schemes transparently.
# Algorithm step 1.c -- process classification
def create_FFP_SP_lists():

    # We need to consider each of the combinations of fast, slow, and negligible
    # processes (FFP, SP, and NP) and make sure the code handles all of them.
    # These combinations (with X denoting the presence of that process type
    # and - denoting the absence of that process type) are:
    #
    #   Case FFP  SP  NP
    #   ================
    #    1    X   X   X
    #    2    X   X   -
    #    3    X   -   X
    #    4    X   -   -
    #    5    -   X   X
    #    6    -   X   -
    #    7    -   -   X
    #    8    -   -   -
    #
    # The structure of ranked_uEF_list should imply that no negligible processes
    # are present, but we include logic for them just to be sure. We also note
    # that any fast quasi-equilibrated reactions with EFs below the value
    # FFP_floor are not throttled. We refer to these internally as fast
    # quasi-equilibrated processes (FQPs) to distinguish them from the truly
    # frivolous fast processes that are throttled.

    # Initialize sorted lists of fast/slow processes
    tg.ascend_FFP_list = []
    tg.descend_SP_list = []

    # Keep track of the number of FFPs so we can check later if any of them are
    # FQPs.
    FFP_ranks = 0

    # Initialize rank breakpoint markers. These markers break the list into
    # three segments: fast qe processes (FFPs), slow rate limiting processes
    # (SPs), and slow negligible processes (NPs). BP_index is typically the
    # fastest non-qe process (the break between the first two segments) unless
    # there are no slow processes (then it is the slowest FFP with an EF higher
    # than FFP_floor), and sSP_index is the slowest rate limiting process (the
    # break between the last two segments). Our initial guesses for the BP and
    # sSP indices are that we have no FFPs and/or no NPs. We then update these
    # indices as we scan the list of processes.
    tg.BP_index = 0 # Cases 5-8 implied (no FFPs)
    tg.BP_type = None
    tg.sSP_index = len(tg.ranked_uEF_list) - 1 # Cases 2, 4, 6, 8 implied (no NPs)
    no_SP = False # Flag for whether there are no slow processes

    # Check for Case 8 (trivial case, no reactions in mechanism, so length of
    # mechanism is zero)
    if len(tg.ranked_uEF_list) == 0:
        tg.BP_type = 'No non-negligible processes'
        print('WARNING: There are no process event frequencies in the rankings. The simulation will likely crash soon. Be sure that tg.max_time is not set too low.')

        # Go ahead and return with the global variables as they are
        return

    # Find the BP index starting at the top of the list and going down. Any
    # fast qe reactions are added in descending order to the list of FFPs.
    # We will then reverse the order after finding the BP.
    for i in range(0, tg.sSP_index + 1):

        # Get reaction/process data
        master_EF_list_idx = tg.ranked_uEF_list[i][0][2][0]
        EF_ratio_i = tg.uEF_list[master_EF_list_idx][3]
        EF_max = tg.uEF_list[master_EF_list_idx][4] # Max of fwd/rev uEFs
        proc_name = tg.ranked_uEF_list[i][0][0]
        rxn_number = proc_name[1:]

        # Check for non-quasi-equilibration with non-negligible EFs
        if EF_max >= tg.NSP_EF_threshold: # EF_max is zero for negligible processes
            # Cases 1-6
            if abs(1 - EF_ratio_i) > tg.qe_tolerance:
                # Algorithm step 1.c.i
                # Cases 1, 2, 5, 6 (will not skip SPs)
                # Cases 5, 6 should terminate with i = 0
                # Cases 1, 2 should terminate with i > 0
                tg.BP_index = i   # This is the BP
                tg.BP_type = 'FRP'
                break # Bail out at the first non-negligible non-qe reaction
            else:   # This is an FFP; add it to the list.
                # Cases 1-4
                # Case 4 handled by normal loop termination (all processes
                # scanned)
                # Algorithm step 1.c.ii
                FFP_ranks += 1
                if proc_name[0] == 'F':   # Forward reaction
                    tg.ascend_FFP_list.append([rxn_number, EF_max, 1,
                        (master_EF_list_idx, i)])
                elif proc_name[0] == 'R':   # Reverse reaction
                    tg.ascend_FFP_list.append([rxn_number, EF_max, 2,
                        (master_EF_list_idx, i)])
                else:
                    pass # Should not happen

                # We have added this process to the list of FFPs. We also need
                # to check if the maximum EF is above the floor. If it is, it
                # may be the BP, so we update the current guess for the BP.
                if EF_max >= tg.FFP_floor:
                    tg.BP_index = i
                    tg.BP_type = 'FFP'
        else: # Algorithm step 1.c.iv
            # Cases 3, 7 (will skip SPs)
            # We have a process with negligible EFs. Any remaining processes
            # will also have negligible EFs, so we can skip the slow
            # processes. The BP for Case 3 is set above if EF_max is larger than
            # FFP_floor and is initialized to 0, which is the correct value for
            # Case 7. By definition, the sSP is the same as the BP.
            no_SP = True
            tg.sSP_index = tg.BP_index
            break

    # Reverse the list of FFPs to be in proper ascending order. This sorting
    # will break ties by putting forward reactions first. The first sorting key
    # (x[1]) is the rate associated with the process group. For paired ranking,
    # this rate is the maximum of the forward and reverse rates. The second
    # sorting key is just the process name, so forward processes will be ranked
    # before reverse processes.
    tg.ascend_FFP_list.sort(key=lambda x: (x[1], x[2]))

    # Need to check for Case 4 (only FFPs/FQPs). The total number of FFPs/FQPs
    # is identical to the number of reactions in the list. There are no SPs and
    # the slowest relevant process is the same as the benchmark process,
    # regardless of whether there are FQPs or not. If there are only FQPs, then
    # the 'benchmark' process is the slowest of the processes, and a special
    # note is made of this. Note that FQPs are never throttled.
    if FFP_ranks == len(tg.ranked_uEF_list):
        # Algorithm step 1.c.i
        # Case 4
        no_SP = True
        if tg.BP_type is None:
            # Only happens if we only have FQPs since the presence of any FFP
            # will result in BP_type having the value 'FFP'
            tg.BP_type = 'Slowest FQP'
            tg.BP_index = FFP_ranks - 1
        tg.sSP_index = tg.BP_index

    # Define a default sSP EF for determining which reaction actually has the
    # sSP. Note that the true sSP is the reaction with the slowest of the slow
    # non-negligible processes, not the reaction with the slowest maximum EF.
    # We choose as the default sSP EF the EF of the BP.
    sSP_EF = tg.ranked_uEF_list[tg.BP_index][0][1]

    # Find the sSP index starting at the first non-FQP and going down. Note that
    # we do not start at the BP index because there may be intervening
    # unthrottled FQPs that are not in the set of slow processes. Any reactions
    # from here to negligibly slow reactions are added to the SP list.  Once we
    # find the first negligibly slow process, we bail out.
    # Algorithm step 1.c.iii
    for i in range(FFP_ranks, tg.sSP_index + 1):
        if no_SP: # We can skip this loop as there are no slow processes
            # Cases 3, 4, 7
            break

        # Get reaction/process data
        master_EF_list_idx = tg.ranked_uEF_list[i][0][2][0]
        EF_max = tg.uEF_list[master_EF_list_idx][4] # Max of fwd/rev uEFs
        proc_name = tg.ranked_uEF_list[i][0][0]
        rxn_number = proc_name[1:]

        if EF_max >= tg.NSP_EF_threshold:  # This is a valid SP -- EF_max is zero for NPs
            # Add process to list of slow processes
            # Cases 1, 2, 5, 6
            if proc_name[0] == 'F': # Forward reaction
                tg.descend_SP_list.append([rxn_number, EF_max, 1,
                    (master_EF_list_idx, i)])
            elif proc_name[0] == 'R': # Reverse reaction
                tg.descend_SP_list.append([rxn_number, EF_max, 2,
                    (master_EF_list_idx, i)])
            else:
                pass # Should not happen
            # Check whether this reaction has the new lowest non-negligible EF
            # and update the index and the lowest non-negligible EF.
            if tg.NSP_EF_threshold < EF_max < sSP_EF:
                tg.sSP_index = i
                sSP_EF = EF_max
        else: # This reaction and all others below it are too slow
            # Note that we should never encounter this condition if
            # ranked_uEF_list was properly constructed.
            # Cases 1, 5
            # We won't get here for 2, 6 (the loop terminates first) but
            # sSP_index is already set to the correct value in the
            # initialization.
            break

    # Print a warning if we have only negligible processes
    # Case 7
    if len(tg.descend_SP_list) == 0 and len(tg.ascend_FFP_list) == 0:
        tg.BP_name = 'No non-negligible processes'
        tg.BP_type = None
        print('WARNING: There are no process event frequencies in the rankings. The simulation will likely crash soon. Be sure that tg.max_time is not set too low.')

    # Return with our sorted lists of fast and slow throttled processes and the
    # BP/sSP indices stored in the globals module
    tg.BP_name = tg.ranked_uEF_list[tg.BP_index][0][0]
    return

# This is function will handle sorting all the processes by speed and then
# segregates the processes into fast, slow, and negligible processes. It calls
# auxiliary functions to do the heavy lifting. It then assigns the various
# structures required by the throttling algorithm to the global dictionaries.
# Algorithm step 1
def rank_EFs_driver():

    # Calculate the unthrottled event frequencies
    back_calculate_uEF()

    # Extract the unthrottled EFs from the global tg.uEF_TOF_list
    # list and assign it to both the unthrottled and throttled master lists.
    get_process_info()
    tg.ptEF_list = deepcopy(tg.uEF_list)

    # Divide the processes into fast, slow, and negligible processes for the
    # ranking scheme.
    create_ranked_EF_list()

    # Create the lists for this scheme
    create_FFP_SP_lists()

################################################################################
#                                                                              #
#          PART II: FUNCTIONS RELATED TO CARRYING OUT THE THROTTLING           #
#                                                                              #
#   This part has the following functions:                                     #
#                                                                              #
#       1.  set_compression_schemes                                            #
#               Creates a progression of compression levels to try             #
#       2.  initialize_throttling_factors_list                                 #
#               Initializes a structure of throttling factors                  #
#       3.  calculate_ptEFs                                                    #
#               calculates the ptEFs for every process                         #
#       4.  check_scale_compression                                            #
#               Tests whether the throttling level meets the requested         #
#               compression amount                                             #
#       5.  set_throttled_rate_constants_list                                  #
#               Generates a list of rate constant expressions incorporating    #
#               the throttling factors                                         #
#       7.  find_aggregate_throttling_factors                                  #
#               Takes the throttling level and process rankings and sets the   #
#               aggregate throttling factors                                   #
#       8.  throttle_rate_constants_driver                                     #
#               Driver function to direct the throttling algorithm             #
#                                                                              #
################################################################################

# This function is responsible for setting the throttling scheme based on the
# number of ranks in the fast and slow lists.
# Algorithm step 2
def set_compression_schemes(FFP_ranks, SP_ranks):

    compression_schemes = []
    for slow_scale in range(0, tg.max_slow_scale+1):
        for fast_scale in range(0, tg.max_fast_scale+1):

            # If we are using full range scaling, we need to exclude slow
            # throttling (slow throttling scales larger than zero) for fast
            # scales equal to zero to avoid meeting the EF_range_full_requested criterion
            # by accidentally compressing the slow processes when there are fast
            # processes that could be compressed instead. This condition will
            # still allow an initial combination of (0, 0).
            if (tg.EF_range_flag == 'full' and FFP_ranks != 0 and
                (slow_scale != 0 and fast_scale == 0)):
                continue  # Skips this tuple

            # Add this tuple to the progression
            compression_schemes.append((fast_scale, slow_scale))

            # If we don't have any fast processes, we don't need to include any
            # of the higher fast compression scales.
            if FFP_ranks == 0:
                break # Skips all remaining tuples

        # If we don't have any slow processes, then we don't need to include any
        # of the higher slow compression scales.
        if SP_ranks == 0:
            break # Skips all remaining tuples

    return compression_schemes

# This function will initialize a local throttling_factors list.
def initialize_throttling_factors_list():

    # The structure of this list is as follows:
    #   First index: [0] - list of FFPs (ascending order), [1] - list of SPs
    #       (descending order)
    #   Second index (for each FFP/SP): Selects sublist for individual processes
    #   Third index: [0] - reaction number, [1] - throttling factor,
    #       [2] - reaction direction, [3] - process name (F/R + reaction number),
    #       [4] - 2-tuple with (1) index to reaction in uEF_list and (2) index to
    #       corresponding entry in ranked_uEF_list.

    # Basic empty lists
    throttling_factors = []

    # Default throttling factor (1) -- no throttling will be applied
    default_throttle_factor = 1

    # Loop over FFPs (index 0) and SPs (index 1)
    for i in range(2):

        sublist = []
        if i == 0: # FFPs
            process_list = tg.ascend_FFP_list
        else: #SPs
            process_list = tg.descend_SP_list

        # Extract data for each process in the list
        for j in range(len(process_list)):
            rxn_number = process_list[j][0]
            rxn_dir = process_list[j][2]
            EF_list_indices = process_list[j][3]
            if rxn_dir == 1: # Forward
                proc_name = 'F' + rxn_number
            elif rxn_dir == 2: # Reverse
                proc_name = 'R' + rxn_number
            else:
                pass # Should not happen

            # Add data to the current sublists
            sublist.append([rxn_number, default_throttle_factor, rxn_dir,
                proc_name, EF_list_indices])

        # Add current sublists to the parent lists
        throttling_factors.append(sublist)

    return throttling_factors

# This function updates the global list of throttled EFs.
def calculate_ptEFs():

    # Calculate the projected EFs for every process. We have to loop over both
    # the fast and slow processes.
    # Algorithm step 2
    for i in [0, 1]: # 0 is list of FFPs, 1 is list of SPs
        # Each j index corresponds to a different fast/slow process
        for j in range(len(tg.aggregate_throttling_factors[i])):

            # Incremental throttling factor for current process
            agg_throttling_factor = tg.aggregate_throttling_factors[i][j][1]

            # Process number for current process
            proc_name = tg.aggregate_throttling_factors[i][j][3]

            # Indices for uEF_list and ranked_uEF_list to make sure we calculate
            # every EF only once
            EF_list_index, ranked_EF_list_index = (
                tg.aggregate_throttling_factors[i][j][4])

            # This a list of all processes associated with this throttling
            # factor
            ranked_uEF_sublist = tg.ranked_uEF_list[ranked_EF_list_index]

            # This loops over every valid ranked process. There are no reactions
            # with invalid (None) EFs in this list due to how it was
            # constructed.
            for k in range(len(ranked_uEF_sublist)):

                # Process number
                proc_name = ranked_uEF_sublist[k][0]

                # Index into uEF_list specifying forward/reverse EF, as given
                # by the 2-tuple of (EF_list_index, EF_list_rxn_index)
                EF_list_rxn_index = ranked_uEF_sublist[k][2][1]

                # Calculation of the throttled EF for the specified reaction
                # directions
                ptEF = ranked_uEF_sublist[k][1] * agg_throttling_factor

                # Set this ptEF in the ptEF_list structure
                tg.ptEF_list[EF_list_index][EF_list_rxn_index] = ptEF

    # Now update the ptEF_list structure with the throttled max EFs
    # right now we have separate if statements to take whatever is not None.
    # This is because max & ">" comparisons don't work with None types.
    # Another approach would be to populate two temporary variables and then
    # give the value "0" to the temporary variable for a None Type,
    # and that way a ">" or max type operator could be used.
    for i in range(len(tg.ptEF_list)):
        if (tg.ptEF_list[i][1] is not None and
            tg.ptEF_list[i][2] is not None):
            tg.ptEF_list[i][4] = max(tg.ptEF_list[i][1:3])
        elif tg.ptEF_list[i][1] is not None:
            tg.ptEF_list[i][4] = tg.ptEF_list[i][1]
        elif tg.ptEF_list[i][2] is not None:
            tg.ptEF_list[i][4] = tg.ptEF_list[i][2]
        else:
            tg.ptEF_list[i][4] = None #This means both forward and reverse reaction had no events.
            pass 

# This function checks for whether the requested throttling amount meets the
# requested scale compression level.
# Algorithm step 2.d -- calculate ratio of fastest EF to slowest EF for both
# full and split ranges and determine if requested compression EF_range_req
# matches the achievable compression.
def check_scale_compression():

    # Set default return value (assume failure of compression level)
    compression_achieved = False

    # Find the upper and lower EF bounds for the fast processes
    if len(tg.ascend_FFP_list) > 0: # We have fast processes

        # Fastest FFP is upper bound for FFPs
        fFFP_ptEF_idx = tg.ascend_FFP_list[-1][3][0]
        fFFP_ptEF = tg.ptEF_list[fFFP_ptEF_idx][4]

        # Now we find the slowest FFP above the floor. If there is no FFP above
        # the floor, then the sFFP and the fFFP will be the same. If there is a
        # sFFP, then we check how close it is to an FQP, if present. Note that
        # the slowest FFP for the purposes of determining the throttling range
        # is not necessarily the slowest /throttled/ FFP; instead, it could be
        # unthrottled if above the floor but within Nsites of the FRP.
        sFFP_idx = None
        for i in range(len(tg.ascend_FFP_list)):
            sFFP_ptEF_idx = tg.ascend_FFP_list[i][3][0]
            sFFP_ptEF = tg.ptEF_list[sFFP_ptEF_idx][4]
            if sFFP_ptEF >= tg.FFP_floor:
                if i > 0:
                    fFQP_ptEF_idx = tg.ascend_FFP_list[i-1][3][0]
                    fFQP_ptEF = tg.ptEF_list[fFQP_ptEF_idx][4]
                sFFP_idx = i
                break

        if sFFP_idx is None: # No throttled FFPs (all FQPs)

            sFFP_ptEF = fFFP_ptEF # This should be the case already

        else: # Throttled FFPs

            # If we have a nearby FQP, we use the floor as the lower bound
            # instead of the regular sFFP ptEF.
            if sFFP_idx > 0 and fFQP_ptEF * tg.Nsites > sFFP_ptEF:
                sFFP_ptEF = tg.FFP_floor
            #TODO: sFFP_ptEF = tg.FFP_floor should be changed because it assigns sFFP_ptEF to tg.FFP_floor rather than creating some kind of effective compression scheme target variable.

    # Find the upper and lower EF bounds for the slow processes
    if len(tg.descend_SP_list) > 0: # We have slow processes

        # FRP is the upper bound for slow processes
        FRP_ptEF_idx = tg.descend_SP_list[0][3][0]
        FRP_ptEF = tg.ptEF_list[FRP_ptEF_idx][4]

        # Slowest SP is the lower bound for slow processes
        sSP_ptEF_idx = tg.descend_SP_list[-1][3][0]
        sSP_ptEF = tg.ptEF_list[sSP_ptEF_idx][4]

    # Initialize EF_range_*_actual values to None so we only have to set the
    # appropriate values later.
    tg.EF_range_fast_actual = None
    tg.EF_range_slow_actual = None
    tg.EF_range_full_actual = None

    # Now check compression levels
    if tg.EF_range_flag == 'split':

        # Calculate the fast ratio and compare it to the requested compression
        # ratio plus a small amount to account for numerical precision issues in
        # the ratio calculation.
        if len(tg.ascend_FFP_list) > 0:
            tg.EF_range_fast_actual = fFFP_ptEF / sFFP_ptEF
            if tg.fast_throttling_scale == tg.max_fast_scale:
                # We are at the maximum fast compression, so we have to accept
                # this as the best we can do, even if it doesn't meet the
                # compression requested. This is important so that if we don't
                # meet the compression we won't incorrectly try all the slow
                # scales too, even if an unthrottled slow scale would be
                # adequate.
                fast_met = True
            elif tg.FFP_roof is None:
                fast_met = (tg.EF_range_fast_actual <= tg.EF_range_fast_requested
                    * (1 + tg.floating_point_rel_tol))
            elif tg.FFP_roof is not None:
                fast_met = (tg.EF_range_fast_actual <= tg.EF_range_fast_requested
                    * (1 + tg.floating_point_rel_tol) and fFFP_ptEF < tg.FFP_roof)
        else: # No fast processes, so this is true by default
            fast_met = True

        # Calculate the slow ratio and compare it to the requested compression
        # ratio plus a small amount to account for numerical precision issues in
        # the ratio calculation.
        if len(tg.descend_SP_list) > 0:
            if tg.slow_throttling_scale == tg.max_slow_scale:
                # This is parallel with the fast check above, although here it
                # doesn't really do much good because if we reach this point,
                # then we've probably tried all the other options and are at the
                # end of the loop anyway.
                slow_met = True
            else:
                tg.EF_range_slow_actual = FRP_ptEF / sSP_ptEF
                slow_met = (tg.EF_range_slow_actual <= tg.EF_range_slow_requested
                            * (1 + tg.floating_point_rel_tol))
        else: # No slow processes, so this is true by default
            slow_met = True

        # Successful compression is achieved when both the fast and slow scale
        # compression amounts are met.
        compression_achieved = (fast_met and slow_met)

    elif tg.EF_range_flag == 'full':

        # Calculate the compression ratio. The numerator and denominator depend
        # on the number of fast and slow processes.
        if len(tg.ascend_FFP_list) > 0 and len(tg.descend_SP_list) > 0: # Both FFPs/SPs
            tg.EF_range_full_actual = fFFP_ptEF / sSP_ptEF
        elif len(tg.ascend_FFP_list) > 0 and len(tg.descend_SP_list) == 0: # FFPs only
            tg.EF_range_full_actual = fFFP_ptEF / sFFP_ptEF
        elif len(tg.ascend_FFP_list) == 0 and len(tg.descend_SP_list) > 0: # SPs only
            tg.EF_range_full_actual = FRP_ptEF / sSP_ptEF
        else: # No reactions, compression acheived by default
            compression_achieved = True
            return compression_achieved

        # Successful compression is achieved when the compression ratio meets
        # the criterion plus a small amount to account for finite precision.
        compression_achieved = (tg.EF_range_full_actual <= tg.EF_range_full_requested
                                * (1 + tg.floating_point_rel_tol))

    return compression_achieved

# This function is for getting the aggregate throttling factors for a
# specified throttling scheme.
# Algorithm step 2.a, 2.b, 2.c. See Table 3 in the manuscript.
def find_aggregate_throttling_factors():

    # Initialize the aggregate throttling factors and the rate constant list
    tg.aggregate_throttling_factors = initialize_throttling_factors_list()

    # Set the number of process ranks to iterate over. This is a convenient
    # method to control whether we throttle fast process, slow processes, or
    # both.
    FFP_ranks = len(tg.ascend_FFP_list)
    SP_ranks = len(tg.descend_SP_list)

    # Bail out if there are no processes at all
    if FFP_ranks == 0 and SP_ranks == 0:
        tg.FFP_step_down_type = 'No Processes in Rankings'
        return

    # Set the staggering factors for the fast and slow processes.
    fast_SF_compression = tg.staggering_factors[tg.fast_throttling_scale]
    slow_staggering_factor = tg.staggering_factors[tg.slow_throttling_scale]

    # Set the EF threshold below which processes are not throttled. This is the
    # floor with only FFPs (unthrottled processes are FQPs) and the max of the
    # floor (i.e., the FQPs) and the FRP*FRP_Buffer threshold (this may include some
    # unthrottled FFPs). By default, FRP_Buffer is Nsites
    # TODO: The lines calculating min_threshold_step_down_type and step_down_ptEF
    # TODO: should probably someday be separated into a functions called "calculate_step_down_ptEF" or something like that.
    # TODO: The calculation of sFFP_stepup_factor would be part of this separated function.
    if SP_ranks == 0 and FFP_ranks > 0:
        FFP_EF_min_threshold = tg.FFP_floor
        min_threshold_step_down_type = 'FFP Floor Reached'
    elif SP_ranks > 0 and FFP_ranks > 0:
        FRP_uEF = tg.descend_SP_list[0][1]
        FFP_EF_min_threshold = max(tg.FFP_floor, FRP_uEF * tg.FRP_Buffer)
        if tg.FFP_floor > FRP_uEF * tg.FRP_Buffer:
            min_threshold_step_down_type = 'FFP Floor Reached'
        else:
            min_threshold_step_down_type = 'FFP/FRP FRP_Buffer Staggering Reached'
    FFP_EF_min_threshold_reached = False
    
    # The default case is 'No Step Down'
    tg.FFP_step_down_type = 'No Step Down, Unthrottled Snapshot'

    # Set the step down type for the case of no FFPs at all
    if FFP_ranks == 0:
        tg.FFP_step_down_type = 'No FFPs to Step Down'

    # Throttle the FFPs. The slowest FFP may be stepped down towards the FQPs
    # and/or the FRP (if no FQPs exist). Subsequent processes are staggered
    # according to the specified staggering factors. The FQPs are never
    # throttled, so their TFs are always 1.
    # Algorithm step 2.a

    # The following flag is used to decide which process is the sFFP and thus
    # subject to step-down.
    sFFP_found = False

    # We'll assume that there are no FFPs. This will be updated if we find one.
    sFFP_index = None

    # Iterate over all fast processes
    for i in range(0, FFP_ranks):
        current_rank_uEF = tg.ascend_FFP_list[i][1]
        if current_rank_uEF >= tg.FFP_floor and not sFFP_found:
            # If if current_rank_uEF < tg.FFP_floor then it's an FQP, not an FFP.
            # So the sFFP is by definition the first FFP above the FFP_floor.
            # We may want to change the names or definitions since FQP is in the asdend_FFP_list.
            # Maybe it should be called ascend_FQP_list, and that only FQPs > FFP_floor are FFPs.
            # This is the first time we have encountered a true FFP, so we note that
            # we have found it and which rank it is. By noting that we have
            # found it, we avoid the case where we would try to step down each
            # FFP individually.
            sFFP_found = True
            sFFP_index = i

        if current_rank_uEF < FFP_EF_min_threshold:
            # These processes are not throttled
            current_rank_ptEF = current_rank_uEF

            # Set the step down label
            if current_rank_uEF < tg.FFP_floor:
                tg.FFP_step_down_type = 'No Step Down, Below floor'
            else:
                tg.FFP_step_down_type = 'No Step Down, Below Nsites * FRP uEF'

        elif i == sFFP_index: # Slowest throttled FFP -- try to step it down

            # Note that we will skip the step down if process rank i is below
            # the minimum throttling threshold.

            # Set the process number for the sFFP index
            sFFP_rxn_number = tg.ascend_FFP_list[sFFP_index][0]
            sFFP_max_dir = tg.ascend_FFP_list[sFFP_index][2]
            if sFFP_max_dir == 1:
                sFFP_proc_name = 'F' + sFFP_rxn_number
            elif sFFP_max_dir == 2:
                sFFP_proc_name = 'R' + sFFP_rxn_number
            else:
                pass # Should not happen

            # We need to step down from the observed rate. We re-calculate this
            # from the old ATF and the uEF.
            if sFFP_proc_name in tg.aggregate_throttling_factors_dict_old:

                # This process has a throttled rate
                current_sFFP_old_TF = tg.aggregate_throttling_factors_dict_old[sFFP_proc_name]

            else: # This process does not have a throttled rate

                current_sFFP_old_TF = 1
            sFFP_uEF = current_rank_uEF
            sFFP_oEF = sFFP_uEF * current_sFFP_old_TF

            # We need to unthrottle any benchmark FFP that has an aggregate
            # throttling factor that is not the largest aggregate throttling
            # factor in order to prevent too aggressive down-stepping.

            # Find the largest aggregate throttling factor for FFPs but not
            # FQPs. Since we know where the sFFP is (we already checked above)
            # and the processes are sorted, we can just start this loop at the
            # sFFP.
            max_TF = 0.0
            for j in range(sFFP_index, len(tg.ascend_FFP_list)):

                rxn_name = tg.ascend_FFP_list[j][0]
                for rxn_dir in ['F', 'R']:
                    proc_name = rxn_dir + rxn_name
                    if proc_name in tg.aggregate_throttling_factors_dict_old:
                        # We have an existing throttling factor for a
                        # non-benchmark process
                        TF = tg.aggregate_throttling_factors_dict_old[proc_name]

                        # If this aggregate throttling factor is larger than the
                        # previous maximum, we save its value. If it is larger
                        # than 1, we cap it at 1 to avoid unthrottling the sFFP
                        # too much, and then we abort the loop as anything
                        # larger would also be set to 1.
                        if 1 > TF > max_TF:
                            max_TF = TF
                        elif TF >= 1:
                            max_TF = 1.0
                            break
                    else:
                        # This process has never been throttled before, so by
                        # definition it has the least aggressive throttling
                        max_TF = 1.0
                        break

            # Set the step-up factor
            sFFP_stepup_factor = max_TF / current_sFFP_old_TF

            # Algorithm step 2.a
            # Test the throttled rate to see where it falls in relation to the
            # floor rate and the minimum separation permitted between the sFFP
            # and the next slower process which is an FQP. The target rate is
            # the largest of the following cases:
            #   1.  The current observed rate divided by the default step down
            #       value tg.FFP_step_down multiplied by the step up value;
            #   2.  The current value of FFP_EF_min_threshold, which is the
            #       minimum allowed rate for throttled FFPs (this is the maximum
            #       of tg.FFP_floor and Nsites times the FRP uEF, if present);
            #       and
            #   3.  The throttled rate that satisfies the minimum allowed
            #       spacing between the sFFP and the fastest FQP (if available).
            #       This minimum allowed spacing is determined from the list of
            #       tg.staggering_factors and the spacing between the
            #       unthrottled rates, with the latter always serving as an
            #       upper bound on the permitted spacing.
            # Then we calculate the throttling factor that will take us to the
            # target rate. This throttling factor is the ratio of the target
            # rate to the unthrottled rate. All other faster processes will be
            # pegged to this rate.
            
            # TODO: The lines calculating min_threshold_step_down_type and step_down_ptEF
            # TODO: should probably someday be separated into a functions called "calculate_step_down_ptEF" or something like that.
            # TODO: The calculation of sFFP_stepup_factor would be part of this separated function.

            #The ptEF_threshold_list variable is a little confusing:   It is a list of
            # threshold values and their "types", so it is a little bit
            # like a dictionary only with "[[value1,key1, [value2:key2]]"
            # then we sort it by the values to get the max value, and
            # the key associated with that value. Using a dictionary
            #  instead of this nested list structure might have been a better idea.
            ptEF_threshold_list = [] 

            # 1. Default step down amount
            step_down_ptEF = sFFP_oEF/tg.FFP_step_down*sFFP_stepup_factor
            if step_down_ptEF > sFFP_uEF:
                print('WARNING: Target FFP step down rate is larger than unthrottled rate. Setting step down rate to unthrottled rate.')
                print('Target rate =', step_down_ptEF, ' Unthrottled rate =', sFFP_uEF)
                step_down_ptEF = sFFP_uEF
                ptEF_threshold_list.append([step_down_ptEF, 'FFP Step Up'])  #Abnormal case.
            else:
                ptEF_threshold_list.append([step_down_ptEF, 'FFP Step Down']) #Normal case.

            # 2. The minimum EF threshold was already calculated above, so we
            # can use it as-is. This includes the floor and the FRP Nsites
            # threshold, if we have an FRP.
            ptEF_threshold_list.append([FFP_EF_min_threshold,
                min_threshold_step_down_type])

            # 3. The minimum spacing allowed between an FQP and the sFFP
            if sFFP_index > 0: # We have FQPs present to account for
                fFQP_uEF = tg.ascend_FFP_list[sFFP_index-1][1]
                if tg.fast_throttling_scale == 0: # No compression
                    sFFP_FQP_SF = min(tg.Nsites, sFFP_uEF/fFQP_uEF)
                else:
                    sFFP_FQP_SF = min(fast_SF_compression, sFFP_uEF/fFQP_uEF)
                sFFP_FQP_SF_ptEF = fFQP_uEF * sFFP_FQP_SF
                ptEF_threshold_list.append([sFFP_FQP_SF_ptEF,
                    'Max FQP Step Reached'])

            # Get the target ptEF from the available options by sorting the list
            # in reverse (descending) order and taking the first element. The
            # step down type is then just the string associated with the
            # threshold.
            ptEF_threshold_list.sort(key=lambda x: x[0], reverse=True)
            sFFP_target_ptEF = ptEF_threshold_list[0][0]
            tg.FFP_step_down_type = ptEF_threshold_list[0][1]

            # Set the base throttling factor. We have to use the unthrottled
            # rate to ensure that (1) we can step down multiple times and (2)
            # that the TF will never go above 1.
            sFFP_TF = sFFP_target_ptEF / sFFP_uEF

            if sFFP_TF > 1.0:
                # Always reset the TF to 1, but only print warning if the
                # departure from 1 is too extreme. This will filter out the
                # (relatively) common occurrence of the target ptEF being
                # slightly larger than the uEF due to finite precision while
                # still providing a useful warning if something went wrong. We
                # don't need to divide by one when checking the relative
                # tolerance.
                if abs(sFFP_TF - 1.0) > tg.floating_point_rel_tol:
                    print('WARNING: Throttling factor for benchmark FFP is above 1.0.')
                    print('  Throttling factor = %1.20f' % sFFP_TF)
                    print('  Target rate =', sFFP_target_ptEF, ' Unthrottled rate =', sFFP_uEF)
                    print('  Resetting throttling factor to 1.0.')
                sFFP_TF = 1.0
                sFFP_target_ptEF = sFFP_uEF

            # Now save the rates and the throttling factor
            tg.aggregate_throttling_factors[0][sFFP_index][1] = sFFP_TF
            current_rank_ptEF = sFFP_target_ptEF
            current_rank_uEF = sFFP_uEF

        else: # Faster throttled FFPs -- find ptEFs using the staggering factors

            # Algorithm step 2.b

            # Get the current rate
            current_rank_uEF = tg.ascend_FFP_list[i][1]

            # Find the staggering factor, which is the minimum of the default
            # staggering factor and the actual spacing between the uEFs of the
            # current process and the next slower process unless there is no
            # compression, in which case the staggering factor is always the
            # uncompressed staggering.
            uEF_SF_natural = current_rank_uEF / last_rank_uEF
            if tg.fast_throttling_scale == 0: # No compression
                active_SF = uEF_SF_natural
            else: # Compression
                active_SF = min(fast_SF_compression, uEF_SF_natural)

            # Calculate the new ptEF (note the multiplication as the current
            # ptEF is larger than the last rank ptEF)
            current_rank_ptEF = last_rank_ptEF * active_SF

            # Check to see if the ptEF is below the minimum threshold, which is
            # the larger of the floor and the FRP Nsites criteria. If it would
            # go below the minimum threshold due to compression, we stop it at
            # the threshold. The uEF for this process rank is above the
            # threshold. This particular check should only happen once, as all
            # process ranks that are faster than this should be staggered above
            # it.
            if current_rank_ptEF < FFP_EF_min_threshold:
                if not FFP_EF_min_threshold_reached:
                    # First occurrence is OK. Just set the ptEF to the
                    # threshold.
                    FFP_EF_min_threshold_reached = True
                    current_rank_ptEF = FFP_EF_min_threshold
                else:
                    # Subsequent occurrences are not OK. Something went wrong,
                    # and this should not be happening.
                    print('WARNING: Encountered repeated attempts to compress FFPs below the minimum threshold. This is a bug!')

            # Calculate the new TF
            current_TF = current_rank_ptEF / current_rank_uEF

            # Save the rates and the throttling factor for the next iteration
            tg.aggregate_throttling_factors[0][i][1] = current_TF

        # Update the process rank EFs
        last_rank_ptEF = current_rank_ptEF
        last_rank_uEF = current_rank_uEF

    # Check for no SPs to throttle. Note that if SP_ranks == 1, the only slow
    # process is the FRP, and this is never throttled (by definition). And if
    # there are no slow processes at all, then there is trivially nothing to do.
    # Also, since there is no concept of 'step up' for SPs (only compression),
    # if there is no compression requested, then we can just leave all the SP
    # TFs at their initial value of 1.
    if SP_ranks < 2 or tg.slow_throttling_scale == 0:
        return

    # Iterate over the slow processes, finding the ptEFs and setting the TFs
    # with the staggering factors. We skip any SPs that are not throttled.
    # Algorithm step 2.c
    FRP_uEF = tg.descend_SP_list[0][1]
    last_rank_ptEF = tg.descend_SP_list[0][1]
    last_rank_uEF = last_rank_ptEF
    SP_EF_max_threshold_reached = False
    for i in range(1, SP_ranks): # This skips the FRP

        # Get the current rate
        current_rank_uEF = tg.descend_SP_list[i][1]

        # If this process is slower than the Nsites threshold, process it
        if current_rank_uEF <= FRP_uEF / float(tg.Nsites):

            # Find the staggering factor, similar to the way we did for the
            # FFPs, except that the ratios between the last rank and current
            # uEFs are inverted.  Since we have compression if we get this far,
            # we don't have to worry about no compression as a special case.
            uEF_SF_natural = last_rank_uEF / current_rank_uEF
            active_SF = min(slow_staggering_factor, uEF_SF_natural)

            # Calculate the new ptEF (note the division as the current ptEF is
            # smaller than the last rank ptEF)
            current_rank_ptEF = last_rank_ptEF / active_SF

            # Check if the ptEF is inside the Nsites window and adjust it if it
            # is
            if current_rank_ptEF > FRP_uEF/tg.Nsites:
                if not SP_EF_max_threshold_reached:
                    # First occurrence is OK. Just reset the ptEF to the
                    # threshold.
                    current_rank_ptEF = FRP_uEF/tg.Nsites
                else:
                    # Subsequent occurrences are not OK. Something went wrong,
                    # and this should not be happening.
                    print('WARNING: Encountered repeated attempts to compress SPs above the maximum threshold. This is a bug!')

            # Calculate the new TF
            current_TF = current_rank_ptEF / current_rank_uEF

            # Save the rates and the throttling factor for the next iteration
            tg.aggregate_throttling_factors[1][i][1] = current_TF

        else: # This process is not throttled -- the ptEF is the uEF

            current_rank_ptEF = current_rank_uEF

        # Update the EFs for the process ranks in preparation for the next
        # iteration
        last_rank_ptEF = current_rank_ptEF
        last_rank_uEF = current_rank_uEF

    # We are now done. The final aggregate_throttling_factors list is stored in
    # the globals module.
    return

# This is a driver function for the rest of the throttling code. It takes the
# sorted fast and slow process lists and a single two element list with
# information on the slowest relevant process (process number and rate),
# determines the appropriate throttling scheme and then loops over the steps in
# the selected scheme until the desired scale compression is achieved. The
# throttling scheme can either be generated automatically (the default) or
# optionally specified by the user.
# Algorithm step 2
def throttle_rate_constants_driver():

    # Set throttling scheme based on number of FFPs and SPs
    SP_ranks = len(tg.descend_SP_list)
    FFP_ranks = len(tg.ascend_FFP_list)
    if tg.compression_scheme_flag is None:
        tg.compression_schemes = [(0, 0)]
    elif str(tg.compression_scheme_flag).lower() == 'auto':
        tg.compression_schemes = set_compression_schemes(FFP_ranks, SP_ranks)
    elif str(tg.compression_scheme_flag).lower() == 'manual':
        if tg.compression_schemes is None:
            print('WARNING: Manual compression scheme requested, but no scheme supplied. Using default progression.')
            tg.compression_schemes = set_compression_schemes(FFP_ranks, SP_ranks)
            tg.compression_scheme_flag = 'auto'
    else:
        print('WARNING: Invalid compression scheme flag. Using default progression.')
        tg.compression_scheme_flag = 'auto'
        tg.compression_schemes = set_compression_schemes(FFP_ranks, SP_ranks)

    # TODO: Convert this to a function accessing the next compression scheme
    # Loop over the throttling scheme
    for compression_scale in tg.compression_schemes:

        # Set global compression scales
        tg.fast_throttling_scale = compression_scale[0]
        tg.slow_throttling_scale = compression_scale[1]

        # Get the new aggregate throttling factors -- if the system has
        # FFPs, it will potentially step them down, even if no compression is
        # requested. This is because compression and FFP step down contribute in
        # different ways to throttling.
        find_aggregate_throttling_factors()

        # Bail out if we have no reactions in either the fast or slow list
        if SP_ranks == 0 and FFP_ranks == 0:
            break

        # Find the projected rates for the current throttling scheme
        calculate_ptEFs()

        # Check whether the throttling scheme is sufficient
        successful_compression = check_scale_compression()

        # If it is sufficient, we can exit the loop
        if successful_compression:
            break

################################################################################
#                                                                              #
#        PART III: FUNCTIONS RELATED TO APPLYING THE THROTTLING FACTORS        #
#                                                                              #
#   This part has the following functions:                                     #
#                                                                              #
#       1.  update_incremental_throttling_factors                              #
#               Keeps the incremental throttling factors dictionary updates    #
#               and makes a list of fast/slow process names                    #
#       2.  update_aggregate_throttling_factors_dict                           #
#               Keeps the aggregate throttling factors dictionary updated      #
#       3.  apply_throttling_factors                                           #
#               Multiplies the pre-exponentials by the throttling factors      #
#       4.  regularize_rate_constants                                          #
#               Adjusts any throttled rate constants that are faster than a    #
#               user-specified threshold                                       #
#                                                                              #
################################################################################


# This function is responsible for keeping the incremental throttling factors
# dictionary up-to-date for the current ranking scheme. It also makes a list of
# all the fast and slow process names. This function uses the old ATF dictionary
# in calculating the ITFs.
# Algorithm step 3
def update_incremental_throttling_factors():

    # Initialize new name list
    tg.throttled_process_names = []

    # List of the aggregate_throttling_factors_dict keys -- these are processes
    # that have been throttled at some time in the past
    prev_throttled_proc_names = [proc_name for proc_name in
        tg.aggregate_throttling_factors_dict_old]

    # We need to build a new incremental throttling factors list and dictionary
    # from the aggregate throttling factors dictionary and the aggregate
    # throttling factors list.
    inc_throttling_factors = []
    tg.incremental_throttling_factors_dict = {}

    # Find the incremental throttling factors for the newly throttled processes.
    # We have to loop over both the fast and slow processes.
    for i in [0, 1]: # 0 is list of FFPs, 1 is list of SPs

        # New sublist for fast/slow process names
        name_sublist = []
        inc_sublist = []

        # Each j index corresponds to a different fast/slow process
        for j in range(len(tg.aggregate_throttling_factors[i])):

            # Reaction number
            rxn_number = tg.aggregate_throttling_factors[i][j][0]

            # Incremental throttling factor for current process
            agg_throttling_factor = tg.aggregate_throttling_factors[i][j][1]

            # Reaction direction
            rxn_dir = tg.aggregate_throttling_factors[i][j][2]

            # Process number for current process
            proc_name = tg.aggregate_throttling_factors[i][j][3]

            # Indices for EF_list and ranked_uEF_list to make sure we set every
            # aggregate factor only once
            EF_indices = tg.aggregate_throttling_factors[i][j][4]
            EF_list_index, ranked_uEF_list_index = EF_indices

            # Update new incremental throttling factor list
            if proc_name in prev_throttled_proc_names:
                inc_throttling_factor = (agg_throttling_factor /
                    tg.aggregate_throttling_factors_dict_old[proc_name])
            else:
                inc_throttling_factor = agg_throttling_factor / 1.0

            # Create a new list with the information for the aggregate
            # throttling factors structure
            inc_sublist.append([rxn_number, inc_throttling_factor, rxn_dir,
                proc_name, EF_indices])

            # This a list of all processes associated with this throttling
            # factor
            ranked_uEF_sublist = tg.ranked_uEF_list[ranked_uEF_list_index]

            # This loops over every valid ranked process. There are no reactions
            # with invalid (None) rates in this list due to how it was
            # constructed.
            for k in range(len(ranked_uEF_sublist)):

                # Process number
                proc_name = ranked_uEF_sublist[k][0]
                name_sublist.append(proc_name)

                # Set the associated throttling factor in the dictionary
                tg.incremental_throttling_factors_dict[proc_name] = (
                    inc_throttling_factor)

        # Add the process names to the list
        tg.throttled_process_names.append(name_sublist)
        inc_throttling_factors.append(inc_sublist)

        # Add the throttled process names to the set of processes with modified
        # pre-exponentials
        tg.modified_preexp_set |= set(name_sublist)

    # Unthrottle any negligible processes
    for proc_name in tg.throttled_negligible_process_names:
        tg.incremental_throttling_factors_dict[proc_name] = (
            1./tg.aggregate_throttling_factors_dict_old[proc_name])

    tg.incremental_throttling_factors = inc_throttling_factors

# This function is responsible for keeping the aggregate throttling factors
# dictionary updated.
# Algorithm step 3
def update_aggregate_throttling_factors_dict():

    # Reset the throttling factors in the dictionary to 1 (no throttling)
    tg.aggregate_throttling_factors_dict = {proc_name: 1.0 for proc_name in
        tg.aggregate_throttling_factors_dict}

    # Loop over the new aggregate throttling list updating the changed factors
    # in the dictionary
    for i in [0, 1]: # 0 is list of FFPs, 1 is list of SPs

        # Each j index corresponds to a different fast/slow process
        for j in range(len(tg.aggregate_throttling_factors[i])):

            # Incremental throttling factor for current process
            agg_throttling_factor = tg.aggregate_throttling_factors[i][j][1]

            # Index for ranked_uEF_list to make sure we set every aggregate
            # factor only once
            ranked_uEF_list_index = tg.aggregate_throttling_factors[i][j][4][1]

            # This a list of all processes associated with this throttling
            # factor
            ranked_uEF_sublist = tg.ranked_uEF_list[ranked_uEF_list_index]

            # This loops over every valid ranked process. There are no reactions
            # with invalid (None) rates in this list due to how it was
            # constructed.
            for k in range(len(ranked_uEF_sublist)):

                # Process number
                proc_name = ranked_uEF_sublist[k][0]

                # Set the associated throttling factor in the dictionary
                tg.aggregate_throttling_factors_dict[proc_name] = (
                    agg_throttling_factor)

# This is a simple function to update the rate constants for each process based
# on the calculated throttling factors.
# Algorithm step 3
def apply_throttling_factors():

    for proc_name in tg.aggregate_throttling_factors_dict:
        param = 'A' + proc_name
        param_val = float(sg.model.settings.parameters[param]['value'])
        throttling_factor = tg.aggregate_throttling_factors_dict[proc_name]
        # Multiplication to throttle the process
        param_val *= throttling_factor
        sg.model.settings.parameters[param]['value'] = param_val
    # In this function we really do need to recalculate all of the rate
    # constants as the next function call will be to the KMC algorithm, and we
    # need the rate constants to be correct for that.
    
    #Jan 8th 2018. Ashi believes the below seattr  line actually uses the "last value" of param to call kmcos to updates *all* parameters,
    #and that it is saved for outside of the loop to prevent all parameters from updating. His memory is that kmcos does not
    #update *any* parameters when you just change the "value" in the dictionary as shown in the loop above, thus this is necessary.
    #however, this will cause a bug if there are no parameters in the above loop (he encountered such a crash) so he added the if statement.
    if len(tg.aggregate_throttling_factors_dict) > 0:
        setattr(sg.model.parameters, param, param_val) 


# Function to reset the pre-exponentials to their unmodified values.
def reset_preexponentials():

    if tg.preexp_dict_original is None:
        # Initialize pre-exponential dictionary (if needed) on the first call
        tg.preexp_dict_original = {}
        params = [p for p in sg.model.settings.parameters if
            p.startswith('AF') or p.startswith('AR')]
        for param in params:
            tg.preexp_dict_original[param] = float(getattr(sg.model.parameters,
                param)['value'])
    else:
        # This is either not the first call, or the base pre-exponential
        # dictionary was already defined. Make sure that all rate constants are
        # reset to the value in the base value and save the old (regularized)
        # pre-exponentials for debugging use.
        tg.preexp_dict_original_reg_old = {}
        for proc_name in tg.modified_preexp_set:
            param = 'A' + proc_name
            param_val_old = sg.model.settings.parameters[param]['value']
            tg.preexp_dict_original_reg_old[param] = param_val_old
            param_val = float(tg.preexp_dict_original[param])
            sg.model.settings.parameters[param]['value'] = param_val
        # Recalculate the base rate constants to ensure any regularization is
        # based on the unmodified rate constants. If we don't need
        # regularization, then we can skip this step for a potentially large
        # performance gain.
        # TODO: Implement a more efficient way of calculating the unmodified
        # rate constants. This would occur in regularize_rate_constants. See
        # that function for more detail.
        if tg.regularization and len(tg.modified_preexp_set) > 0:
            setattr(sg.model.parameters, param, param_val)

        # We have restored the modified pre-exponentials, so we can empty the
        # set that stores which processes were modifeid in preparation for the
        # next run.
        tg.modified_preexp_set = set()

# This function will regularize all of the rate constants that are greater than
# the maximum allowed amount.
# Algorithm step 3
def regularize_rate_constants():

    # TODO: Make a more efficient way to calculate unmodified rate constants for
    # regularization. This will require the regularization factors from the
    # previous snapshot to back-calculate the unmodified rate constants.

    # Construct a list of all processes with non-zero pre-exponentials,
    # regardless of whether they are fast, slow, or negligible. The [1:] is
    # needed to exclude the leading 'A' to get the process name.
    active_processes = [p[1:] for p in tg.preexp_dict_original if tg.preexp_dict_original[p] > 0]

    # For each pre-exponential, check the associated rate constants
    max_process_rates = {}
    for proc_name in active_processes:
        max_proc_rate = max(float(sg.model.rate_constants.by_name(elem_proc))
            for elem_proc in
            sg.model.rate_constants.names('*' + proc_name + '*'))
        if max_proc_rate > tg.max_rate_constant:
            max_process_rates[proc_name] = max_proc_rate

    if len(max_process_rates) > 0:
        print('WARNING: Regularizing rate constant(s) above: ', tg.max_rate_constant)

    # Calculate the factors for setting the out-of-bounds process rate to the
    # maximum
    for proc_name in max_process_rates:
        tg.modified_preexp_set.add(proc_name) # Add this process to the modified processes
        reg_factor = tg.max_rate_constant / max_process_rates[proc_name]
        param = 'A' + proc_name
        param_val = float(sg.model.settings.parameters[param]['value'])
        param_val *= reg_factor
        sg.model.settings.parameters[param]['value'] = param_val
    # The following line will recalculate all of the rate constants. It is
    # currently commented out as this is unnecessary in the current
    # implementation, and there is a substantial performance penalty for doing
    # so. The time it takes to recalculate all the rate constants can easily
    # exceed the amount of time spent on KMC steps, so this should not be done
    # unless there is a very good reason to do so.
#    if len(max_process_rates) > 0:
#        setattr(sg.model.parameters, param, param_val)

################################################################################
#                                                                              #
#    PART IV: FUNCTIONS RELATED TO CARRYING OUT EXECUTION OF THE ALGORITHM     #
#                                                                              #
#   This part has the following functions:                                     #
#                                                                              #
#       1.  calculate_throttling_factors                                       #
#               Driver function that first ranks & classifies the processes    #
#               and then sets the throttling factors that results in the       #
#               needed compression and step-down                               #
#       2.  printout_throttling_info_headers                                   #
#               Prints headers for a debugging file                            #
#       3.  printout_throttling_info                                           #
#               Prints debugging info to a file                                #
#       4.  update_snapshot_variables                                          #
#               Makes sure certain snapshot-relataed variables are updated     #
#       5.  update_throttling_guidelines                                       #
#               Updates some of the control parameters according to            #
#               approximate guidelines                                         #
#       6.  do_throttled_snapshot                                              #
#               Executes exactly one iteration of the throttling algorithm,    #
#               employing a throttled snapshot if this is not the first        #
#               iteration and an unthrottled snapshot otherwise                #
#       7.  do_throttled_snapshots                                             #
#               Repeatedly executes a specified number of snapshots in         #
#               sequence                                                       #
#                                                                              #
################################################################################

# This function calls the various routines from the throttling module to rank
# the processes and calculate the throttling factors. Then it adjusts the
# throttling factors based on various constraints.
def calculate_throttling_factors(unthrottle_slow_processes=False):
    # Algorithm steps 1, 2

    # Rank the processes and generate the associated lists needed for
    # calculating the throttling constants. The TOF data list is actually the
    # observed EFs.
    rank_EFs_driver()

    # Calculate the aggregate throttling factors
    throttle_rate_constants_driver()

    # Unthrottle slow processes if requested
    if unthrottle_slow_processes:
        tg.aggregate_throttling_factors[1] = []

    # Construct a list of the updated incremental throttling factors.
    update_incremental_throttling_factors()

    # Update the aggregate throttling factors dictionary so that it is now
    # consistent with the aggregate throttling factors list.
    update_aggregate_throttling_factors_dict()

# This function will write headers for a file that is useful in debugging the
# throttling algorithm.
def printout_throttling_info_headers():
    throttling_info_file_name = sg.simulation_name + str('_throttling_info.csv')
    with open(throttling_info_file_name, 'w') as ti:
        ti.write('Simulation_name;')
        ti.write('Step;')
        ti.write('Time_(s);')
        ti.write('sps;')
        ti.write('tps;')
        ti.write('BP;')
        ti.write('BP_type;')
        ti.write('FFP_Step_Down;')
        ti.write('Scale;')
        ti.write('Target_(Full,Fast,Slow)_EF_Compression;')
        ti.write('Actual_(Full,Fast,Slow)_EF_Compression;')
        ti.write('Incremental_Fast_Throttled_List;')
        ti.write('Incremental_Slow_Throttled_List;')
        ti.write('Incremental_Throttling_Factors_Dict;')
        ti.write('Aggregate_Fast_Throttled_List;')
        ti.write('Aggregate_Slow_Throttled_List;')
        ti.write('Aggregate_Throttling_Factors_Dict;')
        ti.write('uEF_List;')
        ti.write('ptEF_List\n')

# This function will write data to a file that is useful in debugging the
# throttling algorithm.
def printout_throttling_info(unthrottled_step=False):
    throttling_info_file_name = sg.simulation_name + str('_throttling_info.csv')

    # Getting some variables that will go into the string.
    if unthrottled_step:
        BPstring = str(tg.BP_name) + ' unthrottled_step'
    else:
        BPstring = str(tg.BP_name)
    scale = (tg.fast_throttling_scale, tg.slow_throttling_scale)
    TargetEF_Ratios = (tg.EF_range_full_requested, tg.EF_range_fast_requested, tg.EF_range_slow_requested)
    ActualEF_ratios = (tg.EF_range_full_actual, tg.EF_range_fast_actual,
        tg.EF_range_slow_actual)

    # Below I am constructing the string prior to writing to try to reduce write
    # time and reduce I/O errors.
    stringToWrite = (
        str(sg.simulation_name) + ';' +
        str(sg.steps_so_far) + ';' +
        str(sg.kmc_time) + ';' +
        str(sg.sps_actual) + ';' +
        str(sg.tps_actual) + ';' +
        str(BPstring) + ';' +
        str(tg.BP_type) + ';' +
        str(tg.FFP_step_down_type) + ';' +
        str(scale) + ';' +
        str(TargetEF_Ratios)  + ';' +
        str(ActualEF_ratios)  + ';' +
        str(tg.incremental_throttling_factors[0]) + ';' +
        str(tg.incremental_throttling_factors[1]) + ';' +
        str(tg.incremental_throttling_factors_dict) + ';' +
        str(tg.aggregate_throttling_factors[0]) + ';' +
        str(tg.aggregate_throttling_factors[1]) + ';' +
        str(tg.aggregate_throttling_factors_dict) + ';' +
        str(tg.uEF_list) + ';' +
        str(tg.ptEF_list)  + ';' +
        '\n'
        )

    with open(throttling_info_file_name, 'a') as ti:
        ti.write(stringToWrite)

# TODO: Regularization prior to throttling would improve the selectivity for
# rare configuration slow processes. Will require additional code to ensure that
# FRPs and other benchmarks do not cause fast processes or FRPs to go above the
# rate constant regularization. This would become particularly complicated when
# more complicated regularization schemes are used.

# This function is used to update snapshots-related information in the snapshots
# globals and throttling globals modules.
def update_snapshot_variables(before_after):

    # Get the process names
    tg.proc_names = [sg.TOF_header_array[i] for i in
        range(len(sg.TOF_header_array)) if re.search(tg.regex,
        sg.TOF_header_array[i])]

    # Get the TOF information.
    oEF_TOF_list_local = [float(sg.TOF_data_list[i]) for i in
        range(len(sg.TOF_data_list)) if re.search(tg.regex,
        sg.TOF_header_array[i])]

    # Assign the TOF information and possibly the ATF information depending on
    # whether this update is before or after the current snapshot has been
    # executed.
    if before_after == 'before':
        tg.oEF_TOF_list = oEF_TOF_list_local
        tg.aggregate_throttling_factors_dict_old = deepcopy(
            tg.aggregate_throttling_factors_dict)
    elif before_after == 'after':
        tg.oEF_TOF_list_next = oEF_TOF_list_local

# This function will recalculate some important user-adjustable parameters for
# which we have some approximate guidelines for automatically setting their
# values. We set FFP_floor, sps, and FFP_step_down.
def update_throttling_guidelines():

    # Recalculate step down factor, ef_range, floor with flag to turn
    # on/off use of guidelines
    if tg.use_guideline_FFP_floor:
        tg.FFP_floor = tg.characteristic_EF * tg.Nsites
    if tg.use_guideline_sps:
        if tg.EF_range_flag == 'split':
            tg.throttling_sps = int(tg.EF_range_fast_requested * tg.Nsites *
                tg.n_characteristic_events_target)
        elif tg.EF_range_flag == 'full':
            tg.throttling_sps = int(tg.EF_range_full_requested)
    if tg.use_guideline_FFP_step_down:
        tg.FFP_step_down = max(float(tg.throttling_sps)/tg.Nsites,
            tg.default_FFP_step_down)
    else:
        tg.FFP_step_down = tg.default_FFP_step_down

    # Recalculate NSP threshold
    tg.NSP_EF_threshold = float(tg.Nsites)/tg.max_time

# This function will execute a single snapshot in conjunction with the
# throttling algorithm. If this is the first time a snapshot has ever been
# executed, then no throttling is performed.
# Algorithm steps 1, 2, 3
def do_throttled_snapshot(local_snapshot_idx, sps, tps, eic_module_objects):

    n_snapshots = 1

    # Reset the pre-exponentials to their unmodified state. Modifications may
    # be from either throttling or regularization.
    reset_preexponentials()

    # Regularize very large rate constants
    if tg.regularization:
        regularize_rate_constants()

    # Update the guidelines and the associated SPS in snapshots_globals
    update_throttling_guidelines()

    # We check the passed values of sps and tps. For each one that is None, we
    # set it to the corresponding value in tg (tg.throttling_sps or
    # tg.throttling_tps). If it is not None, then we use it as-is.
    if sps is None:
        sps_local = tg.throttling_sps
    else:
        sps_local = sps
    if tps is None:
        tps_local = tg.throttling_tps
    else:
        tps_local = tps

    # Save the oEF and ATF info from the last snapshot. This also updates the
    # new SPS in the snapshots_globals module.
    update_snapshot_variables('before')

    if local_snapshot_idx == 0:
        # Algorithm step 0
        if tg.print_throttling_info and tg.current_snapshot == 0:
            printout_throttling_info_headers()
        tg.FFP_step_down_type = 'No Step Down, First Snapshot'
        do_snapshots(n_snapshots, sps_local, tps_local)
        if tg.print_throttling_info:
            printout_throttling_info(unthrottled_step=True)
    elif ((local_snapshot_idx % tg.loop_base == 0 and local_snapshot_idx > 0)
        or tg.steady_state_throttling):
        # Algorithm step 1-3 with step 2.f (unthrottle slow processes) active
        calculate_throttling_factors(unthrottle_slow_processes=True)
        apply_throttling_factors()
        do_snapshots(n_snapshots, sps_local, tps_local)
        if tg.print_throttling_info:
            printout_throttling_info(unthrottled_step=True)
    elif local_snapshot_idx % tg.loop_base == 1:
        # Algorithm step 1-3
        calculate_throttling_factors()
        apply_throttling_factors()
        do_snapshots(n_snapshots, sps_local, tps_local)
        if tg.print_throttling_info:
            printout_throttling_info(unthrottled_step=False)
    elif local_snapshot_idx % tg.loop_base > 1: # % operator implicitly maxes out at tg.loop_base - 1
        # Algorithm step 1-3
        calculate_throttling_factors()
        apply_throttling_factors()
        do_snapshots(n_snapshots, sps_local, tps_local)
        if tg.print_throttling_info:
            printout_throttling_info(unthrottled_step=False)

    tg.current_snapshot += 1
    print('Snapshot =', tg.current_snapshot, 'Time =', sg.kmc_time)

    # Construct lists of process names and rates from the data in
    # snapshots_globals, making sure that we only get information that match
    # our naming scheme.
    update_snapshot_variables('after')

    # Save the modules
    if eic_module_objects is not None:
        for module_object in eic_module_objects:
            module_object.save_params()


    if sg.kmc_time >= tg.cutoff_time:
        print('Cutoff Time Exceeded')
        tg.cutoff_time_exceeded = True

# This function will run a total of Nsnapshots iterations of
# do_throttled_snapshot. By default it will start every cycle of
# do_throttled_snapshot calls with an unthrottled snapshot.
def do_throttled_snapshots(Nsnapshots, sps=None, tps=None,
    eic_module_objects=None):

    if tg.reset_snapshot_counter:
        # Default case, start with an unthrottled snapshot
        first_snapshot = 0
    else:
        # Use the global snapshot counter
        first_snapshot = tg.current_snapshot * 1

    for local_snapshot_idx in range(first_snapshot,
        first_snapshot + Nsnapshots):

        # Now perform the actual throttling.
        do_throttled_snapshot(local_snapshot_idx, sps, tps,
            eic_module_objects)

        if tg.cutoff_time_exceeded:
            break

#For throttling module. Requires the module_state_export_import module.
def reload(tg_module_state):
    tg_module_state.load_params()
    # Update the snapshot number #TODO: Check if this +=1 is really necessary. From code, I think this 
    # below line should not be necessary, so I commented it out. Maybe we improved the code flow at some point.
    #tg.current_snapshot += 1
