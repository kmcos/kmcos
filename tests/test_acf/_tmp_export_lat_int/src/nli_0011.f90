module nli_0011
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_b_2_b_1(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_b_2_b_1

    select case(get_species(cell + (/0, 0, 0, default_b_2/)))
      case default
        nli_b_2_b_1 = 0; return
      case(ion)
        select case(get_species(cell + (/0, 0, 0, default_b_1/)))
          case default
            nli_b_2_b_1 = 0; return
          case(empty)
            nli_b_2_b_1 = b_2_b_1; return
        end select
    end select

end function nli_b_2_b_1

end module
