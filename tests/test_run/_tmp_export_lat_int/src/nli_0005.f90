module nli_0005
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_A_desorption(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_A_desorption

    select case(get_species(cell + (/0, 0, 0, default_a/)))
      case default
        nli_A_desorption = 0; return
      case(A)
        nli_A_desorption = A_desorption; return
    end select

end function nli_A_desorption

end module
