module run_proc_0002
use kind_values
use nli_0000
use nli_0001
use nli_0002
use nli_0003
use nli_0004
use nli_0005
use nli_0006
use nli_0007
use proclist_constants
implicit none
contains
subroutine run_proc_AB_react_right(cell)

    integer(kind=iint), dimension(4), intent(in) :: cell

    ! disable processes that have to be disabled
    call del_proc(nli_AB_react_down(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_AB_react_down(cell + (/+0, +1, +0, 0/)), cell + (/+0, +1, +0, 1/))
    call del_proc(nli_AB_react_down(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call del_proc(nli_AB_react_down(cell + (/+1, +1, +0, 0/)), cell + (/+1, +1, +0, 1/))
    call del_proc(nli_AB_react_left(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_AB_react_left(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call del_proc(nli_AB_react_left(cell + (/+2, +0, +0, 0/)), cell + (/+2, +0, +0, 1/))
    call del_proc(nli_AB_react_right(cell + (/-1, +0, +0, 0/)), cell + (/-1, +0, +0, 1/))
    call del_proc(nli_AB_react_right(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_AB_react_right(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call del_proc(nli_AB_react_up(cell + (/+0, -1, +0, 0/)), cell + (/+0, -1, +0, 1/))
    call del_proc(nli_AB_react_up(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_AB_react_up(cell + (/+1, -1, +0, 0/)), cell + (/+1, -1, +0, 1/))
    call del_proc(nli_AB_react_up(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call del_proc(nli_A_adsorption(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_A_adsorption(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call del_proc(nli_A_desorption(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_A_desorption(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call del_proc(nli_B_adsorption(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_B_adsorption(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call del_proc(nli_B_desorption(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_B_desorption(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))

    ! update lattice
    call replace_species(cell + (/0, 0, 0, default_a/), A, empty)
    call replace_species(cell + (/1, 0, 0, default_a/), B, empty)

    ! enable processes that have to be enabled
    call add_proc(nli_AB_react_down(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_AB_react_down(cell + (/+0, +1, +0, 0/)), cell + (/+0, +1, +0, 1/))
    call add_proc(nli_AB_react_down(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call add_proc(nli_AB_react_down(cell + (/+1, +1, +0, 0/)), cell + (/+1, +1, +0, 1/))
    call add_proc(nli_AB_react_left(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_AB_react_left(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call add_proc(nli_AB_react_left(cell + (/+2, +0, +0, 0/)), cell + (/+2, +0, +0, 1/))
    call add_proc(nli_AB_react_right(cell + (/-1, +0, +0, 0/)), cell + (/-1, +0, +0, 1/))
    call add_proc(nli_AB_react_right(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_AB_react_right(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call add_proc(nli_AB_react_up(cell + (/+0, -1, +0, 0/)), cell + (/+0, -1, +0, 1/))
    call add_proc(nli_AB_react_up(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_AB_react_up(cell + (/+1, -1, +0, 0/)), cell + (/+1, -1, +0, 1/))
    call add_proc(nli_AB_react_up(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call add_proc(nli_A_adsorption(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_A_adsorption(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call add_proc(nli_A_desorption(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_A_desorption(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call add_proc(nli_B_adsorption(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_B_adsorption(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))
    call add_proc(nli_B_desorption(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_B_desorption(cell + (/+1, +0, +0, 0/)), cell + (/+1, +0, +0, 1/))

end subroutine run_proc_AB_react_right

end module
