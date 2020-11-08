module nli_0004
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_A_adsorption(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_A_adsorption

    select case(get_species(cell + (/0, 0, 0, default_a/)))
      case default
        nli_A_adsorption = 0; return
      case(empty)
        nli_A_adsorption = A_adsorption; return
    end select

end function nli_A_adsorption

end module
