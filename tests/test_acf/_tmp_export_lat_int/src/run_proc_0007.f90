module run_proc_0007
use kind_values
use nli_0000
use nli_0001
use nli_0002
use nli_0003
use nli_0004
use nli_0005
use nli_0006
use nli_0007
use nli_0008
use nli_0009
use nli_0010
use nli_0011
use proclist_constants
implicit none
contains
subroutine run_proc_b_1_a_2(cell)

    integer(kind=iint), dimension(4), intent(in) :: cell

    ! disable processes that have to be disabled
    call del_proc(nli_a_1_a_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_a_1_b_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_a_2_a_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_a_2_b_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_a_2_b_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_b_1_a_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_b_1_a_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_b_1_b_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_b_2_a_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call del_proc(nli_b_2_b_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))

    ! update lattice
    call replace_species(cell + (/0, 0, 0, default_b_1/), ion, empty)
    call replace_species(cell + (/0, 0, 0, default_a_2/), empty, ion)

    ! enable processes that have to be enabled
    call add_proc(nli_a_1_a_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_a_1_b_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_a_2_a_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_a_2_b_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_a_2_b_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_b_1_a_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_b_1_a_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_b_1_b_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_b_2_a_2(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))
    call add_proc(nli_b_2_b_1(cell + (/+0, +0, +0, 0/)), cell + (/+0, +0, +0, 1/))

end subroutine run_proc_b_1_a_2

end module
