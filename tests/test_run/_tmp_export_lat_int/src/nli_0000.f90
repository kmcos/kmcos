module nli_0000
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_AB_react_down(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_AB_react_down

    select case(get_species(cell + (/0, -1, 0, default_a/)))
      case default
        nli_AB_react_down = 0; return
      case(B)
        select case(get_species(cell + (/0, 0, 0, default_a/)))
          case default
            nli_AB_react_down = 0; return
          case(A)
            nli_AB_react_down = AB_react_down; return
        end select
    end select

end function nli_AB_react_down

end module
