module nli_0001
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_CO_desorption(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_CO_desorption

    select case(get_species(cell + (/0, 0, 0, simple_cubic_hollow/)))
      case default
        nli_CO_desorption = 0; return
      case(CO)
        nli_CO_desorption = CO_desorption; return
    end select

end function nli_CO_desorption

end module
