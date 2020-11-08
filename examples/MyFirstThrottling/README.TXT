  STAGGERED QUASI-EQUILIBRIUM RANK-BASED THROTTLING FOR STEADY STATE (SQERTSS)

       Jonathan E. Sutton [1], Thomas Danielson [1, 2], Aditya Savara [1]

                        [1] Chemical Sciences Division,
                         Oak Ridge National Laboratory

              [2] Department of Materials Science and Engineering,
              Virginia Polytechnic Institute and State University


                              Part I: Introduction

Welcome to the SQERTSS throttling code. It has been designed to accelerate the
convergence to and sampling of steady state during KMC simulations by
automatically adjusting the rate constants of extremely fast and (optionally)
extremely slow KMC processes. Fast processes should be throttled before slow
processes. Slow processes should not be throttled unless the approach to steady
state is very slow. They should be turned off once steady state is reached and
should not be throttled at all if the transient dynamics are important.

This package was originally designed to work with the kmcos KMC simulation
package. However, it is possible to modify it to work with other packages, as we
describe below.

We have also designed this package to employ a process naming scheme that can be
represented by a regular expression (specifically an 'F' or an 'R' followed by
a sequence of any number of digits, a 'p', and another sequence of any number of
digits). This is necessary for our use case and for common use cases with kmcos
because kmcos will frequently return process name and reaction rate lists that
have extra entries corresponding to groups of processes or that are
more-friendly aliases to another process name. The regular expression method
eases parsing these lists to extract only the relevant information.
Alternatively, if this is not an issue, then the raw lists can be used directly
by specifying a regular expression that will match any string of characters.
Alternate naming schemes (or not at all) may be used with the sole restriction
that process pairs must differ only in their leading character, and that leading
character must be an 'F' or an 'R' (for 'F'orward and 'R'everse processes). If
an alternate naming scheme is used, the regular expression will need to be
changed in the throttling_globals module (variable 'regex').

--------------------------------------------------------------------------------

                     Part II: List of External Dependencies

Our throttling code was originally written to interface with an in-house module
for collecting time averaged statistics on rates and coverages in sampling
windows known as snapshots. Our snapshots module was written to interface with
the KMC package kmcos. Recognizing that not everyone will necessarily wish to use
kmcos, we have intentionally limited the interaction of our throttling code with
our snapshots code and with kmcos. Nevertheless, some dependencies remain. We
summarize here the interfaces these dependencies have so that the throttling
code can be adapted to interface with other snapshots and/or KMC
implementations. We cover each throttling module file in turn.

throttling_globals.py
* kmc_settings.simulation_size:
    Number of unit cells on each side of the square simulation box. The total
    number of unit cells (Nsites) is calculated by

      Nsites = kmc_settings.simulation_size^2

throttling.py
* snapshots_globals.model.parameters:
    A dictionary of parameter dictionaries (activation energies,
    pre-exponentials, etc. that are used to calculate the rate constants and/or
    any parameter used by the simulation). The actual implementation is
    unimportant, so long as the model parameters can be reliably stored and
    retrieved.

* snapshots_globals.model.rate_constants.names('pattern'):
    Returns a list of names of elementary processes (each elementary process is
    reaction- and site-specific) matching a specified wildcard pattern. If no
    pattern is given as an argument, then it returns a list of all elementary
    process names. For example it could return:

      ['F1p0_S1', 'F2p0_S2', 'R1p0_S1', 'R2p0_S2']

    if the elementary process types are named 'F1p0', 'R1p0', 'F2p0', and
    'R2p0'; there are sites named 'S1' and 'S2' in the simulation unit cell; and
    not all process types can occur on all sites. The 'F' and 'R' in the
    elementary process types signify 'F'orward and 'R'everse directions in the
    process pairs '1p0' and '2p0'.

    This function is only used in regularizing rate constants. It is not key to
    the main algorithm, and in principle the regularization routine could be
    refactored to eliminate this function.

* snapshots_globals.model.rate_constants.by_name('proc_name'):
    Returns the rate constant (floating point number) when given the name
    (string) of an elementary process.

    Like its companion snapshots_globals.model.rate_constants.names(), this
    function is only used when regularizing rate constants, and this dependency
    could be removed with a rewrite of the regularization routine.

* snapshots_globals.kmc_time:
    Floating point variable that keeps track of the current simulation time

* snapshots_globals.simulation_name:
    A string with the name of the simulation

* snapshots_globals.steps_so_far:
    An integer with the total number of individual KMC steps executed

* snapshots_globals.TOF_header_array:
    List of names (strings) for each elementary process type. For example, with
    four process types 'F1p0', 'R1p0', 'F2p0', and 'R2p0', this would be

      ['F1p0', 'R1p0', 'F2p0', 'R2p0']

    Note that these are averaged over all sites and cells in the simulation box.

* snapshots_globals.TOF_data_list:
    List of TOF values (floating point) in the same order as TOF_header_array.
    For example, processes 'F1p0', 'R1p0', 'F2p0', and 'R2p0' might have
    observed event frequencies

      [1.2, 3.4, 5.6, 7.8]

