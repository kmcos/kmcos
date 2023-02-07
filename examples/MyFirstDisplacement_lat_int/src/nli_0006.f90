module nli_0006
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_hop_right(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_hop_right

    select case(get_species(cell + (/0, 0, 0, default_a/)))
      case default
        nli_hop_right = 0; return
      case(Au)
        select case(get_species(cell + (/1, 0, 0, default_a/)))
          case default
            nli_hop_right = 0; return
          case(empty)
            nli_hop_right = hop_right; return
        end select
    end select

end function nli_hop_right

end module
