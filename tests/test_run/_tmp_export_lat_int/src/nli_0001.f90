module nli_0001
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_AB_react_left(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_AB_react_left

    select case(get_species(cell + (/-1, 0, 0, default_a/)))
      case default
        nli_AB_react_left = 0; return
      case(B)
        select case(get_species(cell + (/0, 0, 0, default_a/)))
          case default
            nli_AB_react_left = 0; return
          case(A)
            nli_AB_react_left = AB_react_left; return
        end select
    end select

end function nli_AB_react_left

end module
