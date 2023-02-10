module nli_0002
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_exc_right_down(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_exc_right_down

    select case(get_species(cell + (/0, 0, 0, default_a/)))
      case default
        nli_exc_right_down = 0; return
      case(Au)
        select case(get_species(cell + (/1, -1, 0, default_a/)))
          case default
            nli_exc_right_down = 0; return
          case(empty)
            nli_exc_right_down = exc_right_down; return
        end select
    end select

end function nli_exc_right_down

end module
