module run_proc_0006

use kind_values
use lattice
use proclist_pars

implicit none
contains

subroutine run_proc_A_desorption(cell)

    integer(kind=iint), dimension(4), intent(in) :: cell


! Disable processes

    if(can_do(AB_react_down,cell + (/ 0, 1, 0, 1/))) then
        call del_proc(AB_react_down,cell + (/ 0, 1, 0, 1/))
    end if
    if(can_do(AB_react_down,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(AB_react_down,cell + (/ 0, 0, 0, 1/))
    end if
    if(can_do(AB_react_left,cell + (/ 1, 0, 0, 1/))) then
        call del_proc(AB_react_left,cell + (/ 1, 0, 0, 1/))
    end if
    if(can_do(AB_react_left,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(AB_react_left,cell + (/ 0, 0, 0, 1/))
    end if
    if(can_do(AB_react_right,cell + (/ -1, 0, 0, 1/))) then
        call del_proc(AB_react_right,cell + (/ -1, 0, 0, 1/))
    end if
    if(can_do(AB_react_right,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(AB_react_right,cell + (/ 0, 0, 0, 1/))
    end if
    if(can_do(AB_react_up,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(AB_react_up,cell + (/ 0, 0, 0, 1/))
    end if
    if(can_do(AB_react_up,cell + (/ 0, -1, 0, 1/))) then
        call del_proc(AB_react_up,cell + (/ 0, -1, 0, 1/))
    end if
    if(can_do(A_desorption,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(A_desorption,cell + (/ 0, 0, 0, 1/))
    end if
    if(can_do(B_desorption,cell + (/ 0, 0, 0, 1/))) then
        call del_proc(B_desorption,cell + (/ 0, 0, 0, 1/))
    end if

! Update the lattice
    call replace_species(cell + (/0, 0, 0, default_a/),A,empty)

! Update rate constants


! Enable processes

    call add_proc(A_adsorption, cell + (/ 0, 0, 0, 1/), gr_A_adsorption(cell + (/ 0, 0, 0, 0/)))
    call add_proc(B_adsorption, cell + (/ 0, 0, 0, 1/), gr_B_adsorption(cell + (/ 0, 0, 0, 0/)))

end subroutine run_proc_A_desorption

end module run_proc_0006
