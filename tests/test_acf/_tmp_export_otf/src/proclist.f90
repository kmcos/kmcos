module proclist
use kind_values
use base, only: &
    update_accum_rate, &
    update_integ_rate, &
    reaccumulate_rates_matrix, &
    determine_procsite, &
    update_clocks, &
    avail_sites, &
    null_species, &
    increment_procstat

use lattice, only: &
    default, &
    default_a_1, &
    default_a_2, &
    default_b_1, &
    default_b_2, &
    allocate_system, &
    nr2lattice, &
    lattice2nr, &
    add_proc, &
    can_do, &
    set_rate_const, &
    replace_species, &
    del_proc, &
    reset_site, &
    system_size, &
    update_rates_matrix, &
    spuck, &
    get_species
use proclist_constants
use proclist_pars
use run_proc_0001
use run_proc_0002
use run_proc_0003
use run_proc_0004
use run_proc_0005
use run_proc_0006
use run_proc_0007
use run_proc_0008
use run_proc_0009
use run_proc_0010
use run_proc_0011
use run_proc_0012

implicit none
integer(kind=iint), parameter, public :: representation_length = 11
integer(kind=iint), public :: seed_size = 33
integer(kind=iint), public :: seed ! random seed
integer(kind=iint), public, dimension(:), allocatable :: seed_arr ! random seed


integer(kind=iint), parameter, public :: nr_of_proc = 12

character(len=3), parameter, public :: backend = "otf"

contains

subroutine do_kmc_steps(n)

!****f* proclist/do_kmc_steps
! FUNCTION
!    Performs ``n`` kMC step.
!    If one has to run many steps without evaluation
!    do_kmc_steps might perform a little better.
!    * first update clock
!    * then configuration sampling step
!    * last execute process
!
! ARGUMENTS
!
!    ``n`` : Number of steps to run
!******
    integer(kind=ilong), intent(in) :: n

    integer(kind=ilong) :: i
    real(kind=rsingle) :: ran_proc, ran_time, ran_site
    integer(kind=iint) :: nr_site, proc_nr

    do i = 1, n
    call random_number(ran_time)
    call random_number(ran_proc)
    call random_number(ran_site)
    call update_accum_rate
    call update_clocks(ran_time)

    call update_integ_rate
    call determine_procsite(ran_proc, ran_site, proc_nr, nr_site)
    call run_proc_nr(proc_nr, nr_site)
    enddo

end subroutine do_kmc_steps

subroutine do_kmc_step()

!****f* proclist/do_kmc_step
! FUNCTION
!    Performs exactly one kMC step.
!    *  first update clock
!    *  then configuration sampling step
!    *  last execute process
!
! ARGUMENTS
!
!    ``none``
!******
    real(kind=rsingle) :: ran_proc, ran_time, ran_site
    integer(kind=iint) :: nr_site, proc_nr

    call random_number(ran_time)
    call random_number(ran_proc)
    call random_number(ran_site)
    call update_accum_rate
    call update_clocks(ran_time)

    call update_integ_rate
    call determine_procsite(ran_proc, ran_site, proc_nr, nr_site)
    call run_proc_nr(proc_nr, nr_site)
end subroutine do_kmc_step

subroutine get_next_kmc_step(proc_nr, nr_site)

!****f* proclist/get_kmc_step
! FUNCTION
!    Determines next step without executing it.
!
! ARGUMENTS
!
!    ``none``
!******
    real(kind=rsingle) :: ran_proc, ran_time, ran_site
    integer(kind=iint), intent(out) :: nr_site, proc_nr

    call random_number(ran_time)
    call random_number(ran_proc)
    call random_number(ran_site)
    call update_accum_rate
    call determine_procsite(ran_proc, ran_time, proc_nr, nr_site)

end subroutine get_next_kmc_step

subroutine get_occupation(occupation)

!****f* proclist/get_occupation
! FUNCTION
!    Evaluate current lattice configuration and returns
!    the normalized occupation as matrix. Different species
!    run along the first axis and different sites run
!    along the second.
!
! ARGUMENTS
!
!    ``none``
!******
    ! nr_of_species = 2, spuck = 4
    real(kind=rdouble), dimension(0:1, 1:4), intent(out) :: occupation

    integer(kind=iint) :: i, j, k, nr, species

    occupation = 0

    do k = 0, system_size(3)-1
        do j = 0, system_size(2)-1
            do i = 0, system_size(1)-1
                do nr = 1, spuck
                    ! shift position by 1, so it can be accessed
                    ! more straightforwardly from f2py interface
                    species = get_species((/i,j,k,nr/))
                    if(species.ne.null_species) then
                    occupation(species, nr) = &
                        occupation(species, nr) + 1
                    endif
                end do
            end do
        end do
    end do

    occupation = occupation/real(system_size(1)*system_size(2)*system_size(3))
