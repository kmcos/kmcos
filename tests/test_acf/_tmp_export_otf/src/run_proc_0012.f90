module run_proc_0012

use kind_values
use lattice
use proclist_pars

implicit none
contains

subroutine run_proc_b_2_b_1(cell)

    integer(kind=iint), dimension(4), intent(in) :: cell


! Disable processes

    if(can_do(a_1_b_1,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(a_1_b_1,cell + (/ 0, 0, 0, 1/))
    end if
    if(can_do(a_2_b_1,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(a_2_b_1,cell + (/ 0, 0, 0, 1/))
    end if
    if(can_do(b_2_a_1,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(b_2_a_1,cell + (/ 0, 0, 0, 1/))
    end if
    if(can_do(b_2_a_2,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(b_2_a_2,cell + (/ 0, 0, 0, 1/))
    end if
    if(can_do(b_2_b_1,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(b_2_b_1,cell + (/ 0, 0, 0, 1/))
    end if

! Update the lattice
    call replace_species(cell + (/0, 0, 0, default_b_1/),empty,ion)
    call replace_species(cell + (/0, 0, 0, default_b_2/),ion,empty)

! Update rate constants


! Enable processes

    call add_proc(b_1_b_2, cell + (/ 0, 0, 0, 1/), gr_b_1_b_2(cell + (/ 0, 0, 0, 0/)))
    select case(get_species(cell + (/0, 0, 0, default_a_1/)))
    case(empty)
        call add_proc(b_1_a_1, cell + (/ 0, 0, 0, 1/), gr_b_1_a_1(cell + (/ 0, 0, 0, 0/)))
    case(ion)
        call add_proc(a_1_b_2, cell + (/ 0, 0, 0, 1/), gr_a_1_b_2(cell + (/ 0, 0, 0, 0/)))
    end select

    select case(get_species(cell + (/0, 0, 0, default_a_2/)))
    case(empty)
        call add_proc(b_1_a_2, cell + (/ 0, 0, 0, 1/), gr_b_1_a_2(cell + (/ 0, 0, 0, 0/)))
    case(ion)
        call add_proc(a_2_b_2, cell + (/ 0, 0, 0, 1/), gr_a_2_b_2(cell + (/ 0, 0, 0, 0/)))
    end select


end subroutine run_proc_b_2_b_1

end module run_proc_0012
