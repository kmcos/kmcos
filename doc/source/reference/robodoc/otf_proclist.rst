proclist/do_kmc_step
----------------------------------------

    Performs exactly one kMC step.
    *  first update clock
    *  then configuration sampling step
    *  last execute process

    ``none``

proclist/do_kmc_steps
""""""""""""""""""""""""""""""""""""""""""""""""""
    Performs ``n`` kMC step.
    If one has to run many steps without evaluation
    do_kmc_steps might perform a little better.
    * first update clock
    * then configuration sampling step
    * last execute process

    ``n`` : Number of steps to run

proclist/do_kmc_steps_time
""""""""""""""""""""""""""""""""""""""""""""""""""
    Performs a variable number of KMC steps to try to match the requested
    simulation time as closely as possible without going over. This routine
    always performs at least one KMC step before terminating.
    * Determine the time step for the next process
    * If the time limit is not exceeded, update clocks, rates, execute process,
      etc.; otherwise, abort.
    Ideally we would use state(seed_size) but that was not working, so hardcoded size.

    ``t`` : Requested simulation time increment (input)
    ``n`` : Maximum number of steps to run (input)
    ``num_iter`` : the number of executed iterations (output)

proclist/get_next_kmc_step
""""""""""""""""""""""""""""""""""""""""""""""""""
    Determines next step without executing it.
    However, it changes the position in the random_number 
    sequence. The python function for
    model.get_next_kmc_step() should be used
    as it makes additional function calls
    to reset the random numbers.
    Calling model.proclist.get_next_kmc_step()
    is discouraged as that will call this subroutine
    directly and will not reset the random numbers.

    ``none``

proclist/get_occupation
""""""""""""""""""""""""""""""""""""""""""""""""""
    Evaluate current lattice configuration and returns
    the normalized occupation as matrix. Different species
    run along the first axis and different sites run
    along the second.

    ``none``

proclist/get_seed
""""""""""""""""""""""""""""""""""""""""""""""""""
   Function to retrieve the state of the random number generator to
    permit reproducible restart trajectories.

    * None

proclist/init
""""""""""""""""""""""""""""""""""""""""""""""""""
     Allocates the system and initializes all sites in the given
     layer.

    * ``input_system_size`` number of unit cell per axis.
    * ``system_name`` identifier for reload file.
    * ``layer`` initial layer.
    * ``no_banner`` [optional] if True no copyright is issued.

proclist/initialize_state
""""""""""""""""""""""""""""""""""""""""""""""""""
    Initialize all sites and book-keeping array
    for the given layer.

    * ``layer`` integer representing layer

proclist/put_seed
""""""""""""""""""""""""""""""""""""""""""""""""""
    Subroutine to set the state of the random number generator to
    permit reproducible restart trajectories.

    * ``state`` an array of integers with the state of the random number
    generator (input)

proclist/run_proc_nr
""""""""""""""""""""""""""""""""""""""""""""""""""
    Runs process ``proc`` on site ``nr_site``.

    * ``proc`` integer representing the process number
    * ``nr_site``  integer representing the site

proclist/seed_gen
""""""""""""""""""""""""""""""""""""""""""""""""""
    Function to transform a single number into a full set of integers
    required for initializing the random number generator.

    * ``sd`` an integer used to seed a simple random number generator
    used to generate additional integers for seeding the production random
    number generator (input)