end subroutine get_occupation

subroutine init(input_system_size, system_name, layer, seed_in, no_banner)

!****f* proclist/init
! FUNCTION
!     Allocates the system and initializes all sites in the given
!     layer.
!
! ARGUMENTS
!
!    * ``input_system_size`` number of unit cell per axis.
!    * ``system_name`` identifier for reload file.
!    * ``layer`` initial layer.
!    * ``no_banner`` [optional] if True no copyright is issued.
!******
    integer(kind=iint), intent(in) :: layer, seed_in
    integer(kind=iint), dimension(2), intent(in) :: input_system_size

    character(len=400), intent(in) :: system_name

    logical, optional, intent(in) :: no_banner

    if (.not. no_banner) then
        print *, "+------------------------------------------------------------+"
        print *, "|                                                            |"
        print *, "| This kMC Model '2d_auto' was written by                    |"
        print *, "|                                                            |"
        print *, "|     Andreas Garhammer (andreas-garhammer@t-online.de)      |"
        print *, "|                                                            |"
        print *, "| and implemented with the help of kmos,                     |"
        print *, "| which is distributed under GNU/GPL Version 3               |"
        print *, "| (C) Max J. Hoffmann mjhoffmann@gmail.com                   |"
        print *, "|                                                            |"
        print *, "| kmos is distributed in the hope that it will be useful     |"
        print *, "| but WIHTOUT ANY WARRANTY; without even the implied         |"
        print *, "| waranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR     |"
        print *, "| PURPOSE. See the GNU General Public License for more       |"
        print *, "| details.                                                   |"
        print *, "|                                                            |"
        print *, "| If using kmos for a publication, attribution is            |"
        print *, "| greatly appreciated.                                       |"
        print *, "| Hoffmann, M. J., Matera, S., & Reuter, K. (2014).          |"
        print *, "| kmos: A lattice kinetic Monte Carlo framework.             |"
        print *, "| Computer Physics Communications, 185(7), 2138-2150.        |"
        print *, "|                                                            |"
        print *, "| Development http://mhoffman.github.org/kmos                |"
        print *, "| Documentation http://kmos.readthedocs.org                  |"
        print *, "| Reference http://dx.doi.org/10.1016/j.cpc.2014.04.003      |"
        print *, "|                                                            |"
        print *, "+------------------------------------------------------------+"
        print *, ""
        print *, ""
    endif
    call allocate_system(nr_of_proc, input_system_size, system_name)
    call initialize_state(layer, seed_in)
end subroutine init

subroutine initialize_state(layer, seed_in)

!****f* proclist/initialize_state
! FUNCTION
!    Initialize all sites and book-keeping array
!    for the given layer.
!
! ARGUMENTS
!
!    * ``layer`` integer representing layer
!******
    integer(kind=iint), intent(in) :: layer, seed_in

    integer(kind=iint) :: i, j, k, nr
    ! initialize random number generator
    allocate(seed_arr(seed_size))
    seed = seed_in
    seed_arr = seed
    call random_seed(size=seed_size)
    call random_seed(put=seed_arr)
    deallocate(seed_arr)
    do k = 0, system_size(3)-1
        do j = 0, system_size(2)-1
            do i = 0, system_size(1)-1
                do nr = 1, spuck
                    call reset_site((/i, j, k, nr/), null_species)
                end do
                select case(layer)
                case (default)
                    call replace_species((/i, j, k, default_a_1/), null_species, ion)
                    call replace_species((/i, j, k, default_a_2/), null_species, ion)
                    call replace_species((/i, j, k, default_b_1/), null_species, empty)
                    call replace_species((/i, j, k, default_b_2/), null_species, empty)
                end select
            end do
        end do
    end do

    do k = 0, system_size(3)-1
        do j = 0, system_size(2)-1
            do i = 0, system_size(1)-1
                call touchup_cell((/i, j, k, 0/))
            end do
        end do
    end do


end subroutine initialize_state

