module nli_0006
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_B_adsorption(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_B_adsorption

    select case(get_species(cell + (/0, 0, 0, default_a/)))
      case default
        nli_B_adsorption = 0; return
      case(empty)
        nli_B_adsorption = B_adsorption; return
    end select

end function nli_B_adsorption

end module
