module nli_0002
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_AB_react_right(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_AB_react_right

    select case(get_species(cell + (/0, 0, 0, default_a/)))
      case default
        nli_AB_react_right = 0; return
      case(A)
        select case(get_species(cell + (/1, 0, 0, default_a/)))
          case default
            nli_AB_react_right = 0; return
          case(B)
            nli_AB_react_right = AB_react_right; return
        end select
    end select

end function nli_AB_react_right

end module
