module nli_0005
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_a_2_b_2(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_a_2_b_2

    select case(get_species(cell + (/0, 0, 0, default_a_2/)))
      case default
        nli_a_2_b_2 = 0; return
      case(ion)
        select case(get_species(cell + (/0, 0, 0, default_b_2/)))
          case default
            nli_a_2_b_2 = 0; return
          case(empty)
            nli_a_2_b_2 = a_2_b_2; return
        end select
    end select

end function nli_a_2_b_2

end module