subroutine recalculate_rates_matrix()

    integer(kind=iint) :: i,j,k

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(a_1_a_2,(/ i, j, k, 1/))) then
                    call update_rates_matrix(a_1_a_2,(/ i, j, k, 1/),gr_a_1_a_2((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(a_1_b_1,(/ i, j, k, 1/))) then
                    call update_rates_matrix(a_1_b_1,(/ i, j, k, 1/),gr_a_1_b_1((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(a_1_b_2,(/ i, j, k, 1/))) then
                    call update_rates_matrix(a_1_b_2,(/ i, j, k, 1/),gr_a_1_b_2((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(a_2_a_1,(/ i, j, k, 1/))) then
                    call update_rates_matrix(a_2_a_1,(/ i, j, k, 1/),gr_a_2_a_1((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(a_2_b_1,(/ i, j, k, 1/))) then
                    call update_rates_matrix(a_2_b_1,(/ i, j, k, 1/),gr_a_2_b_1((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(a_2_b_2,(/ i, j, k, 1/))) then
                    call update_rates_matrix(a_2_b_2,(/ i, j, k, 1/),gr_a_2_b_2((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(b_1_a_1,(/ i, j, k, 1/))) then
                    call update_rates_matrix(b_1_a_1,(/ i, j, k, 1/),gr_b_1_a_1((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(b_1_a_2,(/ i, j, k, 1/))) then
                    call update_rates_matrix(b_1_a_2,(/ i, j, k, 1/),gr_b_1_a_2((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(b_1_b_2,(/ i, j, k, 1/))) then
                    call update_rates_matrix(b_1_b_2,(/ i, j, k, 1/),gr_b_1_b_2((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(b_2_a_1,(/ i, j, k, 1/))) then
                    call update_rates_matrix(b_2_a_1,(/ i, j, k, 1/),gr_b_2_a_1((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(b_2_a_2,(/ i, j, k, 1/))) then
                    call update_rates_matrix(b_2_a_2,(/ i, j, k, 1/),gr_b_2_a_2((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do

    do i=1, system_size(1)
        do j=1, system_size(2)
            do k=1, system_size(3)
                if(can_do(b_2_b_1,(/ i, j, k, 1/))) then
                    call update_rates_matrix(b_2_b_1,(/ i, j, k, 1/),gr_b_2_b_1((/ i, j, k, 0/)))
                end if
            end do
        end do
    end do


    call reaccumulate_rates_matrix()
end subroutine recalculate_rates_matrix
subroutine touchup_cell(cell)
    integer(kind=iint), intent(in), dimension(4) :: cell

    integer(kind=iint), dimension(4) :: site

    integer(kind=iint) :: proc_nr

    site = cell + (/0, 0, 0, 1/)
    do proc_nr = 1, nr_of_proc
        if(avail_sites(proc_nr, lattice2nr(site(1), site(2), site(3), site(4)) , 2).ne.0)then
            call del_proc(proc_nr, site)
        endif
    end do

    select case(get_species(cell + (/0, 0, 0, default_a_1/)))
    case(ion)
    case(empty)
    end select

    select case(get_species(cell + (/0, 0, 0, default_a_2/)))
    case(ion)
    case(empty)
    end select

    select case(get_species(cell + (/0, 0, 0, default_b_1/)))
    case(ion)
    case(empty)
    end select


end subroutine touchup_cell
subroutine run_proc_nr(proc, nr_cell)

!****f* proclist/run_proc_nr
! FUNCTION
!    Runs process ``proc`` on site ``nr_site``.
!
! ARGUMENTS
!
!    * ``proc`` integer representing the process number
!    * ``nr_site``  integer representing the site
!******
    integer(kind=iint), intent(in) :: proc
    integer(kind=iint), intent(in) :: nr_cell

    integer(kind=iint), dimension(4) :: cell

    call increment_procstat(proc)

    ! lsite = lattice_site, (vs. scalar site)
    cell = nr2lattice(nr_cell, :) + (/0, 0, 0, -1/)

    select case(proc)
    case(a_1_a_2)
        call run_proc_a_1_a_2(cell)

    case(a_1_b_1)
        call run_proc_a_1_b_1(cell)

    case(a_1_b_2)
        call run_proc_a_1_b_2(cell)

    case(a_2_a_1)
        call run_proc_a_2_a_1(cell)

    case(a_2_b_1)
        call run_proc_a_2_b_1(cell)

    case(a_2_b_2)
        call run_proc_a_2_b_2(cell)

    case(b_1_a_1)
        call run_proc_b_1_a_1(cell)

    case(b_1_a_2)
        call run_proc_b_1_a_2(cell)

    case(b_1_b_2)
        call run_proc_b_1_b_2(cell)

    case(b_2_a_1)
        call run_proc_b_2_a_1(cell)

    case(b_2_a_2)
        call run_proc_b_2_a_2(cell)

    case(b_2_b_1)
        call run_proc_b_2_b_1(cell)

    end select

end subroutine run_proc_nr

end module proclist
