module nli_0001
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_CO_desorption3(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_CO_desorption3

    select case(get_species(cell + (/0, 0, 0, simple_cubic_hollow3/)))
      case default
        nli_CO_desorption3 = 0; return
      case(CO)
        nli_CO_desorption3 = CO_desorption3; return
    end select

end function nli_CO_desorption3

end module
