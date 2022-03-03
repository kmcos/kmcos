Entry point module for the command-line
   interface. The kmcos executable should be
   on the program path, import this modules
   main function and run it.

   To call kmcos command as you would from the shell,
   use ::

       kmcos.cli.main('...')

   Every command can be shortened as long as it is non-ambiguous, e.g. ::


    kmcos ex <xml-file>

   instead of ::

    kmcos export <xml-file>


   etc.

List of commands
^^^^^^^^^^^^^^^^



``kmcos benchmark``
    Run 1 mio. kMC steps on model in current directory
    and report runtime.


``kmcos build``
    Build kmc_model.so from \*f90 files in the
    current directory.

    Additional Parameters ::
        -d/--debug
            Turn on assertion statements in F90 code

        -n/--no-compiler-optimization
            Do not send optimizing flags to compiler.


``kmcos edit <xml-file> (deprecated)``
    Open the kmcos xml-file in a GUI to edit
    the model.


``kmcos export <xml-file> [<export-path>]``
    Take a kmcos xml-file and export all generated
    source code to the export-path. There try to
    build the kmc_model.so.

    Additional Parameters ::

        -s/--source-only
            Export source only and don't build binary

        -b/--backend (local_smart|lat_int)
            Choose backend. Default is "local_smart".
            lat_int is EXPERIMENTAL and not made
            for production, yet.

        -d/--debug
            Turn on assertion statements in F90 code.
            (Only active in compile step)

           --acf
            Build the modules base_acf.f90 and proclist_acf.f90. Default is false.
            This both modules contain functions to calculate ACF (autocorrelation function) and MSD (mean squared displacement).

        -n/--no-compiler-optimization
            Do not send optimizing flags to compiler.


``kmcos help <command>``
    Print usage information for the given command.


``kmcos help all``
    Display documentation for all commands.


``kmcos import <xml-file>``
    Take a kmcos xml-file and open an ipython shell
    with the project_tree imported as kmc_model.


``kmcos rebuild``
    Export code and rebuild binary module from XML
    information included in kmc_settings.py in
    current directory.

    Additional Parameters ::
        -d/--debug
            Turn on assertion statements in F90 code


``kmcos run``
    Open an interactive shell and create a KMC_Model in it
               run == shell


``kmcos settings-export <xml-file> [<export-path>]``
    Take a kmcos xml-file and export kmc_settings.py
    to the export-path.


``kmcos shell``
    Open an interactive shell and create a KMC_Model in it
               run == shell


``kmcos version``
    Print version number and exit.


``kmcos view``
    Take a kmc_model.so and kmc_settings.py in the
    same directory and start to simulate the
    model visually.

    Additional Parameters ::
        -v/--steps-per-frame <number>
            Number of steps per frame



``kmcos xml``
    Print xml representation of model to stdout