* snapshots.do_snapshots(sps, tps, n_snapshots):
    Function to execute an arbitrary number of 'snapshots' (series of individual
    KMC steps collected together for statistical sampling). It has three
    arguments:

      sps: the integer number of KMC steps per snapshot;
      tps: the maximum time allowed to elapse in a snapshot (optional);
      n_snapshots: the integer number of snapshots to be executed during a
        single call to do_snapshots.

    This function will run a series of n_snapshots of sps individual KMC steps
    each if tps is not specified. If tps is specified, it will run each of the
    n_snapshots snapshots until either sps KMC steps have been executed or tps
    seconds of simulation time have elapsed, whichever occurs first (note that
    sps and tps are reset for each snapshot in the series). It returns no
    arguments, but the state of the lattice is evolved, the simulation clock and
    number of steps are updated, process rates are calculated, and any other
    book-keeping is done. It updates the following snapshots_globals variables
    that are used by the throttling code:

      snapshots_globals.kmc_time
      snapshots_globals.steps_so_far
      snapshots_globals.TOF_data_list

  * export_import_library.module_export_import(save_file, load_file, module):
      A custom class to facilitate reading and writing global module variables
      stored on disk. It has two methods: one for reading (load_params()) and
      one for writing (save_params()). The constructor function has three
      arguments: the name (a string) of the file in which the module data should
      be saved, the name (a string) of the file from which the module data
      should be read, and the Python module object itself. It returns an object
      which contains an imported module and the associated read/write filenames.
      This class is distributed with the throttling algorithm, so there is no
      need to revise it unless a different disk format is desired.

--------------------------------------------------------------------------------

         Part III: Suggested Protocol for Setting Throttling Parameters

We have developed a procedure for setting the throttling parameters. This
protocol is approximate but based on our experience with the throttling code. It
is intended to provide some guidelines for obtaining reliable sampling of the
rare events that control the system evolution in a reasonable amount of wall
time without distorting the overall system dynamics. Nevertheless, these
guidelines are just that: guidelines. Feel free to experiment (carefully!) with
the throttling parameters if you need to get better sampling, faster
performance, etc.

  1.  Run a simulation without throttling to determine number of KMC steps
      executed per unit wall time (KMC_step_rate).
  2.  Estimate rate of predicted FRP (eFRP_EF) or desired simulation time
      resolution (delta_t_target).
  3.  Determine the achievable upper bound on the number of executed throttled
      KMC steps (NSteps_achievable) in a given period of wall time (t_wall).
      Then

        NSteps_achievable = t_wall * KMC_step_rate

  4.  Set the desired ending simulation time (cutoff_time).
  5.  Estimate the average simulation time increment per KMC step
      (KMC_step_delta_t) that will enable the simulation of the desired
      simulation time (cutoff_time) within the achievable number of KMC steps
      (NSteps_achievable).

        KMC_step_delta_t = cutoff_time / NSteps_achievable

  6.  Determine the fastest rate that will give the needed simulation time per
      step using the variable step size method. The fastest rate (EF_cap) for a
      simulation cell with NSites individual sites is then

        EF_cap = 1 / (KMC_step_delta_t * NSites)

  7.  If using a predicted FRP, the floor rate for FFPs is

        FFP_floor = eFRP_EF * NSites

      If using a desired time resolution, the floor rate is based on the
      reciprocal of the desired time resolution

        FFP_floor = (1 / delta_t_target) * NSites

      These two methods can be represented using a single characteristic
      transition rate (characteristic_EF) instead

        FFP_floor = characteristic_EF * NSites

  8.  Determine EF_range_fast_requested from the floor rate and the maximum allowed rate

        EF_range_fast_requested = EF_cap / FFP_floor

  9.  Set the desired number of observed FRP events per snapshot
      (oFRP_events_target) or the desired number of time increments per
      snapshot (n_time_steps_target). For example, 10 is a reasonable lower
      bound for both. As with the floor, these can be thought of as
      characteristic events (either the execution of the FRP or the passage of
      the desired amount of time).
 10.  Set KMC steps per snapshot (sps). If using the FRP method,

        sps = EF_range_fast_requested * NSites * oFRP_events_target

      If using the time resolution method,

        sps = EF_range_fast_requested * NSites * n_time_steps_target

      These have the parallel structure

        sps = EF_range_fast_requested * NSites * n_characteristic_events_target

      where n_characteristic_events_target is the target number of
      characteristic events (either FRP execution or time step increments).

 --------------------------------------------------------------------------------

    Part IV: Regularization
	
At the moment,  the code has a primitive regularization code
 which puts a roof on what a rate constant is allowed to achieve.
 we recommend only using the  regularization if necessary.
 it can distort the selectivity, and it slows down the code.
 the slowdown is actually because kmcos updates *all* rate constants
 even if only one needs to be updated. So this slowdown is not
 actually due to the throttling module.
 One thing to note  it is that the the throttling code
 calculates ptEFs from uEFs. So if a snapshot used regularized
 rate constants, the oEFs and thus uEFs from that (regularized) snapshot will 
 result in ptEFs with the regularization built in.
 Thus,  if one snapshot has regularization,  it is expected that the next one will also.
 deviation from this would cause throttling inaccuracy.
 In principle, gradual regularization (and unregularization) would
 be the ideal thing, but is not  the situation in the current  primitive regularization.
