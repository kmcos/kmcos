module nli_0000
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_CO_adsorption(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_CO_adsorption

    select case(get_species(cell + (/0, 0, 0, simple_cubic_hollow1/)))
      case default
        nli_CO_adsorption = 0; return
      case(empty)
        nli_CO_adsorption = CO_adsorption; return
    end select

end function nli_CO_adsorption

end module
